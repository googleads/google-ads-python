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
"""Tests for the Exception gRPC Interceptor."""

import grpc
import mock
from unittest import TestCase

from google.ads.googleads.errors import GoogleAdsException
from google.ads.googleads import client as Client
from google.ads.googleads.interceptors import ExceptionInterceptor
from google.ads.googleads.interceptors.exception_interceptor import (
    _UnaryStreamWrapper,
)

latest_version = Client._DEFAULT_VERSION

_MOCK_FAILURE_VALUE = b"\n \n\x02\x08\x10\x12\x1aInvalid customer ID '123'."


class ExceptionInterceptorTest(TestCase):
    def _create_test_interceptor(self):
        """Creates and returns an ExceptionInterceptor instance

        Returns:
            An ExceptionInterceptor instance.
        """
        return ExceptionInterceptor(Client._DEFAULT_VERSION)

    def test_handle_grpc_failure(self):
        """Raises non-retryable GoogleAdsFailures as GoogleAdsExceptions."""
        mock_error_message = _MOCK_FAILURE_VALUE

        class MockRpcErrorResponse(grpc.RpcError):
            def code(self):
                return grpc.StatusCode.INVALID_ARGUMENT

            def trailing_metadata(self):
                return ((interceptor._failure_key, mock_error_message),)

            def exception(self):
                return self

        interceptor = self._create_test_interceptor()

        self.assertRaises(
            GoogleAdsException,
            interceptor._handle_grpc_failure,
            MockRpcErrorResponse(),
        )

    def test_handle_grpc_failure_retryable(self):
        """Raises retryable exceptions as-is."""

        class MockRpcErrorResponse(grpc.RpcError):
            def code(self):
                return grpc.StatusCode.INTERNAL

            def exception(self):
                return self

        interceptor = self._create_test_interceptor()

        self.assertRaises(
            MockRpcErrorResponse,
            interceptor._handle_grpc_failure,
            MockRpcErrorResponse(),
        )

    def test_handle_grpc_failure_not_google_ads_failure(self):
        """Raises as-is non-retryable non-GoogleAdsFailure exceptions."""

        class MockRpcErrorResponse(grpc.RpcError):
            def code(self):
                return grpc.StatusCode.INVALID_ARGUMENT

            def trailing_metadata(self):
                return (("bad-failure-key", "arbitrary-value"),)

            def exception(self):
                return self

        interceptor = self._create_test_interceptor()

        self.assertRaises(
            MockRpcErrorResponse,
            interceptor._handle_grpc_failure,
            MockRpcErrorResponse(),
        )

    def test_intercept_unary_unary_response_is_exception(self):
        """If response.exception() is not None exception is handled."""
        mock_exception = grpc.RpcError()

        class MockResponse:
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

        with mock.patch.object(interceptor, "_handle_grpc_failure"):
            interceptor.intercept_unary_unary(
                mock_continuation, mock_client_call_details, mock_request
            )

            interceptor._handle_grpc_failure.assert_called_once_with(
                mock_response
            )

    def test_intercept_unary_stream_response_is_exception(self):
        """Ensure errors raised from response iteration are handled/wrapped."""
        mock_exception = grpc.RpcError()

        class MockResponse:
            # Mock the response object so that it raises an error when
            # iterated upon.
            def __next__(self):
                raise mock_exception

        mock_request = mock.Mock()
        mock_client_call_details = mock.Mock()
        mock_response = MockResponse()

        def mock_continuation(client_call_details, request):
            del client_call_details
            del request
            return mock_response

        interceptor = self._create_test_interceptor()

        with mock.patch.object(interceptor, "_handle_grpc_failure"):
            response = interceptor.intercept_unary_stream(
                mock_continuation, mock_client_call_details, mock_request
            )

            # Ensure the returned value is a wrapped response object.
            self.assertIsInstance(response, _UnaryStreamWrapper)

            # Initiate an iteration of the wrapped response object
            next(response)

            # Check that the error handler method on the interceptor instance
            # was called as a result of the iteration.
            interceptor._handle_grpc_failure.assert_called_once_with(
                mock_response
            )

    def test_intercept_unary_unary_response_is_successful(self):
        """If response.exception() is None response is returned."""

        class MockResponse:
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
            mock_continuation, mock_client_call_details, mock_request
        )

        self.assertEqual(result, mock_response)

    def test_intercept_unary_stream_response_is_successful(self):
        """If response.exception() is None response is returned."""

        class MockResponse:
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

        result = interceptor.intercept_unary_stream(
            mock_continuation, mock_client_call_details, mock_request
        )

        # Ensure the returned value is a wrapped response object.
        self.assertIsInstance(result, _UnaryStreamWrapper)
