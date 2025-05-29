import unittest
from unittest import mock
import sys
import runpy
import argparse

# Script under test
from examples.travel import add_things_to_do_ad
# For patching helpers
from examples.utils import example_helpers

MOCK_DATETIME_STR = "YYYY-MM-DDTHHMMSS"

@mock.patch.object(example_helpers, 'get_printable_datetime', return_value=MOCK_DATETIME_STR)
class TestAddThingsToDoAd(unittest.TestCase):

    def setUp(self): # mock_get_datetime is no longer passed here if class-decorated
        self.mock_google_ads_client = mock.Mock(spec=add_things_to_do_ad.GoogleAdsClient)

        # Mock Services
        self.mock_budget_service = mock.Mock()
        self.mock_campaign_service = mock.Mock()
        self.mock_ad_group_service = mock.Mock()
        self.mock_ad_group_ad_service = mock.Mock()

        def get_service_side_effect(service_name, version=None):
            if service_name == "CampaignBudgetService":
                return self.mock_budget_service
            elif service_name == "CampaignService":
                return self.mock_campaign_service
            elif service_name == "AdGroupService":
                return self.mock_ad_group_service
            elif service_name == "AdGroupAdService":
                return self.mock_ad_group_ad_service
            return mock.DEFAULT
        self.mock_google_ads_client.get_service.side_effect = get_service_side_effect

        # Mock GetType for operations and other types
        # The script uses client.get_type("...") and then assigns to .create or directly
        def get_type_side_effect(type_name, version=None):
            mock_obj = mock.Mock(name=type_name)
            if type_name.endswith("Operation"): # Covers all X_Operation types
                # Ensure .create exists for operation.create = ... assignments
                mock_obj.create = mock.Mock(name=f"{type_name}_Create")
                if type_name == "CampaignOperation":
                    # Specific nested structure for campaign
                    mock_obj.create.travel_campaign_settings = mock.Mock(name="TravelCampaignSettings")
                    mock_obj.create.network_settings = mock.Mock(name="NetworkSettings")
                elif type_name == "AdGroupAdOperation":
                    # Specific nested structure for ad group ad
                    mock_obj.create.ad = mock.Mock(name="AdInfoContainer")
                    # The script sets ad_group_ad.ad.travel_ad, so ad needs travel_ad attribute
                    mock_obj.create.ad.travel_ad = mock.Mock(name="TravelAdInfo") 
            elif type_name == "MaximizeConversionValue":
                # This is assigned directly, not via .create
                pass # Simple mock is fine
            elif type_name == "TravelAdInfo":
                # This is assigned directly, not via .create
                pass # Simple mock is fine
            return mock_obj
        self.mock_google_ads_client.get_type.side_effect = get_type_side_effect
        
        # Mock Enums (provide specific values as needed by tests)
        self.mock_google_ads_client.enums.BudgetDeliveryMethodEnum.STANDARD = "STANDARD_BUDGET_DELIVERY"
        self.mock_google_ads_client.enums.AdvertisingChannelTypeEnum.TRAVEL = "TRAVEL_CHANNEL"
        self.mock_google_ads_client.enums.AdvertisingChannelSubTypeEnum.TRAVEL_ACTIVITIES = "TRAVEL_ACTIVITIES_SUBTYPE"
        self.mock_google_ads_client.enums.CampaignStatusEnum.PAUSED = "PAUSED_CAMPAIGN"
        self.mock_google_ads_client.enums.AdGroupTypeEnum.TRAVEL_ADS = "TRAVEL_ADS_ADGROUP_TYPE"
        self.mock_google_ads_client.enums.AdGroupStatusEnum.ENABLED = "ENABLED_ADGROUP"
        self.mock_google_ads_client.enums.AdGroupAdStatusEnum.ENABLED = "ENABLED_ADGROUP_AD"

        # Mock Mutate Responses (default for each service, can be overridden in tests)
        self.mock_budget_service.mutate_campaign_budgets.return_value = mock.Mock(results=[mock.Mock(resource_name="budgets/123")])
        self.mock_campaign_service.mutate_campaigns.return_value = mock.Mock(results=[mock.Mock(resource_name="campaigns/456")])
        self.mock_ad_group_service.mutate_ad_groups.return_value = mock.Mock(results=[mock.Mock(resource_name="adGroups/789")])
        self.mock_ad_group_ad_service.mutate_ad_group_ads.return_value = mock.Mock(results=[mock.Mock(resource_name="adGroupAds/012")])

    @mock.patch.object(example_helpers, 'get_printable_datetime', return_value=MOCK_DATETIME_STR)
    @mock.patch.object(add_things_to_do_ad, 'main') # Mock the script's main
    @mock.patch.object(add_things_to_do_ad, 'GoogleAdsClient') # Mock the client class
    def test_google_ads_client_load(self, mock_google_ads_client_class, mock_main_script_func, mock_datetime_ignored):
        mock_ads_client_instance = mock.Mock()
        mock_google_ads_client_class.load_from_storage.return_value = mock_ads_client_instance
        
        original_argv = sys.argv
        test_argv = [
            'add_things_to_do_ad.py',
            '--customer_id', 'cust123',
            '--things_to_do_center_account_id', 'ttd456'
        ]
        sys.argv = test_argv
        try:
            runpy.run_module('examples.travel.add_things_to_do_ad', run_name='__main__', alter_sys=True)
        finally:
            sys.argv = original_argv
            
        mock_google_ads_client_class.load_from_storage.assert_called_once_with(version="v19")
        mock_main_script_func.assert_called_once_with(
            mock_ads_client_instance,
            'cust123',
            'ttd456' # Argparse in script converts to int, but main is mocked here.
                     # If testing main's behavior, ensure type conversion.
        )

    # get_printable_datetime is now patched at class level
    @mock.patch.object(add_things_to_do_ad, 'main')
    @mock.patch.object(add_things_to_do_ad, 'GoogleAdsClient')
    def test_argument_parsing(self, mock_google_ads_client_class, mock_main_script_func): # Removed mock_datetime_ignored
        mock_ads_client_instance = mock.Mock()
        mock_google_ads_client_class.load_from_storage.return_value = mock_ads_client_instance

        expected_customer_id = "customer_test_789"
        expected_ttd_id = 98765

        original_argv = sys.argv
        test_argv = [
            'add_things_to_do_ad.py',
            '--customer_id', expected_customer_id,
            '--things_to_do_center_account_id', str(expected_ttd_id) 
        ]
        sys.argv = test_argv
        try:
            runpy.run_module('examples.travel.add_things_to_do_ad', run_name='__main__', alter_sys=True)
        finally:
            sys.argv = original_argv
        
        # The script's __main__ block calls main(client, args.customer_id, args.things_to_do_center_account_id)
        # where things_to_do_center_account_id is converted to int by argparse.
        mock_main_script_func.assert_called_once_with(
            mock_ads_client_instance,
            expected_customer_id,
            expected_ttd_id # Argparse in script converts this to int.
        )

    def test_add_campaign_budget(self): # Removed unused mock_get_datetime argument
        customer_id = "budget_cust_id"
        expected_resource_name = "budgets/test_budget_123"
        self.mock_budget_service.mutate_campaign_budgets.return_value = mock.Mock(
            results=[mock.Mock(resource_name=expected_resource_name)]
        )

        returned_name = add_things_to_do_ad.add_campaign_budget(
            self.mock_google_ads_client, customer_id
        )
        self.assertEqual(returned_name, expected_resource_name)

        self.mock_budget_service.mutate_campaign_budgets.assert_called_once()
        call_args = self.mock_budget_service.mutate_campaign_budgets.call_args
        self.assertEqual(call_args[1]['customer_id'], customer_id)
        
        operations = call_args[1]['operations']
        self.assertEqual(len(operations), 1)
        
        budget_create = operations[0].create
        self.assertEqual(budget_create.name, f"Interplanetary Cruise Budget #{MOCK_DATETIME_STR}")
        self.assertEqual(budget_create.delivery_method, self.mock_google_ads_client.enums.BudgetDeliveryMethodEnum.STANDARD)
        self.assertEqual(budget_create.amount_micros, 50000000)
        self.assertEqual(budget_create.explicitly_shared, True)

    def test_add_things_to_do_campaign(self):
        customer_id = "camp_cust_id"
        budget_resource_name = "budgets/test_budget_123"
        ttd_account_id = 98765
        expected_resource_name = "campaigns/test_campaign_456"

        self.mock_campaign_service.mutate_campaigns.return_value = mock.Mock(
            results=[mock.Mock(resource_name=expected_resource_name)]
        )
        
        # Mock the get_type for MaximizeConversionValue specifically for this test if needed,
        # but setUp already provides a generic mock for it.
        # mock_mcv_object = mock.Mock(name="MaximizeConversionValueObject")
        # self.mock_google_ads_client.get_type.side_effect = lambda type_name, version=None: \
        #     mock_mcv_object if type_name == "MaximizeConversionValue" else get_type_side_effect_orig(type_name, version)
        # This can get complex; relying on setUp's generic mock for get_type is fine.

        returned_name = add_things_to_do_ad.add_things_to_do_campaign(
            self.mock_google_ads_client, customer_id, budget_resource_name, ttd_account_id
        )
        self.assertEqual(returned_name, expected_resource_name)

        self.mock_campaign_service.mutate_campaigns.assert_called_once()
        call_args = self.mock_campaign_service.mutate_campaigns.call_args
        self.assertEqual(call_args[1]['customer_id'], customer_id)
        
        operations = call_args[1]['operations']
        self.assertEqual(len(operations), 1)
        
        campaign_create = operations[0].create
        self.assertEqual(campaign_create.name, f"Interplanetary Cruise Campaign #{MOCK_DATETIME_STR}")
        self.assertEqual(campaign_create.advertising_channel_type, self.mock_google_ads_client.enums.AdvertisingChannelTypeEnum.TRAVEL)
        self.assertEqual(campaign_create.advertising_channel_sub_type, self.mock_google_ads_client.enums.AdvertisingChannelSubTypeEnum.TRAVEL_ACTIVITIES)
        self.assertEqual(campaign_create.travel_campaign_settings.travel_account_id, ttd_account_id)
        self.assertEqual(campaign_create.status, self.mock_google_ads_client.enums.CampaignStatusEnum.PAUSED)
        
        # Check that maximize_conversion_value object was requested from get_type and set
        # The setUp ensures get_type("MaximizeConversionValue") returns a mock.
        # The script assigns this mock to campaign.maximize_conversion_value
        self.mock_google_ads_client.get_type.assert_any_call("MaximizeConversionValue")
        self.assertTrue(campaign_create.maximize_conversion_value is not None) 
        # If specific attributes were set on maximize_conversion_value, check them here. Script doesn't set any.

        self.assertEqual(campaign_create.campaign_budget, budget_resource_name)
        self.assertEqual(campaign_create.network_settings.target_google_search, True)

    def test_add_ad_group(self):
        customer_id = "adgroup_cust_id"
        campaign_resource_name = "campaigns/test_campaign_456"
        expected_resource_name = "adGroups/test_adgroup_789"

        self.mock_ad_group_service.mutate_ad_groups.return_value = mock.Mock(
            results=[mock.Mock(resource_name=expected_resource_name)]
        )

        returned_name = add_things_to_do_ad.add_ad_group(
            self.mock_google_ads_client, customer_id, campaign_resource_name
        )
        self.assertEqual(returned_name, expected_resource_name)

        self.mock_ad_group_service.mutate_ad_groups.assert_called_once()
        call_args = self.mock_ad_group_service.mutate_ad_groups.call_args
        self.assertEqual(call_args[1]['customer_id'], customer_id)
        
        operations = call_args[1]['operations']
        self.assertEqual(len(operations), 1)
        
        ad_group_create = operations[0].create
        self.assertEqual(ad_group_create.name, f"Earth to Mars cruise #{MOCK_DATETIME_STR}")
        self.assertEqual(ad_group_create.campaign, campaign_resource_name)
        self.assertEqual(ad_group_create.type_, self.mock_google_ads_client.enums.AdGroupTypeEnum.TRAVEL_ADS)
        self.assertEqual(ad_group_create.status, self.mock_google_ads_client.enums.AdGroupStatusEnum.ENABLED)

    @mock.patch('builtins.print') # To verify the print at the end of add_ad_group_ad
    def test_add_ad_group_ad(self, mock_print):
        customer_id = "adgroupad_cust_id"
        ad_group_resource_name = "adGroups/test_adgroup_789"
        expected_resource_name = "adGroupAds/test_ad_012"

        self.mock_ad_group_ad_service.mutate_ad_group_ads.return_value = mock.Mock(
            results=[mock.Mock(resource_name=expected_resource_name)]
        )
        
        # The setUp mock for get_type("AdGroupAdOperation").create.ad already has a .travel_ad mock
        # We need to ensure get_type("TravelAdInfo") is called by the script.
        mock_travel_ad_info_obj = self.mock_google_ads_client.get_type("TravelAdInfo")

        add_things_to_do_ad.add_ad_group_ad(
            self.mock_google_ads_client, customer_id, ad_group_resource_name
        ) # This function does not return a value

        self.mock_ad_group_ad_service.mutate_ad_group_ads.assert_called_once()
        call_args = self.mock_ad_group_ad_service.mutate_ad_group_ads.call_args
        self.assertEqual(call_args[1]['customer_id'], customer_id)
        
        operations = call_args[1]['operations']
        self.assertEqual(len(operations), 1)
        
        ad_group_ad_create = operations[0].create
        self.assertEqual(ad_group_ad_create.status, self.mock_google_ads_client.enums.AdGroupAdStatusEnum.ENABLED)
        self.assertEqual(ad_group_ad_create.ad_group, ad_group_resource_name)
        
        # Check that ad.travel_ad was set to the object from get_type("TravelAdInfo")
        self.mock_google_ads_client.get_type.assert_any_call("TravelAdInfo")
        self.assertEqual(ad_group_ad_create.ad.travel_ad, mock_travel_ad_info_obj)
        
        mock_print.assert_any_call(f"Added an ad group ad with resource name: '{expected_resource_name}'.")

    @mock.patch.object(add_things_to_do_ad, 'add_ad_group_ad')
    @mock.patch.object(add_things_to_do_ad, 'add_ad_group')
    @mock.patch.object(add_things_to_do_ad, 'add_things_to_do_campaign')
    @mock.patch.object(add_things_to_do_ad, 'add_campaign_budget')
    def test_main_orchestration(
        self, 
        mock_add_budget, 
        mock_add_campaign, 
        mock_add_ad_group, 
        mock_add_ad_group_ad
    ):
        customer_id = "main_cust_id"
        ttd_account_id = 123456789

        # Define return values for the mocked helper functions
        mock_budget_res_name = "budgets/main_budget"
        mock_campaign_res_name = "campaigns/main_campaign"
        mock_ad_group_res_name = "adGroups/main_ad_group"
        # add_ad_group_ad doesn't return anything

        mock_add_budget.return_value = mock_budget_res_name
        mock_add_campaign.return_value = mock_campaign_res_name
        mock_add_ad_group.return_value = mock_ad_group_res_name
        
        # Call the main function
        add_things_to_do_ad.main(
            self.mock_google_ads_client, customer_id, ttd_account_id
        )

        # Assert that each helper function was called once with the correct arguments
        mock_add_budget.assert_called_once_with(
            self.mock_google_ads_client, customer_id
        )
        mock_add_campaign.assert_called_once_with(
            self.mock_google_ads_client, customer_id, mock_budget_res_name, ttd_account_id
        )
        mock_add_ad_group.assert_called_once_with(
            self.mock_google_ads_client, customer_id, mock_campaign_res_name
        )
        mock_add_ad_group_ad.assert_called_once_with(
            self.mock_google_ads_client, customer_id, mock_ad_group_res_name
        )


if __name__ == '__main__':
    unittest.main()
