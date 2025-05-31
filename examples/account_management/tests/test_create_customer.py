import unittest
from unittest.mock import patch, MagicMock
import io
import sys
from datetime import datetime

# Assuming create_customer.py is in the parent directory and can be imported.
from examples.account_management import create_customer

class TestCreateCustomer(unittest.TestCase):

    @patch('examples.account_management.create_customer.datetime')
    @patch('examples.account_management.create_customer.GoogleAdsClient')
    def test_main_creates_customer_correctly(self, mock_google_ads_client_class, mock_datetime):
        # 1. Setup Mocks
        mock_client_instance = MagicMock()
        mock_google_ads_client_class.load_from_storage.return_value = mock_client_instance

        mock_customer_service = MagicMock()
        mock_client_instance.get_service.return_value = mock_customer_service

        # Mock the response from create_customer_client
        mock_create_customer_response = MagicMock()
        mock_create_customer_response.resource_name = "customers/1234567890"
        mock_customer_service.create_customer_client.return_value = mock_create_customer_response

        # Mock datetime
        mock_now = datetime(2024, 1, 1, 12, 0, 0)
        mock_datetime.today.return_value = mock_now
        expected_descriptive_name = f"Account created with CustomerService on {mock_now.strftime('%Y%m%d %H:%M:%S')}"

        # 2. Prepare arguments for the main function
        manager_customer_id = "manager-123"

        # Expected values based on create_customer.py
        expected_currency_code = "USD"
        expected_time_zone = "America/New_York"
        expected_tracking_url_template = "{lpurl}?device={device}"
        expected_final_url_suffix = "keyword={keyword}&matchtype={matchtype}&adgroupid={adgroupid}"

        # 3. Capture stdout
        captured_output = io.StringIO()
        sys.stdout = captured_output

        # 4. Call the main function
        create_customer.main(
            mock_client_instance,
            manager_customer_id
        )

        # 5. Restore stdout
        sys.stdout = sys.__stdout__

        # 6. Assertions
        mock_client_instance.get_service.assert_called_once_with("CustomerService")

        # Assert create_customer_client was called correctly
        mock_customer_service.create_customer_client.assert_called_once()
        args, kwargs = mock_customer_service.create_customer_client.call_args

        self.assertEqual(kwargs.get('customer_id'), manager_customer_id)

        customer_arg = kwargs.get('customer_client') # Argument name is customer_client
        self.assertIsNotNone(customer_arg)
        self.assertEqual(customer_arg.descriptive_name, expected_descriptive_name)
        self.assertEqual(customer_arg.currency_code, expected_currency_code)
        self.assertEqual(customer_arg.time_zone, expected_time_zone)
        self.assertEqual(customer_arg.tracking_url_template, expected_tracking_url_template)
        self.assertEqual(customer_arg.final_url_suffix, expected_final_url_suffix)

        # Assert the output
        expected_output = (
            f'Customer created with resource name "{mock_create_customer_response.resource_name}" '
            f'under manager account with ID "{manager_customer_id}".\n' # Added newline
        )
        self.assertEqual(captured_output.getvalue(), expected_output)

if __name__ == "__main__":
    unittest.main()
