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
"""Tests for the gRPC Interceptor Mixin class."""


from importlib import import_module
from unittest import TestCase

from google.ads.google_ads.client import _DEFAULT_VERSION as default_version
from google.ads.google_ads.interceptors.interceptor import Interceptor

errors_path = f'google.ads.google_ads.{default_version}.proto.errors.errors_pb2'
error_protos = import_module(errors_path)

_MOCK_FAILURE_VALUE = b"\n \n\x02\x08\x10\x12\x1aInvalid customer ID '123'."


class InterceptorTest(TestCase):

    def test_get_request_id_from_metadata(self):
        """Ensures request-id is retrieved from metadata tuple."""
        mock_metadata = (('request-id', '123456'),)
        result = Interceptor.get_request_id_from_metadata(mock_metadata)
        self.assertEqual(result, '123456')

    def test_get_request_id_no_id(self):
        """Ensures None is returned if metadata does't contain a request ID."""
        mock_metadata = (('another-key', 'another-val'),)
        result = (Interceptor.get_request_id_from_metadata(mock_metadata))
        self.assertEqual(result, None)

    def test_parse_metadata_to_json(self):
        mock_metadata = [
            ('x-goog-api-client',
             'gl-python/123 grpc/123 gax/123'),
            ('developer-token', '0000000000'),
            ('login-customer-id', '9999999999')]

        result = Interceptor.parse_metadata_to_json(mock_metadata)

        self.assertEqual(result, '{\n'
                                 '  "developer-token": "REDACTED",\n'
                                 '  "login-customer-id": "9999999999",\n'
                                 '  "x-goog-api-client": "gl-python/123 '
                                 'grpc/123 gax/123"\n'
                                 '}')

    def test_parse_metadata_to_json_with_none(self):
        mock_metadata = None
        result = Interceptor.parse_metadata_to_json(mock_metadata)
        self.assertEqual(result, '{}')

    def test_get_google_ads_failure(self):
        """Obtains the content of a google ads failure from metadata."""
        interceptor = Interceptor(default_version)
        mock_metadata = ((interceptor._failure_key, _MOCK_FAILURE_VALUE),)
        result = interceptor._get_google_ads_failure(mock_metadata)
        self.assertIsInstance(result, error_protos.GoogleAdsFailure)

    def test_get_google_ads_failure_decode_error(self):
        """Returns none if the google ads failure cannot be decoded."""
        interceptor = Interceptor(default_version)
        mock_failure_value = _MOCK_FAILURE_VALUE + b'1234'
        mock_metadata = ((interceptor._failure_key, mock_failure_value),)
        result = interceptor._get_google_ads_failure(mock_metadata)
        self.assertEqual(result, None)

    def test_get_google_ads_failure_no_failure_key(self):
        """Returns None if an error cannot be found in metadata."""
        mock_metadata = (('another-key', 'another-val'),)
        interceptor = Interceptor(default_version)
        result = interceptor._get_google_ads_failure(mock_metadata)
        self.assertEqual(result, None)

    def test_get_google_ads_failure_with_None(self):
        """Returns None if None is passed."""
        interceptor = Interceptor(default_version)
        result = interceptor._get_google_ads_failure(None)
        self.assertEqual(result, None)
