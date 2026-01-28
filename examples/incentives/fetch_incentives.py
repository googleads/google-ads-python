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
"""This example returns incentives for a given user.

To apply an incentive, use apply_incentive.py.
"""


import argparse
import sys

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.ads.googleads.v23.services import FetchIncentiveRequest, FetchIncentiveResponse
from google.ads.googleads.v23.services.services.incentive_service.client import (
    IncentiveServiceClient,
)


def main(
    client: GoogleAdsClient,
    email_address: str,
    language_code: str,
    country_code: str,
) -> None:
    """Returns incentives for a given user.

    Args:
        client: An initialized GoogleAdsClient instance.
        email_address: The email of the user to fetch incentives for.
        language_code: The language code of the user (e.g. 'en').
        country_code: The country code of the user (e.g. 'US').
    """
    incentive_service: IncentiveServiceClient = client.get_service(
        "IncentiveService"
    )
    fetch_incentive_request: FetchIncentiveRequest = client.get_type(
        "FetchIncentiveRequest"
    )

    fetch_incentive_request.email = email_address
    fetch_incentive_request.language_code = language_code
    fetch_incentive_request.country_code = country_code

    response: FetchIncentiveResponse = incentive_service.fetch_incentive(
        request=fetch_incentive_request
    )

    if response.incentive_offer and response.incentive_offer.cyo_incentives:
        print("Fetched incentive.")
        # If the offer type is CHOOSE_YOUR_OWN_INCENTIVE, there will be three
        # incentives in the response. At the time this example was written, all
        # incentive offers are CYO incentive offers.
        cyo_incentives = response.incentive_offer.cyo_incentives
        print(cyo_incentives.low_offer)
        print(cyo_incentives.medium_offer)
        print(cyo_incentives.high_offer)
    else:
        print("No incentives found.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Returns incentives for a given user."
    )
    # The following argument(s) should be provided to run the example.
    parser.add_argument(
        "-e",
        "--email_address",
        type=str,
        required=True,
        help="The email of the user to fetch incentives for.",
    )
    parser.add_argument(
        "-l",
        "--language_code",
        type=str,
        required=False,
        default="en",
        help="The language code of the user (e.g. 'en').",
    )
    parser.add_argument(
        "-k",
        "--country_code",
        type=str,
        required=False,
        default="US",
        help="The country code of the user (e.g. 'US').",
    )
    args = parser.parse_args()

    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v23")

    try:
        main(
          googleads_client,
          args.email_address,
          args.language_code,
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
