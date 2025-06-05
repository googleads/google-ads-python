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
"""Tests for add_performance_max_campaign."""

import argparse
import unittest
from unittest import mock
import runpy
import warnings

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

# Predefined temporary IDs from the script
_BUDGET_TEMPORARY_ID = "-1"
_PERFORMANCE_MAX_CAMPAIGN_TEMPORARY_ID = "-2"
_ASSET_GROUP_TEMPORARY_ID = "-3"

# Mock resource names for assets created by create_multiple_text_assets
_MOCK_HEADLINE_ASSET_RN_1 = "customers/123/assets/headline1"
_MOCK_HEADLINE_ASSET_RN_2 = "customers/123/assets/headline2"
_MOCK_HEADLINE_ASSET_RN_3 = "customers/123/assets/headline3"
_MOCK_DESCRIPTION_ASSET_RN_1 = "customers/123/assets/desc1"
_MOCK_DESCRIPTION_ASSET_RN_2 = "customers/123/assets/desc2"


class AddPerformanceMaxCampaignTest(unittest.TestCase):
    """Tests for the add_performance_max_campaign example."""

    def _setup_common_mocks(self, mock_load_from_storage, mock_get_image_bytes):
        mock_client = mock.Mock(spec=GoogleAdsClient)
        mock_load_from_storage.return_value = mock_client
        mock_client.enums = mock.Mock()  # For various Enums

        # Mock image fetching
        mock_get_image_bytes.return_value = b"dummy_image_bytes"

        # Mock services
        mock_googleads_service = mock.Mock()
        mock_campaign_budget_service = mock.Mock()
        mock_campaign_service = mock.Mock()
        mock_asset_group_service = mock.Mock()
        mock_asset_service = mock.Mock()
        mock_geo_target_constant_service = mock.Mock()
        # Add other services if needed by path methods

        def get_service_side_effect(service_name, version=None):
            service_map = {
                "GoogleAdsService": mock_googleads_service,
                "CampaignBudgetService": mock_campaign_budget_service,
                "CampaignService": mock_campaign_service,
                "AssetGroupService": mock_asset_group_service,
                "AssetService": mock_asset_service,
                "GeoTargetConstantService": mock_geo_target_constant_service,
            }
            if service_name in service_map:
                return service_map[service_name]
            # Fallback for other services that might just be used for path
            return mock.Mock()
        mock_client.get_service.side_effect = get_service_side_effect

        # Mock path methods - these are essential
        mock_campaign_budget_service.campaign_budget_path.side_effect = lambda cust_id, budget_id: f"customers/{cust_id}/campaignBudgets/{budget_id}"
        mock_campaign_service.campaign_path.side_effect = lambda cust_id, camp_id: f"customers/{cust_id}/campaigns/{camp_id}"
        mock_asset_group_service.asset_group_path.side_effect = lambda cust_id, ag_id: f"customers/{cust_id}/assetGroups/{ag_id}"
        mock_asset_service.asset_path.side_effect = lambda cust_id, asset_id: f"customers/{cust_id}/assets/{asset_id}"
        mock_geo_target_constant_service.geo_target_constant_path.side_effect = lambda geo_id: f"geoTargetConstants/{geo_id}"
        mock_googleads_service.language_constant_path.side_effect = lambda lang_id: f"languageConstants/{lang_id}"
        mock_googleads_service.audience_path.side_effect = lambda cust_id, aud_id: f"customers/{cust_id}/audiences/{aud_id}"
        mock_googleads_service.asset_group_path.side_effect = lambda cust_id, ag_id: f"customers/{cust_id}/assetGroups/{ag_id}" # For asset group signals


        # Mock get_type for various operations and entities
        # Using MagicMock will auto-create attributes as mocks upon access
        mock_client.get_type.side_effect = lambda type_name: mock.MagicMock(name=type_name)

        return mock_client, mock_googleads_service

    def _create_mock_mutate_response(self, results_tuples):
        response = mock.Mock()
        op_responses = []
        for field_name, resource_name_val in results_tuples:
            op_resp = mock.Mock()
            # Mock the _pb.ListFields() behavior
            mock_pb = mock.Mock()
            # Each field_descriptor should have a 'name'
            field_descriptor_mock = mock.Mock()
            field_descriptor_mock.name = field_name
            # The value should have a 'resource_name' if it's an asset_result etc.
            value_mock = mock.Mock()
            if resource_name_val:  # Only set resource_name if provided
                setattr(value_mock, "resource_name", resource_name_val)

            # Make ListFields return a list with one item for simplicity
            mock_pb.ListFields.return_value = [(field_descriptor_mock, value_mock)]
            setattr(op_resp, "_pb", mock_pb)
            # Also set the direct attribute e.g. op_resp.asset_result.resource_name
            result_attr = mock.Mock()
            if resource_name_val:
                result_attr.resource_name = resource_name_val
            setattr(op_resp, field_name, result_attr)
            op_responses.append(op_resp)
        response.mutate_operation_responses = op_responses
        return response

    @mock.patch("examples.advanced_operations.add_performance_max_campaign.get_image_bytes_from_url")
    @mock.patch("examples.advanced_operations.add_performance_max_campaign.GoogleAdsClient.load_from_storage")
    def test_main_success_no_audience_no_brand_guidelines(self, mock_load_from_storage, mock_get_image_bytes):
        mock_client, mock_googleads_service = self._setup_common_mocks(mock_load_from_storage, mock_get_image_bytes)

        # --- Mock responses for create_multiple_text_assets ---
        # First call for headlines
        mock_headline_response = self._create_mock_mutate_response([
            ("asset_result", _MOCK_HEADLINE_ASSET_RN_1),
            ("asset_result", _MOCK_HEADLINE_ASSET_RN_2),
            ("asset_result", _MOCK_HEADLINE_ASSET_RN_3),
        ])
        mock_description_response = self._create_mock_mutate_response([
            ("asset_result", _MOCK_DESCRIPTION_ASSET_RN_1),
            ("asset_result", _MOCK_DESCRIPTION_ASSET_RN_2),
        ])

        # For the main mutate call, we need various result types
        # For simplicity now, make them generic or asset_result like.
        # The actual printed output isn't asserted, just that it doesn't crash.
        main_mutate_op_response_tuples = [("campaign_budget_result", "budget_rn")] + \
                                         [("campaign_result", "camp_rn")] + \
                                         [("campaign_criterion_result", "crit_rn")] * 3 + \
                                         [("asset_group_result", "ag_rn")] + \
                                         [("asset_group_asset_result", "aga_rn")] * 10 + \
                                         [("asset_group_signal_result", "ags_rn")] *1 # Min 1 search theme
        mock_main_mutate_response = self._create_mock_mutate_response(main_mutate_op_response_tuples)


        mock_googleads_service.mutate.side_effect = [
            mock_headline_response,
            mock_description_response,
            mock_main_mutate_response
        ]

        mock_args = argparse.Namespace(
            customer_id="12345",
            audience_id=None,
            brand_guidelines_enabled=False
        )

        with mock.patch("sys.argv", [
            "add_performance_max_campaign.py",
            "-c", mock_args.customer_id,
            # -b is False by default, -a is None by default
        ]), mock.patch(
            "examples.advanced_operations.add_performance_max_campaign.argparse.ArgumentParser"
        ) as mock_argparse:
            mock_argparse.return_value.parse_args.return_value = mock_args
            with warnings.catch_warnings():
                warnings.filterwarnings(
                    "ignore",
                    message="'.*add_performance_max_campaign' found in sys.modules after import of package 'examples.advanced_operations', but prior to execution of 'examples.advanced_operations.add_performance_max_campaign'",
                    category=RuntimeWarning,
                )
                runpy.run_module("examples.advanced_operations.add_performance_max_campaign", run_name="__main__")

        self.assertEqual(mock_googleads_service.mutate.call_count, 3)
        mock_load_from_storage.assert_called_once_with(version="v20")

        # Verify operations passed to the main mutate call
        main_mutate_call_args = mock_googleads_service.mutate.call_args_list[2]
        operations = main_mutate_call_args[1]['mutate_operations'] # operations is a kwarg

        self.assertTrue(any(op.campaign_budget_operation.create.name for op in operations)) # Check if name exists
        self.assertTrue(any(op.campaign_operation.create.name for op in operations))
        self.assertTrue(any(op.asset_group_operation.create.name for op in operations))
        # Check for some AssetGroupAsset operations (linking headlines, descriptions)
        self.assertTrue(sum(1 for op in operations if op.asset_group_asset_operation.create.asset == _MOCK_HEADLINE_ASSET_RN_1) == 1)
        self.assertTrue(sum(1 for op in operations if op.asset_group_asset_operation.create.asset == _MOCK_DESCRIPTION_ASSET_RN_1) == 1)
        # Check for search theme signal (always present)
        self.assertTrue(any(op.asset_group_signal_operation.create.search_theme.text == "travel" for op in operations))
        # No audience signal - check that audience.audience was not set to a string
        self.assertFalse(any(isinstance(op.asset_group_signal_operation.create.audience.audience, str) for op in operations))
        # No CampaignAsset operations for brand guidelines - check that .asset was not set to a string
        self.assertFalse(any(isinstance(op.campaign_asset_operation.create.asset, str) for op in operations))


    @mock.patch("examples.advanced_operations.add_performance_max_campaign.get_image_bytes_from_url")
    @mock.patch("examples.advanced_operations.add_performance_max_campaign.GoogleAdsClient.load_from_storage")
    def test_main_with_audience_and_brand_guidelines(self, mock_load_from_storage, mock_get_image_bytes):
        mock_client, mock_googleads_service = self._setup_common_mocks(mock_load_from_storage, mock_get_image_bytes)

        # Use the same helper to create detailed mock responses
        mock_headline_response = self._create_mock_mutate_response([("asset_result", "...")]*3)
        mock_description_response = self._create_mock_mutate_response([("asset_result", "...")]*2)

        main_mutate_op_response_tuples_brand = [("campaign_budget_result", "budget_rn")] + \
                                               [("campaign_result", "camp_rn")] + \
                                               [("campaign_criterion_result", "crit_rn")] * 3 + \
                                               [("asset_group_result", "ag_rn")] + \
                                               [("asset_group_asset_result", "aga_rn")] * 8 + \
                                               [("campaign_asset_result", "ca_rn")] * 2 + \
                                               [("asset_group_signal_result", "ags_rn")]*2 # Audience + Search Theme
        mock_main_mutate_response = self._create_mock_mutate_response(main_mutate_op_response_tuples_brand)


        mock_googleads_service.mutate.side_effect = [
            mock_headline_response,
            mock_description_response,
            mock_main_mutate_response
        ]

        _AUDIENCE_ID = "aud789"
        mock_args = argparse.Namespace(
            customer_id="12345",
            audience_id=_AUDIENCE_ID,
            brand_guidelines_enabled=True
        )

        with mock.patch("sys.argv", [
            "add_performance_max_campaign.py",
            "-c", mock_args.customer_id,
            "-a", mock_args.audience_id,
            "-b", "True", # Explicitly pass True
        ]), mock.patch(
            "examples.advanced_operations.add_performance_max_campaign.argparse.ArgumentParser"
        ) as mock_argparse:
            mock_argparse.return_value.parse_args.return_value = mock_args
            with warnings.catch_warnings():
                warnings.filterwarnings(
                    "ignore",
                    message="'.*add_performance_max_campaign' found in sys.modules after import of package 'examples.advanced_operations', but prior to execution of 'examples.advanced_operations.add_performance_max_campaign'",
                    category=RuntimeWarning,
                )
                runpy.run_module("examples.advanced_operations.add_performance_max_campaign", run_name="__main__")

        self.assertEqual(mock_googleads_service.mutate.call_count, 3)
        main_mutate_call_args = mock_googleads_service.mutate.call_args_list[2]
        operations = main_mutate_call_args[1]['mutate_operations']

        # Check for audience signal
        self.assertTrue(any(
            op.asset_group_signal_operation.create.audience.audience == f"customers/12345/audiences/{_AUDIENCE_ID}"
            for op in operations
        ))
        # Check for CampaignAsset operations for brand guidelines (business name and logo)
        self.assertTrue(sum(
            1 for op in operations
            if op.campaign_asset_operation.create.field_type == mock_client.enums.AssetFieldTypeEnum.BUSINESS_NAME
        ) == 1)
        self.assertTrue(sum(
            1 for op in operations
            if op.campaign_asset_operation.create.field_type == mock_client.enums.AssetFieldTypeEnum.LOGO
        ) == 1)
        # No AssetGroupAsset for business name/logo when brand guidelines enabled
        self.assertFalse(sum(
            1 for op in operations
            if op.asset_group_asset_operation.create.field_type == mock_client.enums.AssetFieldTypeEnum.BUSINESS_NAME
        ) > 0)


    @mock.patch("examples.advanced_operations.add_performance_max_campaign.get_image_bytes_from_url")
    @mock.patch("examples.advanced_operations.add_performance_max_campaign.GoogleAdsClient.load_from_storage")
    def test_main_google_ads_exception_on_text_assets(self, mock_load_from_storage, mock_get_image_bytes):
        mock_client, mock_googleads_service = self._setup_common_mocks(mock_load_from_storage, mock_get_image_bytes)

        # Configure the mock to raise GoogleAdsException on the first mutate call (headlines)
        mock_error = mock.Mock()
        mock_error.code.return_value.name = "TestAssetError"
        mock_failure = mock.Mock()
        mock_error_detail = mock.Mock()
        mock_error_detail.message = "Test asset error message."
        mock_error_detail.location.field_path_elements = []
        mock_failure.errors = [mock_error_detail]

        exception_to_raise = GoogleAdsException(
            mock_error, mock_failure, "Google Ads API request failed (assets).", request_id="test_text_asset_req_id"
        )
        exception_to_raise.failure = mock_failure
        mock_googleads_service.mutate.side_effect = exception_to_raise

        mock_args = argparse.Namespace(customer_id="12345", audience_id=None, brand_guidelines_enabled=False)

        with mock.patch("sys.argv", ["add_performance_max_campaign.py", "-c", mock_args.customer_id]), \
             mock.patch("examples.advanced_operations.add_performance_max_campaign.argparse.ArgumentParser") as mock_argparse:
            mock_argparse.return_value.parse_args.return_value = mock_args
            with warnings.catch_warnings():
                warnings.filterwarnings(
                    "ignore",
                    message="'.*add_performance_max_campaign' found in sys.modules after import of package 'examples.advanced_operations', but prior to execution of 'examples.advanced_operations.add_performance_max_campaign'",
                    category=RuntimeWarning,
                )
                with self.assertRaises(SystemExit) as cm:
                    runpy.run_module("examples.advanced_operations.add_performance_max_campaign", run_name="__main__")
                self.assertEqual(cm.exception.code, 1)

        mock_googleads_service.mutate.assert_called_once() # Should fail on the first call

if __name__ == "__main__":
    unittest.main()
