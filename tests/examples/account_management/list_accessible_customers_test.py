import unittest
from unittest.mock import patch, MagicMock

from google.ads.googleads.errors import GoogleAdsException
from examples.account_management.list_accessible_customers import main


class ListAccessibleCustomersTest(unittest.TestCase):

    @patch("examples.account_management.list_accessible_customers.GoogleAdsClient.load_from_storage")
    def test_list_accessible_customers_success(self, mock_load_from_storage):
        """Tests the successful retrieval and printing of accessible customer resource names."""
        mock_google_ads_client = MagicMock()
        mock_load_from_storage.return_value = mock_google_ads_client

        mock_customer_service = MagicMock()
        mock_google_ads_client.get_service.return_value = mock_customer_service

        # Mock the response from list_accessible_customers
        mock_response = MagicMock()
        expected_resource_names = [
            "customers/1234567890",
            "customers/0987654321",
            "customers/1122334455",
        ]
        mock_response.resource_names = expected_resource_names
        mock_customer_service.list_accessible_customers.return_value = mock_response

        with patch("builtins.print") as mock_print:
            main(mock_google_ads_client)

        # Assert that get_service was called correctly
        mock_google_ads_client.get_service.assert_called_once_with(
            "CustomerService", version="v19"
        )

        # Assert that list_accessible_customers was called once
        # The script calls it with an empty ListAccessibleCustomersRequest object
        mock_customer_service.list_accessible_customers.assert_called_once()
        # Check that the request object passed is of the correct type if necessary,
        # but for this script, it's just an empty request, so checking the call is enough.

        # Assert that the resource names were printed
        # The script prints: "Accessible customer resource names:"
        # And then each resource name on a new line, prefixed by "- ".
        printed_strings = [c[0][0] for c in mock_print.call_args_list if c[0]]
        
        self.assertTrue(any("Accessible customer resource names:" in s for s in printed_strings))
        for resource_name in expected_resource_names:
            self.assertTrue(any(f"- {resource_name}" in s for s in printed_strings))


    @patch("examples.account_management.list_accessible_customers.GoogleAdsClient.load_from_storage")
    def test_list_accessible_customers_google_ads_exception(self, mock_load_from_storage):
        """Tests handling of GoogleAdsException during customer listing."""
        mock_google_ads_client = MagicMock()
        mock_load_from_storage.return_value = mock_google_ads_client

        mock_customer_service = MagicMock()
        mock_google_ads_client.get_service.return_value = mock_customer_service

        # Configure list_accessible_customers to raise GoogleAdsException
        mock_failure = MagicMock()
        mock_error = MagicMock()
        mock_error.message = "Test GoogleAdsException for list_accessible_customers"
        mock_failure.errors = [mock_error]
        google_ads_exception = GoogleAdsException(
            mock_failure, "call", "trigger", "request_id", "error_code_enum"
        )
        mock_customer_service.list_accessible_customers.side_effect = google_ads_exception

        with patch("sys.exit") as mock_sys_exit, \
             patch("builtins.print") as mock_error_print:
            main(mock_google_ads_client)
            
            mock_sys_exit.assert_called_once_with(1)
            # Check if the exception details were printed
            error_printed = False
            for call_args in mock_error_print.call_args_list:
                if "Test GoogleAdsException for list_accessible_customers" in call_args[0][0]:
                    error_printed = True
                    break
            self.assertTrue(error_printed, "GoogleAdsException details not printed to console.")

        mock_google_ads_client.get_service.assert_called_once_with(
            "CustomerService", version="v19"
        )
        mock_customer_service.list_accessible_customers.assert_called_once()


    @patch("examples.account_management.list_accessible_customers.GoogleAdsClient.load_from_storage")
    def test_list_accessible_customers_no_customers(self, mock_load_from_storage):
        """Tests the case where no accessible customers are found."""
        mock_google_ads_client = MagicMock()
        mock_load_from_storage.return_value = mock_google_ads_client

        mock_customer_service = MagicMock()
        mock_google_ads_client.get_service.return_value = mock_customer_service

        mock_response = MagicMock()
        mock_response.resource_names = [] # Empty list
        mock_customer_service.list_accessible_customers.return_value = mock_response

        with patch("builtins.print") as mock_print:
            main(mock_google_ads_client)

        printed_strings = [c[0][0] for c in mock_print.call_args_list if c[0]]
        # The script prints "No accessible customers found." if the list is empty.
        self.assertTrue(any("No accessible customers found." in s for s in printed_strings))
        # Ensure the header is still printed
        self.assertTrue(any("Accessible customer resource names:" in s for s in printed_strings))


if __name__ == "__main__":
    unittest.main()
