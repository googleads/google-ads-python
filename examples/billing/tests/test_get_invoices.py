import unittest
from unittest.mock import MagicMock, patch
from io import StringIO
from datetime import date, timedelta

from examples.billing import get_invoices

def micros_to_currency_for_test(micros):
    return micros / 1000000.0 if micros is not None else None

class TestGetInvoices(unittest.TestCase):

    # Decorators are applied bottom-up.
    # Innermost: @patch('sys.stdout', new_callable=StringIO) -> mock_stdout (arg 1)
    # Middle:    @patch('examples.billing.get_invoices.GoogleAdsClient') -> mock_google_ads_client_class_in_module (arg 2)
    # Outermost: @patch('examples.billing.get_invoices.micros_to_currency', new=micros_to_currency_for_test) -> NO ARG ADDED
    @patch('examples.billing.get_invoices.micros_to_currency', new=micros_to_currency_for_test)
    @patch('examples.billing.get_invoices.GoogleAdsClient')
    @patch('sys.stdout', new_callable=StringIO)
    def test_main_function(self, mock_stdout, mock_google_ads_client_class_in_module): # Corrected signature

        mock_client_instance = MagicMock()
        mock_invoice_service = MagicMock()
        mock_google_ads_service = MagicMock()

        mock_client_instance.get_service.side_effect = lambda service_name: {
            "InvoiceService": mock_invoice_service,
            "GoogleAdsService": mock_google_ads_service
        }.get(service_name)

        # mock_google_ads_client_class_in_module is the mock for GoogleAdsClient in the get_invoices module
        # This is correctly passed due to the @patch decorator.

        # micros_to_currency is patched with 'new', so no mock object is passed for it.
        # Calls to get_invoices.micros_to_currency will use micros_to_currency_for_test.

        mock_google_ads_service.billing_setup_path.return_value = "customers/12345/billingSetups/67890"
        mock_invoice = MagicMock()
        mock_invoice.resource_name = "customers/12345/invoices/INV001"
        mock_invoice.id = "INV001_ID"
        mock_invoice.type_ = "INVOICE_TYPE_CREDIT"
        mock_invoice.billing_setup = "customers/12345/billingSetups/67890"
        mock_invoice.payments_account_id = "PAY_ACC_ID_001"
        mock_invoice.payments_profile_id = "PAY_PROF_ID_001"
        mock_invoice.issue_date = "2023-10-15"
        mock_invoice.due_date = "2023-11-15"
        mock_invoice.currency_code = "USD"
        mock_invoice.service_date_range = MagicMock()
        mock_invoice.service_date_range.start_date = "2023-10-01"
        mock_invoice.service_date_range.end_date = "2023-10-31"
        mock_invoice.adjustments_subtotal_amount_micros = 1000000
        mock_invoice.adjustments_tax_amount_micros = 200000
        mock_invoice.adjustments_total_amount_micros = 1200000
        mock_invoice.regulatory_costs_subtotal_amount_micros = 50000
        mock_invoice.regulatory_costs_tax_amount_micros = 10000
        mock_invoice.regulatory_costs_total_amount_micros = 60000

        mock_replaced_invoices_list = ["customers/12345/invoices/OLD_INV"]
        mock_invoice.replaced_invoices = MagicMock()
        mock_invoice.replaced_invoices.__bool__.return_value = bool(mock_replaced_invoices_list)
        mock_invoice.replaced_invoices.join.return_value = ", ".join(mock_replaced_invoices_list)

        mock_invoice.subtotal_amount_micros = 20000000
        mock_invoice.tax_amount_micros = 4000000
        mock_invoice.total_amount_micros = 24000000
        mock_invoice.corrected_invoice = None
        mock_invoice.pdf_url = "http://example.com/invoice.pdf"

        mock_account_budget_summary = MagicMock()
        mock_account_budget_summary.account_budget = "customers/12345/accountBudgets/AB001"
        mock_account_budget_summary.account_budget_name = "Test Budget"
        mock_account_budget_summary.customer = "customers/12345"
        mock_account_budget_summary.customer_descriptive_name = "Test Customer"
        mock_account_budget_summary.purchase_order_number = "PO123"
        mock_account_budget_summary.billable_activity_date_range = MagicMock()
        mock_account_budget_summary.billable_activity_date_range.start_date = "2023-10-01"
        mock_account_budget_summary.billable_activity_date_range.end_date = "2023-10-31"
        mock_account_budget_summary.subtotal_amount_micros = 15000000
        mock_account_budget_summary.tax_amount_micros = 3000000
        mock_account_budget_summary.total_amount_micros = 18000000
        mock_invoice.account_budget_summaries = [mock_account_budget_summary]

        mock_invoice_service.list_invoices.return_value = MagicMock(invoices=[mock_invoice])

        customer_id = "12345"
        billing_setup_id = "67890"

        get_invoices.main(mock_client_instance, customer_id, billing_setup_id)

        last_month = date.today().replace(day=1) - timedelta(days=1)
        expected_issue_year = str(last_month.year)
        expected_issue_month = last_month.strftime("%B").upper()

        mock_invoice_service.list_invoices.assert_called_once_with(
            customer_id=customer_id,
            billing_setup="customers/12345/billingSetups/67890",
            issue_year=expected_issue_year,
            issue_month=expected_issue_month,
        )

        output = mock_stdout.getvalue()
        self.assertIn(f"Found the invoice {mock_invoice.resource_name}", output)
        self.assertIn(f"ID (also known as Invoice Number): '{mock_invoice.id}'", output)
        self.assertIn(f"subtotal {micros_to_currency_for_test(mock_invoice.adjustments_subtotal_amount_micros)}", output)

        expected_replaced_invoices_str = ", ".join(mock_replaced_invoices_list) if mock_replaced_invoices_list else "none"
        self.assertIn(f"Replaced invoices: {expected_replaced_invoices_str}", output)

        self.assertIn(f"Account budget '{mock_account_budget_summary.account_budget}'", output)
        self.assertIn(f"subtotal '{micros_to_currency_for_test(mock_account_budget_summary.subtotal_amount_micros)}'", output)

if __name__ == "__main__":
    unittest.main()
