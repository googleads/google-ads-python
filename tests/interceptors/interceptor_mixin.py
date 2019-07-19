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
"""Tests for the gRPC Interceptor Mixin class."""


from unittest import TestCase

from google.ads.google_ads.interceptors.interceptor_mixin import \
    InterceptorMixin

class InterceptorMixinTest(TestCase):
    def test_get_request_id_from_metadata(self):
        """Ensures request-id is retrieved from metadata tuple."""
        mock_metadata = (('request-id', '123456'),)
        result = InterceptorMixin.get_request_id_from_metadata(mock_metadata)
        self.assertEqual(result, '123456')

    def test_get_request_id_no_id(self):
        """Ensures None is returned if metadata does't contain a request ID."""
        mock_metadata = (('another-key', 'another-val'),)
        result = (InterceptorMixin.get_request_id_from_metadata(mock_metadata))
        self.assertEqual(result, None)

    def test_parse_metadata_to_json(self):
        mock_metadata = [
            ('x-goog-api-client',
             'gl-python/123 grpc/123 gax/123'),
            ('developer-token', '0000000000'),
            ('login-customer-id', '9999999999')]

        result = InterceptorMixin.parse_metadata_to_json(mock_metadata)

        self.assertEqual(result, '{\n'
                                 '  "developer-token": "REDACTED",\n'
                                 '  "login-customer-id": "9999999999",\n'
                                 '  "x-goog-api-client": "gl-python/123 '
                                 'grpc/123 gax/123"\n'
                                 '}')

    def test_parse_metadata_to_json_with_none(self):
        mock_metadata = None
        result = InterceptorMixin.parse_metadata_to_json(mock_metadata)
        self.assertEqual(result, '{}')