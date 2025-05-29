import unittest
from unittest import mock
import sys

# Adjust path to import the script under test.
# This assumes the test is run from the root of the repository.
# If examples/travel/ is not in PYTHONPATH, this might be an issue when running the test directly.
# However, for the purpose of this environment, direct import should work if the structure is as expected.
from examples.travel import add_hotel_ad
# The script uses argparse, so we might need it.
import argparse
import runpy # For running the script's __main__ block

class TestAddHotelAd(unittest.TestCase):

    def setUp(self):
        # Mock GoogleAdsClient instance
        # Use spec=True to ensure that the mock only allows attributes/methods that exist on the real class
        self.mock_google_ads_client = mock.Mock(spec=add_hotel_ad.GoogleAdsClient)

        # Mock services
        self.mock_campaign_budget_service = mock.Mock()
        self.mock_campaign_service = mock.Mock()
        self.mock_ad_group_service = mock.Mock()
        self.mock_ad_group_ad_service = mock.Mock()

        # Configure get_service on the client mock
        def get_service_side_effect(service_name, version=None): # Add version to match real signature if used
            if service_name == "CampaignBudgetService":
                return self.mock_campaign_budget_service
            elif service_name == "CampaignService":
                return self.mock_campaign_service
            elif service_name == "AdGroupService":
                return self.mock_ad_group_service
            elif service_name == "AdGroupAdService":
                return self.mock_ad_group_ad_service
            return mock.DEFAULT 
        self.mock_google_ads_client.get_service.side_effect = get_service_side_effect

        # Mock enums (values should match what the script expects)
        self.mock_google_ads_client.enums = mock.Mock()
        # Replicate enum structure more closely if needed, e.g. self.mock_google_ads_client.enums.BudgetDeliveryMethodEnum = mock.Mock()
        # Then self.mock_google_ads_client.enums.BudgetDeliveryMethodEnum.STANDARD = "STANDARD_ENUM_VALUE"
        # For simplicity, direct assignment if the script accesses them like client.enums.BudgetDeliveryMethodEnum.STANDARD
        self.mock_google_ads_client.enums.BudgetDeliveryMethodEnum = mock.Mock()
        self.mock_google_ads_client.enums.BudgetDeliveryMethodEnum.STANDARD = "STANDARD"
        
        self.mock_google_ads_client.enums.AdvertisingChannelTypeEnum = mock.Mock()
        self.mock_google_ads_client.enums.AdvertisingChannelTypeEnum.HOTEL = "HOTEL"
        
        self.mock_google_ads_client.enums.CampaignStatusEnum = mock.Mock()
        self.mock_google_ads_client.enums.CampaignStatusEnum.PAUSED = "PAUSED"
        
        self.mock_google_ads_client.enums.AdGroupStatusEnum = mock.Mock()
        self.mock_google_ads_client.enums.AdGroupStatusEnum.ENABLED = "ENABLED"
        
        self.mock_google_ads_client.enums.AdGroupTypeEnum = mock.Mock()
        self.mock_google_ads_client.enums.AdGroupTypeEnum.HOTEL_ADS = "HOTEL_ADS"
        
        self.mock_google_ads_client.enums.AdGroupAdStatusEnum = mock.Mock()
        self.mock_google_ads_client.enums.AdGroupAdStatusEnum.ENABLED = "ENABLED"

        self.mock_hotel_ad_info_type = mock.Mock(name="HotelAdInfoType")

        # Mock get_type to return mock operation objects
        def get_type_side_effect(type_name, version=None): # Add version to match real signature if used
            mock_operation_container = mock.Mock(name=f"{type_name}_OperationContainer")
            # The actual object to be populated is typically operation.create or operation.update
            # We make the .create attribute a separate mock to inspect it.
            created_object_mock = mock.Mock(name=f"{type_name}_Create")
            
            # If the type_name is for an entity that will be directly manipulated (e.g. campaign.hotel_setting)
            # we might need to pre-populate it if it's accessed before being set.
            # Example: campaign.hotel_setting.hotel_center_id = ...
            # So, campaign_operation.create.hotel_setting needs to be a mock that can have hotel_center_id set.
            if type_name == "CampaignOperation":
                created_object_mock.hotel_setting = mock.Mock()
                created_object_mock.percent_cpc = mock.Mock()
                created_object_mock.network_settings = mock.Mock()
            elif type_name == "AdGroupAdOperation":
                # ad_group_ad.ad.hotel_ad is used with copy_from
                created_object_mock.ad = mock.Mock()
                created_object_mock.ad.hotel_ad = mock.Mock(name="HotelAdOnAdGroupAd")

            mock_operation_container.create = created_object_mock
            
            if type_name == "HotelAdInfo": 
                return self.mock_hotel_ad_info_type 
            return mock_operation_container
        self.mock_google_ads_client.get_type.side_effect = get_type_side_effect
        
        self.mock_google_ads_client.copy_from = mock.Mock()

        self.expected_budget_resource_name = "customers/test_customer_id/campaignBudgets/budget123"
        self.expected_campaign_resource_name = "customers/test_customer_id/campaigns/campaign456"
        self.expected_ad_group_resource_name = "customers/test_customer_id/adGroups/adgroup789"
        self.expected_ad_group_ad_resource_name = "customers/test_customer_id/adGroupAds/adgroupad012"

        mock_budget_response = mock.Mock()
        mock_budget_response.results = [mock.Mock()]
        mock_budget_response.results[0].resource_name = self.expected_budget_resource_name
        self.mock_campaign_budget_service.mutate_campaign_budgets.return_value = mock_budget_response

        mock_campaign_response = mock.Mock()
        mock_campaign_response.results = [mock.Mock()]
        mock_campaign_response.results[0].resource_name = self.expected_campaign_resource_name
        self.mock_campaign_service.mutate_campaigns.return_value = mock_campaign_response

        mock_ad_group_response = mock.Mock()
        mock_ad_group_response.results = [mock.Mock()]
        mock_ad_group_response.results[0].resource_name = self.expected_ad_group_resource_name
        self.mock_ad_group_service.mutate_ad_groups.return_value = mock_ad_group_response
        
        mock_ad_group_ad_response = mock.Mock()
        mock_ad_group_ad_response.results = [mock.Mock()]
        mock_ad_group_ad_response.results[0].resource_name = self.expected_ad_group_ad_resource_name
        self.mock_ad_group_ad_service.mutate_ad_group_ads.return_value = mock_ad_group_ad_response


    @mock.patch('examples.travel.add_hotel_ad.main')
    @mock.patch('examples.travel.add_hotel_ad.GoogleAdsClient.load_from_storage')
    def test_google_ads_client_load(self, mock_load_from_storage, mock_main_function_in_script):
        """Tests that GoogleAdsClient.load_from_storage is called correctly
        and the loaded client is passed to the script's main function.
        """
        mock_google_ads_client_instance = mock.Mock()
        mock_load_from_storage.return_value = mock_google_ads_client_instance
        original_argv = sys.argv
        test_argv = [
            'add_hotel_ad.py',
            '--customer_id', 'test_customer_id_val',
            '--hotel_center_account_id', '12345',
            '--cpc_bid_ceiling_micro_amount', '1000000'
        ]
        sys.argv = test_argv
        try:
            runpy.run_module('examples.travel.add_hotel_ad', run_name='__main__', alter_sys=True)
        finally:
            sys.argv = original_argv
        mock_load_from_storage.assert_called_once_with(version="v19")
        mock_main_function_in_script.assert_called_once_with(
            mock_google_ads_client_instance,
            'test_customer_id_val',
            12345, 
            1000000
        )

    @mock.patch('examples.travel.add_hotel_ad.main') 
    @mock.patch('examples.travel.add_hotel_ad.GoogleAdsClient.load_from_storage')
    def test_argument_parsing(self, mock_load_from_storage, mock_main_function_in_script):
        """Tests that command-line arguments are parsed and passed to main correctly."""
        mock_google_ads_client_instance = mock.Mock()
        mock_load_from_storage.return_value = mock_google_ads_client_instance
        expected_customer_id = "test_customer_999"
        expected_hotel_id = 777
        expected_cpc_bid = 200000
        original_argv = sys.argv
        test_argv = [
            'add_hotel_ad.py',
            '--customer_id', expected_customer_id,
            '--hotel_center_account_id', str(expected_hotel_id),
            '--cpc_bid_ceiling_micro_amount', str(expected_cpc_bid)
        ]
        sys.argv = test_argv
        try:
            runpy.run_module('examples.travel.add_hotel_ad', run_name='__main__', alter_sys=True)
        finally:
            sys.argv = original_argv
        mock_load_from_storage.assert_called_once_with(version="v19")
        mock_main_function_in_script.assert_called_once_with(
            mock_google_ads_client_instance,
            expected_customer_id,
            expected_hotel_id,
            expected_cpc_bid
        )

    @mock.patch('builtins.print')
    def test_main_function_logic_and_api_calls(self, mock_print):
        customer_id = "test_customer_id"
        hotel_center_account_id = 98765
        cpc_bid_ceiling_micro_amount = 2000000

        add_hotel_ad.main(
            self.mock_google_ads_client,
            customer_id,
            hotel_center_account_id,
            cpc_bid_ceiling_micro_amount
        )

        expected_get_service_calls = [
            mock.call("CampaignBudgetService"),
            mock.call("CampaignService"),
            mock.call("AdGroupService"),
            mock.call("AdGroupAdService"),
        ]
        self.assertEqual(self.mock_google_ads_client.get_service.call_args_list, expected_get_service_calls)

        self.mock_campaign_budget_service.mutate_campaign_budgets.assert_called_once()
        args, kwargs = self.mock_campaign_budget_service.mutate_campaign_budgets.call_args
        self.assertEqual(kwargs['customer_id'], customer_id)
        budget_operation = kwargs['operations'][0]
        self.assertTrue(hasattr(budget_operation.create, 'name'))
        self.assertEqual(budget_operation.create.delivery_method, self.mock_google_ads_client.enums.BudgetDeliveryMethodEnum.STANDARD)
        self.assertEqual(budget_operation.create.amount_micros, 500000)
        
        self.mock_campaign_service.mutate_campaigns.assert_called_once()
        args, kwargs = self.mock_campaign_service.mutate_campaigns.call_args
        self.assertEqual(kwargs['customer_id'], customer_id)
        campaign_operation = kwargs['operations'][0]
        self.assertTrue(hasattr(campaign_operation.create, 'name'))
        self.assertEqual(campaign_operation.create.advertising_channel_type, self.mock_google_ads_client.enums.AdvertisingChannelTypeEnum.HOTEL)
        self.assertEqual(campaign_operation.create.hotel_setting.hotel_center_id, hotel_center_account_id)
        self.assertEqual(campaign_operation.create.status, self.mock_google_ads_client.enums.CampaignStatusEnum.PAUSED)
        self.assertEqual(campaign_operation.create.percent_cpc.cpc_bid_ceiling_micros, cpc_bid_ceiling_micro_amount)
        self.assertEqual(campaign_operation.create.campaign_budget, self.expected_budget_resource_name)
        self.assertTrue(campaign_operation.create.network_settings.target_google_search)

        self.mock_ad_group_service.mutate_ad_groups.assert_called_once()
        args, kwargs = self.mock_ad_group_service.mutate_ad_groups.call_args
        self.assertEqual(kwargs['customer_id'], customer_id)
        ad_group_operation = kwargs['operations'][0]
        self.assertTrue(hasattr(ad_group_operation.create, 'name'))
        self.assertEqual(ad_group_operation.create.status, self.mock_google_ads_client.enums.AdGroupStatusEnum.ENABLED)
        self.assertEqual(ad_group_operation.create.campaign, self.expected_campaign_resource_name)
        self.assertEqual(ad_group_operation.create.type_, self.mock_google_ads_client.enums.AdGroupTypeEnum.HOTEL_ADS)
        self.assertEqual(ad_group_operation.create.cpc_bid_micros, 10000000)

        self.mock_ad_group_ad_service.mutate_ad_group_ads.assert_called_once()
        args, kwargs = self.mock_ad_group_ad_service.mutate_ad_group_ads.call_args
        self.assertEqual(kwargs['customer_id'], customer_id)
        ad_group_ad_operation = kwargs['operations'][0]
        self.assertEqual(ad_group_ad_operation.create.ad_group, self.expected_ad_group_resource_name)
        self.assertEqual(ad_group_ad_operation.create.status, self.mock_google_ads_client.enums.AdGroupAdStatusEnum.ENABLED)
        
        # Check that the 'create' object's ad.hotel_ad attribute was passed to copy_from
        self.mock_google_ads_client.copy_from.assert_called_once_with(
            ad_group_ad_operation.create.ad.hotel_ad, 
            self.mock_hotel_ad_info_type 
        )

        expected_print_calls = [
            mock.call(f"Created budget with resource name '{self.expected_budget_resource_name}'."),
            mock.call(f"Added a hotel campaign with resource name '{self.expected_campaign_resource_name}'."),
            mock.call(f"Added a hotel ad group with resource name '{self.expected_ad_group_resource_name}'."),
            mock.call(f"Created hotel ad with resource name '{self.expected_ad_group_ad_resource_name}'."),
        ]
        self.assertEqual(mock_print.call_args_list, expected_print_calls)


if __name__ == "__main__":
    unittest.main()
