import unittest
from unittest import mock
import csv
import io # Use io.StringIO for mocking file operations in memory

# Assuming the script to be tested is in the parent directory.
# Adjust the import path as necessary.
from examples.misc import campaign_report_to_csv
from google.ads.googleads.errors import GoogleAdsException
from google.ads.googleads.v19.services.services.google_ads_service import GoogleAdsServiceClient
from google.ads.googleads.v19.services.types.google_ads_service import SearchGoogleAdsStreamResponse
from google.ads.googleads.v19.resources.types.campaign import Campaign
from google.ads.googleads.v19.resources.types.ad_group import AdGroup
from google.ads.googleads.v19.resources.types.metrics import Metrics
from google.ads.googleads.v19.resources.types.customer import Customer
from google.ads.googleads.v19.services.types.google_ads_service import GoogleAdsRow


class TestCampaignReportToCsv(unittest.TestCase):
    """Tests for the campaign_report_to_csv script."""

    @mock.patch("examples.misc.campaign_report_to_csv.GoogleAdsClient")
    def setUp(self, mock_google_ads_client):
        """Set up mock objects for testing."""
        self.mock_client = mock_google_ads_client.load_from_storage.return_value
        self.mock_google_ads_service = self.mock_client.get_service("GoogleAdsService")

    def _create_mock_row(self, campaign_id, campaign_name, ad_group_id, ad_group_name, impressions, clicks, cost_micros):
        """Helper method to create a mock GoogleAdsRow."""
        row = GoogleAdsRow()
        row.campaign.id = campaign_id
        row.campaign.name = campaign_name
        row.ad_group.id = ad_group_id
        row.ad_group.name = ad_group_name
        row.metrics.impressions = impressions
        row.metrics.clicks = clicks
        row.metrics.cost_micros = cost_micros
        # The customer object is not directly used in the current script's CSV output,
        # but it's part of the GoogleAdsRow structure.
        row.customer.id = 1234567890 # Example customer ID
        return row

    @mock.patch("builtins.open", new_callable=mock.mock_open)
    def test_main_success_with_headers(self, mock_open_file):
        """Test a successful run of main with header writing."""
        customer_id = "1234567890"
        output_filepath = "test_report.csv"
        write_headers = True

        mock_row_1 = self._create_mock_row(1, "Campaign 1", 101, "Ad Group 1-1", 1000, 100, 1000000)
        mock_row_2 = self._create_mock_row(2, "Campaign 2", 201, "Ad Group 2-1", 2000, 200, 2000000)
        mock_batch_1 = mock.Mock(spec=SearchGoogleAdsStreamResponse)
        mock_batch_1.results = [mock_row_1]
        mock_batch_2 = mock.Mock(spec=SearchGoogleAdsStreamResponse)
        mock_batch_2.results = [mock_row_2]

        self.mock_google_ads_service.search_stream.return_value = [mock_batch_1, mock_batch_2]

        campaign_report_to_csv.main(
            self.mock_client, customer_id, output_filepath, write_headers
        )

        self.mock_google_ads_service.search_stream.assert_called_once_with(
            customer_id=customer_id, query=campaign_report_to_csv.QUERY
        )

        # Check what was written to the file
        mock_open_file.assert_called_once_with(output_filepath, "w", newline="", encoding="utf-8")
        # Get all write calls made to the mock file handle
        written_content = "".join(call.args[0] for call in mock_open_file().write.call_args_list)

        # Verify CSV content
        expected_header = [
            "campaign_id", "campaign_name", "ad_group_id", "ad_group_name",
            "impressions", "clicks", "cost_micros"
        ]
        expected_row_1_data = ["1", "Campaign 1", "101", "Ad Group 1-1", "1000", "100", "1000000"]
        expected_row_2_data = ["2", "Campaign 2", "201", "Ad Group 2-1", "2000", "200", "2000000"]

        # Use io.StringIO to read the written content as a CSV
        csv_reader = csv.reader(io.StringIO(written_content))
        header = next(csv_reader)
        self.assertEqual(header, expected_header)
        row1 = next(csv_reader)
        self.assertEqual(row1, expected_row_1_data)
        row2 = next(csv_reader)
        self.assertEqual(row2, expected_row_2_data)


    @mock.patch("builtins.open", new_callable=mock.mock_open)
    def test_main_success_without_headers(self, mock_open_file):
        """Test a successful run of main without header writing."""
        customer_id = "1234567890"
        output_filepath = "test_report_no_headers.csv"
        write_headers = False # Test without headers

        mock_row_1 = self._create_mock_row(3, "Campaign 3", 301, "Ad Group 3-1", 300, 30, 300000)
        mock_batch_1 = mock.Mock(spec=SearchGoogleAdsStreamResponse)
        mock_batch_1.results = [mock_row_1]
        self.mock_google_ads_service.search_stream.return_value = [mock_batch_1]

        campaign_report_to_csv.main(
            self.mock_client, customer_id, output_filepath, write_headers
        )

        self.mock_google_ads_service.search_stream.assert_called_once_with(
            customer_id=customer_id, query=campaign_report_to_csv.QUERY
        )
        mock_open_file.assert_called_once_with(output_filepath, "w", newline="", encoding="utf-8")
        written_content = "".join(call.args[0] for call in mock_open_file().write.call_args_list)

        expected_row_1_data = ["3", "Campaign 3", "301", "Ad Group 3-1", "300", "30", "300000"]

        csv_reader = csv.reader(io.StringIO(written_content))
        # No header expected, so the first row should be data
        row1 = next(csv_reader)
        self.assertEqual(row1, expected_row_1_data)
        # Ensure no other rows (like a header) are present
        with self.assertRaises(StopIteration):
            next(csv_reader)


    def test_main_google_ads_exception(self):
        """Test handling of GoogleAdsException during search_stream."""
        customer_id = "1234567890"
        output_filepath = "test_error.csv"
        write_headers = True

        self.mock_google_ads_service.search_stream.side_effect = GoogleAdsException(
            None, None, None
        )

        with self.assertRaises(GoogleAdsException):
            campaign_report_to_csv.main(
                self.mock_client, customer_id, output_filepath, write_headers
            )

    @mock.patch("examples.misc.campaign_report_to_csv.argparse.ArgumentParser")
    @mock.patch("examples.misc.campaign_report_to_csv.GoogleAdsClient")
    def test_argument_parsing(self, mock_google_ads_client, mock_argument_parser):
        """Test that main is called with parsed arguments."""
        mock_args = mock.Mock()
        mock_args.customer_id = "test_customer_id_arg"
        mock_args.output_filepath = "parsed_output.csv"
        mock_args.no_headers = False # Corresponds to write_headers=True
        mock_argument_parser.return_value.parse_args.return_value = mock_args

        mock_google_ads_client.load_from_storage.return_value = self.mock_client

        import sys
        original_argv = sys.argv
        sys.argv = [
            "campaign_report_to_csv.py",
            "-c", mock_args.customer_id,
            "-f", mock_args.output_filepath
            # Not including --no-headers means write_headers should be True
        ]

        import runpy
        with mock.patch.object(campaign_report_to_csv, "main") as mock_script_main:
            runpy.run_module("examples.misc.campaign_report_to_csv", run_name="__main__")

        mock_script_main.assert_called_once_with(
            self.mock_client,
            mock_args.customer_id,
            mock_args.output_filepath,
            True  # write_headers should be True as --no-headers was not passed
        )
        sys.argv = original_argv

    @mock.patch("examples.misc.campaign_report_to_csv.argparse.ArgumentParser")
    @mock.patch("examples.misc.campaign_report_to_csv.GoogleAdsClient")
    def test_argument_parsing_no_headers_flag(self, mock_google_ads_client, mock_argument_parser):
        """Test argument parsing when --no-headers is specified."""
        mock_args = mock.Mock()
        mock_args.customer_id = "test_customer_id_no_header_arg"
        mock_args.output_filepath = "parsed_output_no_header.csv"
        mock_args.no_headers = True # Corresponds to write_headers=False
        mock_argument_parser.return_value.parse_args.return_value = mock_args

        mock_google_ads_client.load_from_storage.return_value = self.mock_client

        import sys
        original_argv = sys.argv
        sys.argv = [
            "campaign_report_to_csv.py",
            "-c", mock_args.customer_id,
            "-f", mock_args.output_filepath,
            "--no-headers"
        ]

        import runpy
        with mock.patch.object(campaign_report_to_csv, "main") as mock_script_main:
            runpy.run_module("examples.misc.campaign_report_to_csv", run_name="__main__")

        mock_script_main.assert_called_once_with(
            self.mock_client,
            mock_args.customer_id,
            mock_args.output_filepath,
            False  # write_headers should be False
        )
        sys.argv = original_argv


if __name__ == "__main__":
    unittest.main()
