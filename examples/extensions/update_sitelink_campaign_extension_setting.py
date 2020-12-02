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
"""Updates the sitelink campaign extension setting to replace its extension feed
items. Note that this doesn't completely remove your old extension feed items.
See https://developers.google.com/google-ads/api/docs/extensions/extension-settings/overview
for details."""


import argparse
import sys

from google.api_core import protobuf_helpers
import google.api_core.path_template

from google.ads.google_ads.client import GoogleAdsClient
from google.ads.google_ads.errors import GoogleAdsException
from google.ads.google_ads.util import ResourceName


def main(client, customer_id, campaign_id, feed_item_ids):
    """The main method that creates all necessary entities for the example.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        campaign_id: the campaign ID.
        feed_item_ids: the IDs the feed items to replace.
    """
    campaign_extension_setting_service = client.get_service(
        "CampaignExtensionSettingService", version="v6"
    )
    campaign_extension_setting_operation = client.get_type(
        "CampaignExtensionSettingOperation", version="v6"
    )
    extension_feed_item_service = client.get_service(
        "ExtensionFeedItemService", version="v6"
    )

    extension_feed_items = map(
        lambda feed_item_id: extension_feed_item_service.extension_feed_item_path(
            customer_id, feed_item_id
        ),
        feed_item_ids,
    )
    campaign_extension_setting = campaign_extension_setting_operation.update
    extension_type_enum = client.get_type("ExtensionTypeEnum", version="v6")
    composite_id = ResourceName.format_composite(
        # the docs don't make it clear that this should reference the name of the extension type and not the enum
        # e.g. just extension_type_enum.ExtensionType.SITELINK won't work, but the string 'SITELINK' will
        campaign_id, extension_type_enum.ExtensionType.Name(
            extension_type_enum.ExtensionType.SITELINK
        )
    )
    resource_name = campaign_extension_setting_service.campaign_extension_setting_path(
        customer_id, composite_id
    )
    campaign_extension_setting.resource_name = resource_name
    campaign_extension_setting.extension_feed_items[:] = extension_feed_items

    # Produce a field mask enumerating the changed fields
    fm = protobuf_helpers.field_mask(None, campaign_extension_setting)
    campaign_extension_setting_operation.update_mask.CopyFrom(fm)

    try:
        response = campaign_extension_setting_service.mutate_campaign_extension_settings(
            customer_id, [campaign_extension_setting_operation]
        )
        print(
            "Updated campaign extension setting with resource name: "
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
        "--campaign_id", type=str, required=True, help="The campaign ID"
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

    main(
        google_ads_client,
        args.customer_id,
        args.campaign_id,
        args.feed_item_ids,
    )
