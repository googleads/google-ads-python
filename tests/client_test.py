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

import google.ads.google_ads.client
import google.ads.google_ads.v0
import mock
from pyfakefs.fake_filesystem_unittest import TestCase
import yaml


class GoogleAdsClientTest(TestCase):
    """Tests for the google.ads.googleads.client.GoogleAdsClient class."""

    def _create_test_client(self, endpoint=None):
        with mock.patch('google.oauth2.credentials') as mock_credentials:
            mock_credentials_instance = mock_credentials.return_value
            mock_credentials_instance.refresh_token = self.refresh_token
            mock_credentials_instance.client_id = self.client_id
            mock_credentials_instance.client_secret = self.client_secret
            client = google.ads.google_ads.client.GoogleAdsClient(
                mock_credentials_instance, self.developer_token,
                endpoint=endpoint)
            return client

    def setUp(self):
        self.setUpPyfakefs()
        self.developer_token = 'abc123'
        self.client_id = 'client_id_123456789'
        self.client_secret = 'client_secret_987654321'
        self.refresh_token = 'refresh'
        self.login_customer_id = '1234567890'

    def test_load_from_storage_login_customer_id(self):
        config = {
            'developer_token': self.developer_token,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'refresh_token': self.refresh_token,
            'login_customer_id': self.login_customer_id
        }

        file_path = os.path.join(os.path.expanduser('~'), 'google-ads.yaml')
        self.fs.create_file(file_path, contents=yaml.safe_dump(config))

        with mock.patch('google.ads.google_ads.client.GoogleAdsClient'
                        '.__init__') as mock_client_init, \
             mock.patch(
                 'google.oauth2.credentials.Credentials') as mock_credentials:
            mock_client_init.return_value = None
            mock_credentials_instance = mock.Mock()
            mock_credentials.return_value = mock_credentials_instance
            (google.ads.google_ads.client.GoogleAdsClient.load_from_storage())
            mock_client_init.assert_called_once_with(
                credentials=mock_credentials_instance,
                developer_token=self.developer_token,
                endpoint=None,
                login_customer_id=self.login_customer_id)

    def test_load_from_storage_login_customer_id_as_None(self):
        config = {
            'developer_token': self.developer_token,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'refresh_token': self.refresh_token,
            'login_customer_id': None
        }

        file_path = os.path.join(os.path.expanduser('~'), 'google-ads.yaml')
        self.fs.create_file(file_path, contents=yaml.safe_dump(config))

        with mock.patch('google.ads.google_ads.client.GoogleAdsClient'
                        '.__init__') as mock_client_init, \
             mock.patch(
                 'google.oauth2.credentials.Credentials') as mock_credentials:
            mock_client_init.return_value = None
            mock_credentials_instance = mock.Mock()
            mock_credentials.return_value = mock_credentials_instance
            (google.ads.google_ads.client.GoogleAdsClient.load_from_storage())
            mock_client_init.assert_called_once_with(
                credentials=mock_credentials_instance,
                developer_token=self.developer_token,
                endpoint=None,
                login_customer_id=None)

    def test_load_from_storage_invalid_login_customer_id(self):
        config = {
            'developer_token': self.developer_token,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'refresh_token': self.refresh_token,
            'login_customer_id': '123-456-7890'
        }

        file_path = os.path.join(os.path.expanduser('~'), 'google-ads.yaml')
        self.fs.create_file(file_path, contents=yaml.safe_dump(config))

        with mock.patch(
                'google.oauth2.credentials.Credentials') as mock_credentials:
            mock_credentials_instance = mock.Mock()
            mock_credentials.return_value = mock_credentials_instance
            self.assertRaises(
                    ValueError,
                    google.ads.google_ads.client.GoogleAdsClient
                        .load_from_storage)

    def test_load_from_storage_too_short_login_customer_id(self):
        config = {
            'developer_token': self.developer_token,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'refresh_token': self.refresh_token,
            'login_customer_id': '123'
        }

        file_path = os.path.join(os.path.expanduser('~'), 'google-ads.yaml')
        self.fs.create_file(file_path, contents=yaml.safe_dump(config))

        with mock.patch(
                'google.oauth2.credentials.Credentials') as mock_credentials:
            mock_credentials_instance = mock.Mock()
            mock_credentials.return_value = mock_credentials_instance
            self.assertRaises(
                    ValueError,
                    google.ads.google_ads.client.GoogleAdsClient
                        .load_from_storage)

    def test_load_from_storage(self):
        config = {
            'developer_token': self.developer_token,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'refresh_token': self.refresh_token
        }

        file_path = os.path.join(os.path.expanduser('~'), 'google-ads.yaml')
        self.fs.create_file(file_path, contents=yaml.safe_dump(config))

        with mock.patch('google.ads.google_ads.client.GoogleAdsClient'
                        '.__init__') as mock_client_init, \
             mock.patch(
                 'google.oauth2.credentials.Credentials') as mock_credentials:
            mock_client_init.return_value = None
            mock_credentials_instance = mock.Mock()
            mock_credentials.return_value = mock_credentials_instance
            (google.ads.google_ads.client.GoogleAdsClient
             .load_from_storage())
            mock_client_init.assert_called_once_with(
                credentials=mock_credentials_instance,
                developer_token=self.developer_token,
                endpoint=None,
                login_customer_id=None)

    def test_load_from_storage_custom_endpoint(self):
        endpoint = 'alt.endpoint.com'
        config = {
            'developer_token': self.developer_token,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'refresh_token': self.refresh_token,
            'endpoint': endpoint
        }

        file_path = os.path.join(os.path.expanduser('~'), 'google-ads.yaml')
        self.fs.create_file(file_path, contents=yaml.safe_dump(config))

        with mock.patch('google.ads.google_ads.client.GoogleAdsClient'
                        '.__init__') as mock_client_init, \
            mock.patch(
                'google.oauth2.credentials.Credentials') as mock_credentials:
            mock_client_init.return_value = None
            mock_credentials_instance = mock.Mock()
            mock_credentials.return_value = mock_credentials_instance
            google.ads.google_ads.client.GoogleAdsClient.load_from_storage()
            mock_client_init.assert_called_once_with(
                credentials=mock_credentials_instance,
                developer_token=self.developer_token,
                endpoint=endpoint,
                login_customer_id=None)

    def test_load_from_storage_custom_path(self):
        config = {
            'developer_token': self.developer_token,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'refresh_token': self.refresh_token
        }

        file_path = 'test/google-ads.yaml'
        self.fs.create_file(file_path, contents=yaml.safe_dump(config))

        with mock.patch('google.ads.google_ads.client.GoogleAdsClient'
                        '.__init__') as mock_client_init, \
            mock.patch(
                'google.oauth2.credentials.Credentials') as mock_credentials:
            mock_client_init.return_value = None
            mock_credentials_instance = mock.Mock()
            mock_credentials.return_value = mock_credentials_instance
            (google.ads.google_ads.client.GoogleAdsClient
             .load_from_storage(path=file_path))
            mock_client_init.assert_called_once_with(
                credentials=mock_credentials_instance,
                developer_token=self.developer_token,
                endpoint=None,
                login_customer_id=None)

    def test_load_from_storage_file_not_found(self):
        wrong_file_path = 'test/wrong-google-ads.yaml'

        self.assertRaises(
            IOError,
            google.ads.google_ads.client.GoogleAdsClient.load_from_storage,
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
            google.ads.google_ads.client.GoogleAdsClient.load_from_storage,
            path=file_path)

    def test_get_service(self):
        # Retrieve service names for all defined service clients.
        service_names = [
            '%s%s' % (name.rsplit('ServiceClient')[0], 'Service')
            for name in dir(google.ads.google_ads.v0)
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
            % (google.ads.google_ads.client._DEFAULT_VERSION,
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
                address=endpoint, credentials=client.credentials)

    def test_get_service_not_found(self):
        client = self._create_test_client()
        self.assertRaises(ValueError, client.get_service, 'BadService')

    def test_get_service_invalid_version(self):
        client = self._create_test_client()
        self.assertRaises(ValueError, client.get_service, 'GoogleAdsService',
                          version='v0_bad')

    def test_get_type(self):
        # Retrieve names for all types defined in pb2 files.
        type_names = google.ads.google_ads.v0.types.names

        # Iterate through retrieval of all types by name.
        for name in type_names:
            google.ads.google_ads.client.GoogleAdsClient.get_type(name)

    def test_get_type_not_found(self):
        self.assertRaises(
            ValueError, google.ads.google_ads.client.GoogleAdsClient.get_type,
            'BadType')

    def test_get_type_invalid_version(self):
        self.assertRaises(
            ValueError, google.ads.google_ads.client.GoogleAdsClient.get_type,
            'GoogleAdsFailure', version='v0_bad')


class MetadataInterceptorTest(TestCase):

    def setUp(self):
        self.mock_developer_token = '1234567890'
        self.mock_login_customer_id = '0987654321'

    def test_init(self):
        interceptor = google.ads.google_ads.client.MetadataInterceptor(
            self.mock_developer_token,
            self.mock_login_customer_id)

        self.assertEqual(
            interceptor.developer_token_meta,
            ('developer-token', self.mock_developer_token))

        self.assertEqual(
            interceptor.login_customer_id_meta,
            ('login-customer-id', self.mock_login_customer_id)
        )

    def test_init_no_login_customer_id(self):
        interceptor = google.ads.google_ads.client.MetadataInterceptor(
            self.mock_developer_token,
            None)

        self.assertEqual(
            interceptor.developer_token_meta,
            ('developer-token', self.mock_developer_token))

        self.assertEqual(
            interceptor.login_customer_id_meta,
            None
        )

    def test_update_client_call_details_metadata(self):
        interceptor = google.ads.google_ads.client.MetadataInterceptor(
            self.mock_developer_token,
            self.mock_login_customer_id)

        mock_metadata = list([('test-key', 'test-value')])
        mock_client_call_details = mock.Mock()

        client_call_details = interceptor._update_client_call_details_metadata(
            mock_client_call_details, mock_metadata)

        self.assertEqual(client_call_details.metadata, mock_metadata)

    def test_intercept_unary_unary(self):
        interceptor = google.ads.google_ads.client.MetadataInterceptor(
            self.mock_developer_token,
            self.mock_login_customer_id)

        mock_continuation = mock.Mock(return_value=None)
        mock_client_call_details = mock.Mock()
        mock_client_call_details.method = 'test/method'
        mock_client_call_details.timeout = 5
        mock_client_call_details.metadata = [('apples', 'oranges')]
        mock_request = mock.Mock()

        with mock.patch.object(
            interceptor,
            '_update_client_call_details_metadata',
            wraps=interceptor._update_client_call_details_metadata
        ) as mock_updater:
            interceptor.intercept_unary_unary(
                mock_continuation,
                mock_client_call_details,
                mock_request)

            mock_updater.assert_called_once_with(
                mock_client_call_details, [mock_client_call_details.metadata[0],
                interceptor.developer_token_meta,
                interceptor.login_customer_id_meta])

            mock_continuation.assert_called_once()
