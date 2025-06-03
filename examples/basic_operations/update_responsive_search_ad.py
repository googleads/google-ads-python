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
"""This example updates a responsive search ad.

To get responsive search ads, run get_responsive_search_ads.py.
"""


import argparse
import sys
from uuid import uuid4

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.api_core import protobuf_helpers


# [START update_responsive_search_ad]
def main(client, customer_id, ad_id):
    ad_service = client.get_service("AdService")
    ad_operation = client.get_type("AdOperation")

    # Update ad operation.
    ad = ad_operation.update
    ad.resource_name = ad_service.ad_path(customer_id, ad_id)

    # Update some properties of the responsive search ad.
    headline_1 = client.get_type("AdTextAsset")
    headline_1.text = f"Cruise to Pluto #{uuid4().hex[:8]}"
    headline_1.pinned_field = client.enums.ServedAssetFieldTypeEnum.HEADLINE_1

    headline_2 = client.get_type("AdTextAsset")
    headline_2.text = "Tickets on sale now"

    headline_3 = client.get_type("AdTextAsset")
    headline_3.text = "Buy your tickets now"

    ad.responsive_search_ad.headlines.extend(
        [headline_1, headline_2, headline_3]
    )

    description_1 = client.get_type("AdTextAsset")
    description_1.text = "Best space cruise ever."

    description_2 = client.get_type("AdTextAsset")
    description_2.text = (
        "The most wonderful space experience you will ever have."
    )

    ad.final_urls.append("https://www.example.com")
    ad.final_mobile_urls.append("https://www.example.com/mobile")
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
    # [END update_responsive_search_ad]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=(
            "Updates the specified responsive search ad, for the given "
            "customer ID."
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

    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v20")

    try:
        main(googleads_client, args.customer_id, args.ad_id)
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
