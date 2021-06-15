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
"""This code example gets all image assets."""


import argparse
import sys

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

_DEFAULT_PAGE_SIZE = 1000


def main(client, customer_id, page_size):
    """Main method, to run this code example as a standalone application."""
    ga_service = client.get_service("GoogleAdsService")

    query = """
        SELECT
          asset.name,
          asset.image_asset.file_size,
          asset.image_asset.full_size.width_pixels,
          asset.image_asset.full_size.height_pixels,
          asset.image_asset.full_size.url
        FROM asset
        WHERE asset.type = IMAGE"""

    search_request = client.get_type("SearchGoogleAdsRequest")
    search_request.customer_id = customer_id
    search_request.query = query
    search_request.page_size = page_size
    results = ga_service.search(search_request)

    results = ga_service.search(request=search_request)

    count = 0
    for row in results:
        asset = row.asset
        image_asset = asset.image_asset
        count += 1
        print(
            f'Image with name "{asset.name}" found:\n'
            f"\tfile size {image_asset.file_size} bytes\n"
            f"\twidth {image_asset.full_size.width_pixels}px\n"
            f"\theight {image_asset.full_size.height_pixels}px\n"
            f'\turl "{image_asset.full_size.url}"'
        )

    print(f"Total of {count} image(s) found.")


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v8")

    parser = argparse.ArgumentParser(
        description="List all image assets for specified customer."
    )
    # The following argument(s) should be provided to run the example.
    parser.add_argument(
        "-c",
        "--customer_id",
        type=str,
        required=True,
        help="The Google Ads customer ID.",
    )
    args = parser.parse_args()

    try:
        main(googleads_client, args.customer_id, _DEFAULT_PAGE_SIZE)
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
