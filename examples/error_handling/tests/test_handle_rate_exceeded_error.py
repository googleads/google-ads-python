import argparse
import unittest
from unittest.mock import MagicMock, patch, call
from time import sleep

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
# QuotaErrorEnum import removed (or commented out) as it's obtained via client.get_type in production code

from examples.error_handling.handle_rate_exceeded_error import main, NUM_REQUESTS, NUM_RETRIES, RETRY_SECONDS


class TestHandleRateExceededError(unittest.TestCase):
    @patch("examples.error_handling.handle_rate_exceeded_error.GoogleAdsClient")
    @patch("examples.error_handling.handle_rate_exceeded_error.create_ad_group_criterion_operations")
    @patch("examples.error_handling.handle_rate_exceeded_error.request_mutate_and_display_result")
    @patch("examples.error_handling.handle_rate_exceeded_error.sleep") # Mock sleep
    def test_main_success_no_errors(
        self, mock_sleep, mock_request_mutate, mock_create_operations, mock_google_ads_client
    ):
        mock_client_instance = MagicMock(spec=GoogleAdsClient)
        mock_google_ads_client.load_from_storage.return_value = mock_client_instance

        # Mock for client.get_type("QuotaErrorEnum").QuotaError
        mock_quota_error_obj = MagicMock()
        mock_quota_error_obj.RESOURCE_EXHAUSTED = "RESOURCE_EXHAUSTED_PLACEHOLDER"
        mock_quota_error_obj.RESOURCE_TEMPORARILY_EXHAUSTED = "RESOURCE_TEMPORARILY_EXHAUSTED_PLACEHOLDER"

        # client.get_type("QuotaErrorEnum") should return an object that has a QuotaError attribute.
        mock_client_instance.get_type.return_value = MagicMock(QuotaError=mock_quota_error_obj)
        # More specific mocking if get_type is called for other enums in the same test:
        # def get_type_side_effect(name):
        #     if name == "QuotaErrorEnum":
        #         return MagicMock(QuotaError=mock_quota_error_obj)
        #     return MagicMock()
        # mock_client_instance.get_type.side_effect = get_type_side_effect

        mock_operations = [MagicMock()]
        mock_create_operations.return_value = mock_operations

        mock_args = argparse.Namespace(customer_id="123", ad_group_id="456")

        with patch("argparse.ArgumentParser.parse_args", return_value=mock_args):
            main(mock_client_instance, mock_args.customer_id, mock_args.ad_group_id)

        # mock_google_ads_client.load_from_storage.assert_called_once_with(version="v19") # Removed: main is called with an instance
        self.assertEqual(mock_create_operations.call_count, NUM_REQUESTS)
        self.assertEqual(mock_request_mutate.call_count, NUM_REQUESTS)
        mock_request_mutate.assert_has_calls(
            [call(mock_client_instance, "123", mock_operations)] * NUM_REQUESTS
        )
        mock_sleep.assert_not_called() # Sleep should not be called if no errors

    @patch("examples.error_handling.handle_rate_exceeded_error.GoogleAdsClient")
    @patch("examples.error_handling.handle_rate_exceeded_error.create_ad_group_criterion_operations")
    @patch("examples.error_handling.handle_rate_exceeded_error.request_mutate_and_display_result")
    @patch("examples.error_handling.handle_rate_exceeded_error.sleep")
    @patch("builtins.print")
    def test_main_handles_rate_exceeded_error_and_retries(
        self, mock_print, mock_sleep, mock_request_mutate, mock_create_operations, mock_google_ads_client
    ):
        mock_client_instance = MagicMock(spec=GoogleAdsClient)
        mock_google_ads_client.load_from_storage.return_value = mock_client_instance

        # Mock for client.get_type("QuotaErrorEnum").QuotaError
        mock_quota_error_obj = MagicMock()
        mock_quota_error_obj.RESOURCE_EXHAUSTED = "RESOURCE_EXHAUSTED_PLACEHOLDER"
        mock_quota_error_obj.RESOURCE_TEMPORARILY_EXHAUSTED = "RESOURCE_TEMPORARILY_EXHAUSTED_PLACEHOLDER"

        # client.get_type("QuotaErrorEnum") should return an object that has a QuotaError attribute.
        # Using side_effect for more robust mocking if get_type is called for other enums.
        def get_type_side_effect(name):
            if name == "QuotaErrorEnum":
                return MagicMock(QuotaError=mock_quota_error_obj)
            return MagicMock()
        mock_client_instance.get_type.side_effect = get_type_side_effect

        mock_operations = [MagicMock()]
        mock_create_operations.return_value = mock_operations

        # Simulate RateExceededError on the first call for the first request, then success
        rate_exceeded_error = GoogleAdsException(
            error=MagicMock(),
            failure=MagicMock(errors=[
                MagicMock(error_code=MagicMock(quota_error="RESOURCE_TEMPORARILY_EXHAUSTED_PLACEHOLDER"))
            ]),
            call=MagicMock(),
            request_id="test_req_id_rate_exceeded"
        )

        # Let the first request fail once with rate limit, then succeed. Other requests succeed immediately.
        side_effects = [rate_exceeded_error, None] + [None] * (NUM_REQUESTS -1)
        mock_request_mutate.side_effect = side_effects

        mock_args = argparse.Namespace(customer_id="123", ad_group_id="456")

        with patch("argparse.ArgumentParser.parse_args", return_value=mock_args):
            main(mock_client_instance, mock_args.customer_id, mock_args.ad_group_id)

        self.assertEqual(mock_create_operations.call_count, NUM_REQUESTS)
        # Total calls = NUM_REQUESTS (original attempts) + 1 (for the single retry)
        self.assertEqual(mock_request_mutate.call_count, NUM_REQUESTS + 1)
        mock_sleep.assert_called_once_with(RETRY_SECONDS)
        mock_print.assert_any_call(f"Received rate exceeded error, retry after{RETRY_SECONDS} seconds.")

    @patch("examples.error_handling.handle_rate_exceeded_error.GoogleAdsClient")
    @patch("examples.error_handling.handle_rate_exceeded_error.create_ad_group_criterion_operations")
    @patch("examples.error_handling.handle_rate_exceeded_error.request_mutate_and_display_result")
    @patch("examples.error_handling.handle_rate_exceeded_error.sleep")
    @patch("builtins.print")
    def test_main_fails_after_max_retries(
        self, mock_print, mock_sleep, mock_request_mutate, mock_create_operations, mock_google_ads_client
    ):
        mock_client_instance = MagicMock(spec=GoogleAdsClient)
        mock_google_ads_client.load_from_storage.return_value = mock_client_instance

        # Mock for client.get_type("QuotaErrorEnum").QuotaError
        mock_quota_error_obj = MagicMock()
        mock_quota_error_obj.RESOURCE_EXHAUSTED = "RESOURCE_EXHAUSTED_PLACEHOLDER"
        mock_quota_error_obj.RESOURCE_TEMPORARILY_EXHAUSTED = "RESOURCE_TEMPORARILY_EXHAUSTED_PLACEHOLDER"

        def get_type_side_effect(name): # Renamed from mock_get_type to avoid conflict
            if name == "QuotaErrorEnum":
                return MagicMock(QuotaError=mock_quota_error_obj)
            return MagicMock()
        mock_client_instance.get_type.side_effect = get_type_side_effect

        mock_operations = [MagicMock()]
        mock_create_operations.return_value = mock_operations

        # Simulate RateExceededError repeatedly
        rate_exceeded_error = GoogleAdsException(
            error=MagicMock(),
            failure=MagicMock(errors=[
                MagicMock(error_code=MagicMock(quota_error="RESOURCE_EXHAUSTED_PLACEHOLDER"))
            ]),
            call=MagicMock(),
            request_id="test_req_id_persistent_rate_exceeded"
        )
        mock_request_mutate.side_effect = [rate_exceeded_error] * (NUM_RETRIES + 1)

        mock_args = argparse.Namespace(customer_id="123", ad_group_id="456")

        with patch("argparse.ArgumentParser.parse_args", return_value=mock_args):
            with self.assertRaisesRegex(Exception, f"Could not recover after making {NUM_RETRIES} attempts."):
                main(mock_client_instance, mock_args.customer_id, mock_args.ad_group_id)

        # create_operations is called once for the first request
        self.assertEqual(mock_create_operations.call_count, 1)
        # request_mutate is called NUM_RETRIES times (initial attempt + NUM_RETRIES-1 retries)
        self.assertEqual(mock_request_mutate.call_count, NUM_RETRIES)

        expected_sleep_calls = [call(RETRY_SECONDS * (2**i)) for i in range(NUM_RETRIES)]
        mock_sleep.assert_has_calls(expected_sleep_calls)

    @patch("examples.error_handling.handle_rate_exceeded_error.GoogleAdsClient")
    @patch("examples.error_handling.handle_rate_exceeded_error.create_ad_group_criterion_operations")
    @patch("examples.error_handling.handle_rate_exceeded_error.request_mutate_and_display_result")
    @patch("builtins.print")
    def test_main_handles_non_rate_exceeded_google_ads_exception(
        self, mock_print, mock_request_mutate, mock_create_operations, mock_google_ads_client
    ):
        mock_client_instance = MagicMock(spec=GoogleAdsClient)
        mock_google_ads_client.load_from_storage.return_value = mock_client_instance

        # Mock for client.get_type("QuotaErrorEnum").QuotaError
        mock_quota_error_obj = MagicMock()
        mock_quota_error_obj.OTHER_ERROR = "OTHER_PLACEHOLDER"
        mock_quota_error_obj.UNSPECIFIED = "UNSPECIFIED_PLACEHOLDER"
        # Also need the ones used by the SUT if different from above
        mock_quota_error_obj.RESOURCE_EXHAUSTED = "RESOURCE_EXHAUSTED_PLACEHOLDER"
        mock_quota_error_obj.RESOURCE_TEMPORARILY_EXHAUSTED = "RESOURCE_TEMPORARILY_EXHAUSTED_PLACEHOLDER"


        def get_type_side_effect(name): # Renamed from mock_get_type to avoid conflict
            if name == "QuotaErrorEnum":
                return MagicMock(QuotaError=mock_quota_error_obj)
            return MagicMock()
        mock_client_instance.get_type.side_effect = get_type_side_effect

        mock_operations = [MagicMock()]
        mock_create_operations.return_value = mock_operations

        # Simulate a non-rate-exceeded GoogleAdsException
        other_google_ads_exception = GoogleAdsException(
            error=MagicMock(),
            failure=MagicMock(errors=[
                MagicMock(error_code=MagicMock(quota_error="UNSPECIFIED_PLACEHOLDER")) # Different error
            ]),
            call=MagicMock(),
            request_id="test_req_id_other_error"
        )
        mock_request_mutate.side_effect = other_google_ads_exception

        mock_args = argparse.Namespace(customer_id="123", ad_group_id="456")

        with patch("argparse.ArgumentParser.parse_args", return_value=mock_args):
            with self.assertRaises(GoogleAdsException) as cm:
                main(mock_client_instance, mock_args.customer_id, mock_args.ad_group_id)
            self.assertIs(cm.exception, other_google_ads_exception)

        mock_print.assert_any_call(f"Failed to validate keywords: {other_google_ads_exception}")


if __name__ == "__main__":
    unittest.main()
