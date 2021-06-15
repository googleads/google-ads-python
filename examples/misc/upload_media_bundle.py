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
"""This example uploads an HTML5 zip file as a media bundle."""


import argparse
import sys

import requests

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


BUNDLE_URL = "https://goo.gl/9Y7qI2"


def main(client, customer_id):
    media_file_service = client.get_service("MediaFileService")
    media_file_operation = client.get_type("MediaFileOperation")
    media_file = media_file_operation.create
    media_file.name = "Ad Media Bundle"
    media_file.type_ = client.get_type("MediaTypeEnum").MediaType.MEDIA_BUNDLE
    # Download the ZIP as bytes from the URL
    media_file.media_bundle.data = requests.get(BUNDLE_URL).content

    mutate_media_files_response = media_file_service.mutate_media_files(
        customer_id=customer_id, operations=[media_file_operation]
    )
    print(
        f"Uploaded file with resource name "
        f'"{mutate_media_files_response.results[0].resource_name}"'
    )


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v8")

    parser = argparse.ArgumentParser(description="Uploads a media bundle.")
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
        main(googleads_client, args.customer_id)
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
