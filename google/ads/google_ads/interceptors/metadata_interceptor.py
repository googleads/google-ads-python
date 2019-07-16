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
"""A gRPC Interceptor that is responsible to augmenting request metadata.

This class is initialized in the GoogleAdsClient and passed into a grpc
intercept_channel whenever a new service is initialized. It intercepts requests
and updates the metadata in order to insert the developer token and
login-customer-id values.
"""

from collections import namedtuple

from grpc import UnaryUnaryClientInterceptor, ClientCallDetails


class _ClientCallDetails(
        namedtuple(
            '_ClientCallDetails',
            ('method', 'timeout', 'metadata', 'credentials')),
        ClientCallDetails):
    """A wrapper class for initializing a new ClientCallDetails instance."""
    pass


class MetadataInterceptor(UnaryUnaryClientInterceptor):
    """An interceptor that appends custom metadata to requests."""

    def __init__(self, developer_token, login_customer_id):
        self.developer_token_meta = ('developer-token', developer_token)
        self.login_customer_id_meta = (
            ('login-customer-id', login_customer_id) if login_customer_id
            else None)

    def _update_client_call_details_metadata(self, client_call_details,
                                             metadata):
        """Updates the client call details with additional metadata.

        Args:
            client_call_details: An instance of grpc.ClientCallDetails.
            metadata: Additional metadata defined by GoogleAdsClient.

        Returns:
            An new instance of grpc.ClientCallDetails with additional metadata
            from the GoogleAdsClient.
        """
        client_call_details = _ClientCallDetails(
            client_call_details.method, client_call_details.timeout, metadata,
            client_call_details.credentials)

        return client_call_details

    def intercept_unary_unary(self, continuation, client_call_details, request):
        """Intercepts and appends custom metadata.

        Overrides abstract method defined in grpc.UnaryUnaryClientInterceptor.

        Returns:
            A grpc.Call/grpc.Future instance representing a service response.
        """
        if client_call_details.metadata is None:
            metadata = []
        else:
            metadata = list(client_call_details.metadata)

        metadata.append(self.developer_token_meta)

        if self.login_customer_id_meta:
            metadata.append(self.login_customer_id_meta)

        client_call_details = self._update_client_call_details_metadata(
            client_call_details,
            metadata)

        return continuation(client_call_details, request)