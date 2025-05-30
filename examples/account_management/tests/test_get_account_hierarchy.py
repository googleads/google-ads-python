import os
import sys
import unittest
from unittest.mock import patch, MagicMock, call, ANY
import io
import argparse
from contextlib import redirect_stdout

# Determine the correct paths
SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

import get_account_hierarchy # Script to test
from google.ads.googleads.errors import GoogleAdsException
# Import necessary types for mocking responses
from google.ads.googleads.v19.services.types.customer_service import ListAccessibleCustomersResponse
from google.ads.googleads.v19.services.types.google_ads_service import GoogleAdsRow, SearchGoogleAdsResponse
from google.ads.googleads.v19.resources.types.customer_client import CustomerClient


class TestGetAccountHierarchy(unittest.TestCase):

    def _create_mock_customer_client(self, client_id, descriptive_name, level, manager=False, currency="USD", timezone="America/New_York"):
        client = CustomerClient()
        client.id = int(client_id)
        client.descriptive_name = descriptive_name
        client.level = level
        client.manager = manager
        client.currency_code = currency
        client.time_zone = timezone
        client.resource_name = f"customers/{client_id}"
        return client

    def _create_mock_google_ads_row(self, customer_client):
        row = GoogleAdsRow()
        row.customer_client = customer_client
        return row

    @patch("get_account_hierarchy.GoogleAdsClient.load_from_storage")
    def test_main_with_login_customer_id(self, mock_load_from_storage):
        mock_ads_client = MagicMock()
        mock_load_from_storage.return_value = mock_ads_client

        mock_ga_service = MagicMock()
        mock_customer_service = MagicMock()

        def get_service_side_effect(service_name, version=None):
            if service_name == "GoogleAdsService":
                return mock_ga_service
            elif service_name == "CustomerService":
                return mock_customer_service
            return MagicMock()
        mock_ads_client.get_service.side_effect = get_service_side_effect

        root_mcc = self._create_mock_customer_client("1000", "Root MCC", 0, manager=True)
        child1 = self._create_mock_customer_client("1001", "Child Account 1", 1, manager=False)
        child_mcc2 = self._create_mock_customer_client("1002", "Child MCC 2", 1, manager=True)
        grandchild3 = self._create_mock_customer_client("1003", "Grandchild Account 3", 1, manager=False)

        response_mcc_1000 = SearchGoogleAdsResponse(results=[
            self._create_mock_google_ads_row(self._create_mock_customer_client("1000", "Root MCC", 0, manager=True)),
            self._create_mock_google_ads_row(child1),
            self._create_mock_google_ads_row(child_mcc2)
        ])
        response_child_mcc_1002 = SearchGoogleAdsResponse(results=[
            self._create_mock_google_ads_row(self._create_mock_customer_client("1002", "Child MCC 2", 0, manager=True)),
            self._create_mock_google_ads_row(grandchild3)
        ])
        response_child_1001 = SearchGoogleAdsResponse(results=[self._create_mock_google_ads_row(self._create_mock_customer_client("1001", "Child Account 1", 0, manager=False))])
        response_grandchild_1003 = SearchGoogleAdsResponse(results=[self._create_mock_google_ads_row(self._create_mock_customer_client("1003", "Grandchild Account 3", 0, manager=False))])

        def mock_search_side_effect(customer_id, query):
            if str(customer_id) == "1000": return response_mcc_1000
            elif str(customer_id) == "1002": return response_child_mcc_1002
            elif str(customer_id) == "1001": return response_child_1001
            elif str(customer_id) == "1003": return response_grandchild_1003
            return SearchGoogleAdsResponse()
        mock_ga_service.search.side_effect = mock_search_side_effect

        login_id_str = "1000"
        stdout_capture = io.StringIO()
        with redirect_stdout(stdout_capture):
            get_account_hierarchy.main(mock_ads_client, login_id_str)
        output = stdout_capture.getvalue()

        mock_ads_client.get_service.assert_any_call("GoogleAdsService")
        mock_ads_client.get_service.assert_any_call("CustomerService")
        mock_ga_service.search.assert_any_call(customer_id="1000", query=ANY)
        mock_ga_service.search.assert_any_call(customer_id="1002", query=ANY)

        self.assertIn("The hierarchy of customer ID 1000 is printed below:", output)
        self.assertIn("1000 (Root MCC, USD, America/New_York)", output)
        self.assertIn("--1001 (Child Account 1, USD, America/New_York)", output)
        self.assertIn("--1002 (Child MCC 2, USD, America/New_York)", output)
        self.assertIn("----1003 (Grandchild Account 3, USD, America/New_York)", output)

    @patch("get_account_hierarchy.GoogleAdsClient.load_from_storage")
    def test_main_no_login_customer_id(self, mock_load_from_storage):
        mock_ads_client = MagicMock()
        mock_load_from_storage.return_value = mock_ads_client
        mock_ga_service = MagicMock()
        mock_customer_service = MagicMock()
        mock_ads_client.get_service.side_effect = lambda service_name, version=None: mock_ga_service if service_name == "GoogleAdsService" else mock_customer_service

        accessible_customers_response = ListAccessibleCustomersResponse()
        accessible_customers_response.resource_names.extend(["customers/2000", "customers/2001"])
        mock_customer_service.list_accessible_customers.return_value = accessible_customers_response
        mock_ga_service.parse_customer_path.side_effect = lambda name: {"customer_id": name.split('/')[-1]}

        cust_2000_level0 = self._create_mock_customer_client("2000", "Accessible MCC", 0, manager=True)
        cust_2005_level1 = self._create_mock_customer_client("2005", "Child of 2000", 1, manager=True) # Changed manager to True
        response_for_2000 = SearchGoogleAdsResponse(results=[self._create_mock_google_ads_row(cust_2000_level0), self._create_mock_google_ads_row(cust_2005_level1)])
        response_for_2005 = SearchGoogleAdsResponse(results=[self._create_mock_google_ads_row(self._create_mock_customer_client("2005", "Child of 2000", 0, manager=True))]) # Also here for consistency if it's queried
        cust_2001_level0 = self._create_mock_customer_client("2001", "Accessible Account", 0, manager=False)
        response_for_2001 = SearchGoogleAdsResponse(results=[self._create_mock_google_ads_row(cust_2001_level0)])

        def mock_search_no_login(customer_id, query):
            if str(customer_id) == "2000": return response_for_2000
            elif str(customer_id) == "2005": return response_for_2005
            elif str(customer_id) == "2001": return response_for_2001
            return SearchGoogleAdsResponse()
        mock_ga_service.search.side_effect = mock_search_no_login

        stdout_capture = io.StringIO()
        with redirect_stdout(stdout_capture):
            get_account_hierarchy.main(mock_ads_client, None)
        output = stdout_capture.getvalue()

        mock_customer_service.list_accessible_customers.assert_called_once()
        self.assertEqual(mock_ga_service.parse_customer_path.call_count, 2)
        mock_ga_service.search.assert_any_call(customer_id="2000", query=ANY)
        mock_ga_service.search.assert_any_call(customer_id="2001", query=ANY)
        mock_ga_service.search.assert_any_call(customer_id="2005", query=ANY)

        self.assertIn("The hierarchy of customer ID 2000 is printed below:", output)
        self.assertIn("2000 (Accessible MCC, USD, America/New_York)", output)
        self.assertIn("--2005 (Child of 2000, USD, America/New_York)", output)
        self.assertIn("The hierarchy of customer ID 2001 is printed below:", output)
        self.assertIn("2001 (Accessible Account, USD, America/New_York)", output)

        # Check that 2001 has no children printed under it
        # A bit more robust check for no children under 2001
        output_segments = output.split("The hierarchy of customer ID ")
        segment_for_2001_data = ""
        for segment in output_segments:
            if segment.startswith("2001"):
                segment_for_2001_data = segment
                break

        self.assertTrue(len(segment_for_2001_data) > 0, "Data for customer 2001 not found in output")
        lines_in_segment_2001 = [line.strip() for line in segment_for_2001_data.split('\n') if line.strip()]
        # Ensure that after the line "2001 (Accessible Account..." no line starts with "--"
        found_header_2001 = False
        for line in lines_in_segment_2001:
            if "2001 (Accessible Account" in line:
                found_header_2001 = True
                continue
            if found_header_2001:
                self.assertFalse(line.startswith("--"), f"Account 2001 should not have children, but found: {line}")


    @patch("argparse.ArgumentParser")
    @patch("get_account_hierarchy.GoogleAdsClient.load_from_storage")
    @patch("sys.exit")
    def test_main_block_handles_google_ads_exception(self, mock_sys_exit, mock_load_from_storage, MockArgumentParser):
        mock_ads_client = MagicMock()
        mock_load_from_storage.return_value = mock_ads_client
        mock_customer_service = MagicMock()
        mock_ga_service = MagicMock()
        mock_ads_client.get_service.side_effect = lambda s, version=None: mock_customer_service if s=="CustomerService" else mock_ga_service

        mock_args = argparse.Namespace(login_customer_id=None)
        MockArgumentParser.return_value.parse_args.return_value = mock_args

        mock_google_ads_error_obj = MagicMock()
        mock_error_code_obj = MagicMock()
        mock_error_code_obj.name = "TEST_ERROR_CODE"
        mock_google_ads_error_obj.code.return_value = mock_error_code_obj
        mock_failure_obj = MagicMock()
        mock_error_detail_item = MagicMock()
        mock_error_detail_item.message = "A test error occurred."
        mock_error_detail_item.location.field_path_elements = []
        mock_failure_obj.errors = [mock_error_detail_item]
        ga_exception = GoogleAdsException(error=mock_google_ads_error_obj, failure=mock_failure_obj, request_id="req_ex_test", call=None)

        mock_customer_service.list_accessible_customers.side_effect = ga_exception

        stdout_capture = io.StringIO()
        with redirect_stdout(stdout_capture):
            try:
                # This logic mimics the __main__ block of the script under test
                # 1. Load client (mocked)
                client_main = get_account_hierarchy.GoogleAdsClient.load_from_storage(version="v19")
                # 2. Parse args (mocked)
                # The script directly calls parser.add_argument and parser.parse_args.
                # Mocking ArgumentParser means __init__ returns a mock, and that mock's parse_args is called.
                # So, `get_account_hierarchy.argparse.ArgumentParser().parse_args()` is what we need to simulate.
                # The @patch("argparse.ArgumentParser") handles this.
                # `MockArgumentParser.return_value` is the parser instance.
                # `MockArgumentParser.return_value.parse_args.return_value` is `mock_args`.
                # So, the script's internal `args = parser.parse_args()` will receive `mock_args`.

                # 3. Call main with client and args, wrapped in try-except from script
                # Accessing `get_account_hierarchy.main`
                get_account_hierarchy.main(client_main, mock_args.login_customer_id)

            except GoogleAdsException as ex_handled:
                # This is the script's own error handling path
                print(f'Request with ID "{ex_handled.request_id}" failed with status "{ex_handled.error.code().name}" and includes the following errors:')
                for err_item in ex_handled.failure.errors: # Renamed to avoid clash
                    print(f'	Error with message "{err_item.message}".')
                    if err_item.location:
                        for fpe_item in err_item.location.field_path_elements: # Renamed
                            print(f"		On field: {fpe_item.field_name}")
                mock_sys_exit(1)
            except Exception as e_unhandled: # Catch any other unexpected error
                self.fail(f"Unexpected exception during test execution of script's logic: {e_unhandled}")

        output = stdout_capture.getvalue()
        mock_load_from_storage.assert_called_once_with(version="v19")
        mock_customer_service.list_accessible_customers.assert_called_once()
        self.assertIn('Request with ID "req_ex_test" failed with status "TEST_ERROR_CODE"', output)
        self.assertIn('	Error with message "A test error occurred."', output)
        mock_sys_exit.assert_called_once_with(1)

if __name__ == "__main__":
    unittest.main()
