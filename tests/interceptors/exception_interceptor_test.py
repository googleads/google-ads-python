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
from unittest import mock
from unittest import TestCase, IsolatedAsyncioTestCase

from google.protobuf.message import Message as ProtobufMessageType
import proto

from fixtures.proto_plus_fixture import ProtoPlusFixture
from google.ads.googleads.errors import GoogleAdsException
from google.ads.googleads import client as Client
from google.ads.googleads.interceptors import ExceptionInterceptor
from google.ads.googleads.interceptors.exception_interceptor import (
    _UnaryStreamWrapper,
    _UnaryUnaryWrapper,
    _AsyncExceptionInterceptor,
    _AsyncUnaryUnaryCallWrapper,
    _AsyncUnaryStreamCallWrapper,
)

latest_version = Client._DEFAULT_VERSION

_MOCK_FAILURE_VALUE = b"\n \n\x02\x08\x10\x12\x1aInvalid customer ID '123'."


class ExceptionInterceptorTest(TestCase):
    def _create_test_interceptor(self, **kwargs):
        """Creates and returns an ExceptionInterceptor instance

        Returns:
            An ExceptionInterceptor instance.
        """
        return ExceptionInterceptor(Client._DEFAULT_VERSION, **kwargs)

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

        self.assertIsInstance(result, _UnaryUnaryWrapper)

    def test_intercept_unary_unary_proto_plus_proto(self):
        """Returns a proto_plus proto if use_proto_plus is True"""

        class MockResponse:
            def exception(self):
                return None

            def result(self):
                return ProtoPlusFixture()

        mock_request = mock.Mock()
        mock_client_call_details = mock.Mock()
        mock_response = MockResponse()

        def mock_continuation(client_call_details, request):
            del client_call_details
            del request
            return mock_response

        interceptor = self._create_test_interceptor(use_proto_plus=True)

        result = interceptor.intercept_unary_unary(
            mock_continuation, mock_client_call_details, mock_request
        )

        # Ensure the returned value is a wrapped response object.
        self.assertIsInstance(result, _UnaryUnaryWrapper)
        message = result.result()
        self.assertIsInstance(message, proto.Message)

    def test_intercept_unary_unary_protobuf_proto(self):
        """__next__ returns a protobuf proto if use_proto_plus is False"""

        class MockResponse:
            def exception(self):
                return None

            def result(self):
                return ProtoPlusFixture()

        mock_request = mock.Mock()
        mock_client_call_details = mock.Mock()
        mock_response = MockResponse()

        def mock_continuation(client_call_details, request):
            del client_call_details
            del request
            return mock_response

        interceptor = self._create_test_interceptor(use_proto_plus=False)

        result = interceptor.intercept_unary_unary(
            mock_continuation, mock_client_call_details, mock_request
        )

        # Ensure the returned value is a wrapped response object.
        self.assertIsInstance(result, _UnaryUnaryWrapper)
        message = result.result()
        self.assertIsInstance(message, ProtobufMessageType)

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

    def test_intercept_unary_stream_proto_plus_proto(self):
        """__next__ returns a proto_plus proto if use_proto_plus is True"""

        class MockResponse:
            def exception(self):
                return None

            def __next__(self):
                # Return a proto_plus proto object just as the current
                # generated services do.
                return ProtoPlusFixture()

        mock_request = mock.Mock()
        mock_client_call_details = mock.Mock()
        mock_response = MockResponse()

        def mock_continuation(client_call_details, request):
            del client_call_details
            del request
            return mock_response

        interceptor = self._create_test_interceptor(use_proto_plus=True)

        result = interceptor.intercept_unary_stream(
            mock_continuation, mock_client_call_details, mock_request
        )

        # Ensure the returned value is a wrapped response object.
        self.assertIsInstance(result, _UnaryStreamWrapper)
        message = next(result)
        self.assertIsInstance(message, proto.Message)

    def test_intercept_unary_stream_protobuf_proto(self):
        """__next__ returns a protobuf proto if use_proto_plus is False"""

        class MockResponse:
            def exception(self):
                return None

            def __next__(self):
                # Return a proto_plus proto object just as the current
                # generated services do.
                return ProtoPlusFixture()

        mock_request = mock.Mock()
        mock_client_call_details = mock.Mock()
        mock_response = MockResponse()

        def mock_continuation(client_call_details, request):
            del client_call_details
            del request
            return mock_response

        interceptor = self._create_test_interceptor(use_proto_plus=False)

        result = interceptor.intercept_unary_stream(
            mock_continuation, mock_client_call_details, mock_request
        )

        # Ensure the returned value is a wrapped response object.
        self.assertIsInstance(result, _UnaryStreamWrapper)
        message = next(result)
        self.assertIsInstance(message, ProtobufMessageType)


class AsyncExceptionInterceptorTest(IsolatedAsyncioTestCase):
    def _create_test_interceptor(self, **kwargs):
        """Creates and returns an AsyncExceptionInterceptor instance

        Returns:
            An AsyncExceptionInterceptor instance.
        """
        return _AsyncExceptionInterceptor(Client._DEFAULT_VERSION, **kwargs)

    async def test_handle_grpc_failure(self):
        """Raises non-retryable GoogleAdsFailures as GoogleAdsExceptions."""
        mock_error_message = _MOCK_FAILURE_VALUE

        class MockRpcErrorResponse(grpc.RpcError):
            def code(self):
                return grpc.StatusCode.INVALID_ARGUMENT

            async def trailing_metadata(self):
                return ((interceptor._failure_key, mock_error_message),)

            def exception(self):
                return self

        interceptor = self._create_test_interceptor()

        with self.assertRaises(GoogleAdsException):
            await interceptor._handle_grpc_failure_async(MockRpcErrorResponse())

    async def test_handle_grpc_failure_retryable(self):
        """Raises retryable exceptions as-is."""

        class MockRpcErrorResponse(grpc.RpcError):
            def code(self):
                return grpc.StatusCode.INTERNAL

            def exception(self):
                return self

        interceptor = self._create_test_interceptor()

        with self.assertRaises(MockRpcErrorResponse):
            await interceptor._handle_grpc_failure_async(MockRpcErrorResponse())

    async def test_handle_grpc_failure_not_google_ads_failure(self):
        """Raises as-is non-retryable non-GoogleAdsFailure exceptions."""

        class MockRpcErrorResponse(grpc.RpcError):
            def code(self):
                return grpc.StatusCode.INVALID_ARGUMENT

            async def trailing_metadata(self):
                return (("bad-failure-key", "arbitrary-value"),)

            def exception(self):
                return self

        interceptor = self._create_test_interceptor()

        with self.assertRaises(MockRpcErrorResponse):
            await interceptor._handle_grpc_failure_async(MockRpcErrorResponse())

    async def test_intercept_unary_unary_response_is_exception(self):
        """If response.exception() is not None exception is handled."""
        mock_exception = grpc.RpcError()

        class MockCall:
            def __await__(self):
                if False:
                    yield
                raise mock_exception

        mock_request = mock.Mock()
        mock_client_call_details = mock.Mock()
        mock_call = MockCall()

        async def mock_continuation(client_call_details, request):
            return mock_call

        interceptor = self._create_test_interceptor()

        with mock.patch.object(
            interceptor, "_handle_grpc_failure_async"
        ) as mock_handle:
            wrapper = await interceptor.intercept_unary_unary(
                mock_continuation, mock_client_call_details, mock_request
            )

            try:
                await wrapper
            except grpc.RpcError:
                pass

            mock_handle.assert_called_once_with(mock_call)

    async def test_intercept_unary_stream_response_is_exception(self):
        """Ensure errors raised from response iteration are handled/wrapped."""
        mock_exception = grpc.RpcError()

        class MockCall:
            def __aiter__(self):
                async def _aiter():
                    if False:
                        yield
                    raise mock_exception

                return _aiter()

        mock_request = mock.Mock()
        mock_client_call_details = mock.Mock()
        mock_call = MockCall()

        async def mock_continuation(client_call_details, request):
            return mock_call

        interceptor = self._create_test_interceptor()

        with mock.patch.object(
            interceptor, "_handle_grpc_failure_async"
        ) as mock_handle:
            response = await interceptor.intercept_unary_stream(
                mock_continuation, mock_client_call_details, mock_request
            )

            # Ensure the returned value is a wrapped response object.
            self.assertIsInstance(response, _AsyncUnaryStreamCallWrapper)

            # Initiate an iteration of the wrapped response object
            try:
                async for _ in response:
                    # This loop body should not be entered because the exception
                    # is raised on the first attempt to get an item.
                    pass
            except grpc.RpcError:
                pass

            # Check that the error handler method on the interceptor instance
            # was called as a result of the iteration.
            mock_handle.assert_called_once_with(mock_call)

    async def test_intercept_unary_unary_response_is_successful(self):
        """If response.exception() is None response is returned."""

        class MockCall:
            def __await__(self):
                if False:
                    yield
                return ProtoPlusFixture()

        mock_request = mock.Mock()
        mock_client_call_details = mock.Mock()
        mock_call = MockCall()

        async def mock_continuation(client_call_details, request):
            return mock_call

        interceptor = self._create_test_interceptor(use_proto_plus=True)

        result = await interceptor.intercept_unary_unary(
            mock_continuation, mock_client_call_details, mock_request
        )

        self.assertIsInstance(result, _AsyncUnaryUnaryCallWrapper)
        response = await result
        self.assertIsInstance(response, proto.Message)

    async def test_intercept_unary_unary_proto_plus_proto(self):
        """Returns a proto_plus proto if use_proto_plus is True"""

        class MockCall:
            def __await__(self):
                if False:
                    yield
                return ProtoPlusFixture()

        mock_request = mock.Mock()
        mock_client_call_details = mock.Mock()
        mock_call = MockCall()

        async def mock_continuation(client_call_details, request):
            return mock_call

        interceptor = self._create_test_interceptor(use_proto_plus=True)

        result = await interceptor.intercept_unary_unary(
            mock_continuation, mock_client_call_details, mock_request
        )

        # Ensure the returned value is a wrapped response object.
        self.assertIsInstance(result, _AsyncUnaryUnaryCallWrapper)
        message = await result
        self.assertIsInstance(message, proto.Message)

    async def test_intercept_unary_unary_protobuf_proto(self):
        """__next__ returns a protobuf proto if use_proto_plus is False"""

        class MockCall:
            def __await__(self):
                if False:
                    yield
                return ProtoPlusFixture()

        mock_request = mock.Mock()
        mock_client_call_details = mock.Mock()
        mock_call = MockCall()

        async def mock_continuation(client_call_details, request):
            return mock_call

        interceptor = self._create_test_interceptor(use_proto_plus=False)

        result = await interceptor.intercept_unary_unary(
            mock_continuation, mock_client_call_details, mock_request
        )

        # Ensure the returned value is a wrapped response object.
        self.assertIsInstance(result, _AsyncUnaryUnaryCallWrapper)
        message = await result
        self.assertIsInstance(message, ProtobufMessageType)

    async def test_intercept_unary_stream_response_is_successful(self):
        """If response.exception() is None response is returned."""

        class MockCall:
            def __aiter__(self):
                async def _aiter():
                    yield "success"

                return _aiter()

        mock_request = mock.Mock()
        mock_client_call_details = mock.Mock()
        mock_call = MockCall()

        async def mock_continuation(client_call_details, request):
            return mock_call

        interceptor = self._create_test_interceptor()

        result = await interceptor.intercept_unary_stream(
            mock_continuation, mock_client_call_details, mock_request
        )

        # Ensure the returned value is a wrapped response object.
        self.assertIsInstance(result, _AsyncUnaryStreamCallWrapper)

    async def test_intercept_unary_stream_proto_plus_proto(self):
        """__next__ returns a proto_plus proto if use_proto_plus is True"""

        class MockCall:
            def __aiter__(self):
                async def _aiter():
                    yield ProtoPlusFixture()

                return _aiter()

        mock_request = mock.Mock()
        mock_client_call_details = mock.Mock()
        mock_call = MockCall()

        async def mock_continuation(client_call_details, request):
            return mock_call

        interceptor = self._create_test_interceptor(use_proto_plus=True)

        result = await interceptor.intercept_unary_stream(
            mock_continuation, mock_client_call_details, mock_request
        )

        # Ensure the returned value is a wrapped response object.
        self.assertIsInstance(result, _AsyncUnaryStreamCallWrapper)

        message = None
        found = False
        async for item in result:
            message = item
            found = True
            break  # We only need the first item

        self.assertTrue(found, "Iterator should have yielded at least one message")
        self.assertIsInstance(message, proto.Message)

    async def test_intercept_unary_stream_protobuf_proto(self):
        """__next__ returns a protobuf proto if use_proto_plus is False"""

        class MockCall:
            def __aiter__(self):
                async def _aiter():
                    yield ProtoPlusFixture()

                return _aiter()

        mock_request = mock.Mock()
        mock_client_call_details = mock.Mock()
        mock_call = MockCall()

        async def mock_continuation(client_call_details, request):
            return mock_call

        interceptor = self._create_test_interceptor(use_proto_plus=False)

        result = await interceptor.intercept_unary_stream(
            mock_continuation, mock_client_call_details, mock_request
        )

        # Ensure the returned value is a wrapped response object.
        self.assertIsInstance(result, _AsyncUnaryStreamCallWrapper)

        message = None
        found = False
        async for item in result:
            message = item
            found = True
            break  # We only need the first item

        self.assertTrue(found, "Iterator should have yielded at least one message")
        self.assertIsInstance(message, ProtobufMessageType)
