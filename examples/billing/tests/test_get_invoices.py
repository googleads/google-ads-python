import unittest
import sys
from unittest import mock
from io import StringIO
from datetime import date, timedelta

# Assuming 'examples' is in PYTHONPATH
import get_invoices # The script is named get_invoices.py

# Use a real or placeholder GoogleAdsException and other types
try:
    from google.ads.googleads.client import GoogleAdsClient
    from google.ads.googleads.errors import GoogleAdsException
    from google.ads.googleads.v19.services.types.invoice_service import ListInvoicesResponse
    from google.ads.googleads.v19.resources.types.invoice import Invoice
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

    class ListInvoicesResponse: pass
    class Invoice: pass
    class DateRange: pass


class TestGetInvoices(unittest.TestCase):
    MOCK_CUSTOMER_ID = "1234567890"
    MOCK_BILLING_SETUP_ID = "111222333"
    SCRIPT_PATH = "get_invoices" # Assuming direct import due to PYTHONPATH

    # Tests for _micros_to_currency
    def test_micros_to_currency_positive(self):
        self.assertEqual(get_invoices._micros_to_currency(1234567), 1.234567)

    def test_micros_to_currency_zero(self):
        self.assertEqual(get_invoices._micros_to_currency(0), 0.0)

    def test_micros_to_currency_none(self):
        self.assertIsNone(get_invoices._micros_to_currency(None))

    def test_micros_to_currency_negative(self):
        self.assertEqual(get_invoices._micros_to_currency(-500000), -0.5)

    @mock.patch(f"{SCRIPT_PATH}.date") # Mocking date to control date.today()
    def test_main_success_retrieves_invoices(self, mock_date):
        # Mock date.today() to return a fixed date for predictable month calculation
        # Let's say today is Nov 5, 2023. The script should query for OCTOBER 2023.
        mock_date.today.return_value = date(2023, 11, 5)
        expected_issue_year = "2023"
        expected_issue_month = "OCTOBER" # (November - 1 month).strftime("%B").upper()

        mock_client = mock.Mock(spec=GoogleAdsClient)
        mock_invoice_service = mock.Mock()
        mock_google_ads_service = mock.Mock() # For billing_setup_path
        
        # Configure get_service to return the correct mock service
        def get_service_side_effect(service_name):
            if service_name == "InvoiceService":
                return mock_invoice_service
            elif service_name == "GoogleAdsService":
                return mock_google_ads_service
            return mock.DEFAULT
        mock_client.get_service.side_effect = get_service_side_effect
        
        # Mock billing_setup_path
        expected_billing_setup_path = f"customers/{self.MOCK_CUSTOMER_ID}/billingSetups/{self.MOCK_BILLING_SETUP_ID}"
        mock_google_ads_service.billing_setup_path.return_value = expected_billing_setup_path

        # Prepare mock invoice data
        mock_invoice_1 = mock.Mock(spec=Invoice)
        mock_invoice_1.resource_name = "customers/123/invoices/inv1"
        mock_invoice_1.id = "INV001"
        mock_invoice_1.type_ = "CREDIT_MEMO" # Using an enum's string representation
        mock_invoice_1.billing_setup = expected_billing_setup_path
        mock_invoice_1.payments_account_id = "PAI456"
        mock_invoice_1.payments_profile_id = "PPI789"
        mock_invoice_1.issue_date = "2023-10-15"
        mock_invoice_1.due_date = "2023-11-15"
        mock_invoice_1.currency_code = "USD"
        mock_invoice_1.service_date_range = mock.Mock(spec=DateRange, start_date="2023-10-01", end_date="2023-10-31")
        mock_invoice_1.adjustments_subtotal_amount_micros = 100000 # 0.1 USD
        mock_invoice_1.adjustments_tax_amount_micros = 20000   # 0.02 USD
        mock_invoice_1.adjustments_total_amount_micros = 120000   # 0.12 USD
        mock_invoice_1.regulatory_costs_subtotal_amount_micros = 50000 # 0.05 USD
        mock_invoice_1.regulatory_costs_tax_amount_micros = 10000 # 0.01 USD
        mock_invoice_1.regulatory_costs_total_amount_micros = 60000 # 0.06 USD
        # For fields that are list-like and have a join method called on them in the script:
        mock_invoice_1.replaced_invoices = mock.Mock()
        mock_invoice_1.replaced_invoices.join.return_value = "customers/123/invoices/old_invA, customers/123/invoices/old_invB"
        # If replaced_invoices could be empty, its truthiness also matters for the script's conditional
        # if invoice.replaced_invoices else "none"
        # A standard mock is truthy. If it could be empty and evaluate to false:
        # mock_invoice_1.replaced_invoices = [] # Then the script's .join would fail.
        # For this test, we assume it's non-empty and joinable.
        # If it were empty, the script would print "none". We can test that separately if needed.
        # To make it behave as if it's a non-empty list for the conditional, and has a join method:
        # One way:
        # mock_invoice_1.replaced_invoices = mock.Mock(spec=list) # Make it list-like for truthiness
        # mock_invoice_1.replaced_invoices.join = mock.Mock(return_value="customers/123/invoices/old_invA, customers/123/invoices/old_invB")
        # However, the script is invoice.replaced_invoices.join(","). The mock above is fine.
        # If it's a list of strings from the protobuf object, the script should be ", ".join(invoice.replaced_invoices)
        # Sticking to mocking the script as written:
        # The previous mock_invoice_1.replaced_invoices = mock.Mock() with .join works.

        mock_invoice_1.subtotal_amount_micros = 10000000 # 10 USD
        mock_invoice_1.tax_amount_micros = 2000000    # 2 USD
        mock_invoice_1.total_amount_micros = 12000000   # 12 USD
        mock_invoice_1.corrected_invoice = None # or "customers/123/invoices/corrected_inv"
        mock_invoice_1.pdf_url = "http://example.com/invoice1.pdf"
        
        mock_budget_summary_1 = mock.Mock()
        mock_budget_summary_1.account_budget = "customers/123/accountBudgets/budget1"
        mock_budget_summary_1.account_budget_name = "Campaign Budget Alpha"
        mock_budget_summary_1.customer = "customers/123"
        mock_budget_summary_1.customer_descriptive_name = "Advertiser X"
        mock_budget_summary_1.purchase_order_number = "PO123"
        mock_budget_summary_1.billable_activity_date_range = mock.Mock(spec=DateRange, start_date="2023-10-01", end_date="2023-10-15")
        mock_budget_summary_1.subtotal_amount_micros = 7000000 # 7 USD
        mock_budget_summary_1.tax_amount_micros = 1000000   # 1 USD
        mock_budget_summary_1.total_amount_micros = 8000000   # 8 USD
        mock_invoice_1.account_budget_summaries = [mock_budget_summary_1]

        mock_list_invoices_response = mock.Mock(spec=ListInvoicesResponse)
        mock_list_invoices_response.invoices = [mock_invoice_1]
        mock_invoice_service.list_invoices.return_value = mock_list_invoices_response

        captured_output = StringIO()
        sys.stdout = captured_output

        get_invoices.main(mock_client, self.MOCK_CUSTOMER_ID, self.MOCK_BILLING_SETUP_ID)

        sys.stdout = sys.__stdout__

        mock_google_ads_service.billing_setup_path.assert_called_once_with(
            self.MOCK_CUSTOMER_ID, self.MOCK_BILLING_SETUP_ID
        )
        mock_invoice_service.list_invoices.assert_called_once_with(
            customer_id=self.MOCK_CUSTOMER_ID,
            billing_setup=expected_billing_setup_path,
            issue_year=expected_issue_year,
            issue_month=expected_issue_month,
        )
        
        output = captured_output.getvalue()
        self.assertIn(f"Found the invoice {mock_invoice_1.resource_name}", output)
        self.assertIn(f"ID (also known as Invoice Number): '{mock_invoice_1.id}'", output)
        self.assertIn(f"Type: {mock_invoice_1.type_}", output)
        self.assertIn(f"total {get_invoices._micros_to_currency(mock_invoice_1.total_amount_micros)}", output)
        self.assertIn(f"Adjustments:\n        subtotal {get_invoices._micros_to_currency(mock_invoice_1.adjustments_subtotal_amount_micros)}", output)
        # The script uses mock_invoice_1.replaced_invoices.join(', ')
        self.assertIn(f"Replaced invoices: {mock_invoice_1.replaced_invoices.join(', ')}", output)
        self.assertIn(f"Account budget '{mock_budget_summary_1.account_budget}'", output)
        self.assertIn(f"Name (also known as Account Budget): '{mock_budget_summary_1.account_budget_name}'", output)
        self.assertIn(f"total '{get_invoices._micros_to_currency(mock_budget_summary_1.total_amount_micros)}'", output)

    @mock.patch(f"{SCRIPT_PATH}.date")
    def test_main_success_no_invoices_found(self, mock_date):
        mock_date.today.return_value = date(2023, 11, 5) # Example date

        mock_client = mock.Mock(spec=GoogleAdsClient)
        mock_invoice_service = mock.Mock()
        mock_google_ads_service = mock.Mock()
        mock_client.get_service.side_effect = lambda name: mock_invoice_service if name == "InvoiceService" else mock_google_ads_service

        mock_google_ads_service.billing_setup_path.return_value = "mock_path"
        
        mock_list_invoices_response = mock.Mock(spec=ListInvoicesResponse)
        mock_list_invoices_response.invoices = [] # No invoices
        mock_invoice_service.list_invoices.return_value = mock_list_invoices_response

        captured_output = StringIO()
        sys.stdout = captured_output

        get_invoices.main(mock_client, self.MOCK_CUSTOMER_ID, self.MOCK_BILLING_SETUP_ID)

        sys.stdout = sys.__stdout__
        
        mock_invoice_service.list_invoices.assert_called_once()
        self.assertEqual(captured_output.getvalue().strip(), "") # No output if no invoices

    @mock.patch(f"{SCRIPT_PATH}.GoogleAdsClient")
    @mock.patch(f"{SCRIPT_PATH}.argparse.ArgumentParser")
    @mock.patch("sys.exit")
    @mock.patch(f"{SCRIPT_PATH}.date") # Mock date for consistent month calculation
    def test_main_google_ads_exception(
        self, mock_script_date, mock_sys_exit, mock_argparse, mock_google_ads_client_constructor
    ):
        mock_script_date.today.return_value = date(2023, 11, 5) # Example date

        # --- This part simulates the __main__ block execution ----
        mock_args = mock.Mock()
        mock_args.customer_id = self.MOCK_CUSTOMER_ID
        mock_args.billing_setup_id = self.MOCK_BILLING_SETUP_ID
        mock_argparse.return_value.parse_args.return_value = mock_args

        mock_client_instance = mock.Mock(spec=GoogleAdsClient)
        mock_google_ads_client_constructor.load_from_storage.return_value = mock_client_instance
        # --- End of __main__ simulation part ---

        mock_invoice_service = mock.Mock()
        mock_google_ads_service = mock.Mock()
        def get_service_side_effect(service_name):
            if service_name == "InvoiceService":
                return mock_invoice_service
            elif service_name == "GoogleAdsService":
                return mock_google_ads_service
            return mock.DEFAULT
        mock_client_instance.get_service.side_effect = get_service_side_effect
        
        # Setup the exception
        error_message_detail = "Fake list_invoices error."
        ads_exception = GoogleAdsException(
            request_id="test_req_id_list_inv",
            error=mock.Mock(code=lambda: mock.Mock(name="LIST_INVOICES_ERROR")),
            failure=mock.Mock(errors=[mock.Mock(message=error_message_detail, location=None)])
        )
        mock_invoice_service.list_invoices.side_effect = ads_exception
        
        captured_error = StringIO()
        sys.stderr = captured_error

        # Simulate the try-except block in __main__
        try:
            get_invoices.main(
                mock_client_instance, 
                mock_args.customer_id, 
                mock_args.billing_setup_id
            )
        except GoogleAdsException as ex_caught:
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
            mock_sys_exit(1)
        
        sys.stderr = sys.__stderr__

        mock_google_ads_client_constructor.load_from_storage.assert_called_once_with(version="v19")
        mock_sys_exit.assert_called_once_with(1)
        
        error_output = captured_error.getvalue()
        self.assertIn(f'Request with ID "{ads_exception.request_id}" failed', error_output)
        self.assertIn(f'status "{ads_exception.error.code().name}"', error_output)
        self.assertIn(f'Error with message "{error_message_detail}"', error_output)

if __name__ == "__main__":
    unittest.main()
