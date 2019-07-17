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

import json


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

    @classmethod
    def parse_metadata_to_json(self, metadata):
        """Parses metadata from gRPC request and response messages to a JSON str.

        Obscures the value for "developer-token".

        Args:
            metadata: a tuple of metadatum.
        """
        SENSITIVE_INFO_MASK = 'REDACTED'
        metadata_dict = {}

        if metadata is None:
            return '{}'

        for datum in metadata:
            key = datum[0]
            if key == 'developer-token':
                metadata_dict[key] = SENSITIVE_INFO_MASK
            else:
                value = datum[1]
                metadata_dict[key] = value

        return self.format_json_object(metadata_dict)

    @classmethod
    def format_json_object(self, obj):
        """Parses a serializable object into a consistently formatted JSON string.

        Returns:
            A str of formatted JSON serialized from the given object.

        Args:
            obj: an object or dict.
        """

        def default_serializer(value):
            if isinstance(value, bytes):
                return value.decode(errors='ignore')
            else:
                return None

        return str(json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False,
                              default=default_serializer,
                              separators=(',', ': ')))