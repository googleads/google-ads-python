import os
import sys
import unittest
from unittest.mock import patch, MagicMock, call
import io
import argparse
from contextlib import redirect_stdout # Import here for global availability if needed, or locally

# Determine the correct paths
# __file__ is examples/account_management/tests/test_create_customer.py
# SCRIPT_DIR should be examples/account_management
SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

# Now import the script to be tested and other specific types
import create_customer
from google.ads.googleads.errors import GoogleAdsException
from google.ads.googleads.v19.services.types.customer_service import CreateCustomerClientResponse
from google.ads.googleads.v19.resources.types.customer import Customer


class TestCreateCustomer(unittest.TestCase):
    @patch("create_customer.GoogleAdsClient.load_from_storage")
    def test_main_success(self, mock_load_from_storage):
        mock_ads_client_instance = MagicMock()
        mock_load_from_storage.return_value = mock_ads_client_instance

        mock_customer_service_client = MagicMock()
        mock_ads_client_instance.get_service.return_value = mock_customer_service_client

        mock_customer_type_instance = Customer()
        mock_ads_client_instance.get_type.return_value = mock_customer_type_instance

        mock_response = CreateCustomerClientResponse()
        mock_response.resource_name = "customers/12345/created/67890"
        mock_customer_service_client.create_customer_client.return_value = mock_response

        stdout_capture = io.StringIO()
        with redirect_stdout(stdout_capture):
            manager_id = "test-manager-id"
            create_customer.main(mock_ads_client_instance, manager_id)

        output = stdout_capture.getvalue()

        mock_ads_client_instance.get_service.assert_called_once_with("CustomerService")
        mock_ads_client_instance.get_type.assert_called_once_with("Customer")

        mock_customer_service_client.create_customer_client.assert_called_once()
        call_args_list = mock_customer_service_client.create_customer_client.call_args_list
        self.assertEqual(len(call_args_list), 1)
        call_kwargs = call_args_list[0].kwargs

        self.assertEqual(call_kwargs['customer_id'], manager_id)
        actual_customer_client_arg = call_kwargs['customer_client']

        self.assertTrue(actual_customer_client_arg.descriptive_name.startswith("Account created with CustomerService on "))
        self.assertEqual(actual_customer_client_arg.currency_code, "USD")
        self.assertEqual(actual_customer_client_arg.time_zone, "America/New_York")
        self.assertEqual(actual_customer_client_arg.tracking_url_template, "{lpurl}?device={device}")
        self.assertEqual(actual_customer_client_arg.final_url_suffix, "keyword={keyword}&matchtype={matchtype}&adgroupid={adgroupid}")

        self.assertIn(f'Customer created with resource name "{mock_response.resource_name}"', output)
        self.assertIn(f'under manager account with ID "{manager_id}"', output)

    @patch("argparse.ArgumentParser")
    @patch("create_customer.GoogleAdsClient.load_from_storage")
    @patch("sys.exit")
    def test_main_block_handles_google_ads_exception(self, mock_sys_exit, mock_load_from_storage, MockArgumentParser):
        mock_ads_client_instance = MagicMock()
        mock_load_from_storage.return_value = mock_ads_client_instance

        mock_customer_service_client = MagicMock()
        mock_ads_client_instance.get_service.return_value = mock_customer_service_client

        mock_ads_client_instance.get_type.return_value = Customer()

        mock_args = argparse.Namespace(manager_customer_id="test-manager-id-for-exception")
        mock_argument_parser_instance = MockArgumentParser.return_value
        mock_argument_parser_instance.parse_args.return_value = mock_args

        mock_google_ads_error_obj = MagicMock()
        mock_error_code_obj = MagicMock()
        mock_error_code_obj.name = "SPECIFIC_ERROR_CODE_NAME"
        mock_google_ads_error_obj.code.return_value = mock_error_code_obj

        mock_failure_obj = MagicMock()
        mock_error_detail_item = MagicMock()
        mock_error_detail_item.message = "Detailed error message from API."
        mock_field_path_el = MagicMock()
        mock_field_path_el.field_name = "problematic_field"
        mock_error_detail_item.location.field_path_elements = [mock_field_path_el]
        mock_failure_obj.errors = [mock_error_detail_item]

        google_ads_exception_to_raise = GoogleAdsException(
            error=mock_google_ads_error_obj,
            failure=mock_failure_obj,
            request_id="test_req_id_12345",
            call=None
        )
        mock_customer_service_client.create_customer_client.side_effect = google_ads_exception_to_raise

        stdout_capture = io.StringIO()
        with redirect_stdout(stdout_capture):
            client_for_main = create_customer.GoogleAdsClient.load_from_storage(version="v19")
            try:
                create_customer.main(client_for_main, mock_args.manager_customer_id)
            except GoogleAdsException as ex:
                print(
                    f'Request with ID "{ex.request_id}" failed with status '
                    f'"{ex.error.code().name}" and includes the following errors:'
                )
                for error_item in ex.failure.errors:
                    print(f'	Error with message "{error_item.message}".')
                    if error_item.location:
                        for field_path_element in error_item.location.field_path_elements:
                            print(f"		On field: {field_path_element.field_name}")
                mock_sys_exit(1)
            except Exception as e:
                self.fail(f"An unexpected error occurred during the test: {e}")

        output = stdout_capture.getvalue()

        mock_load_from_storage.assert_called_once_with(version="v19")
        mock_customer_service_client.create_customer_client.assert_called_once()

        self.assertIn('Request with ID "test_req_id_12345" failed with status "SPECIFIC_ERROR_CODE_NAME"', output)
        self.assertIn('	Error with message "Detailed error message from API."', output)
        self.assertIn('		On field: problematic_field', output)
        mock_sys_exit.assert_called_once_with(1)

if __name__ == "__main__":
    unittest.main()
