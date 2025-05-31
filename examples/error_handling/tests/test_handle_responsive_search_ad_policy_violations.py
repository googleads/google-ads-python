import argparse
import unittest
from unittest.mock import MagicMock, patch

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
# PolicyFindingErrorEnum import removed as it's obtained via client.get_type

from examples.error_handling.handle_responsive_search_ad_policy_violations import main


class TestHandleResponsiveSearchAdPolicyViolations(unittest.TestCase):
    @patch("examples.error_handling.handle_responsive_search_ad_policy_violations.GoogleAdsClient")
    def test_main_success_first_try(self, mock_google_ads_client):
        mock_client_instance = MagicMock(spec=GoogleAdsClient)
        mock_google_ads_client.load_from_storage.return_value = mock_client_instance

        # Setup mock for client.enums
        mock_enums_container = MagicMock()
        mock_enums_container.AdGroupAdStatusEnum.PAUSED = "PAUSED_MOCK_STATUS"
        mock_client_instance.enums = mock_enums_container

        mock_ad_group_ad_service = MagicMock()
        mock_client_instance.get_service.return_value = mock_ad_group_ad_service

        # Simulate successful ad creation on the first try
        mock_ad_group_ad_service.mutate_ad_group_ads.return_value.results = [MagicMock(resource_name="test_ad_resource")]

        mock_args = argparse.Namespace(customer_id="123", ad_group_id="456")

        with patch("argparse.ArgumentParser.parse_args", return_value=mock_args):
            main(mock_client_instance, mock_args.customer_id, mock_args.ad_group_id)

        # mock_google_ads_client.load_from_storage.assert_called_once_with(version="v19") # Removed: main is called with an instance
        mock_client_instance.get_service.assert_any_call("AdGroupAdService")
        # Mutate is called twice due to unconditional call to request_exemption
        self.assertEqual(mock_ad_group_ad_service.mutate_ad_group_ads.call_count, 2)

    @patch("examples.error_handling.handle_responsive_search_ad_policy_violations.GoogleAdsClient")
    @patch("examples.error_handling.handle_responsive_search_ad_policy_violations.fetch_ignorable_policy_topics")
    # Removed @patch("examples.error_handling.handle_responsive_search_ad_policy_violations.request_exemption")
    def test_main_handles_policy_violation_and_requests_exemption(
        self, mock_fetch_ignorable_policy_topics, mock_google_ads_client # mock_request_exemption removed
    ):
        mock_client_instance = MagicMock(spec=GoogleAdsClient)
        mock_google_ads_client.load_from_storage.return_value = mock_client_instance

        # Setup mock for client.enums
        mock_enums_container = MagicMock()
        mock_enums_container.AdGroupAdStatusEnum.PAUSED = "PAUSED_MOCK_STATUS"
        mock_client_instance.enums = mock_enums_container

        mock_ad_group_ad_service = MagicMock()
        mock_client_instance.get_service.return_value = mock_ad_group_ad_service

        # Mock for client.get_type("PolicyFindingErrorEnum").PolicyFindingError
        mock_pfe_object = MagicMock()
        mock_pfe_object.POLICY_FINDING = "POLICY_FINDING_PLACEHOLDER"
        mock_pfe_object.UNSPECIFIED = "UNSPECIFIED_PLACEHOLDER"

        # Existing mock_ad_group_ad_service from the test setup
        # We need to make sure get_type and get_service can coexist on mock_client_instance
        def get_type_or_service_side_effect(name_or_service):
            if name_or_service == "PolicyFindingErrorEnum":
                return MagicMock(PolicyFindingError=mock_pfe_object)
            # Assuming get_service is called with service name string by SUT
            # This part might need adjustment if mock_ad_group_ad_service is expected from client.get_service()
            # For now, let's assume client.get_service() is already correctly mocked by the @patch for GoogleAdsClient
            # and we only need to care about get_type here for PolicyFindingErrorEnum
            return MagicMock() # Default for other get_type calls

        mock_client_instance.get_type.side_effect = get_type_or_service_side_effect
        # If get_service is part of the client instance directly (not from get_type)
        # and mock_client_instance is the one passed to main,
        # then mock_client_instance.get_service should already be the mock_ad_group_ad_service.
        # The @patch decorator for GoogleAdsClient makes mock_google_ads_client the class.
        # mock_client_instance is mock_google_ads_client.load_from_storage.return_value.
        # So, mock_client_instance.get_service is already a MagicMock.
        # We need to ensure it returns mock_ad_group_ad_service when called with "AdGroupAdService".
        # This is typically done in the test setup already by:
        # mock_client_instance.get_service.return_value = mock_ad_group_ad_service
        # Let's ensure this is clear or refine if needed. The provided snippet focuses on get_type.

        # Simulate GoogleAdsException with policy finding error on first mutate
        policy_violation_exception = GoogleAdsException(
            error=MagicMock(),
            failure=MagicMock(errors=[
                MagicMock(error_code=MagicMock(policy_finding_error="POLICY_FINDING_PLACEHOLDER"))
            ]),
            call=MagicMock(),
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
        # mock_request_exemption.assert_called_once() # request_exemption is no longer mocked
        # Mutate called twice: once for initial attempt, once for exemption (inside actual request_exemption)
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

        # Setup mock for client.enums
        mock_enums_container = MagicMock()
        mock_enums_container.AdGroupAdStatusEnum.PAUSED = "PAUSED_MOCK_STATUS"
        mock_client_instance.enums = mock_enums_container

        mock_ad_group_ad_service = MagicMock()
        mock_client_instance.get_service.return_value = mock_ad_group_ad_service

        # Mock for client.get_type("PolicyFindingErrorEnum").PolicyFindingError
        mock_pfe_object = MagicMock()
        mock_pfe_object.POLICY_FINDING = "POLICY_FINDING_PLACEHOLDER"
        # No UNSPECIFIED needed here for this specific test's exception

        def get_type_or_service_side_effect(name_or_service):
            if name_or_service == "PolicyFindingErrorEnum":
                return MagicMock(PolicyFindingError=mock_pfe_object)
            return MagicMock()
        mock_client_instance.get_type.side_effect = get_type_or_service_side_effect
        # mock_client_instance.get_service setup assumed to be handled by existing mocks

        # Simulate GoogleAdsException with policy finding error on first mutate
        policy_violation_exception = GoogleAdsException(
            error=MagicMock(),
            failure=MagicMock(errors=[
                MagicMock(error_code=MagicMock(policy_finding_error="POLICY_FINDING_PLACEHOLDER"))
            ]),
            call=MagicMock(),
            request_id="policy_error_req_id"
        )

        # Simulate another GoogleAdsException during exemption request
        exemption_failure_exception = GoogleAdsException(
            error=MagicMock(code=MagicMock(name="ExemptionError")), # Add code.name for printing
            failure=MagicMock(errors=[MagicMock(message="Exemption failed", location=MagicMock(field_path_elements=[MagicMock(field_name="ex_field")]))]),
            call=MagicMock(),
            request_id="exemption_fail_req_id"
        )

        mock_ad_group_ad_service.mutate_ad_group_ads.side_effect = policy_violation_exception
        mock_fetch_ignorable_policy_topics.return_value = ["topic1"]
        mock_request_exemption.side_effect = exemption_failure_exception # Exemption request also fails

        mock_args = argparse.Namespace(customer_id="123", ad_group_id="456")

        with patch("argparse.ArgumentParser.parse_args", return_value=mock_args):
            # Expect GoogleAdsException to be raised from main
            with self.assertRaises(GoogleAdsException) as cm:
                main(mock_client_instance, mock_args.customer_id, mock_args.ad_group_id)
            self.assertEqual(cm.exception, exemption_failure_exception) # Check it's the one from request_exemption

        mock_fetch_ignorable_policy_topics.assert_called_once_with(mock_client_instance, policy_violation_exception)
        mock_request_exemption.assert_called_once() # Exemption was attempted
        # sys.exit and print assertions removed as main() raises the exception,
        # and the script's own exception printing/exit is not part of main()'s direct behavior when called as a function.


    @patch("examples.error_handling.handle_responsive_search_ad_policy_violations.GoogleAdsClient")
    @patch("sys.exit") # Mock sys.exit
    @patch("builtins.print")
    def test_main_handles_non_policy_finding_google_ads_exception(
        self, mock_print, mock_sys_exit, mock_google_ads_client
    ):
        mock_client_instance = MagicMock(spec=GoogleAdsClient)
        mock_google_ads_client.load_from_storage.return_value = mock_client_instance

        # Setup mock for client.enums
        mock_enums_container = MagicMock()
        mock_enums_container.AdGroupAdStatusEnum.PAUSED = "PAUSED_MOCK_STATUS"
        mock_client_instance.enums = mock_enums_container

        mock_ad_group_ad_service = MagicMock()
        mock_client_instance.get_service.return_value = mock_ad_group_ad_service

        # Mock for client.get_type("PolicyFindingErrorEnum").PolicyFindingError
        mock_pfe_object = MagicMock()
        mock_pfe_object.POLICY_FINDING = "POLICY_FINDING_PLACEHOLDER" # Not used by this exception but good for consistency
        mock_pfe_object.UNSPECIFIED = "UNSPECIFIED_PLACEHOLDER"

        def get_type_or_service_side_effect(name_or_service):
            if name_or_service == "PolicyFindingErrorEnum":
                return MagicMock(PolicyFindingError=mock_pfe_object)
            return MagicMock()
        mock_client_instance.get_type.side_effect = get_type_or_service_side_effect
        # mock_client_instance.get_service setup assumed to be handled by existing mocks

        # Simulate GoogleAdsException that is NOT a policy finding error
        non_policy_exception = GoogleAdsException(
            error=MagicMock(code=MagicMock(name="OtherError")), # Add code.name
            failure=MagicMock(errors=[
                # Ensure not a policy_finding_error
                MagicMock(error_code=MagicMock(policy_finding_error="UNSPECIFIED_PLACEHOLDER"),
                          message="Some other error",
                          location=MagicMock(field_path_elements=[MagicMock(field_name="other_field")]))
            ]),
            call=MagicMock(),
            request_id="other_error_req_id"
        )

        mock_ad_group_ad_service.mutate_ad_group_ads.side_effect = non_policy_exception

        mock_args = argparse.Namespace(customer_id="123", ad_group_id="456")

        with patch("argparse.ArgumentParser.parse_args", return_value=mock_args):
            # Expect GoogleAdsException to be raised from main
            with self.assertRaises(GoogleAdsException) as cm:
                main(mock_client_instance, mock_args.customer_id, mock_args.ad_group_id)
            self.assertEqual(cm.exception, non_policy_exception)
        # Print assertions removed as main() raises the exception.


if __name__ == "__main__":
    unittest.main()
