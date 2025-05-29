import unittest
from unittest.mock import patch, MagicMock
import argparse
import sys
from datetime import datetime
import io
import runpy

from google.ads.googleads.errors import GoogleAdsException

# Assuming create_customer.py is in examples.account_management
from examples.account_management.create_customer import main


class TestCreateCustomer(unittest.TestCase):
    @patch('examples.account_management.create_customer.datetime')
    @patch('examples.account_management.create_customer.GoogleAdsClient.load_from_storage')
    def test_main_success(self, mock_load_from_storage, mock_datetime):
        # Mock the GoogleAdsClient instance and its methods
        mock_google_ads_client = MagicMock()
        mock_load_from_storage.return_value = mock_google_ads_client # load_from_storage returns the client instance
        mock_customer_service = MagicMock()
        mock_google_ads_client.get_service.return_value = mock_customer_service
        mock_create_customer_response = MagicMock()
        mock_create_customer_response.resource_name = "customers/1234567890/conversionActions/test_client_customer_id"
        mock_customer_service.create_customer_client.return_value = mock_create_customer_response

        # Mock datetime
        mock_datetime.today.return_value.strftime.return_value = "2023-10-27"

        manager_customer_id = "test_manager_id"
        
        # Capture stdout
        captured_output = io.StringIO()
        sys.stdout = captured_output

        # Call main with the mocked client instance and manager_customer_id
        main(mock_google_ads_client, manager_customer_id)

        # Reset stdout
        sys.stdout = sys.__stdout__

        mock_load_from_storage.assert_called_once() # Assert that load_from_storage was called to get the client
        mock_google_ads_client.get_service.assert_called_once_with("CustomerService")
        
        # Assert create_customer_client was called with the correct arguments
        call_args = mock_customer_service.create_customer_client.call_args
        self.assertIsNotNone(call_args) # Ensure it was called
        args, kwargs = call_args
        self.assertEqual(kwargs['customer_id'], manager_customer_id)
        
        customer_client_arg = args[0] 
        self.assertEqual(customer_client_arg.descriptive_name, "Account created with CustomerService on 2023-10-27")
        self.assertEqual(customer_client_arg.currency_code, "USD")
        self.assertEqual(customer_client_arg.time_zone, "America/New_York")
        self.assertEqual(customer_client_arg.tracking_url_template, None)
        self.assertEqual(customer_client_arg.final_url_suffix, None)

        self.assertIn(
            "New customer account with resource name 'customers/1234567890/conversionActions/test_client_customer_id' under manager account 'test_manager_id' was created.",
            captured_output.getvalue()
        )

    @patch('examples.account_management.create_customer.GoogleAdsClient.load_from_storage')
    @patch('sys.exit')
    def test_main_google_ads_exception(self, mock_sys_exit, mock_load_from_storage):
        # Mock the GoogleAdsClient instance and its methods
        mock_google_ads_client = MagicMock()
        mock_load_from_storage.return_value = mock_google_ads_client
        mock_customer_service = MagicMock()
        mock_google_ads_client.get_service.return_value = mock_customer_service

        # Configure create_customer_client to raise GoogleAdsException
        mock_error = MagicMock()
        mock_error.message = "Test GoogleAdsException message"
        mock_failure = MagicMock()
        mock_failure.errors = [mock_error]
        google_ads_exception = GoogleAdsException(
            error=None, # This should be the original gRPC error object if available
            call=None, # This should be the gRPC call object if available
            failure=mock_failure,
            error_code=None, # This could be a more specific error code if available
            message="Test GoogleAdsException"
        )
        mock_customer_service.create_customer_client.side_effect = google_ads_exception

        manager_customer_id = "test_manager_id"

        # Capture stdout
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        # Call main with the mocked client instance and manager_customer_id
        main(mock_google_ads_client, manager_customer_id)

        # Reset stdout
        sys.stdout = sys.__stdout__

        mock_load_from_storage.assert_called_once()
        mock_google_ads_client.get_service.assert_called_once_with("CustomerService")
        mock_customer_service.create_customer_client.assert_called_once()
        mock_sys_exit.assert_called_with(1)

        output = captured_output.getvalue()
        self.assertIn(f"Request with ID", output) 
        self.assertIn(f"Test GoogleAdsException message", output)

    @patch('argparse.ArgumentParser.parse_args')
    @patch('examples.account_management.create_customer.main')
    @patch('examples.account_management.create_customer.GoogleAdsClient.load_from_storage') # Also mock client loading for the script's main execution
    def test_argument_parser(self, mock_load_from_storage, mock_main_function, mock_parse_args):
        # Simulate command line arguments
        test_manager_id = "12345"
        sys.argv = ["create_customer.py", "-m", test_manager_id]

        # Mock parse_args to return the manager_customer_id
        mock_parse_args.return_value = argparse.Namespace(manager_customer_id=test_manager_id)
        
        # Mock the client returned by load_from_storage
        mock_google_ads_client_instance = MagicMock()
        mock_load_from_storage.return_value = mock_google_ads_client_instance

        # Execute the script's main block using runpy
        # This will trigger the argument parsing and the call to main() within the script
        runpy.run_module("examples.account_management.create_customer", run_name="__main__")

        mock_parse_args.assert_called_once()
        # The main function in create_customer.py is called with the client and manager_id
        mock_main_function.assert_called_once_with(mock_google_ads_client_instance, test_manager_id)
