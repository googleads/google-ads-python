import unittest
from unittest import mock
import sys

sys.path.insert(0, '/app') # For subtask environment

from examples.advanced_operations import add_app_campaign

class TestAddAppCampaign(unittest.TestCase):

    def _setup_common_mocks(self, mock_google_ads_client):
        mock_google_ads_client.version = "v19"

        # Mock services
        mock_budget_service = mock.Mock()
        mock_campaign_service = mock.Mock()
        mock_criterion_service = mock.Mock()
        mock_geo_service = mock.Mock()
        mock_google_ads_service = mock.Mock() # For language_constant_path
        mock_ad_group_service = mock.Mock()
        mock_ad_group_ad_service = mock.Mock()

        def get_service_side_effect(service_name, version=None):
            self.assertEqual("v19", version if version else mock_google_ads_client.version)
            services = {
                "CampaignBudgetService": mock_budget_service,
                "CampaignService": mock_campaign_service,
                "CampaignCriterionService": mock_criterion_service,
                "GeoTargetConstantService": mock_geo_service,
                "GoogleAdsService": mock_google_ads_service,
                "AdGroupService": mock_ad_group_service,
                "AdGroupAdService": mock_ad_group_ad_service,
            }
            if service_name in services:
                return services[service_name]
            self.fail(f"Unexpected service requested: {service_name}")
        mock_google_ads_client.get_service.side_effect = get_service_side_effect

        # Mock Enums
        mock_google_ads_client.enums.BudgetDeliveryMethodEnum.STANDARD = "BUDGET_STANDARD"
        mock_google_ads_client.enums.CampaignStatusEnum.PAUSED = "CAMPAIGN_PAUSED"
        mock_google_ads_client.enums.AdvertisingChannelTypeEnum.MULTI_CHANNEL = "MULTI_CHANNEL_TYPE"
        mock_google_ads_client.enums.AdvertisingChannelSubTypeEnum.APP_CAMPAIGN = "APP_CAMPAIGN_SUB_TYPE"
        app_campaign_app_store_enum_mock = mock.Mock(name="AppCampaignAppStoreEnumMock")
        # Store the PropertyMock on self to assert it was called
        self.app_store_enum_property_mock = mock.PropertyMock(return_value="APP_STORE_GOOGLE_FROM_PROPERTY")
        type(app_campaign_app_store_enum_mock).GOOGLE_APP_STORE = self.app_store_enum_property_mock
        mock_google_ads_client.enums.AppCampaignAppStoreEnum = app_campaign_app_store_enum_mock
        mock_google_ads_client.enums.AppCampaignBiddingStrategyGoalTypeEnum.OPTIMIZE_INSTALLS_TARGET_INSTALL_COST = "GOAL_INSTALLS"
        mock_google_ads_client.enums.AdGroupStatusEnum.ENABLED = "AD_GROUP_ENABLED"
        # AdGroupAdStatusEnum is not directly used in the script for App Campaigns, ads are added via AdAssets.

        # Mock GetType objects
        self.mock_objects = {} # Store created mock objects for assertions

        def get_type_side_effect(type_name, version=None):
            mock_op = mock.Mock(name=f"{type_name}_Operation")
            # mock_create_obj is the object that operation.create would return (e.g. Campaign, AdGroup)
            mock_create_obj = mock.Mock(name=f"{type_name}_CreateObject_For_{type_name.replace('Operation', '')}")

            if type_name == "CampaignOperation":
                mock_op.create = mock_create_obj
                # Make app_campaign a MagicMock to see if it handles attribute assignment differently
                mock_create_obj.app_campaign = mock.MagicMock(name="AppCampaignSetting_MagicMock")
                self.mock_objects["Campaign"] = mock_create_obj
                return mock_op
            elif type_name == "AdGroupAdOperation":
                mock_op.create = mock_create_obj
                ad_data_mock = mock.Mock(name="AdData_On_AdGroupAd")
                # Pre-create nested structures for AppAdInfo
                app_ad_info_mock = mock.Mock(name="AppAdInfo_On_AdData")
                app_ad_info_mock.headlines = [] # Initialize as lists for append
                app_ad_info_mock.descriptions = []
                ad_data_mock.app_ad = app_ad_info_mock
                mock_create_obj.ad = ad_data_mock
                self.mock_objects["AdGroupAd"] = mock_create_obj
                return mock_op
            elif "Operation" in type_name: # For other operations (Budget, Criterion, AdGroup)
                mock_op.create = mock_create_obj
                self.mock_objects[type_name.replace("Operation", "")] = mock_create_obj
                return mock_op
            elif type_name == "AdTextAsset":
                # _create_ad_text_asset just sets the 'text' attribute.
                mock_ad_text_asset = mock.Mock(name="AdTextAsset_Instance")
                # self.mock_objects.setdefault("AdTextAssets", []).append(mock_ad_text_asset) # Store if needed for direct check
                return mock_ad_text_asset # Return the asset itself, script appends it to lists on app_ad

            self.fail(f"Unexpected type requested: {type_name}")

        mock_google_ads_client.get_type.side_effect = get_type_side_effect

        return (mock_budget_service, mock_campaign_service, mock_criterion_service,
                mock_geo_service, mock_google_ads_service, mock_ad_group_service,
                mock_ad_group_ad_service)

    @mock.patch("examples.advanced_operations.add_app_campaign.GoogleAdsClient.load_from_storage")
    def test_main_functional(self, mock_load_from_storage):
        mock_google_ads_client = mock.Mock()
        (mock_budget_service, mock_campaign_service, mock_criterion_service,
         mock_geo_service, mock_google_ads_service, mock_ad_group_service,
         mock_ad_group_ad_service) = self._setup_common_mocks(mock_google_ads_client)

        customer_id = "cust123"
        expected_budget_rn = f"customers/{customer_id}/campaignBudgets/budget1"
        expected_campaign_rn = f"customers/{customer_id}/campaigns/campaign1"
        expected_ad_group_rn = f"customers/{customer_id}/adGroups/adgroup1"
        expected_ad_group_ad_rn = f"customers/{customer_id}/adGroupAds/ad1" # Script creates 1 ad with multiple assets

        # Configure service responses
        mock_budget_service.mutate_campaign_budgets.return_value = mock.Mock(results=[mock.Mock(resource_name=expected_budget_rn)])
        mock_campaign_service.mutate_campaigns.return_value = mock.Mock(results=[mock.Mock(resource_name=expected_campaign_rn)])
        # mutate_campaign_criteria is called twice (language, location)
        mock_criterion_service.mutate_campaign_criteria.return_value = mock.Mock(results=[mock.Mock(resource_name="crit1"), mock.Mock(resource_name="crit2")])
        mock_ad_group_service.mutate_ad_groups.return_value = mock.Mock(results=[mock.Mock(resource_name=expected_ad_group_rn)])
        mock_ad_group_ad_service.mutate_ad_group_ads.return_value = mock.Mock(results=[mock.Mock(resource_name=expected_ad_group_ad_rn)])

        # Configure path methods
        mock_google_ads_service.language_constant_path.return_value = "languageConstants/1000" # English
        mock_geo_service.geo_target_constant_path.return_value = "geoTargetConstants/2840" # USA

        # Call the main function
        add_app_campaign.main(mock_google_ads_client, customer_id)

        # --- Assertions ---
        # Budget
        mock_budget_service.mutate_campaign_budgets.assert_called_once()
        budget_op_kwargs = mock_budget_service.mutate_campaign_budgets.call_args[1]
        self.assertEqual(budget_op_kwargs['customer_id'], customer_id)
        budget_obj = self.mock_objects.get("CampaignBudget")
        self.assertIsNotNone(budget_obj)
        self.assertEqual(budget_obj.delivery_method, "BUDGET_STANDARD")

        # Campaign
        mock_campaign_service.mutate_campaigns.assert_called_once()
        campaign_op_kwargs = mock_campaign_service.mutate_campaigns.call_args[1]
        self.assertEqual(campaign_op_kwargs['customer_id'], customer_id)
        campaign_obj = self.mock_objects.get("Campaign")
        self.assertIsNotNone(campaign_obj)
        # Call to main was here, it should be before assertions.
        # add_app_campaign.main(mock_google_ads_client, customer_id) # This is correctly placed before assertions.

        self.assertEqual(campaign_obj.status, "CAMPAIGN_PAUSED")
        self.assertEqual(campaign_obj.campaign_budget, expected_budget_rn)
        self.assertEqual(campaign_obj.advertising_channel_type, "MULTI_CHANNEL_TYPE")
        self.assertEqual(campaign_obj.advertising_channel_sub_type, "APP_CAMPAIGN_SUB_TYPE")

        # Assertions for campaign.app_campaign fields
        # First, assert that our PropertyMock for the enum value was called
        self.app_store_enum_property_mock.assert_called_once()
        self.assertEqual(campaign_obj.app_campaign.app_store, "APP_STORE_GOOGLE_FROM_PROPERTY")
        self.assertEqual(campaign_obj.app_campaign.app_id, "com.google.android.apps.adwords")
        self.assertEqual(campaign_obj.app_campaign.bidding_strategy_goal_type, "GOAL_INSTALLS")

        # Campaign Criteria (Language & Location)
        self.assertEqual(mock_criterion_service.mutate_campaign_criteria.call_count, 2)
        criterion_calls = mock_criterion_service.mutate_campaign_criteria.call_args_list

        # Language Criterion
        lang_crit_op_kwargs = criterion_calls[0][1] # second arg tuple, first item is args, second is kwargs
        self.assertEqual(lang_crit_op_kwargs['customer_id'], customer_id)
        lang_crit_obj = lang_crit_op_kwargs['operations'][0].create # Assuming one op per call for simplicity
        self.assertEqual(lang_crit_obj.campaign, expected_campaign_rn)
        self.assertEqual(lang_crit_obj.language.language_constant, "languageConstants/1000")

        # Location Criterion
        loc_crit_op_kwargs = criterion_calls[1][1]
        self.assertEqual(loc_crit_op_kwargs['customer_id'], customer_id)
        loc_crit_obj = loc_crit_op_kwargs['operations'][0].create
        self.assertEqual(loc_crit_obj.campaign, expected_campaign_rn)
        self.assertEqual(loc_crit_obj.location.geo_target_constant, "geoTargetConstants/2840")

        # Ad Group
        mock_ad_group_service.mutate_ad_groups.assert_called_once()
        ad_group_op_kwargs = mock_ad_group_service.mutate_ad_groups.call_args[1]
        self.assertEqual(ad_group_op_kwargs['customer_id'], customer_id)
        ad_group_obj = self.mock_objects.get("AdGroup")
        self.assertIsNotNone(ad_group_obj)
        self.assertEqual(ad_group_obj.campaign, expected_campaign_rn)
        self.assertEqual(ad_group_obj.status, "AD_GROUP_ENABLED")

        # Ad Group Ad (App Ad)
        mock_ad_group_ad_service.mutate_ad_group_ads.assert_called_once()
        ad_group_ad_op_kwargs = mock_ad_group_ad_service.mutate_ad_group_ads.call_args[1]
        self.assertEqual(ad_group_ad_op_kwargs['customer_id'], customer_id)
        ad_group_ad_obj = self.mock_objects.get("AdGroupAd")
        self.assertIsNotNone(ad_group_ad_obj)
        self.assertEqual(ad_group_ad_obj.ad_group, expected_ad_group_rn)
        # Check app_ad specific fields on ad_group_ad_obj.ad.app_ad
        app_ad_info = ad_group_ad_obj.ad.app_ad # Access the nested mock

        # Check AdTextAssets were created and linked
        # The script's _create_ad_text_asset returns a new AdTextAsset mock each time.
        # These are then appended to app_ad_info.headlines and app_ad_info.descriptions.
        self.assertEqual(len(app_ad_info.headlines), 5) # Script adds 5 headlines
        self.assertEqual(len(app_ad_info.descriptions), 5) # Script adds 5 descriptions

        # Verify the content of these assets (example for the first headline and description)
        # The AdTextAsset mocks were returned by get_type, then script set .text and appended them.
        self.assertTrue(any(headline.text == "App Ad Headline #1" for headline in app_ad_info.headlines))
        self.assertTrue(any(desc.text == "App Ad Description #1" for desc in app_ad_info.descriptions))

if __name__ == "__main__":
    unittest.main()
