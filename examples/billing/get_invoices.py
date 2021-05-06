#!/usr/bin/env python
# Copyright 2021 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Retrieves the invoices issued last month for a given billing setup."""


import argparse
from datetime import date, timedelta
import sys

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


def main(client, customer_id, billing_setup_id):
    """The main method that creates all necessary entities for the example.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        billing_setup_id: a billing setup ID.
    """

    # The last day of last month.
    last_month = date.today().replace(day=1) - timedelta(days=1)
    # [START get_invoices]
    # Issues a request to list invoices.
    response = client.get_service("InvoiceService").list_invoices(
        customer_id=customer_id,
        billing_setup=client.get_service("GoogleAdsService").billing_setup_path(
            customer_id, billing_setup_id
        ),
        # The year needs to be 2019 or later, per the docs:
        # https://developers.google.com/google-ads/api/docs/billing/invoice?hl=en#retrieving_invoices
        issue_year=str(last_month.year),
        issue_month=last_month.strftime("%B").upper(),
    )
    # [END get_invoices]

    # [START get_invoices_1]
    for invoice in response.invoices:
        print(
            f"""
- Found the invoice {invoice.resource_name}
    ID (also known as Invoice Number): '{invoice.id}'
    Type: {invoice.type_}
    Billing setup ID: '{invoice.billing_setup}'
    Payments account ID (also known as Billing Account Number): '{invoice.payments_account_id}'
    Payments profile ID (also known as Billing ID): '{invoice.payments_profile_id}'
    Issue date (also known as Invoice Date): {invoice.issue_date}
    Due date: {invoice.due_date}
    Currency code: {invoice.currency_code}
    Service date range (inclusive): from {invoice.service_date_range.start_date} to {invoice.service_date_range.end_date}
    Adjustments:
        subtotal {_micros_to_currency(invoice.adjustments_subtotal_amount_micros)}
        tax {_micros_to_currency(invoice.adjustments_tax_amount_micros)}
        total {_micros_to_currency(invoice.adjustments_total_amount_micros)}
    Regulatory costs:
        subtotal {_micros_to_currency(invoice.regulatory_costs_subtotal_amount_micros)}
        tax {_micros_to_currency(invoice.regulatory_costs_tax_amount_micros)}
        total {_micros_to_currency(invoice.regulatory_costs_total_amount_micros)}
    Replaced invoices: {invoice.replaced_invoices.join(", ") if invoice.replaced_invoices else "none"}
    Amounts:
        subtotal {_micros_to_currency(invoice.subtotal_amount_micros)}
        tax {_micros_to_currency(invoice.tax_amount_micros)}
        total {_micros_to_currency(invoice.total_amount_micros)}
    Corrected invoice: {invoice.corrected_invoice or "none"}
    PDF URL: {invoice.pdf_url}
    Account budgets:
    """
        )
        for account_budget_summary in invoice.account_budget_summaries:
            print(
                f"""
                  - Account budget '{account_budget_summary.account_budget}':
                      Name (also known as Account Budget): '{account_budget_summary.account_budget_name}'
                      Customer (also known as Account ID): '{account_budget_summary.customer}'
                      Customer descriptive name (also known as Account): '{account_budget_summary.customer_descriptive_name}'
                      Purchase order number (also known as Purchase Order): '{account_budget_summary.purchase_order_number}'
                      Billing activity date range (inclusive):
                        from #{account_budget_summary.billable_activity_date_range.start_date}
                        to #{account_budget_summary.billable_activity_date_range.end_date}
                      Amounts:
                        subtotal '{_micros_to_currency(account_budget_summary.subtotal_amount_micros)}'
                        tax '{_micros_to_currency(account_budget_summary.tax_amount_micros)}'
                        total '{_micros_to_currency(account_budget_summary.total_amount_micros)}'
                """
            )
            # [END get_invoices_1]


def _micros_to_currency(micros):
    return micros / 1000000.0 if micros is not None else None


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v6")

    parser = argparse.ArgumentParser(
        description="Retrieves the invoices issued last month for a given billing setup."
    )
    # The following argument(s) should be provided to run the example.
    parser.add_argument(
        "-c",
        "--customer_id",
        type=str,
        required=True,
        help="The Google Ads customer ID.",
    )
    parser.add_argument(
        "-b",
        "--billing_setup_id",
        type=str,
        required=True,
        help="The billing setup ID.",
    )
    args = parser.parse_args()

    try:
        main(googleads_client, args.customer_id, args.billing_setup_id)
    except GoogleAdsException as ex:
        print(
            f'Request with ID "{ex.request_id}" failed with status '
            f'"{ex.error.code().name}" and includes the following errors:'
        )
        for error in ex.failure.errors:
            print(f'\tError with message "{error.message}".')
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print(f"\t\tOn field: {field_path_element.field_name}")
        sys.exit(1)
