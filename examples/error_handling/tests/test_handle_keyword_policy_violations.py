import argparse
import unittest
from unittest.mock import MagicMock, patch

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

from examples.error_handling.handle_keyword_policy_violations import main


class TestHandleKeywordPolicyViolations(unittest.TestCase):
    @patch("examples.error_handling.handle_keyword_policy_violations.GoogleAdsClient")
    def test_main_success(self, mock_google_ads_client):
        mock_client_instance = MagicMock(spec=GoogleAdsClient)
        mock_google_ads_client.load_from_storage.return_value = mock_client_instance

        mock_ad_group_criterion_service = MagicMock()
        mock_client_instance.get_service.return_value = mock_ad_group_criterion_service

        # Mock successful response from create_keyword_criterion
        mock_ad_group_criterion_service.mutate_ad_group_criteria.return_value.results = [MagicMock(resource_name="test_resource_name")]

        # Mock command line arguments
        mock_args = argparse.Namespace(
            customer_id="1234567890",
            ad_group_id="0987654321",
            keyword_text="test keyword"
        )

        with patch("argparse.ArgumentParser.parse_args", return_value=mock_args):
            main(mock_client_instance, mock_args.customer_id, mock_args.ad_group_id, mock_args.keyword_text)

        mock_google_ads_client.load_from_storage.assert_called_once_with(version="v19")
        mock_client_instance.get_service.assert_any_call("AdGroupCriterionService")
        mock_ad_group_criterion_service.mutate_ad_group_criteria.assert_called()

    @patch("examples.error_handling.handle_keyword_policy_violations.GoogleAdsClient")
    @patch("examples.error_handling.handle_keyword_policy_violations.fetch_exempt_policy_violation_keys")
    @patch("examples.error_handling.handle_keyword_policy_violations.request_exemption")
    def test_main_handles_google_ads_exception_and_requests_exemption(
        self, mock_request_exemption, mock_fetch_exempt_policy_violation_keys, mock_google_ads_client
    ):
        mock_client_instance = MagicMock(spec=GoogleAdsClient)
        mock_google_ads_client.load_from_storage.return_value = mock_client_instance

        mock_ad_group_criterion_service = MagicMock()
        mock_client_instance.get_service.return_value = mock_ad_group_criterion_service

        # Simulate GoogleAdsException during the first attempt to create keyword
        mock_google_ads_exception = GoogleAdsException(
            error=MagicMock(),
            failure=MagicMock(),
            request_id="test_request_id"
        )
        mock_ad_group_criterion_service.mutate_ad_group_criteria.side_effect = [
            mock_google_ads_exception, # First call raises exception
            MagicMock(results=[MagicMock(resource_name="test_resource_name_after_exemption")]) # Second call (after exemption) succeeds
        ]

        # Mock return value for fetching policy violation keys
        mock_fetch_exempt_policy_violation_keys.return_value = [MagicMock()]

        # Mock command line arguments
        mock_args = argparse.Namespace(
            customer_id="1234567890",
            ad_group_id="0987654321",
            keyword_text="test keyword with policy violation"
        )

        with patch("argparse.ArgumentParser.parse_args", return_value=mock_args):
            main(mock_client_instance, mock_args.customer_id, mock_args.ad_group_id, mock_args.keyword_text)

        mock_google_ads_client.load_from_storage.assert_called_once_with(version="v19")
        mock_fetch_exempt_policy_violation_keys.assert_called_once_with(mock_google_ads_exception)
        mock_request_exemption.assert_called_once()

    @patch("examples.error_handling.handle_keyword_policy_violations.GoogleAdsClient")
    @patch("examples.error_handling.handle_keyword_policy_violations.fetch_exempt_policy_violation_keys")
    @patch("examples.error_handling.handle_keyword_policy_violations.request_exemption")
    def test_main_handles_google_ads_exception_during_exemption_request(
        self, mock_request_exemption, mock_fetch_exempt_policy_violation_keys, mock_google_ads_client
    ):
        mock_client_instance = MagicMock(spec=GoogleAdsClient)
        mock_google_ads_client.load_from_storage.return_value = mock_client_instance

        mock_ad_group_criterion_service = MagicMock()
        mock_client_instance.get_service.return_value = mock_ad_group_criterion_service

        # Simulate GoogleAdsException during the first attempt
        mock_google_ads_exception_initial = GoogleAdsException(
            error=MagicMock(),
            failure=MagicMock(),
            request_id="test_request_id_initial"
        )
        # Simulate GoogleAdsException during the exemption request
        mock_google_ads_exception_exemption = GoogleAdsException(
            error=MagicMock(),
            failure=MagicMock(errors=[MagicMock(message=MagicMock())]), # Add errors attribute
            request_id="test_request_id_exemption"
        )

        mock_ad_group_criterion_service.mutate_ad_group_criteria.side_effect = mock_google_ads_exception_initial
        mock_fetch_exempt_policy_violation_keys.return_value = [MagicMock()]
        mock_request_exemption.side_effect = mock_google_ads_exception_exemption


        # Mock command line arguments
        mock_args = argparse.Namespace(
            customer_id="1234567890",
            ad_group_id="0987654321",
            keyword_text="test keyword"
        )

        with patch("argparse.ArgumentParser.parse_args", return_value=mock_args), \
             patch("sys.exit") as mock_sys_exit: # Mock sys.exit
            main(mock_client_instance, mock_args.customer_id, mock_args.ad_group_id, mock_args.keyword_text)
            mock_sys_exit.assert_called_once_with(1) # Assert that sys.exit(1) was called

        mock_fetch_exempt_policy_violation_keys.assert_called_once_with(mock_google_ads_exception_initial)
        mock_request_exemption.assert_called_once()


if __name__ == "__main__":
    unittest.main()
