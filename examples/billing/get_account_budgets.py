#!/usr/bin/env python
# Copyright 2018 Google LLC
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
"""This illustrates how to get all account budgets for a Google Ads customer."""


import argparse
import sys

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


def main(client, customer_id):
    ga_service = client.get_service("GoogleAdsService")

    query = """
        SELECT
          account_budget.status,
          account_budget.billing_setup,
          account_budget.approved_spending_limit_micros,
          account_budget.approved_spending_limit_type,
          account_budget.proposed_spending_limit_micros,
          account_budget.proposed_spending_limit_type,
          account_budget.adjusted_spending_limit_micros,
          account_budget.adjusted_spending_limit_type,
          account_budget.approved_start_date_time,
          account_budget.proposed_start_date_time,
          account_budget.approved_end_date_time,
          account_budget.approved_end_time_type,
          account_budget.proposed_end_date_time,
          account_budget.proposed_end_time_type
        FROM account_budget"""

    response = ga_service.search_stream(customer_id=customer_id, query=query)

    for batch in response:
        for row in batch.results:
            budget = row.account_budget

            # Here and in the statements below, the variable is set to the
            # name of the Enum as a default if the numeric value for the
            # monetary or date fields is not present.
            approved_spending_limit = (
                _micros_to_currency(budget.approved_spending_limit_micros)
                or budget.approved_spending_limit_type.name
            )

            proposed_spending_limit = (
                _micros_to_currency(budget.proposed_spending_limit_micros)
                or budget.proposed_spending_limit_type.name
            )

            adjusted_spending_limit = (
                _micros_to_currency(budget.adjusted_spending_limit_micros)
                or budget.adjusted_spending_limit_type.name
            )

            approved_end_date_time = (
                budget.approved_end_date_time
                or budget.approved_end_time_type.name
            )

            proposed_end_date_time = (
                budget.proposed_end_date_time
                or budget.proposed_end_time_type.name
            )

            amount_served = (
                _micros_to_currency(budget.amount_served_micros) or 0.0
            )

            total_adjustments = (
                _micros_to_currency(budget.total_adjustments_micros) or 0.0
            )

            print(
                f'Account budget "{budget.resource_name}", '
                f'with status "{budget.status.name}", '
                f'billing setup "{budget.billing_setup}", '
                f"amount served {amount_served:.2f}, "
                f"total adjustments {total_adjustments:.2f}, "
                f'approved spending limit "{approved_spending_limit}" '
                f'(proposed "{proposed_spending_limit}" -- '
                f'adjusted "{adjusted_spending_limit}"), approved '
                f'start time "{budget.approved_start_date_time}" '
                f'(proposed "{budget.proposed_start_date_time}"), '
                f'approved end time "{approved_end_date_time}" '
                f'(proposed "{proposed_end_date_time}").'
            )


def _micros_to_currency(micros):
    return micros / 1000000.0 if micros is not None else None


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v8")

    parser = argparse.ArgumentParser(
        description=(
            "Lists all account budgets for given Google Ads customer ID."
        )
    )
    # The following argument(s) should be provided to run the example.
    parser.add_argument(
        "-c",
        "--customer_id",
        type=str,
        required=True,
        help="The Google Ads customer ID.",
    )
    args = parser.parse_args()

    try:
        main(googleads_client, args.customer_id)
    except GoogleAdsException as ex:
        print(
            f'Request with ID "{ex.request_id}" failed with status '
            f'"{ex.error.code().name}" and includes the following errors:'
        )
        for error in ex.failure.errors:
            print(f'	Error with message "{error.message}".')
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print(f"\t\tOn field: {field_path_element.field_name}")
        sys.exit(1)
