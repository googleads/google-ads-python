import os
import unittest
from unittest import mock

# Assuming the script to test is in the parent directory
from examples.shopping_ads import add_listing_scope


class TestAddListingScope(unittest.TestCase):
    """Tests for add_listing_scope.py"""

    @mock.patch.dict(os.environ, {
        "GOOGLE_ADS_CONFIGURATION_FILE_PATH": "google-ads.yaml"
    })
    @mock.patch("examples.shopping_ads.add_listing_scope.GoogleAdsClient.load_from_storage")
    def test_main_runs_successfully(self, mock_load_from_storage):
        """
        Tests that the main function runs without raising an exception.
        Requires CUSTOMER_ID and CAMPAIGN_ID environment variables to be set.
        """
        customer_id = os.environ.get("CUSTOMER_ID")
        campaign_id = os.environ.get("CAMPAIGN_ID")

        if not customer_id or not campaign_id:
            self.skipTest(
                "CUSTOMER_ID or CAMPAIGN_ID environment variables not set. "
                "Skipping integration test."
            )

        # Mock the GoogleAdsClient and its services
        mock_google_ads_client = mock.MagicMock()
        mock_load_from_storage.return_value = mock_google_ads_client

        # Mock the services
        mock_campaign_service = mock.MagicMock()
        mock_google_ads_client.get_service.return_value = mock_campaign_service

        mock_campaign_criterion_service = mock.MagicMock()
        mock_google_ads_client.get_service.return_value = mock_campaign_criterion_service
        
        # Mock the campaign_path method
        mock_campaign_service.campaign_path.return_value = f"customers/{customer_id}/campaigns/{campaign_id}"

        # Mock the mutate_campaign_criteria response
        mock_campaign_criterion_response = mock.MagicMock()
        mock_campaign_criterion_service.mutate_campaign_criteria.return_value = mock_campaign_criterion_response
        mock_campaign_criterion_response.results = [mock.MagicMock()]


        # Call the main function
        try:
            add_listing_scope.main(
                mock_google_ads_client,
                customer_id,
                campaign_id
            )
        except Exception as e:
            self.fail(f"add_listing_scope.main() raised an exception: {e}")

        # Assert that the API calls were made as expected
        # mock_load_from_storage is not called directly by main() when client is passed in
        # mock_load_from_storage.assert_called_once() 
        mock_google_ads_client.get_service.assert_any_call("CampaignService")
        mock_google_ads_client.get_service.assert_any_call("CampaignCriterionService")
        
        mock_campaign_criterion_service.mutate_campaign_criteria.assert_called_once()
        # Add more assertions here based on the expected behavior of the script


if __name__ == "__main__":
    unittest.main()
