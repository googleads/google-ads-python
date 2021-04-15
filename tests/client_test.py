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
"""Tests for the Google Ads API client library."""

from importlib import import_module
from inspect import getmembers
import mock
import os
import pickle
from pyfakefs.fake_filesystem_unittest import TestCase as FileTestCase
import yaml

from proto.enums import ProtoEnumMeta

from google.ads.googleads import client as Client

latest_version = Client._DEFAULT_VERSION
valid_versions = Client._VALID_API_VERSIONS

services_path = f"google.ads.googleads.{latest_version}.services.services"
services = import_module(services_path)


class GoogleAdsClientTest(FileTestCase):
    """Tests for the google.ads.googleads.client.GoogleAdsClient class."""

    def _create_test_client(self, **kwargs):
        with mock.patch.object(
            Client.oauth2, "get_installed_app_credentials"
        ) as mock_credentials:
            mock_credentials_instance = mock_credentials.return_value
            mock_credentials_instance.refresh_token = self.refresh_token
            mock_credentials_instance.client_id = self.client_id
            mock_credentials_instance.client_secret = self.client_secret
            client = Client.GoogleAdsClient(
                mock_credentials_instance,
                self.developer_token,
                endpoint=kwargs.get("endpoint"),
                version=kwargs.get("version"),
                http_proxy=kwargs.get("http_proxy"),
            )
            return client

    def setUp(self):
        self.setUpPyfakefs()
        self.developer_token = "abc123"
        self.client_id = "client_id_123456789"
        self.client_secret = "client_secret_987654321"
        self.refresh_token = "refresh"
        self.login_customer_id = "1234567890"
        self.json_key_file_path = "/test/path/to/config.json"
        self.impersonated_email = "delegated@account.com"
        self.linked_customer_id = "0987654321"
        self.version = latest_version
        self.http_proxy = "https://localhost:8000"

    def test_get_client_kwargs_login_customer_id(self):
        config = {
            "developer_token": self.developer_token,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": self.refresh_token,
            "login_customer_id": self.login_customer_id,
            "linked_customer_id": self.linked_customer_id,
        }
        mock_credentials_instance = mock.Mock()

        with mock.patch.object(
            Client.oauth2,
            "get_installed_app_credentials",
            return_value=mock_credentials_instance,
        ):
            result = Client.GoogleAdsClient._get_client_kwargs(config)
            self.assertEqual(
                result,
                {
                    "credentials": mock_credentials_instance,
                    "developer_token": self.developer_token,
                    "endpoint": None,
                    "login_customer_id": self.login_customer_id,
                    "logging_config": None,
                    "linked_customer_id": self.linked_customer_id,
                    "http_proxy": None,
                },
            )

    def test_get_client_kwargs_login_customer_id_as_None(self):
        config = {
            "developer_token": self.developer_token,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": self.refresh_token,
            "login_customer_id": None,
        }
        mock_credentials_instance = mock.Mock()

        with mock.patch.object(
            Client.oauth2,
            "get_installed_app_credentials",
            return_value=mock_credentials_instance,
        ):
            result = Client.GoogleAdsClient._get_client_kwargs(config)
            self.assertEqual(
                result,
                {
                    "credentials": mock_credentials_instance,
                    "developer_token": self.developer_token,
                    "endpoint": None,
                    "login_customer_id": None,
                    "logging_config": None,
                    "linked_customer_id": None,
                    "http_proxy": None,
                },
            )

    def test_get_client_kwargs_linked_customer_id(self):
        config = {
            "developer_token": self.developer_token,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": self.refresh_token,
            "linked_customer_id": self.linked_customer_id,
        }
        mock_credentials_instance = mock.Mock()

        with mock.patch.object(
            Client.oauth2,
            "get_installed_app_credentials",
            return_value=mock_credentials_instance,
        ):
            result = Client.GoogleAdsClient._get_client_kwargs(config)
            self.assertEqual(
                result,
                {
                    "credentials": mock_credentials_instance,
                    "developer_token": self.developer_token,
                    "endpoint": None,
                    "login_customer_id": None,
                    "logging_config": None,
                    "linked_customer_id": self.linked_customer_id,
                    "http_proxy": None,
                },
            )

    def test_get_client_kwargs_linked_customer_id_as_none(self):
        config = {
            "developer_token": self.developer_token,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": self.refresh_token,
            "linked_customer_id": None,
        }
        mock_credentials_instance = mock.Mock()

        with mock.patch.object(
            Client.oauth2,
            "get_installed_app_credentials",
            return_value=mock_credentials_instance,
        ):
            result = Client.GoogleAdsClient._get_client_kwargs(config)
            self.assertEqual(
                result,
                {
                    "credentials": mock_credentials_instance,
                    "developer_token": self.developer_token,
                    "endpoint": None,
                    "linked_customer_id": None,
                    "logging_config": None,
                    "login_customer_id": None,
                    "http_proxy": None,
                },
            )

    def test_get_client_kwargs(self):
        config = {
            "developer_token": self.developer_token,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": self.refresh_token,
            "http_proxy": self.http_proxy,
        }
        mock_credentials_instance = mock.Mock()

        with mock.patch.object(
            Client.oauth2,
            "get_installed_app_credentials",
            return_value=mock_credentials_instance,
        ):
            result = Client.GoogleAdsClient._get_client_kwargs(config)
            self.assertEqual(
                result,
                {
                    "credentials": mock_credentials_instance,
                    "developer_token": self.developer_token,
                    "endpoint": None,
                    "login_customer_id": None,
                    "logging_config": None,
                    "linked_customer_id": None,
                    "http_proxy": self.http_proxy,
                },
            )

    def test_get_client_kwargs_custom_endpoint(self):
        endpoint = "alt.endpoint.com"
        config = {
            "developer_token": self.developer_token,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": self.refresh_token,
            "endpoint": endpoint,
        }
        mock_credentials_instance = mock.Mock()

        with mock.patch.object(
            Client.oauth2,
            "get_installed_app_credentials",
            return_value=mock_credentials_instance,
        ):
            result = Client.GoogleAdsClient._get_client_kwargs(config)
            self.assertEqual(
                result,
                {
                    "credentials": mock_credentials_instance,
                    "developer_token": self.developer_token,
                    "endpoint": endpoint,
                    "login_customer_id": None,
                    "logging_config": None,
                    "linked_customer_id": None,
                    "http_proxy": None,
                },
            )

    def test_load_from_env(self):
        mock_credentials_instance = mock.Mock()

        with mock.patch.object(
            Client.GoogleAdsClient, "__init__", return_value=None
        ) as mock_client_init, mock.patch.object(
            Client.oauth2,
            "get_installed_app_credentials",
            return_value=mock_credentials_instance,
        ) as mock_credentials, mock.patch.dict(
            os.environ,
            {
                "GOOGLE_ADS_DEVELOPER_TOKEN": self.developer_token,
                "GOOGLE_ADS_CLIENT_ID": self.client_id,
                "GOOGLE_ADS_CLIENT_SECRET": self.client_secret,
                "GOOGLE_ADS_REFRESH_TOKEN": self.refresh_token,
            },
        ) as mock_os_environ:
            Client.GoogleAdsClient.load_from_env()

            mock_client_init.assert_called_once_with(
                credentials=mock_credentials_instance,
                developer_token=self.developer_token,
                endpoint=None,
                login_customer_id=None,
                logging_config=None,
                linked_customer_id=None,
                version=None,
                http_proxy=None,
            )

    def test_load_from_env_versioned(self):
        mock_credentials_instance = mock.Mock()

        with mock.patch.object(
            Client.GoogleAdsClient, "__init__", return_value=None
        ) as mock_client_init, mock.patch.object(
            Client.oauth2,
            "get_installed_app_credentials",
            return_value=mock_credentials_instance,
        ) as mock_credentials, mock.patch.dict(
            os.environ,
            {
                "GOOGLE_ADS_DEVELOPER_TOKEN": self.developer_token,
                "GOOGLE_ADS_CLIENT_ID": self.client_id,
                "GOOGLE_ADS_CLIENT_SECRET": self.client_secret,
                "GOOGLE_ADS_REFRESH_TOKEN": self.refresh_token,
            },
        ) as mock_os_environ:
            Client.GoogleAdsClient.load_from_env(version="v4")

            mock_client_init.assert_called_once_with(
                credentials=mock_credentials_instance,
                developer_token=self.developer_token,
                endpoint=None,
                login_customer_id=None,
                logging_config=None,
                linked_customer_id=None,
                version="v4",
                http_proxy=None,
            )

    def test_load_from_dict(self):
        config = {
            "developer_token": self.developer_token,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": self.refresh_token,
        }
        mock_credentials_instance = mock.Mock()

        with mock.patch.object(
            Client.GoogleAdsClient, "__init__", return_value=None
        ) as mock_client_init, mock.patch.object(
            Client.oauth2,
            "get_installed_app_credentials",
            return_value=mock_credentials_instance,
        ) as mock_credentials:
            Client.GoogleAdsClient.load_from_dict(config)

            mock_client_init.assert_called_once_with(
                credentials=mock_credentials_instance,
                developer_token=self.developer_token,
                endpoint=None,
                login_customer_id=None,
                logging_config=None,
                linked_customer_id=None,
                version=None,
                http_proxy=None,
            )

    def test_load_from_dict_versioned(self):
        config = {
            "developer_token": self.developer_token,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": self.refresh_token,
        }
        mock_credentials_instance = mock.Mock()

        with mock.patch.object(
            Client.GoogleAdsClient, "__init__", return_value=None
        ) as mock_client_init, mock.patch.object(
            Client.oauth2,
            "get_installed_app_credentials",
            return_value=mock_credentials_instance,
        ) as mock_credentials:
            Client.GoogleAdsClient.load_from_dict(config, version="v4")

            mock_client_init.assert_called_once_with(
                credentials=mock_credentials_instance,
                developer_token=self.developer_token,
                endpoint=None,
                login_customer_id=None,
                logging_config=None,
                linked_customer_id=None,
                version="v4",
                http_proxy=None,
            )

    def test_load_from_string(self):
        config = {
            "developer_token": self.developer_token,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": self.refresh_token,
        }
        mock_credentials_instance = mock.Mock()

        with mock.patch.object(
            Client.GoogleAdsClient, "__init__", return_value=None
        ) as mock_client_init, mock.patch.object(
            Client.oauth2,
            "get_installed_app_credentials",
            return_value=mock_credentials_instance,
        ) as mock_credentials:
            Client.GoogleAdsClient.load_from_string(yaml.dump(config))

            mock_client_init.assert_called_once_with(
                credentials=mock_credentials_instance,
                developer_token=self.developer_token,
                endpoint=None,
                login_customer_id=None,
                logging_config=None,
                linked_customer_id=None,
                version=None,
                http_proxy=None,
            )

    def test_load_from_string_versioned(self):
        config = {
            "developer_token": self.developer_token,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": self.refresh_token,
        }
        mock_credentials_instance = mock.Mock()

        with mock.patch.object(
            Client.GoogleAdsClient, "__init__", return_value=None
        ) as mock_client_init, mock.patch.object(
            Client.oauth2,
            "get_installed_app_credentials",
            return_value=mock_credentials_instance,
        ) as mock_credentials:
            Client.GoogleAdsClient.load_from_string(
                yaml.dump(config), version="v4"
            )

            mock_client_init.assert_called_once_with(
                credentials=mock_credentials_instance,
                developer_token=self.developer_token,
                endpoint=None,
                login_customer_id=None,
                logging_config=None,
                linked_customer_id=None,
                version="v4",
                http_proxy=None,
            )

    def test_load_from_storage(self):
        config = {
            "developer_token": self.developer_token,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": self.refresh_token,
        }

        file_path = os.path.join(os.path.expanduser("~"), "google-ads.yaml")
        self.fs.create_file(file_path, contents=yaml.safe_dump(config))
        mock_credentials_instance = mock.Mock()

        with mock.patch.object(
            Client.GoogleAdsClient, "__init__", return_value=None
        ) as mock_client_init, mock.patch.object(
            Client.oauth2,
            "get_installed_app_credentials",
            return_value=mock_credentials_instance,
        ) as mock_credentials:
            Client.GoogleAdsClient.load_from_storage()
            mock_credentials.assert_called_once_with(
                config.get("client_id"),
                config.get("client_secret"),
                config.get("refresh_token"),
                http_proxy=None,
            )
            mock_client_init.assert_called_once_with(
                credentials=mock_credentials_instance,
                developer_token=self.developer_token,
                endpoint=None,
                login_customer_id=None,
                logging_config=None,
                linked_customer_id=None,
                version=None,
                http_proxy=None,
            )

    def test_load_from_storage_versioned(self):
        config = {
            "developer_token": self.developer_token,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": self.refresh_token,
        }

        file_path = os.path.join(os.path.expanduser("~"), "google-ads.yaml")
        self.fs.create_file(file_path, contents=yaml.safe_dump(config))
        mock_credentials_instance = mock.Mock()

        with mock.patch.object(
            Client.GoogleAdsClient, "__init__", return_value=None
        ) as mock_client_init, mock.patch.object(
            Client.oauth2,
            "get_installed_app_credentials",
            return_value=mock_credentials_instance,
        ) as mock_credentials:
            Client.GoogleAdsClient.load_from_storage(version="v4")
            mock_credentials.assert_called_once_with(
                config.get("client_id"),
                config.get("client_secret"),
                config.get("refresh_token"),
                http_proxy=None,
            )
            mock_client_init.assert_called_once_with(
                credentials=mock_credentials_instance,
                developer_token=self.developer_token,
                endpoint=None,
                login_customer_id=None,
                logging_config=None,
                linked_customer_id=None,
                version="v4",
                http_proxy=None,
            )

    def test_load_from_storage_login_cid_int(self):
        login_cid = 1234567890
        config = {
            "developer_token": self.developer_token,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": self.refresh_token,
            "login_customer_id": login_cid,
        }

        file_path = os.path.join(os.path.expanduser("~"), "google-ads.yaml")
        self.fs.create_file(file_path, contents=yaml.safe_dump(config))
        mock_credentials_instance = mock.Mock()

        with mock.patch.object(
            Client.GoogleAdsClient, "__init__", return_value=None
        ) as mock_client_init, mock.patch.object(
            Client.oauth2,
            "get_installed_app_credentials",
            return_value=mock_credentials_instance,
        ) as mock_credentials:
            Client.GoogleAdsClient.load_from_storage()
            mock_credentials.assert_called_once_with(
                config.get("client_id"),
                config.get("client_secret"),
                config.get("refresh_token"),
                http_proxy=None,
            )
            mock_client_init.assert_called_once_with(
                credentials=mock_credentials_instance,
                developer_token=self.developer_token,
                endpoint=None,
                login_customer_id=str(login_cid),
                logging_config=None,
                linked_customer_id=None,
                version=None,
                http_proxy=None,
            )

    def test_load_from_storage_custom_path(self):
        config = {
            "developer_token": self.developer_token,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": self.refresh_token,
        }

        file_path = "test/google-ads.yaml"
        self.fs.create_file(file_path, contents=yaml.safe_dump(config))
        mock_credentials_instance = mock.Mock()

        with mock.patch.object(
            Client.GoogleAdsClient, "__init__", return_value=None
        ) as mock_client_init, mock.patch.object(
            Client.oauth2,
            "get_installed_app_credentials",
            return_value=mock_credentials_instance,
        ):
            Client.GoogleAdsClient.load_from_storage(path=file_path)
            mock_client_init.assert_called_once_with(
                credentials=mock_credentials_instance,
                developer_token=self.developer_token,
                endpoint=None,
                login_customer_id=None,
                logging_config=None,
                linked_customer_id=None,
                version=None,
                http_proxy=None,
            )

    def test_load_from_storage_file_not_found(self):
        wrong_file_path = "test/wrong-google-ads.yaml"

        self.assertRaises(
            IOError,
            Client.GoogleAdsClient.load_from_storage,
            path=wrong_file_path,
        )

    def test_load_from_storage_required_config_missing(self):
        config = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": self.refresh_token,
        }

        file_path = "test/google-ads.yaml"
        self.fs.create_file(file_path, contents=yaml.safe_dump(config))

        self.assertRaises(
            ValueError, Client.GoogleAdsClient.load_from_storage, path=file_path
        )

    def test_load_from_storage_service_account_config(self):
        config = {
            "developer_token": self.developer_token,
            "json_key_file_path": self.json_key_file_path,
            "impersonated_email": self.impersonated_email,
        }

        file_path = os.path.join(os.path.expanduser("~"), "google-ads.yaml")
        self.fs.create_file(file_path, contents=yaml.safe_dump(config))
        mock_credentials_instance = mock.Mock()

        with mock.patch.object(
            Client.GoogleAdsClient, "__init__", return_value=None
        ) as mock_client_init, mock.patch.object(
            Client.oauth2,
            "get_service_account_credentials",
            return_value=mock_credentials_instance,
        ) as mock_credentials:
            Client.GoogleAdsClient.load_from_storage(version=latest_version)
            mock_credentials.assert_called_once_with(
                config.get("json_key_file_path"),
                config.get("impersonated_email"),
                http_proxy=None,
            )
            mock_client_init.assert_called_once_with(
                credentials=mock_credentials_instance,
                developer_token=self.developer_token,
                endpoint=None,
                login_customer_id=None,
                logging_config=None,
                linked_customer_id=None,
                version=latest_version,
                http_proxy=None,
            )

    def test_load_from_storage_service_account_no_impersonated_email(self):
        config = {
            "developer_token": self.developer_token,
            "json_key_file_path": self.json_key_file_path,
        }

        file_path = os.path.join(os.path.expanduser("~"), "google-ads.yaml")
        self.fs.create_file(file_path, contents=yaml.safe_dump(config))
        mock_credentials_instance = mock.Mock()

        with mock.patch.object(
            Client.GoogleAdsClient, "__init__", return_value=None
        ), mock.patch.object(
            Client.oauth2,
            "get_service_account_credentials",
            return_value=mock_credentials_instance,
        ):
            self.assertRaises(
                ValueError, Client.GoogleAdsClient.load_from_storage
            )

    def test_get_service(self):
        # Retrieve service names for all defined service clients.
        for ver in valid_versions:
            services_path = f"google.ads.googleads.{ver}"
            service_names = [
                f'{name.rsplit("ServiceClient")[0]}Service'
                for name in dir(import_module(services_path))
                if "ServiceClient" in name
            ]

            client = self._create_test_client()

            # Iterate through retrieval of all service clients by name.
            for service_name in service_names:
                client.get_service(service_name, version=ver)

    def test_get_service_custom_endpoint(self):
        service_name = "GoogleAdsService"
        service_module_base = "google_ads_service"
        grpc_transport_class_name = f"{service_name}GrpcTransport"
        grpc_transport_module_name = f"{service_module_base}_grpc_transport"
        transport_create_channel_path = (
            f"google.ads.googleads.{Client._DEFAULT_VERSION}.services.services."
            f"{service_module_base}.transports.{grpc_transport_class_name}."
            "create_channel"
        )
        endpoint = "alt.endpoint.com"
        client = self._create_test_client(endpoint=endpoint)

        # The GRPC transport's create_channel method is what allows the
        # GoogleAdsClient to specify a custom endpoint. Here we mock the
        # create_channel method in order to verify that it was given the
        # endpoint specified by the client.
        with mock.patch(transport_create_channel_path) as mock_create_channel:
            # A new channel is created during initialization of the service
            # client.
            client.get_service(service_name)
            mock_create_channel.assert_called_once_with(
                host=endpoint,
                credentials=client.credentials,
                options=Client._GRPC_CHANNEL_OPTIONS,
            )

    def test_get_service_not_found(self):
        client = self._create_test_client()
        self.assertRaises(ValueError, client.get_service, "BadService")

    def test_get_service_invalid_version(self):
        client = self._create_test_client()
        self.assertRaises(
            ValueError,
            client.get_service,
            "GoogleAdsService",
            version="bad_version",
        )

    def test_get_service_with_version(self):
        client = self._create_test_client()
        try:
            client.get_service("GoogleAdsService", version=latest_version)
        except Exception:
            self.fail("get_service with a valid version raised an error")

    def test_get_type(self):
        for ver in valid_versions:
            # Retrieve names for all types defined in pb2 files.
            type_path = f"google.ads.googleads.{ver}"
            type_names = import_module(type_path).__all__
            client = self._create_test_client()
            # Iterate through retrieval of all types by name.
            for name in type_names:
                if name.lower().endswith(
                    "serviceclient"
                ) or name.lower().endswith("transport"):
                    continue

                try:
                    client.get_type(name, version=ver)
                except ValueError as error:
                    self.fail(
                        f"Expected {name} in {ver} to be importable via "
                        f"the client.get_type method: {error}"
                    )

    def test_get_type_not_found(self):
        client = self._create_test_client()
        self.assertRaises(ValueError, client.get_type, "BadType")

    def test_get_type_invalid_version(self):
        client = self._create_test_client()
        self.assertRaises(
            ValueError,
            client.get_type,
            "GoogleAdsFailure",
            version="bad_version",
        )

    def test_init_no_logging_config(self):
        """Should call logging.config.dictConfig if logging config exists."""
        with mock.patch(
            "logging.config.dictConfig"
        ) as mock_dictConfig, mock.patch.object(
            Client.oauth2, "get_installed_app_credentials"
        ) as mock_credentials:
            mock_credentials_instance = mock_credentials.return_value
            mock_credentials_instance.refresh_token = self.refresh_token
            mock_credentials_instance.client_id = self.client_id
            mock_credentials_instance.client_secret = self.client_secret
            Client.GoogleAdsClient(
                latest_version, mock_credentials_instance, self.developer_token
            )
            mock_dictConfig.assert_not_called()

    def test_init_with_logging_config(self):
        """Configured LoggingInterceptor should call logging.dictConfig."""
        config = {"test": True}
        with mock.patch(
            "logging.config.dictConfig"
        ) as mock_dictConfig, mock.patch.object(
            Client.oauth2, "get_installed_app_credentials"
        ) as mock_credentials:
            mock_credentials_instance = mock_credentials.return_value
            mock_credentials_instance.refresh_token = self.refresh_token
            mock_credentials_instance.client_id = self.client_id
            mock_credentials_instance.client_secret = self.client_secret
            Client.GoogleAdsClient(
                latest_version,
                mock_credentials_instance,
                self.developer_token,
                logging_config=config,
            )
            mock_dictConfig.assert_called_once_with(config)

    def test_client_dot_enums_hasattr(self):
        """Ensures hasattr works as expected with real Enum."""
        client = self._create_test_client()
        self.assertTrue(hasattr(client.enums, "CampaignStatusEnum"))

    def test_client_dot_enums_only_enums(self):
        """Ensures non-Enum name raises AttributeError."""
        client = self._create_test_client()
        self.assertRaises(AttributeError, getattr, client.enums, "Campaign")

    def test_client_dot_enums_property(self):
        """Ensures that GoogleAdsClient  exposes Enums via an "enums" attribute.

        This tests the 'client.enums' property for a service in every version
        of the API. It loops over the names of all properties on 'client.enums',
        imports them using client.get_type to ensure they're part of the API,
        and ensures the enum fields are directly accessible wihout needing to
        access the inner Enum object.
        """
        for ver in valid_versions:
            client = self._create_test_client(version=ver)
            self.assertTrue(
                hasattr(client, "enums"),
                "GoogleAdsService in "
                f'{ver} does not have an "enums" attribute.',
            )

            enum_names = import_module(
                f"google.ads.googleads.{ver}.enums"
            ).__all__

            for name in enum_names:
                self.assertTrue(hasattr(client.enums, name))
                self.assertIsInstance(
                    getattr(client.enums, name), ProtoEnumMeta
                )

    def test_client_copy_from_both_wrapped(self):
        """client.copy_from works with two wrapped proto messages."""
        client = self._create_test_client()
        destination = client.get_type("Campaign", version=latest_version)
        origin = client.get_type("Campaign", version=latest_version)
        origin.name = "Test"

        client.copy_from(destination, origin)

        self.assertEqual(destination.name, "Test")
        self.assertIsNot(destination, origin)

    def test_client_copy_from_both_native(self):
        """client.copy_from works with two native proto messages."""
        client = self._create_test_client()
        destination = client.get_type("Campaign", version=latest_version)
        native_dest = type(destination).pb(destination)
        origin = client.get_type("Campaign", version=latest_version)
        native_orig = type(origin).pb(origin)
        origin.name = "Test"

        client.copy_from(native_dest, native_orig)

        self.assertEqual(destination.name, "Test")
        self.assertIsNot(destination, origin)

    def test_client_copy_from_native_origin(self):
        """client.copy_from works with a wrapped dest and a native origin."""
        client = self._create_test_client()
        destination = client.get_type("Campaign", version=latest_version)
        origin = client.get_type("Campaign", version=latest_version)
        native_orig = type(origin).pb(origin)
        origin.name = "Test"

        client.copy_from(destination, native_orig)

        self.assertEqual(destination.name, "Test")
        self.assertIsNot(destination, origin)

    def test_client_copy_from_native_destination(self):
        """client.copy_from works with a native dest and a wrapped origin."""
        client = self._create_test_client()
        destination = client.get_type("Campaign", version=latest_version)
        native_dest = type(destination).pb(destination)
        origin = client.get_type("Campaign", version=latest_version)
        origin.name = "Test"

        client.copy_from(native_dest, origin)

        self.assertEqual(destination.name, "Test")
        self.assertIsNot(destination, origin)

    def test_client_copy_from_different_types_wrapped(self):
        """TypeError is raised with different types of wrapped messasges."""
        client = self._create_test_client()
        destination = client.get_type("AdGroup", version=latest_version)
        origin = client.get_type("Campaign", version=latest_version)
        origin.name = "Test"

        self.assertRaises(TypeError, client.copy_from, destination, origin)

    def test_client_copy_from_different_types_native(self):
        """TypeError is raised with different types of native messasges."""
        client = self._create_test_client()
        destination = client.get_type("AdGroup", version=latest_version)
        native_dest = type(destination).pb(destination)
        origin = client.get_type("Campaign", version=latest_version)
        native_orig = type(origin).pb(origin)
        origin.name = "Test"

        self.assertRaises(TypeError, client.copy_from, native_dest, native_orig)

    def test_client_copy_from_different_types_native_origin(self):
        """TypeError is raised with different types and native origin."""
        client = self._create_test_client()
        destination = client.get_type("AdGroup", version=latest_version)
        origin = client.get_type("Campaign", version=latest_version)
        native_orig = type(origin).pb(origin)
        origin.name = "Test"

        self.assertRaises(TypeError, client.copy_from, destination, native_orig)

    def test_client_copy_from_different_types_native_destination(self):
        """TypeError is raised with different types and native destination."""
        client = self._create_test_client()
        destination = client.get_type("AdGroup", version=latest_version)
        native_dest = type(destination).pb(destination)
        origin = client.get_type("Campaign", version=latest_version)
        origin.name = "Test"

        self.assertRaises(TypeError, client.copy_from, native_dest, origin)

    def test_client_copy_from_non_proto_message(self):
        """ValueError is raised if an object other than a protobuf is given"""
        client = self._create_test_client()
        destination = client.get_type("AdGroup", version=latest_version)
        origin = {"name": "Test"}

        self.assertRaises(ValueError, client.copy_from, destination, origin)

    def test_client_is_picklable(self):
        client = Client.GoogleAdsClient(
            {}, self.developer_token, endpoint=None, version=None,
        )

        try:
            pickled = pickle.dumps(client)
            pickle.loads(pickled)
        except:
            self.fail("Exception occurred when pickling GoogleAdsClient")

    def test_http_proxy(self):
        """Client initialization sets http_proxy in GRPC config options"""
        test_proxy = "https://localhost:8080"
        self._create_test_client(http_proxy=test_proxy)
        self.assertIn(
            ("grpc.http_proxy", test_proxy), Client._GRPC_CHANNEL_OPTIONS
        )

    def test_load_http_proxy_from_env(self):
        mock_credentials_instance = mock.Mock()

        with mock.patch.object(
            Client.GoogleAdsClient, "__init__", return_value=None
        ) as mock_client_init, mock.patch.object(
            Client.oauth2,
            "get_installed_app_credentials",
            return_value=mock_credentials_instance,
        ) as mock_credentials, mock.patch.dict(
            os.environ,
            {
                "GOOGLE_ADS_DEVELOPER_TOKEN": self.developer_token,
                "GOOGLE_ADS_CLIENT_ID": self.client_id,
                "GOOGLE_ADS_CLIENT_SECRET": self.client_secret,
                "GOOGLE_ADS_REFRESH_TOKEN": self.refresh_token,
                "GOOGLE_ADS_HTTP_PROXY": self.http_proxy,
            },
        ) as mock_os_environ:
            Client.GoogleAdsClient.load_from_env()

            mock_client_init.assert_called_once_with(
                credentials=mock_credentials_instance,
                developer_token=self.developer_token,
                endpoint=None,
                login_customer_id=None,
                logging_config=None,
                linked_customer_id=None,
                version=None,
                http_proxy=self.http_proxy,
            )

    def test_load_http_proxy_from_dict(self):
        config = {
            "developer_token": self.developer_token,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": self.refresh_token,
            "http_proxy": self.http_proxy,
        }
        mock_credentials_instance = mock.Mock()

        with mock.patch.object(
            Client.GoogleAdsClient, "__init__", return_value=None
        ) as mock_client_init, mock.patch.object(
            Client.oauth2,
            "get_installed_app_credentials",
            return_value=mock_credentials_instance,
        ) as mock_credentials:
            Client.GoogleAdsClient.load_from_dict(config)

            mock_client_init.assert_called_once_with(
                credentials=mock_credentials_instance,
                developer_token=self.developer_token,
                endpoint=None,
                login_customer_id=None,
                logging_config=None,
                linked_customer_id=None,
                version=None,
                http_proxy=self.http_proxy,
            )

    def test_load_http_proxy_from_string(self):
        config = {
            "developer_token": self.developer_token,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": self.refresh_token,
            "http_proxy": self.http_proxy,
        }
        mock_credentials_instance = mock.Mock()

        with mock.patch.object(
            Client.GoogleAdsClient, "__init__", return_value=None
        ) as mock_client_init, mock.patch.object(
            Client.oauth2,
            "get_installed_app_credentials",
            return_value=mock_credentials_instance,
        ) as mock_credentials:
            Client.GoogleAdsClient.load_from_string(yaml.dump(config))

            mock_client_init.assert_called_once_with(
                credentials=mock_credentials_instance,
                developer_token=self.developer_token,
                endpoint=None,
                login_customer_id=None,
                logging_config=None,
                linked_customer_id=None,
                version=None,
                http_proxy=self.http_proxy,
            )

    def test_load_from_storage(self):
        config = {
            "developer_token": self.developer_token,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": self.refresh_token,
            "http_proxy": self.http_proxy,
        }

        file_path = os.path.join(os.path.expanduser("~"), "google-ads.yaml")
        self.fs.create_file(file_path, contents=yaml.safe_dump(config))
        mock_credentials_instance = mock.Mock()

        with mock.patch.object(
            Client.GoogleAdsClient, "__init__", return_value=None
        ) as mock_client_init, mock.patch.object(
            Client.oauth2,
            "get_installed_app_credentials",
            return_value=mock_credentials_instance,
        ) as mock_credentials:
            Client.GoogleAdsClient.load_from_storage()
            mock_credentials.assert_called_once_with(
                config.get("client_id"),
                config.get("client_secret"),
                config.get("refresh_token"),
                http_proxy=self.http_proxy,
            )
            mock_client_init.assert_called_once_with(
                credentials=mock_credentials_instance,
                developer_token=self.developer_token,
                endpoint=None,
                login_customer_id=None,
                logging_config=None,
                linked_customer_id=None,
                version=None,
                http_proxy=self.http_proxy,
            )
