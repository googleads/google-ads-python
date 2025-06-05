import unittest
from unittest import mock

# Import the main function from the script to be tested
from examples.advanced_operations.add_bidding_data_exclusion import main


class TestAddBiddingDataExclusion(unittest.TestCase):
    """Test case for add_bidding_data_exclusion.py"""

    @mock.patch("examples.advanced_operations.add_bidding_data_exclusion.argparse.ArgumentParser")
    @mock.patch("google.ads.googleads.client.GoogleAdsClient")
    def test_main_function(self, mock_google_ads_client, mock_argparse):
        """Tests that the main function runs without errors."""
        # Mock the GoogleAdsClient.load_from_storage method
        mock_google_ads_client.load_from_storage.return_value = mock.MagicMock()

        # Mock the ArgumentParser.parse_args method
        mock_args = mock.Mock()
        mock_args.customer_id = "1234567890"
        mock_args.start_date_time = "2023-10-01 00:00:00"  # Example start date
        mock_args.end_date_time = "2023-10-02 00:00:00"    # Example end date
        mock_argparse.return_value.parse_args.return_value = mock_args

        # Call the main function
        main(
            mock_google_ads_client,
            mock_args.customer_id,
            mock_args.start_date_time,
            mock_args.end_date_time,
        )


if __name__ == "__main__":
    unittest.main()
