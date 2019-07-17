# Copyright 2019 Google LLC
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

from importlib import import_module

from google.protobuf.message import DecodeError
from grpc import UnaryUnaryClientInterceptor, StatusCode

from google.ads.google_ads.errors import GoogleAdsException

from .interceptor_mixin import InterceptorMixin


class ExceptionInterceptor(InterceptorMixin, UnaryUnaryClientInterceptor):
    """An interceptor that wraps rpc exceptions."""

    # Codes that are retried upon by google.api_core.
    _RETRY_STATUS_CODES = (StatusCode.INTERNAL, StatusCode.RESOURCE_EXHAUSTED)

    def __init__(self, api_version):
        """Initializes the ExceptionInterceptor

        Args:
            api_version: a str of the API version of the request.
        """
        self._api_version = api_version
        self._failure_key = (
            'google.ads.googleads.{}.errors.googleadsfailure-bin'.format(
                api_version))

    def _get_google_ads_failure(self, trailing_metadata):
        """Gets the Google Ads failure details if they exist.

        Args:
            trailing_metadata: a tuple of metadatum from the service response.

        Returns:
            A GoogleAdsFailure that describes how a GoogleAds API call failed.
            Returns None if either the trailing metadata of the request did not
            return the failure details, or if the GoogleAdsFailure fails to
            parse.
        """
        if trailing_metadata is not None:
            for kv in trailing_metadata:
                if kv[0] == self._failure_key:
                    try:
                        error_protos = import_module(
                            'google.ads.google_ads.%s.proto.errors' %
                                self._api_version)
                        ga_failure = error_protos.errors_pb2.GoogleAdsFailure()
                        ga_failure.ParseFromString(kv[1])
                        return ga_failure
                    except DecodeError:
                        return None

        return None

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
        status_code = response.code()
        exception = response.exception()

        if status_code not in self._RETRY_STATUS_CODES:
            trailing_metadata = response.trailing_metadata()
            google_ads_failure = self._get_google_ads_failure(trailing_metadata)

            if google_ads_failure:
                request_id = self.get_request_id_from_metadata(trailing_metadata)

                raise GoogleAdsException(exception, response,
                                         google_ads_failure, request_id)
            else:
                # Raise the original exception if not a GoogleAdsFailure.
                raise exception
        else:
            # Raise the original exception if error has status code
            # INTERNAL or RESOURCE_EXHAUSTED.
            raise exception

    def intercept_unary_unary(self, continuation, client_call_details, request):
        """Intercepts and wraps exceptions in the rpc response.

        Overrides abstract method defined in grpc.UnaryUnaryClientInterceptor.

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