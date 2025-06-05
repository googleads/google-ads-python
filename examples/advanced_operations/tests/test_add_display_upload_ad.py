import unittest
from unittest import mock

# Import the main function from the script to be tested
from examples.advanced_operations.add_display_upload_ad import main


class TestAddDisplayUploadAd(unittest.TestCase):
    """Test case for add_display_upload_ad.py"""

    @mock.patch("examples.advanced_operations.add_display_upload_ad.requests.get")
    @mock.patch("examples.advanced_operations.add_display_upload_ad.argparse.ArgumentParser")
    @mock.patch("google.ads.googleads.client.GoogleAdsClient")
    def test_main_function(self, mock_google_ads_client, mock_argparse, mock_requests_get):
        """Tests that the main function runs without errors."""
        # Mock the requests.get call
        mock_response = mock.MagicMock()
        mock_response.content = b"dummy_bundle_content"
        mock_requests_get.return_value = mock_response

        # Mock the GoogleAdsClient.load_from_storage method
        mock_google_ads_client.load_from_storage.return_value = mock.MagicMock()

        # Mock the ArgumentParser.parse_args method
        mock_args = mock.Mock()
        mock_args.customer_id = "1234567890"
        mock_args.ad_group_id = "111222333"  # Example Ad Group ID as string
        mock_argparse.return_value.parse_args.return_value = mock_args

        # Call the main function
        main(
            mock_google_ads_client,
            mock_args.customer_id,
            mock_args.ad_group_id,
        )

        # Verify that requests.get was called (optional, but good practice)
        mock_requests_get.assert_called_once()


if __name__ == "__main__":
    unittest.main()
