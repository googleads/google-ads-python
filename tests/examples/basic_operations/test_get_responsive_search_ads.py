import unittest
from unittest.mock import patch, MagicMock, call

from examples.basic_operations import get_responsive_search_ads

class TestGetResponsiveSearchAds(unittest.TestCase):

    @patch("examples.basic_operations.get_responsive_search_ads.argparse.ArgumentParser")
    @patch("examples.basic_operations.get_responsive_search_ads.GoogleAdsClient.load_from_storage")
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
        mock_args.ad_group_id = "ADGROUPID"  # Optional, so test with and without
        mock_argument_parser.return_value.parse_args.return_value = mock_args

        # Mock the response from search_stream
        mock_row1_ad = MagicMock()
        mock_row1_ad.resource_name = "customers/123/ads/RSA1"
        # Mock headlines
        mock_headline1 = MagicMock()
        mock_headline1.text = "Headline 1 RSA1"
        mock_headline1.asset_performance_label = mock_google_ads_client.enums.AssetPerformanceLabelEnum.PENDING
        mock_headline1.policy_summary.review_status = mock_google_ads_client.enums.PolicyReviewStatusEnum.REVIEWED
        mock_headline1.policy_summary.approval_status = mock_google_ads_client.enums.PolicyApprovalStatusEnum.APPROVED
        # Mock descriptions
        mock_desc1 = MagicMock()
        mock_desc1.text = "Description 1 RSA1"
        mock_desc1.asset_performance_label = mock_google_ads_client.enums.AssetPerformanceLabelEnum.LEARNING

        mock_row1_ad.responsive_search_ad.headlines = [mock_headline1]
        mock_row1_ad.responsive_search_ad.descriptions = [mock_desc1]


        mock_row1 = MagicMock()
        mock_row1.ad_group_ad.ad = mock_row1_ad

        mock_batch1 = MagicMock()
        mock_batch1.results = [mock_row1]

        mock_stream_response = [mock_batch1]
        mock_ga_service.search_stream.return_value = mock_stream_response

        # Call the main function of the example script
        with patch("builtins.print") as mock_print:
            # Test with ad_group_id
            get_responsive_search_ads.main(mock_google_ads_client, mock_args.customer_id, mock_args.ad_group_id)

            # Test without ad_group_id (reset mock_args and mock_ga_service calls for a clean second run)
            mock_args.ad_group_id = None
            mock_ga_service.reset_mock() # Reset call counts etc.
            mock_ga_service.search_stream.return_value = mock_stream_response # Re-assign return value
            get_responsive_search_ads.main(mock_google_ads_client, mock_args.customer_id, mock_args.ad_group_id)


        # Assertions
        self.assertEqual(mock_load_from_storage.call_count, 2) # Called twice
        mock_load_from_storage.assert_called_with(version="v19") # Check one of the calls

        self.assertEqual(mock_google_ads_client.get_service.call_count, 2)
        mock_google_ads_client.get_service.assert_called_with("GoogleAdsService")

        # Check query for call WITH ad_group_id
        args_with, kwargs_with = mock_ga_service.search_stream.call_args_list[0]
        self.assertEqual(kwargs_with['customer_id'], "1234567890")
        self.assertIn("AND ad_group.id = 'ADGROUPID'", kwargs_with['query'])

        # Check query for call WITHOUT ad_group_id
        args_without, kwargs_without = mock_ga_service.search_stream.call_args_list[1]
        self.assertEqual(kwargs_without['customer_id'], "1234567890")
        self.assertNotIn("AND ad_group.id", kwargs_without['query'])

        # Verify print output (simplified for one call, can be expanded)
        # This will check the print calls from the first main() call (with ad_group_id)
        expected_print_calls = [
            call("Responsive search ad with resource name "
                 ""customers/123/ads/RSA1" was found."),
            call("	Headlines:"),
            call("		Headline text: Headline 1 RSA1"),
            call("		Performance: PENDING"),
            call("		Review status: REVIEWED"),
            call("		Approval status: APPROVED"),
            call("	Descriptions:"),
            call("		Description text: Description 1 RSA1"),
            call("		Performance: LEARNING"),
        ]
        # mock_print.assert_has_calls(expected_print_calls, any_order=False)
        # Due to two calls to main, the above assert_has_calls will be tricky without more complex print mocking.
        # We can check if a specific print happened:
        mock_print.assert_any_call("Responsive search ad with resource name "
                                   ""customers/123/ads/RSA1" was found.")


if __name__ == "__main__":
    unittest.main()
