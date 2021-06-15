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
"""This adds an expanded text ad using advanced features of upgraded URLs."""


import argparse
import sys

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


def main(client, customer_id, ad_group_id):
    ad_group_ad_service = client.get_service("AdGroupAdService")
    ad_group_service = client.get_service("AdGroupService")

    # Create ad group ad.
    ad_group_ad_operation = client.get_type("AdGroupAdOperation")
    ad_group_ad = ad_group_ad_operation.create
    ad_group_ad.ad_group = ad_group_service.ad_group_path(
        customer_id, ad_group_id
    )
    ad_group_ad.status = client.get_type(
        "AdGroupAdStatusEnum"
    ).AdGroupAdStatus.PAUSED

    # Set expanded text ad info
    ad_group_ad.ad.final_urls.extend(
        [
            "http://www.example.com/cruise/space/",
            "http://www.example.com/locations/mars/",
        ]
    )

    ad_group_ad.ad.expanded_text_ad.description = (
        "Low-gravity fun for everyone!"
    )
    ad_group_ad.ad.expanded_text_ad.headline_part1 = "Luxury cruise to Mars"
    ad_group_ad.ad.expanded_text_ad.headline_part2 = (
        "Visit the Red Planet in Style."
    )

    # Specify a tracking URL for 3rd party tracking provider. You may specify
    # one at customer, campaign, ad group, ad, criterion, or feed item levels.
    ad_group_ad.ad.tracking_url_template = (
        "http://tracker.example.com/?season={_season}&promocode={_promocode}&"
        "u={lpurl}"
    )

    # Since your tracking URL has two custom parameters, provide their values
    # too. This can be provided at campaign, ad group, ad, criterion, or feed
    # item levels.
    param_1 = client.get_type("CustomParameter")
    param_1.key = "season"
    param_1.value = "easter123"

    param_2 = client.get_type("CustomParameter")
    param_2.key = "promocode"
    param_2.value = "nj123"
    ad_group_ad.ad.url_custom_parameters.extend([param_1, param_2])

    # Specify a list of final mobile URLs. This field cannot be set if URL field
    # is set, or finalUrls is unset. This may be specified at ad, criterion, and
    # feed item levels.
    ad_group_ad.ad.final_mobile_urls.extend(
        [
            "http://mobile.example.com/cruise/space/",
            "http://mobile.example.com/locations/mars/",
        ]
    )

    # Add the ad group ad.
    ad_group_ad_response = ad_group_ad_service.mutate_ad_group_ads(
        customer_id=customer_id, operations=[ad_group_ad_operation]
    )

    print(
        f'Created expanded text ad "{ad_group_ad_response.results[0].resource_name}".'
    )


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v8")

    parser = argparse.ArgumentParser(
        description=(
            "Adds an expanded text ad to the specified ad group ID, "
            "for the given customer ID."
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
        "-a", "--ad_group_id", type=str, required=True, help="The ad group ID."
    )
    args = parser.parse_args()

    try:
        main(googleads_client, args.customer_id, args.ad_group_id)
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
