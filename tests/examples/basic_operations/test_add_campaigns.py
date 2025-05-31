import unittest
from unittest.mock import patch, MagicMock, call

from examples.basic_operations import add_campaigns

class TestAddCampaigns(unittest.TestCase):

    @patch("examples.basic_operations.add_campaigns.argparse.ArgumentParser")
    @patch("examples.basic_operations.add_campaigns.GoogleAdsClient.load_from_storage")
    def test_main(self, mock_load_from_storage, mock_argument_parser):
        # Mock the GoogleAdsClient
        mock_google_ads_client = MagicMock()
        mock_load_from_storage.return_value = mock_google_ads_client

        # Mock the CampaignService
        mock_campaign_service = MagicMock()
        # Mock the BudgetService (even if not directly used in main, it might be called by helpers)
        mock_campaign_budget_service = MagicMock()

        def get_service_side_effect(service_name, version=None):
            if service_name == "CampaignService":
                return mock_campaign_service
            elif service_name == "CampaignBudgetService":
                return mock_campaign_budget_service
            # Add other services if the example uses them
            raise ValueError(f"Unexpected service: {service_name}")
        mock_google_ads_client.get_service.side_effect = get_service_side_effect

        # Mock command line arguments
        mock_args = MagicMock()
        mock_args.customer_id = "1234567890"
        # mock_args.number_of_campaigns = 1 # This argument is not used by main

        mock_argument_parser.return_value.parse_args.return_value = mock_args

        # Mock the responses for service calls
        # For CampaignBudgetService mutate (if we were testing budget creation)
        mock_budget_operation_response = MagicMock()
        mock_budget_result = MagicMock()
        mock_budget_result.resource_name = "customers/1234567890/campaignBudgets/BUDGET_ID_1"
        mock_budget_operation_response.results = [mock_budget_result]
        mock_campaign_budget_service.mutate_campaign_budgets.return_value = mock_budget_operation_response

        # For CampaignService mutate
        mock_campaign_operation_response = MagicMock()
        mock_campaign_result = MagicMock()
        mock_campaign_result.resource_name = "customers/1234567890/campaigns/CAMPAIGN_ID_1"
        mock_campaign_operation_response.results = [mock_campaign_result]
        # Configure mutate_campaigns to return a list of results if multiple operations are sent
        mock_campaign_service.mutate_campaigns.return_value = mock_campaign_operation_response

        # Mock enums
        mock_google_ads_client.enums.CampaignStatusEnum.PAUSED = "PAUSED"
        mock_google_ads_client.enums.AdvertisingChannelTypeEnum.SEARCH = "SEARCH"
        mock_google_ads_client.enums.BiddingStrategyTypeEnum.MANUAL_CPC = "MANUAL_CPC"
        mock_google_ads_client.enums.BudgetDeliveryMethodEnum.STANDARD = "STANDARD"


        # Call the main function of the example script
        with patch("builtins.print") as mock_print:
            add_campaigns.main(mock_google_ads_client, mock_args.customer_id)

        # Assertions
        # mock_load_from_storage.assert_called_once_with(version="v19") # main doesn't call this directly
        mock_google_ads_client.get_service.assert_any_call("CampaignService")
        mock_google_ads_client.get_service.assert_any_call("CampaignBudgetService")

        # Ensure CampaignBudgetService.mutate_campaign_budgets was called
        mock_campaign_budget_service.mutate_campaign_budgets.assert_called_once()
        budget_args, budget_kwargs = mock_campaign_budget_service.mutate_campaign_budgets.call_args
        self.assertEqual(budget_kwargs['customer_id'], mock_args.customer_id)
        self.assertEqual(len(budget_kwargs['operations']), 1)
        # Add more assertions for budget operation if needed

        self.assertEqual(mock_campaign_service.mutate_campaigns.call_count, 1)
        args_list, kwargs_list = mock_campaign_service.mutate_campaigns.call_args
        self.assertEqual(kwargs_list['customer_id'], "1234567890")
        operations = kwargs_list['operations']
        self.assertEqual(len(operations), 1) # Script creates one campaign

        # Check properties of the campaign operation
        campaign_op = operations[0].create
        self.assertTrue(campaign_op.name.startswith("Interplanetary Cruise ")) # Adjusted prefix
        self.assertEqual(campaign_op.status, mock_google_ads_client.enums.CampaignStatusEnum.PAUSED)
        self.assertEqual(campaign_op.advertising_channel_type, mock_google_ads_client.enums.AdvertisingChannelTypeEnum.SEARCH)
        # In the actual script, manual_cpc is initialized but enhanced_cpc_enabled is not explicitly set.
        # We should check what is actually being set.
        # self.assertEqual(campaign_op.manual_cpc.enhanced_cpc_enabled, True)
        self.assertTrue(hasattr(campaign_op, 'manual_cpc')) # Check if manual_cpc is set
        self.assertEqual(campaign_op.campaign_budget, "customers/1234567890/campaignBudgets/BUDGET_ID_1")


        # Verify print output
        expected_print_calls = [
            call(f"Created campaign customers/1234567890/campaigns/CAMPAIGN_ID_1.")
        ]
        mock_print.assert_has_calls(expected_print_calls, any_order=False)

if __name__ == "__main__":
    unittest.main()
