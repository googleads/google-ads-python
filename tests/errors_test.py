# Copyright 2025 Google LLC
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
"""Tests for the errors used by the Google Ads API client library."""

import unittest
from unittest import mock
import grpc
import requests

from google.ads.googleads import client as Client
from google.ads.googleads import errors

latest_version = Client._DEFAULT_VERSION


class ErrorsTest(unittest.TestCase):

    def setUp(self):
        self.response = mock.Mock(spec=requests.Response)
        self.response.text = "Error details here"
        self.response.headers = {"X-Goog-Upload-Status": "active_error"}
        self.response.ok = False

        self.version = latest_version

    def test_resumable_upload_error_adapter_properties(self):
        adapter = errors.ResumableUploadErrorAdapter(
            self.response, grpc.StatusCode.INVALID_ARGUMENT, self.version
        )

        self.assertEqual(adapter.code(), grpc.StatusCode.INVALID_ARGUMENT)
        self.assertEqual(adapter.details(), "Error details here")
        self.assertIsNone(adapter.initial_metadata())
        self.assertEqual(
            adapter.trailing_metadata(), tuple(self.response.headers.items())
        )
        self.assertFalse(adapter.is_active())
        self.assertIsNone(adapter.time_remaining())

        # Should not raise exception
        adapter.cancel()
        adapter.add_callback(lambda: None)

    def test_raise_formatted_ads_exception(self):
        with mock.patch(
            "google.api_core.exceptions.from_http_response"
        ) as mock_from_http:
            mock_core_error = mock.Mock()
            mock_core_error.grpc_status_code = grpc.StatusCode.NOT_FOUND
            mock_core_error.message = "Core exception message"
            mock_from_http.return_value = mock_core_error

            with self.assertRaises(errors.GoogleAdsException) as cm:
                errors.raise_formatted_ads_exception(self.response, self.version)

            exception = cm.exception
            self.assertEqual(exception.request_id, "active_error")
            self.assertEqual(exception.error.code(), grpc.StatusCode.NOT_FOUND)

            # Checking the dynamic failure construction
            self.assertEqual(len(exception.failure.errors), 1)
            self.assertEqual(
                exception.failure.errors[0].message, "Core exception message"
            )

            # The enum value is mapped by protobuf, but we can verify it's the right type
            e_code = exception.failure.errors[0].error_code
            self.assertIsNotNone(e_code.request_error)

    def test_raise_formatted_for_status_when_not_ok(self):
        with mock.patch(
            "google.ads.googleads.errors.raise_formatted_ads_exception"
        ) as mock_raise:
            errors.raise_formatted_for_status(self.response, self.version)
            mock_raise.assert_called_once_with(self.response, self.version)

    def test_raise_formatted_for_status_when_ok(self):
        self.response.ok = True
        with mock.patch(
            "google.ads.googleads.errors.raise_formatted_ads_exception"
        ) as mock_raise:
            errors.raise_formatted_for_status(self.response, self.version)
            mock_raise.assert_not_called()


if __name__ == "__main__":
    unittest.main()
