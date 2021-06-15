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
"""Gets all billing setup objects available for the specified customer ID."""


import argparse
import sys

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


# [START get_billing_setup]
def main(client, customer_id):
    ga_service = client.get_service("GoogleAdsService")

    query = """
        SELECT
          billing_setup.id,
          billing_setup.status,
          billing_setup.payments_account,
          billing_setup.payments_account_info.payments_account_id,
          billing_setup.payments_account_info.payments_account_name,
          billing_setup.payments_account_info.payments_profile_id,
          billing_setup.payments_account_info.payments_profile_name,
          billing_setup.payments_account_info.secondary_payments_profile_id
        FROM billing_setup"""

    response = ga_service.search_stream(customer_id=customer_id, query=query)

    print("Found the following billing setup results:")
    for batch in response:
        for row in batch.results:
            billing_setup = row.billing_setup
            pai = billing_setup.payments_account_info

            if pai.secondary_payments_profile_id:
                secondary_payments_profile_id = (
                    pai.secondary_payments_profile_id
                )
            else:
                secondary_payments_profile_id = "None"

            print(
                f"Billing setup with ID {billing_setup.id}, "
                f'status "{billing_setup.status.name}", '
                f'payments_account "{billing_setup.payments_account}" '
                f"payments_account_id {pai.payments_account_id}, "
                f'payments_account_name "{pai.payments_account_name}", '
                f"payments_profile_id {pai.payments_profile_id}, "
                f'payments_profile_name "{pai.payments_profile_name}", '
                "secondary_payments_profile_id "
                f"{secondary_payments_profile_id}."
            )
    # [END get_billing_setup]


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v8")

    parser = argparse.ArgumentParser(
        description="Lists all billing setup objects for specified customer."
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
