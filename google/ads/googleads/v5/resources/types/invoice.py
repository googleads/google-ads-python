# -*- coding: utf-8 -*-

# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import proto  # type: ignore


from google.ads.googleads.v5.common.types import dates
from google.ads.googleads.v5.enums.types import invoice_type
from google.protobuf import wrappers_pb2 as wrappers  # type: ignore


__protobuf__ = proto.module(
    package="google.ads.googleads.v5.resources",
    marshal="google.ads.googleads.v5",
    manifest={"Invoice",},
)


class Invoice(proto.Message):
    r"""An invoice. All invoice information is snapshotted to match
    the PDF invoice. For invoices older than the launch of
    InvoiceService, the snapshotted information may not match the
    PDF invoice.

    Attributes:
        resource_name (str):
            Output only. The resource name of the invoice. Multiple
            customers can share a given invoice, so multiple resource
            names may point to the same invoice. Invoice resource names
            have the form:

            ``customers/{customer_id}/invoices/{invoice_id}``
        id (google.protobuf.wrappers_pb2.StringValue):
            Output only. The ID of the invoice. It
            appears on the invoice PDF as "Invoice number".
        type_ (google.ads.googleads.v5.enums.types.InvoiceTypeEnum.InvoiceType):
            Output only. The type of invoice.
        billing_setup (google.protobuf.wrappers_pb2.StringValue):
            Output only. The resource name of this invoice’s billing
            setup.

            ``customers/{customer_id}/billingSetups/{billing_setup_id}``
        payments_account_id (google.protobuf.wrappers_pb2.StringValue):
            Output only. A 16 digit ID used to identify
            the payments account associated with the billing
            setup, e.g. "1234-5678-9012-3456". It appears on
            the invoice PDF as "Billing Account Number".
        payments_profile_id (google.protobuf.wrappers_pb2.StringValue):
            Output only. A 12 digit ID used to identify
            the payments profile associated with the billing
            setup, e.g. "1234-5678-9012". It appears on the
            invoice PDF as "Billing ID".
        issue_date (google.protobuf.wrappers_pb2.StringValue):
            Output only. The issue date in yyyy-mm-dd
            format. It appears on the invoice PDF as either
            "Issue date" or "Invoice date".
        due_date (google.protobuf.wrappers_pb2.StringValue):
            Output only. The due date in yyyy-mm-dd
            format.
        service_date_range (google.ads.googleads.v5.common.types.DateRange):
            Output only. The service period date range of
            this invoice. The end date is inclusive.
        currency_code (google.protobuf.wrappers_pb2.StringValue):
            Output only. The currency code. All costs are
            returned in this currency. A subset of the
            currency codes derived from the ISO 4217
            standard is supported.
        invoice_level_adjustments_micros (google.protobuf.wrappers_pb2.Int64Value):
            Output only. The total amount of invoice
            level adjustments. These adjustments are made on
            the invoice, not on a specific account budget.
        subtotal_amount_micros (google.protobuf.wrappers_pb2.Int64Value):
            Output only. The pretax subtotal amount, in micros. This
            equals the sum of the AccountBudgetSummary subtotal amounts,
            Invoice.adjustments_subtotal_amount_micros, and
            Invoice.regulatory_costs_subtotal_amount_micros. Starting
            with v6, the Invoice.regulatory_costs_subtotal_amount_micros
            is no longer included.
        tax_amount_micros (google.protobuf.wrappers_pb2.Int64Value):
            Output only. The sum of all taxes on the
            invoice, in micros. This equals the sum of the
            AccountBudgetSummary tax amounts, plus taxes not
            associated with a specific account budget.
        total_amount_micros (google.protobuf.wrappers_pb2.Int64Value):
            Output only. The total amount, in micros. This equals the
            sum of Invoice.subtotal_amount_micros and
            Invoice.tax_amount_micros. Starting with v6,
            Invoice.regulatory_costs_subtotal_amount_micros is also
            added as it is no longer already included in
            Invoice.tax_amount_micros.
        corrected_invoice (google.protobuf.wrappers_pb2.StringValue):
            Output only. The resource name of the original invoice
            corrected, wrote off, or canceled by this invoice, if
            applicable. If ``corrected_invoice`` is set,
            ``replaced_invoices`` will not be set. Invoice resource
            names have the form:

            ``customers/{customer_id}/invoices/{invoice_id}``
        replaced_invoices (Sequence[google.protobuf.wrappers_pb2.StringValue]):
            Output only. The resource name of the original invoice(s)
            being rebilled or replaced by this invoice, if applicable.
            There might be multiple replaced invoices due to invoice
            consolidation. The replaced invoices may not belong to the
            same payments account. If ``replaced_invoices`` is set,
            ``corrected_invoice`` will not be set. Invoice resource
            names have the form:

            ``customers/{customer_id}/invoices/{invoice_id}``
        pdf_url (google.protobuf.wrappers_pb2.StringValue):
            Output only. The URL to a PDF copy of the
            invoice. Users need to pass in their OAuth token
            to request the PDF with this URL.
        account_budget_summaries (Sequence[google.ads.googleads.v5.resources.types.Invoice.AccountBudgetSummary]):
            Output only. The list of summarized account
            budget information associated with this invoice.
    """

    class AccountBudgetSummary(proto.Message):
        r"""Represents a summarized account budget billable cost.

        Attributes:
            customer (google.protobuf.wrappers_pb2.StringValue):
                Output only. The resource name of the customer associated
                with this account budget. This contains the customer ID,
                which appears on the invoice PDF as "Account ID". Customer
                resource names have the form:

                ``customers/{customer_id}``
            customer_descriptive_name (google.protobuf.wrappers_pb2.StringValue):
                Output only. The descriptive name of the
                account budget’s customer. It appears on the
                invoice PDF as "Account".
            account_budget (google.protobuf.wrappers_pb2.StringValue):
                Output only. The resource name of the account budget
                associated with this summarized billable cost. AccountBudget
                resource names have the form:

                ``customers/{customer_id}/accountBudgets/{account_budget_id}``
            account_budget_name (google.protobuf.wrappers_pb2.StringValue):
                Output only. The name of the account budget.
                It appears on the invoice PDF as "Account
                budget".
            purchase_order_number (google.protobuf.wrappers_pb2.StringValue):
                Output only. The purchase order number of the
                account budget. It appears on the invoice PDF as
                "Purchase order".
            subtotal_amount_micros (google.protobuf.wrappers_pb2.Int64Value):
                Output only. The pretax subtotal amount
                attributable to this budget during the service
                period, in micros.
            tax_amount_micros (google.protobuf.wrappers_pb2.Int64Value):
                Output only. The tax amount attributable to
                this budget during the service period, in
                micros.
            total_amount_micros (google.protobuf.wrappers_pb2.Int64Value):
                Output only. The total amount attributable to
                this budget during the service period, in
                micros. This equals the sum of the account
                budget subtotal amount and the account budget
                tax amount.
            billable_activity_date_range (google.ads.googleads.v5.common.types.DateRange):
                Output only. The billable activity date range
                of the account budget, within the service date
                range of this invoice. The end date is
                inclusive. This can be different from the
                account budget's start and end time.
        """

        customer = proto.Field(
            proto.MESSAGE, number=1, message=wrappers.StringValue,
        )
        customer_descriptive_name = proto.Field(
            proto.MESSAGE, number=2, message=wrappers.StringValue,
        )
        account_budget = proto.Field(
            proto.MESSAGE, number=3, message=wrappers.StringValue,
        )
        account_budget_name = proto.Field(
            proto.MESSAGE, number=4, message=wrappers.StringValue,
        )
        purchase_order_number = proto.Field(
            proto.MESSAGE, number=5, message=wrappers.StringValue,
        )
        subtotal_amount_micros = proto.Field(
            proto.MESSAGE, number=6, message=wrappers.Int64Value,
        )
        tax_amount_micros = proto.Field(
            proto.MESSAGE, number=7, message=wrappers.Int64Value,
        )
        total_amount_micros = proto.Field(
            proto.MESSAGE, number=8, message=wrappers.Int64Value,
        )
        billable_activity_date_range = proto.Field(
            proto.MESSAGE, number=9, message=dates.DateRange,
        )

    resource_name = proto.Field(proto.STRING, number=1)
    id = proto.Field(proto.MESSAGE, number=2, message=wrappers.StringValue,)
    type_ = proto.Field(
        proto.ENUM, number=3, enum=invoice_type.InvoiceTypeEnum.InvoiceType,
    )
    billing_setup = proto.Field(
        proto.MESSAGE, number=4, message=wrappers.StringValue,
    )
    payments_account_id = proto.Field(
        proto.MESSAGE, number=5, message=wrappers.StringValue,
    )
    payments_profile_id = proto.Field(
        proto.MESSAGE, number=6, message=wrappers.StringValue,
    )
    issue_date = proto.Field(
        proto.MESSAGE, number=7, message=wrappers.StringValue,
    )
    due_date = proto.Field(
        proto.MESSAGE, number=8, message=wrappers.StringValue,
    )
    service_date_range = proto.Field(
        proto.MESSAGE, number=9, message=dates.DateRange,
    )
    currency_code = proto.Field(
        proto.MESSAGE, number=10, message=wrappers.StringValue,
    )
    invoice_level_adjustments_micros = proto.Field(
        proto.MESSAGE, number=11, message=wrappers.Int64Value,
    )
    subtotal_amount_micros = proto.Field(
        proto.MESSAGE, number=12, message=wrappers.Int64Value,
    )
    tax_amount_micros = proto.Field(
        proto.MESSAGE, number=13, message=wrappers.Int64Value,
    )
    total_amount_micros = proto.Field(
        proto.MESSAGE, number=14, message=wrappers.Int64Value,
    )
    corrected_invoice = proto.Field(
        proto.MESSAGE, number=15, message=wrappers.StringValue,
    )
    replaced_invoices = proto.RepeatedField(
        proto.MESSAGE, number=16, message=wrappers.StringValue,
    )
    pdf_url = proto.Field(
        proto.MESSAGE, number=17, message=wrappers.StringValue,
    )
    account_budget_summaries = proto.RepeatedField(
        proto.MESSAGE, number=18, message=AccountBudgetSummary,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
