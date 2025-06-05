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
"""Tests for add_dynamic_search_ads."""

import argparse
import unittest
from unittest import mock
import runpy

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

# Define mock constants for resource names
_MOCK_BUDGET_RESOURCE_NAME = "customers/123/campaignBudgets/456"
_MOCK_CAMPAIGN_RESOURCE_NAME = "customers/123/campaigns/789"
_MOCK_AD_GROUP_RESOURCE_NAME = "customers/123/adGroups/101"
_MOCK_AD_GROUP_AD_RESOURCE_NAME = "customers/123/adGroupAds/112"
_MOCK_AD_GROUP_CRITERION_RESOURCE_NAME = "customers/123/adGroupCriteria/131"


class AddDynamicSearchAdsTest(unittest.TestCase):
    """Tests for the add_dynamic_search_ads example."""

    @mock.patch("examples.advanced_operations.add_dynamic_search_ads.GoogleAdsClient.load_from_storage")
    def test_main_success(self, mock_load_from_storage):
        """Tests the main function runs successfully with mock arguments."""
        mock_client = mock.Mock(spec=GoogleAdsClient)
        mock_load_from_storage.return_value = mock_client
        mock_client.enums = mock.Mock() # For various Enums

        # Mock services
        mock_campaign_budget_service = mock.Mock()
        mock_campaign_service = mock.Mock()
        mock_ad_group_service = mock.Mock()
        mock_ad_group_ad_service = mock.Mock()
        mock_ad_group_criterion_service = mock.Mock()

        def get_service_side_effect(service_name, version=None):
            if service_name == "CampaignBudgetService":
                return mock_campaign_budget_service
            elif service_name == "CampaignService":
                return mock_campaign_service
            elif service_name == "AdGroupService":
                return mock_ad_group_service
            elif service_name == "AdGroupAdService":
                return mock_ad_group_ad_service
            elif service_name == "AdGroupCriterionService":
                return mock_ad_group_criterion_service
            raise ValueError(f"Unexpected service: {service_name}")
        mock_client.get_service.side_effect = get_service_side_effect

        # Mock get_type for operations
        mock_campaign_budget_operation = mock.Mock()
        mock_campaign_operation = mock.Mock()
        mock_ad_group_operation = mock.Mock()
        mock_ad_group_ad_operation = mock.Mock()
        mock_ad_group_criterion_operation = mock.Mock()
        # Mock WebpageConditionInfo separately as it's called multiple times
        mock_webpage_condition_info = mock.Mock()


        type_side_effect_map = {
            "CampaignBudgetOperation": mock_campaign_budget_operation,
            "CampaignOperation": mock_campaign_operation,
            "AdGroupOperation": mock_ad_group_operation,
            "AdGroupAdOperation": mock_ad_group_ad_operation,
            "AdGroupCriterionOperation": mock_ad_group_criterion_operation,
            "WebpageConditionInfo": mock_webpage_condition_info,
        }
        mock_client.get_type.side_effect = lambda type_name: type_side_effect_map[type_name]


        # Mock responses for mutate calls
        mock_budget_response = mock.Mock()
        mock_budget_result = mock.Mock()
        mock_budget_result.resource_name = _MOCK_BUDGET_RESOURCE_NAME
        mock_budget_response.results = [mock_budget_result]
        mock_campaign_budget_service.mutate_campaign_budgets.return_value = mock_budget_response

        mock_campaign_response = mock.Mock()
        mock_campaign_result = mock.Mock()
        mock_campaign_result.resource_name = _MOCK_CAMPAIGN_RESOURCE_NAME
        mock_campaign_response.results = [mock_campaign_result]
        mock_campaign_service.mutate_campaigns.return_value = mock_campaign_response

        mock_ad_group_response = mock.Mock()
        mock_ad_group_result = mock.Mock()
        mock_ad_group_result.resource_name = _MOCK_AD_GROUP_RESOURCE_NAME
        mock_ad_group_response.results = [mock_ad_group_result]
        mock_ad_group_service.mutate_ad_groups.return_value = mock_ad_group_response

        mock_ad_group_ad_response = mock.Mock()
        mock_ad_group_ad_result = mock.Mock()
        mock_ad_group_ad_result.resource_name = _MOCK_AD_GROUP_AD_RESOURCE_NAME
        mock_ad_group_ad_response.results = [mock_ad_group_ad_result]
        mock_ad_group_ad_service.mutate_ad_group_ads.return_value = mock_ad_group_ad_response

        mock_ad_group_criterion_response = mock.Mock()
        mock_ad_group_criterion_result = mock.Mock()
        mock_ad_group_criterion_result.resource_name = _MOCK_AD_GROUP_CRITERION_RESOURCE_NAME
        mock_ad_group_criterion_response.results = [mock_ad_group_criterion_result]
        mock_ad_group_criterion_service.mutate_ad_group_criteria.return_value = mock_ad_group_criterion_response

        # Mock command-line arguments
        mock_args = argparse.Namespace(customer_id="1234567890")

        with mock.patch("sys.argv", [
            "add_dynamic_search_ads.py",
            "-c", mock_args.customer_id,
        ]), mock.patch(
            "examples.advanced_operations.add_dynamic_search_ads.argparse.ArgumentParser"
        ) as mock_argparse:
            mock_argparse.return_value.parse_args.return_value = mock_args
            runpy.run_module("examples.advanced_operations.add_dynamic_search_ads", run_name="__main__")

        mock_load_from_storage.assert_called_once_with(version="v20")
        mock_campaign_budget_service.mutate_campaign_budgets.assert_called_once()
        mock_campaign_service.mutate_campaigns.assert_called_once()
        mock_ad_group_service.mutate_ad_groups.assert_called_once()
        mock_ad_group_ad_service.mutate_ad_group_ads.assert_called_once()
        mock_ad_group_criterion_service.mutate_ad_group_criteria.assert_called_once()

        # Check campaign created with correct budget
        self.assertEqual(mock_campaign_operation.create.campaign_budget, _MOCK_BUDGET_RESOURCE_NAME)
        # Check ad group created with correct campaign
        self.assertEqual(mock_ad_group_operation.create.campaign, _MOCK_CAMPAIGN_RESOURCE_NAME)
        # Check ad group ad created with correct ad group
        self.assertEqual(mock_ad_group_ad_operation.create.ad_group, _MOCK_AD_GROUP_RESOURCE_NAME)
        # Check ad group criterion created with correct ad group
        self.assertEqual(mock_ad_group_criterion_operation.create.ad_group, _MOCK_AD_GROUP_RESOURCE_NAME)


    @mock.patch("examples.advanced_operations.add_dynamic_search_ads.GoogleAdsClient.load_from_storage")
    def test_main_google_ads_exception(self, mock_load_from_storage):
        """Tests the main function when a GoogleAdsException is raised during budget creation."""
        mock_client = mock.Mock(spec=GoogleAdsClient)
        mock_load_from_storage.return_value = mock_client
        mock_client.enums = mock.Mock()

        mock_campaign_budget_service = mock.Mock()
        mock_client.get_service.return_value = mock_campaign_budget_service
        mock_client.get_type.return_value = mock.Mock() # For CampaignBudgetOperation

        # Configure the mock to raise GoogleAdsException
        mock_error = mock.Mock()
        mock_error.code.return_value.name = "TestBudgetError"
        mock_failure = mock.Mock()
        mock_error_detail = mock.Mock()
        mock_error_detail.message = "Test budget error message."
        mock_error_detail.location.field_path_elements = []
        mock_failure.errors = [mock_error_detail]

        exception_to_raise = GoogleAdsException(
            mock_error,
            mock_failure,
            "Google Ads API request failed (budget).",
            request_id="test_budget_request_id"
        )
        exception_to_raise.failure = mock_failure # Ensure failure attribute is set correctly
        mock_campaign_budget_service.mutate_campaign_budgets.side_effect = exception_to_raise

        mock_args = argparse.Namespace(customer_id="1234567890")

        with mock.patch("sys.argv", [
            "add_dynamic_search_ads.py",
            "-c", mock_args.customer_id,
        ]), mock.patch(
            "examples.advanced_operations.add_dynamic_search_ads.argparse.ArgumentParser"
        ) as mock_argparse:
            mock_argparse.return_value.parse_args.return_value = mock_args
            with self.assertRaises(SystemExit) as cm:
                runpy.run_module("examples.advanced_operations.add_dynamic_search_ads", run_name="__main__")

            self.assertEqual(cm.exception.code, 1)

        mock_load_from_storage.assert_called_once_with(version="v20")
        mock_campaign_budget_service.mutate_campaign_budgets.assert_called_once()


if __name__ == "__main__":
    unittest.main()
