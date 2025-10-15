#!/usr/bin/env python
# Copyright 2023 Google LLC
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
"""This code example adds an ad group asset.

To upload image assets, run misc/upload_image_asset.py.
"""


import argparse
import sys

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.ads.googleads.v22.resources.types.ad_group_asset import AdGroupAsset
from google.ads.googleads.v22.services.services.ad_group_asset_service.client import (
    AdGroupAssetServiceClient,
)
from google.ads.googleads.v22.services.types.ad_group_asset_service import (
    AdGroupAssetOperation,
    MutateAdGroupAssetResult,
    MutateAdGroupAssetsResponse,
)


def main(
    client: GoogleAdsClient,
    customer_id: str,
    ad_group_id: str,
    asset_id: str,
) -> None:
    ad_group_asset_service: AdGroupAssetServiceClient = client.get_service(
        "AdGroupAssetService"
    )
    ad_group_asset_resource_name: str = ad_group_asset_service.asset_path(
        customer_id, asset_id
    )

    ad_group_asset_operation: AdGroupAssetOperation = client.get_type(
        "AdGroupAssetOperation"
    )
    ad_group_asset_set: AdGroupAsset = ad_group_asset_operation.create
    ad_group_asset_set.asset = ad_group_asset_resource_name
    ad_group_asset_set.field_type = client.enums.AssetFieldTypeEnum.AD_IMAGE
    ad_group_asset_set.ad_group = ad_group_asset_service.ad_group_path(
        customer_id, ad_group_id
    )
    response: MutateAdGroupAssetsResponse = (
        ad_group_asset_service.mutate_ad_group_assets(
            customer_id=customer_id, operations=[ad_group_asset_operation]
        )
    )

    result: MutateAdGroupAssetResult
    for result in response.results:
        print(
            f"Created ad group asset with resource name: '{result.resource_name}'"
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=(
            "Updates an ad group for specified customer and ad group "
            "id with the given image asset id."
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
        "-s",
        "--asset_id",
        type=str,
        required=True,
        help="The asset ID.",
    )
    args = parser.parse_args()

    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v22")

    try:
        main(
            googleads_client, args.customer_id, args.ad_group_id, args.asset_id
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
