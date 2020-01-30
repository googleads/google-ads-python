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

To get image assets, run get_all_image_assets.py."""


import argparse
import sys
import requests

from google.ads.google_ads.client import GoogleAdsClient
from google.ads.google_ads.errors import GoogleAdsException


def main(client, customer_id):
    """Main method, to run this code example as a standalone application."""

    # Download image from URL
    URL = 'https://goo.gl/3b9Wfh'
    image_content = requests.get(URL).content

    asset_operation = client.get_type('AssetOperation', version='v2')
    asset = asset_operation.create
    asset.type = client.get_type('AssetTypeEnum', version='v2').IMAGE
    asset.image_asset.data.value = image_content
    asset.image_asset.file_size.value = len(image_content)
    asset.image_asset.mime_type = client.get_type('MimeTypeEnum').IMAGE_JPEG
    # Use your favorite image library to determine dimensions
    asset.image_asset.full_size.height_pixels.value = 315
    asset.image_asset.full_size.width_pixels.value = 600
    asset.image_asset.full_size.url.value = URL
    # Optional: Provide a unique friendly name to identify your asset.
    # If you specify the name field, then both the asset name and the image
    # being uploaded should be unique, and should not match another ACTIVE
    # asset in this customer account.
    # asset.name = 'Jupiter Trip #' + uuid.uuid4()

    asset_service = client.get_service('AssetService', version='v2')

    try:
        mutate_asset_response = (
            asset_service.mutate_assets(customer_id,
                                        [asset_operation])
        )
        print('Uploaded file(s):')
        for row in mutate_asset_response.results:
            print(f'\tResource name: {row.resource_name}')

    except GoogleAdsException as ex:
        print(f'Request with ID "{ex.request_id}" failed with status '
              f'"{ex.error.code().name}" and includes the following errors:')
        for error in ex.failure.errors:
            print(f'\tError with message "{error.message}".')
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print(f'\t\tOn field: {field_path_element.field_name}')
        sys.exit(1)


if __name__ == '__main__':
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    google_ads_client = GoogleAdsClient.load_from_storage()

    parser = argparse.ArgumentParser(
        description='Upload an image asset from a URL.')
    # The following argument(s) should be provided to run the example.
    parser.add_argument('-c', '--customer_id', type=str,
                        required=True, help='The Google Ads customer ID.')
    args = parser.parse_args()

    main(google_ads_client, args.customer_id)
