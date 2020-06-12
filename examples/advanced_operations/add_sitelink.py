#!/usr/bin/env python
# Copyright 2019 Google LLC
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
"""Demonstrates how to create a sitelink extension."""


import argparse
import sys

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


def main(client, customer_id):
    # Create an extension setting.
    feed_service = client.get_service("ExtensionFeedItemService")

    extension_feed_item_operation = client.get_type(
        "ExtensionFeedItemOperation"
    )
    extension_feed_item = extension_feed_item_operation.create
    extension_feed_item.sitelink_feed_item.link_text = "Text"
    extension_feed_item.sitelink_feed_item.line1 = "Line 1 Value"
    extension_feed_item.sitelink_feed_item.line2 = "Line 2 Value"
    extension_feed_item.sitelink_feed_item.final_urls.append(
        "http://www.example.com"
    )

    # Add extension
    feed_response = feed_service.mutate_extension_feed_items(
        customer_id=customer_id, operations=[extension_feed_item_operation]
    )

    print(f"Created Sitelink {feed_response.results[0].resource_name}.")


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v6")

    parser = argparse.ArgumentParser(
        description="Creates sitelink for the specified customer id"
    )
    # The following argument(s) should be provided to run the example.
    parser.add_argument(
        "-c",
        "--customer_id",
        type=str,
        required=True,
        help="The Google Ads customer ID",
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
