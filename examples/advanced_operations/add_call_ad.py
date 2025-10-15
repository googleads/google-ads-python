#!/usr/bin/env python
# Copyright 2022 Google LLC
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
"""This example adds a call ad to a given ad group.

More information about call ads can be found at:
https://support.google.com/google-ads/answer/6341403.

To get ad group IDs, run basic_operations/get_ad_groups.py.
"""


import argparse
import sys
from typing import Optional

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.ads.googleads.v22.resources.types.ad import Ad
from google.ads.googleads.v22.resources.types.ad_group_ad import AdGroupAd
from google.ads.googleads.v22.services.services.ad_group_ad_service import (
    AdGroupAdServiceClient,
)
from google.ads.googleads.v22.services.services.google_ads_service import (
    GoogleAdsServiceClient,
)
from google.ads.googleads.v22.services.types.ad_group_ad_service import (
    AdGroupAdOperation,
    MutateAdGroupAdsResponse,
)

# Country code is a two-letter ISO-3166 code, for a list of all codes see:
# https://developers.google.com/google-ads/api/reference/data/codes-formats#expandable-17
_DEFAULT_PHONE_COUNTRY: str = "US"


def main(
    client: GoogleAdsClient,
    customer_id: str,
    ad_group_id: str,
    phone_number: str,
    phone_country: str,
    conversion_action_id: Optional[str],
) -> None:
    """The main method that creates all necessary entities for the example.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        ad_group_id: an ad group ID.
        phone_number: a phone number for your business, e.g. '(800) 555-0100'.
        phone_country: a two-letter ISO-3166 code.
        conversion_action_id: an ID for a conversion action.
    """
    googleads_service: GoogleAdsServiceClient = client.get_service(
        "GoogleAdsService"
    )
    operation: AdGroupAdOperation = client.get_type("AdGroupAdOperation")
    ad_group_ad: AdGroupAd = operation.create
    ad_group_ad.ad_group = googleads_service.ad_group_path(
        customer_id, ad_group_id
    )
    ad_group_ad.status = client.enums.AdGroupAdStatusEnum.PAUSED
    ad: Ad = ad_group_ad.ad
    # The URL of the webpage to refer to.
    ad.final_urls.append("https://www.example.com")
    # Sets basic information.
    ad.call_ad.business_name = "Google"
    ad.call_ad.headline1 = "Travel"
    ad.call_ad.headline2 = "Discover"
    ad.call_ad.description1 = "Travel the World"
    ad.call_ad.description2 = "Travel the Universe"
    # Sets the country code and phone number of the business to call.
    ad.call_ad.country_code = phone_country
    ad.call_ad.phone_number = phone_number
    # Sets the verification URL to a webpage that includes the phone number.
    ad.call_ad.phone_number_verification_url = "https://www.example.com/contact"

    # The fields below are optional.
    # Configures call tracking and reporting.
    ad.call_ad.call_tracked = True
    ad.call_ad.disable_call_conversion = False
    # Sets path parts to append for display.
    ad.call_ad.path1 = "services"
    ad.call_ad.path2 = "travels"

    # Sets the conversion action ID if provided.
    if conversion_action_id:
        ad.call_ad.conversion_action = googleads_service.conversion_action_path(
            customer_id, conversion_action_id
        )
        ad.call_ad.conversion_reporting_state = (
            client.enums.CallConversionReportingStateEnum.USE_RESOURCE_LEVEL_CALL_CONVERSION_ACTION
        )

    # Issues a mutate request to add the ad group ad.
    ad_group_ad_service: AdGroupAdServiceClient = client.get_service(
        "AdGroupAdService"
    )
    response: MutateAdGroupAdsResponse = (
        ad_group_ad_service.mutate_ad_group_ads(
            customer_id=customer_id, operations=[operation]
        )
    )
    resource_name: str = response.results[0].resource_name
    print(f"Created ad group ad with resource name: '{resource_name}'")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=("Adds a call extension to a specific account.")
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
        "-a",
        "--ad_group_id",
        type=str,
        required=True,
        help="An ad group ID.",
    )
    parser.add_argument(
        "-n",
        "--phone_number",
        type=str,
        required=True,
        help=("A phone number for your business, e.g. '(800) 555-0100'"),
    )
    parser.add_argument(
        "-p",
        "--phone_country",
        type=str,
        default=_DEFAULT_PHONE_COUNTRY,
        help=(
            "A two-letter ISO-3166 code representing a country code, for a "
            "list of all codes see: "
            "https://developers.google.com/google-ads/api/reference/data/codes-formats#expandable-17"
        ),
    )
    parser.add_argument(
        "-v",
        "--conversion_action_id",
        type=str,
        help=("An optional conversion action ID to attribute conversions to."),
    )

    args: argparse.Namespace = parser.parse_args()

    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client: GoogleAdsClient = GoogleAdsClient.load_from_storage(
        version="v22"
    )

    try:
        main(
            googleads_client,
            args.customer_id,
            args.ad_group_id,
            args.phone_number,
            args.phone_country,
            args.conversion_action_id,
        )
    except GoogleAdsException as ex:
        print(
            f'Request with ID "{ex.request_id}" failed with status '
            f'"{ex.error.code().name}" and includes the following errors:'
        )
        for error in ex.failure.errors:
            print(f'Error with message "{error.message}".')
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print(f"\t\tOn field: {field_path_element.field_name}")
        sys.exit(1)
