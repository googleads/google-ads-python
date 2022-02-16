#!/usr/bin/env python
# Copyright 2021 Google LLC
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
"""This example shows how to create a Performance Max retail campaign.

This will be created for "All products".

For more information about Performance Max retail campaigns, see
https://developers.google.com/google-ads/api/docs/performance-max/retail

Prerequisites:
- You need to have access to a Merchant Center account. You can find
  instructions to create a Merchant Center account here:
  https://support.google.com/merchants/answer/188924.
  This account must be linked to your Google Ads account. The integration
  instructions can be found at:
  https://developers.google.com/google-ads/api/docs/shopping-ads/merchant-center
- You need your Google Ads account to track conversions. The different ways
  to track conversions can be found here:
  https://support.google.com/google-ads/answer/1722054.
- You must have at least one conversion action in the account. For
  more about conversion actions, see
  https://developers.google.com/google-ads/api/docs/conversions/overview#conversion_actions
"""


import argparse
from datetime import datetime, timedelta
import sys
from uuid import uuid4

from google.api_core import protobuf_helpers
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.ads.googleads.util import convert_snake_case_to_upper_case

import requests


# We specify temporary IDs that are specific to a single mutate request.
# Temporary IDs are always negative and unique within one mutate request.
#
# See https://developers.google.com/google-ads/api/docs/mutating/best-practices
# for further details.
#
# These temporary IDs are fixed because they are used in multiple places.
_BUDGET_TEMPORARY_ID = "-1"
_PERFORMANCE_MAX_CAMPAIGN_TEMPORARY_ID = "-2"
_ASSET_GROUP_TEMPORARY_ID = "-3"

# There are also entities that will be created in the same request but do not
# need to be fixed temporary IDs because they are referenced only once.
next_temp_id = int(_ASSET_GROUP_TEMPORARY_ID) - 1


# [START add_performance_max_retail_campaign]
def main(
    client,
    customer_id,
    merchant_center_account_id,
    sales_country,
    final_url,
):
    """The main method that creates all necessary entities for the example.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        merchant_center_account_id: The Merchant Center account ID.
        sales_country: sales country of products to include in the campaign.
        final_url: the final URL.
    """
    # [START add_performance_max_retail_campaign_1]
    googleads_service = client.get_service("GoogleAdsService")

    # This campaign will override the customer conversion goals.
    # Retrieve the current list of customer conversion goals.
    customer_conversion_goals = _get_customer_conversion_goals(
        client, customer_id
    )

    # Performance Max campaigns require that repeated assets such as headlines
    # and descriptions be created before the campaign.
    # For the list of required assets for a Performance Max campaign, see
    # https://developers.google.com/google-ads/api/docs/performance-max/assets
    #
    # Create the headlines.
    headline_asset_resource_names = _create_multiple_text_assets(
        client,
        customer_id,
        [
            "Travel",
            "Travel Reviews",
            "Book travel",
        ],
    )
    # Create the descriptions.
    description_asset_resource_names = _create_multiple_text_assets(
        client,
        customer_id,
        [
            "Take to the air!",
            "Fly to the sky!",
        ],
    )

    # The below methods create and return MutateOperations that we later
    # provide to the GoogleAdsService.Mutate method in order to create the
    # entities in a single request. Since the entities for a Performance Max
    # campaign are closely tied to one-another, it's considered a best practice
    # to create them in a single Mutate request so they all complete
    # successfully or fail entirely, leaving no orphaned entities. See:
    # https://developers.google.com/google-ads/api/docs/mutating/overview
    campaign_budget_operation = _create_campaign_budget_operation(
        client,
        customer_id,
    )
    performance_max_campaign_operation = (
        _create_performance_max_campaign_operation(
            client,
            customer_id,
            merchant_center_account_id,
            sales_country,
        )
    )
    campaign_criterion_operations = _create_campaign_criterion_operations(
        client,
        customer_id,
    )
    asset_group_operations = _create_asset_group_operation(
        client,
        customer_id,
        final_url,
        headline_asset_resource_names,
        description_asset_resource_names,
    )
    conversion_goal_operations = _create_conversion_goal_operations(
        client,
        customer_id,
        customer_conversion_goals,
    )

    # Send the operations in a single Mutate request.
    response = googleads_service.mutate(
        customer_id=customer_id,
        mutate_operations=[
            # It's important to create these entities in this order because
            # they depend on each other.
            campaign_budget_operation,
            performance_max_campaign_operation,
            # Expand the list of multiple operations into the list of
            # other mutate operations.
            *campaign_criterion_operations,
            *asset_group_operations,
            *conversion_goal_operations,
        ],
    )
    _print_response_details(response)
    # [END add_performance_max_retail_campaign_1]


# [START add_performance_max_retail_campaign_2]
def _create_campaign_budget_operation(
    client,
    customer_id,
):
    """Creates a MutateOperation that creates a new CampaignBudget.

    A temporary ID will be assigned to this campaign budget so that it can be
    referenced by other objects being created in the same Mutate request.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.

    Returns:
        a MutateOperation that creates a CampaignBudget.
    """
    mutate_operation = client.get_type("MutateOperation")
    campaign_budget_operation = mutate_operation.campaign_budget_operation
    campaign_budget = campaign_budget_operation.create
    campaign_budget.name = f"Performance Max retail campaign budget #{uuid4()}"
    # The budget period already defaults to DAILY.
    campaign_budget.amount_micros = 50000000
    campaign_budget.delivery_method = (
        client.enums.BudgetDeliveryMethodEnum.STANDARD
    )
    # A Performance Max campaign cannot use a shared campaign budget.
    campaign_budget.explicitly_shared = False

    # Set a temporary ID in the budget's resource name so it can be referenced
    # by the campaign in later steps.
    campaign_budget.resource_name = client.get_service(
        "CampaignBudgetService"
    ).campaign_budget_path(customer_id, _BUDGET_TEMPORARY_ID)

    return mutate_operation
    # [END add_performance_max_retail_campaign_2]


# [START add_performance_max_retail_campaign_3]
def _create_performance_max_campaign_operation(
    client,
    customer_id,
    merchant_center_account_id,
    sales_country,
):
    """Creates a MutateOperation that creates a new Performance Max campaign.

    A temporary ID will be assigned to this campaign so that it can
    be referenced by other objects being created in the same Mutate request.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        merchant_center_account_id: The Merchant Center account ID.
        sales_country: Sales country of products to include in the campaign.

    Returns:
        a MutateOperation that creates a campaign.
    """
    mutate_operation = client.get_type("MutateOperation")
    campaign = mutate_operation.campaign_operation.create
    campaign.name = f"Performance Max retail campaign #{uuid4()}"
    # Set the campaign status as PAUSED. The campaign is the only entity in
    # the mutate request that should have its status set.
    campaign.status = client.enums.CampaignStatusEnum.PAUSED
    # All Performance Max campaigns have an advertising_channel_type of
    # PERFORMANCE_MAX. The advertising_channel_sub_type should not be set.
    campaign.advertising_channel_type = (
        client.enums.AdvertisingChannelTypeEnum.PERFORMANCE_MAX
    )
    # Bidding strategy must be set directly on the campaign.
    # Setting a portfolio bidding strategy by resource name is not supported.
    # Max Conversion and Max Conversion Value are the only strategies supported
    # for Performance Max campaigns.
    # An optional ROAS (Return on Advertising Spend) can be set for
    # maximize_conversion_value. The ROAS value must be specified as a ratio in
    # the API. It is calculated by dividing "total value" by "total spend".
    # For more information on Max Conversion Value, see the support article:
    # http://support.google.com/google-ads/answer/7684216.
    # A target_roas of 3.5 corresponds to a 350% return on ad spend.
    campaign.bidding_strategy_type = (
        client.enums.BiddingStrategyTypeEnum.MAXIMIZE_CONVERSION_VALUE
    )
    campaign.maximize_conversion_value.target_roas = 3.5

    # Set the shopping settings.
    campaign.shopping_setting.merchant_id = merchant_center_account_id
    campaign.shopping_setting.sales_country = sales_country

    # Set the Final URL expansion opt out. This flag is specific to
    # Performance Max campaigns. If opted out (True), only the final URLs in
    # the asset group or URLs specified in the advertiser's Google Merchant
    # Center or business data feeds are targeted.
    # If opted in (False), the entire domain will be targeted. For best
    # results, set this value to false to opt in and allow URL expansions. You
    # can optionally add exclusions to limit traffic to parts of your website.
    campaign.url_expansion_opt_out = False

    # Assign the resource name with a temporary ID.
    campaign_service = client.get_service("CampaignService")
    campaign.resource_name = campaign_service.campaign_path(
        customer_id, _PERFORMANCE_MAX_CAMPAIGN_TEMPORARY_ID
    )
    # Set the budget using the given budget resource name.
    campaign.campaign_budget = campaign_service.campaign_budget_path(
        customer_id, _BUDGET_TEMPORARY_ID
    )

    # Optional fields
    campaign.start_date = (datetime.now() + timedelta(1)).strftime("%Y%m%d")
    campaign.end_date = (datetime.now() + timedelta(365)).strftime("%Y%m%d")

    return mutate_operation
    # [END add_performance_max_retail_campaign_3]


# [START add_performance_max_retail_campaign_4]
def _create_campaign_criterion_operations(
    client,
    customer_id,
):
    """Creates a list of MutateOperations that create new campaign criteria.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.

    Returns:
        a list of MutateOperations that create new campaign criteria.
    """
    campaign_service = client.get_service("CampaignService")
    geo_target_constant_service = client.get_service("GeoTargetConstantService")
    googleads_service = client.get_service("GoogleAdsService")

    operations = []
    # Set the LOCATION campaign criteria.
    # Target all of New York City except Brooklyn.
    # Location IDs are listed here:
    # https://developers.google.com/google-ads/api/reference/data/geotargets
    # and they can also be retrieved using the GeoTargetConstantService as shown
    # here: https://developers.google.com/google-ads/api/docs/targeting/location-targeting
    #
    # We will add one positive location target for New York City (ID=1023191)
    # and one negative location target for Brooklyn (ID=1022762).
    # First, add the positive (negative = False) for New York City.
    mutate_operation = client.get_type("MutateOperation")
    campaign_criterion = mutate_operation.campaign_criterion_operation.create
    campaign_criterion.campaign = campaign_service.campaign_path(
        customer_id, _PERFORMANCE_MAX_CAMPAIGN_TEMPORARY_ID
    )
    campaign_criterion.location.geo_target_constant = (
        geo_target_constant_service.geo_target_constant_path("1023191")
    )
    campaign_criterion.negative = False
    operations.append(mutate_operation)

    # Next add the negative target for Brooklyn.
    mutate_operation = client.get_type("MutateOperation")
    campaign_criterion = mutate_operation.campaign_criterion_operation.create
    campaign_criterion.campaign = campaign_service.campaign_path(
        customer_id, _PERFORMANCE_MAX_CAMPAIGN_TEMPORARY_ID
    )
    campaign_criterion.location.geo_target_constant = (
        geo_target_constant_service.geo_target_constant_path("1022762")
    )
    campaign_criterion.negative = True
    operations.append(mutate_operation)

    # Set the LANGUAGE campaign criterion.
    mutate_operation = client.get_type("MutateOperation")
    campaign_criterion = mutate_operation.campaign_criterion_operation.create
    campaign_criterion.campaign = campaign_service.campaign_path(
        customer_id, _PERFORMANCE_MAX_CAMPAIGN_TEMPORARY_ID
    )
    # Set the language.
    # For a list of all language codes, see:
    # https://developers.google.com/google-ads/api/reference/data/codes-formats#expandable-7
    campaign_criterion.language.language_constant = (
        googleads_service.language_constant_path("1000")  # English
    )
    operations.append(mutate_operation)

    return operations
    # [END add_performance_max_retail_campaign_4]


# [START add_performance_max_retail_campaign_5]
def _create_multiple_text_assets(client, customer_id, texts):
    """Creates multiple text assets and returns the list of resource names.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        texts: a list of strings, each of which will be used to create a text
          asset.

    Returns:
        asset_resource_names: a list of asset resource names.
    """
    # Here again we use the GoogleAdService to create multiple text
    # assets in a single request.
    googleads_service = client.get_service("GoogleAdsService")

    operations = []
    for text in texts:
        mutate_operation = client.get_type("MutateOperation")
        asset = mutate_operation.asset_operation.create
        asset.text_asset.text = text
        operations.append(mutate_operation)

    # Send the operations in a single Mutate request.
    response = googleads_service.mutate(
        customer_id=customer_id,
        mutate_operations=operations,
    )
    asset_resource_names = []
    for result in response.mutate_operation_responses:
        if result._pb.HasField("asset_result"):
            asset_resource_names.append(result.asset_result.resource_name)
    _print_response_details(response)
    return asset_resource_names
    # [END add_performance_max_retail_campaign_5]


# [START add_performance_max_retail_campaign_6]
def _create_asset_group_operation(
    client,
    customer_id,
    final_url,
    headline_asset_resource_names,
    description_asset_resource_names,
):
    """Creates a list of MutateOperations that create a new asset_group.

    A temporary ID will be assigned to this asset group so that it can
    be referenced by other objects being created in the same Mutate request.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        final_url: the final URL.
        headline_asset_resource_names: a list of headline resource names.
        description_asset_resource_names: a list of description resource names.

    Returns:
        MutateOperations that create a new asset group and related assets.
    """
    asset_group_service = client.get_service("AssetGroupService")
    campaign_service = client.get_service("CampaignService")

    operations = []

    # Create the AssetGroup.
    mutate_operation = client.get_type("MutateOperation")
    asset_group = mutate_operation.asset_group_operation.create
    asset_group.name = f"Performance Max retail asset group #{uuid4()}"
    asset_group.campaign = campaign_service.campaign_path(
        customer_id, _PERFORMANCE_MAX_CAMPAIGN_TEMPORARY_ID
    )
    asset_group.final_urls.append(final_url)
    asset_group.final_mobile_urls.append(final_url)
    asset_group.status = client.enums.AssetGroupStatusEnum.PAUSED
    asset_group.resource_name = asset_group_service.asset_group_path(
        customer_id,
        _ASSET_GROUP_TEMPORARY_ID,
    )
    operations.append(mutate_operation)

    # For the list of required assets for a Performance Max campaign, see
    # https://developers.google.com/google-ads/api/docs/performance-max/assets

    # An AssetGroup is linked to an Asset by creating a new AssetGroupAsset
    # and providing:
    #   the resource name of the AssetGroup
    #   the resource name of the Asset
    #   the field_type of the Asset in this AssetGroup.
    #
    # To learn more about AssetGroups, see
    # https://developers.google.com/google-ads/api/docs/performance-max/asset-groups

    # Link the previously created multiple text assets.

    # Link the headline assets.
    for resource_name in headline_asset_resource_names:
        mutate_operation = client.get_type("MutateOperation")
        asset_group_asset = mutate_operation.asset_group_asset_operation.create
        asset_group_asset.field_type = client.enums.AssetFieldTypeEnum.HEADLINE
        asset_group_asset.asset_group = asset_group_service.asset_group_path(
            customer_id,
            _ASSET_GROUP_TEMPORARY_ID,
        )
        asset_group_asset.asset = resource_name
        operations.append(mutate_operation)

    #  Link the description assets.
    for resource_name in description_asset_resource_names:
        mutate_operation = client.get_type("MutateOperation")
        asset_group_asset = mutate_operation.asset_group_asset_operation.create
        asset_group_asset.field_type = (
            client.enums.AssetFieldTypeEnum.DESCRIPTION
        )
        asset_group_asset.asset_group = asset_group_service.asset_group_path(
            customer_id,
            _ASSET_GROUP_TEMPORARY_ID,
        )
        asset_group_asset.asset = resource_name
        operations.append(mutate_operation)

    # Create and link the long headline text asset.
    mutate_operations = _create_and_link_text_asset(
        client,
        customer_id,
        "Travel the World",
        client.enums.AssetFieldTypeEnum.LONG_HEADLINE,
    )
    operations.extend(mutate_operations)

    # Create and link the business name text asset.
    mutate_operations = _create_and_link_text_asset(
        client,
        customer_id,
        "Interplanetary Cruises",
        client.enums.AssetFieldTypeEnum.BUSINESS_NAME,
    )
    operations.extend(mutate_operations)

    # Create and link the image assets.

    # Create and link the Logo Asset.
    mutate_operations = _create_and_link_image_asset(
        client,
        customer_id,
        "https://gaagl.page.link/bjYi",
        client.enums.AssetFieldTypeEnum.LOGO,
        "Logo Image",
    )
    operations.extend(mutate_operations)

    # Create and link the Marketing Image Asset.
    mutate_operations = _create_and_link_image_asset(
        client,
        customer_id,
        "https://gaagl.page.link/Eit5",
        client.enums.AssetFieldTypeEnum.MARKETING_IMAGE,
        "Marketing Image",
    )
    operations.extend(mutate_operations)

    # Create and link the Square Marketing Image Asset.
    mutate_operations = _create_and_link_image_asset(
        client,
        customer_id,
        "https://gaagl.page.link/bjYi",
        client.enums.AssetFieldTypeEnum.SQUARE_MARKETING_IMAGE,
        "Square Marketing Image",
    )
    operations.extend(mutate_operations)
    return operations
    # [END add_performance_max_retail_campaign_6]


# [START add_performance_max_retail_campaign_7]
def _create_and_link_text_asset(client, customer_id, text, field_type):
    """Creates a list of MutateOperations that create a new linked text asset.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        text: the text of the asset to be created.
        field_type: the field_type of the new asset in the AssetGroupAsset.

    Returns:
        MutateOperations that create a new linked text asset.
    """
    global next_temp_id
    operations = []
    asset_service = client.get_service("AssetService")
    asset_group_service = client.get_service("AssetGroupService")

    # Create the Text Asset.
    mutate_operation = client.get_type("MutateOperation")
    asset = mutate_operation.asset_operation.create
    asset.resource_name = asset_service.asset_path(customer_id, next_temp_id)
    asset.text_asset.text = text
    operations.append(mutate_operation)

    # Create an AssetGroupAsset to link the Asset to the AssetGroup.
    mutate_operation = client.get_type("MutateOperation")
    asset_group_asset = mutate_operation.asset_group_asset_operation.create
    asset_group_asset.field_type = field_type
    asset_group_asset.asset_group = asset_group_service.asset_group_path(
        customer_id,
        _ASSET_GROUP_TEMPORARY_ID,
    )
    asset_group_asset.asset = asset_service.asset_path(
        customer_id, next_temp_id
    )
    operations.append(mutate_operation)

    next_temp_id -= 1
    return operations
    # [END add_performance_max_retail_campaign_7]


# [START add_performance_max_retail_campaign_8]
def _create_and_link_image_asset(client, customer_id, url, field_type, asset_name):
    """Creates a list of MutateOperations that create a new linked image asset.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        url: the url of the image to be retrieved and put into an asset.
        field_type: the field_type of the new asset in the AssetGroupAsset.
        asset_name: the asset name.

    Returns:
        MutateOperations that create a new linked image asset.
    """
    global next_temp_id
    operations = []
    asset_service = client.get_service("AssetService")
    asset_group_service = client.get_service("AssetGroupService")

    # Create the Image Asset.
    mutate_operation = client.get_type("MutateOperation")
    asset = mutate_operation.asset_operation.create
    asset.resource_name = asset_service.asset_path(customer_id, next_temp_id)
    asset.type_ = client.enums.AssetTypeEnum.IMAGE
    # Provide a unique friendly name to identify your asset.
    # When there is an existing image asset with the same content but a different
    # name, the new name will be dropped silently.
    asset.name = asset_name
    asset.image_asset.data = _get_image_bytes(url)
    operations.append(mutate_operation)

    # Create an AssetGroupAsset to link the Asset to the AssetGroup.
    mutate_operation = client.get_type("MutateOperation")
    asset_group_asset = mutate_operation.asset_group_asset_operation.create
    asset_group_asset.field_type = field_type
    asset_group_asset.asset_group = asset_group_service.asset_group_path(
        customer_id,
        _ASSET_GROUP_TEMPORARY_ID,
    )
    asset_group_asset.asset = asset_service.asset_path(
        customer_id, next_temp_id
    )
    operations.append(mutate_operation)

    next_temp_id -= 1
    return operations
    # [END add_performance_max_retail_campaign_8]


# [START add_performance_max_retail_campaign_9]
def _get_customer_conversion_goals(client, customer_id):
    """Retrieves the list of customer conversion goals.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.

    Returns:
        a list of dicts containing the category and origin of customer
        conversion goals.
    """
    ga_service = client.get_service("GoogleAdsService")
    customer_conversion_goals = []
    query = """
            SELECT
              customer_conversion_goal.category,
              customer_conversion_goal.origin
            FROM customer_conversion_goal
            """
    # The number of conversion goals is typically less than 50 so we use
    # GoogleAdsService.search instead of search_stream.
    search_request = client.get_type("SearchGoogleAdsRequest")
    search_request.customer_id = customer_id
    search_request.query = query
    search_request.page_size = 10000
    results = ga_service.search(request=search_request)

    # Iterate over the results and build the list of conversion goals.
    for row in results:
        customer_conversion_goals.append(
            {
                "category": row.customer_conversion_goal.category,
                "origin": row.customer_conversion_goal.origin,
            }
        )
    return customer_conversion_goals


def _create_conversion_goal_operations(
    client,
    customer_id,
    customer_conversion_goals,
):
    """Creates a list of MutateOperations that override customer conversion goals.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        customer_conversion_goals: the list of customer conversion goals that
          will be overridden.

    Returns:
        MutateOperations that update campaign conversion goals.
    """
    campaign_conversion_goal_service = client.get_service(
        "CampaignConversionGoalService"
    )
    operations = []

    # To override the customer conversion goals, we will change the
    # biddability of each of the customer conversion goals so that only
    # the desired conversion goal is biddable in this campaign.
    for customer_conversion_goal in customer_conversion_goals:
        mutate_operation = client.get_type("MutateOperation")
        campaign_conversion_goal = (
            mutate_operation.campaign_conversion_goal_operation.update
        )

        campaign_conversion_goal.resource_name = (
            campaign_conversion_goal_service.campaign_conversion_goal_path(
                customer_id,
                _PERFORMANCE_MAX_CAMPAIGN_TEMPORARY_ID,
                customer_conversion_goal["category"].name,
                customer_conversion_goal["origin"].name,
            )
        )
        # Change the biddability for the campaign conversion goal.
        # Set biddability to True for the desired (category, origin).
        # Set biddability to False for all other conversion goals.
        # Note:
        #  1- It is assumed that this Conversion Action
        #     (category=PURCHASE, origin=WEBSITE) exists in this account.
        #  2- More than one goal can be biddable if desired. This example
        #     shows only one.
        if (
            customer_conversion_goal["category"]
            == client.enums.ConversionActionCategoryEnum.PURCHASE
            and customer_conversion_goal["origin"]
            == client.enums.ConversionOriginEnum.WEBSITE
        ):
            biddable = True
        else:
            biddable = False
        campaign_conversion_goal.biddable = biddable
        field_mask = protobuf_helpers.field_mask(
            None, campaign_conversion_goal._pb
        )
        client.copy_from(
            mutate_operation.campaign_conversion_goal_operation.update_mask,
            field_mask,
        )
        operations.append(mutate_operation)

    return operations
    # [END add_performance_max_retail_campaign_9]


def _get_image_bytes(url):
    """Loads image data from a URL.

    Args:
        url: a URL str.

    Returns:
        Images bytes loaded from the given URL.
    """
    response = requests.get(url)
    return response.content


def _print_response_details(response):
    """Prints the details of a MutateGoogleAdsResponse.

    Parses the "response" oneof field name and uses it to extract the new
    entity's name and resource name.

    Args:
        response: a MutateGoogleAdsResponse object.
    """
    # Parse the Mutate response to print details about the entities that
    # were created by the request.
    suffix = "_result"
    for result in response.mutate_operation_responses:
        for field_descriptor, value in result._pb.ListFields():
            if field_descriptor.name.endswith(suffix):
                name = field_descriptor.name[: -len(suffix)]
            else:
                name = field_descriptor.name
            print(
                f"Created a(n) {convert_snake_case_to_upper_case(name)} with "
                f"{str(value).strip()}."
            )


# [END add_performance_max_retail_campaign]

if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v10")

    parser = argparse.ArgumentParser(
        description=("Creates a Performance Max retail campaign.")
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
        "-m",
        "--merchant_center_account_id",
        type=int,
        required=True,
        help="The Merchant Center account ID.",
    )
    parser.add_argument(
        "-f",
        "--sales_country",
        type=str,
        required=False,
        default="US",
        help="The sales country of products to include in the campaign",
    )
    parser.add_argument(
        "-u",
        "--final_url",
        type=str,
        required=False,
        default="http://www.example.com",
        help="The final URL for the asset group of the campaign.",
    )

    args = parser.parse_args()

    try:
        main(
            googleads_client,
            args.customer_id,
            args.merchant_center_account_id,
            args.sales_country,
            args.final_url,
        )
    except GoogleAdsException as ex:
        print(
            f'Request with ID "{ex.request_id}" failed with status '
            f'"{ex.error.code().name}" and includes the following errors:'
        )
        for error in ex.failure.errors:
            print(f'Error with message "{error.message}".')
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print(f"\t\tOn field: {field_path_element.field_name}")
        sys.exit(1)
