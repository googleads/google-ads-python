#!/usr/bin/env python
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
"""Tests for add_call_ad."""

import argparse
import unittest
from unittest import mock

from examples.advanced_operations.add_call_ad import main
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


class AddCallAdTest(unittest.TestCase):
    """Tests for the add_call_ad example."""

    @mock.patch("examples.advanced_operations.add_call_ad.GoogleAdsClient.load_from_storage")
    def test_main(self, mock_load_from_storage):
        """Tests the main function with mock arguments."""
        # Create a mock GoogleAdsClient instance
        mock_client = mock.Mock(spec=GoogleAdsClient)
        # Add the enums attribute to the mock_client
        mock_client.enums = mock.Mock()
        # Configure the mock_load_from_storage to return the mock_client
        mock_load_from_storage.return_value = mock_client

        # Create mock services
        mock_googleads_service = mock.Mock()
        mock_ad_group_ad_service = mock.Mock()
        mock_client.get_service.side_effect = [
            mock_googleads_service,
            mock_ad_group_ad_service,
        ]

        # Mock the AdGroupAdOperation
        mock_operation = mock.Mock()
        mock_client.get_type.return_value = mock_operation

        # Mock the mutate_ad_group_ads response
        mock_mutate_response = mock.Mock()
        mock_mutate_response.results = [mock.Mock()]
        mock_mutate_response.results[0].resource_name = "TestResourceName"
        mock_ad_group_ad_service.mutate_ad_group_ads.return_value = (
            mock_mutate_response
        )

        # Mock command-line arguments
        mock_args = argparse.Namespace(
            customer_id="1234567890",
            ad_group_id="0987654321",
            phone_number="(800) 555-0100",
            phone_country="US",
            conversion_action_id="1122334455",
        )

        # Call the main function by simulating command-line execution
        with mock.patch("sys.argv", [
            "add_call_ad.py",
            "-c", mock_args.customer_id,
            "-a", mock_args.ad_group_id,
            "-n", mock_args.phone_number,
            "-p", mock_args.phone_country,
            "-v", mock_args.conversion_action_id,
        ]), mock.patch(
            "examples.advanced_operations.add_call_ad.argparse.ArgumentParser"
        ) as mock_argparse:
            # Mock parse_args to return the predefined mock_args
            mock_argparse_instance = mock_argparse.return_value
            mock_argparse_instance.parse_args.return_value = mock_args

            # Import and run the main function from the script's __main__ block
            from examples.advanced_operations import add_call_ad

            # We need to reload the module to ensure that the main function
            # is executed in the context of the test case with the mocked objects.
            # import importlib
            # importlib.reload(add_call_ad)
            import runpy
            runpy.run_module("examples.advanced_operations.add_call_ad", run_name="__main__")

        # Assert that the necessary methods were called
        mock_load_from_storage.assert_called_once_with(version="v20")
        mock_client.get_service.assert_any_call("GoogleAdsService")
        mock_client.get_service.assert_any_call("AdGroupAdService")
        mock_client.get_type.assert_called_once_with("AdGroupAdOperation")
        mock_ad_group_ad_service.mutate_ad_group_ads.assert_called_once()

    @mock.patch("examples.advanced_operations.add_call_ad.GoogleAdsClient.load_from_storage")
    def test_main_google_ads_exception(self, mock_load_from_storage):
        """Tests the main function when a GoogleAdsException is raised."""
        # Create a mock GoogleAdsClient instance
        mock_client = mock.Mock(spec=GoogleAdsClient)
        # Add the enums attribute to the mock_client
        mock_client.enums = mock.Mock()
        # Configure the mock_load_from_storage to return the mock_client
        mock_load_from_storage.return_value = mock_client

        # Mock services to raise GoogleAdsException
        mock_googleads_service = mock.Mock()
        mock_ad_group_ad_service = mock.Mock()
        mock_client.get_service.side_effect = [
            mock_googleads_service,
            mock_ad_group_ad_service,
        ]
        # Configure the mock to raise GoogleAdsException
        mock_error = mock.Mock()
        mock_error.code.return_value.name = "TestError"
        # Create a mock failure object with an errors attribute
        mock_failure = mock.Mock()
        # Each error in ex.failure.errors should have a message attribute
        # and optionally a location attribute.
        mock_error_detail = mock.Mock()
        mock_error_detail.message = "Test error message."
        mock_error_detail.location.field_path_elements = [] # No field path elements for simplicity
        mock_failure.errors = [mock_error_detail]
        exception_to_raise = GoogleAdsException(
            mock_error,
            "Dummy failure message that will be overwritten",
            "Google Ads API request failed.",
            request_id="test_request_id"
        )
        # Explicitly set the failure attribute to be the mock_failure object
        exception_to_raise.failure = mock_failure
        mock_ad_group_ad_service.mutate_ad_group_ads.side_effect = exception_to_raise

        # Mock command-line arguments
        mock_args = argparse.Namespace(
            customer_id="1234567890",
            ad_group_id="0987654321",
            phone_number="(800) 555-0100",
            phone_country="US",
            conversion_action_id="1122334455",
        )

        # Call the main function by simulating command-line execution
        # and assert that it exits with code 1
        with mock.patch("sys.argv", [
            "add_call_ad.py",
            "-c", mock_args.customer_id,
            "-a", mock_args.ad_group_id,
            "-n", mock_args.phone_number,
            "-p", mock_args.phone_country,
            "-v", mock_args.conversion_action_id,
        ]), mock.patch(
            "examples.advanced_operations.add_call_ad.argparse.ArgumentParser"
        ) as mock_argparse:
            # Mock parse_args to return the predefined mock_args
            mock_argparse_instance = mock_argparse.return_value
            mock_argparse_instance.parse_args.return_value = mock_args

            # Import and run the main function from the script's __main__ block
            from examples.advanced_operations import add_call_ad

            import runpy
            with self.assertRaises(SystemExit) as cm:
                runpy.run_module("examples.advanced_operations.add_call_ad", run_name="__main__")

            self.assertEqual(cm.exception.code, 1)


if __name__ == "__main__":
    unittest.main()
