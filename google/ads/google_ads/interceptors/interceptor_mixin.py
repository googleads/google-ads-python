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
"""A mixin class to store shared functionality for all the gRPC Interceptors.

This mixin class centralizes sets of functionality that are common across all
Interceptors, including retrieving data from gRPC metadata and initializing
instances of grpc.ClientCallDetails.
"""

_REQUEST_ID_KEY = 'request-id'

class InterceptorMixin:
    @classmethod
    def get_request_id_from_metadata(self, trailing_metadata):
        """Gets the request ID for the Google Ads API request.

        Args:
            trailing_metadata: a tuple of metadatum from the service response.

        Returns:
            A str request ID associated with the Google Ads API request, or None
            if it doesn't exist.
        """
        for kv in trailing_metadata:
            if kv[0] == _REQUEST_ID_KEY:
                return kv[1]  # Return the found request ID.

        return None