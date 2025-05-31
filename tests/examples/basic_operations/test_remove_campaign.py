import unittest
from unittest.mock import patch, MagicMock, call

from examples.basic_operations import remove_campaign

class TestRemoveCampaign(unittest.TestCase):

    @patch("examples.basic_operations.remove_campaign.argparse.ArgumentParser")
    @patch("examples.basic_operations.remove_campaign.GoogleAdsClient.load_from_storage")
    def test_main(self, mock_load_from_storage, mock_argument_parser):
        # Mock the GoogleAdsClient
        mock_google_ads_client = MagicMock()
        mock_load_from_storage.return_value = mock_google_ads_client

        # Mock the CampaignService
        mock_campaign_service = MagicMock()
        mock_google_ads_client.get_service.return_value = mock_campaign_service

        # Mock client.get_type for CampaignOperation
        mock_campaign_operation_type = MagicMock()
        mock_google_ads_client.get_type.return_value = mock_campaign_operation_type

        # Mock command line arguments
        mock_args = MagicMock()
        mock_args.customer_id = "1234567890"
        mock_args.campaign_id = "CAMPAIGNID1"
        mock_argument_parser.return_value.parse_args.return_value = mock_args

        # Mock the response for CampaignService.mutate_campaigns
        mock_mutate_response = MagicMock()
        mock_mutate_result = MagicMock()
        # The resource name in the response for a remove operation is the campaign's resource name itself
        campaign_resource_name = f"customers/{mock_args.customer_id}/campaigns/{mock_args.campaign_id}"
        mock_mutate_result.resource_name = campaign_resource_name
        mock_mutate_response.results = [mock_mutate_result]
        mock_campaign_service.mutate_campaigns.return_value = mock_mutate_response

        # Call the main function of the example script
        with patch("builtins.print") as mock_print:
            remove_campaign.main(mock_google_ads_client, mock_args.customer_id, mock_args.campaign_id)

        # Assertions
        mock_load_from_storage.assert_called_once_with(version="v19")
        mock_google_ads_client.get_service.assert_called_once_with("CampaignService")
        mock_google_ads_client.get_type.assert_called_once_with("CampaignOperation")

        # Check CampaignService.mutate_campaigns call
        self.assertEqual(mock_campaign_service.mutate_campaigns.call_count, 1)
        args_mutate, kwargs_mutate = mock_campaign_service.mutate_campaigns.call_args

        self.assertEqual(kwargs_mutate['customer_id'], mock_args.customer_id)

        operation = kwargs_mutate['operations'][0]
        # For a remove operation, the 'remove' field of the operation should be the resource name
        self.assertEqual(operation.remove, campaign_resource_name)

        # Verify print output
        expected_print_call = call(
            f"Removed campaign with resource name '{campaign_resource_name}'."
        )
        mock_print.assert_has_calls([expected_print_call])

if __name__ == "__main__":
    unittest.main()
