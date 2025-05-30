import os
import sys
import unittest
from unittest.mock import patch, MagicMock
import io
import argparse
from contextlib import redirect_stdout

# Determine the correct paths
SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

import list_accessible_customers # Script to test
from google.ads.googleads.errors import GoogleAdsException
from google.ads.googleads.v19.services.types.customer_service import ListAccessibleCustomersResponse

class TestListAccessibleCustomers(unittest.TestCase):

    @patch("list_accessible_customers.GoogleAdsClient.load_from_storage")
    def test_main_success(self, mock_load_from_storage):
        mock_ads_client = MagicMock()
        mock_load_from_storage.return_value = mock_ads_client

        mock_customer_service = MagicMock()
        mock_ads_client.get_service.return_value = mock_customer_service

        # Prepare mock response
        mock_response = ListAccessibleCustomersResponse()
        mock_response.resource_names.extend(["customers/12345", "customers/67890"])
        mock_customer_service.list_accessible_customers.return_value = mock_response

        stdout_capture = io.StringIO()
        with redirect_stdout(stdout_capture):
            # The main function in list_accessible_customers.py takes the client as an argument.
            list_accessible_customers.main(mock_ads_client)

        output = stdout_capture.getvalue()

        mock_ads_client.get_service.assert_called_once_with("CustomerService")
        mock_customer_service.list_accessible_customers.assert_called_once()

        self.assertIn("customers/12345", output)
        self.assertIn("customers/67890", output)
        self.assertIn("Total results: 2", output)

    @patch("argparse.ArgumentParser") # To control args if __main__ block uses them
    @patch("list_accessible_customers.GoogleAdsClient.load_from_storage")
    @patch("sys.exit")
    def test_main_block_google_ads_exception(self, mock_sys_exit, mock_load_from_storage, MockArgumentParser):
        mock_ads_client = MagicMock()
        mock_load_from_storage.return_value = mock_ads_client

        mock_customer_service = MagicMock()
        mock_ads_client.get_service.return_value = mock_customer_service

        # Configure argparse mock if needed by the script's __main__
        # list_accessible_customers.py __main__ doesn't parse specific args for main()
        mock_args = argparse.Namespace() # No specific args needed for this script
        MockArgumentParser.return_value.parse_args.return_value = mock_args

        # Configure the exception
        mock_google_ads_error_obj = MagicMock()
        mock_error_code_obj = MagicMock()
        mock_error_code_obj.name = "UNAUTHENTICATED"
        mock_google_ads_error_obj.code.return_value = mock_error_code_obj
        mock_failure_obj = MagicMock()
        mock_error_detail_item = MagicMock()
        mock_error_detail_item.message = "User authentication failed."
        mock_error_detail_item.location.field_path_elements = []
        mock_failure_obj.errors = [mock_error_detail_item]
        ga_exception = GoogleAdsException(
            error=mock_google_ads_error_obj, failure=mock_failure_obj, request_id="req_auth_failed_list", call=None
        )
        mock_customer_service.list_accessible_customers.side_effect = ga_exception

        stdout_capture = io.StringIO()
        with redirect_stdout(stdout_capture):
            # Simulate the __main__ block execution of list_accessible_customers.py
            try:
                # Script's __main__ loads client
                client_main = list_accessible_customers.GoogleAdsClient.load_from_storage(version="v19")
                # Script's __main__ calls main()
                list_accessible_customers.main(client_main)
            except GoogleAdsException as ex_handled:
                # Script's __main__ prints error and exits
                print(
                    f'Request with ID "{ex_handled.request_id}" failed with status '
                    f'"{ex_handled.error.code().name}" and includes the following errors:'
                )
                for err_item in ex_handled.failure.errors:
                    print(f'	Error with message "{err_item.message}".')
                    if err_item.location:
                        for fpe_item in err_item.location.field_path_elements:
                            print(f"		On field: {fpe_item.field_name}")
                mock_sys_exit(1)
            except Exception as e_unhandled:
                self.fail(f"Unexpected exception: {e_unhandled}")

        output = stdout_capture.getvalue()

        mock_load_from_storage.assert_called_once_with(version="v19")
        mock_customer_service.list_accessible_customers.assert_called_once()
        self.assertIn('Request with ID "req_auth_failed_list" failed with status "UNAUTHENTICATED"', output)
        self.assertIn('	Error with message "User authentication failed."', output)
        mock_sys_exit.assert_called_once_with(1)

if __name__ == "__main__":
    unittest.main()
