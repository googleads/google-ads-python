#!/usr/bin/env python
# Copyright 2020 Google LLC
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
"""This example updates an expanded text ad.

To get expanded text ads, run get_expanded_text_ads.py.
"""


import argparse
import sys
import uuid

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.api_core import protobuf_helpers


# [START update_expanded_text_ad]
def main(client, customer_id, ad_id):
    ad_service = client.get_service("AdService")
    ad_operation = client.get_type("AdOperation")

    # Update ad operation.
    ad = ad_operation.update
    ad.resource_name = ad_service.ad_path(customer_id, ad_id)
    ad.expanded_text_ad.headline_part1 = (
        f"Cruise to Pluto {str(uuid.uuid4())[:8]}"
    )
    ad.expanded_text_ad.headline_part2 = "Tickets on sale now"
    ad.expanded_text_ad.description = "Best space cruise ever."
    ad.final_urls.append("http://www.example.com")
    ad.final_mobile_urls.append("http://www.example.com/mobile")
    client.copy_from(
        ad_operation.update_mask, protobuf_helpers.field_mask(None, ad._pb)
    )

    # Updates the ad.
    ad_response = ad_service.mutate_ads(
        customer_id=customer_id, operations=[ad_operation]
    )
    print(
        f'Ad with resource name "{ad_response.results[0].resource_name}" '
        "was updated."
    )
    # [END update_expanded_text_ad]


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v8")

    parser = argparse.ArgumentParser(
        description=(
            "Updates the specified expanded text ad, "
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
        "-i", "--ad_id", type=str, required=True, help="The ad ID."
    )
    args = parser.parse_args()

    try:
        main(googleads_client, args.customer_id, args.ad_id)
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
