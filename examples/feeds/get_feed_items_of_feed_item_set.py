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
"""This example gets all feed items of the specified feed item set.

To create a new feed item set, run create_feed_item_set.py.
To link a feed item to a feed item set, run link_feed_item_set.py.
"""


import argparse
import sys

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


def main(client, customer_id, feed_id, feed_item_set_id):
    """The main method that creates all necessary entities for the example.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        feed_id: the ID for a Feed belonging to the given customer.
        feed_item_set_id: the ID for a FeedItemSet belonging to the given
            customer.
    """
    ga_service = client.get_service("GoogleAdsService")
    feed_item_set_service = client.get_service("FeedItemSetService")

    feed_item_set_path = feed_item_set_service.feed_item_set_path(
        customer_id, feed_id, feed_item_set_id
    )
    query = f"""
        SELECT
          feed_item_set_link.feed_item
        FROM feed_item_set_link
        WHERE feed_item_set_link.feed_item_set = '{feed_item_set_path}'"""

    # Issues a search request using streaming.
    search_request = client.get_type("SearchGoogleAdsStreamRequest")
    search_request.customer_id = customer_id
    search_request.query = query
    response = ga_service.search_stream(request=search_request)

    print(
        "The feed items with the following resource names are linked with "
        f"the feed item set with ID {feed_item_set_id}:"
    )
    for batch in response:
        for row in batch.results:
            print(f"'{row.feed_item_set_link.feed_item}'")


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v8")

    parser = argparse.ArgumentParser(
        description="Gets all feed items of the specified feed item set."
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
        "-i", "--feed_id", type=str, required=True, help="The Feed ID.",
    )
    parser.add_argument(
        "-s",
        "--feed_item_set_id",
        type=str,
        required=True,
        help="The Feed Item Set ID.",
    )
    args = parser.parse_args()

    try:
        main(
            googleads_client,
            args.customer_id,
            args.feed_id,
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
