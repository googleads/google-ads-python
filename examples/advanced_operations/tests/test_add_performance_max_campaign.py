import unittest
from unittest import mock

# Import the main function from the script to be tested
from examples.advanced_operations.add_performance_max_campaign import main


class TestAddPerformanceMaxCampaign(unittest.TestCase):
    """Test case for add_performance_max_campaign.py"""

    @mock.patch("examples.advanced_operations.add_performance_max_campaign.get_image_bytes_from_url")
    @mock.patch("examples.advanced_operations.add_performance_max_campaign.argparse.ArgumentParser")
    @mock.patch("google.ads.googleads.client.GoogleAdsClient")
    def test_main_function(self, mock_google_ads_client, mock_argparse, mock_get_image_bytes):
        """Tests that the main function runs without errors."""
        # Mock the get_image_bytes_from_url helper
        mock_get_image_bytes.return_value = b"dummy_image_bytes"

        # Mock the GoogleAdsClient.load_from_storage method
        mock_google_ads_client.load_from_storage.return_value = mock.MagicMock()

        # Mock the ArgumentParser.parse_args method
        mock_args = mock.Mock()
        mock_args.customer_id = "1234567890"
        mock_args.audience_id = None  # Or some mock ID "789012"
        mock_args.brand_guidelines_enabled = False
        mock_argparse.return_value.parse_args.return_value = mock_args

        # Call the main function
        main(
            mock_google_ads_client,
            mock_args.customer_id,
            mock_args.audience_id,
            mock_args.brand_guidelines_enabled,
        )

        # Verify that get_image_bytes_from_url was called for logos and images
        # The script calls it for:
        # 1. Business Logo (in create_and_link_brand_assets)
        # 2. Marketing Image (in create_and_link_image_asset)
        # 3. Square Marketing Image (in create_and_link_image_asset)
        self.assertEqual(mock_get_image_bytes.call_count, 3)


if __name__ == "__main__":
    unittest.main()
