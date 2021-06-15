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
"""This example adds an expanded text ad.

To get expanded text ads, run get_expanded_text_ads.py.
"""


import argparse
import sys
import uuid

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


# [START add_expanded_text_ads]
def main(client, customer_id, ad_group_id, number_of_ads):
    ad_group_ad_service = client.get_service("AdGroupAdService")
    ad_group_service = client.get_service("AdGroupService")

    ad_group_ad_operations = []
    for i in range(number_of_ads):
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
        ad_group_ad.ad.final_urls.append("http://www.example.com")
        ad_group_ad.ad.expanded_text_ad.description = "Buy your tickets now!"
        ad_group_ad.ad.expanded_text_ad.headline_part1 = (
            f"Cruise {i} to Mars {str(uuid.uuid4())[:8]}"
        )
        ad_group_ad.ad.expanded_text_ad.headline_part2 = (
            "Best space cruise line"
        )
        ad_group_ad.ad.expanded_text_ad.path1 = "all-inclusive"
        ad_group_ad.ad.expanded_text_ad.path2 = "deals"

        ad_group_ad_operations.append(ad_group_ad_operation)

    ad_group_ad_response = ad_group_ad_service.mutate_ad_group_ads(
        customer_id=customer_id, operations=ad_group_ad_operations
    )

    for result in ad_group_ad_response.results:
        print(f'Created ad group ad "{result.resource_name}".')
    # [END add_expanded_text_ads]


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
    parser.add_argument(
        "-n",
        "--number_of_ads",
        type=int,
        required=False,
        default=1,
        help="The number of ads.",
    )
    args = parser.parse_args()

    try:
        main(
            googleads_client,
            args.customer_id,
            args.ad_group_id,
            args.number_of_ads,
        )
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
