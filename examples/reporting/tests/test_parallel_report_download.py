import unittest
from unittest.mock import MagicMock, patch, call
import sys
import os

# Add the examples directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from reporting.parallel_report_download import (
    generate_inputs,
    issue_search_request,
    main,
    MAX_RETRIES,
    BACKOFF_FACTOR,
)
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

# Initialize a client for type retrieval. This doesn't need real credentials.
# We mock load_from_storage to avoid filesystem access or network calls during test module loading
# for the client instance that will be used by the code under test.
# However, for setting up type information (Campaign, Metrics, etc.) and service client classes
import yaml

# (GoogleAdsServiceClient) correctly for v19, we need a real client instance that is
# configured for v19 and can provide these definitions.
minimal_yaml_config_str = """
developer_token: FAKE_TOKEN
use_proto_plus: True
login_customer_id: "1234567890"
# Adding fake OAuth2 credentials to satisfy client initialization requirements
client_id: FAKE_CLIENT_ID
client_secret: FAKE_CLIENT_SECRET
refresh_token: FAKE_REFRESH_TOKEN
"""
minimal_config_dict = yaml.safe_load(minimal_yaml_config_str)

# Prevent credentials from attempting to refresh during helper client initialization
with patch("google.oauth2.credentials.Credentials.refresh", return_value=None) as mock_refresh:
    _helper_real_client_v19_for_types = GoogleAdsClient.load_from_dict(
        config_dict=minimal_config_dict, version="v19"
    )

with patch.object(GoogleAdsClient, "load_from_storage", return_value=MagicMock()) as mock_load_storage:
    # This mock_load_storage patch is for when the code *under test* calls
    # GoogleAdsClient.load_from_storage. In our tests, the client is passed directly.
    # However, if parallel_report_download.py itself called load_from_storage at module level,
    # this patch would affect it. The main script calls it inside if __name__ == "__main__".
    # For the purpose of our test setup, client_mock_returned_by_load_storage
    # helps get the types correctly if we didn't have _helper_real_client_v19_for_types.
    # Given we now have _helper_real_client_v19_for_types, this specific mock's role in type loading is reduced,
    # but it's still useful for controlling what load_from_storage returns if called by SUT.
    # Let's ensure it's configured to use the helper as well for consistency,
    # although the global types are already resolved using the helper directly.
    # It's a MagicMock due to the patch. We configure it to delegate type/service retrieval
    # to our helper_real_client_v19_for_types.
    client_mock_returned_by_load_storage = mock_load_storage.return_value
    client_mock_returned_by_load_storage.configure_mock(**{
        "get_type": lambda name, version="v19": _helper_real_client_v19_for_types.get_type(name, version=version),
        "get_service": lambda name, version="v19": _helper_real_client_v19_for_types.get_service(name, version=version)
    })

# Dynamically get service client class and type classes using the _helper_real_client_v19_for_types.
# Assuming get_type() might be returning an instance, get its class via type().
GoogleAdsServiceClient_class = _helper_real_client_v19_for_types.get_service("GoogleAdsService", version="v19").__class__

_SearchGoogleAdsStreamResponse_maybe_instance = _helper_real_client_v19_for_types.get_type("SearchGoogleAdsStreamResponse", version="v19")
SearchGoogleAdsStreamResponse_class = type(_SearchGoogleAdsStreamResponse_maybe_instance)

_Metrics_maybe_instance = _helper_real_client_v19_for_types.get_type("Metrics", version="v19")
Metrics_class = type(_Metrics_maybe_instance)

_Campaign_maybe_instance = _helper_real_client_v19_for_types.get_type("Campaign", version="v19")
Campaign_class = type(_Campaign_maybe_instance)

_AdGroup_maybe_instance = _helper_real_client_v19_for_types.get_type("AdGroup", version="v19")
AdGroup_class = type(_AdGroup_maybe_instance)

_GoogleAdsRow_maybe_instance = _helper_real_client_v19_for_types.get_type("GoogleAdsRow", version="v19")
GoogleAdsRow_class = type(_GoogleAdsRow_maybe_instance)


class ParallelReportDownloadTest(unittest.TestCase):
    def setUp(self):
        # This is the mock client instance that will be passed to the functions under test.
        # It should behave like a GoogleAdsClient.
        self.mock_google_ads_client = MagicMock(spec=GoogleAdsClient)

        # This is the mock for the GoogleAdsService client.
        self.mock_ga_service = MagicMock(spec=GoogleAdsServiceClient_class) # Use the class obtained above

        # Configure the mock_google_ads_client to return mock_ga_service when get_service is called.
        self.mock_google_ads_client.get_service.return_value = self.mock_ga_service

        # Configure get_type on the mock_google_ads_client to also use the helper for consistency,
        # in case the code under test calls client.get_type().
        # It should return the *class* of the type, so we use the _class variables.
        # This lambda needs to map type names to their classes.
        type_class_map = {
            "SearchGoogleAdsStreamResponse": SearchGoogleAdsStreamResponse_class,
            "Metrics": Metrics_class,
            "Campaign": Campaign_class,
            "AdGroup": AdGroup_class,
            "GoogleAdsRow": GoogleAdsRow_class,
        }
        self.mock_google_ads_client.get_type.side_effect = lambda name, version="v19": type_class_map.get(name)


    def test_generate_inputs(self):
        customer_ids = ["123", "456"]
        queries = ["query1", "query2"]
        inputs = list(
            generate_inputs(self.mock_google_ads_client, customer_ids, queries)
        )

        self.assertEqual(len(inputs), len(customer_ids) * len(queries))
        for i, (client, customer_id, query) in enumerate(inputs):
            self.assertEqual(client, self.mock_google_ads_client)
            self.assertIn(customer_id, customer_ids)
            self.assertIn(query, queries)

    def _create_mock_search_stream_response(self, campaign_id, impressions, clicks, ad_group_id=None):
        # Use the _class variables obtained at module level
        mock_row = GoogleAdsRow_class()
        mock_row.campaign = Campaign_class()
        mock_row.campaign.id = campaign_id
        mock_row.metrics = Metrics_class()
        mock_row.metrics.impressions = impressions
        mock_row.metrics.clicks = clicks
        if ad_group_id:
            mock_row.ad_group = AdGroup_class()
            mock_row.ad_group.id = ad_group_id

        mock_response = SearchGoogleAdsStreamResponse_class()
        mock_response.results.append(mock_row)
        return [mock_response]

    def test_issue_search_request_success(self):
        customer_id = "123"
        query = "SELECT campaign.id, metrics.impressions, metrics.clicks FROM campaign"

        mock_stream = self._create_mock_search_stream_response(campaign_id=1, impressions=100, clicks=10)
        self.mock_ga_service.search_stream.return_value = mock_stream

        success, result = issue_search_request(
            self.mock_google_ads_client, customer_id, query
        )

        self.assertTrue(success)
        self.assertIn("results", result)
        self.assertEqual(len(result["results"]), 1)
        self.assertIn("Campaign ID 1 had 100 impressions and 10 clicks.", result["results"][0])
        self.mock_ga_service.search_stream.assert_called_once_with(
            customer_id=customer_id, query=query
        )

    def test_issue_search_request_success_with_ad_group(self):
        customer_id = "123"
        query = "SELECT campaign.id, ad_group.id, metrics.impressions, metrics.clicks FROM ad_group"

        mock_stream = self._create_mock_search_stream_response(campaign_id=1, ad_group_id=2, impressions=100, clicks=10)
        self.mock_ga_service.search_stream.return_value = mock_stream

        success, result = issue_search_request(
            self.mock_google_ads_client, customer_id, query
        )

        self.assertTrue(success)
        self.assertIn("results", result)
        self.assertEqual(len(result["results"]), 1)
        self.assertIn("Ad Group ID 2 in Campaign ID 1 had 100 impressions and 10 clicks.", result["results"][0])
        self.mock_ga_service.search_stream.assert_called_once_with(
            customer_id=customer_id, query=query
        )


    @patch("time.sleep", return_value=None)  # Mock time.sleep to speed up test
    def test_issue_search_request_failure_then_success(self, mock_sleep):
        customer_id = "123"
        query = "query"

        # Simulate failure then success
        mock_google_ads_exception = GoogleAdsException(
            error=MagicMock(),
            failure=MagicMock(),
            call=MagicMock(),
            request_id="test_request_id"
        )
        mock_stream = self._create_mock_search_stream_response(campaign_id=1, impressions=100, clicks=10)
        self.mock_ga_service.search_stream.side_effect = [
            mock_google_ads_exception,
            mock_stream,
        ]

        success, result = issue_search_request(
            self.mock_google_ads_client, customer_id, query
        )

        self.assertTrue(success)
        self.assertEqual(self.mock_ga_service.search_stream.call_count, 2)
        mock_sleep.assert_called_once_with(1 * BACKOFF_FACTOR)


    @patch("time.sleep", return_value=None)  # Mock time.sleep to speed up test
    def test_issue_search_request_failure_max_retries(self, mock_sleep):
        customer_id = "123"
        query = "query"

        mock_google_ads_exception = GoogleAdsException(
            error=MagicMock(),
            failure=MagicMock(),
            call=MagicMock(),
            request_id="test_request_id"
        )
        self.mock_ga_service.search_stream.side_effect = mock_google_ads_exception

        success, result = issue_search_request(
            self.mock_google_ads_client, customer_id, query
        )

        self.assertFalse(success)
        self.assertIn("exception", result)
        self.assertEqual(result["exception"], mock_google_ads_exception)
        self.assertEqual(result["customer_id"], customer_id)
        self.assertEqual(result["query"], query)
        self.assertEqual(self.mock_ga_service.search_stream.call_count, MAX_RETRIES + 1)
        # Check that sleep was called with increasing backoff
        expected_sleep_calls = [call(i * BACKOFF_FACTOR) for i in range(1, MAX_RETRIES + 1)]
        mock_sleep.assert_has_calls(expected_sleep_calls)


    @patch("reporting.parallel_report_download.multiprocessing.Pool")
    def test_main_function(self, mock_pool):
        customer_ids = ["123", "456"]
        mock_pool_instance = MagicMock()
        mock_pool.return_value.__enter__.return_value = mock_pool_instance

        # Simulate results from issue_search_request
        results_data = [
            (True, {"results": ["result1"]}),
            (False, {"exception": MagicMock(), "customer_id": "456", "query": "query2"}),
        ]
        mock_pool_instance.starmap.return_value = results_data

        with patch("builtins.print") as mock_print:
            main(self.mock_google_ads_client, customer_ids)

        # Check that generate_inputs was called (indirectly via main)
        # We can't directly check the call to generate_inputs here without more refactoring
        # of the main function, but we can check that starmap was called with the
        # expected number of arguments based on customers and queries.
        # Expected queries defined in main()
        expected_query_count = 2
        # The 'inputs' passed to starmap is an itertools.product object.
        # We need to compare its list representation with the expected list of inputs.
        actual_starmap_inputs = list(mock_pool_instance.starmap.call_args[0][1])
        expected_starmap_inputs = list(generate_inputs(self.mock_google_ads_client, customer_ids, [
            # These are the queries defined in parallel_report_download.main
            """
        SELECT campaign.id, metrics.impressions, metrics.clicks
        FROM campaign
        WHERE segments.date DURING LAST_30_DAYS""",
            """
        SELECT campaign.id, ad_group.id, metrics.impressions, metrics.clicks
        FROM ad_group
        WHERE segments.date DURING LAST_30_DAYS"""
        ]))
        self.assertEqual(actual_starmap_inputs, expected_starmap_inputs)

        # Check output
        # This is a bit brittle as it depends on exact print formatting
        # Consider capturing stdout in a more robust way if this becomes an issue
        mock_print.assert_any_call("Total successful results: 1\nTotal failed results: 1\n")
        mock_print.assert_any_call("Successes:")
        mock_print.assert_any_call("result1")
        mock_print.assert_any_call("Failures:")
        # Cannot easily assert the full failure message due to MagicMock in exception

if __name__ == "__main__":
    unittest.main()
