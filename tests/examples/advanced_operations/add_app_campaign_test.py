# Copyright 2026 Google LLC
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
"""Tests for add_app_campaign example."""

from datetime import datetime
import io
import unittest
from unittest import mock

from examples.advanced_operations import add_app_campaign
from google.ads.googleads.client import GoogleAdsClient


class TestAddAppCampaign(unittest.TestCase):
    """Tests for add_app_campaign helper functions and main flow."""

    def setUp(self):
        super().setUp()
        self.client = GoogleAdsClient(
            credentials=mock.MagicMock(),
            developer_token="test_token",
            version="v24",
            use_proto_plus=True,
        )
        self.mock_services = {
            "CampaignBudgetService": mock.MagicMock(),
            "CampaignService": mock.MagicMock(),
            "CampaignCriterionService": mock.MagicMock(),
            "GeoTargetConstantService": mock.MagicMock(),
            "GoogleAdsService": mock.MagicMock(),
            "AdGroupService": mock.MagicMock(),
            "AdGroupAdService": mock.MagicMock(),
        }
        self.mock_services[
            "GeoTargetConstantService"
        ].geo_target_constant_path.side_effect = (
            lambda loc_id: f"geoTargetConstants/{loc_id}"
        )
        self.mock_services[
            "GoogleAdsService"
        ].language_constant_path.side_effect = (
            lambda lang_id: f"languageConstants/{lang_id}"
        )
        self.client.get_service = mock.MagicMock(
            side_effect=self.mock_services.__getitem__
        )

    def test_create_budget_sets_unshared_standard_budget(self):
        budget_service = self.mock_services["CampaignBudgetService"]
        budget_service.mutate_campaign_budgets.return_value.results = [
            mock.MagicMock(resource_name="customers/123/campaignBudgets/11")
        ]

        with mock.patch("sys.stdout", io.StringIO()):
            resource_name = add_app_campaign.create_budget(self.client, "123")

        self.assertEqual(resource_name, "customers/123/campaignBudgets/11")
        call_kwargs = budget_service.mutate_campaign_budgets.call_args.kwargs
        budget = call_kwargs["operations"][0].create
        self.assertEqual(budget.amount_micros, 50000000)
        self.assertEqual(
            budget.delivery_method,
            self.client.enums.BudgetDeliveryMethodEnum.STANDARD,
        )
        self.assertFalse(budget.explicitly_shared)

    @mock.patch("examples.advanced_operations.add_app_campaign.datetime")
    def test_create_campaign_anchors_iso_dates_to_single_now_call(
        self, mock_datetime
    ):
        mock_datetime.now.return_value = datetime(2026, 6, 15, 23, 59, 59)
        campaign_service = self.mock_services["CampaignService"]
        campaign_service.mutate_campaigns.return_value.results = [
            mock.MagicMock(resource_name="customers/123/campaigns/22")
        ]

        with mock.patch("sys.stdout", io.StringIO()):
            resource_name = add_app_campaign.create_campaign(
                self.client, "123", "customers/123/campaignBudgets/11"
            )

        self.assertEqual(resource_name, "customers/123/campaigns/22")
        mock_datetime.now.assert_called_once_with()

        call_kwargs = campaign_service.mutate_campaigns.call_args.kwargs
        campaign = call_kwargs["operations"][0].create
        self.assertEqual(campaign.start_date_time, "2026-06-16 00:00:00")
        self.assertEqual(campaign.end_date_time, "2027-06-15 23:59:59")
        self.assertEqual(
            campaign.advertising_channel_type,
            self.client.enums.AdvertisingChannelTypeEnum.MULTI_CHANNEL,
        )
        self.assertEqual(
            campaign.advertising_channel_sub_type,
            self.client.enums.AdvertisingChannelSubTypeEnum.APP_CAMPAIGN,
        )
        self.assertEqual(campaign.target_cpa.target_cpa_micros, 1000000)
        self.assertEqual(
            campaign.app_campaign_setting.app_id,
            "com.google.android.apps.adwords",
        )
        self.assertEqual(
            campaign.app_campaign_setting.app_store,
            self.client.enums.AppCampaignAppStoreEnum.GOOGLE_APP_STORE,
        )
        self.assertEqual(
            campaign.contains_eu_political_advertising,
            self.client.enums.EuPoliticalAdvertisingStatusEnum.DOES_NOT_CONTAIN_EU_POLITICAL_ADVERTISING,
        )

    def test_create_app_ad_builds_headlines_and_descriptions(self):
        ad_group_ad_service = self.mock_services["AdGroupAdService"]
        ad_group_ad_service.mutate_ad_group_ads.return_value.results = [
            mock.MagicMock(resource_name="customers/123/adGroupAds/33~44")
        ]

        with mock.patch("sys.stdout", io.StringIO()):
            add_app_campaign.create_app_ad(
                self.client, "123", "customers/123/adGroups/33"
            )

        call_kwargs = ad_group_ad_service.mutate_ad_group_ads.call_args.kwargs
        ad_group_ad = call_kwargs["operations"][0].create
        self.assertEqual(ad_group_ad.ad_group, "customers/123/adGroups/33")
        self.assertEqual(
            [h.text for h in ad_group_ad.ad.app_ad.headlines],
            ["A cool puzzle game", "Remove connected blocks"],
        )
        self.assertEqual(
            [d.text for d in ad_group_ad.ad.app_ad.descriptions],
            ["3 difficulty levels", "4 colorful fun skins"],
        )

    def test_main_runs_full_campaign_creation_sequence(self):
        self.mock_services[
            "CampaignBudgetService"
        ].mutate_campaign_budgets.return_value.results = [
            mock.MagicMock(resource_name="customers/123/campaignBudgets/11")
        ]
        self.mock_services[
            "CampaignService"
        ].mutate_campaigns.return_value.results = [
            mock.MagicMock(resource_name="customers/123/campaigns/22")
        ]
        self.mock_services[
            "CampaignCriterionService"
        ].mutate_campaign_criteria.return_value.results = []
        self.mock_services[
            "AdGroupService"
        ].mutate_ad_groups.return_value.results = [
            mock.MagicMock(resource_name="customers/123/adGroups/33")
        ]
        self.mock_services[
            "AdGroupAdService"
        ].mutate_ad_group_ads.return_value.results = [
            mock.MagicMock(resource_name="customers/123/adGroupAds/33~44")
        ]

        with mock.patch("sys.stdout", io.StringIO()):
            add_app_campaign.main(self.client, "123")

        self.mock_services[
            "CampaignCriterionService"
        ].mutate_campaign_criteria.assert_called_once()
        criteria_ops = self.mock_services[
            "CampaignCriterionService"
        ].mutate_campaign_criteria.call_args.kwargs["operations"]
        self.assertEqual(len(criteria_ops), 4)


if __name__ == "__main__":
    unittest.main()
