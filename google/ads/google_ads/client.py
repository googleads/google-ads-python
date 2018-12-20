# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""A client and common configurations for the Google Ads API."""

import logging
import os
import yaml
from collections import namedtuple

import google.api_core.grpc_helpers
import google.auth.transport.requests
import google.oauth2.credentials
import google.ads.google_ads.errors
from google.ads.google_ads.v0.proto.errors import errors_pb2
import grpc


_logger = logging.getLogger(__name__)

_REQUIRED_KEYS = ('client_id', 'client_secret', 'refresh_token',
                  'developer_token')
_SERVICE_CLIENT_TEMPLATE = '%sClient'
_SERVICE_GRPC_TRANSPORT_TEMPLATE = '%sGrpcTransport'
_PROTO_TEMPLATE = '%s_pb2'
_DEFAULT_TOKEN_URI = 'https://accounts.google.com/o/oauth2/token'
_DEFAULT_VERSION = 'v0'


class GoogleAdsClient(object):
    """Google Ads client used to configure settings and fetch services."""

    @classmethod
    def _get_client_kwargs_from_yaml(cls, yaml_str):
        """Utility function used to load client kwargs from YAML string.

        Args:
            yaml_str: a str containing client configuration in YAML format.

        Returns:
            A dict containing configuration data that will be provided to the
            GoogleAdsClient initializer as keyword arguments.

        Raises:
            ValueError: If the configuration lacks a required field.
        """
        config_data = yaml.safe_load(yaml_str) or {}

        if all(required_key in config_data for required_key in _REQUIRED_KEYS):
            credentials = google.oauth2.credentials.Credentials(
                None,
                refresh_token=config_data['refresh_token'],
                client_id=config_data['client_id'],
                client_secret=config_data['client_secret'],
                token_uri=_DEFAULT_TOKEN_URI)
            credentials.refresh(google.auth.transport.requests.Request())

            login_customer_id = config_data.get('login_customer_id')
            login_customer_id = str(
                login_customer_id) if login_customer_id else None

            return {'credentials': credentials,
                    'developer_token': config_data['developer_token'],
                    'endpoint': config_data.get('endpoint'),
                    'login_customer_id': login_customer_id}
        else:
            raise ValueError('A required field in the configuration data was'
                             'not found. The required fields are: %s'
                             % str(_REQUIRED_KEYS))

    @classmethod
    def get_type(cls, name, version=_DEFAULT_VERSION):
        """Returns the specified common, enum, error, or resource type.

        Args:
            name: a str indicating the name of the type that is being retrieved;
                e.g. you may specify "CampaignOperation" to retrieve a
                CampaignOperation instance.
            version: a str indicating the version of the Google Ads API to be
                used.

        Returns:
            A Message instance representing the desired type.

        Raises:
            AttributeError: If the type for the specified name doesn't exist
                in the given version.
        """
        try:
            message_type = getattr(_get_version(version).types, name)
        except AttributeError:
            raise ValueError('Specified type "%s" does not exist in Google Ads '
                             'API %s.' % (name, version))
        return message_type()

    @classmethod
    def load_from_string(cls, yaml_str):
        """Creates a GoogleAdsClient with data stored in the YAML string.

        Args:
            yaml_str: a str containing YAML configuration data used to
                initialize a GoogleAdsClient.

        Returns:
            A GoogleAdsClient initialized with the values specified in the
            string.

        Raises:
            ValueError: If the configuration lacks a required field.
        """
        return cls(**cls._get_client_kwargs_from_yaml(yaml_str))

    @classmethod
    def load_from_storage(cls, path=None):
        """Creates a GoogleAdsClient with data stored in the specified file.

        Args:
            path: a str indicating the path to a YAML file containing
                configuration data used to initialize a GoogleAdsClient.

        Returns:
            A GoogleAdsClient initialized with the values in the specified file.

        Raises:
            FileNotFoundError: If the specified configuration file doesn't
                exist.
            IOError: If the configuration file can't be loaded.
            ValueError: If the configuration file lacks a required field.
        """
        if path is None:
            path = os.path.join(os.path.expanduser('~'), 'google-ads.yaml')

        if not os.path.isabs(path):
            path = os.path.expanduser(path)

        with open(path, 'rb') as handle:
            yaml_str = handle.read()

        return cls.load_from_string(yaml_str)

    def __init__(self, credentials, developer_token, endpoint=None,
                 login_customer_id=None):
        """Initializer for the GoogleAdsClient.

        Args:
            credentials: a google.oauth2.credentials.Credentials instance.
            developer_token: a str developer token.
            endpoint: a str specifying an optional alternative API endpoint.
            login_customer_id: a str specifying a login customer ID.
        """
        _validate_login_customer_id(login_customer_id)

        self.credentials = credentials
        self.developer_token = developer_token
        self.endpoint = endpoint
        self.login_customer_id = login_customer_id

    def get_service(self, name, version=_DEFAULT_VERSION):
        """Returns a service client instance for the specified service_name.

        Args:
            name: a str indicating the name of the service for which a
                service client is being retrieved; e.g. you may specify
                "CampaignService" to retrieve a CampaignServiceClient instance.
            version: a str indicating the version of the Google Ads API to be
                used.

        Returns:
            A service client instance associated with the given service_name.

        Raises:
            AttributeError: If the specified name doesn't exist.
        """
        version = _get_version(version)

        try:
            service_client = getattr(version, _SERVICE_CLIENT_TEMPLATE % name)
        except AttributeError:
            raise ValueError('Specified service "%s" does not exist in Google '
                             'Ads API %s.' % (name, version))

        try:
            service_transport_class = getattr(
                version, _SERVICE_GRPC_TRANSPORT_TEMPLATE % name)
        except AttributeError:
            raise ValueError('Grpc transport does not exist for the specified '
                             'service "%s".' % name)

        channel = service_transport_class.create_channel(
            address=(self.endpoint if self.endpoint
                     else service_client.SERVICE_ADDRESS),
            credentials=self.credentials)

        channel = grpc.intercept_channel(
            channel,
            MetadataInterceptor(self.developer_token, self.login_customer_id),
            ExceptionInterceptor(),
        )

        service_transport = service_transport_class(channel=channel)

        return service_client(transport=service_transport)


class ExceptionInterceptor(grpc.UnaryUnaryClientInterceptor):
    """An interceptor that wraps rpc exceptions."""

    _FAILURE_KEY = 'google.ads.googleads.v0.errors.googleadsfailure-bin'
    _REQUEST_ID_KEY = 'request-id'
    # Codes that are retried upon by google.api_core.
    _RETRY_STATUS_CODES = (
        grpc.StatusCode.INTERNAL, grpc.StatusCode.RESOURCE_EXHAUSTED)

    def _get_google_ads_failure(self, trailing_metadata):
        """Gets the Google Ads failure details if they exist.

        Args:
            trailing_metadata:

        Returns:
            A GoogleAdsFailure that describes how a GoogleAds API call failed.
            Returns None if either the trailing metadata of the request did not
            return the failure details, or if the GoogleAdsFailure fails to
            parse.
        """
        for kv in trailing_metadata:
            if kv[0] == self._FAILURE_KEY:
                try:
                    ga_failure = errors_pb2.GoogleAdsFailure()
                    ga_failure.ParseFromString(kv[1])
                    return ga_failure
                except google.protobuf.message.DecodeError:
                    return None

    def _get_request_id(self, trailing_metadata):
        """Gets the request ID for the Google Ads API request.

        Args:
            trailing_metadata:

        Returns:
            A str request ID associated with the Google Ads API request, or None
            if it doesn't exist.
        """
        for kv in trailing_metadata:
            if kv[0] == self._REQUEST_ID_KEY:
                return kv[1]  # Return the found request ID.

        return None

    def _handle_grpc_exception(self, exception):
        """Handles gRPC exceptions of type RpcError by attempting to
           convert them to a more readable GoogleAdsException. Certain types of
           exceptions are not converted; if the object's trailing metadata does
           not indicate that it is a GoogleAdsException, or if it falls under
           a certain category of status code, (INTERNAL or RESOURCE_EXHAUSTED).
           See documentation for more information about gRPC status codes:
           https://github.com/grpc/grpc/blob/master/doc/statuscodes.md

        Args:
            exception: an exception of type RpcError.

        Raises:
            GoogleAdsException: If the exception's trailing metadata
                indicates that it is a GoogleAdsException.
            RpcError: If the exception's trailing metadata is empty or is not
                indicative of a GoogleAdsException, or if the exception has a
                status code of INTERNAL or RESOURCE_EXHAUSTED.
        """
        if exception._state.code not in self._RETRY_STATUS_CODES:
            trailing_metadata = exception.trailing_metadata()
            google_ads_failure = self._get_google_ads_failure(
                trailing_metadata)

            if google_ads_failure:
                request_id = self._get_request_id(trailing_metadata)

                raise google.ads.google_ads.errors.GoogleAdsException(
                    exception, exception, google_ads_failure, request_id)
            else:
                # Raise the original exception if not a GoogleAdsFailure.
                raise exception
        else:
            # Raise the original exception if error has status code
            # INTERNAL or RESOURCE_EXHAUSTED.
            raise exception

    def intercept_unary_unary(self, continuation, client_call_details, request):
        """Intercepts and wraps exceptions in the rpc response.

        Overrides abstract method defined in grpc.UnaryUnaryClientInterceptor.

        Raises:
            GoogleAdsException: If the exception's trailing metadata
                indicates that it is a GoogleAdsException.
            RpcError: If the exception's trailing metadata is empty or is not
                indicative of a GoogleAdsException, or if the exception has a
                status code of INTERNAL or RESOURCE_EXHAUSTED.
        """
        try:
            response = continuation(client_call_details, request)
        except grpc.RpcError as ex:
            self._handle_grpc_exception(ex)

        if response.exception():
            # Any exception raised within the continuation function that is not
            # an RpcError will be set on the response object and raised here.
            raise response.exception()

        return response


class LoggingInterceptor(grpc.UnaryUnaryClientInterceptor):
    """An interceptor that logs rpc requests and responses."""

    def intercept_unary_unary(self, continuation, client_call_details, request):
        """Intercepts and logs API interactions.

        Overrides abstract method defined in grpc.UnaryUnaryClientInterceptor.
        """
        _logger.debug('Method: "%s" called with Request: "%s"'
                      % (client_call_details.method, request))

        response = continuation(client_call_details, request)

        # TODO: Handle response here.

        return response


class MetadataInterceptor(grpc.UnaryUnaryClientInterceptor):
    """An interceptor that appends custom metadata to requests."""

    def __init__(self, developer_token, login_customer_id):
        self.developer_token_meta = ('developer-token', developer_token)
        self.login_customer_id_meta = (
            ('login-customer-id', login_customer_id) if login_customer_id
            else None)

    def _update_client_call_details_metadata(
            self, client_call_details, metadata):
        client_call_details = _ClientCallDetails(
            client_call_details.method, client_call_details.timeout, metadata,
            client_call_details.credentials)

        return client_call_details

    def intercept_unary_unary(self, continuation, client_call_details, request):
        """Intercepts and appends custom metadata.

        Overrides abstract method defined in grpc.UnaryUnaryClientInterceptor.
        """
        if client_call_details.metadata is None:
            metadata = []
        else:
            metadata = list(client_call_details.metadata)

        metadata.append(self.developer_token_meta)

        if self.login_customer_id_meta:
            metadata.append(self.login_customer_id_meta)

        client_call_details = self._update_client_call_details_metadata(
            client_call_details,
            metadata)

        return continuation(client_call_details, request)


class _ClientCallDetails(
        namedtuple(
            '_ClientCallDetails',
            ('method', 'timeout', 'metadata', 'credentials')),
        grpc.ClientCallDetails):
    """An wrapper class for initializing a new ClientCallDetails instance."""
    pass


def _get_version(name):
    """Returns the given API version.

    Args:
        name: a str indicating the API version.

    Returns:
        A module associated with the given API version.
    """
    try:
        version = getattr(google.ads.google_ads, name)
    except AttributeError:
        raise ValueError('Specified Google Ads API version "%s" does not exist.'
                         % name)
    return version


def _validate_login_customer_id(login_customer_id):
    """Validates a login customer ID.

    Args:
        login_customer_id: a str from config indicating a login customer ID.

    Raises:
        ValueError: If the login customer ID is not
        an int in the range 0 - 9999999999.
    """
    if login_customer_id is not None:
        if not login_customer_id.isdigit() or len(login_customer_id) != 10:
            raise ValueError('The specified login customer ID is invalid. '
                             'It must be a ten digit number represented '
                             'as a string, i.e. "1234567890"')
