import unittest
from unittest import mock
import argparse
import sys

# Mock Google Ads Client and Exception if not available in the environment
try:
    from google.ads.googleads.client import GoogleAdsClient
    from google.ads.googleads.errors import GoogleAdsException
    # For PolicyApprovalStatusEnum and AdGroupAdStatusEnum
    from google.ads.googleads.v19.enums.types import policy_approval_status as policy_approval_status_enum_types
    from google.ads.googleads.v19.enums.types import ad_group_ad_status as ad_group_ad_status_enum_types

except ImportError:
    GoogleAdsClient = mock.MagicMock()
    GoogleAdsException = type('GoogleAdsException', (Exception,), {})
    # Mock enums if not available
    policy_approval_status_enum_types = mock.MagicMock()
    policy_approval_status_enum_types.PolicyApprovalStatusEnum.DISAPPROVED = "DISAPPROVED_MOCK" # Use a distinct value
    ad_group_ad_status_enum_types = mock.MagicMock()
    ad_group_ad_status_enum_types.AdGroupAdStatusEnum.ENABLED = "ENABLED_MOCK"


# Import the module to be tested
from examples.campaign_management import get_all_disapproved_ads as ga_script

class TestGetAllDisapprovedAds(unittest.TestCase):

    @mock.patch.object(GoogleAdsClient, "load_from_storage")
    def setUp(self, mock_load_from_storage):
        self.mock_google_ads_client = mock.MagicMock(spec=GoogleAdsClient)
        self.mock_google_ads_client.configure_mock(version="v19")
        mock_load_from_storage.return_value = self.mock_google_ads_client

        self.mock_google_ads_service = mock.MagicMock()
        self.mock_google_ads_client.get_service.return_value = self.mock_google_ads_service

        # Set up mock enums on the client instance if the script uses client.enums
        self.mock_google_ads_client.enums.PolicyApprovalStatusEnum = policy_approval_status_enum_types.PolicyApprovalStatusEnum
        self.mock_google_ads_client.enums.AdGroupAdStatusEnum = ad_group_ad_status_enum_types.AdGroupAdStatusEnum


        # Prepare mock GoogleAdsRow objects
        self.mock_row1 = mock.MagicMock()
        self.mock_row1.ad_group_ad.ad.id = 111
        self.mock_row1.ad_group_ad.ad.type_.name = "EXPANDED_TEXT_AD"
        # Policy summary
        pt_entry1 = mock.MagicMock()
        pt_entry1.topic = "Test Topic 1"
        pt_entry1.type_.name = "PROHIBITED_CONTENT"
        # Evidences (list of PolicyTopicEvidence)
        evidence1_text = mock.MagicMock()
        evidence1_text.text_list.texts = ["Evidence Text A", "Evidence Text B"]
        pt_entry1.evidences = [evidence1_text] # The script expects a list of evidences for each entry
        self.mock_row1.ad_group_ad.policy_summary.policy_topic_entries = [pt_entry1]
        self.mock_row1.ad_group_ad.policy_summary.approval_status = self.mock_google_ads_client.enums.PolicyApprovalStatusEnum.DISAPPROVED
        self.mock_row1.campaign.id = 1000
        self.mock_row1.ad_group.id = 2000


        self.mock_row2 = mock.MagicMock()
        self.mock_row2.ad_group_ad.ad.id = 222
        self.mock_row2.ad_group_ad.ad.type_.name = "RESPONSIVE_SEARCH_AD"
        # Policy summary
        pt_entry2 = mock.MagicMock()
        pt_entry2.topic = "Test Topic 2"
        pt_entry2.type_.name = "DESTINATION_MISMATCH"
        # Evidences
        evidence2_text = mock.MagicMock()
        evidence2_text.text_list.texts = ["Evidence Text C"]
        pt_entry2.evidences = [evidence2_text]
        self.mock_row2.ad_group_ad.policy_summary.policy_topic_entries = [pt_entry2]
        self.mock_row2.ad_group_ad.policy_summary.approval_status = self.mock_google_ads_client.enums.PolicyApprovalStatusEnum.DISAPPROVED
        self.mock_row2.campaign.id = 1000
        self.mock_row2.ad_group.id = 2001


    @mock.patch("argparse.ArgumentParser")
    @mock.patch("builtins.print")
    def test_main_with_disapproved_ads(self, mock_print, mock_argparse):
        customer_id = "12345"
        campaign_id = "1000" # Corresponds to campaign.id in mock_rows
        mock_args = argparse.Namespace(customer_id=customer_id, campaign_id=campaign_id)
        mock_argparse.return_value.parse_args.return_value = mock_args

        # Mock the response from google_ads_service.search
        mock_search_response = mock.MagicMock()
        # The script iterates over the response directly, so it should be an iterable of rows
        # The script also accesses response.total_results_count
        mock_search_response.total_results_count = 2
        # Make the mock response iterable to simulate stream-like behavior if needed,
        # or just return a list of rows if the script expects response.results
        # The script directly iterates `google_ads_service.search(request=search_request)`
        # So, the search method itself should be an iterable, or return an object that is.
        # Let's assume search returns an iterable of rows directly for simplicity matching the script's loop.
        self.mock_google_ads_service.search.return_value = iter([self.mock_row1, self.mock_row2])
        # If search returns a response object with a .results attribute:
        # mock_search_response.results = [self.mock_row1, self.mock_row2]
        # self.mock_google_ads_service.search.return_value = mock_search_response


        ga_script.main(self.mock_google_ads_client, customer_id, campaign_id)

        self.mock_google_ads_client.get_service.assert_called_once_with("GoogleAdsService", version="v19")
        
        self.mock_google_ads_service.search.assert_called_once()
        call_args = self.mock_google_ads_service.search.call_args
        request_arg = call_args[1]['request'] # or call_args.kwargs['request']
        self.assertEqual(request_arg.customer_id, customer_id)
        expected_query = ga_script.QUERY.format(campaign_id=campaign_id) # Use QUERY from the script
        self.assertEqual(request_arg.query, expected_query)

        # Assert print statements
        mock_print.assert_any_call(
            "Ad group ad with ID 111, type 'EXPANDED_TEXT_AD', and status 'DISAPPROVED' "
            "was found in campaign ID 1000, ad group ID 2000 "
            "with the following policy topic entries:"
        )
        mock_print.assert_any_call(
            "\tPolicy topic entry with topic 'Test Topic 1' and type "
            "'PROHIBITED_CONTENT' was found."
        )
        mock_print.assert_any_call("\t\tEvidence text: 'Evidence Text A'")
        mock_print.assert_any_call("\t\tEvidence text: 'Evidence Text B'")

        mock_print.assert_any_call(
            "Ad group ad with ID 222, type 'RESPONSIVE_SEARCH_AD', and status 'DISAPPROVED' "
            "was found in campaign ID 1000, ad group ID 2001 "
            "with the following policy topic entries:"
        )
        # ... similar assertions for row2 ...

        # The script doesn't explicitly print total_results_count from the response object.
        # It counts disapproved ads itself.
        mock_print.assert_any_call("Number of disapproved ads found: 2")


    @mock.patch("argparse.ArgumentParser")
    @mock.patch("builtins.print")
    def test_main_no_disapproved_ads(self, mock_print, mock_argparse):
        customer_id = "12345"
        campaign_id = "1001" # A campaign with no disapproved ads
        mock_args = argparse.Namespace(customer_id=customer_id, campaign_id=campaign_id)
        mock_argparse.return_value.parse_args.return_value = mock_args

        self.mock_google_ads_service.search.return_value = iter([]) # Empty stream

        ga_script.main(self.mock_google_ads_client, customer_id, campaign_id)
        
        mock_print.assert_any_call("Number of disapproved ads found: 0")
        # Check that other print statements for ad details were not called
        found_ad_detail_print = False
        for call_arg in mock_print.call_args_list:
            if "Ad group ad with ID" in call_arg[0][0]:
                found_ad_detail_print = True
                break
        self.assertFalse(found_ad_detail_print, "Should not print ad details if none are found.")


    @mock.patch("argparse.ArgumentParser")
    @mock.patch("builtins.print")
    @mock.patch("sys.exit")
    def test_main_google_ads_exception(self, mock_sys_exit, mock_print, mock_argparse):
        customer_id = "12345"
        campaign_id = "1002"
        mock_args = argparse.Namespace(customer_id=customer_id, campaign_id=campaign_id)
        mock_argparse.return_value.parse_args.return_value = mock_args

        # Create a mock GoogleAdsException instance
        mock_failure = mock.MagicMock()
        mock_error = mock.MagicMock()
        mock_error.message = "Test API Search Error"
        mock_failure.errors = [mock_error]
        google_ads_exception_instance = GoogleAdsException()
        google_ads_exception_instance._failure = mock_failure
        google_ads_exception_instance.request_id = "test_search_req_id"

        self.mock_google_ads_service.search.side_effect = google_ads_exception_instance

        ga_script.main(self.mock_google_ads_client, customer_id, campaign_id)

        printed_error = False
        for call in mock_print.call_args_list:
            if "Test API Search Error" in str(call[0]) and "ErrorCode" in str(call[0]):
                printed_error = True
                break
        self.assertTrue(printed_error, "GoogleAdsException error message was not printed correctly.")
        mock_sys_exit.assert_called_once_with(1)


if __name__ == "__main__":
    unittest.main()
