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
import logging.config
import json
import grpc
from collections import namedtuple
from importlib import import_module

from google.protobuf.message import DecodeError

from google.ads.google_ads import config
from google.ads.google_ads import oauth2
from google.ads.google_ads.errors import GoogleAdsException

_logger = logging.getLogger(__name__)

_SERVICE_CLIENT_TEMPLATE = '%sClient'
_SERVICE_GRPC_TRANSPORT_TEMPLATE = '%sGrpcTransport'
_PROTO_TEMPLATE = '%s_pb2'
_VALID_API_VERSIONS = ['v2', 'v1']
_DEFAULT_VERSION = _VALID_API_VERSIONS[0]
_REQUEST_ID_KEY = 'request-id'
GRPC_CHANNEL_OPTIONS = [
    ('grpc.max_metadata_size', 16 * 1024 * 1024),
    ('grpc.max_receive_message_length', 64 * 1024 * 1024)]

class GoogleAdsClient(object):
    """Google Ads client used to configure settings and fetch services."""

    @classmethod
    def _get_client_kwargs(cls, config_data):
        """Converts configuration dict into kwargs required by the client.

        Args:
            config_data: a dict containing client configuration.

        Returns:
            A dict containing kwargs that will be provided to the
            GoogleAdsClient initializer.

        Raises:
            ValueError: If the configuration lacks a required field.
        """
        return {'credentials': oauth2.get_credentials(config_data),
                'developer_token': config_data.get('developer_token'),
                'endpoint': config_data.get('endpoint'),
                'login_customer_id': config_data.get('login_customer_id'),
                'logging_config': config_data.get('logging')}

    @classmethod
    def load_from_env(cls):
        """Creates a GoogleAdsClient with data stored in the env variables.

        Returns:
            A GoogleAdsClient initialized with the values specified in the
            env variables.

        Raises:
            ValueError: If the configuration lacks a required field.
        """
        config_data = config.load_from_env()
        kwargs = cls._get_client_kwargs(config_data)
        return cls(**kwargs)

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
        config_data = config.parse_yaml_document_to_dict(yaml_str)
        kwargs = cls._get_client_kwargs(config_data)
        return cls(**kwargs)

    @classmethod  
    def load_from_dict(cls, config_dict):
        """Creates a GoogleAdsClient with data stored in the config_dict.

        Args:
            config_dict: a dict consisting of configuration data used to
                initialize a GoogleAdsClient.

        Returns:
            A GoogleAdsClient initialized with the values specified in the
                dict.

        Raises:
            ValueError: If the configuration lacks a required field.
        """
        config_data = config.load_from_dict(config_dict)
        kwargs = cls._get_client_kwargs(config_data)
        return cls(**kwargs)

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
        config_data = config.load_from_yaml_file(path)
        kwargs = cls._get_client_kwargs(config_data)
        return cls(**kwargs)

    @classmethod
    def get_type(cls, name, version=_DEFAULT_VERSION):
        """Returns the specified common, enum, error, or resource type.

        Args:
            name: a str indicating the name of the type that is being retrieved;
                e.g. you may specify "CampaignOperation" to retrieve a
                CampaignOperation instance.
            version: a str indicating the the Google Ads API version to be used.

        Returns:
            A Message instance representing the desired type.

        Raises:
            AttributeError: If the type for the specified name doesn't exist
                in the given version.
        """
        try:
            message_type = getattr(_get_version(version).types, name)
        except AttributeError:
            raise ValueError('Specified type "{}" does not exist in Google Ads '
                             'API %s.'.format(name, version))
        return message_type()

    def __init__(self, credentials, developer_token, endpoint=None,
                 login_customer_id=None, logging_config=None):
        """Initializer for the GoogleAdsClient.

        Args:
            credentials: a google.oauth2.credentials.Credentials instance.
            developer_token: a str developer token.
            endpoint: a str specifying an optional alternative API endpoint.
            login_customer_id: a str specifying a login customer ID.
            logging_config: a dict specifying logging config options.
        """
        self.credentials = credentials
        self.developer_token = developer_token
        self.endpoint = endpoint
        self.login_customer_id = login_customer_id
        self.logging_config = logging_config

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
        api_module = _get_version(version)

        try:
            service_client = getattr(api_module,
                                     _SERVICE_CLIENT_TEMPLATE % name)
        except AttributeError:
            raise ValueError('Specified service "%s" does not exist in Google '
                             'Ads API %s.' % (name, version))

        try:
            service_transport_class = getattr(
                api_module, _SERVICE_GRPC_TRANSPORT_TEMPLATE % name)
        except AttributeError:
            raise ValueError('Grpc transport does not exist for the specified '
                             'service "%s".' % name)

        endpoint = (self.endpoint if self.endpoint
                    else service_client.SERVICE_ADDRESS)

        channel = service_transport_class.create_channel(
            address=endpoint,
            credentials=self.credentials,
            options=GRPC_CHANNEL_OPTIONS)

        channel = grpc.intercept_channel(
            channel,
            MetadataInterceptor(self.developer_token, self.login_customer_id),
            LoggingInterceptor(self.logging_config, endpoint),
            ExceptionInterceptor(version)
        )

        service_transport = service_transport_class(channel=channel)

        return service_client(transport=service_transport)


class ExceptionInterceptor(grpc.UnaryUnaryClientInterceptor):
    """An interceptor that wraps rpc exceptions."""

    # Codes that are retried upon by google.api_core.
    _RETRY_STATUS_CODES = (
        grpc.StatusCode.INTERNAL, grpc.StatusCode.RESOURCE_EXHAUSTED)

    def __init__(self, version=_DEFAULT_VERSION):
        """Initializes the ExceptionInterceptor

        Args:
            version: a str of the API version of the request.
        """
        self._version = version
        self._failure_key = (
            'google.ads.googleads.%s.errors.googleadsfailure-bin' % version)


    def _get_google_ads_failure(self, trailing_metadata):
        """Gets the Google Ads failure details if they exist.

        Args:
            trailing_metadata: a tuple of metadatum from the service response.

        Returns:
            A GoogleAdsFailure that describes how a GoogleAds API call failed.
            Returns None if either the trailing metadata of the request did not
            return the failure details, or if the GoogleAdsFailure fails to
            parse.
        """
        if trailing_metadata is not None:
            for kv in trailing_metadata:
                if kv[0] == self._failure_key:
                    try:
                        error_protos = import_module(
                            'google.ads.google_ads.%s.proto.errors' %
                                self._version)
                        ga_failure = error_protos.errors_pb2.GoogleAdsFailure()
                        ga_failure.ParseFromString(kv[1])
                        return ga_failure
                    except DecodeError:
                        return None

        return None

    def _handle_grpc_failure(self, response):
        """Attempts to convert failed responses to a GoogleAdsException object.

        Handles failed gRPC responses of by attempting to convert them
        to a more readable GoogleAdsException. Certain types of exceptions are
        not converted; if the object's trailing metadata does not indicate that
        it is a GoogleAdsException, or if it falls under a certain category of
        status code, (INTERNAL or RESOURCE_EXHAUSTED). See documentation for
        more information about gRPC status codes:
        https://github.com/grpc/grpc/blob/master/doc/statuscodes.md

        Args:
            response: a grpc.Call/grpc.Future instance.

        Raises:
            GoogleAdsException: If the exception's trailing metadata
                indicates that it is a GoogleAdsException.
            RpcError: If the exception's is a gRPC exception but the trailing
                metadata is empty or is not indicative of a GoogleAdsException,
                or if the exception has a status code of INTERNAL or
                RESOURCE_EXHAUSTED.
            Exception: If not a GoogleAdsException or RpcException the error
                will be raised as-is.
        """
        status_code = response.code()
        exception = response.exception()

        if status_code not in self._RETRY_STATUS_CODES:
            trailing_metadata = response.trailing_metadata()
            google_ads_failure = self._get_google_ads_failure(trailing_metadata)

            if google_ads_failure:
                request_id = _get_request_id_from_metadata(trailing_metadata)

                raise GoogleAdsException(exception, response,
                                         google_ads_failure, request_id)
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

        Returns:
            A grpc.Call instance representing a service response.

        Raises:
            GoogleAdsException: If the exception's trailing metadata
                indicates that it is a GoogleAdsException.
            RpcError: If the exception's trailing metadata is empty or is not
                indicative of a GoogleAdsException, or if the exception has a
                status code of INTERNAL or RESOURCE_EXHAUSTED.
        """
        response = continuation(client_call_details, request)
        exception = response.exception()

        if exception:
            self._handle_grpc_failure(response)
        else:
            return response


class LoggingInterceptor(grpc.UnaryUnaryClientInterceptor):
    """An interceptor that logs rpc requests and responses."""

    _FULL_REQUEST_LOG_LINE = ('Request\n-------\nMethod: {}\nHost: {}\n'
                              'Headers: {}\nRequest: {}\n\nResponse\n-------\n'
                              'Headers: {}\nResponse: {}\n')
    _FULL_FAULT_LOG_LINE = ('Request\n-------\nMethod: {}\nHost: {}\n'
                            'Headers: {}\nRequest: {}\n\nResponse\n-------\n'
                            'Headers: {}\nFault: {}\n')
    _SUMMARY_LOG_LINE = ('Request made: ClientCustomerId: {}, Host: {}, '
                         'Method: {}, RequestId: {}, IsFault: {}, '
                         'FaultMessage: {}')

    def __init__(self, logging_config=None, endpoint=None):
        """Initializer for the LoggingInterceptor.

        Args:
            logging_config: configuration dict for logging.
            endpoint: a str specifying an optional alternative API endpoint.
        """
        self.endpoint = endpoint
        if logging_config:
            logging.config.dictConfig(logging_config)

    def _get_trailing_metadata(self, response):
        """Retrieves trailing metadata from a response object.

        If the exception is a GoogleAdsException the trailing metadata will be
        on its error object, otherwise it will be on the response object.

        Returns:
            A tuple of metadatum representing response header key value pairs.

        Args:
            response: A grpc.Call/grpc.Future instance.
        """
        try:
            trailing_metadata = response.trailing_metadata()

            if not trailing_metadata:
                return _get_trailing_metadata_from_interceptor_exception(
                    response.exception())

            return trailing_metadata
        except AttributeError:
            return _get_trailing_metadata_from_interceptor_exception(
                response.exception())

    def _get_initial_metadata(self, client_call_details):
        """Retrieves the initial metadata from client_call_details.

        Returns an empty tuple if metadata isn't present on the
        client_call_details object.

        Returns:
            A tuple of metadatum representing request header key value pairs.

        Args:
            client_call_details: An instance of grpc.ClientCallDetails.
        """
        return getattr(client_call_details, 'metadata', tuple())

    def _get_call_method(self, client_call_details):
        """Retrieves the call method from client_call_details.

        Returns None if the method is not present on the client_call_details
        object.

        Returns:
            A str with the call method or None if it isn't present.

        Args:
            client_call_details: An instance of grpc.ClientCallDetails.
        """
        return getattr(client_call_details, 'method', None)

    def _get_customer_id(self, request):
        """Retrieves the customer_id from the grpc request.

        Returns None if a customer_id is not present on the request object.

        Returns:
            A str with the customer id from the request or None if it isn't
            present.

        Args:
            request: An instance of a request proto message.
        """
        return getattr(request, 'customer_id', None)

    def _parse_exception_to_str(self, exception):
        """Parses response exception object to str for logging.

        Returns:
            A str representing a exception from the API.

        Args:
            exception: A grpc.Call instance.
        """
        try:
            # If the exception is from the Google Ads API then the failure
            # attribute will be an instance of GoogleAdsFailure and can be
            # concatenated into a log string.
            return exception.failure
        except AttributeError:
            try:
                # if exception.failure isn't present then it's likely this is a
                # transport error with a .debug_error_string method and the
                # returned JSON string will need to be formatted.
                return _format_json_object(json.loads(
                    exception.debug_error_string()))
            except (AttributeError, ValueError):
                # if both attempts to retrieve serializable error data fail
                # then simply return an empty JSON string
                return '{}'

    def _get_fault_message(self, exception):
        """Retrieves a fault/error message from an exception object.

        Returns None if no error message can be found on the exception.

        Returns:
            A str with an error message or None if one cannot be found.

        Args:
            response: A grpc.Call/grpc.Future instance.
            exception: A grpc.Call instance.
        """
        try:
            return exception.failure.errors[0].message
        except AttributeError:
            try:
                return exception.details()
            except AttributeError:
                return None

    def _log_successful_request(self, method, customer_id, metadata_json,
                                request_id, request, trailing_metadata_json,
                                response):
        """Handles logging of a successful request.

        Args:
            method: The method of the request.
            customer_id: The customer ID associated with the request.
            metadata_json: A JSON str of initial_metadata.
            request_id: A unique ID for the request provided in the response.
            request: An instance of a request proto message.
            trailing_metadata_json: A JSON str of trailing_metadata.
            response: A grpc.Call/grpc.Future instance.
        """
        _logger.debug(self._FULL_REQUEST_LOG_LINE.format(method, self.endpoint,
                      metadata_json, request, trailing_metadata_json,
                      response.result()))

        _logger.info(self._SUMMARY_LOG_LINE.format(customer_id, self.endpoint,
                     method, request_id, False, None))

    def _log_failed_request(self, method, customer_id, metadata_json,
                            request_id, request, trailing_metadata_json,
                            response):
        """Handles logging of a failed request.

        Args:
            method: The method of the request.
            customer_id: The customer ID associated with the request.
            metadata_json: A JSON str of initial_metadata.
            request_id: A unique ID for the request provided in the response.
            request: An instance of a request proto message.
            trailing_metadata_json: A JSON str of trailing_metadata.
            response: A JSON str of the the response message.
        """
        exception_str = self._parse_exception_to_str(response.exception())
        fault_message = self._get_fault_message(response.exception())

        _logger.info(self._FULL_FAULT_LOG_LINE.format(method, self.endpoint,
                     metadata_json, request, trailing_metadata_json,
                     exception_str))

        _logger.warning(self._SUMMARY_LOG_LINE.format(customer_id, self.endpoint,
                        method, request_id, True, fault_message))

    def _log_request(self, client_call_details, request, response):
        """Handles logging all requests.

        Args:
            client_call_details: An instance of grpc.ClientCallDetails.
            request: An instance of a request proto message.
            response: A grpc.Call/grpc.Future instance.
        """
        method = self._get_call_method(client_call_details)
        customer_id = self._get_customer_id(request)
        initial_metadata = self._get_initial_metadata(client_call_details)
        initial_metadata_json = _parse_metadata_to_json(initial_metadata)
        trailing_metadata = self._get_trailing_metadata(response)
        request_id = _get_request_id_from_metadata(trailing_metadata)
        trailing_metadata_json = _parse_metadata_to_json(trailing_metadata)

        if response.exception():
            self._log_failed_request(method, customer_id, initial_metadata_json,
                                     request_id, request,
                                     trailing_metadata_json, response)
        else:
            self._log_successful_request(method, customer_id,
                                         initial_metadata_json, request_id,
                                         request, trailing_metadata_json,
                                         response)

    def intercept_unary_unary(self, continuation, client_call_details, request):
        """Intercepts and logs API interactions.

        Overrides abstract method defined in grpc.UnaryUnaryClientInterceptor.

        Returns:
            A grpc.Call/grpc.Future instance representing a service response.
        """
        response = continuation(client_call_details, request)

        if _logger.isEnabledFor(logging.WARNING):
            self._log_request(client_call_details, request, response)

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

        Returns:
            A grpc.Call/grpc.Future instance representing a service response.
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
    """A wrapper class for initializing a new ClientCallDetails instance."""
    pass


def _get_trailing_metadata_from_interceptor_exception(exception):
    """Retrieves trailing metadata from an exception object.

    Args:
        exception: an instance of grpc.Call.

    Returns:
        A tuple of trailing metadata key value pairs.
    """
    try:
        # GoogleAdsFailure exceptions will contain trailing metadata on the
        # error attribute.
        return exception.error.trailing_metadata()
    except AttributeError:
        try:
            # Transport failures, i.e. issues at the gRPC layer, will contain
            # trailing metadata on the exception iself.
            return exception.trailing_metadata()
        except AttributeError:
            # if trailing metadata is not found in either location then
            # return an empty tuple
            return tuple()


def _get_version(name):
    """Returns the given API version.

    Args:
        name: a str indicating the API version.

    Returns:
        A module associated with the given API version.
    """
    try:
        version = import_module('google.ads.google_ads.%s' % name)
    except ImportError:
        raise ValueError('Specified Google Ads API version "%s" does not '
                         'exist. Valid API versions are: "%s"' %
                                 (name, '", "'.join(_VALID_API_VERSIONS)))
    return version


def _format_json_object(obj):
    """Parses a serializable object into a consistently formatted JSON string.

    Returns:
        A str of formatted JSON serialized from the given object.

    Args:
        obj: an object or dict.
    """
    def default_serializer(value):
        if isinstance(value, bytes):
            return value.decode(errors='ignore')
        else:
            return None

    return str(json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False,
                          default=default_serializer, separators=(',', ': ')))


def _parse_metadata_to_json(metadata):
    """Parses metadata from gRPC request and response messages to a JSON str.

    Obscures the value for "developer-token".

    Args:
        metadata: a tuple of metadatum.
    """
    SENSITIVE_INFO_MASK = 'REDACTED'
    metadata_dict = {}

    if metadata is None:
        return '{}'

    for datum in metadata:
        key = datum[0]
        if key == 'developer-token':
            metadata_dict[key] = SENSITIVE_INFO_MASK
        else:
            value = datum[1]
            metadata_dict[key] = value

    return _format_json_object(metadata_dict)


def _get_request_id_from_metadata(trailing_metadata):
    """Gets the request ID for the Google Ads API request.

    Args:
        trailing_metadata: a tuple of metadatum from the service response.

    Returns:
        A str request ID associated with the Google Ads API request, or None
        if it doesn't exist.
    """
    for kv in trailing_metadata:
        if kv[0] == _REQUEST_ID_KEY:
            return kv[1]  # Return the found request ID.

    return None
