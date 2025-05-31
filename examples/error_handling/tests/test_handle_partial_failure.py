import argparse
import unittest
from unittest.mock import MagicMock, patch, call

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

from examples.error_handling.handle_partial_failure import main, print_results, is_partial_failure_error_present


class TestHandlePartialFailure(unittest.TestCase):
    @patch("examples.error_handling.handle_partial_failure.GoogleAdsClient")
    @patch("examples.error_handling.handle_partial_failure.create_ad_groups")
    @patch("examples.error_handling.handle_partial_failure.print_results")
    def test_main_success(
        self, mock_print_results, mock_create_ad_groups, mock_google_ads_client
    ):
        mock_client_instance = MagicMock(spec=GoogleAdsClient)
        mock_google_ads_client.load_from_storage.return_value = mock_client_instance

        mock_ad_group_response = MagicMock()
        mock_create_ad_groups.return_value = mock_ad_group_response

        mock_args = argparse.Namespace(
            customer_id="1234567890", campaign_id="campaign_id_1"
        )

        with patch("argparse.ArgumentParser.parse_args", return_value=mock_args):
            main(mock_client_instance, mock_args.customer_id, mock_args.campaign_id)

        # mock_google_ads_client.load_from_storage.assert_called_once_with(version="v19") # Removed: main is called with an instance
        mock_create_ad_groups.assert_called_once_with(
            mock_client_instance, mock_args.customer_id, mock_args.campaign_id
        )
        mock_print_results.assert_called_once_with(
            mock_client_instance, mock_ad_group_response
        )

    @patch("examples.error_handling.handle_partial_failure.GoogleAdsClient")
    @patch("examples.error_handling.handle_partial_failure.create_ad_groups")
    def test_main_handles_google_ads_exception(
        self, mock_create_ad_groups, mock_google_ads_client
    ):
        mock_client_instance = MagicMock(spec=GoogleAdsClient)
        mock_google_ads_client.load_from_storage.return_value = mock_client_instance

        mock_google_ads_exception = GoogleAdsException(
            error=MagicMock(code=MagicMock(name="TestError")),
            failure=MagicMock(errors=[MagicMock(message="Test message", location=MagicMock(field_path_elements=[MagicMock(field_name="test_field")]))]),
            call=MagicMock(),
            request_id="test_request_id",
        )
        mock_create_ad_groups.side_effect = mock_google_ads_exception

        mock_args = argparse.Namespace(
            customer_id="1234567890", campaign_id="campaign_id_1"
        )

        with patch("argparse.ArgumentParser.parse_args", return_value=mock_args), \
             patch("sys.exit") as mock_sys_exit, \
             patch("builtins.print") as mock_print:
            main(mock_client_instance, mock_args.customer_id, mock_args.campaign_id)
            mock_sys_exit.assert_called_once_with(1)

            # Check if error details are printed
            mock_print.assert_any_call(
                f'Request with ID "{mock_google_ads_exception.request_id}" failed with status '
                f'"{mock_google_ads_exception.error.code().name}" and includes the following errors:'
            )
            mock_print.assert_any_call(f'	Error with message "Test message".')
            mock_print.assert_any_call(f"		On field: test_field")


    def test_is_partial_failure_error_present_true(self):
        mock_response_with_error = MagicMock()
        # Simulate a partial failure error (code is non-zero)
        mock_response_with_error.partial_failure_error = MagicMock(code=1)
        self.assertTrue(is_partial_failure_error_present(mock_response_with_error))

    def test_is_partial_failure_error_present_false(self):
        mock_response_no_error = MagicMock()
        # Simulate no partial failure error (code is zero)
        mock_response_no_error.partial_failure_error = MagicMock(code=0)
        self.assertFalse(is_partial_failure_error_present(mock_response_no_error))

    @patch("builtins.print")
    def test_print_results_with_partial_failure(self, mock_print):
        mock_client = MagicMock(spec=GoogleAdsClient)
        mock_response = MagicMock()

        # Simulate a partial failure error
        mock_response.partial_failure_error = MagicMock(code=1)

        # Mock GoogleAdsFailure deserialization
        mock_failure_message_type = MagicMock()
        mock_client.get_type.return_value = mock_failure_message_type

        mock_deserialized_failure = MagicMock()
        mock_failure_message_type.deserialize.return_value = mock_deserialized_failure

        mock_error = MagicMock()
        mock_error.location.field_path_elements = [MagicMock(index=0)]
        mock_error.message = "Partial failure message"
        mock_error.error_code = "PARTIAL_ERROR_CODE"
        mock_deserialized_failure.errors = [mock_error]

        # Simulate error_details attribute
        mock_error_detail = MagicMock()
        mock_error_detail.value = b"serialized_failure_data"
        mock_response.partial_failure_error.details = [mock_error_detail]

        # Simulate one successful result and one failed (empty) result
        mock_successful_result = MagicMock(resource_name="successful_resource")
        mock_response.results = [mock_successful_result, None]

        print_results(mock_client, mock_response)

        mock_print.assert_any_call("Partial failures occurred. Details will be shown below.\n")
        mock_print.assert_any_call(
            "A partial failure at index 0 occurred "
            "\nError message: Partial failure message\nError code: "
            "PARTIAL_ERROR_CODE"
        )
        mock_print.assert_any_call("Created ad group with resource_name: successful_resource.")
        # Ensure that the empty message (failed operation) is not printed
        self.assertNotIn(call("Created ad group with resource_name: None."), mock_print.call_args_list)


    @patch("builtins.print")
    def test_print_results_no_partial_failure(self, mock_print):
        mock_client = MagicMock(spec=GoogleAdsClient)
        mock_response = MagicMock()
        # Simulate no partial failure error
        mock_response.partial_failure_error = MagicMock(code=0)
        mock_response.results = [MagicMock(resource_name="res1"), MagicMock(resource_name="res2")]

        print_results(mock_client, mock_response)

        mock_print.assert_any_call(
            "All operations completed successfully. No partial failure to show."
        )
        mock_print.assert_any_call("Created ad group with resource_name: res1.")
        mock_print.assert_any_call("Created ad group with resource_name: res2.")


if __name__ == "__main__":
    unittest.main()
