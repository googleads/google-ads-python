# Copyright 2024 Google LLC
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

import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, timezone, timedelta
import re
import requests

# Assuming example_helpers.py is one level up and in the same package path
# This might need adjustment based on how tests are run.
# If running with pytest from the root, this relative import should work.
from examples.utils import example_helpers


class TestExampleHelpers(unittest.TestCase):

    def test_get_printable_datetime(self):
        dt_str = example_helpers.get_printable_datetime()
        self.assertIsInstance(dt_str, str)

        # Regex to check the ISO format with milliseconds and timezone
        # Example: 2023-03-23T15:45:25.123+04:00 or 2023-03-23T15:45:25.123Z
        iso_pattern = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}(Z|[+-]\d{2}:\d{2})$"
        self.assertIsNotNone(re.fullmatch(iso_pattern, dt_str),
                             f"Datetime string '{dt_str}' does not match ISO pattern.")

        # Check if the time is current (within a small delta, e.g., 5 seconds)
        # This part can be a bit flaky in CI, but useful locally.
        try:
            # Parse the string. Python's fromisoformat doesn't always handle all timezone offsets perfectly,
            # especially if they are not 'Z'. We might need to manually adjust or use a library
            # if this becomes an issue. For now, let's try direct parsing if possible,
            # or compare with a freshly generated one.
            parsed_dt = datetime.fromisoformat(dt_str)
            now_utc = datetime.now(timezone.utc)
            # Ensure both are offset-aware for comparison
            if parsed_dt.tzinfo is None: # Should not happen with the function's logic
                parsed_dt = parsed_dt.replace(tzinfo=timezone.utc)

            # Get current time in the same timezone as parsed_dt for accurate comparison
            now_in_parsed_dt_tz = datetime.now(parsed_dt.tzinfo)

            self.assertLess(abs(parsed_dt - now_in_parsed_dt_tz), timedelta(seconds=5),
                            "The generated datetime is not close to the current time.")
        except ValueError as e:
            self.fail(f"Could not parse the datetime string '{dt_str}': {e}")


    @patch('requests.get')
    def test_get_image_bytes_from_url_success(self, mock_requests_get):
        mock_response = MagicMock()
        expected_content = b"image_bytes_here"
        mock_response.content = expected_content
        # Make the mock response an iterable to satisfy requests.Response behavior if needed by other code
        mock_response.iter_content = MagicMock(return_value=iter([expected_content]))
        mock_response.status_code = 200 # success code
        mock_requests_get.return_value = mock_response

        test_url = "http://example.com/image.png"
        actual_content = example_helpers.get_image_bytes_from_url(test_url)

        mock_requests_get.assert_called_once_with(test_url)
        self.assertEqual(actual_content, expected_content)

    @patch('requests.get')
    def test_get_image_bytes_from_url_failure(self, mock_requests_get):
        test_url = "http://example.com/nonexistent_image.png"
        # Configure the mock to raise an exception when .content is accessed or when called
        mock_requests_get.side_effect = requests.exceptions.RequestException("Test error")

        with self.assertRaises(requests.exceptions.RequestException):
            example_helpers.get_image_bytes_from_url(test_url)

        mock_requests_get.assert_called_once_with(test_url)

if __name__ == "__main__":
    unittest.main()
