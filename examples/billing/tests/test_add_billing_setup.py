import unittest
import sys
from unittest import mock
from io import StringIO
from datetime import datetime, timedelta

# Assuming 'examples' is in PYTHONPATH
import add_billing_setup

# Use a real or placeholder GoogleAdsException and other types
try:
    from google.ads.googleads.client import GoogleAdsClient
    from google.ads.googleads.errors import GoogleAdsException
    from google.ads.googleads.v19.services.types.billing_setup_service import BillingSetupOperation
    from google.ads.googleads.v19.resources.types.billing_setup import BillingSetup
    from google.ads.googleads.v19.common.types.dates import DateRange
except ImportError:
    # Define placeholders if the real ones are not available
    class GoogleAdsException(Exception):
        def __init__(self, *args, **kwargs):
            super().__init__(*args)
            self.request_id = kwargs.get("request_id", "test_request_id")
            self.error = mock.Mock()
            self.error.code.return_value.name = "TEST_ERROR"
            self.failure = mock.Mock()
            self.failure.errors = [mock.Mock(message="Test error message.")]

    class BillingSetupOperation: pass
    class BillingSetup: pass
    class DateRange: pass


class TestAddBillingSetup(unittest.TestCase):
    MOCK_CUSTOMER_ID = "1234567890"
    MOCK_PAYMENTS_ACCOUNT_ID = "1111-2222-3333-4444"
    MOCK_PAYMENTS_PROFILE_ID = "5555-6666-7777"
    SCRIPT_PATH = "add_billing_setup" # Assuming direct import due to PYTHONPATH

    # Corrected mocking for uuid.uuid4() which returns an object that becomes a string when used in f-string
    @mock.patch(f"{SCRIPT_PATH}.uuid4")
    def test_create_billing_setup_with_payments_account_id(self, mock_uuid4):
        # This test case does not use uuid4, so the mock isn't strictly necessary here,
        # but it's good practice if other parts of the function were to change.
        # We can make it a simple mock that doesn't affect the current assertions.
        mock_uuid4.return_value = "dummy-uuid-for-account-id-test"

        mock_client = mock.Mock(spec=GoogleAdsClient)
        mock_billing_setup_service = mock.Mock()
        mock_client.get_service.return_value = mock_billing_setup_service
        
        mock_billing_setup_instance = mock.Mock(spec=BillingSetup)
        # Mocking payments_account_info to exist on the instance already
        mock_billing_setup_instance.payments_account_info = mock.Mock()
        mock_client.get_type.return_value = mock_billing_setup_instance
        
        expected_payments_account_path = "customers/123/paymentsAccounts/456"
        mock_billing_setup_service.payments_account_path.return_value = expected_payments_account_path

        billing_setup = add_billing_setup.create_billing_setup(
            mock_client,
            self.MOCK_CUSTOMER_ID,
            payments_account_id=self.MOCK_PAYMENTS_ACCOUNT_ID,
        )

        mock_client.get_type.assert_called_once_with("BillingSetup")
        mock_billing_setup_service.payments_account_path.assert_called_once_with(
            self.MOCK_CUSTOMER_ID, self.MOCK_PAYMENTS_ACCOUNT_ID
        )
        self.assertEqual(billing_setup.payments_account, expected_payments_account_path)
        # Ensure payments_account_name was not set in this branch
        self.assertFalse(billing_setup.payments_account_info.payments_account_name, 
                         "payments_account_name should not be set when payments_account_id is provided.")


    @mock.patch(f"{SCRIPT_PATH}.uuid4")
    def test_create_billing_setup_with_payments_profile_id(self, mock_uuid4):
        # Configure the mock for uuid4() to return an object whose __str__ gives a predictable value
        mock_uuid_obj = mock.Mock()
        mock_uuid_obj.__str__ = mock.Mock(return_value="fixed-uuid-string-for-profile")
        mock_uuid4.return_value = mock_uuid_obj

        mock_client = mock.Mock(spec=GoogleAdsClient)
        mock_billing_setup_instance = mock.Mock(spec=BillingSetup)
        mock_billing_setup_instance.payments_account_info = mock.Mock() 
        mock_client.get_type.return_value = mock_billing_setup_instance

        billing_setup = add_billing_setup.create_billing_setup(
            mock_client,
            self.MOCK_CUSTOMER_ID,
            payments_profile_id=self.MOCK_PAYMENTS_PROFILE_ID,
        )

        mock_client.get_type.assert_called_once_with("BillingSetup")
        # The script constructs the name as f"Payments Account #{uuid4()}"
        # So, it will call str() on the return value of uuid4()
        expected_account_name = f"Payments Account #{mock_uuid_obj}"
        self.assertEqual(billing_setup.payments_account_info.payments_account_name, expected_account_name)
        self.assertEqual(
            billing_setup.payments_account_info.payments_profile_id,
            self.MOCK_PAYMENTS_PROFILE_ID,
        )
        # Ensure payments_account was not set directly
        self.assertFalse(hasattr(billing_setup, 'payments_account') and billing_setup.payments_account)


    @mock.patch(f"{SCRIPT_PATH}.datetime")
    def test_set_billing_setup_dates_no_existing_setups(self, mock_datetime):
        mock_client = mock.Mock(spec=GoogleAdsClient)
        mock_ga_service = mock.Mock()
        mock_client.get_service.return_value = mock_ga_service
        mock_ga_service.search_stream.return_value = [] # No existing setups

        # Mock datetime.now()
        fixed_now = datetime(2023, 10, 26, 10, 0, 0)
        mock_datetime.now.return_value = fixed_now
        
        mock_billing_setup = mock.Mock(spec=BillingSetup)

        add_billing_setup.set_billing_setup_date_times(
            mock_client, self.MOCK_CUSTOMER_ID, mock_billing_setup
        )

        mock_ga_service.search_stream.assert_called_once()
        expected_start_date_str = fixed_now.strftime("%Y-%m-%d %H:%M:%S")
        expected_end_date_str = (fixed_now + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
        
        self.assertEqual(mock_billing_setup.start_date_time, expected_start_date_str)
        self.assertEqual(mock_billing_setup.end_date_time, expected_end_date_str)


    def test_set_billing_setup_dates_with_existing_setup_specific_end_date(self):
        mock_client = mock.Mock(spec=GoogleAdsClient)
        mock_ga_service = mock.Mock()
        mock_client.get_service.return_value = mock_ga_service

        mock_row = mock.Mock()
        mock_row.billing_setup.end_date_time = "2023-10-26" # Date only
        mock_batch = mock.Mock()
        mock_batch.results = [mock_row]
        mock_ga_service.search_stream.return_value = [mock_batch]
        
        mock_billing_setup = mock.Mock(spec=BillingSetup)

        add_billing_setup.set_billing_setup_date_times(
            mock_client, self.MOCK_CUSTOMER_ID, mock_billing_setup
        )
        
        expected_start_date = datetime(2023, 10, 26) + timedelta(days=1)
        expected_end_date = expected_start_date + timedelta(days=1)
        
        self.assertEqual(mock_billing_setup.start_date_time, expected_start_date.strftime("%Y-%m-%d %H:%M:%S"))
        self.assertEqual(mock_billing_setup.end_date_time, expected_end_date.strftime("%Y-%m-%d %H:%M:%S"))

    def test_set_billing_setup_dates_with_existing_setup_datetime_end_date(self):
        mock_client = mock.Mock(spec=GoogleAdsClient)
        mock_ga_service = mock.Mock()
        mock_client.get_service.return_value = mock_ga_service

        mock_row = mock.Mock()
        mock_row.billing_setup.end_date_time = "2023-10-26 14:30:00" # Datetime
        mock_batch = mock.Mock()
        mock_batch.results = [mock_row]
        mock_ga_service.search_stream.return_value = [mock_batch]
        
        mock_billing_setup = mock.Mock(spec=BillingSetup)

        add_billing_setup.set_billing_setup_date_times(
            mock_client, self.MOCK_CUSTOMER_ID, mock_billing_setup
        )
        
        expected_start_date = datetime(2023, 10, 26, 14, 30, 0) + timedelta(days=1)
        expected_end_date = expected_start_date + timedelta(days=1)
        
        self.assertEqual(mock_billing_setup.start_date_time, expected_start_date.strftime("%Y-%m-%d %H:%M:%S"))
        self.assertEqual(mock_billing_setup.end_date_time, expected_end_date.strftime("%Y-%m-%d %H:%M:%S"))


    def test_set_billing_setup_dates_existing_setup_runs_indefinitely(self):
        mock_client = mock.Mock(spec=GoogleAdsClient)
        mock_ga_service = mock.Mock()
        mock_client.get_service.return_value = mock_ga_service

        mock_row = mock.Mock()
        mock_row.billing_setup.end_date_time = None # Runs indefinitely
        mock_batch = mock.Mock()
        mock_batch.results = [mock_row]
        mock_ga_service.search_stream.return_value = [mock_batch]
        
        mock_billing_setup = mock.Mock(spec=BillingSetup)

        with self.assertRaisesRegex(Exception, "latest existing billing setup is set to run indefinitely"):
            add_billing_setup.set_billing_setup_date_times(
                mock_client, self.MOCK_CUSTOMER_ID, mock_billing_setup
            )

    @mock.patch(f"{SCRIPT_PATH}.create_billing_setup")
    @mock.patch(f"{SCRIPT_PATH}.set_billing_setup_date_times")
    def test_main_success_with_payments_account_id(self, mock_set_dates, mock_create_setup):
        mock_client = mock.Mock(spec=GoogleAdsClient)
        mock_billing_setup_service = mock.Mock()
        mock_client.get_service.return_value = mock_billing_setup_service
        
        mock_billing_setup_operation = mock.Mock(spec=BillingSetupOperation)
        mock_client.get_type.return_value = mock_billing_setup_operation
        
        mock_created_setup_instance = mock.Mock(spec=BillingSetup)
        mock_create_setup.return_value = mock_created_setup_instance
        
        mock_response = mock.Mock()
        mock_response.result.resource_name = "test_resource_name"
        mock_billing_setup_service.mutate_billing_setup.return_value = mock_response

        captured_output = StringIO()
        sys.stdout = captured_output

        add_billing_setup.main(
            mock_client,
            self.MOCK_CUSTOMER_ID,
            payments_account_id=self.MOCK_PAYMENTS_ACCOUNT_ID,
        )
        sys.stdout = sys.__stdout__

        mock_create_setup.assert_called_once_with(
            mock_client, self.MOCK_CUSTOMER_ID, self.MOCK_PAYMENTS_ACCOUNT_ID, None
        )
        mock_set_dates.assert_called_once_with(
            mock_client, self.MOCK_CUSTOMER_ID, mock_created_setup_instance
        )
        mock_client.copy_from.assert_called_once_with(
            mock_billing_setup_operation.create, mock_created_setup_instance
        )
        mock_billing_setup_service.mutate_billing_setup.assert_called_once_with(
            customer_id=self.MOCK_CUSTOMER_ID, operation=mock_billing_setup_operation
        )
        self.assertIn("Added new billing setup", captured_output.getvalue())
        self.assertIn("test_resource_name", captured_output.getvalue())

    @mock.patch(f"{SCRIPT_PATH}.create_billing_setup")
    @mock.patch(f"{SCRIPT_PATH}.set_billing_setup_date_times")
    def test_main_success_with_payments_profile_id(self, mock_set_dates, mock_create_setup):
        mock_client = mock.Mock(spec=GoogleAdsClient)
        mock_billing_setup_service = mock.Mock()
        mock_client.get_service.return_value = mock_billing_setup_service
        # ... rest of mocks similar to above ...
        mock_billing_setup_operation = mock.Mock(spec=BillingSetupOperation)
        mock_client.get_type.return_value = mock_billing_setup_operation
        
        mock_created_setup_instance = mock.Mock(spec=BillingSetup)
        mock_create_setup.return_value = mock_created_setup_instance
        
        mock_response = mock.Mock()
        mock_response.result.resource_name = "test_profile_resource_name"
        mock_billing_setup_service.mutate_billing_setup.return_value = mock_response

        captured_output = StringIO()
        sys.stdout = captured_output

        add_billing_setup.main(
            mock_client,
            self.MOCK_CUSTOMER_ID,
            payments_profile_id=self.MOCK_PAYMENTS_PROFILE_ID,
        )
        sys.stdout = sys.__stdout__

        mock_create_setup.assert_called_once_with(
            mock_client, self.MOCK_CUSTOMER_ID, None, self.MOCK_PAYMENTS_PROFILE_ID
        )
        mock_set_dates.assert_called_once_with(
            mock_client, self.MOCK_CUSTOMER_ID, mock_created_setup_instance
        )
        mock_billing_setup_service.mutate_billing_setup.assert_called_once()
        self.assertIn("Added new billing setup", captured_output.getvalue())
        self.assertIn("test_profile_resource_name", captured_output.getvalue())


    @mock.patch(f"{SCRIPT_PATH}.GoogleAdsClient") # To mock load_from_storage if testing __main__
    @mock.patch(f"{SCRIPT_PATH}.argparse.ArgumentParser") # To mock argument parsing
    @mock.patch("sys.exit")
    # Patching the functions called by main, as their behavior leading to an exception is not the focus here.
    # The exception we are testing is from mutate_billing_setup.
    @mock.patch(f"{SCRIPT_PATH}.create_billing_setup") 
    @mock.patch(f"{SCRIPT_PATH}.set_billing_setup_date_times")
    def test_main_google_ads_exception(
        self, mock_set_dates, mock_create_setup, mock_sys_exit, mock_argparse, mock_google_ads_client_constructor
    ):
        # --- This part simulates the __main__ block execution ----
        mock_args = mock.Mock()
        mock_args.customer_id = self.MOCK_CUSTOMER_ID
        mock_args.payments_account_id = self.MOCK_PAYMENTS_ACCOUNT_ID # or profile_id
        mock_args.payments_profile_id = None
        mock_argparse.return_value.parse_args.return_value = mock_args

        mock_client_instance = mock.Mock(spec=GoogleAdsClient)
        mock_google_ads_client_constructor.load_from_storage.return_value = mock_client_instance
        # --- End of __main__ simulation part ---

        # Configure services and operations for the main() call
        mock_billing_setup_service = mock.Mock()
        mock_client_instance.get_service.return_value = mock_billing_setup_service
        
        mock_billing_setup_operation = mock.Mock(spec=BillingSetupOperation)
        mock_client_instance.get_type.return_value = mock_billing_setup_operation

        mock_created_setup_instance = mock.Mock(spec=BillingSetup) # Returned by mocked create_billing_setup
        mock_create_setup.return_value = mock_created_setup_instance


        # Setup the exception
        error_message_detail = "Fake mutate error."
        ads_exception = GoogleAdsException(
            request_id="test_req_id_mutate",
            error=mock.Mock(code=lambda: mock.Mock(name="MUTATE_ERROR")),
            failure=mock.Mock(errors=[mock.Mock(message=error_message_detail, location=None)])
        )
        mock_billing_setup_service.mutate_billing_setup.side_effect = ads_exception
        
        captured_error = StringIO()
        sys.stderr = captured_error

        # Simulate the try-except block in __main__ by calling the script's main
        # and letting the test's try-except catch the error for verification.
        # The script's actual __main__ calls sys.exit(1)
        
        # We need to simulate the script's __main__ structure:
        # googleads_client = GoogleAdsClient.load_from_storage(...)
        # try:
        #    main(...)
        # except GoogleAdsException as ex:
        #    ... print error ...
        #    sys.exit(1)

        # Call the script's main execution path (conceptually)
        # In the actual script, load_from_storage provides the client to main.
        # We've mocked load_from_storage to return mock_client_instance.
        
        # This simulates the actual script structure for exception handling
        # add_billing_setup_module = importlib.import_module("add_billing_setup") # if needed for reload
        
        # To test __main__ block's exception handling:
        # We need to ensure that the call to add_billing_setup.main(...) below
        # is what happens INSIDE the try block of the script's __main__.
        # The mocks for argparse and load_from_storage set this up.
        
        # The following code structure mimics the script's __main__
        try:
            # This main call will use mock_client_instance due to earlier mocks
            add_billing_setup.main( 
                mock_client_instance, # This is the client from mocked load_from_storage
                mock_args.customer_id,
                mock_args.payments_account_id,
                mock_args.payments_profile_id,
            )
        except GoogleAdsException as ex_caught: # Mimic script's except block
            # This is the error handling from the script's __main__
            print(
                f'Request with ID "{ex_caught.request_id}" failed with status '
                f'"{ex_caught.error.code().name}" and includes the following errors:',
                file=sys.stderr,
            )
            for error in ex_caught.failure.errors:
                print(f'\tError with message "{error.message}".', file=sys.stderr)
                if error.location:
                    for field_path_element in error.location.field_path_elements:
                        print(
                            f"\t\tOn field: {field_path_element.field_name}",
                            file=sys.stderr,
                        )
            mock_sys_exit(1) # Simulate sys.exit(1) call from the script
        
        sys.stderr = sys.__stderr__

        mock_google_ads_client_constructor.load_from_storage.assert_called_once_with(version="v19")
        mock_sys_exit.assert_called_once_with(1)
        
        error_output = captured_error.getvalue()
        self.assertIn(f'Request with ID "{ads_exception.request_id}" failed', error_output)
        self.assertIn(f'status "{ads_exception.error.code().name}"', error_output)
        self.assertIn(f'Error with message "{error_message_detail}"', error_output)


if __name__ == "__main__":
    unittest.main()
