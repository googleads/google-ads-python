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

import grpc

from grpc import UnaryUnaryClientInterceptor, UnaryStreamClientInterceptor

from .interceptor import Interceptor


class _UnaryStreamWrapper(grpc.Call, grpc.Future):
    def __init__(self, underlay_call, failure_handler):
        super().__init__()
        self._underlay_call = underlay_call
        self._failure_handler = failure_handler
        self._exception = None

    def initial_metadata(self):
        return self._underlay_call.initial_metadata()

    def trailing_metadata(self):
        return self._underlay_call.initial_metadata()

    def code(self):
        return self._underlay_call.code()

    def details(self):
        return self._underlay_call.details()

    def debug_error_string(self):
        return self._underlay_call.debug_error_string()

    def cancelled(self):
        return self._underlay_call.cancelled()

    def running(self):
        return self._underlay_call.running()

    def done(self):
        return self._underlay_call.done()

    def result(self, timeout=None):
        return self._underlay_call.result(timeout=timeout)

    def exception(self, timeout=None):
        if self._exception:
            return self._exception
        else:
            return self._underlay_call.exception(timeout=timeout)

    def traceback(self, timeout=None):
        return self._underlay_call.traceback(timeout=timeout)

    def add_done_callback(self, fn):
        return self._underlay_call.add_done_callback(fn)

    def add_callback(self, callback):
        return self._underlay_call.add_callback(callback)

    def is_active(self):
        return self._underlay_call.is_active()

    def time_remaining(self):
        return self._underlay_call.time_remaining()

    def cancel(self):
        return self._underlay_call.cancel()

    def __iter__(self):
        return self

    def __next__(self):
        try:
            return next(self._underlay_call)
        except StopIteration:
            raise
        except Exception:
            try:
                self._failure_handler(self._underlay_call)
            except Exception as e:
                self._exception = e
                raise e


class ExceptionInterceptor(
    Interceptor, UnaryUnaryClientInterceptor, UnaryStreamClientInterceptor
):
    """An interceptor that wraps rpc exceptions."""

    def __init__(self, api_version):
        """Initializes the ExceptionInterceptor.

        Args:
            api_version: a str of the API version of the request.
        """
        super().__init__(api_version)
        self._api_version = api_version

    def _handle_grpc_failure(self, response):
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
            RpcError: If the exception's is a gRPC exception but the trailing
                metadata is empty or is not indicative of a GoogleAdsException,
                or if the exception has a status code of INTERNAL or
                RESOURCE_EXHAUSTED.
            Exception: If not a GoogleAdsException or RpcException the error
                will be raised as-is.
        """
        raise self._get_error_from_response(response)

    def intercept_unary_unary(self, continuation, client_call_details, request):
        """Intercepts and wraps exceptions in the rpc response.

        Overrides abstract method defined in grpc.UnaryUnaryClientInterceptor.

        Args:
            continuation: a function to continue the request process.
            client_call_details: a grpc._interceptor._ClientCallDetails
                instance containing request metadata.
            request: a SearchGoogleAdsRequest or SearchGoogleAdsStreamRequest
                message class instance.

        Returns:
            A grpc.Call instance representing a service response.

        Raises:
            GoogleAdsException: If the exception's trailing metadata
                indicates that it is a GoogleAdsException.
            RpcError: If the exception's trailing metadata is empty or is not
                indicative of a GoogleAdsException, or if the exception has a
                status code of INTERNAL or RESOURCE_EXHAUSTED.
        """
        response = continuation(client_call_details, request)
        exception = response.exception()

        if exception:
            self._handle_grpc_failure(response)
        else:
            return response

    def intercept_unary_stream(
        self, continuation, client_call_details, request
    ):
        """Intercepts and wraps exceptions in the rpc response.

        Overrides abstract method defined in grpc.UnaryStreamClientInterceptor.

        Args:
            continuation: a function to continue the request process.
            client_call_details: a grpc._interceptor._ClientCallDetails
                instance containing request metadata.
            request: a SearchGoogleAdsRequest or SearchGoogleAdsStreamRequest
                message class instance.

        Returns:
            A grpc.Call instance representing a service response.

        Raises:
            GoogleAdsException: If the exception's trailing metadata
                indicates that it is a GoogleAdsException.
            RpcError: If the exception's trailing metadata is empty or is not
                indicative of a GoogleAdsException, or if the exception has a
                status code of INTERNAL or RESOURCE_EXHAUSTED.
        """
        response = continuation(client_call_details, request)
        return _UnaryStreamWrapper(response, self._handle_grpc_failure)
