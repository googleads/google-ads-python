# Copyright 2020 Google LLC
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

from importlib import import_module
import logging.config

import grpc.experimental

from google.ads.google_ads import config, oauth2, util
from google.ads.google_ads.interceptors import (
    MetadataInterceptor,
    ExceptionInterceptor,
    LoggingInterceptor,
)


_logger = logging.getLogger(__name__)

_SERVICE_CLIENT_TEMPLATE = "{}Client"
_SERVICE_GRPC_TRANSPORT_TEMPLATE = "{}GrpcTransport"

_VALID_API_VERSIONS = ["v6", "v5", "v4", "v3"]
_DEFAULT_VERSION = _VALID_API_VERSIONS[0]

_GRPC_CHANNEL_OPTIONS = [
    ("grpc.max_metadata_size", 16 * 1024 * 1024),
    ("grpc.max_receive_message_length", 64 * 1024 * 1024),
]


unary_stream_single_threading_option = util.get_nested_attr(
    grpc, "experimental.ChannelOptions.SingleThreadedUnaryStream", None
)

if unary_stream_single_threading_option:
    _GRPC_CHANNEL_OPTIONS.append((unary_stream_single_threading_option, 1))


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
        return {
            "credentials": oauth2.get_credentials(config_data),
            "developer_token": config_data.get("developer_token"),
            "endpoint": config_data.get("endpoint"),
            "login_customer_id": config_data.get("login_customer_id"),
            "logging_config": config_data.get("logging"),
            "linked_customer_id": config_data.get("linked_customer_id"),
        }

    @classmethod
    def _get_api_services_by_version(cls, version):
        """Returns a module with all services and types for a given API version.

        Args:
            version: a str indicating the API version.

        Returns:
            A module containing all services and types for the a API version.
        """
        try:
            version_module = import_module(f"google.ads.google_ads.{version}")
        except ImportError:
            raise ValueError(
                'Specified Google Ads API version "{}" does not '
                'exist. Valid API versions are: "{}"'.format(
                    version, '", "'.join(_VALID_API_VERSIONS)
                )
            )
        return version_module

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
        if name.lower().endswith("pb2"):
            raise ValueError(
                f'Specified type "{name}" must be a class,' f" not a module"
            )

        try:
            type_classes = cls._get_api_services_by_version(version).types
            message_class = getattr(type_classes, name)
        except AttributeError:
            raise ValueError(
                f'Specified type "{name}" does not exist in '
                f"Google Ads API {version}"
            )
        return message_class()

    def __init__(
        self,
        credentials,
        developer_token,
        endpoint=None,
        login_customer_id=None,
        logging_config=None,
        linked_customer_id=None,
    ):
        """Initializer for the GoogleAdsClient.

        Args:
            credentials: a google.oauth2.credentials.Credentials instance.
            developer_token: a str developer token.
            endpoint: a str specifying an optional alternative API endpoint.
            login_customer_id: a str specifying a login customer ID.
            logging_config: a dict specifying logging config options.
            linked_customer_id: a str specifying a linked customer ID.
        """
        if logging_config:
            logging.config.dictConfig(logging_config)

        self.credentials = credentials
        self.developer_token = developer_token
        self.endpoint = endpoint
        self.login_customer_id = login_customer_id
        self.linked_customer_id = linked_customer_id

    def get_service(self, name, version=_DEFAULT_VERSION, interceptors=None):
        """Returns a service client instance for the specified service_name.

        Args:
            name: a str indicating the name of the service for which a
                service client is being retrieved; e.g. you may specify
                "CampaignService" to retrieve a CampaignServiceClient instance.
            version: a str indicating the version of the Google Ads API to be
                used.
            interceptors: an optional list of interceptors to include in
                requests. NOTE: this parameter is not intended for non-Google
                use and is not officially supported.

        Returns:
            A service client instance associated with the given service_name.

        Raises:
            AttributeError: If the specified name doesn't exist.
        """
        api_module = self._get_api_services_by_version(version)
        interceptors = interceptors or []

        try:
            service_client = getattr(
                api_module, _SERVICE_CLIENT_TEMPLATE.format(name)
            )
        except AttributeError:
            raise ValueError(
                'Specified service {}" does not exist in Google '
                "Ads API {}.".format(name, version)
            )

        try:
            service_transport_class = getattr(
                api_module, _SERVICE_GRPC_TRANSPORT_TEMPLATE.format(name)
            )
        except AttributeError:
            raise ValueError(
                "Grpc transport does not exist for the specified "
                'service "{}".'.format(name)
            )

        endpoint = (
            self.endpoint if self.endpoint else service_client.SERVICE_ADDRESS
        )

        channel = service_transport_class.create_channel(
            address=endpoint,
            credentials=self.credentials,
            options=_GRPC_CHANNEL_OPTIONS,
        )

        interceptors = interceptors + [
            MetadataInterceptor(
                self.developer_token,
                self.login_customer_id,
                self.linked_customer_id,
            ),
            LoggingInterceptor(_logger, version, endpoint),
            ExceptionInterceptor(version),
        ]

        channel = grpc.intercept_channel(channel, *interceptors)

        service_transport = service_transport_class(channel=channel)

        return service_client(transport=service_transport)
