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
        mock_args.ad_group_id = "ADGROUPID_01" # Optional, so test with it present
        mock_argument_parser.return_value.parse_args.return_value = mock_args

        # Mock the response from search
        # This is a row from the SearchGoogleAdsResponse, not AdGroupAd directly
        mock_row1 = MagicMock()
        mock_ad_group_ad = mock_row1.ad_group_ad # This is the AdGroupAd object

        mock_ad_group_ad.ad.resource_name = "customers/1234567890/ads/AD_ID_1"
        mock_ad_group_ad.status.name = "ENABLED" # Example status

        # RSA has headlines and descriptions (AdTextAsset)
        mock_headline1 = MagicMock()
        mock_headline1.text = "Cruise to Mars"
        mock_headline1.pinned_field.name = "HEADLINE_1" # Script uses asset.pinned_field.name

        mock_description1 = MagicMock()
        mock_description1.text = "Visit the Red Planet in style."
        mock_description1.pinned_field.name = "DESCRIPTION_1"

        mock_ad_group_ad.ad.responsive_search_ad.headlines = [mock_headline1]
        mock_ad_group_ad.ad.responsive_search_ad.descriptions = [mock_description1]
        # The script doesn't print final_urls for RSA, it prints headlines and descriptions

        # search returns an iterable of these rows
        mock_ga_service.search.return_value = [mock_row1]

        # Enums are compared by their .name attribute by the script, so no need to mock them as strings here
        # if the attributes being accessed on them (like .name) are already strings or MagicMocks.
        # The script uses ad.responsive_search_ad.headlines which are AdTextAssets.
        # ad_text_assets_to_strs accesses asset.text and asset.pinned_field.name.


        # Call the main function of the example script
        with patch("builtins.print") as mock_print:
            get_responsive_search_ads.main(mock_google_ads_client, mock_args.customer_id, mock_args.ad_group_id)

        # Assertions
        mock_google_ads_client.get_service.assert_called_once_with("GoogleAdsService")

        # Check that search was called
        mock_ga_service.search.assert_called_once()
        call_args = mock_ga_service.search.call_args

        # The first argument to search is the request object
        request_arg = call_args[1]['request'] # request is a keyword argument
        self.assertEqual(request_arg.customer_id, mock_args.customer_id)
        # Verify query construction based on ad_group_id presence
        self.assertIn(f"AND ad_group.id = {mock_args.ad_group_id}", request_arg.query)


        # Verify print output - this will be complex due to loops and formatting
        # We'll check for key pieces of information.
        # Note: The exact formatting of pinned fields might require more specific mocking if it's complex.
        # This example assumes simple text output for headlines and descriptions.

        # Expected calls based on the mocked ad structure
        # The script's print format is:
        # print(f"Responsive search ad with resource name \"{ad.resource_name}\", status {row.ad_group_ad.status.name} was found.")
        # print(f"Headlines:\n{headlines_str}\nDescriptions:\n{descriptions_str}\n")

        expected_ad_info_print = call(
            f"Responsive search ad with resource name \"{mock_ad_group_ad.ad.resource_name}\", status {mock_ad_group_ad.status.name} was found."
        )

        # Output from ad_text_assets_to_strs
        expected_headline_str = f"\t {mock_headline1.text} pinned to {mock_headline1.pinned_field.name}"
        expected_description_str = f"\t {mock_description1.text} pinned to {mock_description1.pinned_field.name}"

        expected_details_print = call(f"Headlines:\n{expected_headline_str}\nDescriptions:\n{expected_description_str}\n")

        expected_calls = [expected_ad_info_print, expected_details_print]

        mock_print.assert_has_calls(expected_calls, any_order=False)


    @patch("examples.basic_operations.get_responsive_search_ads.argparse.ArgumentParser")
    @patch("examples.basic_operations.get_responsive_search_ads.GoogleAdsClient.load_from_storage")
    def test_main_no_ad_group_id(self, mock_load_from_storage, mock_argument_parser):
        # Test the case where ad_group_id is None
        mock_google_ads_client = MagicMock()
        mock_load_from_storage.return_value = mock_google_ads_client
        mock_ga_service = MagicMock()
        mock_google_ads_client.get_service.return_value = mock_ga_service

        mock_args = MagicMock()
        mock_args.customer_id = "1234567890"
        mock_args.ad_group_id = None # Test this path
        mock_argument_parser.return_value.parse_args.return_value = mock_args

        mock_ga_service.search.return_value = [] # No results needed for this query check path

        with patch("builtins.print"): # Suppress print for this test
            get_responsive_search_ads.main(mock_google_ads_client, mock_args.customer_id, mock_args.ad_group_id)

        mock_ga_service.search.assert_called_once()
        request_arg = mock_ga_service.search.call_args[1]['request']
        self.assertNotIn("AND ad_group.id", request_arg.query)


if __name__ == "__main__":
    unittest.main()
