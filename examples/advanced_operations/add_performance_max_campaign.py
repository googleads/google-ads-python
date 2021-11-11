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
"""This example shows how to create a Performance Max campaign.

For more information about Performance Max campaigns, see
https://developers.google.com/google-ads/api/docs/performance-max/overview

Prerequisites:
- You must have at least one conversion action in the account. For
more about conversion actions, see
https://developers.google.com/google-ads/api/docs/conversions/overview#conversion_actions

This example uses the default customer conversion goals. For an example
of setting campaign-specific conversion goals, see
shopping_ads/add_performance_max_retail_campaign.py
"""


import argparse
from datetime import datetime, timedelta
import sys
from uuid import uuid4

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


# [START add_performance_max_campaign]
def main(
    client,
    customer_id,
):
    """The main method that creates all necessary entities for the example.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
    """
    # [START add_performance_max_campaign_1]
    googleads_service = client.get_service("GoogleAdsService")

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
        )
    )
    campaign_criterion_operations = _create_campaign_criterion_operations(
        client,
        customer_id,
    )
    asset_group_operations = _create_asset_group_operation(
        client,
        customer_id,
        headline_asset_resource_names,
        description_asset_resource_names,
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
            # other mutate operations
            *campaign_criterion_operations,
            *asset_group_operations,
        ],
    )
    _print_response_details(response)
    # [END add_performance_max_campaign_1]


# [START add_performance_max_campaign_2]
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
    campaign_budget.name = f"Performance Max campaign budget #{uuid4()}"
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
    # [END add_performance_max_campaign_2]


# [START add_performance_max_campaign_3]
def _create_performance_max_campaign_operation(
    client,
    customer_id,
):
    """Creates a MutateOperation that creates a new Performance Max campaign.

    A temporary ID will be assigned to this campaign so that it can
    be referenced by other objects being created in the same Mutate request.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.

    Returns:
        a MutateOperation that creates a campaign.
    """
    mutate_operation = client.get_type("MutateOperation")
    campaign = mutate_operation.campaign_operation.create
    campaign.name = f"Performance Max campaign #{uuid4()}"
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
    # Max Conversion and Maximize Conversion Value are the only strategies
    # supported for Performance Max campaigns.
    # An optional ROAS (Return on Advertising Spend) can be set for
    # maximize_conversion_value. The ROAS value must be specified as a ratio in
    # the API. It is calculated by dividing "total value" by "total spend".
    # For more information on Maximize Conversion Value, see the support
    # article: http://support.google.com/google-ads/answer/7684216.
    # A target_roas of 3.5 corresponds to a 350% return on ad spend.
    campaign.bidding_strategy_type = (
        client.enums.BiddingStrategyTypeEnum.MAXIMIZE_CONVERSION_VALUE
    )
    campaign.maximize_conversion_value.target_roas = 3.5

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
    # [END add_performance_max_campaign_3]


# [START add_performance_max_campaign_4]
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
    language_constant_service = client.get_service("LanguageConstantService")

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
        language_constant_service.language_constant_path("1000")  # English
    )
    operations.append(mutate_operation)

    return operations
    # [END add_performance_max_campaign_4]


# [START add_performance_max_campaign_5]
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
    # [END add_performance_max_campaign_5]


# [START add_performance_max_campaign_6]
def _create_asset_group_operation(
    client,
    customer_id,
    headline_asset_resource_names,
    description_asset_resource_names,
):
    """Creates a list of MutateOperations that create a new asset_group.

    A temporary ID will be assigned to this asset group so that it can
    be referenced by other objects being created in the same Mutate request.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        headline_asset_resource_names: a list of headline resource names.
        description_asset_resource_names: a list of description resource names.

    Returns:
        MutateOperations that create a new asset group and related assets.
    """
    asset_group_service = client.get_service("AssetGroupService")
    campaign_service = client.get_service("CampaignService")

    operations = []

    # Create the AssetGroup
    mutate_operation = client.get_type("MutateOperation")
    asset_group = mutate_operation.asset_group_operation.create
    asset_group.name = f"Performance Max asset group #{uuid4()}"
    asset_group.campaign = campaign_service.campaign_path(
        customer_id, _PERFORMANCE_MAX_CAMPAIGN_TEMPORARY_ID
    )
    asset_group.final_urls.append("http://www.example.com")
    asset_group.final_mobile_urls.append("http://www.example.com")
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
    )
    operations.extend(mutate_operations)

    # Create and link the Marketing Image Asset.
    mutate_operations = _create_and_link_image_asset(
        client,
        customer_id,
        "https://gaagl.page.link/Eit5",
        client.enums.AssetFieldTypeEnum.MARKETING_IMAGE,
    )
    operations.extend(mutate_operations)

    # Create and link the Square Marketing Image Asset.
    mutate_operations = _create_and_link_image_asset(
        client,
        customer_id,
        "https://gaagl.page.link/bjYi",
        client.enums.AssetFieldTypeEnum.SQUARE_MARKETING_IMAGE,
    )
    operations.extend(mutate_operations)
    return operations
    # [END add_performance_max_campaign_6]


# [START add_performance_max_campaign_7]
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
    # [END add_performance_max_campaign_7]


# [START add_performance_max_campaign_8]
def _create_and_link_image_asset(client, customer_id, url, field_type):
    """Creates a list of MutateOperations that create a new linked image asset.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        url: the url of the image to be retrieved and put into an asset.
        field_type: the field_type of the new asset in the AssetGroupAsset.

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
    # [END add_performance_max_campaign_8]


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


# [END add_performance_max_campaign]

if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v9")

    parser = argparse.ArgumentParser(
        description=("Creates a Performance Max campaign.")
    )
    # The following argument(s) should be provided to run the example.
    parser.add_argument(
        "-c",
        "--customer_id",
        type=str,
        required=True,
        help="The Google Ads customer ID.",
    )

    args = parser.parse_args()

    try:
        main(
            googleads_client,
            args.customer_id,
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
