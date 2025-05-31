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
        mock_google_ads_client.get_service.return_value = mock_campaign_service

        # Mock command line arguments
        mock_args = MagicMock()
        mock_args.customer_id = "1234567890"
        mock_argument_parser.return_value.parse_args.return_value = mock_args

        # Mock the responses for service calls
        mock_campaign_operation_response = MagicMock()
        # Simulate that one campaign was created
        mock_campaign_result = MagicMock()
        mock_campaign_result.resource_name = "customers/1234567890/campaigns/CAMPAIGN_ID_1"
        mock_campaign_operation_response.results = [mock_campaign_result]
        mock_campaign_service.mutate_campaigns.return_value = mock_campaign_operation_response

        # Call the main function of the example script
        with patch("builtins.print") as mock_print:
            add_campaigns.main(mock_google_ads_client, mock_args.customer_id)

        # Assertions
        mock_load_from_storage.assert_called_once_with(version="v19")
        mock_google_ads_client.get_service.assert_called_once_with("CampaignService")

        self.assertEqual(mock_campaign_service.mutate_campaigns.call_count, 1)
        args, kwargs = mock_campaign_service.mutate_campaigns.call_args
        self.assertEqual(kwargs['customer_id'], "1234567890")
        operations = kwargs['operations']
        # The example creates 1 campaign, but the script has a loop for _NUMBER_OF_CAMPAIGNS (default 1)
        # For simplicity here, assuming _NUMBER_OF_CAMPAIGNS = 1 or that the test setup matches one operation.
        # If _NUMBER_OF_CAMPAIGNS was different, this would need adjustment or the constant mocked.
        self.assertEqual(len(operations), 1)

        # Check properties of the created campaign operation
        campaign_op = operations[0].create
        self.assertTrue(campaign_op.name.startswith("Interplanetary Cruise #"))
        self.assertEqual(campaign_op.advertising_channel_type, mock_google_ads_client.enums.AdvertisingChannelTypeEnum.SEARCH)
        self.assertEqual(campaign_op.status, mock_google_ads_client.enums.CampaignStatusEnum.PAUSED)
        self.assertEqual(campaign_op.manual_cpc.enhanced_cpc_enabled, True)
        self.assertEqual(campaign_op.campaign_budget, mock_campaign_service.client.get_type("CampaignBudgetOperation").create.name) # This needs careful mocking if budget is created separately
        self.assertEqual(campaign_op.network_settings.target_google_search, True)


        # Verify print output
        # Assuming one campaign result as mocked
        expected_print_calls = [
            call(f"Created campaign customers/1234567890/campaigns/CAMPAIGN_ID_1.")
        ]
        mock_print.assert_has_calls(expected_print_calls, any_order=False)

if __name__ == "__main__":
    unittest.main()
