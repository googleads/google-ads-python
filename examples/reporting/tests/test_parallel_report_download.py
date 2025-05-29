import unittest
from unittest import mock

# This will allow us to import the script from the parent directory
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import argparse
import multiprocessing
import runpy

import parallel_report_download
from google.ads.googleads.client import GoogleAdsClient # For spec
from google.ads.googleads.errors import GoogleAdsException
# v19 imports (ensure these are correct based on library structure)
from google.ads.googleads.v19.services.services.google_ads_service import GoogleAdsServiceClient
from google.ads.googleads.v19.services.types.google_ads_service import SearchGoogleAdsStreamResponse
# from google.ads.googleads.v19.common.types import Value # Not used in current example but good to have if needed
from google.ads.googleads.v19.resources.types.ad_group import AdGroup
from google.ads.googleads.v19.resources.types.campaign import Campaign
from google.ads.googleads.v19.common.types.metrics import Metrics
from google.ads.googleads.v19.services.types.google_ads_service import GoogleAdsRow

class TestParallelReportDownload(unittest.TestCase):
    def test_generate_inputs(self):
        mock_client = mock.Mock()
        customer_ids = ["123", "456"]
        queries = ["QUERY_1", "QUERY_2"]

        inputs_iterable = parallel_report_download.generate_inputs(
            mock_client, customer_ids, queries
        )
        inputs_list = list(inputs_iterable)

        self.assertEqual(len(inputs_list), len(customer_ids) * len(queries))

        expected_inputs = [
            (mock_client, "123", "QUERY_1"),
            (mock_client, "123", "QUERY_2"),
            (mock_client, "456", "QUERY_1"),
            (mock_client, "456", "QUERY_2"),
        ]

        # Convert to sets of tuples to ignore order for comparison,
        # or ensure the order is deterministic and compare lists directly.
        # For product, the order is deterministic.
        self.assertEqual(inputs_list, expected_inputs)

    def test_issue_search_request_success(self):
        mock_client = mock.Mock(spec=GoogleAdsClient)
        # If GoogleAdsClient is imported directly in parallel_report_download
        # from google.ads.googleads.client import GoogleAdsClient
        # then spec should be GoogleAdsClient from that import.
        # Let's assume it's available as parallel_report_download.GoogleAdsClient for now.

        # Ensure the client has the _client_wrapper attribute structure if that's how version is accessed
        # or directly set version if the object would have it.
        # The main script does client = GoogleAdsClient.load_from_storage(version="v19")
        # The client object itself doesn't directly have a 'version' attribute,
        # it's used during initialization. We need to ensure our mocks behave as if called by a v19 client.
        # For the purpose of this function, the client is already initialized.
        # We primarily care about mocking get_service.

        mock_ga_service = mock.Mock(spec=GoogleAdsServiceClient) # Use the imported v19 service client
        mock_client.get_service.return_value = mock_ga_service

        # Setup mock rows and response for campaign query
        mock_row_campaign = mock.Mock(spec=GoogleAdsRow)
        mock_row_campaign.campaign = mock.Mock(spec=Campaign)
        mock_row_campaign.campaign.id = 1001
        mock_row_campaign.metrics = mock.Mock(spec=Metrics)
        mock_row_campaign.metrics.impressions = 150
        mock_row_campaign.metrics.clicks = 15

        mock_batch_campaign = mock.Mock(spec=SearchGoogleAdsStreamResponse)
        mock_batch_campaign.results = [mock_row_campaign]
        
        mock_ga_service.search_stream.return_value = [mock_batch_campaign]

        customer_id = "test_customer_1"
        campaign_query = "SELECT campaign.id, metrics.impressions, metrics.clicks FROM campaign"

        success, result_dict = parallel_report_download.issue_search_request(
            mock_client, customer_id, campaign_query
        )

        self.assertTrue(success)
        self.assertIn("results", result_dict)
        self.assertEqual(len(result_dict["results"]), 1)
        self.assertEqual(
            result_dict["results"][0],
            "Campaign ID 1001 had 150 impressions and 15 clicks."
        )
        mock_ga_service.search_stream.assert_called_once_with(
            customer_id=customer_id, query=campaign_query
        )
        mock_client.get_service.assert_called_with("GoogleAdsService")


        # Test with ad_group query
        mock_ga_service.search_stream.reset_mock() # Reset for the next call
        mock_client.get_service.reset_mock()


        mock_row_ad_group = mock.Mock(spec=GoogleAdsRow)
        mock_row_ad_group.campaign = mock.Mock(spec=Campaign)
        mock_row_ad_group.campaign.id = 2002
        mock_row_ad_group.ad_group = mock.Mock(spec=AdGroup)
        mock_row_ad_group.ad_group.id = 3003
        mock_row_ad_group.metrics = mock.Mock(spec=Metrics)
        mock_row_ad_group.metrics.impressions = 250
        mock_row_ad_group.metrics.clicks = 25

        mock_batch_ad_group = mock.Mock(spec=SearchGoogleAdsStreamResponse)
        mock_batch_ad_group.results = [mock_row_ad_group]
        
        mock_ga_service.search_stream.return_value = [mock_batch_ad_group]
        
        ad_group_query = "SELECT campaign.id, ad_group.id, metrics.impressions, metrics.clicks FROM ad_group"
        success, result_dict = parallel_report_download.issue_search_request(
            mock_client, customer_id, ad_group_query
        )

        self.assertTrue(success)
        self.assertIn("results", result_dict)
        self.assertEqual(len(result_dict["results"]), 1)
        self.assertEqual(
            result_dict["results"][0],
            "Ad Group ID 3003 in Campaign ID 2002 had 250 impressions and 25 clicks."
        )
        mock_ga_service.search_stream.assert_called_once_with(
            customer_id=customer_id, query=ad_group_query
        )
        mock_client.get_service.assert_called_with("GoogleAdsService")

    @mock.patch('time.sleep') # Mock time.sleep to avoid actual delays
    def test_issue_search_request_error_and_retry_success(self, mock_sleep):
        mock_client = mock.Mock(spec=GoogleAdsClient)
        mock_ga_service = mock.Mock(spec=GoogleAdsServiceClient)
        mock_client.get_service.return_value = mock_ga_service

        customer_id = "test_customer_retry"
        # Ensure query matches mock row structure for expected output string
        query = "SELECT campaign.id, metrics.impressions, metrics.clicks FROM campaign" 

        # Minimal exception for testing retries
        exception = GoogleAdsException(None, None, None) 
        
        mock_row_campaign = mock.Mock(spec=GoogleAdsRow)
        mock_row_campaign.campaign = mock.Mock(spec=Campaign)
        mock_row_campaign.campaign.id = 789
        mock_row_campaign.metrics = mock.Mock(spec=Metrics)
        mock_row_campaign.metrics.impressions = 10
        mock_row_campaign.metrics.clicks = 1

        mock_batch_success = mock.Mock(spec=SearchGoogleAdsStreamResponse)
        mock_batch_success.results = [mock_row_campaign]
        
        num_failures = 2 # Example: fail twice, then succeed on the 3rd attempt
        side_effects_list = [exception] * num_failures + [[mock_batch_success]]
        mock_ga_service.search_stream.side_effect = side_effects_list

        success, result_dict = parallel_report_download.issue_search_request(
            mock_client, customer_id, query
        )

        self.assertTrue(success)
        self.assertIn("results", result_dict)
        self.assertEqual(len(result_dict["results"]), 1) # Ensure only one result string
        self.assertEqual(result_dict["results"][0], "Campaign ID 789 had 10 impressions and 1 clicks.")
        self.assertEqual(mock_ga_service.search_stream.call_count, num_failures + 1)
        self.assertEqual(mock_sleep.call_count, num_failures)
        
        # Verify sleep call arguments if precise backoff timing is critical to test
        expected_sleep_calls = [
            mock.call(i * parallel_report_download.BACKOFF_FACTOR) 
            for i in range(1, num_failures + 1)
        ]
        mock_sleep.assert_has_calls(expected_sleep_calls, any_order=False) # Ensure order of sleeps

    @mock.patch('time.sleep')
    def test_issue_search_request_error_max_retries_exceeded(self, mock_sleep):
        mock_client = mock.Mock(spec=GoogleAdsClient)
        mock_ga_service = mock.Mock(spec=GoogleAdsServiceClient)
        mock_client.get_service.return_value = mock_ga_service

        customer_id = "test_customer_max_retry"
        query = "SELECT campaign.id FROM campaign" # Query content doesn't matter as much here

        # Construct a GoogleAdsException with details the main script might use for logging
        mock_error_payload = mock.Mock() 
        mock_error_payload.code.return_value.name = "TEST_ERROR_CODE"
        
        mock_failure_payload = mock.Mock() 
        mock_error_message_detail = mock.Mock()
        mock_error_message_detail.message = "Detailed error message for max retries test."
        mock_error_message_detail.location = None 
        mock_failure_payload.errors = [mock_error_message_detail]

        exception_instance = GoogleAdsException(
            error=mock_error_payload,
            failure=mock_failure_payload,
            call=mock.Mock(), # Mock call object
            request_id="test_request_id_exhausted"
        )
        
        # search_stream will be called MAX_RETRIES + 1 times before giving up
        num_calls_for_failure = parallel_report_download.MAX_RETRIES + 1
        mock_ga_service.search_stream.side_effect = [exception_instance] * num_calls_for_failure

        success, result_dict = parallel_report_download.issue_search_request(
            mock_client, customer_id, query
        )

        self.assertFalse(success)
        self.assertIn("exception", result_dict)
        self.assertIs(result_dict["exception"], exception_instance) 
        self.assertEqual(result_dict["customer_id"], customer_id)
        self.assertEqual(result_dict["query"], query)
        
        self.assertEqual(mock_ga_service.search_stream.call_count, num_calls_for_failure)
        self.assertEqual(mock_sleep.call_count, parallel_report_download.MAX_RETRIES)

    @mock.patch('builtins.print')
    @mock.patch('multiprocessing.Pool')
    @mock.patch('parallel_report_download.generate_inputs')
    def test_main_function_success_and_failure(
        self,
        mock_generate_inputs, # Corresponds to @mock.patch('parallel_report_download.generate_inputs')
        mock_pool_constructor, # Corresponds to @mock.patch('multiprocessing.Pool')
        mock_print            # Corresponds to @mock.patch('builtins.print')
    ):
        # --- Setup Mocks ---
        mock_client_instance = mock.Mock(spec=GoogleAdsClient) 

        dummy_inputs = [
            (mock_client_instance, "cust1", "q1"),
            (mock_client_instance, "cust2", "q2"),
            (mock_client_instance, "cust3", "q3")
        ]
        mock_generate_inputs.return_value = dummy_inputs

        mock_pool_instance = mock.Mock()
        mock_pool_constructor.return_value.__enter__.return_value = mock_pool_instance

        mock_google_ads_exception = mock.Mock(spec=GoogleAdsException)
        mock_google_ads_exception.request_id = "test_req_id_main"
        
        mock_error_code = mock.Mock()
        mock_error_code.name = "INTERNAL_ERROR"
        mock_error_obj = mock.Mock() # Renamed from mock_error to avoid conflict if it's a var name
        mock_error_obj.code.return_value = mock_error_code
        mock_google_ads_exception.error = mock_error_obj
        
        mock_failure_error_detail = mock.Mock()
        mock_failure_error_detail.message = "Specific error message for cust2"
        mock_failure_error_detail.location = None 

        mock_failure_obj = mock.Mock() # Renamed from mock_failure
        mock_failure_obj.errors = [mock_failure_error_detail]
        mock_google_ads_exception.failure = mock_failure_obj

        mock_starmap_results = [
            (True, {"results": ["Success data for cust1, q1"]}),
            (False, {
                "exception": mock_google_ads_exception,
                "customer_id": "cust2",
                "query": "q2" 
            }),
            (True, {"results": ["Success data for cust3, q3"]}),
        ]
        mock_pool_instance.starmap.return_value = mock_starmap_results

        customer_ids_arg = ["cust1", "cust2", "cust3"]

        parallel_report_download.main(mock_client_instance, customer_ids_arg)

        mock_generate_inputs.assert_called_once_with(
            mock_client_instance, 
            customer_ids_arg, 
            [parallel_report_download.campaign_query, parallel_report_download.ad_group_query]
        )
        
        mock_pool_constructor.assert_called_once_with(parallel_report_download.MAX_PROCESSES)
        mock_pool_instance.starmap.assert_called_once_with(
            parallel_report_download.issue_search_request, dummy_inputs 
        )

        print_calls_args = [call_args[0][0] if call_args[0] else "" for call_args in mock_print.call_args_list]
        full_print_output = "".join(print_calls_args)

        self.assertIn("Total successful results: 2", full_print_output)
        self.assertIn("Total failed results: 1", full_print_output)
        self.assertIn("Successes:", full_print_output)
        self.assertIn("Success data for cust1, q1", full_print_output)
        self.assertIn("Success data for cust3, q3", full_print_output)
        self.assertIn("Failures:", full_print_output)
        expected_failure_string = (
            'Request with ID "test_req_id_main" failed with status '
            '"INTERNAL_ERROR" for customer_id '
            'cust2 and query "q2" and includes the following errors:'
        )
        self.assertIn(expected_failure_string, full_print_output)
        self.assertIn('\tError with message "Specific error message for cust2".', full_print_output)

    @mock.patch('google.ads.googleads.client.GoogleAdsClient.load_from_storage')
    @mock.patch('argparse.ArgumentParser')
    @mock.patch('parallel_report_download.main') 
    def test_if_name_main_block(
        self,
        mock_main_function_in_module, # Corresponds to @mock.patch('parallel_report_download.main')
        mock_arg_parser_constructor,  # Corresponds to @mock.patch('argparse.ArgumentParser')
        mock_load_client              # Corresponds to @mock.patch('google.ads.googleads.client.GoogleAdsClient.load_from_storage')
    ):
        mock_parser_instance = mock.Mock()
        mock_arg_parser_constructor.return_value = mock_parser_instance

        # --- Test with login_customer_id ---
        mock_args_with_login = argparse.Namespace(
            customer_ids=["id1", "id2"],
            login_customer_id="login_id123"
        )
        mock_parser_instance.parse_args.return_value = mock_args_with_login

        mock_client_instance_with_login = mock.Mock(spec=GoogleAdsClient)
        mock_client_instance_with_login.login_customer_id = None 
        mock_load_client.return_value = mock_client_instance_with_login
        
        # Ensure parallel_report_download is treated as the main module context
        # This requires parallel_report_download.py to be in sys.path
        # The sys.path.append at the top of the test file should handle this.
        runpy.run_module("parallel_report_download", run_name="__main__")

        mock_load_client.assert_called_once_with(version="v19")
        self.assertEqual(mock_client_instance_with_login.login_customer_id, "login_id123")
        mock_main_function_in_module.assert_called_once_with(
            mock_client_instance_with_login, mock_args_with_login.customer_ids
        )

        # --- Reset mocks for the next case ---
        mock_main_function_in_module.reset_mock()
        mock_load_client.reset_mock()
        mock_arg_parser_constructor.reset_mock() 
        mock_parser_instance.reset_mock() 

        # --- Test without login_customer_id ---
        mock_args_no_login = argparse.Namespace(
            customer_ids=["id3"],
            login_customer_id=None 
        )
        mock_parser_instance.parse_args.return_value = mock_args_no_login

        mock_client_instance_no_login = mock.Mock(spec=GoogleAdsClient)
        mock_client_instance_no_login.login_customer_id = None # Client's default login_customer_id is None
        mock_load_client.return_value = mock_client_instance_no_login
        
        runpy.run_module("parallel_report_download", run_name="__main__")
        
        mock_load_client.assert_called_once_with(version="v19")
        self.assertIsNone(mock_client_instance_no_login.login_customer_id) 
        
        mock_main_function_in_module.assert_called_once_with(
            mock_client_instance_no_login, mock_args_no_login.customer_ids
        )

if __name__ == '__main__':
    unittest.main()
