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
"""Adds a geo target to an extension feed item for targeting."""


import argparse
import sys

from google.api_core import protobuf_helpers

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


# [START add_geo_target]
def main(client, customer_id, feed_item_id, geo_target_constant_id):
    """The main method that creates all necessary entities for the example.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        feed_item_id: the ID of an extension feed item.
        geo_target_constant_id: the geo target constant ID to add to the
            extension feed item.
    """
    extension_feed_item_service = client.get_service("ExtensionFeedItemService")

    extension_feed_item_operation = client.get_type(
        "ExtensionFeedItemOperation"
    )
    extension_feed_item = extension_feed_item_operation.update
    # Creates an extension feed item using the specified feed item ID and
    # geo target constant ID for targeting.
    extension_feed_item.resource_name = extension_feed_item_service.extension_feed_item_path(
        customer_id, feed_item_id
    )
    extension_feed_item.targeted_geo_target_constant = client.get_service(
        "GeoTargetConstantService"
    ).geo_target_constant_path(geo_target_constant_id)
    client.copy_from(
        extension_feed_item_operation.update_mask,
        protobuf_helpers.field_mask(None, extension_feed_item._pb),
    )

    response = extension_feed_item_service.mutate_extension_feed_items(
        customer_id=customer_id, operations=[extension_feed_item_operation]
    )
    print(
        "Updated extension feed item with resource name: "
        f"'{response.results[0].resource_name}'."
    )
    # [END add_geo_target]


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v8")

    parser = argparse.ArgumentParser(
        description="Adds a geo target to an extension feed item for targeting."
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
        "--feed_item_id",
        type=str,
        required=True,
        help="The ID of the extension feed item to add a geo target to.",
    )
    parser.add_argument(
        "-g",
        "--geo_target_constant_id",
        type=str,
        default="2840",  # country code for "US"
        help="A geo target constant ID. A list of available IDs can be "
        "referenced here: https://developers.google.com/google-ads/api/reference/data/geotargets",
    )

    args = parser.parse_args()

    try:
        main(
            googleads_client,
            args.customer_id,
            args.feed_item_id,
            args.geo_target_constant_id,
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
