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
"""Creates a new feed item set for a specified feed.

The feed must belong to either a Google Ads location extension or an affiliate
extension. This is equivalent to a "location group" in the Google Ads UI. See
https://support.google.com/google-ads/answer/9288588 for more detail.
"""

import argparse
import sys
import uuid

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


def main(client, customer_id, feed_id):
    """The main method that creates all necessary entities for the example.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        feed_id: the ID for a Feed belonging to the given customer.
    """
    feed_item_set_service = client.get_service("FeedItemSetService")
    feed_item_set_operation = client.get_type("FeedItemSetOperation")

    feed_item_set = feed_item_set_operation.create
    feed_resource_name = client.get_service("FeedService").feed_path(
        customer_id, feed_id
    )
    feed_item_set.feed = feed_resource_name
    feed_item_set.display_name = f"Feed Item Set #{uuid.uuid4()}"

    # A feed item set can be created as a dynamic set by setting an optional
    # filter field below. If your feed is a location extension, uncomment the code
    # that sets dynamic_location_set_filter. If your feed is an affiliate
    # extension, set dynamic_affiliate_location_set_filter instead.

    # 1) Location Extension
    # NOTE: Does not support Curated location extensions.
    # dynamic_location_set_filter = feed_item_set.dynamic_location_set_filter
    # business_name_filter = dynamic_location_set_filter.business_name_filter
    # business_name_filter.business_name = 'INSERT_YOUR_BUSINESS_NAME_HERE'
    # business_name_filter.filter_type = client.get_type(
    #     "FeedItemSetStringFilterTypeEnum"
    # ).FeedItemSetStringFilterType.EXACT

    # 2) Affiliate Extension
    # dynamic_affiliate_location_set_filter = feed_item_set.dynamic_affiliate_location_set_filter
    # dynamic_affiliate_location_set_filter.chain_ids.extend([INSERT_CHAIN_IDS_HERE])

    response = feed_item_set_service.mutate_feed_item_sets(
        customer_id=customer_id, operations=[feed_item_set_operation]
    )
    print(
        "Created a feed item set with resource name: "
        f"'{response.results[0].resource_name}'"
    )


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v8")

    parser = argparse.ArgumentParser(
        description="Creates a new feed item set for a specified feed."
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
    args = parser.parse_args()

    try:
        main(
            googleads_client, args.customer_id, args.feed_id,
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
