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
"""This code example uploads an image."""


import argparse
import sys
import requests

from google.ads.google_ads.client import GoogleAdsClient
from google.ads.google_ads.errors import GoogleAdsException


def main(client, customer_id):
    """Main method, to run this code example as a standalone application."""
    URL = "https://goo.gl/3b9Wfh"

    media_file_operation = client.get_type("MediaFileOperation", version="v5")
    media_file = media_file_operation.create
    media_file.name = "Ad Image"
    media_file.type = client.get_type("MediaTypeEnum", version="v5").IMAGE
    media_file.source_url = URL
    # Download the image as bytes from the URL
    media_file.image.data = requests.get(URL).content

    media_file_service = client.get_service("MediaFileService", version="v5")

    try:
        mutate_media_files_response = media_file_service.mutate_media_files(
            customer_id, [media_file_operation]
        )
        print(f"Uploaded file(s):")
        for row in mutate_media_files_response.results:
            print(f"\tResource name: {row.resource_name}")

    except GoogleAdsException as ex:
        print(
            'Request with ID "%s" failed with status "%s" and includes the '
            "following errors:" % (ex.request_id, ex.error.code().name)
        )
        for error in ex.failure.errors:
            print('\tError with message "%s".' % error.message)
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print("\t\tOn field: %s" % field_path_element.field_name)
        sys.exit(1)


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    google_ads_client = GoogleAdsClient.load_from_storage()

    parser = argparse.ArgumentParser(description="Upload an image from a URL.")
    # The following argument(s) should be provided to run the example.
    parser.add_argument(
        "-c",
        "--customer_id",
        type=str,
        required=True,
        help="The Google Ads customer ID.",
    )
    args = parser.parse_args()

    main(google_ads_client, args.customer_id)
