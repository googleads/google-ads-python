import argparse
import unittest
from unittest.mock import MagicMock, patch

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.ads.googleads.v19.enums.types.policy_finding_error import PolicyFindingErrorEnum

from examples.error_handling.handle_responsive_search_ad_policy_violations import main


class TestHandleResponsiveSearchAdPolicyViolations(unittest.TestCase):
    @patch("examples.error_handling.handle_responsive_search_ad_policy_violations.GoogleAdsClient")
    def test_main_success_first_try(self, mock_google_ads_client):
        mock_client_instance = MagicMock(spec=GoogleAdsClient)
        mock_google_ads_client.load_from_storage.return_value = mock_client_instance

        mock_ad_group_ad_service = MagicMock()
        mock_client_instance.get_service.return_value = mock_ad_group_ad_service

        # Simulate successful ad creation on the first try
        mock_ad_group_ad_service.mutate_ad_group_ads.return_value.results = [MagicMock(resource_name="test_ad_resource")]

        mock_args = argparse.Namespace(customer_id="123", ad_group_id="456")

        with patch("argparse.ArgumentParser.parse_args", return_value=mock_args):
            main(mock_client_instance, mock_args.customer_id, mock_args.ad_group_id)

        mock_google_ads_client.load_from_storage.assert_called_once_with(version="v19")
        mock_client_instance.get_service.assert_any_call("AdGroupAdService")
        # Mutate should be called once if successful on first try
        mock_ad_group_ad_service.mutate_ad_group_ads.assert_called_once()

    @patch("examples.error_handling.handle_responsive_search_ad_policy_violations.GoogleAdsClient")
    @patch("examples.error_handling.handle_responsive_search_ad_policy_violations.fetch_ignorable_policy_topics")
    @patch("examples.error_handling.handle_responsive_search_ad_policy_violations.request_exemption")
    def test_main_handles_policy_violation_and_requests_exemption(
        self, mock_request_exemption, mock_fetch_ignorable_policy_topics, mock_google_ads_client
    ):
        mock_client_instance = MagicMock(spec=GoogleAdsClient)
        mock_google_ads_client.load_from_storage.return_value = mock_client_instance

        mock_ad_group_ad_service = MagicMock()
        mock_client_instance.get_service.return_value = mock_ad_group_ad_service

        # Simulate GoogleAdsException with policy finding error on first mutate
        policy_violation_exception = GoogleAdsException(
            error=MagicMock(),
            failure=MagicMock(errors=[
                MagicMock(error_code=MagicMock(policy_finding_error=PolicyFindingErrorEnum.PolicyFindingError.POLICY_FINDING))
            ]),
            request_id="policy_error_req_id"
        )

        # First call to mutate_ad_group_ads raises policy error, second (exemption) succeeds
        mock_ad_group_ad_service.mutate_ad_group_ads.side_effect = [
            policy_violation_exception,
            MagicMock(results=[MagicMock(resource_name="exempted_ad_resource")])
        ]

        mock_fetch_ignorable_policy_topics.return_value = ["topic1", "topic2"]

        mock_args = argparse.Namespace(customer_id="123", ad_group_id="456")

        with patch("argparse.ArgumentParser.parse_args", return_value=mock_args):
            main(mock_client_instance, mock_args.customer_id, mock_args.ad_group_id)

        mock_fetch_ignorable_policy_topics.assert_called_once_with(mock_client_instance, policy_violation_exception)
        mock_request_exemption.assert_called_once()
        # Mutate called twice: once for initial attempt, once for exemption
        self.assertEqual(mock_ad_group_ad_service.mutate_ad_group_ads.call_count, 2)

    @patch("examples.error_handling.handle_responsive_search_ad_policy_violations.GoogleAdsClient")
    @patch("examples.error_handling.handle_responsive_search_ad_policy_violations.fetch_ignorable_policy_topics")
    @patch("examples.error_handling.handle_responsive_search_ad_policy_violations.request_exemption")
    @patch("sys.exit") # Mock sys.exit to check if it's called
    @patch("builtins.print")
    def test_main_handles_google_ads_exception_during_exemption(
        self, mock_print, mock_sys_exit, mock_request_exemption, mock_fetch_ignorable_policy_topics, mock_google_ads_client
    ):
        mock_client_instance = MagicMock(spec=GoogleAdsClient)
        mock_google_ads_client.load_from_storage.return_value = mock_client_instance

        mock_ad_group_ad_service = MagicMock()
        mock_client_instance.get_service.return_value = mock_ad_group_ad_service

        # Simulate GoogleAdsException with policy finding error on first mutate
        policy_violation_exception = GoogleAdsException(
            error=MagicMock(),
            failure=MagicMock(errors=[
                MagicMock(error_code=MagicMock(policy_finding_error=PolicyFindingErrorEnum.PolicyFindingError.POLICY_FINDING))
            ]),
            request_id="policy_error_req_id"
        )

        # Simulate another GoogleAdsException during exemption request
        exemption_failure_exception = GoogleAdsException(
            error=MagicMock(code=MagicMock(name="ExemptionError")), # Add code.name for printing
            failure=MagicMock(errors=[MagicMock(message="Exemption failed", location=MagicMock(field_path_elements=[MagicMock(field_name="ex_field")]))]),
            request_id="exemption_fail_req_id"
        )

        mock_ad_group_ad_service.mutate_ad_group_ads.side_effect = policy_violation_exception
        mock_fetch_ignorable_policy_topics.return_value = ["topic1"]
        mock_request_exemption.side_effect = exemption_failure_exception # Exemption request also fails

        mock_args = argparse.Namespace(customer_id="123", ad_group_id="456")

        with patch("argparse.ArgumentParser.parse_args", return_value=mock_args):
            main(mock_client_instance, mock_args.customer_id, mock_args.ad_group_id)

        mock_fetch_ignorable_policy_topics.assert_called_once_with(mock_client_instance, policy_violation_exception)
        mock_request_exemption.assert_called_once() # Exemption was attempted
        mock_sys_exit.assert_called_once_with(1) # Should exit due to unhandled exception in main

        # Verify that the details of the exemption_failure_exception are printed
        mock_print.assert_any_call(
            f"Request with ID '{exemption_failure_exception.request_id}' failed with status "
            f"'{exemption_failure_exception.error.code().name}' and includes the following errors:"
        )
        mock_print.assert_any_call(f"	Error with message 'Exemption failed'.")
        mock_print.assert_any_call(f"		On field: ex_field")


    @patch("examples.error_handling.handle_responsive_search_ad_policy_violations.GoogleAdsClient")
    @patch("sys.exit") # Mock sys.exit
    @patch("builtins.print")
    def test_main_handles_non_policy_finding_google_ads_exception(
        self, mock_print, mock_sys_exit, mock_google_ads_client
    ):
        mock_client_instance = MagicMock(spec=GoogleAdsClient)
        mock_google_ads_client.load_from_storage.return_value = mock_client_instance

        mock_ad_group_ad_service = MagicMock()
        mock_client_instance.get_service.return_value = mock_ad_group_ad_service

        # Simulate GoogleAdsException that is NOT a policy finding error
        non_policy_exception = GoogleAdsException(
            error=MagicMock(code=MagicMock(name="OtherError")), # Add code.name
            failure=MagicMock(errors=[
                # Ensure not a policy_finding_error
                MagicMock(error_code=MagicMock(policy_finding_error=PolicyFindingErrorEnum.PolicyFindingError.UNSPECIFIED),
                          message="Some other error",
                          location=MagicMock(field_path_elements=[MagicMock(field_name="other_field")]))
            ]),
            request_id="other_error_req_id"
        )

        mock_ad_group_ad_service.mutate_ad_group_ads.side_effect = non_policy_exception

        mock_args = argparse.Namespace(customer_id="123", ad_group_id="456")

        with patch("argparse.ArgumentParser.parse_args", return_value=mock_args):
            main(mock_client_instance, mock_args.customer_id, mock_args.ad_group_id)

        mock_sys_exit.assert_called_once_with(1) # Should exit
        # Verify that the details of the non_policy_exception are printed
        mock_print.assert_any_call(
            f"Request with ID '{non_policy_exception.request_id}' failed with status "
            f"'{non_policy_exception.error.code().name}' and includes the following errors:"
        )
        mock_print.assert_any_call(f"	Error with message 'Some other error'.")
        mock_print.assert_any_call(f"		On field: other_field")


if __name__ == "__main__":
    unittest.main()
