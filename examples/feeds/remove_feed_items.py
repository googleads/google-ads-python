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
"""Removes feed items from a feed."""


import argparse
import sys

from google.ads.google_ads.client import GoogleAdsClient
from google.ads.google_ads.errors import GoogleAdsException
from google.ads.google_ads.util import ResourceName


def main(client, customer_id, feed_id, feed_item_ids):
    """The main method that creates all necessary entities for the example.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        feed_id: the ID for a Feed belonging to the given customer.
        feed_item_ids: a list of FeedItem IDs belonging to the given Feed.
    """
    feed_item_service = client.get_service("FeedItemService", version="v5")

    operations = []
    for feed_item_id in feed_item_ids:
        # Constructs an operation that will remove the feed item based on the
        # resource name.
        feed_item_operation = client.get_type("FeedItemOperation", version="v5")
        # Constructs a resource name for a feed_item, which is in the
        # format: customers/{customer_id}/feedItems/{feed_id}~{feed_item_id}
        feed_item_operation.remove = feed_item_service.feed_item_path(
            customer_id,
            ResourceName.format_composite(feed_id, feed_item_id),
        )
        operations.append(feed_item_operation)

    try:
        response = feed_item_service.mutate_feed_items(customer_id, operations)

        for feed_item in response.results:
            print(
                "Removed feed item with resource name: "
                f"'{feed_item.resource_name}'"
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
        description="Removes feed items from a feed."
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
        "-f",
        "--feed_id",
        type=str,
        required=True,
        help="The ID of the feed to remove feed items from.",
    )
    parser.add_argument(
        "-i",
        "--feed_item_ids",
        nargs=2,
        type=str,
        required=True,
        help="Space-delimited list of IDs for feed items to remove from the"
        "given feed.",
    )
    args = parser.parse_args()

    main(
        google_ads_client, args.customer_id, args.feed_id, args.feed_item_ids,
    )
