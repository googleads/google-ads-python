import unittest
from unittest.mock import MagicMock, patch, call # Ensure call is imported
from io import StringIO
from datetime import datetime, timedelta
import uuid

from examples.billing.add_billing_setup import (
    main,
    create_billing_setup,
    set_billing_setup_date_times,
)

class TestAddBillingSetup(unittest.TestCase):

    def setUp(self):
        self.mock_client = MagicMock()
        self.customer_id = "12345"

    def test_create_billing_setup_with_payments_account_id(self):
        payments_account_id = "1111-2222-3333-4444"
        expected_payments_account_path = f"customers/{self.customer_id}/paymentsAccounts/{payments_account_id}"

        mock_billing_setup_obj = MagicMock(name="BillingSetupInstance")
        # payments_account_info will be auto-created by MagicMock if accessed.
        # We want to check that no attributes *on* payments_account_info are set by the SUT.
        mock_billing_setup_obj.payments_account_info = MagicMock(name="PaymentsAccountInfoOnBillingSetup")

        self.mock_client.get_type.return_value = mock_billing_setup_obj

        mock_billing_setup_service_for_path = MagicMock()
        mock_billing_setup_service_for_path.payments_account_path.return_value = expected_payments_account_path

        original_get_service = self.mock_client.get_service
        def side_effect_get_service(service_name):
            if service_name == "BillingSetupService":
                return mock_billing_setup_service_for_path
            return MagicMock()

        with patch.object(self.mock_client, 'get_service', side_effect=side_effect_get_service):
            billing_setup_obj_returned = create_billing_setup(
                self.mock_client, self.customer_id, payments_account_id=payments_account_id
            )

        self.mock_client.get_type.assert_called_once_with("BillingSetup")
        self.assertEqual(billing_setup_obj_returned, mock_billing_setup_obj)
        self.assertEqual(billing_setup_obj_returned.payments_account, expected_payments_account_path)
        mock_billing_setup_service_for_path.payments_account_path.assert_called_once_with(
            self.customer_id, payments_account_id
        )

        # Check that attributes on payments_account_info were not set.
        # mock_calls records calls like obj.attr = value as ('__setattr__', ('attr', value))
        for call_obj in mock_billing_setup_obj.payments_account_info.mock_calls:
            if call_obj[0] == '__setattr__':
                self.assertNotIn(call_obj[1][0], ['payments_account_name', 'payments_profile_id'],
                                 f"Attribute {call_obj[1][0]} should not have been set on payments_account_info")

    @patch('examples.billing.add_billing_setup.uuid4')
    def test_create_billing_setup_with_payments_profile_id(self, mock_uuid4):
        payments_profile_id = "PROFILE-123"
        mock_uuid_obj = MagicMock()
        mock_uuid_obj.__str__.return_value = "mock-uuid-123"
        mock_uuid4.return_value = mock_uuid_obj

        mock_billing_setup_obj = MagicMock(name="BillingSetupInstance")
        mock_billing_setup_obj.payments_account_info = MagicMock(name="PaymentsAccountInfoInstance")
        # Ensure payments_account is not on the mock initially, so hasattr can be used.
        if hasattr(mock_billing_setup_obj, 'payments_account'):
             delattr(mock_billing_setup_obj, 'payments_account') # Make hasattr work reliably

        self.mock_client.get_type.return_value = mock_billing_setup_obj

        billing_setup_obj_returned = create_billing_setup(
            self.mock_client, self.customer_id, payments_profile_id=payments_profile_id
        )

        self.mock_client.get_type.assert_called_once_with("BillingSetup")
        self.assertEqual(billing_setup_obj_returned, mock_billing_setup_obj)
        self.assertEqual(billing_setup_obj_returned.payments_account_info.payments_account_name, f"Payments Account #mock-uuid-123")
        self.assertEqual(billing_setup_obj_returned.payments_account_info.payments_profile_id, payments_profile_id)

        # Check that payments_account was not set by the SUT.
        # If it was never set by SUT, hasattr should be False (after our delattr).
        self.assertFalse(hasattr(mock_billing_setup_obj, 'payments_account'),
                         "payments_account attribute should not be set when payments_profile_id is used.")

    @patch('examples.billing.add_billing_setup.datetime')
    def test_set_billing_setup_date_times_no_existing_setup(self, mock_dt_module):
        mock_now = datetime(2023, 1, 1, 12, 0, 0)
        mock_dt_module.now.return_value = mock_now

        mock_billing_setup_instance = MagicMock()
        mock_ga_service = MagicMock()
        self.mock_client.get_service.return_value = mock_ga_service
        mock_ga_service.search_stream.return_value = iter([])

        set_billing_setup_date_times(self.mock_client, self.customer_id, mock_billing_setup_instance)

        self.mock_client.get_service.assert_called_once_with("GoogleAdsService")
        mock_ga_service.search_stream.assert_called_once()
        expected_start_datetime_str = mock_now.strftime("%Y-%m-%d %H:%M:%S")
        expected_end_datetime_str = (mock_now + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")

        self.assertEqual(mock_billing_setup_instance.start_date_time, expected_start_datetime_str)
        self.assertEqual(mock_billing_setup_instance.end_date_time, expected_end_datetime_str)

    def test_set_billing_setup_date_times_existing_with_end_date_full_format(self):
        mock_billing_setup_instance = MagicMock()
        mock_ga_service = MagicMock()
        self.mock_client.get_service.return_value = mock_ga_service

        mock_row = MagicMock()
        mock_row.billing_setup.end_date_time = "2023-01-15 10:00:00"
        mock_batch = MagicMock()
        mock_batch.results = [mock_row]
        mock_ga_service.search_stream.return_value = iter([mock_batch])

        set_billing_setup_date_times(self.mock_client, self.customer_id, mock_billing_setup_instance)

        expected_start_date = datetime(2023, 1, 15, 10, 0, 0) + timedelta(days=1)
        expected_start_datetime_str = expected_start_date.strftime("%Y-%m-%d %H:%M:%S")
        expected_end_datetime_str = (expected_start_date + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")

        self.assertEqual(mock_billing_setup_instance.start_date_time, expected_start_datetime_str)
        self.assertEqual(mock_billing_setup_instance.end_date_time, expected_end_datetime_str)

    def test_set_billing_setup_date_times_existing_with_end_date_only_format(self):
        mock_billing_setup_instance = MagicMock()
        mock_ga_service = MagicMock()
        self.mock_client.get_service.return_value = mock_ga_service

        mock_row = MagicMock()
        mock_row.billing_setup.end_date_time = "2023-01-20"
        mock_batch = MagicMock()
        mock_batch.results = [mock_row]
        mock_ga_service.search_stream.return_value = iter([mock_batch])

        set_billing_setup_date_times(self.mock_client, self.customer_id, mock_billing_setup_instance)

        expected_start_date = datetime(2023, 1, 20, 0, 0, 0) + timedelta(days=1)
        expected_start_datetime_str = expected_start_date.strftime("%Y-%m-%d %H:%M:%S")
        expected_end_datetime_str = (expected_start_date + timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")

        self.assertEqual(mock_billing_setup_instance.start_date_time, expected_start_datetime_str)
        self.assertEqual(mock_billing_setup_instance.end_date_time, expected_end_datetime_str)

    def test_set_billing_setup_date_times_existing_runs_forever(self):
        mock_billing_setup_instance = MagicMock()
        mock_ga_service = MagicMock()
        self.mock_client.get_service.return_value = mock_ga_service

        mock_row = MagicMock()
        mock_row.billing_setup.end_date_time = None
        mock_batch = MagicMock()
        mock_batch.results = [mock_row]
        mock_ga_service.search_stream.return_value = iter([mock_batch])

        with self.assertRaisesRegex(Exception, "latest existing billing setup is set to run indefinitely"):
            set_billing_setup_date_times(self.mock_client, self.customer_id, mock_billing_setup_instance)

    @patch('examples.billing.add_billing_setup.create_billing_setup')
    @patch('examples.billing.add_billing_setup.set_billing_setup_date_times')
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_function_with_payments_account_id(self, mock_stdout, mock_set_dates, mock_create_setup):
        self.mock_client.reset_mock()

        mock_created_billing_setup = MagicMock(name="MockedBillingSetupInstance")
        mock_create_setup.return_value = mock_created_billing_setup

        mock_billing_setup_service_main = MagicMock(name="BillingSetupServiceForMain")
        mock_operation_type_main = MagicMock(name="BillingSetupOperationForMain")
        mock_operation_type_main.create = MagicMock(name="OperationCreate")

        def main_get_service_side_effect(service_name):
            if service_name == "BillingSetupService":
                return mock_billing_setup_service_main
            return MagicMock()
        self.mock_client.get_service.side_effect = main_get_service_side_effect

        def main_get_type_side_effect(type_name):
            if type_name == "BillingSetupOperation":
                return mock_operation_type_main
            return MagicMock()
        self.mock_client.get_type.side_effect = main_get_type_side_effect

        mock_mutate_response = MagicMock()
        expected_resource_name = f"customers/{self.customer_id}/billingSetups/789"
        mock_mutate_response.result.resource_name = expected_resource_name
        mock_billing_setup_service_main.mutate_billing_setup.return_value = mock_mutate_response

        payments_account_id_for_main = "PAY_ACC_ID_MAIN"
        main(self.mock_client, self.customer_id, payments_account_id=payments_account_id_for_main)

        mock_create_setup.assert_called_once_with(
            self.mock_client, self.customer_id, payments_account_id_for_main, None
        )
        mock_set_dates.assert_called_once_with(
            self.mock_client, self.customer_id, mock_created_billing_setup
        )
        self.mock_client.get_type.assert_called_once_with("BillingSetupOperation")
        self.mock_client.copy_from.assert_called_once_with(
            mock_operation_type_main.create, mock_created_billing_setup
        )
        self.mock_client.get_service.assert_called_once_with("BillingSetupService")
        mock_billing_setup_service_main.mutate_billing_setup.assert_called_once_with(
            customer_id=self.customer_id, operation=mock_operation_type_main
        )
        self.assertEqual(
            mock_stdout.getvalue(),
            f"Added new billing setup with resource name {expected_resource_name}\n"
        )

if __name__ == "__main__":
    unittest.main()
