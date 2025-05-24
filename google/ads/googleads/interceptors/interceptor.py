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
"""A mixin class to store shared functionality for all the gRPC Interceptors.

This mixin class centralizes sets of functionality that are common across all
Interceptors, including retrieving data from gRPC metadata and initializing
instances of grpc.ClientCallDetails.
"""

from dataclasses import dataclass, field
from importlib import import_module
from typing import (
    Any,
    AnyStr,
    Dict,
    List,
    Optional,
    Sequence,
    Tuple,
    Union,
    TYPE_CHECKING,
)
import json

from google.protobuf.message import DecodeError, Message
from grpc import (
    Call,
    CallCredentials,
    ClientCallDetails,
    RpcError,
    StatusCode,
)

from google.ads.googleads.errors import GoogleAdsException

if TYPE_CHECKING:
    # This is a forward reference for type hinting purposes only.
    # It assumes that a GoogleAdsFailure message type will be available
    # at runtime, dynamically imported based on api_version.
    # A more concrete type like 'from google.ads.googleads.v16.errors.types import GoogleAdsFailure'
    # could be used if the version is fixed or if a base type exists.
    # Using 'Any' or 'Message' is also an option if more generic typing is preferred.
    GoogleAdsFailure = Message  # Placeholder for actual GoogleAdsFailure proto type

_REQUEST_ID_KEY: str = "request-id"
# Codes that are retried upon by google.api_core.
_RETRY_STATUS_CODES: Tuple[StatusCode, StatusCode] = (
    StatusCode.INTERNAL,
    StatusCode.RESOURCE_EXHAUSTED,
)


class Interceptor:
    _SENSITIVE_INFO_MASK: str = "REDACTED"
    # Instance attributes to be defined in __init__
    _error_protos: Optional[Any]  # Module for error types
    _failure_key: str
    _api_version: str

    @dataclass
    class _ClientCallDetails(ClientCallDetails):
        """Wrapper class for initializing a new ClientCallDetails instance."""

        # Ensure fields from ClientCallDetails are correctly typed if overridden
        # or provide new ones.
        method: str
        timeout: Optional[float] = None
        metadata: Optional[Sequence[Tuple[str, AnyStr]]] = None
        credentials: Optional[CallCredentials] = None
        # Adding type hints for any other fields if they exist in parent
        # For example, if ClientCallDetails has 'type', it should be here too.
        # type: Optional[str] = None # Example if 'type' was a field

    @classmethod
    def get_request_id_from_metadata(
        cls, trailing_metadata: Sequence[Tuple[str, str]]
    ) -> Optional[str]:
        """Gets the request ID for the Google Ads API request.

        Args:
            trailing_metadata: A sequence of metadata tuples from the service
                response, where values are strings.

        Returns:
            A str request ID associated with the Google Ads API request, or None
            if it doesn't exist.
        """
        if not trailing_metadata:
            return None

        for key, value in trailing_metadata:
            if key == _REQUEST_ID_KEY:
                return value  # Return the found request ID.

        return None

    @classmethod
    def parse_metadata_to_json(
        cls, metadata: Optional[Sequence[Tuple[str, AnyStr]]]
    ) -> str:
        """Parses metadata from gRPC request and response messages to a JSON str.

        Obscures the value for "developer-token".

        Args:
            metadata: A sequence of metadata tuples. Values can be str or bytes.

        Returns:
            A str of metadata formatted as JSON key/value pairs.
        """
        metadata_dict: Dict[str, Union[str, bytes]] = {}

        if metadata is None:
            return "{}"

        for key, value in metadata:
            if key == "developer-token":
                metadata_dict[key] = cls._SENSITIVE_INFO_MASK
            else:
                metadata_dict[key] = value

        return cls.format_json_object(metadata_dict)

    @classmethod
    def format_json_object(cls, obj: Any) -> str:
        """Parses a serializable object into a consistently formatted JSON string.

        Args:
            obj: An object or dict to serialize to JSON.

        Returns:
            A str of metadata formatted as JSON key/value pairs.
        """

        def default_serializer(value: Any) -> Optional[str]:
            if isinstance(value, bytes):
                return value.decode(errors="ignore")
            # Add other custom serializers if needed, otherwise,
            # json.dumps will raise TypeError for unsupported types.
            # Returning None or raising TypeError are options.
            # For this specific use, it seems only bytes needed special handling.
            # If other non-serializable types are expected, they should be handled.
            try:
                # Check if it's serializable by trying to dump it (inefficient)
                # or by checking against known serializable types.
                # For now, assume other types are either serializable or should fail.
                json.dumps(value) # This is just a check, not for output
                return value # Let json.dumps handle it
            except TypeError:
                return str(value) # Fallback to string representation

        try:
            return str(
                json.dumps(
                    obj,
                    indent=2,
                    sort_keys=True,
                    ensure_ascii=False,
                    default=default_serializer,
                    separators=(",", ": "),
                )
            )
        except (TypeError, OverflowError) as e:
            # Fallback if json.dumps fails for reasons other than handled by default_serializer
            return f'{{"error": "Failed to serialize object to JSON: {e}"}}'

    @classmethod
    def get_trailing_metadata_from_interceptor_exception(
        cls, exception: Any
    ) -> Sequence[Tuple[str, AnyStr]]:
        """Retrieves trailing metadata from an exception object.

        Args:
            exception: An exception instance, typically grpc.Call or related.

        Returns:
            A sequence of trailing metadata key-value pairs, or an empty tuple
            if metadata cannot be retrieved.
        """
        trailing_meta: Optional[Sequence[Tuple[str, AnyStr]]] = None
        # Prioritize specific exception types if known, e.g., GoogleAdsException
        if isinstance(exception, GoogleAdsException) and hasattr(exception, "error"):
            # Assuming error object has trailing_metadata method
            ga_error_obj = getattr(exception, "error", None)
            if hasattr(ga_error_obj, "trailing_metadata"):
                trailing_meta = ga_error_obj.trailing_metadata()
        elif hasattr(exception, "trailing_metadata"):
            # For grpc.RpcError or grpc.Call
            trailing_meta = exception.trailing_metadata()
        
        return trailing_meta if trailing_meta is not None else tuple()

    @classmethod
    def get_client_call_details_instance(
        cls,
        method: str,
        timeout: Optional[float] = None,
        metadata: Optional[List[Tuple[str, AnyStr]]] = None,
        credentials: Optional[CallCredentials] = None,
    ) -> "Interceptor._ClientCallDetails":
        """Initializes an instance of the ClientCallDetails with the given data.

        Args:
            method: A str of the service method being invoked.
            timeout: An optional float of the request timeout.
            metadata: An optional list of metadata tuples.
            credentials: An optional grpc.CallCredentials instance for the RPC.

        Returns:
            An instance of _ClientCallDetails that wraps grpc.ClientCallDetails.
        """
        return cls._ClientCallDetails(
            method=method,
            timeout=timeout,
            metadata=metadata,
            credentials=credentials,
        )

    def __init__(self, api_version: str) -> None:
        self._error_protos = None  # Will be populated by _get_google_ads_failure
        self._failure_key = (
            f"google.ads.googleads.{api_version}.errors.googleadsfailure-bin"
        )
        self._api_version = api_version

    def _get_error_from_response(
        self, response: Call
    ) -> Union[GoogleAdsException, RpcError, Exception]:
        """Attempts to wrap failed responses as GoogleAdsException instances.

        Handles failed gRPC responses by attempting to convert them
        to a more readable GoogleAdsException. Certain types of exceptions are
        not converted if the object's trailing metadata does not indicate that
        it is a GoogleAdsException, or if it falls under a certain category of
        status code (INTERNAL or RESOURCE_EXHAUSTED). See documentation for
        more information about gRPC status codes:
        https://github.com/grpc/grpc/blob/master/doc/statuscodes.md

        Args:
            response: A grpc.Call/grpc.Future instance from a gRPC call.

        Returns:
            A GoogleAdsException if the failure is a Google Ads API error.
            An RpcError for other gRPC-level errors not classified as
            GoogleAdsFailures or if the status code indicates a retryable
            gRPC error.
            The original Exception if it's neither of the above.
        """
        status_code: Optional[StatusCode] = response.code()
        # Ensure response_exception is typed, it can be None if no exception occurred
        # or an RpcError if one did.
        response_exception: Optional[RpcError] = response.exception()

        if status_code not in _RETRY_STATUS_CODES:
            # Ensure trailing_metadata is correctly typed
            trailing_metadata: Optional[Sequence[Tuple[str, Union[str, bytes]]]]
            trailing_metadata = response.trailing_metadata()
            
            google_ads_failure: Optional[Message] = self._get_google_ads_failure(
                trailing_metadata
            )

            if google_ads_failure and response_exception:
                # Ensure request_id is typed
                request_id: Optional[str] = None
                if trailing_metadata:
                    # get_request_id_from_metadata expects Sequence[Tuple[str, str]]
                    # We need to ensure byte values are decoded if that's the case.
                    # For now, let's assume they are strings or handle conversion.
                    # This part might need careful handling of AnyStr.
                    # For simplicity, assuming metadata values are strings for request_id.
                    str_trailing_metadata: List[Tuple[str, str]] = []
                    for k, v in trailing_metadata:
                        if isinstance(v, bytes):
                            str_trailing_metadata.append((k, v.decode(errors="ignore")))
                        else:
                            str_trailing_metadata.append((k, v))
                    request_id = self.get_request_id_from_metadata(str_trailing_metadata)

                return GoogleAdsException(
                    response_exception,  # This is an RpcError
                    response,  # This is the Call object
                    google_ads_failure,  # This is the parsed GoogleAdsFailure proto
                    request_id,
                )
            elif response_exception:
                # Return the original gRPC RpcError
                return response_exception
            else:
                # This case should ideally not happen if status_code indicates an error.
                # If there's no exception and no GoogleAdsFailure,
                # it implies a non-OK status without a standard error payload.
                # Create a generic RpcError or raise a custom error.
                # For now, returning a generic Exception.
                return Exception(f"gRPC call failed with status {status_code} but no exception or GoogleAdsFailure.")

        elif response_exception:
            # For retryable status codes, return the original RpcError
            return response_exception
        else:
            # This case (retryable status code but no exception object) is unusual.
            # Potentially create an RpcError here.
            return Exception(f"gRPC call failed with retryable status {status_code} but no exception object.")


    def _get_google_ads_failure(
        self, trailing_metadata: Optional[Sequence[Tuple[str, Union[str, bytes]]]]
    ) -> "Optional[GoogleAdsFailure]": # Use the TYPE_CHECKING import
        """Gets the Google Ads failure details if they exist.

        Args:
            trailing_metadata: A sequence of metadata tuples from the service
                response. Values can be str or bytes.

        Returns:
            A GoogleAdsFailure message instance if found and parsed successfully,
            otherwise None.
        """
        if trailing_metadata:
            for key, value in trailing_metadata:
                if key == self._failure_key:
                    # Ensure value is bytes for deserialize
                    bin_value = value if isinstance(value, bytes) else value.encode()
                    try:
                        if not self._error_protos:
                            # Dynamically import the errors module based on API version
                            self._error_protos = import_module(
                                f"google.ads.googleads.{self._api_version}.errors.types.errors"
                            )
                        
                        # Assuming GoogleAdsFailure is available in the imported module
                        # and has a deserialize method.
                        if hasattr(self._error_protos, "GoogleAdsFailure"):
                            failure_type = getattr(self._error_protos, "GoogleAdsFailure")
                            if hasattr(failure_type, "deserialize"):
                                return failure_type.deserialize(bin_value)
                        return None # Should not happen if module structure is consistent
                    except (DecodeError, ModuleNotFoundError, AttributeError):
                        # Failed to parse or find the GoogleAdsFailure type
                        return None
        return None
