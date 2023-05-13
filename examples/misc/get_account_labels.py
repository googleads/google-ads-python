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
"""This example illustrates how to get a list of all labels, their IDs, their
descriptions, their statuses and their background colors for an account, then
prints them to the console in tabular format.
"""

import argparse
import sys
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


def main(client, customer_id):
    ga_service = client.get_service("GoogleAdsService")

    query = """
        SELECT
          label.id,
          label.name,
          label.text_label.description,
          label.status,
          label.text_label.background_color
        FROM label"""

    # Issues a search request using streaming.
    search_request = client.get_type("SearchGoogleAdsStreamRequest")
    search_request.customer_id = customer_id
    search_request.query = query

    stream = ga_service.search_stream(search_request)

    print(
        "Label Name".ljust(30),
        "Label ID".ljust(15),
        "Label Description".ljust(40),
        "Label Status".ljust(15),
        "Label Background Color",
    )

    for batch in stream:
        for row in batch.results:
            print(
                f"{row.label.name.ljust(30)} {str(row.label.id).ljust(15)} "
                f"{row.label.text_label.description.ljust(40)} "
                f"{row.label.status.name.ljust(15)} "
                f"{row.label.text_label.background_color}"
            )


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v13")

    parser = argparse.ArgumentParser(
        description=(
            "Retrieves all labels along with their IDs, descriptions, "
            "statuses, and background colors."
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
    args = parser.parse_args()

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
