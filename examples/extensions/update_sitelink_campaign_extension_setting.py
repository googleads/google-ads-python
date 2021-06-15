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
"""Updates the sitelink campaign extension setting.

Replaces the extension feed items of the sitelink campaign extension setting
with the given feed item IDs. Note that this doesn't completely remove your
old extension feed items. See
https://developers.google.com/google-ads/api/docs/extensions/extension-settings/overview
for details.
"""


import argparse
import sys

from google.api_core import protobuf_helpers

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


# [START update_sitelink_campaign_extension_setting]
def main(client, customer_id, campaign_id, feed_item_ids):
    """The main method that creates all necessary entities for the example.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        campaign_id: the campaign ID.
        feed_item_ids: the IDs the feed items to replace.
    """
    campaign_extension_setting_service = client.get_service(
        "CampaignExtensionSettingService"
    )
    campaign_extension_setting_operation = client.get_type(
        "CampaignExtensionSettingOperation"
    )
    extension_feed_item_service = client.get_service("ExtensionFeedItemService")

    campaign_extension_setting = campaign_extension_setting_operation.update
    # Replace the current extension feed items with the given list
    campaign_extension_setting.extension_feed_items.extend(
        [
            extension_feed_item_service.extension_feed_item_path(
                customer_id, feed_item_id
            )
            for feed_item_id in feed_item_ids
        ]
    )

    extension_type_enum = client.get_type("ExtensionTypeEnum").ExtensionType
    resource_name = campaign_extension_setting_service.campaign_extension_setting_path(
        customer_id, campaign_id, extension_type_enum.SITELINK.name
    )
    campaign_extension_setting.resource_name = resource_name

    # Produce a field mask enumerating the changed fields
    client.copy_from(
        campaign_extension_setting_operation.update_mask,
        protobuf_helpers.field_mask(None, campaign_extension_setting._pb),
    )

    # Update the campaign extension settings
    response = campaign_extension_setting_service.mutate_campaign_extension_settings(
        customer_id=customer_id,
        operations=[campaign_extension_setting_operation],
    )
    print(
        "Updated campaign extension setting with resource name: "
        f'"{response.results[0].resource_name}".'
    )
    # [END update_sitelink_campaign_extension_setting]


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v8")

    parser = argparse.ArgumentParser(
        description=(
            "Updates the sitelink campaign extension setting to replace its "
            "extension feed items."
        )
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
        "-i", "--campaign_id", type=str, required=True, help="The campaign ID",
    )
    parser.add_argument(
        "-f",
        "--feed_item_ids",
        nargs="+",
        type=str,
        required=True,
        help="The IDs of the feed items to replace",
    )
    args = parser.parse_args()

    try:
        main(
            googleads_client,
            args.customer_id,
            args.campaign_id,
            args.feed_item_ids,
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
