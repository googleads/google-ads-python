import unittest
from unittest.mock import patch, MagicMock, call

from examples.basic_operations import get_campaigns

class TestGetCampaigns(unittest.TestCase):

    @patch("examples.basic_operations.get_campaigns.argparse.ArgumentParser")
    @patch("examples.basic_operations.get_campaigns.GoogleAdsClient.load_from_storage")
    def test_main(self, mock_load_from_storage, mock_argument_parser):
        # Mock the GoogleAdsClient
        mock_google_ads_client = MagicMock()
        mock_load_from_storage.return_value = mock_google_ads_client

        # Mock the GoogleAdsService
        mock_ga_service = MagicMock()
        mock_google_ads_client.get_service.return_value = mock_ga_service

        # Mock command line arguments
        mock_args = MagicMock()
        mock_args.customer_id = "1234567890"
        mock_argument_parser.return_value.parse_args.return_value = mock_args

        # Mock the response from search_stream
        mock_row1 = MagicMock()
        mock_row1.campaign.id = "111"
        mock_row1.campaign.name = "Test Campaign 1"

        mock_row2 = MagicMock()
        mock_row2.campaign.id = "222"
        mock_row2.campaign.name = "Test Campaign 2"

        mock_batch1 = MagicMock()
        mock_batch1.results = [mock_row1, mock_row2]

        mock_stream_response = [mock_batch1]
        mock_ga_service.search_stream.return_value = mock_stream_response

        # Call the main function of the example script
        with patch("builtins.print") as mock_print:
            get_campaigns.main(mock_google_ads_client, mock_args.customer_id)

        # Assertions
        mock_load_from_storage.assert_called_once_with(version="v19")
        mock_google_ads_client.get_service.assert_called_once_with("GoogleAdsService")

        expected_query = """
        SELECT
          campaign.id,
          campaign.name
        FROM campaign
        ORDER BY campaign.id"""
        mock_ga_service.search_stream.assert_called_once_with(
            customer_id=mock_args.customer_id, query=expected_query
        )

        # Verify print output
        expected_print_calls = [
            call("Campaign with ID 111 and name "Test Campaign 1" was found."),
            call("Campaign with ID 222 and name "Test Campaign 2" was found.")
        ]
        mock_print.assert_has_calls(expected_print_calls, any_order=False)

if __name__ == "__main__":
    unittest.main()
