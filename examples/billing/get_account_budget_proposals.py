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


from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


_DEFAULT_PAGE_SIZE = 1000


def main(client, customer_id, page_size):
    ga_service = client.get_service("GoogleAdsService")

    query = (
        "SELECT account_budget_proposal.id, "
        "account_budget_proposal.account_budget,"
        "account_budget_proposal.billing_setup,"
        "account_budget_proposal.status,"
        "account_budget_proposal.proposed_name,"
        "account_budget_proposal.proposed_notes,"
        "account_budget_proposal.proposed_purchase_order_number,"
        "account_budget_proposal.proposal_type,"
        "account_budget_proposal.approval_date_time,"
        "account_budget_proposal.creation_date_time "
        "FROM account_budget_proposal"
    )

    search_request = client.get_type("SearchGoogleAdsRequest")
    search_request.customer_id = customer_id
    search_request.query = query
    search_request.page_size = page_size

    results = ga_service.search(request=search_request)

    for row in results:
        budget_proposal = row.account_budget_proposal

        print(
            'Account budget proposal with ID "{budget_proposal.id}", '
            'status "{budget_proposal.status.name}", '
            'account_budget "{budget_proposal.account_budget}", '
            'billing_setup "{budget_proposal.billing_setup}", '
            'proposed_name "{budget_proposal.proposed_name}", '
            'proposed_notes "{budget_proposal.proposed_notes}", '
            "proposed_po_number "
            '"{budget_proposal.proposed_purchase_order_number}", '
            'proposal_type "{budget_proposal.proposal_type.name}", '
            'approval_date_time "{budget_proposal.approval_date_time}", '
            'creation_date_time "{budget_proposal.creation_date_time}"'
        )


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v8")

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

    try:
        main(googleads_client, args.customer_id, _DEFAULT_PAGE_SIZE)
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
