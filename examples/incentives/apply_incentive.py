#!/usr/bin/env python
# Copyright 2025 Google LLC
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
"""This example applies an incentive to a user's account.

This example is a no-op if the user already has an accepted incentive. If the
user attempts to apply a new incentive, the response will simply return the
existing incentive that has already been applied to the account. Use the
fetch_incentives.py example to get the available incentives.
"""


import argparse
import sys

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.ads.googleads.v23.services import ApplyIncentiveRequest, ApplyIncentiveResponse
from google.ads.googleads.v23.services.services.incentive_service.client import (
    IncentiveServiceClient,
)


def main(
    client: GoogleAdsClient,
    customer_id: str,
    incentive_id: str,
    country_code: str = None,
) -> None:
    """Applies an incentive for the ads customer.

    Args:
        client: An initialized GoogleAdsClient instance.
        customer_id: The client customer ID.
        country_code: The country code of the user.
        incentive_id: The incentive ID to select.
    """
    incentive_service: IncentiveServiceClient = client.get_service("IncentiveService")
    apply_incentive_request: ApplyIncentiveRequest = client.get_type(
        "ApplyIncentiveRequest"
    )

    apply_incentive_request.customer_id = customer_id
    apply_incentive_request.selected_incentive_id = incentive_id

    if country_code:
        apply_incentive_request.country_code = country_code

    response: ApplyIncentiveResponse = incentive_service.apply_incentive(
        request=apply_incentive_request
    )

    print("Applied incentive.")
    print(f"Coupon Code: {response.coupon_code}")
    print(f"Creation Time: {response.creation_time}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Applies an incentive for the ads customer."
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
        "-i",
        "--incentive_id",
        type=int,
        required=True,
        help="The incentive ID to select.",
    )
    parser.add_argument(
        "-k",
        "--country_code",
        type=str,
        required=False,
        help="The country code of the user (e.g. 'US').",
    )
    args = parser.parse_args()

    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v23")

    try:
        main(
            googleads_client,
            args.customer_id,
            args.incentive_id,
            args.country_code,
        )
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