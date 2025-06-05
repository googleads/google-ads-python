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
"""Tests for add_responsive_search_ad_full."""

import argparse
import unittest
from unittest import mock
import runpy

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

# Mock resource names
_MOCK_CUSTOMIZER_ATTRIBUTE_RN = "customers/123/customizerAttributes/ca1"
_MOCK_CUSTOMER_CUSTOMIZER_RN = "customers/123/customerCustomizers/cc1"
_MOCK_BUDGET_RN = "customers/123/campaignBudgets/bud1"
_MOCK_CAMPAIGN_RN = "customers/123/campaigns/camp1"
_MOCK_AD_GROUP_RN = "customers/123/adGroups/ag1"
_MOCK_AD_GROUP_AD_RN = "customers/123/adGroupAds/aga1"
_MOCK_KEYWORD_RN_PREFIX = "customers/123/adGroupCriteria/kw"
_MOCK_GEO_TARGET_RN_PREFIX = "customers/123/campaignCriteria/geo"
_MOCK_GEO_CONSTANT_RN_PREFIX = "geoTargetConstants/"


class AddResponsiveSearchAdFullTest(unittest.TestCase):
    """Tests for the add_responsive_search_ad_full example."""

    def _setup_common_mocks(self, mock_load_from_storage):
        mock_client = mock.MagicMock(spec=GoogleAdsClient)
        mock_load_from_storage.return_value = mock_client

        # Explicitly set enums to a MagicMock, then set specific enum types on it.
        mock_client.enums = mock.MagicMock()
        mock_client.enums.BudgetDeliveryMethodEnum = mock.MagicMock()
        mock_client.enums.CustomizerAttributeTypeEnum = mock.MagicMock()
        mock_client.enums.AdvertisingChannelTypeEnum = mock.MagicMock()
        mock_client.enums.CampaignStatusEnum = mock.MagicMock()
        mock_client.enums.AdGroupStatusEnum = mock.MagicMock()
        mock_client.enums.AdGroupTypeEnum = mock.MagicMock()
        mock_client.enums.AdGroupAdStatusEnum = mock.MagicMock()
        mock_client.enums.ServedAssetFieldTypeEnum = mock.MagicMock()
        mock_client.enums.AdGroupCriterionStatusEnum = mock.MagicMock()
        mock_client.enums.KeywordMatchTypeEnum = mock.MagicMock()
        # Ensure specific values are also mocks if they are accessed directly
        # For example, client.enums.BudgetDeliveryMethodEnum.STANDARD
        # The MagicMock for BudgetDeliveryMethodEnum will create STANDARD as a MagicMock on access.

        # Mock services
        self.mock_services = {
            "CustomizerAttributeService": mock.MagicMock(),
            "CustomerCustomizerService": mock.MagicMock(),
            "CampaignBudgetService": mock.MagicMock(),
            "CampaignService": mock.MagicMock(),
            "AdGroupService": mock.MagicMock(),
            "AdGroupAdService": mock.MagicMock(),
            "AdGroupCriterionService": mock.MagicMock(),
            "GeoTargetConstantService": mock.MagicMock(),
            "CampaignCriterionService": mock.MagicMock(),
        }
        mock_client.get_service.side_effect = lambda service_name, version=None: self.mock_services[service_name]

        # Mock get_type to return MagicMocks that can then be configured
        mock_client.get_type.side_effect = lambda type_name: mock.MagicMock(name=type_name)

        return mock_client

    @mock.patch("examples.advanced_operations.add_responsive_search_ad_full.GoogleAdsClient.load_from_storage")
    def test_main_success_no_customizer(self, mock_load_from_storage):
        mock_client = self._setup_common_mocks(mock_load_from_storage)

        # --- Configure mock service responses ---
        # CampaignBudgetService
        self.mock_services["CampaignBudgetService"].mutate_campaign_budgets.return_value.results = [
            mock.MagicMock(resource_name=_MOCK_BUDGET_RN)
        ]
        # CampaignService
        self.mock_services["CampaignService"].mutate_campaigns.return_value.results = [
            mock.MagicMock(resource_name=_MOCK_CAMPAIGN_RN)
        ]
        # AdGroupService
        self.mock_services["AdGroupService"].mutate_ad_groups.return_value.results = [
            mock.MagicMock(resource_name=_MOCK_AD_GROUP_RN)
        ]
        # AdGroupAdService
        self.mock_services["AdGroupAdService"].mutate_ad_group_ads.return_value.results = [
            mock.MagicMock(resource_name=_MOCK_AD_GROUP_AD_RN)
        ]
        # AdGroupCriterionService (for keywords)
        self.mock_services["AdGroupCriterionService"].mutate_ad_group_criteria.return_value.results = [
            mock.MagicMock(resource_name=f"{_MOCK_KEYWORD_RN_PREFIX}{i}") for i in range(3)
        ]
        # GeoTargetConstantService
        mock_geo_suggestion1 = mock.MagicMock()
        mock_geo_suggestion1.geo_target_constant.resource_name = f"{_MOCK_GEO_CONSTANT_RN_PREFIX}1"
        mock_geo_suggestion2 = mock.MagicMock()
        mock_geo_suggestion2.geo_target_constant.resource_name = f"{_MOCK_GEO_CONSTANT_RN_PREFIX}2"
        self.mock_services["GeoTargetConstantService"].suggest_geo_target_constants.return_value.geo_target_constant_suggestions = [
            mock_geo_suggestion1, mock_geo_suggestion2
        ]
        # CampaignCriterionService (for geo targets)
        self.mock_services["CampaignCriterionService"].mutate_campaign_criteria.return_value.results = [
            mock.MagicMock(resource_name=f"{_MOCK_GEO_TARGET_RN_PREFIX}{i}") for i in range(2)
        ]

        mock_args = argparse.Namespace(customer_id="123", customizer_attribute_name=None)

        with mock.patch("sys.argv", ["add_responsive_search_ad_full.py", "-c", mock_args.customer_id]), \
             mock.patch("examples.advanced_operations.add_responsive_search_ad_full.argparse.ArgumentParser") as mock_argparse:
            mock_argparse.return_value.parse_args.return_value = mock_args
            runpy.run_module("examples.advanced_operations.add_responsive_search_ad_full", run_name="__main__")

        mock_load_from_storage.assert_called_once_with(version="v20")
        self.mock_services["CustomizerAttributeService"].mutate_customizer_attributes.assert_not_called()
        self.mock_services["CustomerCustomizerService"].mutate_customer_customizers.assert_not_called()
        self.mock_services["CampaignBudgetService"].mutate_campaign_budgets.assert_called_once()
        self.mock_services["CampaignService"].mutate_campaigns.assert_called_once()
        self.mock_services["AdGroupService"].mutate_ad_groups.assert_called_once()
        self.mock_services["AdGroupAdService"].mutate_ad_group_ads.assert_called_once()
        self.mock_services["AdGroupCriterionService"].mutate_ad_group_criteria.assert_called_once()
        self.mock_services["GeoTargetConstantService"].suggest_geo_target_constants.assert_called_once()
        self.mock_services["CampaignCriterionService"].mutate_campaign_criteria.assert_called_once()

        # Verify campaign created with correct budget
        campaign_op_create = self.mock_services["CampaignService"].mutate_campaigns.call_args[1]['operations'][0].create
        self.assertEqual(campaign_op_create.campaign_budget, _MOCK_BUDGET_RN)
        # Verify ad group created with correct campaign
        ad_group_op_create = self.mock_services["AdGroupService"].mutate_ad_groups.call_args[1]['operations'][0].create
        self.assertEqual(ad_group_op_create.campaign, _MOCK_CAMPAIGN_RN)
        # Verify ad group ad created with correct ad group
        ad_group_ad_op_create = self.mock_services["AdGroupAdService"].mutate_ad_group_ads.call_args[1]['operations'][0].create
        self.assertEqual(ad_group_ad_op_create.ad_group, _MOCK_AD_GROUP_RN)
         # Verify one of the descriptions does not contain CUSTOMIZER
        self.assertFalse(any("CUSTOMIZER" in desc.text for desc in ad_group_ad_op_create.ad.responsive_search_ad.descriptions))


    @mock.patch("examples.advanced_operations.add_responsive_search_ad_full.GoogleAdsClient.load_from_storage")
    def test_main_success_with_customizer(self, mock_load_from_storage):
        mock_client = self._setup_common_mocks(mock_load_from_storage)
        _CUSTOMIZER_NAME = "TestPrice"

        # --- Configure mock service responses (similar to above, plus customizer services) ---
        self.mock_services["CustomizerAttributeService"].mutate_customizer_attributes.return_value.results = [
            mock.MagicMock(resource_name=_MOCK_CUSTOMIZER_ATTRIBUTE_RN)
        ]
        self.mock_services["CustomerCustomizerService"].mutate_customer_customizers.return_value.results = [
            mock.MagicMock(resource_name=_MOCK_CUSTOMER_CUSTOMIZER_RN)
        ]
        # Other services as in the no_customizer test
        self.mock_services["CampaignBudgetService"].mutate_campaign_budgets.return_value.results = [mock.MagicMock(resource_name=_MOCK_BUDGET_RN)]
        self.mock_services["CampaignService"].mutate_campaigns.return_value.results = [mock.MagicMock(resource_name=_MOCK_CAMPAIGN_RN)]
        self.mock_services["AdGroupService"].mutate_ad_groups.return_value.results = [mock.MagicMock(resource_name=_MOCK_AD_GROUP_RN)]
        self.mock_services["AdGroupAdService"].mutate_ad_group_ads.return_value.results = [mock.MagicMock(resource_name=_MOCK_AD_GROUP_AD_RN)]
        self.mock_services["AdGroupCriterionService"].mutate_ad_group_criteria.return_value.results = [mock.MagicMock()]*3
        mock_geo_suggestion = mock.MagicMock()
        mock_geo_suggestion.geo_target_constant.resource_name = f"{_MOCK_GEO_CONSTANT_RN_PREFIX}1"
        self.mock_services["GeoTargetConstantService"].suggest_geo_target_constants.return_value.geo_target_constant_suggestions = [mock_geo_suggestion]
        self.mock_services["CampaignCriterionService"].mutate_campaign_criteria.return_value.results = [mock.MagicMock()]


        mock_args = argparse.Namespace(customer_id="123", customizer_attribute_name=_CUSTOMIZER_NAME)

        with mock.patch("sys.argv", ["add_responsive_search_ad_full.py", "-c", mock_args.customer_id, "-n", _CUSTOMIZER_NAME]), \
             mock.patch("examples.advanced_operations.add_responsive_search_ad_full.argparse.ArgumentParser") as mock_argparse:
            mock_argparse.return_value.parse_args.return_value = mock_args
            runpy.run_module("examples.advanced_operations.add_responsive_search_ad_full", run_name="__main__")

        self.mock_services["CustomizerAttributeService"].mutate_customizer_attributes.assert_called_once()
        customizer_attr_op_create = self.mock_services["CustomizerAttributeService"].mutate_customizer_attributes.call_args[1]['operations'][0].create
        self.assertEqual(customizer_attr_op_create.name, _CUSTOMIZER_NAME)

        self.mock_services["CustomerCustomizerService"].mutate_customer_customizers.assert_called_once()
        customer_customizer_op_create = self.mock_services["CustomerCustomizerService"].mutate_customer_customizers.call_args[1]['operations'][0].create
        self.assertEqual(customer_customizer_op_create.customizer_attribute, _MOCK_CUSTOMIZER_ATTRIBUTE_RN)

        # Verify one of the descriptions contains the customizer attribute resource name
        ad_group_ad_op_create = self.mock_services["AdGroupAdService"].mutate_ad_group_ads.call_args[1]['operations'][0].create
        # The descriptions are added via extend. Check the args to extend.
        extend_call_args = ad_group_ad_op_create.ad.responsive_search_ad.descriptions.extend.call_args
        self.assertIsNotNone(extend_call_args)
        extended_assets = extend_call_args[0][0] #call_args is ((pos_args,), kwargs)
        self.assertTrue(any(
            f"CUSTOMIZER.{_CUSTOMIZER_NAME}" in asset.text # Use the simple name
            for asset in extended_assets
        ))


    @mock.patch("examples.advanced_operations.add_responsive_search_ad_full.GoogleAdsClient.load_from_storage")
    def test_main_google_ads_exception(self, mock_load_from_storage):
        mock_client = self._setup_common_mocks(mock_load_from_storage)

        # Configure CampaignBudgetService to raise an exception
        mock_error = mock.MagicMock()
        mock_error.code.return_value.name = "TestBudgetError"
        mock_failure = mock.MagicMock()
        mock_failure.errors = [mock.MagicMock(message="Test budget error message.")]

        exception_to_raise = GoogleAdsException(
            mock_error, mock_failure, "Google Ads API request failed (budget).", request_id="test_budget_req_id"
        )
        # Explicitly set the .failure attribute as the constructor might not assign it as expected
        exception_to_raise.failure = mock_failure
        self.mock_services["CampaignBudgetService"].mutate_campaign_budgets.side_effect = exception_to_raise

        mock_args = argparse.Namespace(customer_id="123", customizer_attribute_name=None)

        with mock.patch("sys.argv", ["add_responsive_search_ad_full.py", "-c", mock_args.customer_id]), \
             mock.patch("examples.advanced_operations.add_responsive_search_ad_full.argparse.ArgumentParser") as mock_argparse:
            mock_argparse.return_value.parse_args.return_value = mock_args
            with self.assertRaises(SystemExit) as cm:
                runpy.run_module("examples.advanced_operations.add_responsive_search_ad_full", run_name="__main__")
            self.assertEqual(cm.exception.code, 1)

        self.mock_services["CampaignBudgetService"].mutate_campaign_budgets.assert_called_once()

if __name__ == "__main__":
    unittest.main()
