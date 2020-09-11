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
"""This example illustrates how to get all account budget proposals.

To add an account budget proposal, run add_account_budget_proposal.py
"""


import argparse
import sys


import google.ads.google_ads.client


_DEFAULT_PAGE_SIZE = 1000


def main(client, customer_id, page_size):
    ga_service = client.get_service("GoogleAdsService", version="v5")

    query = """
        SELECT
          account_budget_proposal.id,
          account_budget_proposal.account_budget,
          account_budget_proposal.billing_setup,
          account_budget_proposal.status,
          account_budget_proposal.proposed_name,
          account_budget_proposal.proposed_notes,
          account_budget_proposal.proposed_purchase_order_number,
          account_budget_proposal.proposal_type,
          account_budget_proposal.approval_date_time,
          account_budget_proposal.creation_date_time
        FROM account_budget_proposal"""

    results = ga_service.search(customer_id, query=query, page_size=page_size)

    try:
        # Use the enum types to determine the enum names from the values.
        proposal_status_enum = client.get_type(
            "AccountBudgetProposalStatusEnum"
        ).AccountBudgetProposalStatus
        proposal_type_enum = client.get_type(
            "AccountBudgetProposalTypeEnum"
        ).AccountBudgetProposalType

        for row in results:
            budget_proposal = row.account_budget_proposal

            print(
                'Account budget proposal with ID "%s", status "%s", '
                'account_budget "%s", billing_setup "%s", '
                'proposed_name "%s", proposed_notes "%s", '
                'proposed_po_number "%s", proposal_type "%s", '
                'approval_date_time "%s", creation_date_time "%s"'
                % (
                    budget_proposal.id.value,
                    proposal_status_enum.Name(budget_proposal.status),
                    budget_proposal.account_budget.value,
                    budget_proposal.billing_setup.value,
                    budget_proposal.proposed_name.value,
                    budget_proposal.proposed_notes.value,
                    budget_proposal.proposed_purchase_order_number.value,
                    proposal_type_enum.Name(budget_proposal.proposal_type),
                    budget_proposal.approval_date_time.value,
                    budget_proposal.creation_date_time.value,
                )
            )
    except google.ads.google_ads.errors.GoogleAdsException as ex:
        print(
            'Request with ID "%s" failed with status "%s" and includes the '
            "following errors:" % (ex.request_id, ex.error.code().name)
        )
        for error in ex.failure.errors:
            print('\tError with message "%s".' % error.message)
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print("\t\tOn field: %s" % field_path_element.field_name)
        sys.exit(1)


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    google_ads_client = (
        google.ads.google_ads.client.GoogleAdsClient.load_from_storage()
    )

    parser = argparse.ArgumentParser(
        description="Lists all account budget proposals."
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

    main(google_ads_client, args.customer_id, _DEFAULT_PAGE_SIZE)
