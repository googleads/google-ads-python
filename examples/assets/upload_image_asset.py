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
"""This code example uploads an image asset.

To get image assets, run get_all_image_assets.py.
"""


import argparse
import sys

from examples.utils.example_helpers import get_image_bytes_from_url
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.ads.googleads.v22.services.types.asset_service import AssetOperation
from google.ads.googleads.v22.resources.types.asset import Asset


# [START upload_image_asset]
def main(client: GoogleAdsClient, customer_id: str) -> None:
    """Main method, to run this code example as a standalone application."""

    # Download image from URL
    url: str = "https://gaagl.page.link/Eit5"
    image_content: bytes = get_image_bytes_from_url(url)

    asset_service = client.get_service("AssetService")
    asset_operation: AssetOperation = client.get_type("AssetOperation")
    asset: Asset = asset_operation.create
    asset.type_ = client.enums.AssetTypeEnum.IMAGE
    asset.image_asset.data = image_content
    asset.image_asset.file_size = len(image_content)
    asset.image_asset.mime_type = client.enums.MimeTypeEnum.IMAGE_JPEG
    # Use your favorite image library to determine dimensions
    asset.image_asset.full_size.height_pixels = 315
    asset.image_asset.full_size.width_pixels = 600
    asset.image_asset.full_size.url = url
    # Provide a unique friendly name to identify your asset.
    # When there is an existing image asset with the same content but a different
    # name, the new name will be dropped silently.
    asset.name = "Marketing Image"

    mutate_asset_response = asset_service.mutate_assets(
        customer_id=customer_id, operations=[asset_operation]
    )
    print("Uploaded file(s):")
    for row in mutate_asset_response.results:
        print(f"\tResource name: {row.resource_name}")

    # [END upload_image_asset]


if __name__ == "__main__":
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Upload an image asset from a URL."
    )
    # The following argument(s) should be provided to run the example.
    parser.add_argument(
        "-c",
        "--customer_id",
        type=str,
        required=True,
        help="The Google Ads customer ID.",
    )
    args: argparse.Namespace = parser.parse_args()

    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client: GoogleAdsClient = GoogleAdsClient.load_from_storage(
        version="v22"
    )

    try:
        main(googleads_client, args.customer_id)
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
