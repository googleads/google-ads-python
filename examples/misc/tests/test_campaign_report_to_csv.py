import unittest
from unittest.mock import patch, MagicMock, call
import csv
import os
import sys
from datetime import datetime

# Adjust sys.path to allow import of the script under test
_PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from examples.misc import campaign_report_to_csv

# Define a fixed output directory for tests to manage created files
# Assuming os.path.join behavior: os.path.join("anything", "/absolute/path") returns "/absolute/path"
# If _TEST_CSV_FILEPATH is absolute, the script should use it directly.
_TEST_OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "test_output")
_TEST_CSV_FILENAME = "test_campaign_report.csv"
_TEST_CSV_FILEPATH = os.path.abspath(os.path.join(_TEST_OUTPUT_DIR, _TEST_CSV_FILENAME))


class TestCampaignReportToCsv(unittest.TestCase):

    def setUp(self):
        if not os.path.exists(_TEST_OUTPUT_DIR):
            os.makedirs(_TEST_OUTPUT_DIR)
        if os.path.exists(_TEST_CSV_FILEPATH):
            os.remove(_TEST_CSV_FILEPATH)

    def tearDown(self):
        if os.path.exists(_TEST_CSV_FILEPATH):
            os.remove(_TEST_CSV_FILEPATH)
        if os.path.exists(_TEST_OUTPUT_DIR) and not os.listdir(_TEST_OUTPUT_DIR):
            os.rmdir(_TEST_OUTPUT_DIR)

    def _create_mock_google_ads_row(self, descriptive_name, date, campaign_name, impressions, clicks, cost_micros):
        """Helper to create a MagicMock object that mimics a GoogleAdsRow based on script's output."""
        row = MagicMock()
        row.customer.descriptive_name = descriptive_name
        row.segments.date = date
        row.campaign.name = campaign_name
        row.metrics.impressions = impressions
        row.metrics.clicks = clicks
        row.metrics.cost_micros = cost_micros
        return row

    @patch('examples.misc.campaign_report_to_csv.GoogleAdsClient.load_from_storage')
    def test_report_generation_with_headers(self, mock_load_from_storage):
        mock_ads_client = MagicMock()
        mock_load_from_storage.return_value = mock_ads_client
        mock_ga_service = mock_ads_client.get_service.return_value

        # Sample data matching script's output fields
        mock_rows_data = [
            ("Test Account 1", "2023-10-26", "Campaign Alpha", 1000, 150, 5000000),
            ("Test Account 1", "2023-10-26", "Campaign Beta", 2500, 300, 12000000),
        ]
        # search_stream returns an iterable of batches, each batch has 'results'
        mock_search_stream_response = [MagicMock(results=[self._create_mock_google_ads_row(*data) for data in mock_rows_data])]
        mock_ga_service.search_stream.return_value = mock_search_stream_response
        
        customer_id = "1234567890"
        
        campaign_report_to_csv.main(
            mock_ads_client, customer_id, output_file=_TEST_CSV_FILEPATH, write_headers=True
        )

        self.assertTrue(os.path.exists(_TEST_CSV_FILEPATH))

        # Script's actual headers
        expected_headers = ["Account", "Date", "Campaign", "Impressions", "Clicks", "Cost"]
        with open(_TEST_CSV_FILEPATH, mode='r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            headers = next(reader)
            self.assertEqual(headers, expected_headers)
            
            content = list(reader)
            self.assertEqual(len(content), len(mock_rows_data))
            for i, row_data in enumerate(mock_rows_data):
                self.assertEqual(content[i][0], str(row_data[0])) # Account
                self.assertEqual(content[i][1], str(row_data[1])) # Date
                self.assertEqual(content[i][2], str(row_data[2])) # Campaign
                self.assertEqual(content[i][3], str(row_data[3])) # Impressions
                self.assertEqual(content[i][4], str(row_data[4])) # Clicks
                self.assertEqual(content[i][5], str(row_data[5])) # Cost
        
        mock_ga_service.search_stream.assert_called_once()
        # Verify the search_request object passed to search_stream
        args, _ = mock_ga_service.search_stream.call_args
        search_request = args[0]
        self.assertEqual(search_request.customer_id, customer_id)
        self.assertIn("FROM campaign", search_request.query)


    @patch('examples.misc.campaign_report_to_csv.GoogleAdsClient.load_from_storage')
    def test_report_generation_without_headers(self, mock_load_from_storage):
        mock_ads_client = MagicMock()
        mock_load_from_storage.return_value = mock_ads_client
        mock_ga_service = mock_ads_client.get_service.return_value

        mock_rows_data = [
            ("Test Account 2", "2023-10-27", "Campaign Gamma", 500, 50, 2000000),
        ]
        mock_search_stream_response = [MagicMock(results=[self._create_mock_google_ads_row(*data) for data in mock_rows_data])]
        mock_ga_service.search_stream.return_value = mock_search_stream_response
        customer_id = "9876543210"

        campaign_report_to_csv.main(
            mock_ads_client, customer_id, output_file=_TEST_CSV_FILEPATH, write_headers=False
        )

        self.assertTrue(os.path.exists(_TEST_CSV_FILEPATH))

        with open(_TEST_CSV_FILEPATH, mode='r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            content = list(reader)
            self.assertEqual(len(content), len(mock_rows_data))
            for i, row_data in enumerate(mock_rows_data):
                self.assertEqual(content[i][0], str(row_data[0])) # Account
                self.assertEqual(content[i][1], str(row_data[1])) # Date
                self.assertEqual(content[i][2], str(row_data[2])) # Campaign
                self.assertEqual(content[i][3], str(row_data[3])) # Impressions
                self.assertEqual(content[i][4], str(row_data[4])) # Clicks
                self.assertEqual(content[i][5], str(row_data[5])) # Cost
        
        mock_ga_service.search_stream.assert_called_once()
        args, _ = mock_ga_service.search_stream.call_args
        search_request = args[0]
        self.assertEqual(search_request.customer_id, customer_id)

if __name__ == "__main__":
    unittest.main()
