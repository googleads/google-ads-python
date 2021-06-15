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
"""Migrates a feed-based promotion extension to an asset-based extension.

The new asset-based extension will then be associated with the same campaigns
and ad groups as the original feed-based extension. Finally, the old feed-based
extension will be mutated so it no longer serves.
"""


import argparse
import sys
from uuid import uuid4

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


def main(client, customer_id, feed_item_id):
    """The main method that creates all necessary entities for the example.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        feed_item_id: an extension feed item ID.
    """
    extension_feed_item_service = client.get_service("ExtensionFeedItemService")
    resource_name = extension_feed_item_service.extension_feed_item_path(
        customer_id, feed_item_id
    )

    # Get the target extension feed item
    extension_feed_item = _get_extension_feed_item(
        client, customer_id, feed_item_id
    )

    # Get all campaign IDs associated with the extension feed item.
    campaign_ids = _get_targeted_campaign_ids(
        client, customer_id, resource_name
    )

    # Get all ad group IDs associated with the extension feed item.
    ad_group_ids = _get_targeted_ad_group_ids(
        client, customer_id, resource_name
    )

    # Create a new Promotion asset that matches the target extension feed item.
    promotion_asset_resource_name = _create_promotion_asset_from_feed(
        client, customer_id, extension_feed_item
    )

    # Associate the new Promotion asset with the same campaigns as the original.
    _associate_asset_with_campaigns(
        client, customer_id, promotion_asset_resource_name, campaign_ids
    )

    # Associate the new Promotion asset with the same ad groups as the original.
    _associate_asset_with_ad_groups(
        client, customer_id, promotion_asset_resource_name, ad_group_ids
    )


def _get_extension_feed_item(client, customer_id, feed_item_id):
    """Gets the requested Promotion-type extension feed item.

    Note that extension feed items pertain to feeds that were created by Google.
    Use FeedService to instead retrieve a user-created Feed.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        feed_item_id: an extension feed item ID.

    Returns:
        an ExtensionFeedItem instance.
    """
    ga_service = client.get_service("GoogleAdsService")

    query = f"""
      SELECT
        extension_feed_item.id,
        extension_feed_item.ad_schedules,
        extension_feed_item.device,
        extension_feed_item.status,
        extension_feed_item.start_date_time,
        extension_feed_item.end_date_time,
        extension_feed_item.targeted_campaign,
        extension_feed_item.targeted_ad_group,
        extension_feed_item.promotion_feed_item.discount_modifier,
        extension_feed_item.promotion_feed_item.final_mobile_urls,
        extension_feed_item.promotion_feed_item.final_url_suffix,
        extension_feed_item.promotion_feed_item.final_urls,
        extension_feed_item.promotion_feed_item.language_code,
        extension_feed_item.promotion_feed_item.money_amount_off.amount_micros,
        extension_feed_item.promotion_feed_item.money_amount_off.currency_code,
        extension_feed_item.promotion_feed_item.occasion,
        extension_feed_item.promotion_feed_item.orders_over_amount.amount_micros,
        extension_feed_item.promotion_feed_item.orders_over_amount.currency_code,
        extension_feed_item.promotion_feed_item.percent_off,
        extension_feed_item.promotion_feed_item.promotion_code,
        extension_feed_item.promotion_feed_item.promotion_end_date,
        extension_feed_item.promotion_feed_item.promotion_start_date,
        extension_feed_item.promotion_feed_item.promotion_target,
        extension_feed_item.promotion_feed_item.tracking_url_template
    FROM extension_feed_item
    WHERE
        extension_feed_item.extension_type = 'PROMOTION'
        AND extension_feed_item.id = {feed_item_id}
    LIMIT 1"""

    # Issue a search request to get the extension feed item contents.
    response = ga_service.search_stream(customer_id=customer_id, query=query)

    try:
        stream_response = next(response)
    except StopIteration:
        print(f"Error: No ExtensionFeedItem found with ID {feed_item_id}.")
        sys.exit(1)

    extension_feed_item = stream_response.results[0].extension_feed_item
    print(
        "Retrieved details for ad extension with ID: {extension_feed_item.id}."
    )

    # Create a query to retrieve any URL customer parameters attached to the
    # extension feed item.
    url_custom_params_query = f"""
      SELECT
        feed_item.url_custom_parameters
      FROM feed_item
      WHERE feed_item.id = {extension_feed_item.id}"""

    # Issue a search request to get any URL custom parameters.
    response = ga_service.search_stream(
        customer_id=customer_id, query=url_custom_params_query
    )

    try:
        url_stream_response = next(response)
    except StopIteration:
        print(f"Error: No FeedItems found with ID {feed_item_id}.")
        sys.exit(1)

    feed_item = url_stream_response.results[0].feed_item
    parameters = feed_item.url_custom_parameters
    num_params = len(parameters)
    print(f"Retrieved {num_params} attached URL custom parameters.")

    if num_params > 0:
        extension_feed_item.promotion_feed_item.url_custom_parameters.extend(
            parameters
        )

    return extension_feed_item


# [START migrate_promotion_feed_to_asset_1]
def _get_targeted_campaign_ids(client, customer_id, resource_name):
    """Retrieves all campaigns associated with the given FeedItem resource name.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        resource_name: an extension feed item resource name.

    Returns:
        a list of campaign IDs.
    """
    ga_service = client.get_service("GoogleAdsService")

    query = """
      SELECT
        campaign.id,
        campaign_extension_setting.extension_feed_items
      FROM campaign_extension_setting
      WHERE
        campaign_extension_setting.extension_type = 'PROMOTION'
        AND campaign.status != 'REMOVED'"""

    response = ga_service.search_stream(customer_id=customer_id, query=query)

    campaign_ids = []

    for batch in response:
        for row in batch.results:
            feed_items = row.campaign_extension_setting.extension_feed_items
            if resource_name in feed_items:
                print(f"Found matching campaign with ID: '{row.campaign.id}'")
                campaign_ids.append(row.campaign.id)

    return campaign_ids


# [END migrate_promotion_feed_to_asset_1]


def _get_targeted_ad_group_ids(client, customer_id, resource_name):
    """Retrieves all ad groups associated with the given FeedItem resource name.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        resource_name: an extension feed item resource name.

    Returns:
        a list of ad group IDs.
    """
    ga_service = client.get_service("GoogleAdsService")

    query = """
      SELECT
        ad_group.id,
        ad_group_extension_setting.extension_feed_items
      FROM ad_group_extension_setting
      WHERE
        ad_group_extension_setting.extension_type = 'PROMOTION'
        AND ad_group.status != 'REMOVED'"""

    response = ga_service.search_stream(customer_id=customer_id, query=query)

    ad_group_ids = []

    for batch in response:
        for row in batch.results:
            feed_items = row.ad_group_extension_setting.extension_feed_items
            if resource_name in feed_items:
                print(f"Found matching ad group with ID: '{row.ad_group.id}'")
                ad_group_ids.append(row.ad_group.id)

    return ad_group_ids


# [START migrate_promotion_feed_to_asset]
def _create_promotion_asset_from_feed(client, customer_id, extension_feed_item):
    """Retrieves all campaigns associated with the given FeedItem resource name.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        extension_feed_item: an extension feed item.

    Returns:
        the resource name of a newly created promotion asset.
    """
    asset_service = client.get_service("AssetService")
    promotion_feed_item = extension_feed_item.promotion_feed_item

    # Create an asset operation to start building the new promotion asset using
    # data from the given extension feed item.
    asset_operation = client.get_type("AssetOperation")
    asset = asset_operation.create
    asset.name = f"Migrated from feed item ID '{extension_feed_item.id}'"
    asset.tracking_url_template = promotion_feed_item.tracking_url_template
    asset.final_url_suffix = promotion_feed_item.final_url_suffix
    asset.final_urls.extend(promotion_feed_item.final_urls)
    asset.final_mobile_urls.extend(promotion_feed_item.final_mobile_urls)

    promotion_asset = asset.promotion_asset
    promotion_asset.promotion_target = promotion_feed_item.promotion_target
    promotion_asset.discount_modifier = promotion_feed_item.discount_modifier
    promotion_asset.redemption_start_date = (
        promotion_feed_item.promotion_start_date
    )
    promotion_asset.redemption_end_date = promotion_feed_item.promotion_end_date
    promotion_asset.occasion = promotion_feed_item.occasion
    promotion_asset.language_code = promotion_feed_item.language_code
    promotion_asset.ad_schedule_targets.extend(extension_feed_item.ad_schedules)

    # Either percent_off or money_amount_off must be set.
    if promotion_feed_item.percent_off > 0:
        # Adjust the percent off scale after copying. Extension feed items
        # interpret 1,000,000 as 1% and assets interpret 1,000,000 as 100% so
        # to migrate the correct discount value we must divide it by 100.
        promotion_asset.percent_off = int(promotion_feed_item.percent_off / 100)
    else:
        # If percent_off is not set then copy money_amount_off. This field is
        # an instance of Money in both cases, so setting the field with
        # copy_from is possible. Using regular assignment is also valid here.
        client.copy_from(
            promotion_asset.money_amount_off,
            promotion_feed_item.money_amount_off,
        )

    # Check if promotion_code field is set
    if promotion_feed_item.promotion_code:
        promotion_asset.promotion_code = promotion_feed_item.promotion_code
    else:
        # If promotion_code is not set then copy orders_over_amount. This field
        # is an instance of Money in both cases, so setting the field with
        # copy_from is possible. Using regular assignment is also valid here.
        client.copy_from(
            promotion_asset.orders_over_amount,
            promotion_feed_item.orders_over_amount,
        )

    # Set the start and end dates if set in the existing extension.
    if promotion_feed_item.promotion_start_date:
        promotion_asset.start_date = promotion_feed_item.promotion_start_date

    if promotion_feed_item.promotion_end_date:
        promotion_asset.end_date = promotion_feed_item.promotion_end_date

    response = asset_service.mutate_assets(
        customer_id=customer_id, operations=[asset_operation]
    )
    resource_name = response.results[0].resource_name
    print(f"Created promotion asset with resource name: '{resource_name}'")

    return resource_name


# [END migrate_promotion_feed_to_asset]


# [START migrate_promotion_feed_to_asset_2]
def _associate_asset_with_campaigns(
    client, customer_id, promotion_asset_resource_name, campaign_ids
):
    """Associates the specified promotion asset with the specified campaigns.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        promotion_asset_resource_name: the resource name for a promotion asset.
        campaign_ids: a list of campaign IDs.
    """
    if len(campaign_ids) == 0:
        print(f"Asset was not associated with any campaigns.")
        return

    campaign_service = client.get_service("CampaignService")
    campaign_asset_service = client.get_service("CampaignAssetService")

    operations = []

    for campaign_id in campaign_ids:
        operation = client.get_type("CampaignAssetOperation")
        campaign_asset = operation.create
        campaign_asset.asset = promotion_asset_resource_name
        campaign_asset.field_type = client.enums.AssetFieldTypeEnum.PROMOTION
        campaign_asset.campaign = campaign_service.campaign_path(
            customer_id, campaign_id
        )
        operations.append(operation)

    response = campaign_asset_service.mutate_campaign_assets(
        customer_id=customer_id, operations=operations
    )

    for result in response.results:
        print(
            "Created campaign asset with resource name: "
            f"'{result.resource_name}'"
        )


# [END migrate_promotion_feed_to_asset_2]


def _associate_asset_with_ad_groups(
    client, customer_id, promotion_asset_resource_name, ad_group_ids
):
    """Associates the specified promotion asset with the specified campaigns.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        promotion_asset_resource_name: the resource name for a promotion asset.
        ad_groups_ids: a list of ad group IDs.
    """
    if len(ad_group_ids) == 0:
        print(f"Asset was not associated with any ad groups.")
        return

    ad_group_service = client.get_service("AdGroupService")
    ad_group_asset_service = client.get_service("AdGroupAssetService")

    operations = []

    for ad_group_id in ad_group_ids:
        operation = client.get_type("AdGroupAssetOperation")
        ad_group_asset = operation.create
        ad_group_asset.asset = promotion_asset_resource_name
        ad_group_asset.field_type = client.enums.AssetFieldTypeEnum.PROMOTION
        ad_group_asset.ad_group = ad_group_service.ad_group_path(
            customer_id, ad_group_id
        )
        operations.append(operation)

    response = ad_group_asset_service.mutate_ad_group_assets(
        customer_id=customer_id, operations=operations
    )

    for result in response.results:
        print(
            "Created ad group asset with resource name: "
            f"'{result.resource_name}'"
        )


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v8")

    parser = argparse.ArgumentParser(
        description="Migrates a feed-based promotion extension to an "
        "asset-based extension."
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
        help="The ID of the ExtensionFeedItem to migrate.",
    )
    args = parser.parse_args()

    try:
        main(googleads_client, args.customer_id, args.feed_item_id)
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
