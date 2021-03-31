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
"""Tests for the Logging gRPC Interceptor."""


from importlib import import_module
import json
import logging
from unittest import TestCase

import mock

from google.ads.googleads import client as Client
from google.ads.googleads.interceptors import LoggingInterceptor
import google.ads.googleads.interceptors.logging_interceptor as interceptor_module


default_version = Client._DEFAULT_VERSION
module_prefix = f"google.ads.googleads.{default_version}"

customer_service = import_module(
    f"{module_prefix}.services.types.customer_service"
)
google_ads_service = import_module(
    f"{module_prefix}.services.types.google_ads_service"
)
customer_user_access_service = import_module(
    f"{module_prefix}.services.types.customer_user_access_service"
)
customer_user_access = import_module(
    f"{module_prefix}.resources.types.customer_user_access"
)
customer_user_access_invitation = import_module(
    f"{module_prefix}.resources.types.customer_user_access_invitation"
)
change_event = import_module(f"{module_prefix}.resources.types.change_event")
feed = import_module(f"{module_prefix}.resources.types.feed")


class LoggingInterceptorTest(TestCase):
    """Tests for the google.ads.googleads.client.LoggingInterceptor class."""

    _MOCK_CONFIG = {"test": True}
    _MOCK_ENDPOINT = "www.test-endpoint.com"
    _MOCK_INITIAL_METADATA = [
        ("developer-token", "123456"),
        ("header", "value"),
    ]
    _MOCK_CUSTOMER_ID = "123456"
    _MOCK_REQUEST_ID = "654321xyz"
    _MOCK_METHOD = "test/method"
    _MOCK_TRAILING_METADATA = (("request-id", _MOCK_REQUEST_ID),)
    _MOCK_TRANSPORT_ERROR_METADATA = tuple()
    _MOCK_ERROR_MESSAGE = "Test error message"
    _MOCK_TRANSPORT_ERROR_MESSAGE = "Received RST_STREAM with error code 2"
    _MOCK_DEBUG_ERROR_STRING = '{"description":"Error received from peer"}'
    _MOCK_RESPONSE_MSG = google_ads_service.SearchGoogleAdsResponse()
    _MOCK_EXCEPTION = mock.Mock()
    _MOCK_ERROR = mock.Mock()
    _MOCK_FAILURE = mock.Mock()

    def _create_test_interceptor(
        self, logger=mock.Mock(), version=None, endpoint=_MOCK_ENDPOINT
    ):
        """Creates a LoggingInterceptor instance.

        Accepts parameters that are used to override defaults when needed
        for testing.

        Args:
            config: A dict configuration
            endpoint: A str representing an endpoint

        Returns:
            A LoggingInterceptor instance.
        """
        if not version:
            version = default_version

        return LoggingInterceptor(logger, version, endpoint)

    def _get_mock_client_call_details(self):
        """Generates a mock client_call_details object for use in tests.

        Returns:
            A Mock instance with "method" and "metadata" attributes.
        """
        mock_client_call_details = mock.Mock()
        mock_client_call_details.method = self._MOCK_METHOD
        mock_client_call_details.metadata = self._MOCK_INITIAL_METADATA
        return mock_client_call_details

    def _get_mock_request(self):
        """Generates a mock request object for use in tests.

        Returns:
            A Mock instance with a "customer_id" attribute.
        """
        mock_request = mock.Mock()
        mock_request.customer_id = self._MOCK_CUSTOMER_ID
        return mock_request

    def _get_trailing_metadata_fn(self):
        """Generates a mock trailing_metadata function used for testing.

        Returns:
            A function that returns a tuple of mock metadata.
        """

        def mock_trailing_metadata_fn():
            return self._MOCK_TRAILING_METADATA

        return mock_trailing_metadata_fn

    def _get_mock_exception(self):
        """Generates a mock GoogleAdsException exception instance for testing.

        Returns:
            A Mock instance with the following attributes - "message",
            "request_id", "failure", and "error." The "failure" attribute has an
            "error" attribute that is an array of mock error objects, and the
            "error" attribute is an object with a "trailing_metadata" method
            that returns a tuble of mock metadata.
        """
        exception = self._MOCK_EXCEPTION
        error = self._MOCK_ERROR
        error.message = self._MOCK_ERROR_MESSAGE
        exception.request_id = self._MOCK_REQUEST_ID
        exception.failure = self._MOCK_FAILURE
        exception.failure.errors = [error]
        exception.error = self._MOCK_ERROR
        exception.error.trailing_metadata = self._get_trailing_metadata_fn()
        return exception

    def _get_mock_transport_exception(self):
        """Generates a mock gRPC transport error.

        Specifically an error not generated by the Google Ads API and that
        is not an instance of GoogleAdsException.

        Returns:
            A Mock instance with mock "debug_error_string," "details," and
            "trailing_metadata" methods.
        """

        def _mock_debug_error_string():
            return self._MOCK_DEBUG_ERROR_STRING

        def _mock_details():
            return self._MOCK_TRANSPORT_ERROR_MESSAGE

        def _mock_trailing_metadata():
            return self._MOCK_TRANSPORT_ERROR_METADATA

        exception = mock.Mock()
        exception.debug_error_string = _mock_debug_error_string
        exception.details = _mock_details
        exception.trailing_metadata = _mock_trailing_metadata
        # These attributes are explicitly deleted because they will otherwise
        # get mocked automatically and not generate AttributeErrors that trigger
        # default values in certain helper methods.
        del exception.error
        del exception.failure
        del exception.request_id
        return exception

    def _get_mock_response(self, failed=False):
        """Generates a mock response object for use in tests.

        Accepts a "failed" param that tells the returned mocked response to
        mimic a failed response.

        Returns:
            A Mock instance with mock "exception" and "trailing_metadata"
            methods

        Args:
            failed: a bool indicating whether the mock response should be in a
                failed state or not. Default is False.
        """

        def mock_exception_fn():
            if failed:
                return self._get_mock_exception()
            return None

        def mock_result_fn():
            return self._MOCK_RESPONSE_MSG

        mock_response = mock.Mock()
        mock_response.exception = mock_exception_fn
        mock_response.trailing_metadata = self._get_trailing_metadata_fn()
        mock_response.result = mock_result_fn
        return mock_response

    def _get_mock_continuation_fn(self, fail=False):
        """Generates a mock continuation function for use in tests.

        Accepts a "failed" param that tell the function to return a failed
        mock response or not.

        Returns:
            A function that returns a mock response object.

        Args:
            failed: a bool indicating whether the function should return a
            response that mocks a failure.
        """

        def mock_continuation_fn(*args):
            mock_response = self._get_mock_response(fail)
            return mock_response

        return mock_continuation_fn

    def test_intercept_unary_unary_unconfigured(self):
        """No _logger methods should be called.

        When intercepting requests, no logging methods should be called if
        LoggingInterceptor was initialized without a configuration.
        """
        mock_client_call_details = self._get_mock_client_call_details()
        mock_continuation_fn = self._get_mock_continuation_fn()
        mock_request = self._get_mock_request()
        # Since logging configuration is global it needs to be reset here
        # so that state from previous tests does not affect these assertions
        logging.disable(logging.CRITICAL)
        logger_spy = mock.Mock(wraps=Client._logger)
        interceptor = LoggingInterceptor(logger_spy, default_version)
        interceptor.intercept_unary_unary(
            mock_continuation_fn, mock_client_call_details, mock_request
        )

        logger_spy.debug.assert_not_called()
        logger_spy.info.assert_not_called()
        logger_spy.warning.assert_not_called()

    def test_intercept_unary_stream_unconfigured(self):
        """No _logger methods should be called.

        When intercepting requests, no logging methods should be called if
        LoggingInterceptor was initialized without a configuration.
        """
        mock_client_call_details = self._get_mock_client_call_details()
        mock_continuation_fn = self._get_mock_continuation_fn()
        mock_request = self._get_mock_request()
        # Since logging configuration is global it needs to be reset here
        # so that state from previous tests does not affect these assertions
        logging.disable(logging.CRITICAL)
        logger_spy = mock.Mock(wraps=Client._logger)
        interceptor = LoggingInterceptor(logger_spy, default_version)
        interceptor.intercept_unary_stream(
            mock_continuation_fn, mock_client_call_details, mock_request
        )

        logger_spy.debug.assert_not_called()
        logger_spy.info.assert_not_called()
        logger_spy.warning.assert_not_called()

    def test_intercept_unary_unary_successful_request(self):
        """_logger.info and _logger.debug should be called.

        LoggingInterceptor should call _logger.info and _logger.debug with
        a specific str parameter when a request succeeds.
        """
        mock_client_call_details = self._get_mock_client_call_details()
        mock_continuation_fn = self._get_mock_continuation_fn()
        mock_request = self._get_mock_request()
        mock_response = mock_continuation_fn(
            mock_client_call_details, mock_request
        )
        mock_trailing_metadata = mock_response.trailing_metadata()

        with mock.patch("logging.config.dictConfig"), mock.patch(
            "google.ads.googleads.client._logger"
        ) as mock_logger:
            interceptor = self._create_test_interceptor(logger=mock_logger)
            interceptor.intercept_unary_unary(
                mock_continuation_fn, mock_client_call_details, mock_request
            )

            mock_logger.info.assert_called_once_with(
                interceptor._SUMMARY_LOG_LINE.format(
                    self._MOCK_CUSTOMER_ID,
                    self._MOCK_ENDPOINT,
                    mock_client_call_details.method,
                    self._MOCK_REQUEST_ID,
                    False,
                    None,
                )
            )

            initial_metadata = interceptor.parse_metadata_to_json(
                mock_client_call_details.metadata
            )
            trailing_metadata = interceptor.parse_metadata_to_json(
                mock_trailing_metadata
            )

            mock_logger.debug.assert_called_once_with(
                interceptor._FULL_REQUEST_LOG_LINE.format(
                    self._MOCK_METHOD,
                    self._MOCK_ENDPOINT,
                    initial_metadata,
                    mock_request,
                    trailing_metadata,
                    mock_response.result(),
                )
            )

    def test_intercept_unary_stream_successful_request(self):
        """_logger.info and _logger.debug should be called.

        LoggingInterceptor should call _logger.info and _logger.debug with
        a specific str parameter when a request succeeds.
        """
        mock_client_call_details = self._get_mock_client_call_details()
        mock_request = self._get_mock_request()
        mock_response = self._get_mock_response()
        mock_trailing_metadata = mock_response.trailing_metadata()

        def mock_add_done_callback(fn):
            fn(mock_response)

        mock_response.add_done_callback = mock_add_done_callback
        mock_continuation_fn = mock.Mock(return_value=mock_response)

        with mock.patch("logging.config.dictConfig"), mock.patch(
            "google.ads.googleads.client._logger"
        ) as mock_logger:
            interceptor = self._create_test_interceptor(logger=mock_logger)
            interceptor.intercept_unary_stream(
                mock_continuation_fn, mock_client_call_details, mock_request
            )

            mock_logger.info.assert_called_once_with(
                interceptor._SUMMARY_LOG_LINE.format(
                    self._MOCK_CUSTOMER_ID,
                    self._MOCK_ENDPOINT,
                    mock_client_call_details.method,
                    self._MOCK_REQUEST_ID,
                    False,
                    None,
                )
            )

            initial_metadata = interceptor.parse_metadata_to_json(
                mock_client_call_details.metadata
            )
            trailing_metadata = interceptor.parse_metadata_to_json(
                mock_trailing_metadata
            )

            mock_logger.debug.assert_called_once_with(
                interceptor._FULL_REQUEST_LOG_LINE.format(
                    self._MOCK_METHOD,
                    self._MOCK_ENDPOINT,
                    initial_metadata,
                    mock_request,
                    trailing_metadata,
                    mock_response.result(),
                )
            )

    def test_intercept_unary_unary_failed_request(self):
        """_logger.warning and _logger.info should be called.

        LoggingInterceptor should call _logger.warning and _logger.info with
        a specific str parameter when a request fails.
        """
        mock_client_call_details = self._get_mock_client_call_details()
        mock_continuation_fn = self._get_mock_continuation_fn(fail=True)
        mock_request = self._get_mock_request()

        with mock.patch("logging.config.dictConfig"), mock.patch(
            "google.ads.googleads.client._logger"
        ) as mock_logger:
            interceptor = self._create_test_interceptor(logger=mock_logger)
            mock_response = interceptor.intercept_unary_unary(
                mock_continuation_fn, mock_client_call_details, mock_request
            )

            mock_trailing_metadata = mock_response.trailing_metadata()

            mock_logger.warning.assert_called_once_with(
                interceptor._SUMMARY_LOG_LINE.format(
                    self._MOCK_CUSTOMER_ID,
                    self._MOCK_ENDPOINT,
                    mock_client_call_details.method,
                    self._MOCK_REQUEST_ID,
                    True,
                    self._MOCK_ERROR_MESSAGE,
                )
            )

            initial_metadata = interceptor.parse_metadata_to_json(
                mock_client_call_details.metadata
            )
            trailing_metadata = interceptor.parse_metadata_to_json(
                mock_trailing_metadata
            )

            mock_logger.info.assert_called_once_with(
                interceptor._FULL_FAULT_LOG_LINE.format(
                    self._MOCK_METHOD,
                    self._MOCK_ENDPOINT,
                    initial_metadata,
                    mock_request,
                    trailing_metadata,
                    mock_response.exception().failure,
                )
            )

    def test_intercept_unary_stream_failed_request(self):
        """_logger.warning and _logger.info should be called.

        LoggingInterceptor should call _logger.warning and _logger.info with
        a specific str parameter when a request fails.
        """
        mock_response = self._get_mock_response(failed=True)

        def mock_add_done_callback(fn):
            fn(mock_response)

        mock_client_call_details = self._get_mock_client_call_details()
        mock_request = self._get_mock_request()
        mock_response.add_done_callback = mock_add_done_callback
        mock_continuation_fn = mock.Mock(return_value=mock_response)

        with mock.patch("logging.config.dictConfig"), mock.patch(
            "google.ads.googleads.client._logger"
        ) as mock_logger:
            interceptor = self._create_test_interceptor(logger=mock_logger)
            mock_response = interceptor.intercept_unary_stream(
                mock_continuation_fn, mock_client_call_details, mock_request
            )

            mock_trailing_metadata = mock_response.trailing_metadata()

            mock_logger.warning.assert_called_once_with(
                interceptor._SUMMARY_LOG_LINE.format(
                    self._MOCK_CUSTOMER_ID,
                    self._MOCK_ENDPOINT,
                    mock_client_call_details.method,
                    self._MOCK_REQUEST_ID,
                    True,
                    self._MOCK_ERROR_MESSAGE,
                )
            )

            initial_metadata = interceptor.parse_metadata_to_json(
                mock_client_call_details.metadata
            )
            trailing_metadata = interceptor.parse_metadata_to_json(
                mock_trailing_metadata
            )

            mock_logger.info.assert_called_once_with(
                interceptor._FULL_FAULT_LOG_LINE.format(
                    self._MOCK_METHOD,
                    self._MOCK_ENDPOINT,
                    initial_metadata,
                    mock_request,
                    trailing_metadata,
                    mock_response.exception().failure,
                )
            )

    def test_get_initial_metadata(self):
        """_Returns a tuple of metadata from client_call_details."""
        with mock.patch("logging.config.dictConfig"):
            mock_client_call_details = mock.Mock()
            mock_client_call_details.metadata = self._MOCK_INITIAL_METADATA
            interceptor = self._create_test_interceptor()
            result = interceptor._get_initial_metadata(mock_client_call_details)
            self.assertEqual(result, self._MOCK_INITIAL_METADATA)

    def test_get_initial_metadata_none(self):
        """Returns an empty tuple if initial_metadata isn't present."""
        with mock.patch("logging.config.dictConfig"):
            mock_client_call_details = {}
            interceptor = self._create_test_interceptor()
            result = interceptor._get_initial_metadata(mock_client_call_details)
            self.assertEqual(result, self._MOCK_TRANSPORT_ERROR_METADATA)

    def test_get_call_method(self):
        """Returns a str of the call method from client_call_details."""
        with mock.patch("logging.config.dictConfig"):
            mock_client_call_details = mock.Mock()
            mock_client_call_details.method = self._MOCK_METHOD
            interceptor = self._create_test_interceptor()
            result = interceptor._get_call_method(mock_client_call_details)
            self.assertEqual(result, self._MOCK_METHOD)

    def test_get_call_method_none(self):
        """Returns None if method is not present on client_call_details."""
        with mock.patch("logging.config.dictConfig"):
            mock_client_call_details = {}
            interceptor = self._create_test_interceptor()
            result = interceptor._get_call_method(mock_client_call_details)
            self.assertEqual(result, None)

    def test_parse_exception_to_str_transport_failure(self):
        """ Calls _format_json_object with error obj's debug_error_string."""
        interceptor = self._create_test_interceptor()

        with mock.patch("logging.config.dictConfig"), mock.patch.object(
            interceptor, "format_json_object"
        ) as mock_parser:
            mock_exception = self._get_mock_transport_exception()
            interceptor._parse_exception_to_str(mock_exception)
            mock_parser.assert_called_once_with(
                json.loads(self._MOCK_DEBUG_ERROR_STRING)
            )

    def test_parse_exception_to_str_unknown_failure(self):
        """Returns an empty JSON string if nothing can be parsed to JSON."""
        with mock.patch("logging.config.dictConfig"):
            mock_exception = mock.Mock()
            del mock_exception.failure
            del mock_exception.debug_error_string
            interceptor = self._create_test_interceptor()
            result = interceptor._parse_exception_to_str(mock_exception)
            self.assertEqual(result, "{}")

    def test_get_trailing_metadata(self):
        """Retrieves metadata from a response object."""
        with mock.patch("logging.config.dictConfig"):
            mock_response = self._get_mock_response()
            interceptor = self._create_test_interceptor()
            result = interceptor._get_trailing_metadata(mock_response)
            self.assertEqual(result, self._MOCK_TRAILING_METADATA)

    def test_get_trailing_metadata_google_ads_failure(self):
        """Retrieves metadata from a failed response."""
        with mock.patch("logging.config.dictConfig"):
            mock_response = self._get_mock_response(failed=True)
            del mock_response.trailing_metadata
            interceptor = self._create_test_interceptor()
            result = interceptor._get_trailing_metadata(mock_response)
            self.assertEqual(result, self._MOCK_TRAILING_METADATA)

    def test_get_trailing_metadata_transport_failure(self):
        """Retrieves metadata from a transport error."""
        with mock.patch("logging.config.dictConfig"):

            def mock_transport_exception():
                return self._get_mock_transport_exception()

            mock_response = mock.Mock()
            del mock_response.trailing_metadata
            mock_response.exception = mock_transport_exception
            interceptor = self._create_test_interceptor()
            result = interceptor._get_trailing_metadata(mock_response)
            self.assertEqual(result, tuple())

    def test_get_trailing_metadata_unknown_failure(self):
        """Returns an empty tuple if metadata cannot be found."""
        with mock.patch("logging.config.dictConfig"):

            def mock_unknown_exception():
                # using a mock transport exception but deleting the
                # trailing_metadata attribute to simulate an unknown error type
                exception = self._get_mock_transport_exception()
                del exception.trailing_metadata
                return exception

            mock_response = mock.Mock()
            del mock_response.trailing_metadata
            mock_response.exception = mock_unknown_exception
            interceptor = self._create_test_interceptor()
            result = interceptor._get_trailing_metadata(mock_response)
            self.assertEqual(result, tuple())

    def test_get_fault_message(self):
        """Returns None if an error message cannot be found."""
        with mock.patch("logging.config.dictConfig"):
            mock_exception = None
            interceptor = self._create_test_interceptor()
            result = interceptor._get_fault_message(mock_exception)
            self.assertEqual(result, None)

    def test_get_fault_message_google_ads_failure(self):
        """Retrieves an error message from a GoogleAdsException."""
        with mock.patch("logging.config.dictConfig"):
            mock_exception = self._get_mock_exception()
            interceptor = self._create_test_interceptor()
            result = interceptor._get_fault_message(mock_exception)
            self.assertEqual(result, self._MOCK_ERROR_MESSAGE)

    def test_get_fault_message_transport_failure(self):
        """Retrieves an error message from a transport error object."""
        with mock.patch("logging.config.dictConfig"):
            mock_exception = self._get_mock_transport_exception()
            interceptor = self._create_test_interceptor()
            result = interceptor._get_fault_message(mock_exception)
            self.assertEqual(result, self._MOCK_TRANSPORT_ERROR_MESSAGE)

    def test_get_customer_id_not_present(self):
        """Returns None if request has no customer_id or resource_name."""
        mock_request = {}
        interceptor = self._create_test_interceptor()
        self.assertEqual(interceptor._get_customer_id(mock_request), None)

    def test_get_customer_id(self):
        """Retrieves a customer_id from a request object."""
        mock_request = self._get_mock_request()
        interceptor = self._create_test_interceptor()
        self.assertEqual(
            interceptor._get_customer_id(mock_request), self._MOCK_CUSTOMER_ID
        )

    def test_get_customer_id_from_resource_name(self):
        """Retrieves a customer_id from a request object via resource_name."""
        resource_name = f"customers/{self._MOCK_CUSTOMER_ID}"
        mock_request = customer_service.GetCustomerRequest(
            resource_name=resource_name
        )
        interceptor = self._create_test_interceptor()
        self.assertEqual(
            interceptor._get_customer_id(mock_request), self._MOCK_CUSTOMER_ID
        )

    def test_get_customer_id_from_invalid_resource_name(self):
        """Returns None for a resource_name not starting with 'customers'."""
        resource_name = f"languageConstants/{self._MOCK_CUSTOMER_ID}"
        mock_request = customer_service.GetCustomerRequest(
            resource_name=resource_name
        )
        interceptor = self._create_test_interceptor()
        self.assertEqual(interceptor._get_customer_id(mock_request), None)

    def test_copy_message(self):
        """Creates a copy of the given message."""
        message = customer_user_access.CustomerUserAccess()
        copy = interceptor_module._copy_message(message)
        self.assertIsInstance(copy, message.__class__)
        self.assertIsNot(message, copy)

    def test_mask_message_fields(self):
        """Returns a copy of the message with named fields masked."""
        message = customer_user_access.CustomerUserAccess()
        message.email_address = "test@test.com"
        message.inviter_user_email_address = "inviter@test.com"
        copy = interceptor_module._mask_message_fields(
            ["email_address", "inviter_user_email_address"], message, "REDACTED"
        )
        self.assertIsInstance(copy, message.__class__)
        self.assertIsNot(message, copy)
        self.assertEqual(copy.email_address, "REDACTED")
        self.assertEqual(copy.inviter_user_email_address, "REDACTED")

    def test_mask_message_fields_nested(self):
        """Masks nested fields on an object."""
        message = customer_user_access_service.MutateCustomerUserAccessRequest(
            operation=customer_user_access_service.CustomerUserAccessOperation(
                update=customer_user_access.CustomerUserAccess(
                    email_address="test@test.com",
                    inviter_user_email_address="inviter@test.com",
                )
            )
        )
        copy = interceptor_module._mask_message_fields(
            [
                "operation.update.email_address",
                "operation.update.inviter_user_email_address",
            ],
            message,
            "REDACTED",
        )
        self.assertIsInstance(copy, message.__class__)
        self.assertIsNot(message, copy)
        self.assertEqual(copy.operation.update.email_address, "REDACTED")
        self.assertEqual(
            copy.operation.update.inviter_user_email_address, "REDACTED"
        )

    def test_mask_message_fields_unset_field(self):
        """Field is not masked if it is not set."""
        message = customer_user_access.CustomerUserAccess()
        copy = interceptor_module._mask_message_fields(
            ["email_address"], message, "REDACTED"
        )
        self.assertFalse("email_address" in copy)

    def test_mask_message_fields_unset_nested(self):
        """Nested field is not masked if it is not set."""
        message = customer_user_access_service.MutateCustomerUserAccessRequest()
        copy = interceptor_module._mask_message_fields(
            [
                "operation.update.email_address",
                "operation.update.inviter_user_email_address",
            ],
            message,
            "REDACTED",
        )
        self.assertFalse("email_address" in copy.operation.update)
        self.assertFalse("inviter_user_email_address" in copy.operation.update)

    def test_mask_message_fields_bad_field_name(self):
        """No error is raised if a given field is not defined on the message."""
        message = customer_user_access.CustomerUserAccess()
        copy = interceptor_module._mask_message_fields(
            ["bad_name"], message, "REDACTED"
        )
        self.assertFalse("email_address" in copy)
        self.assertFalse("inviter_user_email_address" in copy)

    def test_mask_message_fields_bad_nested_field_name(self):
        """No error is raised if a nested field is not defined."""
        message = customer_user_access.CustomerUserAccess()
        copy = interceptor_module._mask_message_fields(
            ["bad_name.another_bad.yet_another"], message, "REDACTED"
        )
        self.assertFalse("email_address" in copy)
        self.assertFalse("inviter_user_email_address" in copy)

    def test_mask_search_google_ads_response(self):
        """Copies and masks a SearchGoogleAdsResponse message instance."""
        response = google_ads_service.SearchGoogleAdsResponse()
        row = google_ads_service.GoogleAdsRow(
            customer_user_access=customer_user_access.CustomerUserAccess(
                email_address="test@test.com"
            )
        )
        response.results.append(row)
        copy = interceptor_module._mask_message(response, "REDACTED")
        self.assertIsInstance(copy, response.__class__)
        self.assertIsNot(response, copy)
        self.assertEqual(
            copy.results[0].customer_user_access.email_address, "REDACTED"
        )

    def test_mask_search_google_ads_stream_response(self):
        """Copies and masks a SearchGoogleAdsStreamResponse message instance."""
        response = google_ads_service.SearchGoogleAdsStreamResponse()
        row = google_ads_service.GoogleAdsRow(
            customer_user_access=customer_user_access.CustomerUserAccess(
                email_address="test@test.com"
            )
        )
        response.results.append(row)
        copy = interceptor_module._mask_message(response, "REDACTED")
        self.assertIsInstance(copy, response.__class__)
        self.assertIsNot(response, copy)
        self.assertEqual(
            copy.results[0].customer_user_access.email_address, "REDACTED"
        )

    def test_mask_search_change_event(self):
        """Masks ChangeEvent messages found on a SearchStream response."""
        response = google_ads_service.SearchGoogleAdsStreamResponse()
        row = google_ads_service.GoogleAdsRow(
            change_event=change_event.ChangeEvent(user_email="test@test.com")
        )
        response.results.append(row)
        copy = interceptor_module._mask_message(response, "REDACTED")
        self.assertEqual(copy.results[0].change_event.user_email, "REDACTED")

    def test_mask_search_places_location_feed_data(self):
        """Masks Feed.places_location_feed_data on a SearchStream response."""
        response = google_ads_service.SearchGoogleAdsStreamResponse()
        row = google_ads_service.GoogleAdsRow(
            feed=feed.Feed(
                places_location_feed_data=feed.Feed.PlacesLocationFeedData(
                    email_address="test@test.com"
                )
            )
        )
        response.results.append(row)
        copy = interceptor_module._mask_message(response, "REDACTED")
        self.assertEqual(
            copy.results[0].feed.places_location_feed_data.email_address,
            "REDACTED",
        )

    def test_mask_customer_user_access(self):
        """Copies and masks a CustomerUserAccess message instance."""
        customer_user_access_obj = customer_user_access.CustomerUserAccess(
            email_address="test@test.com",
            inviter_user_email_address="inviter@test.com",
        )
        copy = interceptor_module._mask_message(
            customer_user_access_obj, "REDACTED"
        )
        self.assertIsInstance(copy, customer_user_access_obj.__class__)
        self.assertIsNot(copy, customer_user_access_obj)
        self.assertEqual(copy.email_address, "REDACTED")
        self.assertEqual(copy.inviter_user_email_address, "REDACTED")

    def test_mask_mutate_customer_user_access_request(self):
        """Copies and masks a MutateCustomerUserAccessRequest instance."""
        request = customer_user_access_service.MutateCustomerUserAccessRequest(
            operation=customer_user_access_service.CustomerUserAccessOperation(
                update=customer_user_access.CustomerUserAccess(
                    email_address="test@test.com",
                    inviter_user_email_address="inviter@test.com",
                )
            )
        )
        copy = interceptor_module._mask_message(request, "REDACTED")
        self.assertIsInstance(copy, request.__class__)
        self.assertIsNot(copy, request)
        self.assertEqual(copy.operation.update.email_address, "REDACTED")
        self.assertEqual(
            copy.operation.update.inviter_user_email_address, "REDACTED"
        )

    def test_mask_create_customer_client_request(self):
        """Copies and masks a CreateCustomerClientRequest instance."""
        request = customer_service.CreateCustomerClientRequest(
            email_address="test@test.com",
        )
        copy = interceptor_module._mask_message(request, "REDACTED")
        self.assertIsInstance(copy, request.__class__)
        self.assertIsNot(copy, request)
        self.assertEqual(copy.email_address, "REDACTED")

    def test_mask_places_location_feed_data(self):
        """Copies and masks a PlacesLocationFeedData instance."""
        message = feed.Feed(
            places_location_feed_data=feed.Feed.PlacesLocationFeedData(
                email_address="test@test.com"
            )
        )
        copy = interceptor_module._mask_message(message, "REDACTED")
        self.assertIsInstance(copy, message.__class__)
        self.assertIsNot(copy, message)
        self.assertEqual(
            copy.places_location_feed_data.email_address, "REDACTED"
        )

    def test_mask_customer_user_access_invitation_email(self):
        """Copies and masks a CustomerUserAccessInvitation instance."""
        message = customer_user_access_invitation.CustomerUserAccessInvitation(
            email_address="test@test.com"
        )
        copy = interceptor_module._mask_message(message, "REDACTED")
        self.assertIsInstance(copy, message.__class__)
        self.assertEqual(copy.email_address, "REDACTED")
