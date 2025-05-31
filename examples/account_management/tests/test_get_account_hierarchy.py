import unittest
from unittest.mock import patch, MagicMock
import io
import sys

from examples.account_management import get_account_hierarchy
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.v19.services.services.customer_service import CustomerServiceClient
from google.ads.googleads.v19.services.services.google_ads_service import GoogleAdsServiceClient
# Re-attempting import from v19 based on `ls` output.
# Previous error was "No module named 'google.ads.googleads.v19.types'".
# Trying "google.ads.googleads.v19.services.types" instead.
from google.ads.googleads.v19.services.types import GoogleAdsRow


class TestGetAccountHierarchy(unittest.TestCase):

    @patch('examples.account_management.get_account_hierarchy.GoogleAdsClient')
    def test_main_prints_hierarchy_correctly_with_manager_id(self, mock_google_ads_client_class):
        # 1. Setup Mocks
        mock_client_instance = MagicMock(spec=GoogleAdsClient)
        mock_google_ads_client_class.load_from_storage.return_value = mock_client_instance

        mock_google_ads_service = MagicMock(spec=GoogleAdsServiceClient)
        # This mock is only used if login_customer_id is None in main()
        mock_customer_service = MagicMock(spec=CustomerServiceClient)

        def get_service_side_effect(service_name, version=None): # Script doesn't pass version
            if service_name == "GoogleAdsService":
                return mock_google_ads_service
            elif service_name == "CustomerService":
                return mock_customer_service
            raise ValueError(f"Unexpected service requested: {service_name}")

        mock_client_instance.get_service.side_effect = get_service_side_effect

        # 2. Prepare arguments for the main function
        login_manager_id_str = "1000"

        # 3. Mock responses for GoogleAdsService.search()
        # This function is called in a loop by the script's BFS logic.
        # The query is fixed in the script; behavior changes based on the 'customer_id' argument to search().
        def mock_search_logic(*, customer_id, query): # Use keyword args to match GoogleAdsService.search
            response_rows = []

            # Simulate response for initial call with login_manager_id_str (e.g., "1000")
            if customer_id == login_manager_id_str:
                # Manager M (ID 1000) - this is the root_customer_client
                row_m = GoogleAdsRow()
                row_m.customer_client.id = 1000
                row_m.customer_client.descriptive_name = "Manager Account M"
                row_m.customer_client.currency_code = "USD"
                row_m.customer_client.time_zone = "America/New_York"
                row_m.customer_client.level = 0
                row_m.customer_client.manager = True # Manager M is a manager
                response_rows.append(row_m)

                # Child C1 (ID 2000) of Manager M - level 1 relative to M
                row_c1 = GoogleAdsRow()
                row_c1.customer_client.id = 2000
                row_c1.customer_client.descriptive_name = "Child Account C1"
                row_c1.customer_client.currency_code = "USD"
                row_c1.customer_client.time_zone = "America/Los_Angeles"
                row_c1.customer_client.level = 1
                row_c1.customer_client.manager = True # C1 is also a manager
                response_rows.append(row_c1)

                # Child C2 (ID 3000) of Manager M - level 1 relative to M
                row_c2 = GoogleAdsRow()
                row_c2.customer_client.id = 3000
                row_c2.customer_client.descriptive_name = "Child Account C2"
                row_c2.customer_client.currency_code = "EUR"
                row_c2.customer_client.time_zone = "Europe/London"
                row_c2.customer_client.level = 1
                row_c2.customer_client.manager = False # C2 is NOT a manager
                response_rows.append(row_c2)

            # Simulate response when script calls search for customer_id "2000" (Child C1)
            elif customer_id == "2000":
                # Child C1 (ID 2000) itself - now as level 0 in this context
                row_c1_self = GoogleAdsRow()
                row_c1_self.customer_client.id = 2000
                row_c1_self.customer_client.descriptive_name = "Child Account C1"
                row_c1_self.customer_client.currency_code = "USD"
                row_c1_self.customer_client.time_zone = "America/Los_Angeles"
                row_c1_self.customer_client.level = 0
                row_c1_self.customer_client.manager = True
                response_rows.append(row_c1_self)

                # Grandchild GC1 (ID 4000) of M, child of C1 - level 1 relative to C1
                row_gc1 = GoogleAdsRow()
                row_gc1.customer_client.id = 4000
                row_gc1.customer_client.descriptive_name = "Grandchild Account GC1"
                row_gc1.customer_client.currency_code = "CAD"
                row_gc1.customer_client.time_zone = "America/Toronto"
                row_gc1.customer_client.level = 1
                row_gc1.customer_client.manager = False # GC1 is NOT a manager
                response_rows.append(row_gc1)

            # Simulate response for customer_id "3000" (Child C2)
            # C2 is not a manager, so the script processes it, finds its level 0 representation,
            # but doesn't add new entries to unprocessed_customer_ids from its children.
            elif customer_id == "3000":
                row_c2_self = GoogleAdsRow()
                row_c2_self.customer_client.id = 3000
                row_c2_self.customer_client.descriptive_name = "Child Account C2"
                row_c2_self.customer_client.currency_code = "EUR"
                row_c2_self.customer_client.time_zone = "Europe/London"
                row_c2_self.customer_client.level = 0
                row_c2_self.customer_client.manager = False
                response_rows.append(row_c2_self)

            return iter(response_rows) # googleads_service.search returns an iterator

        mock_google_ads_service.search.side_effect = mock_search_logic

        # 4. Capture stdout
        captured_output = io.StringIO()
        sys.stdout = captured_output

        # 5. Call the main function from the script
        get_account_hierarchy.main(mock_client_instance, login_manager_id_str)

        # 6. Restore stdout
        sys.stdout = sys.__stdout__

        # 7. Assertions
        # list_accessible_customers should NOT be called when login_customer_id is provided
        mock_customer_service.list_accessible_customers.assert_not_called()

        # Assert that GoogleAdsService.search was called correctly
        # Call 1: customer_id="1000" (root manager)
        # Call 2: customer_id="2000" (Child C1, which is a manager)
        # Child C2 (ID 3000) is not a manager, so its ID is not added to unprocessed_customer_ids for a separate search call.
        self.assertEqual(mock_google_ads_service.search.call_count, 2)

        expected_query = """
        SELECT
          customer_client.client_customer,
          customer_client.level,
          customer_client.manager,
          customer_client.descriptive_name,
          customer_client.currency_code,
          customer_client.time_zone,
          customer_client.id
        FROM customer_client
        WHERE customer_client.level <= 1"""

        mock_google_ads_service.search.assert_any_call(customer_id=login_manager_id_str, query=expected_query)
        mock_google_ads_service.search.assert_any_call(customer_id="2000", query=expected_query)
        # The following call does not happen because customer "3000" is not a manager
        # mock_google_ads_service.search.assert_any_call(customer_id="3000", query=expected_query)

        # Verify the printed output
        output = captured_output.getvalue()

        expected_output_lines = [
            f"The hierarchy of customer ID {login_manager_id_str} is printed below:",
            "Customer ID (Descriptive Name, Currency Code, Time Zone)",
            "1000 (Manager Account M, USD, America/New_York)",
            "--2000 (Child Account C1, USD, America/Los_Angeles)",
            "----4000 (Grandchild Account GC1, CAD, America/Toronto)",
            "--3000 (Child Account C2, EUR, Europe/London)",
            "" # Ensure trailing newline
        ]
        expected_output = "\n".join(expected_output_lines)

        self.assertEqual(output, expected_output)

if __name__ == "__main__":
    unittest.main()
