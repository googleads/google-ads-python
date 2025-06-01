import os
import sys
import unittest
from unittest.mock import MagicMock, patch, call # Ensure 'call' is imported if not already

# Dynamically add the parent directory to sys.path to resolve analyzer module
# This makes the test runnable whether discovered or run directly
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.join(current_dir, '..')

# Check if the parent directory is already in sys.path to avoid duplicates
# and to ensure the original sys.path is respected if possible.
original_sys_path = list(sys.path) # Take a copy
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
    path_inserted = True
else:
    path_inserted = False

try:
    import analyzer
except ImportError as e:
    # If it still fails, raise an error that's informative.
    raise ImportError(
        f"Failed to import 'analyzer' module. "
        f"Attempted to add '{parent_dir}' to sys.path. "
        f"Original error: {e}"
    )
finally:
    # Clean up sys.path if we modified it.
    # This prevents side effects if tests are run in a persistent session.
    if path_inserted:
        if sys.path[0] == parent_dir:
            sys.path.pop(0)
        elif parent_dir in sys.path: # Fallback removal if it wasn't at index 0
             sys.path.remove(parent_dir)


class TestAnalyzer(unittest.TestCase):

    @patch('builtins.print')
    @patch('google.ads.googleads.client.GoogleAdsClient.load_from_storage')
    def test_account_hierarchy_module_with_customer_id(self, mock_load_from_storage, mock_print):
        mock_ads_client = MagicMock()
        mock_load_from_storage.return_value = mock_ads_client

        mock_google_ads_service = MagicMock()
        mock_customer_service = MagicMock()

        mock_ads_client.get_service.side_effect = lambda service_name, version=None: \
            mock_google_ads_service if service_name == "GoogleAdsService" else \
            mock_customer_service if service_name == "CustomerService" else MagicMock()

        # Mock responses for GoogleAdsService search
        def mock_search_side_effect(customer_id, query):
            # Mock for initial call with customer_id='123'
            if customer_id == '123':
                # Row for root account '123'
                mock_row_root = MagicMock()
                mock_row_root.customer_client.id = '123'
                mock_row_root.customer_client.descriptive_name = 'Root Account'
                mock_row_root.customer_client.currency_code = 'USD'
                mock_row_root.customer_client.time_zone = 'America/New_York'
                mock_row_root.customer_client.manager = True
                mock_row_root.customer_client.level = 0

                # Row for child account '456' (manager)
                mock_row_child1 = MagicMock()
                mock_row_child1.customer_client.id = '456'
                mock_row_child1.customer_client.descriptive_name = 'Child 1'
                mock_row_child1.customer_client.currency_code = 'USD'
                mock_row_child1.customer_client.time_zone = 'America/New_York'
                mock_row_child1.customer_client.manager = True
                mock_row_child1.customer_client.level = 1

                # Row for child account '789' (not a manager)
                mock_row_child2 = MagicMock()
                mock_row_child2.customer_client.id = '789'
                mock_row_child2.customer_client.descriptive_name = 'Child 2'
                mock_row_child2.customer_client.currency_code = 'EUR'
                mock_row_child2.customer_client.time_zone = 'Europe/London'
                mock_row_child2.customer_client.manager = False
                mock_row_child2.customer_client.level = 1
                return iter([mock_row_root, mock_row_child1, mock_row_child2])
            # Mock for call with child manager customer_id='456'
            elif customer_id == '456':
                # Row for manager account '456' itself (as root of this query)
                mock_row_manager_self = MagicMock()
                mock_row_manager_self.customer_client.id = '456'
                mock_row_manager_self.customer_client.descriptive_name = 'Child 1' # Name consistency
                mock_row_manager_self.customer_client.currency_code = 'USD'
                mock_row_manager_self.customer_client.time_zone = 'America/New_York'
                mock_row_manager_self.customer_client.manager = True # It is a manager
                mock_row_manager_self.customer_client.level = 0 # Level 0 for this specific query

                # Row for grandchild account '45601'
                mock_row_grandchild = MagicMock()
                mock_row_grandchild.customer_client.id = '45601'
                mock_row_grandchild.customer_client.descriptive_name = 'Grandchild 1.1'
                mock_row_grandchild.customer_client.currency_code = 'USD'
                mock_row_grandchild.customer_client.time_zone = 'America/New_York'
                mock_row_grandchild.customer_client.manager = False
                mock_row_grandchild.customer_client.level = 1 # Level 1 relative to '456'
                return iter([mock_row_manager_self, mock_row_grandchild])
            return iter([]) # Default empty response

        mock_google_ads_service.search.side_effect = mock_search_side_effect

        # Mock CustomerService (not directly used by account_hierarchy_module for hierarchy logic,
        # but good to have a basic mock if the client tries to get it)
        mock_customer_service.list_accessible_customers.return_value = MagicMock(resource_names=[])


        analyzer.account_hierarchy_module(mock_ads_client, '123')

        # _DEFAULT_LOG_SPACE_LENGTH is 4
        # Depth 0: "-"
        # Depth 1: "-----"
        # Depth 2: "---------"
        expected_prints = [
            call("\nThe hierarchy of customer ID 123 is printed below:"),
            call("Customer ID (Descriptive Name, Currency Code, Time Zone)"),
            call("-", end=""),
            call("123 (Root Account, USD, America/New_York)"),
            call("-----", end=""),
            call("456 (Child 1, USD, America/New_York)"),
            call("---------", end=""),
            call("45601 (Grandchild 1.1, USD, America/New_York)"),
            call("-----", end=""),
            call("789 (Child 2, EUR, Europe/London)")
        ]
        mock_print.assert_has_calls(expected_prints, any_order=False)

    @patch('builtins.print')
    @patch('google.ads.googleads.client.GoogleAdsClient.load_from_storage')
    def test_account_hierarchy_module_without_customer_id(self, mock_load_from_storage, mock_print):
        mock_ads_client = MagicMock()
        mock_load_from_storage.return_value = mock_ads_client

        mock_google_ads_service = MagicMock()
        mock_customer_service = MagicMock()

        mock_ads_client.get_service.side_effect = lambda service_name, version=None: \
            mock_google_ads_service if service_name == "GoogleAdsService" else \
            mock_customer_service if service_name == "CustomerService" else MagicMock()

        # Mock list_accessible_customers response
        mock_accessible_customers_response = MagicMock()
        mock_accessible_customers_response.resource_names = ["customers/111", "customers/222"]
        mock_customer_service.list_accessible_customers.return_value = mock_accessible_customers_response

        # Mock responses for GoogleAdsService search
        def mock_search_side_effect(customer_id, query):
            if customer_id == '111':
                mock_row_root1 = MagicMock()
                mock_row_root1.customer_client.id = '111'
                mock_row_root1.customer_client.descriptive_name = 'Acc One'
                mock_row_root1.customer_client.currency_code = 'USD'
                mock_row_root1.customer_client.time_zone = 'America/New_York'
                mock_row_root1.customer_client.manager = True
                mock_row_root1.customer_client.level = 0

                mock_row_child1_1 = MagicMock()
                mock_row_child1_1.customer_client.id = '11101'
                mock_row_child1_1.customer_client.descriptive_name = 'Child Acc One'
                mock_row_child1_1.customer_client.currency_code = 'USD'
                mock_row_child1_1.customer_client.time_zone = 'America/New_York'
                mock_row_child1_1.customer_client.manager = False
                mock_row_child1_1.customer_client.level = 1
                return iter([mock_row_root1, mock_row_child1_1])
            elif customer_id == '222':
                mock_row_root2 = MagicMock()
                mock_row_root2.customer_client.id = '222'
                mock_row_root2.customer_client.descriptive_name = 'Acc Two'
                mock_row_root2.customer_client.currency_code = 'EUR'
                mock_row_root2.customer_client.time_zone = 'Europe/Dublin'
                mock_row_root2.customer_client.manager = True # Making it a manager for potential deeper hierarchy
                mock_row_root2.customer_client.level = 0

                mock_row_child2_1 = MagicMock()
                mock_row_child2_1.customer_client.id = '22201'
                mock_row_child2_1.customer_client.descriptive_name = 'Child Acc Two'
                mock_row_child2_1.customer_client.currency_code = 'EUR'
                mock_row_child2_1.customer_client.time_zone = 'Europe/Dublin'
                mock_row_child2_1.customer_client.manager = False
                mock_row_child2_1.customer_client.level = 1
                return iter([mock_row_root2, mock_row_child2_1])
            return iter([])

        mock_google_ads_service.search.side_effect = mock_search_side_effect

        analyzer.account_hierarchy_module(mock_ads_client, None)

        expected_prints = [
            call("No manager ID is specified. The example will print the hierarchies of all accessible customer IDs."),
            call("Total results: 2"),
            call('Customer resource name: "customers/111"'),
            call('Customer resource name: "customers/222"'),
            call("\nThe hierarchy of customer ID 111 is printed below:"),
            call("Customer ID (Descriptive Name, Currency Code, Time Zone)"),
            call("-", end=""),
            call("111 (Acc One, USD, America/New_York)"),
            call("-----", end=""),
            call("11101 (Child Acc One, USD, America/New_York)"),
            call("\nThe hierarchy of customer ID 222 is printed below:"),
            call("Customer ID (Descriptive Name, Currency Code, Time Zone)"),
            call("-", end=""),
            call("222 (Acc Two, EUR, Europe/Dublin)"),
            call("-----", end=""),
            call("22201 (Child Acc Two, EUR, Europe/Dublin)"),
        ]
        mock_print.assert_has_calls(expected_prints, any_order=False)

    @patch('builtins.print')
    @patch('google.ads.googleads.client.GoogleAdsClient.load_from_storage')
    def test_get_users_module(self, mock_load_from_storage, mock_print):
        mock_ads_client = MagicMock()
        mock_load_from_storage.return_value = mock_ads_client

        mock_google_ads_service = MagicMock()
        # For this test, only GoogleAdsService is expected.
        mock_ads_client.get_service.side_effect = lambda service_name, version=None: \
            mock_google_ads_service if service_name == "GoogleAdsService" else MagicMock()

        # Prepare mock rows for the search response
        mock_row1 = MagicMock()
        mock_user_access1 = mock_row1.customer_user_access
        mock_user_access1.user_id = 'user001'
        mock_user_access1.email_address = 'test1@example.com'
        mock_user_access1.access_role.name = 'ADMIN'
        mock_user_access1.access_creation_date_time = '2023-01-15 09:30:00'
        # mock_user_access1.inviter_user_email_address = 'inviter1@example.com' # Not printed in current analyzer.py

        mock_row2 = MagicMock()
        mock_user_access2 = mock_row2.customer_user_access
        mock_user_access2.user_id = 'user002'
        mock_user_access2.email_address = 'test2@example.net'
        mock_user_access2.access_role.name = 'STANDARD'
        mock_user_access2.access_creation_date_time = '2023-02-20 14:00:00'
        # mock_user_access2.inviter_user_email_address = 'inviter2@example.net' # Not printed

        mock_google_ads_service.search.return_value = iter([mock_row1, mock_row2])

        customer_id_to_test = '9876543210'
        analyzer.get_users_module(mock_ads_client, customer_id_to_test)

        expected_prints = [
            call(f"The given customer ID has access to the client account with ID {mock_user_access1.user_id}, "
                 f"with an access role of '{mock_user_access1.access_role.name}', "
                 f"and creation time of '{mock_user_access1.access_creation_date_time}'."),
            call(f"The given customer ID has access to the client account with ID {mock_user_access2.user_id}, "
                 f"with an access role of '{mock_user_access2.access_role.name}', "
                 f"and creation time of '{mock_user_access2.access_creation_date_time}'.")
        ]

        # Check that search was called with the correct customer ID
        mock_google_ads_service.search.assert_called_once()
        call_args, call_kwargs = mock_google_ads_service.search.call_args
        self.assertEqual(call_kwargs['customer_id'], customer_id_to_test)
        # It's also good to check the query if it's stable, but for now, customer_id is the main variable part.

        mock_print.assert_has_calls(expected_prints, any_order=False)


if __name__ == '__main__':
    unittest.main()
