#!/usr/bin/env python
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
"""Tests for add_display_upload_ad."""

import argparse
import unittest
from unittest import mock
import runpy
import warnings

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


# Define mock constants for resource names
_MOCK_ASSET_RESOURCE_NAME = "customers/12345/assets/67890"
_MOCK_AD_GROUP_AD_RESOURCE_NAME = "customers/12345/adGroupAds/24680"


class AddDisplayUploadAdTest(unittest.TestCase):
    """Tests for the add_display_upload_ad example."""

    @mock.patch("examples.advanced_operations.add_display_upload_ad.requests.get")
    @mock.patch("examples.advanced_operations.add_display_upload_ad.GoogleAdsClient.load_from_storage")
    def test_main_success(self, mock_load_from_storage, mock_requests_get):
        """Tests the main function runs successfully with mock arguments."""
        mock_client = mock.Mock(spec=GoogleAdsClient)
        mock_load_from_storage.return_value = mock_client
        mock_client.enums = mock.Mock() # For AdGroupAdStatusEnum, AssetTypeEnum, etc.

        # Mock requests.get() to return a mock response with content
        mock_response = mock.Mock()
        mock_response.content = b"dummy_zip_content"
        mock_requests_get.return_value = mock_response

        # Mock AssetService
        mock_asset_service = mock.Mock()
        mock_client.get_service.return_value = mock_asset_service
        mock_asset_operation = mock.Mock()
        mock_client.get_type.return_value = mock_asset_operation
        mock_mutate_assets_response = mock.Mock()
        # Ensure results is a list containing a mock object
        mock_asset_result = mock.Mock()
        mock_asset_result.resource_name = _MOCK_ASSET_RESOURCE_NAME
        mock_mutate_assets_response.results = [mock_asset_result]
        mock_asset_service.mutate_assets.return_value = mock_mutate_assets_response

        # Mock AdGroupAdService & AdGroupService (for ad_group_path)
        mock_ad_group_ad_service = mock.Mock()
        mock_ad_group_service = mock.Mock()

        def get_service_side_effect(service_name, version=None):
            if service_name == "AssetService":
                return mock_asset_service
            elif service_name == "AdGroupAdService":
                return mock_ad_group_ad_service
            elif service_name == "AdGroupService": # For ad_group_path
                return mock_ad_group_service
            raise ValueError(f"Unexpected service: {service_name}")
        mock_client.get_service.side_effect = get_service_side_effect

        mock_ad_group_path = "customers/12345/adGroups/09876"
        mock_ad_group_service.ad_group_path.return_value = mock_ad_group_path

        mock_ad_group_ad_operation = mock.Mock()
        # Need to make get_type return a new mock for the second call
        # The first call to get_type is for AssetOperation
        # The second call to get_type is for AdGroupAdOperation
        # Use mock_client to get the type, not the undefined 'client'
        mock_client.get_type.side_effect = [mock_client.get_type("AssetOperation"), mock_ad_group_ad_operation]


        mock_mutate_ad_group_ads_response = mock.Mock()
        # Ensure results is a list containing a mock object
        mock_ad_group_ad_result = mock.Mock()
        mock_ad_group_ad_result.resource_name = _MOCK_AD_GROUP_AD_RESOURCE_NAME
        mock_mutate_ad_group_ads_response.results = [mock_ad_group_ad_result]
        mock_ad_group_ad_service.mutate_ad_group_ads.return_value = mock_mutate_ad_group_ads_response

        # Mock command-line arguments
        mock_args = argparse.Namespace(
            customer_id="1234567890",
            ad_group_id="0987654321",
        )

        with mock.patch("sys.argv", [
            "add_display_upload_ad.py",
            "-c", mock_args.customer_id,
            "-a", str(mock_args.ad_group_id), # ad_group_id is int in script
        ]), mock.patch(
            "examples.advanced_operations.add_display_upload_ad.argparse.ArgumentParser"
        ) as mock_argparse:
            mock_argparse.return_value.parse_args.return_value = mock_args
            with warnings.catch_warnings():
                warnings.filterwarnings(
                    "ignore",
                    message="'.*add_display_upload_ad' found in sys.modules after import of package 'examples.advanced_operations', but prior to execution of 'examples.advanced_operations.add_display_upload_ad'",
                    category=RuntimeWarning,
                )
                runpy.run_module("examples.advanced_operations.add_display_upload_ad", run_name="__main__")

        mock_load_from_storage.assert_called_once_with(version="v20")
        mock_requests_get.assert_called_once_with("https://gaagl.page.link/ib87")
        mock_asset_service.mutate_assets.assert_called_once()
        mock_ad_group_ad_service.mutate_ad_group_ads.assert_called_once()
        # Check that the correct ad_group_path was used
        self.assertEqual(
            mock_ad_group_ad_operation.create.ad_group, mock_ad_group_path
        )
        # Check that the asset from the first call was used in the second
        self.assertEqual(
            mock_ad_group_ad_operation.create.ad.display_upload_ad.media_bundle.asset,
            _MOCK_ASSET_RESOURCE_NAME
        )

    @mock.patch("examples.advanced_operations.add_display_upload_ad.requests.get")
    @mock.patch("examples.advanced_operations.add_display_upload_ad.GoogleAdsClient.load_from_storage")
    def test_main_google_ads_exception(self, mock_load_from_storage, mock_requests_get):
        """Tests the main function when a GoogleAdsException is raised."""
        mock_client = mock.Mock(spec=GoogleAdsClient)
        mock_load_from_storage.return_value = mock_client
        mock_client.enums = mock.Mock()

        mock_response = mock.Mock()
        mock_response.content = b"dummy_zip_content"
        mock_requests_get.return_value = mock_response

        mock_asset_service = mock.Mock()
        mock_client.get_service.return_value = mock_asset_service

        # Configure the mock to raise GoogleAdsException
        mock_error = mock.Mock()
        mock_error.code.return_value.name = "TestAssetError"
        mock_failure = mock.Mock()
        mock_error_detail = mock.Mock()
        mock_error_detail.message = "Test asset error message."
        mock_error_detail.location.field_path_elements = []
        mock_failure.errors = [mock_error_detail]

        # Create the exception instance
        exception_to_raise = GoogleAdsException(
            mock_error,
            mock_failure, # This should be the failure object
            "Google Ads API request failed (assets).", # This is the message string
            request_id="test_asset_request_id"
        )
        # Ensure ex.failure is the mock_failure object, not the message string.
        # The GoogleAdsException constructor might assign the message to ex.failure
        # if the failure object itself is not correctly structured or if the message
        # parameter takes precedence in some cases.
        # To be safe, let's explicitly set it, similar to test_add_call_ad.
        exception_to_raise.failure = mock_failure
        mock_asset_service.mutate_assets.side_effect = exception_to_raise

        mock_args = argparse.Namespace(
            customer_id="1234567890",
            ad_group_id="0987654321",
        )

        with mock.patch("sys.argv", [
            "add_display_upload_ad.py",
            "-c", mock_args.customer_id,
            "-a", str(mock_args.ad_group_id),
        ]), mock.patch(
            "examples.advanced_operations.add_display_upload_ad.argparse.ArgumentParser"
        ) as mock_argparse:
            mock_argparse.return_value.parse_args.return_value = mock_args
            with warnings.catch_warnings():
                warnings.filterwarnings(
                    "ignore",
                    message="'.*add_display_upload_ad' found in sys.modules after import of package 'examples.advanced_operations', but prior to execution of 'examples.advanced_operations.add_display_upload_ad'",
                    category=RuntimeWarning,
                )
                with self.assertRaises(SystemExit) as cm:
                    runpy.run_module("examples.advanced_operations.add_display_upload_ad", run_name="__main__")

                self.assertEqual(cm.exception.code, 1)

        mock_load_from_storage.assert_called_once_with(version="v20")
        mock_requests_get.assert_called_once_with("https://gaagl.page.link/ib87")
        mock_asset_service.mutate_assets.assert_called_once()


if __name__ == "__main__":
    unittest.main()
