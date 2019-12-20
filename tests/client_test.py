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

import os
import mock
import yaml
from importlib import import_module
from pyfakefs.fake_filesystem_unittest import TestCase as FileTestCase

from google.ads.google_ads import client as Client

latest_version = Client._DEFAULT_VERSION
valid_versions = Client._VALID_API_VERSIONS

services_path = 'google.ads.google_ads.{}.proto.services'.format(latest_version)
services = import_module(services_path)

class GoogleAdsClientTest(FileTestCase):
    """Tests for the google.ads.googleads.client.GoogleAdsClient class."""

    def _create_test_client(self, endpoint=None):
        with mock.patch.object(
            Client.oauth2,
            'get_installed_app_credentials'
        ) as mock_credentials:
            mock_credentials_instance = mock_credentials.return_value
            mock_credentials_instance.refresh_token = self.refresh_token
            mock_credentials_instance.client_id = self.client_id
            mock_credentials_instance.client_secret = self.client_secret
            client = Client.GoogleAdsClient(mock_credentials_instance,
                                            self.developer_token, endpoint=endpoint)
            return client

    def setUp(self):
        self.setUpPyfakefs()
        self.developer_token = 'abc123'
        self.client_id = 'client_id_123456789'
        self.client_secret = 'client_secret_987654321'
        self.refresh_token = 'refresh'
        self.login_customer_id = '1234567890'
        self.path_to_private_key_file = '/test/path/to/config.json'
        self.delegated_account = 'delegated@account.com'


    def test_get_client_kwargs_login_customer_id(self):
        config = {
            'developer_token': self.developer_token,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'refresh_token': self.refresh_token,
            'login_customer_id': self.login_customer_id}
        mock_credentials_instance = mock.Mock()

        with mock.patch.object(
            Client.oauth2,
            'get_installed_app_credentials',
            return_value=mock_credentials_instance):
            result = Client.GoogleAdsClient._get_client_kwargs(config)
            self.assertEqual(
                result,
                {
                    'credentials': mock_credentials_instance,
                    'developer_token': self.developer_token,
                    'endpoint': None,
                    'login_customer_id': self.login_customer_id,
                    'logging_config': None
                })

    def test_get_client_kwargs_login_customer_id_as_None(self):
        config = {
            'developer_token': self.developer_token,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'refresh_token': self.refresh_token,
            'login_customer_id': None}
        mock_credentials_instance = mock.Mock()

        with mock.patch.object(
            Client.oauth2,
            'get_installed_app_credentials',
            return_value=mock_credentials_instance):
            result = Client.GoogleAdsClient._get_client_kwargs(config)
            self.assertEqual(
                result,
                {
                    'credentials': mock_credentials_instance,
                    'developer_token': self.developer_token,
                    'endpoint': None,
                    'login_customer_id': None,
                    'logging_config': None
                })

    def test_get_client_kwargs(self):
        config = {
            'developer_token': self.developer_token,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'refresh_token': self.refresh_token}
        mock_credentials_instance = mock.Mock()

        with mock.patch.object(
            Client.oauth2,
            'get_installed_app_credentials',
            return_value=mock_credentials_instance):
            result = Client.GoogleAdsClient._get_client_kwargs(config)
            self.assertEqual(
                result,
                {
                    'credentials': mock_credentials_instance,
                    'developer_token': self.developer_token,
                    'endpoint': None,
                    'login_customer_id': None,
                    'logging_config': None
                })

    def test_get_client_kwargs_custom_endpoint(self):
        endpoint = 'alt.endpoint.com'
        config = {
            'developer_token': self.developer_token,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'refresh_token': self.refresh_token,
            'endpoint': endpoint}
        mock_credentials_instance = mock.Mock()

        with mock.patch.object(
            Client.oauth2,
            'get_installed_app_credentials',
            return_value=mock_credentials_instance):
            result = Client.GoogleAdsClient._get_client_kwargs(config)
            self.assertEqual(
                result,
                {
                    'credentials': mock_credentials_instance,
                    'developer_token': self.developer_token,
                    'endpoint': endpoint,
                    'login_customer_id': None,
                    'logging_config': None
                })

    def test_load_from_dict(self):
        config = {
            'developer_token': self.developer_token,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'refresh_token': self.refresh_token}
        mock_credentials_instance = mock.Mock()

        with mock.patch.object(
            Client.GoogleAdsClient,
            '__init__',
            return_value=None
        ) as mock_client_init, mock.patch.object(
            Client.oauth2,
            'get_installed_app_credentials',
            return_value=mock_credentials_instance
        ) as mock_credentials:
          Client.GoogleAdsClient.load_from_dict(config)
          
          mock_client_init.assert_called_once_with(
          credentials=mock_credentials_instance,
          developer_token=self.developer_token,
          endpoint=None,
          login_customer_id=None,
          logging_config=None)

    def test_load_from_storage(self):
        config = {
            'developer_token': self.developer_token,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'refresh_token': self.refresh_token}

        file_path = os.path.join(os.path.expanduser('~'), 'google-ads.yaml')
        self.fs.create_file(file_path, contents=yaml.safe_dump(config))
        mock_credentials_instance = mock.Mock()

        with mock.patch.object(
            Client.GoogleAdsClient,
            '__init__',
            return_value=None
        ) as mock_client_init, mock.patch.object(
            Client.oauth2,
            'get_installed_app_credentials',
            return_value=mock_credentials_instance
        ) as mock_credentials:
            Client.GoogleAdsClient.load_from_storage()
            mock_credentials.assert_called_once_with(
                config.get('client_id'),
                config.get('client_secret'),
                config.get('refresh_token'))
            mock_client_init.assert_called_once_with(
                credentials=mock_credentials_instance,
                developer_token=self.developer_token,
                endpoint=None,
                login_customer_id=None,
                logging_config=None)

    def test_load_from_storage_login_cid_int(self):
        login_cid = 1234567890
        config = {
            'developer_token': self.developer_token,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'refresh_token': self.refresh_token,
            'login_customer_id': login_cid}

        file_path = os.path.join(os.path.expanduser('~'), 'google-ads.yaml')
        self.fs.create_file(file_path, contents=yaml.safe_dump(config))
        mock_credentials_instance = mock.Mock()

        with mock.patch.object(
            Client.GoogleAdsClient,
            '__init__',
            return_value=None
        ) as mock_client_init, mock.patch.object(
            Client.oauth2,
            'get_installed_app_credentials',
            return_value=mock_credentials_instance
        ) as mock_credentials:
            Client.GoogleAdsClient.load_from_storage()
            mock_credentials.assert_called_once_with(
                config.get('client_id'),
                config.get('client_secret'),
                config.get('refresh_token'))
            mock_client_init.assert_called_once_with(
                credentials=mock_credentials_instance,
                developer_token=self.developer_token,
                endpoint=None,
                login_customer_id=str(login_cid),
                logging_config=None)

    def test_load_from_storage_custom_path(self):
        config = {
            'developer_token': self.developer_token,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'refresh_token': self.refresh_token}

        file_path = 'test/google-ads.yaml'
        self.fs.create_file(file_path, contents=yaml.safe_dump(config))
        mock_credentials_instance = mock.Mock()

        with mock.patch.object(
            Client.GoogleAdsClient,
            '__init__',
            return_value=None
        ) as mock_client_init, mock.patch.object(
            Client.oauth2,
            'get_installed_app_credentials',
            return_value=mock_credentials_instance):
            Client.GoogleAdsClient.load_from_storage(path=file_path)
            mock_client_init.assert_called_once_with(
                credentials=mock_credentials_instance,
                developer_token=self.developer_token,
                endpoint=None,
                login_customer_id=None,
                logging_config=None)

    def test_load_from_storage_file_not_found(self):
        wrong_file_path = 'test/wrong-google-ads.yaml'

        self.assertRaises(
            IOError,
            Client.GoogleAdsClient.load_from_storage,
            path=wrong_file_path)

    def test_load_from_storage_required_config_missing(self):
        config = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'refresh_token': self.refresh_token
        }

        file_path = 'test/google-ads.yaml'
        self.fs.create_file(file_path, contents=yaml.safe_dump(config))

        self.assertRaises(
            ValueError,
            Client.GoogleAdsClient.load_from_storage,
            path=file_path)

    def test_load_from_storage_service_account_config(self):
        config = {
            'developer_token': self.developer_token,
            'path_to_private_key_file': self.path_to_private_key_file,
            'delegated_account': self.delegated_account
        }

        file_path = os.path.join(os.path.expanduser('~'), 'google-ads.yaml')
        self.fs.create_file(file_path, contents=yaml.safe_dump(config))
        mock_credentials_instance = mock.Mock()

        with mock.patch.object(
            Client.GoogleAdsClient,
            '__init__',
            return_value=None
        ) as mock_client_init, mock.patch.object(
            Client.oauth2,
            'get_service_account_credentials',
            return_value=mock_credentials_instance
        ) as mock_credentials:
            Client.GoogleAdsClient.load_from_storage()
            mock_credentials.assert_called_once_with(
                config.get('path_to_private_key_file'),
                config.get('delegated_account'))
            mock_client_init.assert_called_once_with(
                credentials=mock_credentials_instance,
                developer_token=self.developer_token,
                endpoint=None,
                login_customer_id=None,
                logging_config=None)

    def test_load_from_storage_service_account_no_delegated_account(self):
        config = {
            'developer_token': self.developer_token,
            'path_to_private_key_file': self.path_to_private_key_file}

        file_path = os.path.join(os.path.expanduser('~'), 'google-ads.yaml')
        self.fs.create_file(file_path, contents=yaml.safe_dump(config))
        mock_credentials_instance = mock.Mock()

        with mock.patch.object(
            Client.GoogleAdsClient,
            '__init__',
            return_value=None), mock.patch.object(
            Client.oauth2,
            'get_service_account_credentials',
            return_value=mock_credentials_instance):
            self.assertRaises(
                ValueError,
                Client.GoogleAdsClient.load_from_storage)

    def test_get_service(self):
        # Retrieve service names for all defined service clients.
        for ver in valid_versions:
            services_path = 'google.ads.google_ads.%s' % ver
            service_names = [
                '%s%s' % (name.rsplit('ServiceClient')[0], 'Service')
                for name in dir(import_module(services_path))
                if 'ServiceClient' in name]

            client = self._create_test_client()

            # Iterate through retrieval of all service clients by name.
            for service_name in service_names:
                client.get_service(service_name)

    def test_get_service_custom_endpoint(self):
        service_name = 'GoogleAdsService'
        service_module_base = 'google_ads_service'
        grpc_transport_class_name = '%sGrpcTransport' % service_name
        grpc_transport_module_name = '%s_grpc_transport' % service_module_base
        transport_create_channel_path = (
            'google.ads.google_ads.%s.services.transports.%s.%s.create_channel'
            % (Client._DEFAULT_VERSION,
               grpc_transport_module_name,
               grpc_transport_class_name))
        endpoint = 'alt.endpoint.com'
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
                address=endpoint, credentials=client.credentials,
                options=Client._GRPC_CHANNEL_OPTIONS)

    def test_get_service_not_found(self):
        client = self._create_test_client()
        self.assertRaises(ValueError, client.get_service, 'BadService')

    def test_get_service_invalid_version(self):
        client = self._create_test_client()
        self.assertRaises(ValueError, client.get_service, 'GoogleAdsService',
                          version='bad_version')

    def test_get_service_with_version(self):
        client = self._create_test_client()
        try:
            client.get_service('GoogleAdsService', version=latest_version)
        except Exception:
            self.fail('get_service with a valid version raised an error')

# XXX: deferred test for fixing lazy loading
#    def test_get_service_with_interceptor(self):
#        client = self._create_test_client()
#
#        class Interceptor:
#            pass
#
#        interceptor = Interceptor()
#
#        with mock.patch.object(
#            Client,
#            'intercept_channel'
#        ) as mock_intercept_channel:
#            client.get_service('GoogleAdsService', interceptors=[interceptor])
#            first_interceptor = mock_intercept_channel.call_args[0][1]
#            self.assertEqual(first_interceptor, interceptor)
#
    def test_get_type(self):
        for ver in valid_versions:
            # Retrieve names for all types defined in pb2 files.
            type_path = f'google.ads.google_ads.{ver}.types'
            type_names = import_module(type_path).__all__
            # Iterate through retrieval of all types by name.
            for name in type_names:
                if name.lower().endswith('pb2'):
                    continue
                Client.GoogleAdsClient.get_type(
                    name, version=ver)

    def test_get_type_not_found(self):
        self.assertRaises(
            ValueError, Client.GoogleAdsClient.get_type,
            'BadType')

    def test_get_type_invalid_version(self):
        self.assertRaises(
            ValueError, Client.GoogleAdsClient.get_type,
            'GoogleAdsFailure', version='bad_version')

    def test_init_no_logging_config(self):
        """Should only call logging.config.dictConfig if logging config exists.
        """
        with mock.patch(
            'logging.config.dictConfig'
        ) as mock_dictConfig, mock.patch.object(
            Client.oauth2,
            'get_installed_app_credentials'
        ) as mock_credentials:
            mock_credentials_instance = mock_credentials.return_value
            mock_credentials_instance.refresh_token = self.refresh_token
            mock_credentials_instance.client_id = self.client_id
            mock_credentials_instance.client_secret = self.client_secret
            Client.GoogleAdsClient(mock_credentials_instance,
                                   self.developer_token)
            mock_dictConfig.assert_not_called()

    def test_init_with_logging_config(self):
        """Configured LoggingInterceptor should call logging.dictConfig.
        """
        config = {'test': True}
        with mock.patch(
            'logging.config.dictConfig'
        ) as mock_dictConfig, mock.patch.object(
            Client.oauth2,
            'get_installed_app_credentials'
        ) as mock_credentials:
            mock_credentials_instance = mock_credentials.return_value
            mock_credentials_instance.refresh_token = self.refresh_token
            mock_credentials_instance.client_id = self.client_id
            mock_credentials_instance.client_secret = self.client_secret
            Client.GoogleAdsClient(mock_credentials_instance,
                                   self.developer_token, logging_config=config)
            mock_dictConfig.assert_called_once_with(config)
