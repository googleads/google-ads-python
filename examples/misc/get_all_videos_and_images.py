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
"""This code example gets information about all video and image files."""


import argparse
import sys
from google.ads.google_ads.client import GoogleAdsClient
from google.ads.google_ads.errors import GoogleAdsException

_DEFAULT_PAGE_SIZE = 1000


def main(client, customer_id, page_size):
    """Main method, to run this code example as a standalone application."""
    ga_service = client.get_service("GoogleAdsService", version="v5")

    # Creates a query that will retrieve all video and image files.
    query = (
        "SELECT media_file.id, media_file.name, media_file.type "
        "FROM media_file ORDER BY media_file.id"
    )

    # Issues a search request by specifying page size.
    results = ga_service.search(customer_id, query=query, page_size=page_size)

    media_type_enum = client.get_type("MediaTypeEnum", version="v5").MediaType

    # Iterates over all rows and prints the information about each media file.
    try:
        for row in results:
            media_file = row.media_file
            print(
                f"Media file with ID {media_file.id}, "
                f'name "{media_file.name}", '
                f"type {media_type_enum.Name(media_file.type)} was found."
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
        description="List all videos and images for specified customer."
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

    main(google_ads_client, args.customer_id, _DEFAULT_PAGE_SIZE)
