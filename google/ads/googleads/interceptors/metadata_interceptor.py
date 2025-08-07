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
"""A gRPC Interceptor that is responsible to augmenting request metadata.

This class is initialized in the GoogleAdsClient and passed into a grpc
intercept_channel whenever a new service is initialized. It intercepts requests
and updates the metadata in order to insert the developer token and
login-customer-id values.
"""

# TODO: Explicitly importing the protobuf package version here should be removed
# once the below issue is resolved, and the protobuf version is added to the
# request user-agent directly by the google-api-core package:
# https://github.com/googleapis/python-api-core/issues/416
from importlib import metadata
from typing import Any, Callable, List, Optional, Tuple, TypeVar, Union

from google.protobuf.internal.api_implementation import Type as ApiImplementationType
from grpc import (
    Call,
    ClientCallDetails,
    UnaryUnaryClientInterceptor,
    UnaryStreamClientInterceptor,
)

from .interceptor import Interceptor


try:
    _PROTOBUF_VERSION: Optional[str] = metadata.version("protobuf")
except metadata.PackageNotFoundError: # pragma: no cover
    _PROTOBUF_VERSION = None


# Determine which protobuf implementation is being used.
_PB_IMPL_HEADER: str
if ApiImplementationType() == "cpp":
    _PB_IMPL_HEADER = "+c"
elif ApiImplementationType() == "python":
    _PB_IMPL_HEADER = "+n"
else:  # pragma: no cover
    _PB_IMPL_HEADER = ""


# Define generic types for request and response, though not strictly necessary
# for this interceptor as it mainly deals with metadata.
RequestT = TypeVar("RequestT")
ResponseT = TypeVar("ResponseT") # Not directly used but good for consistency

# Type for the continuation callable
ContinuationCallable = Callable[[ClientCallDetails, RequestT], Call]


class MetadataInterceptor(
    Interceptor, UnaryUnaryClientInterceptor, UnaryStreamClientInterceptor
):
    """An interceptor that appends custom metadata to requests."""

    developer_token_meta: Tuple[str, str]
    login_customer_id_meta: Optional[Tuple[str, str]]
    linked_customer_id_meta: Optional[Tuple[str, str]]
    use_cloud_org_for_api_access: Optional[bool]

    def __init__(
        self,
        developer_token: str,
        login_customer_id: Optional[str],
        linked_customer_id: Optional[str] = None,
        use_cloud_org_for_api_access: Optional[bool] = None,
    ) -> None:
        """Initialization method for this class.

        Args:
            developer_token: A str developer token.
            login_customer_id: An optional str specifying a login customer ID.
            linked_customer_id: An optional str specifying a linked customer ID.
            use_cloud_org_for_api_access: An optional boolean specifying
                whether to use the Google Cloud Organization of your Google
                Cloud project instead of developer token to determine your
                Google Ads API access levels. Use this flag only if you are
                enrolled into a limited pilot that supports this configuration.
        """
        # Note: api_version is not used by this interceptor but is required by
        # the parent Interceptor class.
        # We can pass a default or decide if it needs to be passed in.
        # For now, assuming it's handled by a broader client config or not needed here.
        # super().__init__(api_version="v0") # Example if a dummy version is needed.
        # Based on parent Interceptor, it does not take api_version in __init__.
        # It seems the parent Interceptor's __init__ is:
        # def __init__(self, api_version):
        # So, if this class is meant to be standalone usable or tested without
        # the full client context providing api_version to parent, this might be an issue.
        # However, as part of the client, api_version would be passed to parent.
        # This interceptor itself does not use self._api_version.

        self.developer_token_meta = ("developer-token", developer_token)
        self.login_customer_id_meta = (
            ("login-customer-id", login_customer_id)
            if login_customer_id
            else None
        )
        self.linked_customer_id_meta = (
            ("linked-customer-id", linked_customer_id)
            if linked_customer_id
            else None
        )
        self.use_cloud_org_for_api_access = use_cloud_org_for_api_access

    def _update_client_call_details_metadata(
        self,
        client_call_details: ClientCallDetails,
        metadata: List[Tuple[str, str]],
    ) -> ClientCallDetails:
        """Updates the client call details with additional metadata.

        Args:
            client_call_details: An instance of grpc.ClientCallDetails.
            metadata: Additional metadata to be included in the call.

        Returns:
            A new instance of grpc.ClientCallDetails with additional metadata
            from the GoogleAdsClient.
        """
        # get_client_call_details_instance is part of the parent Interceptor class
        # Its signature is:
        # get_client_call_details_instance(cls, method, timeout, metadata, credentials=None)
        # So, we need to pass all required fields.
        updated_client_call_details = self.get_client_call_details_instance(
            method=client_call_details.method,
            timeout=client_call_details.timeout,
            metadata=metadata, # This is List[Tuple[str, str]]
            credentials=client_call_details.credentials,
        )
        # The return type of get_client_call_details_instance is Interceptor._ClientCallDetails
        # which is a subclass of ClientCallDetails.
        return updated_client_call_details


    def _intercept(
        self,
        continuation: ContinuationCallable[RequestT, ResponseT],
        client_call_details: ClientCallDetails,
        request: RequestT,
    ) -> Call:
        """Generic interceptor used for Unary-Unary and Unary-Stream requests.

        Args:
            continuation: A function to continue the request process.
            client_call_details: A grpc.ClientCallDetails instance
                containing request metadata.
            request: A request message class instance (TypeVar RequestT).

        Returns:
            A grpc.Call/grpc.Future instance representing a service response.
        """
        current_metadata: List[Tuple[str, str]]
        if client_call_details.metadata is None:
            current_metadata = []
        else:
            # ClientCallDetails.metadata is Sequence[Tuple[str, AnyStr]]
            # We need List[Tuple[str, str]] for modification and for
            # _update_client_call_details_metadata.
            # AnyStr can be bytes, so we decode if necessary.
            current_metadata = []
            for k, v_any in client_call_details.metadata:
                v_str = v_any if isinstance(v_any, str) else v_any.decode()
                current_metadata.append((k, v_str))


        # If self.use_cloud_org_for_api_access is not True, add the developer
        # token to the request's metadata
        if not self.use_cloud_org_for_api_access:
            current_metadata.append(self.developer_token_meta)

        if self.login_customer_id_meta:
            current_metadata.append(self.login_customer_id_meta)

        if self.linked_customer_id_meta:
            current_metadata.append(self.linked_customer_id_meta)

        # TODO: This logic should be updated or removed once the following is
        # fixed: https://github.com/googleapis/python-api-core/issues/416
        if _PROTOBUF_VERSION: # Only proceed if _PROTOBUF_VERSION is not None
            for i, metadatum_tuple in enumerate(current_metadata):
                key, value = metadatum_tuple
                # Check if the user agent header key is in the current metadatum
                if key == "x-goog-api-client": # Ensure exact match for key
                    # Check that "pb" isn't already included in the user agent.
                    if "pb/" not in value: # Check against "pb/" for specificity
                        # Append the protobuf version key value pair to the end of
                        # the string.
                        value += f" pb/{_PROTOBUF_VERSION}{_PB_IMPL_HEADER}"
                        # Update the metadatum in the list
                        current_metadata[i] = (key, value)
                        # Exit the loop since we already found and updated the user agent.
                        break

        updated_client_call_details = self._update_client_call_details_metadata(
            client_call_details, current_metadata
        )

        return continuation(updated_client_call_details, request)

    def intercept_unary_unary(
        self,
        continuation: ContinuationCallable[RequestT, ResponseT],
        client_call_details: ClientCallDetails,
        request: RequestT,
    ) -> Call:
        """Intercepts and appends custom metadata for Unary-Unary requests.

        Overrides abstract method defined in grpc.UnaryUnaryClientInterceptor.

        Args:
            continuation: A function to continue the request process.
            client_call_details: A grpc.ClientCallDetails instance
                containing request metadata.
            request: A request message class instance (TypeVar RequestT).

        Returns:
            A grpc.Call/grpc.Future instance representing a service response.
        """
        return self._intercept(continuation, client_call_details, request)

    def intercept_unary_stream(
        self,
        continuation: ContinuationCallable[RequestT, ResponseT],
        client_call_details: ClientCallDetails,
        request: RequestT,
    ) -> Call:
        """Intercepts and appends custom metadata to Unary-Stream requests.

        Overrides abstract method defined in grpc.UnaryStreamClientInterceptor.

        Args:
            continuation: A function to continue the request process.
            client_call_details: A grpc.ClientCallDetails instance
                containing request metadata.
            request: A request message class instance (TypeVar RequestT).

        Returns:
            A grpc.Call/grpc.Future instance representing a service response.
        """
        return self._intercept(continuation, client_call_details, request)
