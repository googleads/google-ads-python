import unittest
from unittest.mock import patch, MagicMock
import io
import sys

from examples.account_management import list_accessible_customers
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.v19.services.services.customer_service import CustomerServiceClient
# The script uses ListAccessibleCustomersResponse, but we only need to mock its relevant attribute.

class TestListAccessibleCustomers(unittest.TestCase):

    @patch('examples.account_management.list_accessible_customers.GoogleAdsClient')
    def test_main_prints_accessible_customers(self, mock_google_ads_client_class):
        # 1. Setup Mocks
        mock_client_instance = MagicMock(spec=GoogleAdsClient)
        mock_google_ads_client_class.load_from_storage.return_value = mock_client_instance

        mock_customer_service = MagicMock(spec=CustomerServiceClient)
        mock_client_instance.get_service.return_value = mock_customer_service

        # Mock the response from list_accessible_customers
        # It should be an object with a 'resource_names' attribute (list of strings)
        mock_list_response = MagicMock()
        mock_customer_resource_names = [
            "customers/1234567890",
            "customers/0987654321",
            "customers/1122334455"
        ]
        mock_list_response.resource_names = mock_customer_resource_names
        mock_customer_service.list_accessible_customers.return_value = mock_list_response

        # 2. Capture stdout
        captured_output = io.StringIO()
        sys.stdout = captured_output

        # 3. Call the main function (takes the client as an argument)
        list_accessible_customers.main(mock_client_instance)

        # 4. Restore stdout
        sys.stdout = sys.__stdout__

        # 5. Assertions
        # Assert get_service was called
        mock_client_instance.get_service.assert_called_once_with("CustomerService")

        # Assert list_accessible_customers was called
        mock_customer_service.list_accessible_customers.assert_called_once_with() # No arguments

        # Verify printed output
        output = captured_output.getvalue()

        expected_lines = [f"Total results: {len(mock_customer_resource_names)}\n"]
        for resource_name in mock_customer_resource_names:
            expected_lines.append(f'Customer resource name: "{resource_name}"\n')

        expected_output = "".join(expected_lines)
        self.assertEqual(output, expected_output)

if __name__ == "__main__":
    unittest.main()
