import unittest
from unittest import mock

from google.ads.googleads.client import GoogleAdsClient
import argparse

# Import the main function from the script to be tested
from examples.advanced_operations.add_ad_customizer import main


class TestAddAdCustomizer(unittest.TestCase):
    """Test case for add_ad_customizer.py"""

    @mock.patch("examples.advanced_operations.add_ad_customizer.argparse.ArgumentParser")
    @mock.patch("google.ads.googleads.client.GoogleAdsClient")
    def test_main_function(self, mock_google_ads_client, mock_argparse):
        """Tests that the main function runs without errors."""
        # Mock the GoogleAdsClient.load_from_storage method
        mock_google_ads_client.load_from_storage.return_value = mock.MagicMock()

        # Mock the ArgumentParser.parse_args method
        mock_args = mock.Mock()
        mock_args.customer_id = "1234567890"
        mock_args.ad_group_id = "111111"  # Use a single ad_group_id
        # The customizer_attribute_name is not directly passed to main
        mock_argparse.return_value.parse_args.return_value = mock_args

        # Call the main function
        main(
            mock_google_ads_client,
            mock_args.customer_id,
            mock_args.ad_group_id,  # Pass the single ad_group_id
        )

        # The load_from_storage method is not called directly on the mock
        # when the client is passed as an argument to main.
        # So, this assertion is removed.
        # mock_google_ads_client.load_from_storage.assert_called_once()


if __name__ == "__main__":
    unittest.main()
