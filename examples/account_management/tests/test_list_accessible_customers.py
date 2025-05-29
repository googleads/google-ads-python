import unittest
from unittest.mock import patch, Mock, MagicMock
import sys
import io

from google.ads.googleads.errors import GoogleAdsException
from google.ads.googleads.v19.services.types.customer_service import ListAccessibleCustomersResponse

# Assuming list_accessible_customers.py is in examples.account_management
# The prompt refers to examples.list_accessible_customers, but the path should be examples.account_management.list_accessible_customers
from examples.account_management.list_accessible_customers import main as list_accessible_customers_main

class TestListAccessibleCustomers(unittest.TestCase):
    @patch('examples.account_management.list_accessible_customers.GoogleAdsClient')
    def setUp(self, mock_google_ads_client_class):
        # This mock_google_ads_client_class is the patched class itself.
        # We need to configure its load_from_storage method to return our client instance.
        self.mock_google_ads_client = MagicMock()
        mock_google_ads_client_class.load_from_storage.return_value = self.mock_google_ads_client
        
        # Mock CustomerService
        self.mock_customer_service = MagicMock()
        self.mock_google_ads_client.get_service.return_value = self.mock_customer_service

        # Capture stdout
        self.held_stdout = sys.stdout
        sys.stdout = io.StringIO()

    def tearDown(self):
        sys.stdout = self.held_stdout # Restore stdout
        patch.stopall() # Stop all patches started with @patch

    def test_main_success_lists_customers(self):
        # Configure list_accessible_customers to return a mock response
        mock_response = ListAccessibleCustomersResponse()
        mock_response.resource_names = ["customers/123", "customers/456", "customers/789"]
        self.mock_customer_service.list_accessible_customers.return_value = mock_response

        list_accessible_customers_main(self.mock_google_ads_client)

        # Assertions
        self.mock_google_ads_client.get_service.assert_called_once_with("CustomerService", version="v19")
        self.mock_customer_service.list_accessible_customers.assert_called_once()
        
        output = sys.stdout.getvalue()
        self.assertIn("Total results: 3", output)
        self.assertIn("customers/123", output)
        self.assertIn("customers/456", output)
        self.assertIn("customers/789", output)

    def test_main_success_no_customers(self):
        # Configure list_accessible_customers to return an empty list
        mock_response = ListAccessibleCustomersResponse()
        mock_response.resource_names = []
        self.mock_customer_service.list_accessible_customers.return_value = mock_response

        list_accessible_customers_main(self.mock_google_ads_client)

        # Assertions
        self.mock_google_ads_client.get_service.assert_called_once_with("CustomerService", version="v19")
        self.mock_customer_service.list_accessible_customers.assert_called_once()
        
        output = sys.stdout.getvalue()
        self.assertIn("Total results: 0", output)
        # Ensure no customer IDs are printed by checking for "customers/" prefix absence or specific non-presence
        self.assertNotIn("customers/", output.replace("Total results: 0\n", ""))

    @patch('sys.exit') # To check if sys.exit is called
    def test_main_google_ads_exception(self, mock_sys_exit):
        # Configure list_accessible_customers to raise GoogleAdsException
        mock_error_payload = MagicMock() # For GoogleAdsException.failure.errors[0]
        mock_error_payload.message = "Test GoogleAdsException from list_accessible_customers"
        mock_failure = MagicMock()
        mock_failure.errors = [mock_error_payload]
        
        google_ads_exception = GoogleAdsException(
            error=None, # Original gRPC error
            call=None,  # gRPC call object
            failure=mock_failure,
            error_code=None, # More specific error code
            message="Simulated GoogleAdsException during list_accessible_customers"
        )
        self.mock_customer_service.list_accessible_customers.side_effect = google_ads_exception

        list_accessible_customers_main(self.mock_google_ads_client)

        mock_sys_exit.assert_called_once_with(1)
        output = sys.stdout.getvalue()
        
        # Check for parts of the generic GoogleAdsException message format
        self.assertIn("Request with ID", output) 
        # Check for the specific error message
        self.assertIn("Test GoogleAdsException from list_accessible_customers", output)
        
        self.mock_customer_service.list_accessible_customers.assert_called_once()

    @patch('examples.account_management.list_accessible_customers.main') # Mock the script's main function
    @patch('examples.account_management.list_accessible_customers.GoogleAdsClient.load_from_storage') # Mock client loading for __main__
    def test_argument_parser_and_run(self, mock_load_from_storage, mock_script_main_function):
        # Mock the client instance that load_from_storage would return in the script's __main__
        mock_script_client_instance = MagicMock()
        mock_load_from_storage.return_value = mock_script_client_instance

        # The script's __main__ block might look like:
        # if __name__ == "__main__":
        #     googleads_client = GoogleAdsClient.load_from_storage()
        #     main(googleads_client)
        # We need to execute this block.

        # Execute the script's main block using runpy
        import runpy
        runpy.run_module("examples.account_management.list_accessible_customers", run_name="__main__")

        # Assert that GoogleAdsClient.load_from_storage was called by the script's __main__
        mock_load_from_storage.assert_called_once()
        
        # Assert that the script's main function (which is mocked) was called with the loaded client
        mock_script_main_function.assert_called_once_with(mock_script_client_instance)


if __name__ == "__main__":
    unittest.main()
