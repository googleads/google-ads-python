# Copyright 2021 Google LLC
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
"""Tests for add_app_campaign.py."""

from unittest import mock
from unittest import TestCase

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.ads.googleads.v20.enums import (
    BudgetDeliveryMethodEnum,
    CampaignStatusEnum,
    AdvertisingChannelTypeEnum,
    AdvertisingChannelSubTypeEnum,
    AppCampaignAppStoreEnum,
    AppCampaignBiddingStrategyGoalTypeEnum,
    AdGroupStatusEnum,
    AdGroupAdStatusEnum,
)

from examples.advanced_operations.add_app_campaign import (
    main,
    create_budget,
    create_campaign,
    set_campaign_targeting_criteria,
    create_ad_group,
    create_app_ad,
    create_ad_text_asset,
)

_CUSTOMER_ID = "1234567890"
_BUDGET_RESOURCE_NAME = f"customers/{_CUSTOMER_ID}/campaignBudgets/1"
_CAMPAIGN_RESOURCE_NAME = f"customers/{_CUSTOMER_ID}/campaigns/1"
_AD_GROUP_RESOURCE_NAME = f"customers/{_CUSTOMER_ID}/adGroups/1"
_AD_GROUP_AD_RESOURCE_NAME = f"customers/{_CUSTOMER_ID}/adGroupAds/1"
_GEO_TARGET_CONSTANT_NAME_CALIFORNIA = "geoTargetConstants/21137" # California
_GEO_TARGET_CONSTANT_NAME_MEXICO = "geoTargetConstants/2484" # Mexico
_LANGUAGE_CONSTANT_ENGLISH = "languageConstants/1000" # English
_LANGUAGE_CONSTANT_SPANISH = "languageConstants/1003" # Spanish


@mock.patch("examples.advanced_operations.add_app_campaign.GoogleAdsClient.load_from_storage")
class AddAppCampaignTest(TestCase):
    def setUp(self):
        self.client_mock = mock.MagicMock(spec=GoogleAdsClient)
        self.campaign_budget_service_mock = self.client_mock.get_service("CampaignBudgetService")
        self.campaign_service_mock = self.client_mock.get_service("CampaignService")
        self.campaign_criterion_service_mock = self.client_mock.get_service("CampaignCriterionService")
        self.geo_target_constant_service_mock = self.client_mock.get_service("GeoTargetConstantService")
        self.googleads_service_mock = self.client_mock.get_service("GoogleAdsService")
        self.ad_group_service_mock = self.client_mock.get_service("AdGroupService")
        self.ad_group_ad_service_mock = self.client_mock.get_service("AdGroupAdService")

        # Mock enums needed by the script
        self.client_mock.enums = mock.MagicMock() # Ensure enums attribute exists

        mock_budget_delivery_method_enum = mock.MagicMock()
        mock_budget_delivery_method_enum.STANDARD = 2
        self.client_mock.enums.BudgetDeliveryMethodEnum = mock_budget_delivery_method_enum

        mock_campaign_status_enum = mock.MagicMock()
        mock_campaign_status_enum.PAUSED = 3
        self.client_mock.enums.CampaignStatusEnum = mock_campaign_status_enum

        mock_ad_channel_type_enum = mock.MagicMock()
        mock_ad_channel_type_enum.MULTI_CHANNEL = 8
        self.client_mock.enums.AdvertisingChannelTypeEnum = mock_ad_channel_type_enum

        mock_ad_channel_sub_type_enum = mock.MagicMock()
        mock_ad_channel_sub_type_enum.APP_CAMPAIGN = 2
        self.client_mock.enums.AdvertisingChannelSubTypeEnum = mock_ad_channel_sub_type_enum

        mock_app_store_enum = mock.MagicMock()
        mock_app_store_enum.GOOGLE_APP_STORE = 2
        self.client_mock.enums.AppCampaignAppStoreEnum = mock_app_store_enum

        mock_bidding_strategy_goal_enum = mock.MagicMock()
        mock_bidding_strategy_goal_enum.OPTIMIZE_INSTALLS_TARGET_INSTALL_COST = 2
        self.client_mock.enums.AppCampaignBiddingStrategyGoalTypeEnum = mock_bidding_strategy_goal_enum

        mock_ad_group_status_enum = mock.MagicMock()
        mock_ad_group_status_enum.ENABLED = 2
        self.client_mock.enums.AdGroupStatusEnum = mock_ad_group_status_enum

        mock_ad_group_ad_status_enum = mock.MagicMock()
        mock_ad_group_ad_status_enum.ENABLED = 2
        self.client_mock.enums.AdGroupAdStatusEnum = mock_ad_group_ad_status_enum

        # Mock responses
        self.campaign_budget_service_mock.mutate_campaign_budgets.return_value.results = [
            mock.Mock(resource_name=_BUDGET_RESOURCE_NAME)
        ]
        self.campaign_service_mock.mutate_campaigns.return_value.results = [
            mock.Mock(resource_name=_CAMPAIGN_RESOURCE_NAME)
        ]
        self.campaign_criterion_service_mock.mutate_campaign_criteria.return_value.results = [
            mock.Mock(resource_name="criterion1"), mock.Mock(resource_name="criterion2"),
            mock.Mock(resource_name="criterion3"), mock.Mock(resource_name="criterion4"),
        ]
        self.ad_group_service_mock.mutate_ad_groups.return_value.results = [
            mock.Mock(resource_name=_AD_GROUP_RESOURCE_NAME)
        ]
        self.ad_group_ad_service_mock.mutate_ad_group_ads.return_value.results = [
            mock.Mock(resource_name=_AD_GROUP_AD_RESOURCE_NAME)
        ]

        # Mock path helpers
        self.geo_target_constant_service_mock.geo_target_constant_path.side_effect = [
            _GEO_TARGET_CONSTANT_NAME_CALIFORNIA, _GEO_TARGET_CONSTANT_NAME_MEXICO
        ]
        self.googleads_service_mock.language_constant_path.side_effect = [
            _LANGUAGE_CONSTANT_ENGLISH, _LANGUAGE_CONSTANT_SPANISH
        ]

        # Mock types for create_ad_text_asset
        self.client_mock.get_type.return_value = mock.MagicMock()


    def test_create_budget(self, mock_load_client):
        mock_load_client.return_value = self.client_mock
        budget_rn = create_budget(self.client_mock, _CUSTOMER_ID)
        self.assertEqual(budget_rn, _BUDGET_RESOURCE_NAME)
        self.campaign_budget_service_mock.mutate_campaign_budgets.assert_called_once()
        # TODO: Add assertions on operation details


    def test_create_campaign(self, mock_load_client):
        mock_load_client.return_value = self.client_mock
        campaign_rn = create_campaign(self.client_mock, _CUSTOMER_ID, _BUDGET_RESOURCE_NAME)
        self.assertEqual(campaign_rn, _CAMPAIGN_RESOURCE_NAME)
        self.campaign_service_mock.mutate_campaigns.assert_called_once()
        # TODO: Add assertions on operation details


    def test_set_campaign_targeting_criteria(self, mock_load_client):
        mock_load_client.return_value = self.client_mock
        set_campaign_targeting_criteria(self.client_mock, _CUSTOMER_ID, _CAMPAIGN_RESOURCE_NAME)
        self.campaign_criterion_service_mock.mutate_campaign_criteria.assert_called_once()
        self.assertEqual(self.geo_target_constant_service_mock.geo_target_constant_path.call_count, 2)
        self.assertEqual(self.googleads_service_mock.language_constant_path.call_count, 2)
        # TODO: Add assertions on operation details (e.g. types of criteria)


    def test_create_ad_group(self, mock_load_client):
        mock_load_client.return_value = self.client_mock
        ad_group_rn = create_ad_group(self.client_mock, _CUSTOMER_ID, _CAMPAIGN_RESOURCE_NAME)
        self.assertEqual(ad_group_rn, _AD_GROUP_RESOURCE_NAME)
        self.ad_group_service_mock.mutate_ad_groups.assert_called_once()
        # TODO: Add assertions on operation details


    def test_create_ad_text_asset(self, mock_load_client):
        mock_load_client.return_value = self.client_mock
        text = "Test asset text"
        # Configure get_type to return a mock AdTextAsset that can have 'text' set
        mock_ad_text_asset = mock.MagicMock()
        self.client_mock.get_type.return_value = mock_ad_text_asset

        asset = create_ad_text_asset(self.client_mock, text)

        self.client_mock.get_type.assert_called_once_with("AdTextAsset")
        self.assertEqual(asset.text, text)


    def test_create_app_ad(self, mock_load_client):
        mock_load_client.return_value = self.client_mock
        # Mock create_ad_text_asset to simplify this test
        with mock.patch("examples.advanced_operations.add_app_campaign.create_ad_text_asset") as mock_create_text_asset:
            mock_asset = mock.MagicMock()
            mock_create_text_asset.return_value = mock_asset

            ad_rn = create_app_ad(self.client_mock, _CUSTOMER_ID, _AD_GROUP_RESOURCE_NAME)

            self.assertEqual(ad_rn, _AD_GROUP_AD_RESOURCE_NAME)
            self.ad_group_ad_service_mock.mutate_ad_group_ads.assert_called_once()
            self.assertEqual(mock_create_text_asset.call_count, 4) # Called for 2 headlines and 2 descriptions
            # TODO: Add assertions on operation details (e.g. number of headlines/descriptions)


    @mock.patch("examples.advanced_operations.add_app_campaign.create_budget")
    @mock.patch("examples.advanced_operations.add_app_campaign.create_campaign")
    @mock.patch("examples.advanced_operations.add_app_campaign.set_campaign_targeting_criteria")
    @mock.patch("examples.advanced_operations.add_app_campaign.create_ad_group")
    @mock.patch("examples.advanced_operations.add_app_campaign.create_app_ad")
    def test_main_success(
        self,
        mock_create_app_ad,
        mock_create_ad_group,
        mock_set_targeting,
        mock_create_campaign,
        mock_create_budget,
        mock_load_client
    ):
        mock_load_client.return_value = self.client_mock
        mock_create_budget.return_value = _BUDGET_RESOURCE_NAME
        mock_create_campaign.return_value = _CAMPAIGN_RESOURCE_NAME
        mock_create_ad_group.return_value = _AD_GROUP_RESOURCE_NAME

        main(self.client_mock, _CUSTOMER_ID)

        mock_create_budget.assert_called_once_with(self.client_mock, _CUSTOMER_ID)
        mock_create_campaign.assert_called_once_with(self.client_mock, _CUSTOMER_ID, _BUDGET_RESOURCE_NAME)
        mock_set_targeting.assert_called_once_with(self.client_mock, _CUSTOMER_ID, _CAMPAIGN_RESOURCE_NAME)
        mock_create_ad_group.assert_called_once_with(self.client_mock, _CUSTOMER_ID, _CAMPAIGN_RESOURCE_NAME)
        mock_create_app_ad.assert_called_once_with(self.client_mock, _CUSTOMER_ID, _AD_GROUP_RESOURCE_NAME)


    @mock.patch("examples.advanced_operations.add_app_campaign.create_budget")
    def test_main_google_ads_exception(self, mock_create_budget, mock_load_client):
        mock_load_client.return_value = self.client_mock
        mock_create_budget.side_effect = GoogleAdsException(
            error=mock.Mock(),
            failure=mock.Mock(errors=[mock.Mock(message="Test Error")]),
            request_id="test_request_id",
            call=mock.Mock()
        )

        with self.assertRaises(GoogleAdsException):
            main(self.client_mock, _CUSTOMER_ID)

if __name__ == "__main__":
    TestCase.main()
