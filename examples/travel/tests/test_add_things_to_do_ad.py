import unittest
from unittest.mock import patch, MagicMock, call
# import argparse # No longer needed
import sys
# import importlib # No longer needed

sys.path.append(".")
sys.path.append("examples")

from travel import add_things_to_do_ad

class TestAddThingsToDoAd(unittest.TestCase):

    @patch("travel.add_things_to_do_ad.GoogleAdsClient") # Patch class
    # Removed argparse patch
    def test_main(self, MockGoogleAdsClient): # Receive patched class
        mock_client_instance = MockGoogleAdsClient.return_value # Get instance

        customer_id = "test_customer_id"
        things_to_do_center_account_id = 67890

        mock_campaign_budget_service = MagicMock()
        mock_campaign_service = MagicMock()
        mock_ad_group_service = MagicMock()
        mock_ad_group_ad_service = MagicMock()

        mock_client_instance.get_service.side_effect = [
            mock_campaign_budget_service,
            mock_campaign_service,
            mock_ad_group_service,
            mock_ad_group_ad_service,
        ]

        # Mock service responses
        mock_budget_response = MagicMock()
        mock_budget_response.results = [MagicMock(resource_name="budget_resource_name_ttd")]
        mock_campaign_budget_service.mutate_campaign_budgets.return_value = mock_budget_response

        mock_campaign_response = MagicMock()
        mock_campaign_response.results = [MagicMock(resource_name="campaign_resource_name_ttd")]
        mock_campaign_service.mutate_campaigns.return_value = mock_campaign_response

        mock_ad_group_response = MagicMock()
        mock_ad_group_response.results = [MagicMock(resource_name="ad_group_resource_name_ttd")]
        mock_ad_group_service.mutate_ad_groups.return_value = mock_ad_group_response

        mock_ad_group_ad_response = MagicMock()
        mock_ad_group_ad_response.results = [MagicMock(resource_name="ad_group_ad_resource_name_ttd")]
        mock_ad_group_ad_service.mutate_ad_group_ads.return_value = mock_ad_group_ad_response

        # Mock types and enums on the client instance
        type_mocks = {}
        def get_type_dynamic(type_name):
            if type_name not in type_mocks:
                mock_type_obj = MagicMock(name=type_name)
                if type_name == "CampaignBudgetOperation":
                    mock_type_obj.create = MagicMock()
                elif type_name == "CampaignOperation":
                    mock_type_obj.create = MagicMock()
                    mock_type_obj.create.travel_campaign_settings = MagicMock()
                    mock_type_obj.create.network_settings = MagicMock()
                    # For maximize_conversion_value, it's assigned client.get_type("MaximizeConversionValue")
                    # So, ensure that type returns a mock that can be assigned.
                elif type_name == "AdGroupOperation":
                    mock_type_obj.create = MagicMock()
                elif type_name == "AdGroupAdOperation":
                    mock_type_obj.create = MagicMock()
                    mock_type_obj.create.ad = MagicMock() # For ad.travel_ad
                elif type_name == "MaximizeConversionValue": # This is a type itself
                    pass # Just needs to be assignable
                elif type_name == "TravelAdInfo": # This is a type itself
                    pass # Just needs to be assignable
                type_mocks[type_name] = mock_type_obj
            return type_mocks[type_name]

        mock_client_instance.get_type.side_effect = get_type_dynamic

        mock_client_instance.enums = MagicMock()
        mock_client_instance.enums.BudgetDeliveryMethodEnum.STANDARD = "STANDARD"
        mock_client_instance.enums.AdvertisingChannelTypeEnum.TRAVEL = "TRAVEL"
        mock_client_instance.enums.AdvertisingChannelSubTypeEnum.TRAVEL_ACTIVITIES = "TRAVEL_ACTIVITIES"
        mock_client_instance.enums.CampaignStatusEnum.PAUSED = "PAUSED"
        mock_client_instance.enums.AdGroupTypeEnum.TRAVEL_ADS = "TRAVEL_ADS"
        mock_client_instance.enums.AdGroupStatusEnum.ENABLED = "ENABLED"
        mock_client_instance.enums.AdGroupAdStatusEnum.ENABLED = "ENABLED"

        with patch("builtins.print") as mock_print:
            add_things_to_do_ad.main(
                mock_client_instance, # Pass instance
                customer_id,
                things_to_do_center_account_id,
            )

        # No load_from_storage assertion

        # Check service calls and operation details
        mock_campaign_budget_service.mutate_campaign_budgets.assert_called_once()
        budget_op_create = mock_campaign_budget_service.mutate_campaign_budgets.call_args[1]['operations'][0].create
        self.assertEqual(budget_op_create.explicitly_shared, True)
        self.assertTrue(budget_op_create.name.startswith("Interplanetary Cruise Budget #"))

        mock_campaign_service.mutate_campaigns.assert_called_once()
        campaign_op_create = mock_campaign_service.mutate_campaigns.call_args[1]['operations'][0].create
        self.assertEqual(campaign_op_create.advertising_channel_type, "TRAVEL")
        self.assertEqual(campaign_op_create.advertising_channel_sub_type, "TRAVEL_ACTIVITIES")
        self.assertEqual(campaign_op_create.travel_campaign_settings.travel_account_id, things_to_do_center_account_id)
        self.assertTrue(hasattr(campaign_op_create, 'maximize_conversion_value')) # Check if the attribute was set
        self.assertEqual(campaign_op_create.network_settings.target_google_search, True)
        self.assertEqual(campaign_op_create.campaign_budget, "budget_resource_name_ttd")


        mock_ad_group_service.mutate_ad_groups.assert_called_once()
        ad_group_op_create = mock_ad_group_service.mutate_ad_groups.call_args[1]['operations'][0].create
        self.assertEqual(ad_group_op_create.type_, "TRAVEL_ADS")
        self.assertEqual(ad_group_op_create.campaign, "campaign_resource_name_ttd")

        mock_ad_group_ad_service.mutate_ad_group_ads.assert_called_once()
        ad_group_ad_op_create = mock_ad_group_ad_service.mutate_ad_group_ads.call_args[1]['operations'][0].create
        self.assertTrue(hasattr(ad_group_ad_op_create.ad, 'travel_ad')) # Check if the attribute was set
        self.assertEqual(ad_group_ad_op_create.ad_group, "ad_group_resource_name_ttd")


        # Check print statements
        expected_prints = [
            call("Added a budget with resource name: 'budget_resource_name_ttd'."),
            call("Added a Things to do campaign with resource name: 'campaign_resource_name_ttd'."),
            call("Added an ad group with resource name: 'ad_group_resource_name_ttd'."),
            call("Added an ad group ad with resource name: 'ad_group_ad_resource_name_ttd'."),
        ]
        mock_print.assert_has_calls(expected_prints, any_order=False)

if __name__ == "__main__":
    unittest.main()
