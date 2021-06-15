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
"""This example removes a billing setup with the specified ID.

To get available billing setups, run get_billing_setups.py.
"""


import argparse
import sys

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


# [START remove_billing_setup]
def main(client, customer_id, billing_setup_id):
    billing_setup_service = client.get_service("BillingSetupService")

    # Create billing setup operation.
    billing_setup_operation = client.get_type("BillingSetupOperation")
    billing_setup_operation.remove = billing_setup_service.billing_setup_path(
        customer_id, billing_setup_id
    )

    # Remove the billing setup.
    billing_setup_response = billing_setup_service.mutate_billing_setup(
        customer_id=customer_id, operation=billing_setup_operation
    )
    print(
        "Removed billing setup "
        f'"{billing_setup_response.results[0].resource_name}"'
    )
    # [END remove_billing_setup]


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v8")

    parser = argparse.ArgumentParser(
        description=(
            "Removes billing setup for specified customer and billing "
            "setup ID."
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
            print(f'	Error with message "{error.message}".')
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print(f"\t\tOn field: {field_path_element.field_name}")
        sys.exit(1)
