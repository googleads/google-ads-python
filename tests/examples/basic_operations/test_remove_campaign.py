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

        # Mock command line arguments
        mock_args = MagicMock()
        mock_args.customer_id = "1234567890"
        mock_args.campaign_id = "CAMPAIGN_ID_TO_REMOVE"
        mock_argument_parser.return_value.parse_args.return_value = mock_args

        # Mock the campaign_path method
        expected_campaign_resource_name = f"customers/{mock_args.customer_id}/campaigns/{mock_args.campaign_id}"
        mock_campaign_service.campaign_path.return_value = expected_campaign_resource_name

        # Mock the response from CampaignService.mutate_campaigns
        mock_mutate_response = MagicMock()
        mock_mutate_result = MagicMock()
        mock_mutate_result.resource_name = expected_campaign_resource_name
        mock_mutate_response.results = [mock_mutate_result]
        mock_campaign_service.mutate_campaigns.return_value = mock_mutate_response

        # Mock CampaignOperation
        # The script builds this operation using client.get_type
        mock_campaign_operation_instance = MagicMock()

        def get_type_side_effect(type_name, version=None):
            if type_name == "CampaignOperation":
                # Return the pre-configured mock for CampaignOperation
                return mock_campaign_operation_instance
            raise ValueError(f"Unexpected type: {type_name}")
        mock_google_ads_client.get_type.side_effect = get_type_side_effect


        # Call the main function of the example script
        with patch("builtins.print") as mock_print:
            remove_campaign.main(mock_google_ads_client, mock_args.customer_id, mock_args.campaign_id)

        # Assertions
        mock_google_ads_client.get_service.assert_called_once_with("CampaignService")
        mock_campaign_service.campaign_path.assert_called_once_with(mock_args.customer_id, mock_args.campaign_id)

        # Verify CampaignService.mutate_campaigns call
        mock_campaign_service.mutate_campaigns.assert_called_once()
        _, mutate_kwargs = mock_campaign_service.mutate_campaigns.call_args
        self.assertEqual(mutate_kwargs['customer_id'], mock_args.customer_id)

        operations = mutate_kwargs['operations']
        self.assertEqual(len(operations), 1)
        # Check that the 'remove' attribute of the operation was set to the resource name
        # The actual operation instance passed to mutate_campaigns is operations[0]
        # which should be our mock_campaign_operation_instance due to get_type mocking
        self.assertEqual(mock_campaign_operation_instance.remove, expected_campaign_resource_name)
        # Ensure the operation passed was indeed the one we mocked
        self.assertIs(operations[0], mock_campaign_operation_instance)


        # Verify print output
        expected_print_calls = [
            call(f"Removed campaign {expected_campaign_resource_name}.")
        ]
        mock_print.assert_has_calls(expected_print_calls, any_order=False)

if __name__ == "__main__":
    unittest.main()
