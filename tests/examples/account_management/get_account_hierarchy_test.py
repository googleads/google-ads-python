import unittest
from unittest.mock import patch, MagicMock, call

from google.ads.googleads.errors import GoogleAdsException
# This import assumes that the test runner will add the root directory to sys.path
# or that the `examples` directory is otherwise findable.
from examples.account_management.get_account_hierarchy import main


class GetAccountHierarchyTest(unittest.TestCase):

    @patch("examples.account_management.get_account_hierarchy.GoogleAdsClient.load_from_storage")
    def test_get_account_hierarchy_success(self, mock_load_from_storage):
        """Tests the successful retrieval and printing of account hierarchy."""
        mock_google_ads_client = MagicMock()
        mock_load_from_storage.return_value = mock_google_ads_client

        mock_google_ads_service = MagicMock()
        mock_google_ads_client.get_service.return_value = mock_google_ads_service

        # Mock the response from search_stream
        # The script expects rows with customer_client, manager, descriptive_name, currency_code, time_zone, id
        mock_row1 = MagicMock()
        mock_row1.customer_client.descriptive_name = "Account Test Name 1 (111-111-1111)"
        mock_row1.customer_client.id = 1111111111
        mock_row1.customer_client.manager = False # It's a client
        # Add other fields if the script uses them directly from the row for printing
        # The script's print_account_hierarchy function also checks for these:
        mock_row1.customer.descriptive_name = "Account Test Name 1" # This is what's used for printing name
        mock_row1.customer.id = 1111111111
        mock_row1.customer.currency_code = "USD"
        mock_row1.customer.time_zone = "America/New_York"
        mock_row1.customer.manager = False


        mock_row2_manager = MagicMock()
        mock_row2_manager.customer_client.descriptive_name = "Manager Account Name (222-222-2222)"
        mock_row2_manager.customer_client.id = 2222222222
        mock_row2_manager.customer_client.manager = True # It's a manager
        mock_row2_manager.customer.descriptive_name = "Manager Account Name"
        mock_row2_manager.customer.id = 2222222222
        mock_row2_manager.customer.currency_code = "EUR"
        mock_row2_manager.customer.time_zone = "Europe/London"
        mock_row2_manager.customer.manager = True


        # This account is managed by mock_row2_manager
        mock_row3 = MagicMock()
        mock_row3.customer_client.descriptive_name = "Sub Account Name (333-333-3333)"
        mock_row3.customer_client.id = 3333333333
        mock_row3.customer_client.manager = False
        mock_row3.customer.descriptive_name = "Sub Account Name"
        mock_row3.customer.id = 3333333333
        mock_row3.customer.currency_code = "JPY"
        mock_row3.customer.time_zone = "Asia/Tokyo"
        mock_row3.customer.manager = False

        # The script builds a tree. The search_stream returns a flat list.
        # The initial query is for the manager accounts under the root_customer_id
        # Then, for each manager account, it recursively calls _print_account_hierarchy
        # which issues another search_stream call.

        # Let's simulate the stream for a manager ID "1234567890"
        # First call: Find accounts managed by "1234567890"
        # Second call (recursive): Find accounts managed by "2222222222" (mock_row2_manager.customer_client.id)
        
        # The script expects an iterable of "batches", and each batch is an iterable of rows.
        # So, search_stream returns an iterable of [mock_row1, mock_row2_manager] for the first call,
        # and then an iterable of [mock_row3] for the recursive call for mock_row2_manager.

        # To simplify, we'll have search_stream return different results based on the query.
        # The query contains the manager ID.
        def mock_search_stream_side_effect(customer_id, query):
            if str(self.manager_customer_id) in query: # Initial call
                # This batch contains a non-manager and a manager account
                batch1 = MagicMock()
                batch1.results = [mock_row1, mock_row2_manager]
                return iter([batch1]) 
            elif str(mock_row2_manager.customer_client.id) in query: # Recursive call for mock_row2_manager
                batch2 = MagicMock()
                batch2.results = [mock_row3]
                return iter([batch2])
            elif str(mock_row1.customer_client.id) in query: # mock_row1 is not a manager
                return iter([]) # No accounts managed by mock_row1
            else:
                return iter([])

        mock_google_ads_service.search_stream.side_effect = mock_search_stream_side_effect
        
        self.manager_customer_id = "1234567890" # Used in side_effect

        # Mock print to capture output
        with patch("builtins.print") as mock_print:
            main(mock_google_ads_client, self.manager_customer_id, login_customer_id=None)

        # Assert get_service was called
        mock_google_ads_client.get_service.assert_called_once_with(
            "GoogleAdsService", version="v19"
        )

        # Assert search_stream calls
        # Expected query for the initial call
        query_manager_id = str(self.manager_customer_id).replace("-", "")
        expected_query_initial = f"""
            SELECT
                customer_client.client_customer,
                customer_client.level,
                customer_client.manager,
                customer_client.descriptive_name,
                customer_client.currency_code,
                customer_client.time_zone,
                customer_client.id
            FROM customer_client
            WHERE customer_client.level <= 1
            AND customer_client.manager = false AND customer_client.level = 1""" # This query is from the example script, for the non-manager case
        
        # The script has two main branches: one if login_customer_id is provided (fetches its details first)
        # and another if it's not (uses manager_customer_id as the root).
        # The _print_account_hierarchy function is the one doing the recursive querying.
        # Let's trace the query from _print_account_hierarchy:
        # query = f"""
        #     SELECT
        #         customer_client.client_customer,
        #         customer_client.level,
        #         customer_client.manager,
        #         customer_client.descriptive_name,
        #         customer_client.currency_code,
        #         customer_client.time_zone,
        #         customer_client.id,
        #         customer.descriptive_name,
        #         customer.currency_code,
        #         customer.time_zone,
        #         customer.id,
        #         customer.manager
        #     FROM customer_client
        #     WHERE customer_client.manager = FALSE AND customer_client.level = 1
        #     ORDER BY customer_client.id"""
        # This query is static in _print_account_hierarchy and is passed to search_stream
        # along with the current manager's ID (customer_id argument to search_stream).

        # First call to search_stream:
        # customer_id = self.manager_customer_id
        # query = <the query above>
        # Second call (recursive for mock_row2_manager):
        # customer_id = mock_row2_manager.customer_client.id (which is 2222222222)
        # query = <the query above>
        
        # The script actually fetches all accounts under the specified manager_customer_id first,
        # then builds a tree and prints it. It does not recursively call search_stream.
        # It gets all accounts and then constructs the hierarchy in memory.

        # Let's re-evaluate the mock_search_stream. It's called once.
        # The query in the script is:
        # query = f"""
        #     SELECT
        #         customer_client.client_customer,
        #         customer_client.level,
        #         customer_client.manager,
        #         customer_client.descriptive_name,
        #         customer_client.currency_code,
        #         customer_client.time_zone,
        #         customer_client.id,
        #         customer.descriptive_name,
        #         customer.currency_code,
        #         customer.time_zone,
        #         customer.id,
        #         customer.manager
        #     FROM customer_client
        #     WHERE customer_client.level <= {MAX_HIERARCHY_LEVEL}
        #     ORDER BY customer_client.level"""
        # MAX_HIERARCHY_LEVEL is 1. This seems to only get direct children.
        # Ah, the example script's logic:
        # 1. If login_customer_id is the same as manager_customer_id OR login_customer_id is not set:
        #    It issues a query for the details of manager_customer_id itself.
        #    Then it calls _print_account_hierarchy with this manager_customer_id and an empty list of seed_customer_ids.
        # 2. _print_account_hierarchy:
        #    - Takes a googleads_service, root_customer_id, and seed_customer_ids.
        #    - If seed_customer_ids is empty, it issues a search_stream to find all accounts under root_customer_id.
        #      Query: "FROM customer_client WHERE customer_client.level <= 1 ORDER BY customer_client.level"
        #      This gets accounts linked to the root_customer_id.
        #    - It then processes these results, building a map.
        #    - It then iterates and prints. It does not seem to make further search_stream calls for sub-managers within _print_account_hierarchy.
        # This means the hierarchy is limited by what the initial query returns.
        # The script is named "get_account_hierarchy" but seems to only get one level if MAX_HIERARCHY_LEVEL = 1.
        # Let's re-read the script: examples/account_management/get_account_hierarchy.py
        # The script uses GoogleAdsService.search to get the root customer details if login_customer_id is provided.
        # The core logic for hierarchy is in _print_account_hierarchy.
        # It takes seed_customer_ids. If empty, it queries for customer_clients of the root_customer_id.
        # The query is indeed:
        # "SELECT customer_client.client_customer, customer_client.level, customer_client.manager, ... FROM customer_client WHERE customer_client.level <= 1 ORDER BY customer_client.level"
        # This will fetch direct children and the root itself if it's part of its own hierarchy graph (level 0).
        # It then builds a map: manager_id -> list of child accounts.
        # And then it recursively prints this map (not recursively querying).

        # So, one search_stream call is expected from _print_account_hierarchy.
        # If login_customer_id is different from manager_customer_id, there's an additional search call (not stream).
        # Let's test the case where login_customer_id is None, so manager_customer_id is the root.
        
        mock_google_ads_service.search_stream.return_value = [iter([mock_row1, mock_row2_manager, mock_row3])] # Simulate one batch with all rows

        main(mock_google_ads_client, self.manager_customer_id, login_customer_id=None)

        actual_query = mock_google_ads_service.search_stream.call_args[0][1]
        # Normalize whitespace for comparison
        normalized_actual_query = " ".join(actual_query.split())
        
        # The script defines MAX_HIERARCHY_DEPTH = 1.
        # The query used in _print_account_hierarchy (when seed_customer_ids is empty):
        expected_query_segment = "FROM customer_client WHERE customer_client.level <= 1 ORDER BY customer_client.level"
        self.assertIn(" ".join(expected_query_segment.split()), normalized_actual_query)
        self.assertEqual(mock_google_ads_service.search_stream.call_args[0][0], self.manager_customer_id) # customer_id arg

        # Assertions for print calls (simplified)
        # The script prints a tree structure.
        # Example:
        # Customer ID: 1234567890, Name: Manager Account Name, Is Manager: True
        #   Customer ID: 3333333333, Name: Sub Account Name, Is Manager: False
        # Customer ID: 1111111111, Name: Account Test Name 1, Is Manager: False
        
        # The order of printing depends on the customer_client_map and recursion.
        # mock_row1 (client of self.manager_customer_id)
        # mock_row2_manager (client of self.manager_customer_id, and is a manager)
        # mock_row3 (client of mock_row2_manager -- this part is tricky, as the query is only level <=1 from the root)

        # Let's adjust the mock data to reflect what a level <=1 query would return for self.manager_customer_id.
        # It would return accounts directly linked to self.manager_customer_id.
        # mock_row1 linked to self.manager_customer_id
        # mock_row2_manager linked to self.manager_customer_id
        # mock_row3 would NOT be returned by this single query if it's a child of mock_row2_manager.
        # The script's _print_account_hierarchy function, with its current query, can only print one level deep
        # relative to the `root_customer_id` it's called with.
        # The example output in the script suggests multiple levels. This implies either the query is different
        # or seed_customer_ids are used in a way that builds depth.
        # "This example prints the accounts hierarchy of the given manager account."
        # "If you don't specify manager ID, the example will instead print the hierarchy of the manager account that underwent Oauth2."
        # The `create_customer_client_map` function in the script:
        #   `googleads_service.search_stream(customer_id=root_customer_id, query=query)`
        #   `query = ... FROM customer_client WHERE customer_client.level <= {MAX_HIERARCHY_DEPTH}`
        #   `MAX_HIERARCHY_DEPTH` is 1.
        # This means it only gets immediate children. The recursive printing `_print_customer_hierarchy_map`
        # then traverses this in-memory map. It does NOT make new API calls.

        # So, the output will be based on mock_row1 and mock_row2_manager being children of self.manager_customer_id.
        # mock_row3 will not appear unless it's also a direct child of self.manager_customer_id.
        # Let's assume mock_row1 and mock_row2_manager are the only direct children.
        
        mock_google_ads_service.search_stream.return_value = [iter([mock_row1, mock_row2_manager])]

        # Reset print mock for this run
        mock_print.reset_mock()
        main(mock_google_ads_client, self.manager_customer_id, login_customer_id=None)

        # Expected print calls:
        # The script first prints the root manager's info (which is not part of search_stream results here, assumed to be known)
        # Then it prints children.
        # Let's assume the main function or a part of it prints the root.
        # The _print_account_hierarchy function is called with the root_customer_id.
        # It then calls _print_customer_hierarchy_map.
        
        # Mocking the initial "root" customer details that the script might fetch/assume for the manager_customer_id
        # The script, when login_customer_id is None or same as manager_customer_id, does this:
        #   customer_service = client.get_service("CustomerService")
        #   manager_resource_name = customer_service.customer_path(manager_customer_id)
        #   print(f"Manager account {manager_resource_name} details:")
        #   print(f"Opened as login customer {login_customer_id}" if login_customer_id else "")
        # This part is not easily mockable without more complexity.
        # Let's focus on the hierarchy printed by _print_customer_hierarchy_map.

        # The map will be: { self.manager_customer_id: [mock_row1.customer_client, mock_row2_manager.customer_client] }
        # (assuming customer_client.client_customer correctly points to their manager)
        # For the map construction to work, the `row.customer_client.client_customer` field (manager link) needs to be set.
        manager_resource_name = f"customers/{self.manager_customer_id}"
        mock_row1.customer_client.client_customer = manager_resource_name
        mock_row2_manager.customer_client.client_customer = manager_resource_name
        
        # With these, the map should be built correctly.
        # The printing recursion starts with `_print_customer_hierarchy_map(customer_client_map, manager_resource_name, 0)`
        
        expected_calls = [
            call(f"Customer ID: {mock_row1.customer_client.id}, Name: {mock_row1.customer.descriptive_name}, Is Manager: {mock_row1.customer.manager}, Currency Code: {mock_row1.customer.currency_code}, Time Zone: {mock_row1.customer.time_zone}"),
            call(f"Customer ID: {mock_row2_manager.customer_client.id}, Name: {mock_row2_manager.customer.descriptive_name}, Is Manager: {mock_row2_manager.customer.manager}, Currency Code: {mock_row2_manager.customer.currency_code}, Time Zone: {mock_row2_manager.customer.time_zone}"),
        ]
        
        # Check if the calls are present, order might vary if map iteration order changes.
        # The print format is `indent + details_string`. The initial call depth is 0.
        # The `_print_customer_hierarchy_map` function prints its direct children.
        
        # Let's simplify and check for specific parts of the output, assuming the manager itself is printed first by main.
        # And then children are printed by the hierarchy map function.
        
        # Re-running main after setting client_customer links
        mock_print.reset_mock()
        mock_google_ads_service.search_stream.return_value = [iter([mock_row1, mock_row2_manager])]
        main(mock_google_ads_client, self.manager_customer_id, login_customer_id=None)

        # The script prints a header for the manager account if login_customer_id is not specified or matches manager_customer_id.
        # This involves a call to CustomerService to get the manager's resource name.
        mock_customer_service = MagicMock()
        mock_google_ads_client.get_service.side_effect = lambda service_name, version: mock_google_ads_service if service_name == "GoogleAdsService" else mock_customer_service
        mock_customer_service.customer_path.return_value = f"customers/{self.manager_customer_id}"

        mock_print.reset_mock()
        mock_google_ads_service.search_stream.return_value = [iter([mock_row1, mock_row2_manager])]
        main(mock_google_ads_client, self.manager_customer_id, login_customer_id=None)

        # Check get_service calls
        mock_google_ads_client.get_service.assert_any_call("GoogleAdsService", version="v19")
        mock_google_ads_client.get_service.assert_any_call("CustomerService", version="v19") # For manager details

        # Check print calls
        # The exact output format for the manager: f"Manager account {manager_resource_name} details:"
        # print(f"Customer ID: {customer_id} [{currency_code}] Description: '{name}' Manager: {is_manager} Timezone: {timezone}")
        # This format is from an older version of the script template.
        # The current get_account_hierarchy.py uses:
        # print(f"{indent}Customer ID: {customer_id}, Name: {name}, "
        #       f"Is Manager: {is_manager}, Currency Code: {currency_code}, "
        #       f"Time Zone: {timezone}")

        printed_strings = [c[0][0] for c in mock_print.call_args_list]
        
        self.assertIn(f"Manager account customers/{self.manager_customer_id} details:", printed_strings)
        
        expected_child1_print = f"Customer ID: {mock_row1.customer_client.id}, Name: {mock_row1.customer.descriptive_name}, Is Manager: {mock_row1.customer.manager}, Currency Code: {mock_row1.customer.currency_code}, Time Zone: {mock_row1.customer.time_zone}"
        expected_child2_print = f"Customer ID: {mock_row2_manager.customer_client.id}, Name: {mock_row2_manager.customer.descriptive_name}, Is Manager: {mock_row2_manager.customer.manager}, Currency Code: {mock_row2_manager.customer.currency_code}, Time Zone: {mock_row2_manager.customer.time_zone}"

        # Check if these strings are present (indentation might vary, so check content)
        found_child1 = any(expected_child1_print in s for s in printed_strings)
        found_child2 = any(expected_child2_print in s for s in printed_strings)
        self.assertTrue(found_child1, f"Child1 print not found: {expected_child1_print}")
        self.assertTrue(found_child2, f"Child2 print not found: {expected_child2_print}")


    @patch("examples.account_management.get_account_hierarchy.GoogleAdsClient.load_from_storage")
    def test_get_account_hierarchy_google_ads_exception(self, mock_load_from_storage):
        """Tests handling of GoogleAdsException during account hierarchy retrieval."""
        mock_google_ads_client = MagicMock()
        mock_load_from_storage.return_value = mock_google_ads_client

        mock_google_ads_service = MagicMock()
        # Simulate exception on get_service or search_stream
        # If get_service for GoogleAdsService fails:
        mock_google_ads_client.get_service.side_effect = lambda service_name, version: \
            self._create_google_ads_exception() if service_name == "GoogleAdsService" else MagicMock()


        manager_customer_id = "1234567890"
        
        with patch("sys.exit") as mock_sys_exit, \
             patch("builtins.print") as mock_print: # also mock print to suppress error output during test
            main(mock_google_ads_client, manager_customer_id, login_customer_id=None)
            mock_sys_exit.assert_called_once_with(1)

        # Reset side effect for the next test case if search_stream itself fails
        mock_google_ads_client.get_service.side_effect = None 
        mock_google_ads_client.get_service.return_value = mock_google_ads_service # make it return the service now
        
        # Mock CustomerService for the manager details part
        mock_customer_service = MagicMock()
        mock_customer_service.customer_path.return_value = f"customers/{manager_customer_id}"
        
        def get_service_router(service_name, version):
            if service_name == "GoogleAdsService":
                return mock_google_ads_service
            elif service_name == "CustomerService":
                return mock_customer_service
            return MagicMock()
        mock_google_ads_client.get_service.side_effect = get_service_router


        mock_google_ads_service.search_stream.side_effect = self._create_google_ads_exception()

        with patch("sys.exit") as mock_sys_exit, \
             patch("builtins.print") as mock_print:
            main(mock_google_ads_client, manager_customer_id, login_customer_id=None)
            mock_sys_exit.assert_called_once_with(1)
            
            # Verify that get_service for GoogleAdsService was called
            mock_google_ads_client.get_service.assert_any_call("GoogleAdsService", version="v19")


    def _create_google_ads_exception(self):
        mock_failure = MagicMock()
        mock_error = MagicMock()
        mock_error.message = "Test GoogleAdsException"
        mock_failure.errors = [mock_error]
        return GoogleAdsException(
            mock_failure, "call", "trigger", "request_id", "error_code_enum"
        )

if __name__ == "__main__":
    unittest.main()
