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
"""This example adds a hotel callout extension to a specific account.

It also adds the hotel callout extension to a campaign and an ad group under
the account.
"""


import argparse
import sys


from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


def main(
    client, customer_id, campaign_id, ad_group_id, callout_text, language_code
):
    """The main method that creates all necessary entities for the example.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        campaign_id: a str of a campaign ID.
        ad_group_id: a str of an ad_group ID.
        callout_text: a str of text for a hotel callout feed item.
        language_code: the language of the hotel callout feed item text.
    """
    # Creates an extension feed item as hotel callout.
    extension_feed_item_resource_name = _add_extension_feed_item(
        client, customer_id, callout_text, language_code
    )
    # Adds the extension feed item to the account.
    _add_extension_to_account(
        client, customer_id, extension_feed_item_resource_name
    )
    # Adds the extension feed item to the campaign.
    _add_extension_to_campaign(
        client, customer_id, campaign_id, extension_feed_item_resource_name
    )
    # Adds the extension feed item to the ad group.
    _add_extension_to_ad_group(
        client, customer_id, ad_group_id, extension_feed_item_resource_name
    )


def _add_extension_feed_item(client, customer_id, callout_text, language_code):
    """Creates a new extension feed item for the callout extension.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        callout_text: a str of text for a hotel callout feed item.
        language_code: the language of the hotel callout feed item text.

    Returns:
        a str resource name of the newly created extension feed item.
    """
    extension_feed_item_operation = client.get_type(
        "ExtensionFeedItemOperation"
    )
    extension_feed_item = extension_feed_item_operation.create
    extension_feed_item.hotel_callout_feed_item.text = callout_text
    extension_feed_item.hotel_callout_feed_item.language_code = language_code

    extension_feed_item_service = client.get_service("ExtensionFeedItemService")
    response = extension_feed_item_service.mutate_extension_feed_items(
        customer_id=customer_id, operations=[extension_feed_item_operation]
    )
    resource_name = response.results[0].resource_name
    print(
        f"Created an extension feed item with resource name: "
        "'{resource_name}'"
    )
    return resource_name


def _add_extension_to_account(
    client, customer_id, extension_feed_item_resource_name
):
    """Adds the extension feed item to the customer account.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        extension_feed_item_resource_name: a str resource name of an extension
            feed item.
    """
    customer_extension_setting_operation = client.get_type(
        "CustomerExtensionSettingOperation"
    )
    customer_extension_setting = customer_extension_setting_operation.create
    customer_extension_setting.extension_type = client.get_type(
        "ExtensionTypeEnum"
    ).ExtensionType.HOTEL_CALLOUT
    customer_extension_setting.extension_feed_items.append(
        extension_feed_item_resource_name
    )

    customer_extension_setting_service = client.get_service(
        "CustomerExtensionSettingService"
    )
    response = customer_extension_setting_service.mutate_customer_extension_settings(
        customer_id=customer_id,
        operations=[customer_extension_setting_operation],
    )
    print(
        "Created a customer extension setting with resource name: "
        f"'{response.results[0].resource_name}'"
    )


def _add_extension_to_campaign(
    client, customer_id, campaign_id, extension_feed_item_resource_name
):
    """Adds the extension feed item to the specified campaign.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        campaign_id: a str of a campaign ID.
        extension_feed_item_resource_name: a str resource name of an extension
            feed item.
    """
    campaign_extension_setting_operation = client.get_type(
        "CampaignExtensionSettingOperation"
    )
    campaign_extension_setting = campaign_extension_setting_operation.create
    campaign_extension_setting.campaign = client.get_service(
        "CampaignService"
    ).campaign_path(customer_id, campaign_id)
    campaign_extension_setting.extension_type = client.get_type(
        "ExtensionTypeEnum"
    ).ExtensionType.HOTEL_CALLOUT
    campaign_extension_setting.extension_feed_items.append(
        extension_feed_item_resource_name
    )

    campaign_extension_setting_service = client.get_service(
        "CampaignExtensionSettingService"
    )
    response = campaign_extension_setting_service.mutate_campaign_extension_settings(
        customer_id=customer_id,
        operations=[campaign_extension_setting_operation],
    )
    print(
        "Created a campaign extension setting with resource name: "
        f"'{response.results[0].resource_name}'"
    )


def _add_extension_to_ad_group(
    client, customer_id, ad_group_id, extension_feed_item_resource_name
):
    """Adds the extension feed item to the specified ad group.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        ad_group_id: a str of an ad_group ID.
        extension_feed_item_resource_name: a str resource name of an extension
            feed item.
    """
    ad_group_extension_setting_operation = client.get_type(
        "AdGroupExtensionSettingOperation"
    )
    ad_group_extension_setting = ad_group_extension_setting_operation.create
    ad_group_extension_setting.ad_group = client.get_service(
        "AdGroupService"
    ).ad_group_path(customer_id, ad_group_id)
    ad_group_extension_setting.extension_type = client.get_type(
        "ExtensionTypeEnum"
    ).ExtensionType.HOTEL_CALLOUT
    ad_group_extension_setting.extension_feed_items.append(
        extension_feed_item_resource_name
    )

    ad_group_extension_setting_service = client.get_service(
        "AdGroupExtensionSettingService"
    )
    response = ad_group_extension_setting_service.mutate_ad_group_extension_settings(
        customer_id=customer_id,
        operations=[ad_group_extension_setting_operation],
    )
    print(
        "Created a ad_group extension setting with resource name: "
        f"'{response.results[0].resource_name}'"
    )


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v8")

    parser = argparse.ArgumentParser(
        description="Adds a hotel callout extension to the given account."
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
        "-i", "--campaign_id", type=str, required=True, help="The campaign ID.",
    )
    parser.add_argument(
        "-a",
        "--ad_group_id",
        type=str,
        required=False,
        help="The ad group ID. ",
    )
    parser.add_argument(
        "-t",
        "--callout_text",
        type=str,
        required=True,
        help=(
            "The text of the hotel callout feed item. This text has a maximum "
            "length of 25 characters."
        ),
    )
    parser.add_argument(
        "-l",
        "--language_code",
        type=str,
        required=True,
        help=(
            "The language of the text on the hotel callout feed item. For a "
            "list of supported languages see: "
            "https://developers.google.com/hotels/hotel-ads/api-reference/language-codes."
        ),
    )
    args = parser.parse_args()

    try:
        main(
            googleads_client,
            args.customer_id,
            args.campaign_id,
            args.ad_group_id,
            args.callout_text,
            args.language_code,
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
