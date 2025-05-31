import unittest
from unittest.mock import patch, MagicMock, call

from examples.basic_operations import update_campaign

class TestUpdateCampaign(unittest.TestCase):

    @patch("examples.basic_operations.update_campaign.argparse.ArgumentParser")
    @patch("examples.basic_operations.update_campaign.GoogleAdsClient.load_from_storage")
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
        mock_args.campaign_id = "CAMPAIGNID1"
        mock_argument_parser.return_value.parse_args.return_value = mock_args

        campaign_resource_name = f"customers/{mock_args.customer_id}/campaigns/{mock_args.campaign_id}"

        # Mock the response for CampaignService.mutate_campaigns
        mock_mutate_response = MagicMock()
        mock_mutate_result = MagicMock()
        mock_mutate_result.resource_name = campaign_resource_name
        mock_mutate_response.results = [mock_mutate_result]
        mock_campaign_service.mutate_campaigns.return_value = mock_mutate_response

        # Call the main function of the example script
        with patch("builtins.print") as mock_print,              patch("google.ads.googleads.client.GoogleAdsClient.get_type") as mock_get_type_on_instance,              patch("google.protobuf.field_mask_pb2.FieldMask") as mock_field_mask:

            # Mocking get_type on the instance of the client used in main
            mock_campaign_type_instance = MagicMock()
            mock_campaign_type_instance.resource_name = campaign_resource_name
            # Set initial status to something different than what it will be updated to
            mock_campaign_type_instance.status = mock_google_ads_client.enums.CampaignStatusEnum.ENABLED

            def get_type_instance_side_effect(type_name):
                if type_name == "Campaign":
                    return mock_campaign_type_instance
                elif type_name == "CampaignOperation":
                    return MagicMock()
                raise ValueError(f"Unexpected type for instance: {type_name}")
            mock_get_type_on_instance.side_effect = get_type_instance_side_effect

            update_campaign.main(mock_google_ads_client, mock_args.customer_id, mock_args.campaign_id)

        # Assertions
        mock_load_from_storage.assert_called_once_with(version="v19")
        mock_google_ads_client.get_service.assert_called_once_with("CampaignService")

        mock_get_type_on_instance.assert_any_call("CampaignOperation")
        mock_get_type_on_instance.assert_any_call("Campaign")

        self.assertEqual(mock_campaign_service.mutate_campaigns.call_count, 1)
        args_mutate, kwargs_mutate = mock_campaign_service.mutate_campaigns.call_args

        self.assertEqual(kwargs_mutate['customer_id'], mock_args.customer_id)

        operation = kwargs_mutate['operations'][0]
        # Check the update field of the operation
        self.assertEqual(operation.update.resource_name, campaign_resource_name)
        self.assertEqual(operation.update.status, mock_google_ads_client.enums.CampaignStatusEnum.PAUSED)

        # Check that FieldMask was called correctly
        mock_field_mask.assert_called_once_with(paths=['status'])
        self.assertEqual(operation.update_mask, mock_field_mask.return_value)

        # Verify print output
        expected_print_call = call(
            f"Campaign with resource name '{campaign_resource_name}' was updated."
        )
        mock_print.assert_has_calls([expected_print_call])

if __name__ == "__main__":
    unittest.main()
