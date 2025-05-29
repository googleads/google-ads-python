import unittest
from unittest.mock import patch, Mock, MagicMock, call
import argparse
import sys
import io

from google.ads.googleads.errors import GoogleAdsException
from google.ads.googleads.v16.services.services.google_ads_service import GoogleAdsServiceClient
from google.ads.googleads.v16.services.services.customer_service import CustomerServiceClient
from google.ads.googleads.v16.resources.types.customer_client import CustomerClient as CustomerClientType
from google.ads.googleads.v16.services.types.google_ads_service import GoogleAdsRow

# Assuming get_account_hierarchy.py is in examples.account_management
from examples.account_management.get_account_hierarchy import (
    main as get_account_hierarchy_main,
    print_account_hierarchy,
    _build_manager_map, # Import this if it's used directly or needs testing
    _get_account_hierarchy # Import this if it's used directly or needs testing
)

class TestGetAccountHierarchy(unittest.TestCase):
    def setUp(self):
        self.mock_google_ads_client = MagicMock()
        self.mock_googleads_service = MagicMock(spec=GoogleAdsServiceClient)
        self.mock_customer_service = MagicMock(spec=CustomerServiceClient)

        self.mock_google_ads_client.get_service.side_effect = lambda service_name, version: {
            "GoogleAdsService": self.mock_googleads_service,
            "CustomerService": self.mock_customer_service,
        }[service_name]

    # Helper method to create mock GoogleAdsRow with CustomerClient
    def _create_mock_customer_client_row(self, id, descriptive_name, currency_code, time_zone, level, manager, resource_name_prefix="customers/"):
        mock_row = MagicMock(spec=GoogleAdsRow)
        mock_row.customer_client = MagicMock(spec=CustomerClientType)
        mock_row.customer_client.id = id
        mock_row.customer_client.descriptive_name = descriptive_name
        mock_row.customer_client.currency_code = currency_code
        mock_row.customer_client.time_zone = time_zone
        mock_row.customer_client.level = level
        mock_row.customer_client.manager = manager
        mock_row.customer_client.resource_name = f"{resource_name_prefix}{id}"
        return mock_row

    def test_print_account_hierarchy_recursive(self):
        # Create mock customer clients
        root_customer_client_mock = self._create_mock_customer_client_row(
            id=123, descriptive_name="Root Account", currency_code="USD",
            time_zone="America/New_York", level=0, manager=False
        ).customer_client

        child1_mock = self._create_mock_customer_client_row(
            id=456, descriptive_name="Child Account 1", currency_code="USD",
            time_zone="America/New_York", level=1, manager=False
        ).customer_client

        child2_manager_mock = self._create_mock_customer_client_row(
            id=789, descriptive_name="Child Manager Account 2", currency_code="EUR",
            time_zone="Europe/London", level=1, manager=True
        ).customer_client
        
        grandchild_mock = self._create_mock_customer_client_row(
            id=101, descriptive_name="Grandchild Account", currency_code="GBP",
            time_zone="Europe/Dublin", level=2, manager=False
        ).customer_client


        # Structure:
        # Root (123)
        #  |- Child 1 (456)
        #  |- Child Manager 2 (789)
        #      |- Grandchild (101)

        customer_ids_to_child_accounts = {
            123: [child1_mock, child2_manager_mock],
            456: [],
            789: [grandchild_mock],
            101: []
        }

        captured_output = io.StringIO()
        sys.stdout = captured_output

        print_account_hierarchy(root_customer_client_mock, customer_ids_to_child_accounts, 0)

        sys.stdout = sys.__stdout__  # Reset stdout

        expected_output = (
            "Customer ID: 123, Name: 'Root Account', Currency: USD, Time Zone: America/New_York, Is Manager: False, Level: 0\n"
            "  Customer ID: 456, Name: 'Child Account 1', Currency: USD, Time Zone: America/New_York, Is Manager: False, Level: 1\n"
            "  Customer ID: 789, Name: 'Child Manager Account 2', Currency: EUR, Time Zone: Europe/London, Is Manager: True, Level: 1\n"
            "    Customer ID: 101, Name: 'Grandchild Account', Currency: GBP, Time Zone: Europe/Dublin, Is Manager: False, Level: 2\n"
        )
        actual_output = captured_output.getvalue()
        
        # Normalize line endings for comparison, as the expected output uses \n
        self.assertEqual(actual_output.replace('\r\n', '\n'), expected_output)

    @patch('examples.account_management.get_account_hierarchy.GoogleAdsClient.load_from_storage')
    def test_main_with_login_customer_id(self, mock_load_from_storage):
        mock_load_from_storage.return_value = self.mock_google_ads_client
        login_customer_id = "123"

        # Define the hierarchy
        # Root (123) - Manager
        #  |- Child 1 (456) - Not a manager
        #  |- Child 2 (789) - Manager
        #      |- Grandchild 1 (101) - Not a manager
        
        root_customer_row = self._create_mock_customer_client_row(
            id=123, descriptive_name="Root Manager Account", currency_code="USD",
            time_zone="America/New_York", level=0, manager=True
        )
        child1_row = self._create_mock_customer_client_row(
            id=456, descriptive_name="Child Account 1", currency_code="USD",
            time_zone="America/New_York", level=1, manager=False
        )
        child2_manager_row = self._create_mock_customer_client_row(
            id=789, descriptive_name="Child Manager Account 2", currency_code="EUR",
            time_zone="Europe/London", level=1, manager=True
        )
        grandchild1_row = self._create_mock_customer_client_row(
            id=101, descriptive_name="Grandchild Account 1", currency_code="GBP",
            time_zone="Europe/Dublin", level=2, manager=False
        )

        # Mock the search responses
        # First call for the root customer and its direct children
        self.mock_googleads_service.search.side_effect = [
            # Initial call for login_customer_id=123
            iter([root_customer_row, child1_row, child2_manager_row]),
            # Call for manager account 789
            iter([grandchild1_row]),
            # Subsequent calls for non-manager accounts (should not happen for them or return empty)
            iter([]), # For 456
            iter([])  # For 101
        ]

        captured_output = io.StringIO()
        sys.stdout = captured_output

        get_account_hierarchy_main(self.mock_google_ads_client, login_customer_id)

        sys.stdout = sys.__stdout__  # Reset stdout

        expected_output = (
            "Customer ID: 123, Name: 'Root Manager Account', Currency: USD, Time Zone: America/New_York, Is Manager: True, Level: 0\n"
            "  Customer ID: 456, Name: 'Child Account 1', Currency: USD, Time Zone: America/New_York, Is Manager: False, Level: 1\n"
            "  Customer ID: 789, Name: 'Child Manager Account 2', Currency: EUR, Time Zone: Europe/London, Is Manager: True, Level: 1\n"
            "    Customer ID: 101, Name: 'Grandchild Account 1', Currency: GBP, Time Zone: Europe/Dublin, Is Manager: False, Level: 2\n"
        )
        actual_output = captured_output.getvalue()
        self.assertEqual(actual_output.replace('\r\n', '\n'), expected_output)

        # Verify calls to GoogleAdsService.search
        # Query for root and its children
        query_for_root_and_children = (
            "SELECT customer_client.id, customer_client.descriptive_name, "
            "customer_client.currency_code, customer_client.time_zone, "
            "customer_client.manager, customer_client.level, customer_client.resource_name "
            "FROM customer_client "
            "WHERE customer_client.level <= 1"
        )
        # Query for children of a manager
        query_for_specific_manager_children = (
            "SELECT customer_client.id, customer_client.descriptive_name, "
            "customer_client.currency_code, customer_client.time_zone, "
            "customer_client.manager, customer_client.level, customer_client.resource_name "
            "FROM customer_client"
        )


        expected_calls = [
            call(customer_id=login_customer_id, query=query_for_root_and_children),
            call(customer_id="789", query=query_for_specific_manager_children)
        ]
        self.mock_googleads_service.search.assert_has_calls(expected_calls, any_order=False)
        # Depending on the exact implementation of _get_account_hierarchy, 
        # there might be more calls if it tries to fetch children of non-managers.
        # For now, we check the essential calls. A more robust check would be to verify the number of calls.
        self.assertLessEqual(self.mock_googleads_service.search.call_count, 4) # Root + ChildManager + 2 children (non-managers)


    @patch('examples.account_management.get_account_hierarchy.GoogleAdsClient.load_from_storage')
    @patch('examples.account_management.get_account_hierarchy.parse_customer_path') # Mocking at the module level where it's used
    def test_main_without_login_customer_id(self, mock_parse_customer_path, mock_load_from_storage):
        mock_load_from_storage.return_value = self.mock_google_ads_client

        # Mock list_accessible_customers response
        accessible_customers_response = Mock()
        accessible_customers_response.resource_names = ["customers/111", "customers/222"]
        self.mock_customer_service.list_accessible_customers.return_value = accessible_customers_response

        # Mock parse_customer_path
        mock_parse_customer_path.side_effect = lambda resource_name: {"customer_id": resource_name.split("/")[-1]}

        # Define hierarchies for each accessible customer
        # Customer 111
        customer_111_root = self._create_mock_customer_client_row(
            id=111, descriptive_name="Accessible Root 1", currency_code="USD",
            time_zone="America/New_York", level=0, manager=False
        )
        # Customer 222 (Manager)
        customer_222_root_manager = self._create_mock_customer_client_row(
            id=222, descriptive_name="Accessible Root Manager 2", currency_code="EUR",
            time_zone="Europe/Paris", level=0, manager=True
        )
        customer_222_child = self._create_mock_customer_client_row(
            id=333, descriptive_name="Child of 222", currency_code="EUR",
            time_zone="Europe/Paris", level=1, manager=False
        )

        # Mock GoogleAdsService.search responses for each customer
        self.mock_googleads_service.search.side_effect = [
            # For customer 111 (not a manager)
            iter([customer_111_root]),
            iter([]), # No children to fetch for 111 if it was a manager, or if it's not a manager, this might not be called or should be empty
            # For customer 222 (is a manager)
            iter([customer_222_root_manager, customer_222_child]), # Root and its direct children
            iter([]), # No grandchildren for 333
        ]

        captured_output = io.StringIO()
        sys.stdout = captured_output

        get_account_hierarchy_main(self.mock_google_ads_client, login_customer_id=None)

        sys.stdout = sys.__stdout__  # Reset stdout

        expected_output = (
            "Customer ID: 111, Name: 'Accessible Root 1', Currency: USD, Time Zone: America/New_York, Is Manager: False, Level: 0\n"
            "Customer ID: 222, Name: 'Accessible Root Manager 2', Currency: EUR, Time Zone: Europe/Paris, Is Manager: True, Level: 0\n"
            "  Customer ID: 333, Name: 'Child of 222', Currency: EUR, Time Zone: Europe/Paris, Is Manager: False, Level: 1\n"
        )
        actual_output = captured_output.getvalue()
        self.assertEqual(actual_output.replace('\r\n', '\n'), expected_output)

        self.mock_customer_service.list_accessible_customers.assert_called_once()
        mock_parse_customer_path.assert_has_calls([
            call("customers/111"),
            call("customers/222")
        ], any_order=True) # Order might vary depending on internal processing

        # Verify search calls
        query_for_root_and_children = ( # Used when a manager is found, or for the initial seed customer
            "SELECT customer_client.id, customer_client.descriptive_name, "
            "customer_client.currency_code, customer_client.time_zone, "
            "customer_client.manager, customer_client.level, customer_client.resource_name "
            "FROM customer_client "
            "WHERE customer_client.level <= 1"
        )
        # This query is used when a specific manager's children are fetched.
        query_for_specific_manager_children = (
            "SELECT customer_client.id, customer_client.descriptive_name, "
            "customer_client.currency_code, customer_client.time_zone, "
            "customer_client.manager, customer_client.level, customer_client.resource_name "
            "FROM customer_client"
        )

        expected_search_calls = [
            call(customer_id="111", query=query_for_root_and_children), # For customer 111
            call(customer_id="222", query=query_for_root_and_children), # For customer 222
            # If 222 is a manager and has children, there would be another call for its children,
            # but the current mock setup for print_account_hierarchy implies _get_account_hierarchy
            # is called for each seed, and it builds the map.
            # The current mock for search.side_effect for 222 already returns its child.
            # If _get_account_hierarchy fetches children for managers recursively, then for 222 (manager)
            # it would make one call, get child 333. If 333 was a manager, another call for 333.
            # The script logic is that _get_account_hierarchy is called for *each* seed customer.
            # So, for customer_111 (not manager), one call.
            # For customer_222 (manager), one call that gets its child.
            # If child 333 was a manager, then _get_account_hierarchy (for 222) would make another call for 333.
            # Let's adjust the expectation based on _get_account_hierarchy being called per seed customer,
            # and it internally handles recursion for that seed.
        ]
        # Check that the calls were made, without enforcing strict order for the top-level seed customers
        self.mock_googleads_service.search.assert_any_call(customer_id="111", query=query_for_root_and_children)
        self.mock_googleads_service.search.assert_any_call(customer_id="222", query=query_for_root_and_children)
        # The number of calls depends on how many managers are found and explored.
        # Customer 111 (not a manager): 1 call (initial)
        # Customer 222 (manager, has one child 333 which is not a manager): 1 call (initial, gets child)
        # Total = 2 essential calls to get the hierarchy as defined.
        self.assertEqual(self.mock_googleads_service.search.call_count, 2)


    @patch('examples.account_management.get_account_hierarchy.GoogleAdsClient.load_from_storage')
    @patch('sys.exit')
    def test_main_google_ads_exception_with_login_id(self, mock_sys_exit, mock_load_from_storage):
        mock_load_from_storage.return_value = self.mock_google_ads_client
        login_customer_id = "123"

        # Configure GoogleAdsService.search to raise GoogleAdsException
        mock_error = MagicMock()
        mock_error.message = "Test GoogleAdsException from search"
        mock_failure = MagicMock()
        mock_failure.errors = [mock_error]
        google_ads_exception = GoogleAdsException(
            error=None, call=None, failure=mock_failure, error_code=None,
            message="Simulated GoogleAdsException during search"
        )
        self.mock_googleads_service.search.side_effect = google_ads_exception

        captured_output = io.StringIO()
        sys.stdout = captured_output

        get_account_hierarchy_main(self.mock_google_ads_client, login_customer_id)

        sys.stdout = sys.__stdout__  # Reset stdout

        mock_sys_exit.assert_called_once_with(1)
        output = captured_output.getvalue()
        self.assertIn("Request with ID", output) # Part of the generic error message
        self.assertIn("Test GoogleAdsException from search", output)
        self.mock_googleads_service.search.assert_called_once()

    @patch('examples.account_management.get_account_hierarchy.GoogleAdsClient.load_from_storage')
    @patch('sys.exit')
    def test_main_google_ads_exception_without_login_id(self, mock_sys_exit, mock_load_from_storage):
        mock_load_from_storage.return_value = self.mock_google_ads_client

        # Configure CustomerService.list_accessible_customers to raise GoogleAdsException
        mock_error = MagicMock()
        mock_error.message = "Test GoogleAdsException from list_accessible_customers"
        mock_failure = MagicMock()
        mock_failure.errors = [mock_error]
        google_ads_exception = GoogleAdsException(
            error=None, call=None, failure=mock_failure, error_code=None,
            message="Simulated GoogleAdsException during list_accessible_customers"
        )
        self.mock_customer_service.list_accessible_customers.side_effect = google_ads_exception

        captured_output = io.StringIO()
        sys.stdout = captured_output

        get_account_hierarchy_main(self.mock_google_ads_client, login_customer_id=None)

        sys.stdout = sys.__stdout__  # Reset stdout

        mock_sys_exit.assert_called_once_with(1)
        output = captured_output.getvalue()
        self.assertIn("Request with ID", output) # Part of the generic error message
        self.assertIn("Test GoogleAdsException from list_accessible_customers", output)
        self.mock_customer_service.list_accessible_customers.assert_called_once()

    @patch('examples.account_management.get_account_hierarchy.GoogleAdsClient.load_from_storage')
    @patch('examples.account_management.get_account_hierarchy.main') # Mock the main function in the script
    @patch('argparse.ArgumentParser.parse_args')
    def test_argument_parser_with_login_customer_id(self, mock_parse_args, mock_script_main, mock_load_from_storage):
        # Simulate command line arguments: python get_account_hierarchy.py -l 123
        test_login_id = "123"
        sys.argv = ["get_account_hierarchy.py", "-l", test_login_id]
        
        # Mock parse_args to return the specific login_customer_id
        mock_parse_args.return_value = argparse.Namespace(login_customer_id=test_login_id)
        
        # Mock the client returned by load_from_storage
        mock_google_ads_client_instance = MagicMock()
        mock_load_from_storage.return_value = mock_google_ads_client_instance

        # Execute the script's main block using runpy
        # This will trigger argument parsing and the call to main() within the script
        import runpy
        runpy.run_module("examples.account_management.get_account_hierarchy", run_name="__main__")

        mock_load_from_storage.assert_called_once() # Client should be loaded
        mock_parse_args.assert_called_once()
        # Assert that the script's main function was called with the loaded client and the parsed login_customer_id
        mock_script_main.assert_called_once_with(mock_google_ads_client_instance, test_login_id)

    @patch('examples.account_management.get_account_hierarchy.GoogleAdsClient.load_from_storage')
    @patch('examples.account_management.get_account_hierarchy.main') # Mock the main function in the script
    @patch('argparse.ArgumentParser.parse_args')
    def test_argument_parser_without_login_customer_id(self, mock_parse_args, mock_script_main, mock_load_from_storage):
        # Simulate command line arguments: python get_account_hierarchy.py
        sys.argv = ["get_account_hierarchy.py"]

        # Mock parse_args to return None for login_customer_id (as if -l was not provided)
        mock_parse_args.return_value = argparse.Namespace(login_customer_id=None)

        # Mock the client returned by load_from_storage
        mock_google_ads_client_instance = MagicMock()
        mock_load_from_storage.return_value = mock_google_ads_client_instance
        
        import runpy
        runpy.run_module("examples.account_management.get_account_hierarchy", run_name="__main__")

        mock_load_from_storage.assert_called_once()
        mock_parse_args.assert_called_once()
        # Assert that the script's main function was called with the loaded client and None for login_customer_id
        mock_script_main.assert_called_once_with(mock_google_ads_client_instance, None)


if __name__ == "__main__":
    unittest.main()
