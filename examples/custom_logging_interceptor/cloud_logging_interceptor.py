# Copyright 2022 Google LLC
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
"""A custom gRPC Interceptor that logs requests and responses to Cloud Logging.

The custom interceptor object is passed into the get_service method of the
GoogleAdsClient. It intercepts requests and responses, parses them into a
human readable structure and logs them using the logging service instantiated
within the class (in this case, a Cloud Logging client).
"""

import logging
import time
from typing import Any, Callable, Dict, Optional, Union

import grpc
from google.cloud import logging as cloud_logging

from google.ads.googleads.interceptors import LoggingInterceptor, mask_message


class CloudLoggingInterceptor(LoggingInterceptor):
    """An interceptor that logs rpc request and response details to Google Cloud Logging.

    This class inherits logic from the LoggingInterceptor, which simplifies the
    implementation here. Some logic is required here in order to make the
    underlying logic work -- comments make note of this where applicable.
    NOTE: Inheriting from the LoggingInterceptor class could yield unexpected side
    effects. For example, if the LoggingInterceptor class is updated, this class would
    inherit the updated logic, which could affect its functionality. One option to avoid
    this is to inherit from the Interceptor class instead, and selectively copy whatever
    logic is needed from the LoggingInterceptor class."""

    # Define rpc_start and rpc_end attributes for timing RPCs.
    rpc_start: float
    rpc_end: float

    def __init__(
        self, api_version: str, logger_name: Optional[str] = "cloud_logging_interceptor"
    ) -> None:
        """Initializer for the CloudLoggingInterceptor.

        Args:
            api_version: a str of the API version of the request.
            logger_name: an optional str for the name of the logger.
        """
        super().__init__(logger=None, api_version=api_version)
        # Instantiate the Cloud Logging client.
        logging_client: cloud_logging.Client = cloud_logging.Client()
        self.logger: cloud_logging.Logger = logging_client.logger(logger_name)
        # Initialize endpoint attribute, will be set in log_request if needed
        self.endpoint: Optional[str] = None


    def log_successful_request(
        self,
        method: str,
        customer_id: Optional[str],
        metadata_json: str,
        request_id: str,
        request: Any,
        trailing_metadata_json: str,
        response: Union[grpc.Call, grpc.Future],
    ) -> None:
        """Handles logging of a successful request.

        Args:
            method: The method of the request.
            customer_id: The customer ID associated with the request.
            metadata_json: A JSON str of initial_metadata.
            request_id: A unique ID for the request provided in the response.
            request: An instance of a request proto message.
            trailing_metadata_json: A JSON str of trailing_metadata.
            response: A grpc.Call/grpc.Future instance.
        """
        # Retrieve and mask the RPC result from the response future.
        # This method is available from the LoggingInterceptor class.
        # Ensure self._cache is set in order for this to work.
        # The response result could contain up to 10,000 rows of data,
        # so consider truncating this value before logging it, to save
        # on data storage costs and maintain readability.
        result: Any = self.retrieve_and_mask_result(response)

        # elapsed_ms is the approximate elapsed time of the RPC, in milliseconds.
        # There are different ways to define and measure elapsed time, so use
        # whatever approach makes sense for your monitoring purposes.
        # rpc_start and rpc_end are set in the intercept_unary_* methods below.
        elapsed_ms: float = (self.rpc_end - self.rpc_start) * 1000

        debug_log: Dict[str, Any] = {
            "method": method,
            "host": metadata_json,
            "request_id": request_id,
            "request": str(request),
            "headers": trailing_metadata_json,
            "response": str(result),
            "is_fault": False,
            "elapsed_ms": elapsed_ms,
        }
        self.logger.log_struct(debug_log, severity="DEBUG")

        info_log: Dict[str, Any] = {
            "customer_id": customer_id,
            "method": method,
            "request_id": request_id,
            "is_fault": False,
            # Available from the Interceptor class.
            "api_version": self._api_version,
        }
        self.logger.log_struct(info_log, severity="INFO")

    def log_failed_request(
        self,
        method: str,
        customer_id: Optional[str],
        metadata_json: str,
        request_id: str,
        request: Any,
        trailing_metadata_json: str,
        response: Union[grpc.Call, grpc.Future],
    ) -> None:
        """Handles logging of a failed request.

        Args:
            method: The method of the request.
            customer_id: The customer ID associated with the request.
            metadata_json: A JSON str of initial_metadata.
            request_id: A unique ID for the request provided in the response.
            request: An instance of a request proto message.
            trailing_metadata_json: A JSON str of trailing_metadata.
            response: A grpc.Call/grpc.Future instance for failed requests.
        """
        exception: grpc.RpcError = self._get_error_from_response(response)
        exception_str: str = self._parse_exception_to_str(exception)
        fault_message: str = self._get_fault_message(exception)

        info_log: Dict[str, Any] = {
            "method": method,
            "endpoint": self.endpoint,
            "host": metadata_json,
            "request_id": request_id,
            "request": str(request),
            "headers": trailing_metadata_json,
            "exception": exception_str,
            "is_fault": True,
        }
        self.logger.log_struct(info_log, severity="INFO")

        error_log: Dict[str, Any] = {
            "method": method,
            "endpoint": self.endpoint,
            "request_id": request_id,
            "customer_id": customer_id,
            "is_fault": True,
            "fault_message": fault_message,
        }
        self.logger.log_struct(error_log, severity="ERROR")

    def intercept_unary_unary(
        self,
        continuation: Callable[[grpc.ClientCallDetails, Any], grpc.Call],
        client_call_details: grpc.ClientCallDetails,
        request: Any,
    ) -> Union[grpc.Call, grpc.Future]:
        """Intercepts and logs API interactions.

        Overrides abstract method defined in grpc.UnaryUnaryClientInterceptor.

        Args:
            continuation: a function to continue the request process.
            client_call_details: a grpc.ClientCallDetails instance containing
                request metadata.
            request: a SearchGoogleAdsRequest or SearchGoogleAdsStreamRequest
                message class instance.

        Returns:
            A grpc.Call/grpc.Future instance representing a service response.
        """
        # Set the rpc_end value to current time when RPC completes.
        def update_rpc_end(response_future: grpc.Future) -> None:
            self.rpc_end = time.perf_counter()

        # Capture precise clock time to later calculate approximate elapsed
        # time of the RPC.
        self.rpc_start = time.perf_counter()

        # The below call is REQUIRED.
        response: Union[grpc.Call, grpc.Future] = continuation(
            client_call_details, request
        )

        # Ensure response is a Future to add done callback
        if isinstance(response, grpc.Future):
            response.add_done_callback(update_rpc_end)
        elif isinstance(response, grpc.Call):
            # For synchronous calls, set rpc_end immediately after call returns
            self.rpc_end = time.perf_counter()


        self.log_request(client_call_details, request, response)

        # The below return is REQUIRED.
        return response

    def intercept_unary_stream(
        self,
        continuation: Callable[[grpc.ClientCallDetails, Any], grpc.Call],
        client_call_details: grpc.ClientCallDetails,
        request: Any,
    ) -> grpc.Call:
        """Intercepts and logs API interactions for Unary-Stream requests.

        Overrides abstract method defined in grpc.UnaryStreamClientInterceptor.

        Args:
            continuation: a function to continue the request process.
            client_call_details: a grpc.ClientCallDetails instance containing
                request metadata.
            request: a SearchGoogleAdsRequest or SearchGoogleAdsStreamRequest
                message class instance.

        Returns:
            A grpc.Call/grpc.Future instance representing a service response.
        """

        def on_rpc_complete(response_future: grpc.Future) -> None:
            self.rpc_end = time.perf_counter()
            self.log_request(client_call_details, request, response_future)

        # Capture precise clock time to later calculate approximate elapsed
        # time of the RPC.
        self.rpc_start = time.perf_counter()

        # The below call is REQUIRED.
        response: grpc.Call = continuation(client_call_details, request)

        # Set self._cache to the cache on the response wrapper in order to
        # access the streaming logs. This is REQUIRED in order to log streaming
        # requests.
        # The LoggingInterceptor class uses self._cache, ensure it's set.
        if hasattr(response, "get_cache"):
            self._cache = response.get_cache()
        else:
            # If get_cache is not available, this means the response object
            # is not the expected wrapper. Logging streaming responses might
            # not work as intended.
            logging.warning(
                "Response object does not have get_cache method. "
                "Streaming response logging might be affected."
            )


        # Ensure response is a Future to add done callback (though for streams it's usually a Call)
        if isinstance(response, grpc.Future):
             response.add_done_callback(on_rpc_complete)
        elif isinstance(response, grpc.Call):
            # For streaming calls, we might need to handle completion differently
            # or rely on the fact that log_request will be called as data streams.
            # For simplicity, we'll assume log_request is called appropriately
            # by the base class or that the stream completion will trigger a state
            # where rpc_end can be set if needed.
            # If the stream itself is a future (e.g. for server-side streaming RPCs that complete),
            # then a callback can be added.
            # For client-side streaming or bidi, it's more complex.
            # Here, we assume the LoggingInterceptor's handling of _cache
            # is sufficient for extracting stream data.
            pass


        # The below return is REQUIRED.
        return response
