import unittest
from unittest import mock
import sys

sys.path.insert(0, '/app') # For subtask environment

from examples.advanced_operations import add_dynamic_search_ads

class TestAddDynamicSearchAds(unittest.TestCase):

    def _setup_common_mocks(self, mock_google_ads_client):
        mock_google_ads_client.version = "v19"
        self.mock_objects = {}  # To store .create objects from operations
        self.webpage_condition_mocks = [] # To store WebpageConditionInfo mocks

        # Mock Services
        mock_budget_service = mock.Mock(name="CampaignBudgetService")
        mock_campaign_service = mock.Mock(name="CampaignService")
        mock_ad_group_service = mock.Mock(name="AdGroupService")
        mock_ad_group_ad_service = mock.Mock(name="AdGroupAdService")
        mock_criterion_service = mock.Mock(name="AdGroupCriterionService")

        def get_service_side_effect(service_name, version=None):
            self.assertEqual("v19", version if version else mock_google_ads_client.version)
            services = {
                "CampaignBudgetService": mock_budget_service,
                "CampaignService": mock_campaign_service,
                "AdGroupService": mock_ad_group_service,
                "AdGroupAdService": mock_ad_group_ad_service,
                "AdGroupCriterionService": mock_criterion_service,
            }
            if service_name in services:
                return services[service_name]
            self.fail(f"Unexpected service requested: {service_name}")
        mock_google_ads_client.get_service.side_effect = get_service_side_effect

        # Mock Enums
        mock_google_ads_client.enums.BudgetDeliveryMethodEnum.STANDARD = "BUDGET_STANDARD"
        mock_google_ads_client.enums.AdvertisingChannelTypeEnum.SEARCH = "SEARCH_CHANNEL"
        mock_google_ads_client.enums.CampaignStatusEnum.PAUSED = "CAMPAIGN_PAUSED"
        mock_google_ads_client.enums.AdGroupTypeEnum.SEARCH_DYNAMIC_ADS = "ADGROUP_DSA_TYPE"
        # Script sets AdGroup status to PAUSED initially
        ad_group_status_enum_mock = mock.Mock()
        ad_group_status_enum_mock.ENABLED = "ADGROUP_ENABLED"
        ad_group_status_enum_mock.PAUSED = "ADGROUP_PAUSED" # Script uses PAUSED
        mock_google_ads_client.enums.AdGroupStatusEnum = ad_group_status_enum_mock
        mock_google_ads_client.enums.AdGroupAdStatusEnum.PAUSED = "ADGROUPAD_PAUSED" # Script uses PAUSED for AdGroupAd
        # Script sets AdGroupCriterion status to PAUSED
        ad_group_criterion_status_enum_mock = mock.Mock()
        ad_group_criterion_status_enum_mock.ENABLED = "CRITERION_ENABLED"
        ad_group_criterion_status_enum_mock.PAUSED = "CRITERION_PAUSED" # Script uses PAUSED
        mock_google_ads_client.enums.AdGroupCriterionStatusEnum = ad_group_criterion_status_enum_mock
        # For WebpageConditionInfo
        operand_enum = mock.Mock()
        operand_enum.URL = "OPERAND_URL"
        operand_enum.PAGE_TITLE = "OPERAND_PAGE_TITLE"
        mock_google_ads_client.enums.WebpageConditionOperandEnum = operand_enum


        def get_type_side_effect(type_name, version=None):
            mock_op = mock.Mock(name=f"{type_name}_Operation")
            mock_create_obj = mock.Mock(name=f"{type_name}_CreateObject_For_{type_name.replace('Operation', '')}")

            if type_name == "CampaignOperation":
                mock_op.create = mock_create_obj
                mock_create_obj.dynamic_search_ads_setting = mock.Mock(name="DynamicSearchAdsSetting")
                self.mock_objects["Campaign"] = mock_create_obj
                return mock_op
            elif type_name == "AdGroupCriterionOperation":
                mock_op.create = mock_create_obj
                mock_create_obj.webpage = mock.Mock(name="WebpageCriterionInfo")
                mock_create_obj.webpage.conditions = [] # Initialize list for append
                self.mock_objects["AdGroupCriterion"] = mock_create_obj
                return mock_op
            elif "Operation" in type_name: # Budget, AdGroup, AdGroupAd
                mock_op.create = mock_create_obj
                self.mock_objects[type_name.replace("Operation", "")] = mock_create_obj
                return mock_op
            elif type_name == "WebpageConditionInfo":
                # Script creates multiple WebpageConditionInfo objects
                condition_mock = mock.Mock(name=f"WebpageConditionInfo_Instance_{len(self.webpage_condition_mocks)+1}")
                self.webpage_condition_mocks.append(condition_mock)
                return condition_mock

            self.fail(f"Unexpected type requested: {type_name}")
        mock_google_ads_client.get_type.side_effect = get_type_side_effect

        return (mock_budget_service, mock_campaign_service, mock_ad_group_service,
                mock_ad_group_ad_service, mock_criterion_service)

    @mock.patch("examples.advanced_operations.add_dynamic_search_ads.GoogleAdsClient.load_from_storage")
    def test_main_functional(self, mock_load_from_storage):
        mock_google_ads_client = mock.Mock()
        (mock_budget_service, mock_campaign_service, mock_ad_group_service,
         mock_ad_group_ad_service, mock_criterion_service) = self._setup_common_mocks(mock_google_ads_client)

        customer_id = "custDSA123"
        budget_rn = f"customers/{customer_id}/campaignBudgets/budgetDSA"
        campaign_rn = f"customers/{customer_id}/campaigns/campaignDSA"
        ad_group_rn = f"customers/{customer_id}/adGroups/adGroupDSA"
        ad_group_ad_rn = f"customers/{customer_id}/adGroupAds/adDSA"
        criterion_rn = f"customers/{customer_id}/adGroupCriteria/criterionDSA"

        # Service responses
        mock_budget_service.mutate_campaign_budgets.return_value = mock.Mock(results=[mock.Mock(resource_name=budget_rn)])
        mock_campaign_service.mutate_campaigns.return_value = mock.Mock(results=[mock.Mock(resource_name=campaign_rn)])
        mock_ad_group_service.mutate_ad_groups.return_value = mock.Mock(results=[mock.Mock(resource_name=ad_group_rn)])
        mock_ad_group_ad_service.mutate_ad_group_ads.return_value = mock.Mock(results=[mock.Mock(resource_name=ad_group_ad_rn)])
        mock_criterion_service.mutate_ad_group_criteria.return_value = mock.Mock(results=[mock.Mock(resource_name=criterion_rn)])

        add_dynamic_search_ads.main(mock_google_ads_client, customer_id)

        # --- Assertions ---
        # Budget
        mock_budget_service.mutate_campaign_budgets.assert_called_once()
        budget_obj = self.mock_objects.get("CampaignBudget")
        self.assertEqual(budget_obj.delivery_method, "BUDGET_STANDARD")
        self.assertTrue(hasattr(budget_obj, "name")) # Name is set with uuid

        # Campaign
        mock_campaign_service.mutate_campaigns.assert_called_once()
        campaign_obj = self.mock_objects.get("Campaign")
        self.assertEqual(campaign_obj.campaign_budget, budget_rn)
        self.assertEqual(campaign_obj.status, "CAMPAIGN_PAUSED")
        self.assertEqual(campaign_obj.advertising_channel_type, "SEARCH_CHANNEL")
        self.assertTrue(hasattr(campaign_obj, "name")) # Name is set with uuid
        # DSA Settings
        self.assertEqual(campaign_obj.dynamic_search_ads_setting.domain_name, "example.com")
        self.assertEqual(campaign_obj.dynamic_search_ads_setting.language_code, "en")

        # AdGroup
        mock_ad_group_service.mutate_ad_groups.assert_called_once()
        ad_group_obj = self.mock_objects.get("AdGroup")
        self.assertEqual(ad_group_obj.campaign, campaign_rn)
        self.assertEqual(ad_group_obj.type_, "ADGROUP_DSA_TYPE")
        self.assertEqual(ad_group_obj.status, "ADGROUP_PAUSED") # Script sets to PAUSED
        self.assertTrue(hasattr(ad_group_obj, "name"))

        # AdGroupAd (ExpandedDynamicSearchAd)
        mock_ad_group_ad_service.mutate_ad_group_ads.assert_called_once()
        ad_group_ad_obj = self.mock_objects.get("AdGroupAd")
        self.assertEqual(ad_group_ad_obj.ad_group, ad_group_rn)
        self.assertEqual(ad_group_ad_obj.status, "ADGROUPAD_PAUSED")
        # Check Ad (ExpandedDynamicSearchAdInfo)
        self.assertIsNotNone(ad_group_ad_obj.ad.expanded_dynamic_search_ad)
        self.assertEqual(ad_group_ad_obj.ad.expanded_dynamic_search_ad.description, "Buy tickets now!") # Corrected

        # AdGroupCriterion (Webpage criterion)
        mock_criterion_service.mutate_ad_group_criteria.assert_called_once()
        criterion_obj = self.mock_objects.get("AdGroupCriterion")
        self.assertEqual(criterion_obj.ad_group, ad_group_rn)
        self.assertEqual(criterion_obj.status, "CRITERION_PAUSED") # Corrected based on script
        self.assertIsNotNone(criterion_obj.webpage)
        self.assertEqual(criterion_obj.webpage.criterion_name, "Special Offers") # Corrected path to webpage.criterion_name

        # Check Webpage Conditions (script adds 2)
        self.assertEqual(len(self.webpage_condition_mocks), 2)
        self.assertEqual(len(criterion_obj.webpage.conditions), 2)

        condition1_script_mock = criterion_obj.webpage.conditions[0]
        self.assertEqual(condition1_script_mock.operand, "OPERAND_URL")
        self.assertEqual(condition1_script_mock.argument, "/specialoffers") # Corrected

        condition2_script_mock = criterion_obj.webpage.conditions[1]
        self.assertEqual(condition2_script_mock.operand, "OPERAND_PAGE_TITLE")
        self.assertEqual(condition2_script_mock.argument, "Special Offer") # Corrected

if __name__ == '__main__':
    unittest.main()
