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
import json
import grpc
from collections import namedtuple
from importlib import import_module

from google.ads.google_ads import config
from google.ads.google_ads import oauth2

from google.ads.google_ads.interceptors import MetadataInterceptor, \
    ExceptionInterceptor, LoggingInterceptor

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
        if logging_config:
            logging.config.dictConfig(logging_config)

        self.credentials = credentials
        self.developer_token = developer_token
        self.endpoint = endpoint
        self.login_customer_id = login_customer_id
        # self.logging_config = logging_config

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
            LoggingInterceptor(_logger, endpoint),
            ExceptionInterceptor(version)
        )

        service_transport = service_transport_class(channel=channel)

        return service_client(transport=service_transport)


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
