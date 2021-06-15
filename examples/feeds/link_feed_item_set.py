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
"""Links the specified feed item set to the specified feed item.

The specified feed item set must not be created as a dynamic set, i.e. both
dynamic_location_set_filter and dynamic_affiliate_location_set_filter must not
be set. Learn more here:
https://developers.google.com/google-ads/api/docs/location-extensions/feed-item-set?hl=en#adding-feed-item
"""

import argparse
import sys

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


def main(client, customer_id, feed_id, feed_item_id, feed_item_set_id):
    """The main method that creates all necessary entities for the example.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        feed_id: the ID of the feed associated with the specified feed item set.
        feed_item_id: the ID of the specified feed item.
        feed_item_set_id: the ID of the feed item set to link to the feed item.
    """
    feed_item_set_link_service = client.get_service("FeedItemSetLinkService")
    feed_item_set_link_operation = client.get_type("FeedItemSetLinkOperation")

    # Construct an operation that will link the feed item to the feed item set.
    feed_item_set_link = feed_item_set_link_operation.create

    # Construct a resource name for a feed item, which is in the format:
    # customers/{customer_id}/feedItems/{feed_id}~{feed_item_id}
    feed_item_set_link.feed_item = client.get_service(
        "FeedItemService"
    ).feed_item_path(customer_id, feed_id, feed_item_id)
    # Construct a resource name for a feed item set, which is in the
    # format: customers/{customer_id}/feedItemSets/{feed_id}~{feed_item_set_id}
    feed_item_set_link.feed_item_set = client.get_service(
        "FeedItemSetService"
    ).feed_item_set_path(customer_id, feed_id, feed_item_set_id)

    # Issue a mutate request to add the feed item set link on the server.
    response = feed_item_set_link_service.mutate_feed_item_set_links(
        customer_id=customer_id, operations=[feed_item_set_link_operation]
    )
    print(
        "Created a feed item set link with resource name: "
        f"'{response.results[0].resource_name}'"
    )


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v8")

    parser = argparse.ArgumentParser(
        description="Links the specified feed item set to the specified feed item."
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
        "-f", "--feed_id", type=str, required=True, help="The feed ID.",
    )
    parser.add_argument(
        "-i",
        "--feed_item_id",
        type=str,
        required=True,
        help="The feed item ID.",
    )
    parser.add_argument(
        "-s",
        "--feed_item_set_id",
        type=str,
        required=True,
        help="The feed item set ID.",
    )
    args = parser.parse_args()

    try:
        main(
            googleads_client,
            args.customer_id,
            args.feed_id,
            args.feed_item_id,
            args.feed_item_set_id,
        )
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
