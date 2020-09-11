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

from google.ads.google_ads.client import GoogleAdsClient
from google.ads.google_ads.errors import GoogleAdsException


def main(client, customer_id, feed_item_id, geo_target_constant_id):
    """The main method that creates all necessary entities for the example.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        feed_item_id: the ID of an extension feed item.
        geo_target_constant_id: the geo target constant ID to add to the
            extension feed item.
    """
    extension_feed_item_service = client.get_service(
        "ExtensionFeedItemService", version="v5"
    )

    extension_feed_item_operation = client.get_type(
        "ExtensionFeedItemOperation", version="v5"
    )
    extension_feed_item = extension_feed_item_operation.update
    # Creates an extension feed item using the specified feed item ID and
    # geo target constant ID for targeting.
    extension_feed_item.resource_name = extension_feed_item_service.extension_feed_item_path(
        customer_id, feed_item_id
    )
    extension_feed_item.targeted_geo_target_constant.value = client.get_service(
        "GeoTargetConstantService", version="v5"
    ).geo_target_constant_path(geo_target_constant_id)
    fm = protobuf_helpers.field_mask(None, extension_feed_item)
    extension_feed_item_operation.update_mask.CopyFrom(fm)

    try:
        response = extension_feed_item_service.mutate_extension_feed_items(
            customer_id, [extension_feed_item_operation]
        )
        print(
            "Updated extension feed item with resource name: "
            f'"{response.results[0].resource_name}".'
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
        "referenced here: https://developers.google.com/adwords/api/docs/appendix/geotargeting.",
    )

    args = parser.parse_args()

    main(
        google_ads_client,
        args.customer_id,
        args.feed_item_id,
        args.geo_target_constant_id,
    )
