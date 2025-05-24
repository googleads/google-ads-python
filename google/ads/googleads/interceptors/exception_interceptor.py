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
"""A gRPC Interceptor that is responsible for handling Google Ads API errors.

This class is initialized in the GoogleAdsClient and passed into a grpc
intercept_channel whenever a new service is initialized. It intercepts requests
to determine if a non-retryable Google Ads API error has been encountered. If
so it translates the error to a GoogleAdsFailure instance and raises it.
"""

from typing import Any, Callable, TypeVar, Union, NoReturn

import grpc
from grpc import (
    UnaryUnaryClientInterceptor,
    UnaryStreamClientInterceptor,
    ClientCallDetails,
    Call,
)

from google.ads.googleads.errors import GoogleAdsException
from .interceptor import Interceptor
from .response_wrappers import _UnaryStreamWrapper, _UnaryUnaryWrapper

# Define generic types for request and response messages.
# These are typically protobuf message instances.
RequestType = TypeVar("RequestType")
ResponseType = TypeVar("ResponseType")
# Type for the continuation callable in intercept_unary_unary
UnaryUnaryContinuation = Callable[
    [ClientCallDetails, RequestType], Union[Call, Any]
]
# Type for the continuation callable in intercept_unary_stream
UnaryStreamContinuation = Callable[
    [ClientCallDetails, RequestType], Union[grpc.Call, Any]
]


class ExceptionInterceptor(
    Interceptor, UnaryUnaryClientInterceptor, UnaryStreamClientInterceptor
):
    """An interceptor that wraps rpc exceptions."""

    _api_version: str
    _use_proto_plus: bool

    def __init__(self, api_version: str, use_proto_plus: bool = False):
        """Initializes the ExceptionInterceptor.

        Args:
            api_version: A str of the API version of the request.
            use_proto_plus: A boolean of whether returned messages should be
                proto_plus or protobuf.
        """
        super().__init__(api_version)
        self._api_version = api_version
        self._use_proto_plus = use_proto_plus

    def _handle_grpc_failure(self, response: grpc.Call) -> NoReturn:
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
            grpc.RpcError: If the exception's is a gRPC exception but the trailing
                metadata is empty or is not indicative of a GoogleAdsException,
                or if the exception has a status code of INTERNAL or
                RESOURCE_EXHAUSTED.
            Exception: If not a GoogleAdsException or RpcException the error
                will be raised as-is.
        """
        # Assuming _get_error_from_response is defined in the parent Interceptor
        # and raises an exception, so this method effectively has -> NoReturn
        raise self._get_error_from_response(response)  # type: ignore

    def intercept_unary_unary(
        self,
        continuation: UnaryUnaryContinuation[RequestType, ResponseType],
        client_call_details: ClientCallDetails,
        request: RequestType,
    ) -> Union[_UnaryUnaryWrapper, ResponseType, Call]:
        """Intercepts and wraps exceptions in the rpc response.

        Overrides abstract method defined in grpc.UnaryUnaryClientInterceptor.

        Args:
            continuation: a function to continue the request process.
            client_call_details: a grpc._interceptor._ClientCallDetails
                instance containing request metadata.
            request: A protobuf message class instance for the request.

        Returns:
            A _UnaryUnaryWrapper instance if successful, otherwise this method
            will raise an exception via _handle_grpc_failure. The actual
            return type from continuation can be grpc.Call or a future-like
            object that has an `exception()` method.

        Raises:
            GoogleAdsException: If the exception's trailing metadata
                indicates that it is a GoogleAdsException.
            grpc.RpcError: If the exception's trailing metadata is empty or is not
                indicative of a GoogleAdsException, or if the exception has a
                status code of INTERNAL or RESOURCE_EXHAUSTED.
        """
        response_call = continuation(client_call_details, request)
        # response_call is often a grpc.Call / grpc.Future in unary-unary.
        # It has an exception() method to check for errors.
        exception = response_call.exception()

        if exception:
            # _handle_grpc_failure is guaranteed to raise, so the execution stops here.
            self._handle_grpc_failure(response_call)
        else:
            # If there's no exception, wrap the successful response.
            return _UnaryUnaryWrapper(
                response_call, use_proto_plus=self._use_proto_plus
            )

    def intercept_unary_stream(
        self,
        continuation: UnaryStreamContinuation[RequestType, ResponseType],
        client_call_details: ClientCallDetails,
        request: RequestType,
    ) -> _UnaryStreamWrapper:
        """Intercepts and wraps exceptions in the rpc response.

        Overrides abstract method defined in grpc.UnaryStreamClientInterceptor.

        Args:
            continuation: a function to continue the request process.
            client_call_details: a grpc._interceptor._ClientCallDetails
                instance containing request metadata.
            request: A protobuf message class instance for the request.

        Returns:
            A _UnaryStreamWrapper instance that wraps the stream response.

        Raises:
            This method itself doesn't raise directly but passes
            _handle_grpc_failure to _UnaryStreamWrapper, which may raise if
            errors occur during streaming or if the initial call fails.
        """
        # In unary-stream, continuation returns an object that is an iterator
        # of responses, often a grpc.Call.
        response_stream_call = continuation(client_call_details, request)
        return _UnaryStreamWrapper(
            response_stream_call, # type: ignore
            self._handle_grpc_failure,
            use_proto_plus=self._use_proto_plus,
        )
