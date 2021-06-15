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
"""Update the sitelink extension feed item with the specified link text."""


import argparse
import sys

from google.api_core import protobuf_helpers

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


# [START update_sitelink]
def main(client, customer_id, feed_item_id, sitelink_text):
    """The main method that creates all necessary entities for the example.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        feed_item_id: the ID of an extension feed item.
        sitelink_text: the updated sitelink text.
    """
    extension_feed_item_service = client.get_service("ExtensionFeedItemService")
    extension_feed_item_operation = client.get_type(
        "ExtensionFeedItemOperation"
    )
    extension_feed_item = extension_feed_item_operation.update
    # Update the extension feed item using the specified feed item ID
    extension_feed_item.resource_name = extension_feed_item_service.extension_feed_item_path(
        customer_id, feed_item_id
    )
    extension_feed_item.sitelink_feed_item.link_text = sitelink_text

    # Produce a field mask enumerating the changed fields
    client.copy_from(
        extension_feed_item_operation.update_mask,
        protobuf_helpers.field_mask(None, extension_feed_item._pb),
    )

    # Update the extension feed item
    response = extension_feed_item_service.mutate_extension_feed_items(
        customer_id=customer_id, operations=[extension_feed_item_operation]
    )
    print(
        "Updated extension feed item with resource name: "
        f'"{response.results[0].resource_name}".'
    )
    # [END update_sitelink]


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v8")

    parser = argparse.ArgumentParser(
        description="Update sitelink extension feed item with the specified "
        "link text."
    )
    # The following argument(s) should be provided to run the example.
    parser.add_argument(
        "-c",
        "--customer_id",
        type=str,
        required=True,
        help="The Google Ads customer ID",
    )
    parser.add_argument(
        "-f",
        "--feed_item_id",
        type=str,
        required=True,
        help="The ID of the extension feed item to update",
    )
    parser.add_argument(
        "-s",
        "--sitelink_text",
        type=str,
        required=True,
        help="The updated sitelink text",
    )
    args = parser.parse_args()

    try:
        main(
            googleads_client,
            args.customer_id,
            args.feed_item_id,
            args.sitelink_text,
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
