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
"""This example illustrates how to retrieve expanded text ads."""


import argparse
import sys

from google.ads.google_ads.client import GoogleAdsClient
from google.ads.google_ads.errors import GoogleAdsException


def main(client, customer_id, ad_group_id=None):
    ga_service = client.get_service("GoogleAdsService", version="v5")
    ad_group_ad_status_enum = client.get_type(
        "AdGroupAdStatusEnum", version="v5"
    ).AdGroupAdStatus

    query = """
        SELECT
          ad_group.id,
          ad_group_ad.ad.id,
          ad_group_ad.ad.expanded_text_ad.headline_part1,
          ad_group_ad.ad.expanded_text_ad.headline_part2,
          ad_group_ad.status
        FROM ad_group_ad
        WHERE ad_group_ad.ad.type = EXPANDED_TEXT_AD"""

    if ad_group_id:
        query += f" AND ad_group.id = {ad_group_id}"

    response = ga_service.search_stream(customer_id, query=query)

    try:
        for batch in response:
            for row in batch.results:
                ad = row.ad_group_ad.ad

                if ad.expanded_text_ad:
                    expanded_text_ad_info = ad.expanded_text_ad

                print(
                    f"Expanded text ad with ID {ad.id}, status "
                    f'"{ad_group_ad_status_enum.Name(row.ad_group_ad.status)}", '
                    "and headline "
                    f'"{expanded_text_ad_info.headline_part1}"'
                    f' - "{expanded_text_ad_info.headline_part2}" was '
                    f"found in ad group with ID {row.ad_group.id}."
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


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    google_ads_client = GoogleAdsClient.load_from_storage()

    parser = argparse.ArgumentParser(
        description="List ad groups for specified customer."
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
        required=False,
        help="The ad group ID. ",
    )
    args = parser.parse_args()

    main(google_ads_client, args.customer_id, ad_group_id=args.ad_group_id)
