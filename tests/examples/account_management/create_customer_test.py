import unittest
from unittest.mock import patch, MagicMock

from google.ads.googleads.errors import GoogleAdsException
# This import assumes that the test runner will add the root directory to sys.path
# or that the `examples` directory is otherwise findable.
from examples.account_management.create_customer import main


class CreateCustomerTest(unittest.TestCase):

    @patch("examples.account_management.create_customer.GoogleAdsClient.load_from_storage")
    def test_create_customer_success(self, mock_load_from_storage):
        """Tests the successful creation of a customer."""
        # Create a mock GoogleAdsClient
        mock_google_ads_client = MagicMock()
        mock_load_from_storage.return_value = mock_google_ads_client

        # Create a mock CustomerService
        mock_customer_service = MagicMock()
        mock_google_ads_client.get_service.return_value = mock_customer_service

        # Mock the create_customer_client method to return a mock response object
        # This response object structure might need adjustment based on what the actual method returns
        # and what the main function does with it. For now, a simple MagicMock.
        mock_create_customer_response = MagicMock()
        mock_create_customer_response.resource_name = "customers/1234567890/customerClients/9876543210"
        mock_customer_service.create_customer_client.return_value = mock_create_customer_response

        # Define test arguments
        manager_customer_id = "1234567890"
        currency_code = "USD"
        time_zone = "America/New_York"
        # The descriptive_name is optional in the script, so we'll test with it.
        descriptive_name = "Test Customer"

        # Call the main function with test arguments
        # The original script takes client_customer_id as an argument, but it's not used.
        # The create_customer.py script expects:
        # main(client, manager_customer_id, currency_code, time_zone, descriptive_name=None)
        # We are mocking the client, so we pass the mock_google_ads_client
        main(
            mock_google_ads_client,
            manager_customer_id,
            currency_code,
            time_zone,
            descriptive_name,
        )

        # Assert that get_service was called with the correct service name and version
        mock_google_ads_client.get_service.assert_called_once_with(
            "CustomerService", version="v19"
        )

        # Assert that create_customer_client was called once with the correct parameters
        # The original script builds a CustomerClient object. We need to check the attributes
        # of the customer_client argument passed to create_customer_client.
        self.assertEqual(mock_customer_service.create_customer_client.call_count, 1)
        call_args = mock_customer_service.create_customer_client.call_args
        
        # call_args is a tuple (args, kwargs). We expect (customer_id, customer_client, modify)
        # or (request=...) if using a request object.
        # The script uses: customer_service.create_customer_client(customer_id=manager_customer_id, customer_client=customer_client)
        self.assertEqual(call_args[1]['customer_id'], manager_customer_id)
        
        # Check the customer_client object passed
        customer_client_arg = call_args[1]['customer_client']
        self.assertEqual(customer_client_arg.descriptive_name, descriptive_name)
        self.assertEqual(customer_client_arg.currency_code, currency_code)
        self.assertEqual(customer_client_arg.time_zone, time_zone)
        # The original script also sets client_customer.applied_labels, but only if an optional
        # "labels" argument is provided to main(). We are not testing that here.


    @patch("examples.account_management.create_customer.GoogleAdsClient.load_from_storage")
    def test_create_customer_google_ads_exception(self, mock_load_from_storage):
        """Tests handling of GoogleAdsException during customer creation."""
        mock_google_ads_client = MagicMock()
        mock_load_from_storage.return_value = mock_google_ads_client

        mock_customer_service = MagicMock()
        mock_google_ads_client.get_service.return_value = mock_customer_service

        # Configure create_customer_client to raise GoogleAdsException
        # The exception needs to be instantiated with a failure object.
        # We can mock the failure object and its errors.
        mock_failure = MagicMock()
        mock_error = MagicMock()
        mock_error.message = "Test GoogleAdsException"
        mock_failure.errors = [mock_error]
        google_ads_exception = GoogleAdsException(
            mock_failure, "call", "trigger", "request_id", "error_code_enum"
        )
        mock_customer_service.create_customer_client.side_effect = google_ads_exception

        manager_customer_id = "1234567890"
        currency_code = "USD"
        time_zone = "America/New_York"
        descriptive_name = "Test Customer Exception"
        
        # We expect the main function to catch the GoogleAdsException and print an error message.
        # To verify this, we can check if sys.exit(1) is called, or if specific error logging occurs.
        # For simplicity, we'll assert that the exception is indeed raised and propagated
        # to the test if not caught, or if caught, that the program exits or logs.
        # The script's main function has a try-except block that prints the error and calls sys.exit(1).
        # We can mock sys.exit to check if it's called.
        with patch("sys.exit") as mock_sys_exit:
            main(
                mock_google_ads_client,
                manager_customer_id,
                currency_code,
                time_zone,
                descriptive_name,
            )
            # Assert that sys.exit was called, implying the exception was caught.
            mock_sys_exit.assert_called_once_with(1)

        mock_google_ads_client.get_service.assert_called_once_with(
            "CustomerService", version="v19"
        )
        mock_customer_service.create_customer_client.assert_called_once()


if __name__ == "__main__":
    unittest.main()
