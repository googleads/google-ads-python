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
"""This example gets non-removed responsive search ads in a specified ad group.

To add responsive search ads, run basic_operations/add_responsive_search_ad.py.
To get ad groups, run basic_operations/get_ad_groups.py.
"""

import argparse
import sys
from typing import List, Optional, Sequence

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.ads.googleads.v22.common.types.ad_asset import AdTextAsset
from google.ads.googleads.v22.resources.types.ad import Ad
from google.ads.googleads.v22.services.services.google_ads_service import (
    GoogleAdsServiceClient,
)
from google.ads.googleads.v22.services.types.google_ads_service import (
    SearchGoogleAdsRequest,
    SearchGoogleAdsResponse,
)


def main(
    client: GoogleAdsClient,
    customer_id: str,
    ad_group_id: Optional[str] = None,
) -> None:
    ga_service: GoogleAdsServiceClient = client.get_service("GoogleAdsService")

    query: str = """
        SELECT
          ad_group.id,
          ad_group_ad.ad.id,
          ad_group_ad.ad.responsive_search_ad.headlines,
          ad_group_ad.ad.responsive_search_ad.descriptions,
          ad_group_ad.status
        FROM ad_group_ad
          WHERE ad_group_ad.ad.type = RESPONSIVE_SEARCH_AD
          AND ad_group_ad.status != REMOVED"""

    # Optional: Specify an ad group ID to restrict search to only a given
    # ad group.
    if ad_group_id:
        query += f" AND ad_group.id = {ad_group_id}"

    ga_search_request: SearchGoogleAdsRequest = client.get_type(
        "SearchGoogleAdsRequest"
    )
    ga_search_request.customer_id = customer_id
    ga_search_request.query = query
    results: SearchGoogleAdsResponse = ga_service.search(
        request=ga_search_request
    )

    one_found: bool = False

    for row in results:
        one_found = True
        ad: Ad = row.ad_group_ad.ad
        print(
            "Responsive search ad with resource name "
            f'"{ad.resource_name}", status {row.ad_group_ad.status.name} '
            "was found."
        )
        headlines: str = "\n".join(
            ad_text_assets_to_strs(ad.responsive_search_ad.headlines)
        )
        descriptions: str = "\n".join(
            ad_text_assets_to_strs(ad.responsive_search_ad.descriptions)
        )
        print(f"Headlines:\n{headlines}\nDescriptions:\n{descriptions}\n")

    if not one_found:
        print("No responsive search ads were found.")


def ad_text_assets_to_strs(assets: Sequence[AdTextAsset]) -> List[str]:
    """Converts a list of AdTextAssets to a list of user-friendly strings."""
    s: List[str] = []
    asset: AdTextAsset
    for asset in assets:
        s.append(f"\t {asset.text} pinned to {asset.pinned_field.name}")
    return s


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="List responsive display ads for specified customer. "
        "An ad_group is optional."
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
            ad_group_id=args.ad_group_id,
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
