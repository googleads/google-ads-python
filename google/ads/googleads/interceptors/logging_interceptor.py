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
"""A gRPC Interceptor that is responsible for logging requests and responses.

This class is initialized in the GoogleAdsClient and passed into a grpc
intercept_channel whenever a new service is initialized. It intercepts requests
and responses, parses them into a human readable structure and logs them using
the passed in logger instance.
"""

from copy import deepcopy
from typing import (
    Any,
    Callable,
    Dict,
    Optional,
    Sequence,
    Tuple,
    TypeVar,
    Union,
)
import json
import logging

from google.protobuf.message import Message
from grpc import (
    Call,
    ClientCallDetails,
    Future,
    RpcError,
    UnaryUnaryClientInterceptor,
    UnaryStreamClientInterceptor,
)

from google.ads.googleads.errors import GoogleAdsException
from google.ads.googleads.interceptors.interceptor import Interceptor
from google.ads.googleads.interceptors.helpers import mask_message
# SimpleNamespace is not used in this file after inspection, so removing the import.

# Define generic types for request and response messages.
RequestType = TypeVar("RequestType", bound=Message)
ResponseType = TypeVar("ResponseType", bound=Message)

# Type for the continuation callable in intercept_unary_unary and intercept_unary_stream
UnaryContinuation = Callable[
    [ClientCallDetails, RequestType], Call
]  # Call is a Future-like object


class LoggingInterceptor(
    Interceptor, UnaryUnaryClientInterceptor, UnaryStreamClientInterceptor
):
    """An interceptor that logs rpc requests and responses."""

    _FULL_REQUEST_LOG_LINE: str = (
        "Request\n-------\nMethod: {}\nHost: {}\n"
        "Headers: {}\nRequest: {}\n\nResponse\n-------\n"
        "Headers: {}\nResponse: {}\n"
    )
    _FULL_FAULT_LOG_LINE: str = (
        "Request\n-------\nMethod: {}\nHost: {}\n"
        "Headers: {}\nRequest: {}\n\nResponse\n-------\n"
        "Headers: {}\nFault: {}\n"
    )
    _SUMMARY_LOG_LINE: str = (
        "Request made: ClientCustomerId: {}, Host: {}, "
        "Method: {}, RequestId: {}, IsFault: {}, "
        "FaultMessage: {}"
    )

    # Instance attributes
    endpoint: Optional[str]
    logger: logging.Logger
    _cache: Optional[Any] # Stores response cache for stream responses. Type is Any as structure is internal.
    # _api_version is inherited from Interceptor and typed there

    def __init__(
        self,
        logger: logging.Logger,
        api_version: str,
        endpoint: Optional[str] = None,
    ):
        """Initializer for the LoggingInterceptor.

        Args:
            logger: An instance of logging.Logger.
            api_version: A str of the API version of the request.
            endpoint: An optional str specifying the endpoint for requests.
        """
        super().__init__(api_version)
        self.endpoint = endpoint
        self.logger = logger
        # _cache is initialized in intercept_unary_stream, default to None here.
        self._cache = None

    def _get_trailing_metadata(
        self, response: Call
    ) -> Sequence[Tuple[str, Union[str, bytes]]]:
        """Retrieves trailing metadata from a response object.

        If the exception is a GoogleAdsException the trailing metadata will be
        on its error object, otherwise it will be on the response object.

        Returns:
            A sequence of metadata tuples (key, value) where value can be
            str or bytes.

        Args:
            response: A grpc.Call/grpc.Future instance.
        """
        trailing_metadata: Optional[Sequence[Tuple[str, Union[str, bytes]]]] = None
        try:
            trailing_metadata = response.trailing_metadata()
        except AttributeError: # pragma: no cover
            # This might occur if response is not a standard gRPC Call object.
            pass

        if not trailing_metadata:
            # Try to get from exception if response indicates one
            exception = response.exception()
            if exception:
                # get_trailing_metadata_from_interceptor_exception expects Any
                return self.get_trailing_metadata_from_interceptor_exception(
                    exception
                )
        
        return trailing_metadata if trailing_metadata is not None else tuple()


    def _get_initial_metadata(
        self, client_call_details: ClientCallDetails
    ) -> Sequence[Tuple[str, Union[str, bytes]]]:
        """Retrieves the initial metadata from client_call_details.

        Returns an empty tuple if metadata isn't present on the
        client_call_details object.

        Returns:
            A sequence of metadata tuples (key, value) where value can be
            str or bytes.

        Args:
            client_call_details: An instance of grpc.ClientCallDetails.
        """
        # client_call_details.metadata is Optional[Sequence[Tuple[str, AnyStr]]]
        # AnyStr is Union[str, bytes].
        metadata = getattr(client_call_details, "metadata", None)
        return metadata if metadata is not None else tuple()

    def _get_call_method(
        self, client_call_details: ClientCallDetails
    ) -> Optional[str]:
        """Retrieves the call method from client_call_details.

        Returns None if the method is not present on the client_call_details
        object.

        Returns:
            A str with the call method or None if it isn't present.

        Args:
            client_call_details: An instance of grpc.ClientCallDetails.
        """
        # client_call_details.method is str
        return getattr(client_call_details, "method", None)

    def _get_customer_id(self, request: RequestType) -> Optional[str]:
        """Retrieves the customer_id from the grpc request.

        Returns None if a customer_id is not present on the request object.

        Returns:
            A str with the customer id from the request or None if it isn't
            present.

        Args:
            request: An instance of a request proto message (TypeVar RequestType).
        """
        customer_id: Optional[str] = None
        if hasattr(request, "customer_id"):
            customer_id = getattr(request, "customer_id", None)
        elif hasattr(request, "resource_name"):
            # Attempt to parse customer_id from resource_name
            # e.g. "customers/12345/campaigns/67890"
            resource_name_str = getattr(request, "resource_name", "")
            if isinstance(resource_name_str, str):
                segments = resource_name_str.split("/")
                if len(segments) > 1 and segments[0] == "customers":
                    customer_id = segments[1]
        return customer_id

    def _parse_exception_to_str(
        self, exception: Union[GoogleAdsException, RpcError, Exception]
    ) -> str:
        """Parses response exception object to str for logging.

        Returns:
            A str representing an exception from the API.

        Args:
            exception: An RpcError, GoogleAdsException, or generic Exception instance.
        """
        if isinstance(exception, GoogleAdsException):
            # GoogleAdsException has a 'failure' attribute (GoogleAdsFailure proto)
            # and a 'message' attribute. str(exception) should be comprehensive.
            # Accessing .failure directly can be complex if it's deeply nested.
            # Using the string representation of GoogleAdsFailure if available.
            if hasattr(exception, "failure") and exception.failure:
                return str(exception.failure)
            else: # Fallback for GoogleAdsException without specific failure details
                return str(exception)
        elif isinstance(exception, RpcError):
            # RpcError has debug_error_string(), details(), code()
            # Try to get a structured JSON if possible from debug_error_string
            try:
                debug_str = exception.debug_error_string()
                if debug_str:
                    # debug_error_string is often JSON-like but not always perfect JSON
                    # We attempt to parse it as JSON, otherwise, use it as is.
                    try:
                        return self.format_json_object(json.loads(debug_str))
                    except json.JSONDecodeError:
                        # If not JSON, return the raw debug string or a formatted version
                        return f'{{"debug_error_string": "{debug_str}"}}'
            except AttributeError:
                pass # Fall through if debug_error_string is not available
            # Fallback to details() or standard string representation
            if hasattr(exception, "details") and callable(exception.details):
                details = exception.details()
                if details: return str(details)
            return str(exception) # Generic RpcError string
        else: # For other types of exceptions
            return str(exception)


    def _get_fault_message(
        self, exception: Union[GoogleAdsException, RpcError, Exception]
    ) -> Optional[str]:
        """Retrieves a fault/error message from an exception object.

        Returns None if no error message can be found on the exception.

        Returns:
            A str with an error message or None if one cannot be found.

        Args:
            exception: An RpcError, GoogleAdsException, or generic Exception instance.
        """
        if isinstance(exception, GoogleAdsException):
            # GoogleAdsException often has a list of errors in failure.errors
            if hasattr(exception, "failure") and hasattr(
                exception.failure, "errors"
            ):
                if exception.failure.errors and hasattr(
                    exception.failure.errors[0], "message"
                ):
                    return str(exception.failure.errors[0].message)
            # Fallback to the main message of GoogleAdsException
            return str(exception.message) if hasattr(exception, "message") else str(exception)
        elif isinstance(exception, RpcError):
            # RpcError has a details() method
            if hasattr(exception, "details") and callable(exception.details):
                details = exception.details()
                if details: return str(details)
            return None # Or str(exception) if a general message is desired
        else: # For other types of exceptions
            return str(exception)


    def log_successful_request(
        self,
        method: Optional[str],
        customer_id: Optional[str],
        metadata_json: str,
        request_id: Optional[str],
        request: RequestType, # Masked request
        trailing_metadata_json: str,
        response_call: Call, # The gRPC Call/Future object
    ) -> None:
        """Handles logging of a successful request.

        Args:
            method: The method of the request.
            customer_id: The customer ID associated with the request.
            metadata_json: A JSON str of initial_metadata.
            request_id: A unique ID for the request provided in the response.
            request: An instance of a (masked) request proto message.
            trailing_metadata_json: A JSON str of trailing_metadata.
            response_call: The grpc.Call/grpc.Future instance for the response.
        """
        # Retrieve and mask the actual response message (result of the call)
        # The 'response' parameter was the Call object. We need its result.
        masked_result_str: str
        try:
            # retrieve_and_mask_result expects a Call object
            actual_response_message = self.retrieve_and_mask_result(response_call)
            # Convert the (potentially masked) protobuf message to a string for logging
            # This assumes actual_response_message is a protobuf Message or already a string
            if isinstance(actual_response_message, Message):
                masked_result_str = str(actual_response_message)
            else: # If it's already stringified/masked by retrieve_and_mask_result
                masked_result_str = actual_response_message
        except Exception: # pragma: no cover
            masked_result_str = "[Could not retrieve or mask response result]"


        if self.logger.isEnabledFor(logging.DEBUG):
            # request is already masked and converted to str in log_request
            self.logger.debug(
                self._FULL_REQUEST_LOG_LINE.format(
                    method,
                    self.endpoint,
                    metadata_json,
                    str(request), # Ensure request (masked proto) is string
                    trailing_metadata_json,
                    masked_result_str,
                )
            )

        if self.logger.isEnabledFor(logging.INFO):
            self.logger.info(
                self._SUMMARY_LOG_LINE.format(
                    customer_id if customer_id else "N/A", # Ensure customer_id is not None
                    self.endpoint,
                    method,
                    request_id if request_id else "N/A", # Ensure request_id is not None
                    False,
                    "N/A", # No fault message for successful request
                )
            )


    def log_failed_request(
        self,
        method: Optional[str],
        customer_id: Optional[str],
        metadata_json: str,
        request_id: Optional[str],
        request: RequestType, # Masked request
        trailing_metadata_json: str,
        response_call: Call, # The gRPC Call/Future object with the exception
    ) -> None:
        """Handles logging of a failed request.

        Args:
            method: The method of the request.
            customer_id: The customer ID associated with the request.
            metadata_json: A JSON str of initial_metadata.
            request_id: A unique ID for the request provided in the response.
            request: An instance of a (masked) request proto message.
            trailing_metadata_json: A JSON str of trailing_metadata.
            response_call: The grpc.Call/grpc.Future instance containing the exception.
        """
        # _get_error_from_response expects a Call object
        exception = self._get_error_from_response(response_call)
        exception_str = self._parse_exception_to_str(exception)
        fault_message = self._get_fault_message(exception)

        # Note: Original code logged _FULL_FAULT_LOG_LINE at INFO level.
        # This seems more like a DEBUG level log, similar to _FULL_REQUEST_LOG_LINE.
        # Keeping original behavior for now.
        if self.logger.isEnabledFor(logging.INFO):
            # request is already masked and converted to str in log_request
            self.logger.info(
                self._FULL_FAULT_LOG_LINE.format(
                    method,
                    self.endpoint,
                    metadata_json,
                    str(request), # Ensure request (masked proto) is string
                    trailing_metadata_json,
                    exception_str,
                )
            )

        self.logger.warning(
            self._SUMMARY_LOG_LINE.format(
                customer_id if customer_id else "N/A",
                self.endpoint,
                method,
                request_id if request_id else "N/A",
                True, # IsFault
                fault_message if fault_message else "N/A",
            )
        )

    def log_request(
        self,
        client_call_details: ClientCallDetails,
        request: RequestType,
        response_call: Call,
    ) -> None:
        """Handles logging all requests.

        Args:
            client_call_details: An instance of grpc.ClientCallDetails.
            request: An instance of a request proto message.
            response_call: A grpc.Call/grpc.Future instance for the response.
        """
        method = self._get_call_method(client_call_details)
        # Retrieve customer_id from the original request before masking
        customer_id = self._get_customer_id(request)
        
        initial_metadata = self._get_initial_metadata(client_call_details)
        initial_metadata_json = self.parse_metadata_to_json(initial_metadata)
        
        trailing_metadata = self._get_trailing_metadata(response_call)
        # get_request_id_from_metadata expects Sequence[Tuple[str, str]]
        # Need to convert AnyStr values in trailing_metadata if they are bytes.
        str_trailing_metadata: List[Tuple[str, str]] = []
        for k, v_bytes_or_str in trailing_metadata:
            if isinstance(v_bytes_or_str, bytes):
                str_trailing_metadata.append((k, v_bytes_or_str.decode(errors="ignore")))
            else:
                str_trailing_metadata.append((k, v_bytes_or_str))
        request_id = self.get_request_id_from_metadata(str_trailing_metadata)
        trailing_metadata_json = self.parse_metadata_to_json(trailing_metadata)

        # Mask the request for logging. mask_message returns the same type as input.
        # It's important that request_for_logging is what's passed to log_successful/failed_request
        # if we want the logged request body to be the masked one.
        # The original 'request' object (unmasked) is used for _get_customer_id.
        request_for_logging: RequestType = mask_message(deepcopy(request), self._SENSITIVE_INFO_MASK)


        if response_call.exception():
            self.log_failed_request(
                method,
                customer_id,
                initial_metadata_json,
                request_id,
                request_for_logging, # Pass masked request
                trailing_metadata_json,
                response_call,
            )
        else:
            self.log_successful_request(
                method,
                customer_id,
                initial_metadata_json,
                request_id,
                request_for_logging, # Pass masked request
                trailing_metadata_json,
                response_call,
            )

    def intercept_unary_unary(
        self,
        continuation: UnaryContinuation[RequestType, ResponseType],
        client_call_details: ClientCallDetails,
        request: RequestType,
    ) -> Call:
        """Intercepts and logs API interactions.

        Overrides abstract method defined in grpc.UnaryUnaryClientInterceptor.

        Args:
            continuation: A function to continue the request process.
            client_call_details: A grpc.ClientCallDetails instance
                containing request metadata.
            request: A request proto message instance.

        Returns:
            A grpc.Call/grpc.Future instance representing a service response.
        """
        response_call = continuation(client_call_details, request)

        # Logging is done based on the final status of response_call (success/failure)
        # For unary-unary, this can be done after `continuation` returns,
        # by checking response_call.exception().
        # A callback is also an option if preferred for consistency with streams.
        if self.logger.isEnabledFor(logging.INFO) or self.logger.isEnabledFor(
            logging.DEBUG
        ) or self.logger.isEnabledFor(logging.WARNING): # Check any relevant log level
            self.log_request(client_call_details, request, response_call)
        
        return response_call


    def intercept_unary_stream(
        self,
        continuation: UnaryContinuation[RequestType, ResponseType],
        client_call_details: ClientCallDetails,
        request: RequestType,
    ) -> Call:
        """Intercepts and logs API interactions for Unary-Stream requests.

        Overrides abstract method defined in grpc.UnaryStreamClientInterceptor.

        Args:
            continuation: A function to continue the request process.
            client_call_details: A grpc.ClientCallDetails instance
                containing request metadata.
            request: A request proto message instance.

        Returns:
            A grpc.Call/grpc.Future instance representing a service response.
        """

        def on_rpc_complete(response_future: Union[Call, Future]) -> None:
            # This callback is for when the entire stream RPC is complete.
            # The response_future here represents the overall status of the call.
            if self.logger.isEnabledFor(logging.INFO) or self.logger.isEnabledFor(
                logging.DEBUG
            ) or self.logger.isEnabledFor(logging.WARNING): # Check any relevant log level
                # Ensure response_future is treated as Call for log_request
                if isinstance(response_future, Future) and not isinstance(response_future, Call):
                    # This path might need a mock/wrapper if log_request strictly needs Call methods
                    # not on Future, but generally Future is Call-like for exception/result.
                    # For now, assuming log_request can handle it or Future is Call-like enough.
                    pass # log_request will be called with this Future object
                self.log_request(client_call_details, request, response_future) # type: ignore

        response_call = continuation(client_call_details, request)
        
        # For streaming responses, the logging of the overall call (summary, fault)
        # should happen when the call is entirely done.
        response_call.add_done_callback(on_rpc_complete)
        
        # Store the cache if it exists, for retrieve_and_mask_result
        if hasattr(response_call, "get_cache"):
            self._cache = response_call.get_cache()
        else: # pragma: no cover
            self._cache = None # Ensure _cache is defined even if get_cache isn't present

        return response_call

    def retrieve_and_mask_result(self, response_call: Call) -> Any:
        """If the cache is populated (for streams), mask the cached initial
        stream response object. Otherwise, mask the non-streaming response result.

        Args:
            response_call: A grpc.Call/grpc.Future instance.

        Returns:
            A masked response message (str or protobuf Message) or a string
            indicating an error in retrieval.
        """
        result_to_mask: Any = None
        # For stream responses, an initial response might be cached.
        if self._cache and hasattr(self._cache, "initial_response_object"):
            result_to_mask = self._cache.initial_response_object
        
        if result_to_mask is None:
            try:
                # For unary calls, or if no initial cached response for streams.
                if callable(getattr(response_call, "result", None)):
                    result_to_mask = response_call.result()
                else: # pragma: no cover
                    # This case should ideally not be hit if response_call is a valid Call/Future
                    return "[Response result not available or call in progress]"
            except Exception as e: # pragma: no cover
                return f"[Failed to retrieve response result: {e}]"
        
        if result_to_mask is None: # pragma: no cover
             # Should not happen if .result() behaves as expected (blocks or raises)
            return "[No response result to mask]"

        # Mask the response object if debug level logging is enabled and it's a Message.
        # If already string (e.g. from an error), it won't be re-masked by mask_message.
        # The mask_message helper should handle non-Message types gracefully.
        if self.logger.isEnabledFor(logging.DEBUG):
            # mask_message returns the same type as input if it's a proto message.
            # If result_to_mask is not a proto message, mask_message should ideally return it as-is.
            return mask_message(result_to_mask, self._SENSITIVE_INFO_MASK)
        else:
            # If not DEBUG, return string representation without sensitive fields
            # This relies on the default string conversion of protobuf messages
            # not leaking sensitive data, or using a custom non-masking serializer.
            # For simplicity, we'll stringify. If it's already a string, this is a no-op.
            return str(result_to_mask)
