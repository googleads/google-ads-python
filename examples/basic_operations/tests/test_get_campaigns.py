import unittest
from unittest.mock import patch, MagicMock, call # Added call for multiple print checks
import sys
from io import StringIO

# Attempt to import the main function from the script to be tested
try:
    from examples.basic_operations.get_campaigns import main as get_campaigns_main
except ImportError:
    get_campaigns_main = None

class TestGetCampaigns(unittest.TestCase):
    # Patch GoogleAdsClient.load_from_storage, as that's standard
    @patch("examples.basic_operations.get_campaigns.GoogleAdsClient.load_from_storage")
    def test_get_campaigns_mocked_service(self, mock_load_from_storage):
        if not get_campaigns_main:
            self.skipTest("get_campaigns.py main function not found or import failed.")

        # --- Setup Mocks ---
        mock_client = MagicMock()
        mock_load_from_storage.return_value = mock_client

        # Mock GoogleAdsService
        mock_google_ads_service = mock_client.get_service("GoogleAdsService", version="v19")

        # Mock the search_stream response
        # Create mock GoogleAdsRow objects that the search_stream will effectively yield
        mock_campaign_row_1 = MagicMock()
        # The script only uses campaign.id and campaign.name from the row
        mock_campaign_row_1.campaign.id = 101
        mock_campaign_row_1.campaign.name = "Test Campaign 1"
        # resource_name is not strictly needed for test pass criteria as it's not in query/output
        # mock_campaign_row_1.campaign.resource_name = "customers/1234567890/campaigns/101"


        mock_campaign_row_2 = MagicMock()
        mock_campaign_row_2.campaign.id = 102
        mock_campaign_row_2.campaign.name = "Test Campaign 2"
        # mock_campaign_row_2.campaign.resource_name = "customers/1234567890/campaigns/102"

        # Create mock SearchGoogleAdsStreamResponse objects (these are the "batch" objects)
        mock_batch_1 = MagicMock()
        mock_batch_1.results = [mock_campaign_row_1] # Each batch.results is a list of rows

        mock_batch_2 = MagicMock()
        mock_batch_2.results = [mock_campaign_row_2]

        # search_stream returns an iterator of these mock_batch objects
        mock_google_ads_service.search_stream.return_value = iter([mock_batch_1, mock_batch_2])

        customer_id = "1234567890"

        # --- Capture stdout ---
        old_stdout = sys.stdout
        sys.stdout = captured_output = StringIO()

        # --- Call the main function ---
        # Assuming main takes client and customer_id. May need adjustment for 'limit'.
        # This will depend on get_campaigns.py's main() and argparse setup.
        try:
            # If limit is an argument, it should be passed.
            # For now, assuming it's either not there or handled by argparse if main is called directly.
            get_campaigns_main(mock_client, customer_id)
        except Exception as e:
            self.fail(f"Running get_campaigns_main failed: {e}")


        # --- Restore stdout ---
        sys.stdout = old_stdout
        output = captured_output.getvalue() # Don't strip() yet if checking multiple lines

        # --- Assertions ---

        # 1. Assert search_stream was called correctly
        # Query from get_campaigns.py:
        expected_query = """
        SELECT
          campaign.id,
          campaign.name
        FROM campaign
        ORDER BY campaign.id"""

        mock_google_ads_service.search_stream.assert_called_once_with(
            customer_id=customer_id,
            query=expected_query
        )

        # 2. Assert the script output
        # This depends on the print format in get_campaigns.py
        expected_output_1 = f"Campaign with ID {mock_campaign_row_1.campaign.id} and name \"{mock_campaign_row_1.campaign.name}\" was found."
        expected_output_2 = f"Campaign with ID {mock_campaign_row_2.campaign.id} and name \"{mock_campaign_row_2.campaign.name}\" was found."

        self.assertIn(expected_output_1, output)
        self.assertIn(expected_output_2, output)
        # For more precise checking of multiple print calls in order:
        # with patch('builtins.print') as mock_print:
        #     get_campaigns_main(mock_client, customer_id)
        #     calls = [call(expected_output_1), call(expected_output_2)]
        #     mock_print.assert_has_calls(calls, any_order=False) # any_order=False if order matters

if __name__ == "__main__":
    unittest.main()
