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
import json
import logging

import google.ads.google_ads.client
import google.ads.google_ads.v0
import grpc

from google.ads.google_ads.v0.proto.services import google_ads_service_pb2
from google.ads.google_ads.v0.proto.errors import errors_pb2 as error_protos
from google.ads.google_ads.errors import GoogleAdsException
from unittest import TestCase
from pyfakefs.fake_filesystem_unittest import TestCase as FileTestCase


class ModuleLevelTest(TestCase):
    def test_parse_metadata_to_json(self):
        mock_metadata = [
            ('x-goog-api-client',
             'gl-python/123 grpc/123 gax/123'),
            ('developer-token', '0000000000'),
            ('login-customer-id', '9999999999')]

        result = (google.ads.google_ads.client.
                  _parse_metadata_to_json(mock_metadata))

        self.assertEqual(result, '{\n'
                                 '  "developer-token": "REDACTED",\n'
                                 '  "login-customer-id": "9999999999",\n'
                                 '  "x-goog-api-client": "gl-python/123 '
                                 'grpc/123 gax/123"\n'
                                 '}')

    def test_parse_metadata_to_json_with_none(self):
        mock_metadata = None

        result = (google.ads.google_ads.client.
                  _parse_metadata_to_json(mock_metadata))

        self.assertEqual(result, '{}')


class GoogleAdsClientTest(FileTestCase):
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
                login_customer_id=self.login_customer_id,
                logging_config=None)

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
                login_customer_id=None,
                logging_config=None)

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
                login_customer_id=None,
                logging_config=None)

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
                login_customer_id=None,
                logging_config=None)

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
                login_customer_id=None,
                logging_config=None)

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


class LoggingInterceptorTest(TestCase):
    """Tests for the google.ads.googleads.client.LoggingInterceptor class."""
    _MOCK_CONFIG = {'test': True}
    _MOCK_ENDPOINT = 'www.test-endpoint.com'
    _MOCK_INITIAL_METADATA = [('developer-token', '123456'),
                              ('header', 'value')]
    _MOCK_CUSTOMER_ID = '123456'
    _MOCK_REQUEST_ID = '654321xyz'
    _MOCK_METHOD = 'test/method'
    _MOCK_TRAILING_METADATA = (('request-id', _MOCK_REQUEST_ID),)
    _MOCK_ERROR_MESSAGE = 'Test error message'

    def _create_test_interceptor(self, config=_MOCK_CONFIG,
                                 endpoint=_MOCK_ENDPOINT):
        return google.ads.google_ads.client.LoggingInterceptor(config, endpoint)

    def _get_mock_client_call_details(self):
        mock_client_call_details = mock.Mock()
        mock_client_call_details.method = self._MOCK_METHOD
        mock_client_call_details.metadata = self._MOCK_INITIAL_METADATA
        return mock_client_call_details

    def _get_mock_request(self):
        mock_request = mock.Mock()
        mock_request.customer_id = self._MOCK_CUSTOMER_ID
        return mock_request

    def _get_trailing_metadata_fn(self):
        def mock_trailing_metadata_fn():
            return self._MOCK_TRAILING_METADATA

        return mock_trailing_metadata_fn

    def _get_mock_exception(self):
        exception = mock.Mock()
        error = mock.Mock()
        error.message = self._MOCK_ERROR_MESSAGE
        exception.request_id = self._MOCK_REQUEST_ID
        exception.failure = mock.Mock()
        exception.failure.errors = [error]
        exception.error = mock.Mock()
        exception.error.trailing_metadata = self._get_trailing_metadata_fn()
        return exception

    def _get_mock_transport_exception(self):
        def _mock_debug_error_string():
            return u'{"description":"Error received from peer"}'

        exception = mock.Mock()
        exception.debug_error_string = _mock_debug_error_string
        del exception.failure
        return exception

    def _get_mock_response(self, failed=False):
        def mock_exception_fn():
            if failed:
                return self._get_mock_exception()
            return None

        mock_response = mock.Mock()
        mock_response.exception = mock_exception_fn
        mock_response.trailing_metadata = self._get_trailing_metadata_fn()
        return mock_response

    def _get_mock_continuation_fn(self, fail=False):
        def mock_continuation_fn(client_call_details, request):
            mock_response = self._get_mock_response(fail)
            return mock_response

        return mock_continuation_fn

    def test_init_no_config(self):
        with mock.patch('logging.config.dictConfig') as mock_dictConfig:
            interceptor = google.ads.google_ads.client.LoggingInterceptor()
            mock_dictConfig.assert_not_called()

    def test_init_with_config(self):
        config = {'test': True}
        with mock.patch('logging.config.dictConfig') as mock_dictConfig:
            interceptor = google.ads.google_ads.client.LoggingInterceptor(
                config)
            mock_dictConfig.assert_called_once_with(config)

    def test_intercept_unary_unary_unconfigured(self):
        mock_client_call_details = self._get_mock_client_call_details()
        mock_continuation_fn = self._get_mock_continuation_fn()
        mock_request = self._get_mock_request()

        with mock.patch(
                'google.ads.google_ads.client.MessageToJson') as mock_formatter:
            # Since logging configuration is global it needs to be reset here
            # so that state from previous tests does not affect these assertions
            logging.disable(logging.CRITICAL)
            logger_spy = mock.Mock(wraps=google.ads.google_ads.client._logger)
            interceptor = google.ads.google_ads.client.LoggingInterceptor()
            interceptor.intercept_unary_unary(
                mock_continuation_fn,
                mock_client_call_details,
                mock_request)

            logger_spy.debug.assert_not_called()
            logger_spy.info.assert_not_called()
            logger_spy.warning.assert_not_called()


    def test_intercept_unary_unary_successful_request(self):
        mock_client_call_details = self._get_mock_client_call_details()
        mock_continuation_fn = self._get_mock_continuation_fn()
        mock_request = self._get_mock_request()
        mock_json_message = '{"test": "request-response"}'
        mock_response = mock_continuation_fn(
            mock_client_call_details, mock_request)
        mock_trailing_metadata = mock_response.trailing_metadata()

        with mock.patch('logging.config.dictConfig'), \
            mock.patch('google.ads.google_ads.client._logger') as mock_logger, \
            mock.patch(
                'google.ads.google_ads.client.MessageToJson') as mock_formatter:
            mock_formatter.return_value = mock_json_message
            interceptor = self._create_test_interceptor()
            interceptor.intercept_unary_unary(
                mock_continuation_fn,
                mock_client_call_details,
                mock_request)

            mock_logger.info.assert_called_once_with(
                interceptor._SUMMARY_LOG_LINE
                % (
                    self._MOCK_CUSTOMER_ID,
                    self._MOCK_ENDPOINT,
                    mock_client_call_details.method,
                    self._MOCK_REQUEST_ID,
                    False,
                    None
                )
            )

            mock_logger.debug.assert_called_once_with(
                interceptor._FULL_REQUEST_LOG_LINE
                % (
                    self._MOCK_METHOD,
                    self._MOCK_ENDPOINT,
                    google.ads.google_ads.client.
                    _parse_metadata_to_json(mock_client_call_details.metadata),
                    mock_json_message,
                    google.ads.google_ads.client.
                    _parse_metadata_to_json(mock_trailing_metadata),
                    mock_json_message
                )
            )

    def test_intercept_unary_unary_failed_request(self):
        mock_client_call_details = self._get_mock_client_call_details()
        mock_continuation_fn = self._get_mock_continuation_fn(fail=True)
        mock_request = self._get_mock_request()
        mock_json_message = '{"test": "request-response"}'
        mock_response = mock_continuation_fn(
            mock_client_call_details, mock_request)
        mock_trailing_metadata = mock_response.trailing_metadata()

        with mock.patch('logging.config.dictConfig'), \
            mock.patch('google.ads.google_ads.client._logger') as mock_logger, \
            mock.patch(
                'google.ads.google_ads.client.MessageToJson') as mock_formatter:
            mock_formatter.return_value = mock_json_message
            interceptor = self._create_test_interceptor()
            interceptor.intercept_unary_unary(
                mock_continuation_fn,
                mock_client_call_details,
                mock_request)

            mock_logger.warning.assert_called_once_with(
                interceptor._SUMMARY_LOG_LINE
                % (
                    self._MOCK_CUSTOMER_ID,
                    self._MOCK_ENDPOINT,
                    mock_client_call_details.method,
                    self._MOCK_REQUEST_ID,
                    True,
                    self._MOCK_ERROR_MESSAGE
                )
            )

            mock_logger.info.assert_called_once_with(
                interceptor._FULL_FAULT_LOG_LINE
                % (
                    self._MOCK_METHOD,
                    self._MOCK_ENDPOINT,
                    google.ads.google_ads.client.
                    _parse_metadata_to_json(mock_client_call_details.metadata),
                    mock_json_message,
                    google.ads.google_ads.client.
                    _parse_metadata_to_json(mock_trailing_metadata),
                    mock_json_message
                )
            )

    def test_get_initial_metadata(self):
        with mock.patch('logging.config.dictConfig'):
            mock_client_call_details = mock.Mock()
            mock_client_call_details.metadata = self._MOCK_INITIAL_METADATA
            interceptor = self._create_test_interceptor()
            result = interceptor._get_initial_metadata(mock_client_call_details)
            self.assertEqual(result, self._MOCK_INITIAL_METADATA)

    def test_get_initial_metadata_none(self):
        with mock.patch('logging.config.dictConfig'):
            mock_client_call_details = {}
            interceptor = self._create_test_interceptor()
            result = interceptor._get_initial_metadata(mock_client_call_details)
            self.assertEqual(result, None)

    def test_get_call_method(self):
        with mock.patch('logging.config.dictConfig'):
            mock_client_call_details = mock.Mock()
            mock_client_call_details.method = self._MOCK_METHOD
            interceptor = self._create_test_interceptor()
            result = interceptor._get_call_method(mock_client_call_details)
            self.assertEqual(result, self._MOCK_METHOD)

    def test_get_call_method_none(self):
        with mock.patch('logging.config.dictConfig'):
            mock_client_call_details = {}
            interceptor = self._create_test_interceptor()
            result = interceptor._get_call_method(mock_client_call_details)
            self.assertEqual(result, None)

    def test_get_request_id(self):
        with mock.patch('logging.config.dictConfig'):
            mock_response = self._get_mock_response()
            mock_exception = None
            interceptor = self._create_test_interceptor()
            result = interceptor._get_request_id(mock_response, mock_exception)
            self.assertEqual(result, self._MOCK_REQUEST_ID)

    def test_get_request_id_google_ads_failure(self):
        with mock.patch('logging.config.dictConfig'):
            mock_response = self._get_mock_response(failed=True)
            mock_exception = mock_response.exception()
            interceptor = self._create_test_interceptor()
            result = interceptor._get_request_id(mock_response, mock_exception)
            self.assertEqual(result, self._MOCK_REQUEST_ID)

    def test_get_request_id_transport_failure(self):
        with mock.patch('logging.config.dictConfig'):
            mock_response = self._get_mock_response(failed=True)
            mock_exception = mock_response.exception()
            # exceptions on transport errors have no request_id because they
            # don't interact with a server that can provide one.
            del mock_exception.request_id
            interceptor = self._create_test_interceptor()
            result = interceptor._get_request_id(mock_response, mock_exception)
            self.assertEqual(result, None)

    def test_parse_response_to_json(self):
        with mock.patch('logging.config.dictConfig'), \
            mock.patch(
                'google.ads.google_ads.client.MessageToJson') as mock_formatter:
            mock_response = self._get_mock_response()
            mock_exception = mock_response.exception()
            interceptor = self._create_test_interceptor()
            interceptor._parse_response_to_json(mock_response, mock_exception)
            mock_formatter.assert_called_once_with(mock_response.result())

    def test_parse_response_to_json_google_ads_failure(self):
        with mock.patch('logging.config.dictConfig'), \
            mock.patch(
                'google.ads.google_ads.client.MessageToJson') as mock_formatter:
            mock_response = mock.Mock()
            mock_exception = self._get_mock_exception()
            interceptor = self._create_test_interceptor()
            interceptor._parse_response_to_json(mock_response, mock_exception)
            mock_formatter.assert_called_once_with(mock_exception.failure)

    def test_parse_response_to_json_transport_failure(self):
        with mock.patch('logging.config.dictConfig'), \
            mock.patch(
                'google.ads.google_ads.client._parse_to_json') as mock_parser:
            mock_response = mock.Mock()
            mock_exception = self._get_mock_transport_exception()
            interceptor = self._create_test_interceptor()
            interceptor._parse_response_to_json(mock_response, mock_exception)
            mock_parser.assert_called_once_with(
                mock_exception.debug_error_string())

    def test_parse_response_to_json_unknown_failure(self):
        with mock.patch('logging.config.dictConfig'):
            mock_response = mock.Mock()
            mock_exception = mock.Mock()
            del mock_exception.failure
            del mock_exception.debug_error_string
            interceptor = self._create_test_interceptor()
            result = interceptor._parse_response_to_json(
                mock_response, mock_exception)
            self.assertEqual(result, '{}')

    def test_get_trailing_metadata(self):
        with mock.patch('logging.config.dictConfig'):
            mock_response = self._get_mock_response()
            mock_exception = mock_response.exception()
            interceptor = self._create_test_interceptor()
            result = interceptor._get_trailing_metadata(
                mock_response, mock_exception)
            self.assertEqual(result, self._MOCK_TRAILING_METADATA)

    def test_get_trailing_metadata_google_ads_failure(self):
        with mock.patch('logging.config.dictConfig'):
            mock_response = self._get_mock_response(failed=True)
            mock_exception = mock_response.exception()
            interceptor = self._create_test_interceptor()
            result = interceptor._get_trailing_metadata(
                mock_response, mock_exception)
            self.assertEqual(result, self._MOCK_TRAILING_METADATA)

    def test_get_trailing_metadata_transport_failure(self):
        with mock.patch('logging.config.dictConfig'):
            mock_response = self._get_mock_response(failed=True)
            mock_exception = mock_response.exception()
            del mock_exception.error
            interceptor = self._create_test_interceptor()
            result = interceptor._get_trailing_metadata(
                mock_response, mock_exception)
            self.assertEqual(result, self._MOCK_TRAILING_METADATA)

    def test_get_trailing_metadata_unknown_failure(self):
        with mock.patch('logging.config.dictConfig'):
            mock_response = {}
            mock_exception = {}
            interceptor = self._create_test_interceptor()
            result = interceptor._get_trailing_metadata(
                mock_response, mock_exception)
            self.assertEqual(result, tuple())


class ExceptionInterceptorTest(TestCase):
    """Tests for the google.ads.googleads.client.ExceptionInterceptor class."""

    def _create_test_interceptor(self):
        return google.ads.google_ads.client.ExceptionInterceptor()

    def test_init_(self):
        interceptor = self._create_test_interceptor()
        self.assertEqual(interceptor._RETRY_STATUS_CODES,
            (grpc.StatusCode.INTERNAL, grpc.StatusCode.RESOURCE_EXHAUSTED))

    def test_get_request_id(self):
        mock_metadata = (('request-id', '123456'),)
        interceptor = self._create_test_interceptor()
        result = interceptor._get_request_id(mock_metadata)
        self.assertEqual(result, '123456')

    def test_get_request_id_no_id(self):
        mock_metadata = (('another-key', 'another-val'),)
        interceptor = self._create_test_interceptor()
        result = interceptor._get_request_id(mock_metadata)
        self.assertEqual(result, None)

    def test_get_google_ads_failure(self):
        interceptor = self._create_test_interceptor()
        mock_metadata = ((interceptor._FAILURE_KEY,
            "\n \n\x02\x08\x10\x12\x1aInvalid customer ID '123'."),)
        result = interceptor._get_google_ads_failure(mock_metadata)
        self.assertIsInstance(result, error_protos.GoogleAdsFailure)

    def test_get_google_ads_failure_decode_error(self):
        interceptor = self._create_test_interceptor()
        mock_metadata = ((interceptor._FAILURE_KEY,
            "\n \n\x02\x08\x10Invalid customer ID '123'."),)
        result = interceptor._get_google_ads_failure(mock_metadata)
        self.assertEqual(result, None)

    def test_get_google_ads_failure_no_failure_key(self):
        mock_metadata = (('another-key', 'another-val'),)
        interceptor = self._create_test_interceptor()
        result = interceptor._get_google_ads_failure(mock_metadata)
        self.assertEqual(result, None)

    def test_get_google_ads_failure_with_None(self):
        interceptor = self._create_test_interceptor()
        result = interceptor._get_google_ads_failure(None)
        self.assertEqual(result, None)

    def test_handle_grpc_exception(self):
        """If exception is not retryable and is a GoogleAdsFailure convert to
           GoogleAdsException and raise.
        """
        class MockRpcError(grpc.RpcError):
            def code(self):
                return grpc.StatusCode.INVALID_ARGUMENT

            def trailing_metadata(self):
                return ((interceptor._FAILURE_KEY,
                    '\n \n\x02\x08\x10\x12\x1aInvalid customer ID \'123\'.'),)

        interceptor = self._create_test_interceptor()

        self.assertRaises(
            GoogleAdsException,
            interceptor._handle_grpc_exception,
            MockRpcError()
        )

    def test_handle_grpc_exception_retryable(self):
        """If exception is retryable raise as-is.
        """
        class MockRpcError(grpc.RpcError):
            def code(self):
                return grpc.StatusCode.INTERNAL

        interceptor = self._create_test_interceptor()

        self.assertRaises(
            MockRpcError,
            interceptor._handle_grpc_exception,
            MockRpcError()
        )

    def test_handle_grpc_exception_not_google_ads_failure(self):
        """If exception is not retryable and not a GoogleAdsFailure raise as-is.
        """
        class MockRpcError(grpc.RpcError):
            def code(self):
                return grpc.StatusCode.INVALID_ARGUMENT

            def trailing_metadata(self):
                return (('bad-failure-key', 'arbitrary-value'),)

        interceptor = self._create_test_interceptor()

        self.assertRaises(
            MockRpcError,
            interceptor._handle_grpc_exception,
            MockRpcError()
        )

    def test_intercept_unary_unary_response_is_exception(self):
        """If response.exception() is not None exception is handled."""
        mock_exception = grpc.RpcError()
        class MockResponse():
            def exception(self):
                return mock_exception

        mock_request = mock.Mock()
        mock_client_call_details = mock.Mock()
        mock_response = MockResponse()

        def mock_continuation(client_call_details, request):
            del client_call_details
            del request
            return mock_response

        interceptor = self._create_test_interceptor()

        with mock.patch.object(interceptor, '_handle_grpc_exception'):
            interceptor.intercept_unary_unary(
                mock_continuation, mock_client_call_details, mock_request)

            interceptor._handle_grpc_exception.assert_called_once_with(
                mock_exception)

    def test_intercept_unary_unary_response_is_successful(self):
        """If response.exception() is None response is returned."""
        class MockResponse():
            def exception(self):
                return None

        mock_request = mock.Mock()
        mock_client_call_details = mock.Mock()
        mock_response = MockResponse()

        def mock_continuation(client_call_details, request):
            del client_call_details
            del request
            return mock_response

        interceptor = self._create_test_interceptor()

        result = interceptor.intercept_unary_unary(
            mock_continuation, mock_client_call_details, mock_request)

        self.assertEqual(result, mock_response)
