import unittest
from unittest import mock

# Import the main function from the script to be tested
from examples.advanced_operations.add_call_ad import main


class TestAddCallAd(unittest.TestCase):
    """Test case for add_call_ad.py"""

    @mock.patch("examples.advanced_operations.add_call_ad.argparse.ArgumentParser")
    @mock.patch("google.ads.googleads.client.GoogleAdsClient")
    def test_main_function(self, mock_google_ads_client, mock_argparse):
        """Tests that the main function runs without errors."""
        # Mock the GoogleAdsClient.load_from_storage method
        mock_google_ads_client.load_from_storage.return_value = mock.MagicMock()

        # Mock the ArgumentParser.parse_args method
        mock_args = mock.Mock()
        mock_args.customer_id = "1234567890"
        mock_args.ad_group_id = "111222333"
        mock_args.phone_number = "(800) 555-0100"
        mock_args.phone_country = "US"
        mock_args.conversion_action_id = "444555666"  # Can be None as well
        mock_argparse.return_value.parse_args.return_value = mock_args

        # Call the main function
        main(
            mock_google_ads_client,
            mock_args.customer_id,
            mock_args.ad_group_id,
            mock_args.phone_number,
            mock_args.phone_country,
            mock_args.conversion_action_id,
        )


if __name__ == "__main__":
    unittest.main()
