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
from typing import Dict, List, Union
from uuid import uuid4

from google.api_core import protobuf_helpers

from examples.utils.example_helpers import get_image_bytes_from_url
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.ads.googleads.util import convert_snake_case_to_upper_case
from google.ads.googleads.v22.enums.types.conversion_action_category import (
    ConversionActionCategoryEnum,
)
from google.ads.googleads.v22.enums.types.conversion_origin import (
    ConversionOriginEnum,
)
from google.ads.googleads.v22.enums.types.asset_field_type import (
    AssetFieldTypeEnum,
)
from google.ads.googleads.v22.resources.types.asset import Asset
from google.ads.googleads.v22.resources.types.asset_group import AssetGroup
from google.ads.googleads.v22.resources.types.asset_group_asset import (
    AssetGroupAsset,
)
from google.ads.googleads.v22.resources.types.asset_group_listing_group_filter import (
    AssetGroupListingGroupFilter,
)
from google.ads.googleads.v22.resources.types.campaign import Campaign
from google.ads.googleads.v22.resources.types.campaign_asset import (
    CampaignAsset,
)
from google.ads.googleads.v22.resources.types.campaign_budget import (
    CampaignBudget,
)
from google.ads.googleads.v22.resources.types.campaign_conversion_goal import (
    CampaignConversionGoal,
)
from google.ads.googleads.v22.resources.types.campaign_criterion import (
    CampaignCriterion,
)
from google.ads.googleads.v22.services.services.asset_group_service import (
    AssetGroupServiceClient,
)
from google.ads.googleads.v22.services.services.asset_service import (
    AssetServiceClient,
)
from google.ads.googleads.v22.services.services.campaign_budget_service import (
    CampaignBudgetServiceClient,
)
from google.ads.googleads.v22.services.services.campaign_conversion_goal_service import (
    CampaignConversionGoalServiceClient,
)
from google.ads.googleads.v22.services.services.campaign_service import (
    CampaignServiceClient,
)
from google.ads.googleads.v22.services.services.geo_target_constant_service import (
    GeoTargetConstantServiceClient,
)
from google.ads.googleads.v22.services.services.google_ads_service import (
    GoogleAdsServiceClient,
)
from google.ads.googleads.v22.services.types.google_ads_service import (
    MutateGoogleAdsResponse,
    MutateOperationResponse,
    SearchGoogleAdsRequest,
    SearchGoogleAdsResponse,
)
from google.ads.googleads.v22.services.types.google_ads_service import (
    MutateOperation,
)

# We specify temporary IDs that are specific to a single mutate request.
# Temporary IDs are always negative and unique within one mutate request.
#
# See https://developers.google.com/google-ads/api/docs/mutating/best-practices
# for further details.
#
# These temporary IDs are fixed because they are used in multiple places.
_BUDGET_TEMPORARY_ID: str = "-1"
_PERFORMANCE_MAX_CAMPAIGN_TEMPORARY_ID: str = "-2"
_ASSET_GROUP_TEMPORARY_ID: str = "-3"

# There are also entities that will be created in the same request but do not
# need to be fixed temporary IDs because they are referenced only once.
_next_temp_id: int = int(_ASSET_GROUP_TEMPORARY_ID) - 1


# [START add_performance_max_retail_campaign]
def main(
    client: GoogleAdsClient,
    customer_id: str,
    merchant_center_account_id: int,
    final_url: str,
    brand_guidelines_enabled: bool,
) -> None:
    """The main method that creates all necessary entities for the example.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        merchant_center_account_id: The Merchant Center account ID.
        final_url: the final URL.
        brand_guidelines_enabled: a boolean value indicating if the campaign is
          enabled for brand guidelines.
    """
    # [START add_performance_max_retail_campaign_1]
    googleads_service: GoogleAdsServiceClient = client.get_service(
        "GoogleAdsService"
    )

    # This campaign will override the customer conversion goals.
    # Retrieve the current list of customer conversion goals.
    customer_conversion_goals: List[
        Dict[
            str,
            Union[
                ConversionActionCategoryEnum.ConversionActionCategory,
                ConversionOriginEnum.ConversionOrigin,
            ],
        ]
    ] = get_customer_conversion_goals(client, customer_id)

    # Performance Max campaigns require that repeated assets such as headlines
    # and descriptions be created before the campaign.
    # For the list of required assets for a Performance Max campaign, see
    # https://developers.google.com/google-ads/api/docs/performance-max/assets
    #
    # Create the headlines.
    headline_asset_resource_names: List[str] = create_multiple_text_assets(
        client,
        customer_id,
        [
            "Travel",
            "Travel Reviews",
            "Book travel",
        ],
    )
    # Create the descriptions.
    description_asset_resource_names: List[str] = create_multiple_text_assets(
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
    campaign_budget_operation: MutateOperation = (
        create_campaign_budget_operation(
            client,
            customer_id,
        )
    )
    performance_max_campaign_operation: MutateOperation = (
        create_performance_max_campaign_operation(
            client,
            customer_id,
            merchant_center_account_id,
            brand_guidelines_enabled,
        )
    )
    campaign_criterion_operations: List[MutateOperation] = (
        create_campaign_criterion_operations(
            client,
            customer_id,
        )
    )
    asset_group_operation: MutateOperation = create_asset_group_operation(
        client, customer_id, final_url
    )
    listing_group_filter_operation: MutateOperation = (
        create_listing_group_filter_operation(client, customer_id)
    )
    asset_and_asset_group_asset_operations: List[MutateOperation] = (
        create_asset_and_asset_group_asset_operations(
            client,
            customer_id,
            headline_asset_resource_names,
            description_asset_resource_names,
            brand_guidelines_enabled,
        )
    )
    conversion_goal_operations: List[MutateOperation] = (
        create_conversion_goal_operations(
            client,
            customer_id,
            customer_conversion_goals,
        )
    )

    # Send the operations in a single Mutate request.
    response: MutateGoogleAdsResponse = googleads_service.mutate(
        customer_id=customer_id,
        mutate_operations=[
            # It's important to create these entities in this order because
            # they depend on each other.
            campaign_budget_operation,
            performance_max_campaign_operation,
            # Expand the list of multiple operations into the list of
            # other mutate operations.
            *campaign_criterion_operations,
            asset_group_operation,
            listing_group_filter_operation,
            *asset_and_asset_group_asset_operations,
            *conversion_goal_operations,
        ],
    )
    print_response_details(response)
    # [END add_performance_max_retail_campaign_1]


# [START add_performance_max_retail_campaign_2]
def create_campaign_budget_operation(
    client: GoogleAdsClient,
    customer_id: str,
) -> MutateOperation:
    """Creates a MutateOperation that creates a new CampaignBudget.

    A temporary ID will be assigned to this campaign budget so that it can be
    referenced by other objects being created in the same Mutate request.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.

    Returns:
        a MutateOperation that creates a CampaignBudget.
    """
    mutate_operation: MutateOperation = client.get_type("MutateOperation")
    campaign_budget_operation = mutate_operation.campaign_budget_operation
    campaign_budget: CampaignBudget = campaign_budget_operation.create
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
    campaign_budget_service: CampaignBudgetServiceClient = client.get_service(
        "CampaignBudgetService"
    )
    campaign_budget.resource_name = (
        campaign_budget_service.campaign_budget_path(
            customer_id, _BUDGET_TEMPORARY_ID
        )
    )

    return mutate_operation
    # [END add_performance_max_retail_campaign_2]


# [START add_performance_max_retail_campaign_3]
def create_performance_max_campaign_operation(
    client: GoogleAdsClient,
    customer_id: str,
    merchant_center_account_id: int,
    brand_guidelines_enabled: bool,
) -> MutateOperation:
    """Creates a MutateOperation that creates a new Performance Max campaign.

    A temporary ID will be assigned to this campaign so that it can
    be referenced by other objects being created in the same Mutate request.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        merchant_center_account_id: The Merchant Center account ID.
        brand_guidelines_enabled: a boolean value indicating if the campaign is
          enabled for brand guidelines.

    Returns:
        a MutateOperation that creates a campaign.
    """
    mutate_operation: MutateOperation = client.get_type("MutateOperation")
    campaign: Campaign = mutate_operation.campaign_operation.create
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
    # campaign.maximize_conversion_value.target_roas = 3.5
    # For first time users, it's recommended not to set a target ROAS.
    # Although target ROAS is optional, you still need to define it
    # even if you do not want to use it.
    campaign.maximize_conversion_value.target_roas = None
    # Below is what you would use if you want to maximize conversions
    # campaign.maximize_conversions.target_cpa_micros = None
    # The target CPA is optional. This is the average amount that you would
    # like to spend per conversion action.

    # Set the shopping settings.
    campaign.shopping_setting.merchant_id = merchant_center_account_id

    # Optional: To use products only from a specific feed, set
    # shopping_setting.feed_label to the feed label used in Merchant Center.
    # See: https://support.google.com/merchants/answer/12453549.
    # Omitting the shopping_setting.feed_label field will use products from all
    # feeds.
    # campaign.shopping_setting.feed_label = "INSERT_FEED_LABEL_HERE"

    # Set if the campaign is enabled for brand guidelines. For more information
    # on brand guidelines, see https://support.google.com/google-ads/answer/14934472.
    campaign.brand_guidelines_enabled = brand_guidelines_enabled

    # Assign the resource name with a temporary ID.
    campaign_service: CampaignServiceClient = client.get_service(
        "CampaignService"
    )
    campaign.resource_name = campaign_service.campaign_path(
        customer_id, _PERFORMANCE_MAX_CAMPAIGN_TEMPORARY_ID
    )
    # Set the budget using the given budget resource name.
    campaign_budget_service: CampaignBudgetServiceClient = client.get_service(
        "CampaignBudgetService"
    )
    campaign.campaign_budget = campaign_budget_service.campaign_budget_path(
        customer_id, _BUDGET_TEMPORARY_ID
    )

    # Declare whether or not this campaign serves political ads targeting the
    # EU. Valid values are:
    #   CONTAINS_EU_POLITICAL_ADVERTISING
    #   DOES_NOT_CONTAIN_EU_POLITICAL_ADVERTISING
    campaign.contains_eu_political_advertising = (
        client.enums.EuPoliticalAdvertisingStatusEnum.DOES_NOT_CONTAIN_EU_POLITICAL_ADVERTISING
    )

    # Optional fields
    campaign.start_date = (datetime.now() + timedelta(1)).strftime("%Y%m%d")
    campaign.end_date = (datetime.now() + timedelta(365)).strftime("%Y%m%d")

    # Configures the optional opt-in/out status for asset automation settings.
    for asset_automation_type_enum in [
        client.enums.AssetAutomationTypeEnum.GENERATE_IMAGE_EXTRACTION,
        client.enums.AssetAutomationTypeEnum.FINAL_URL_EXPANSION_TEXT_ASSET_AUTOMATION,
        client.enums.AssetAutomationTypeEnum.TEXT_ASSET_AUTOMATION,
        client.enums.AssetAutomationTypeEnum.GENERATE_ENHANCED_YOUTUBE_VIDEOS,
        client.enums.AssetAutomationTypeEnum.GENERATE_IMAGE_ENHANCEMENT
    ]:
        asset_automattion_setting: Campaign.AssetAutomationSetting = client.get_type("Campaign").AssetAutomationSetting()
        asset_automattion_setting.asset_automation_type = asset_automation_type_enum
        asset_automattion_setting.asset_automation_status = client.enums.AssetAutomationStatusEnum.OPTED_IN
        campaign.asset_automation_settings.append(asset_automattion_setting)

    return mutate_operation
    # [END add_performance_max_retail_campaign_3]


# [START add_performance_max_retail_campaign_4]
def create_campaign_criterion_operations(
    client: GoogleAdsClient,
    customer_id: str,
) -> List[MutateOperation]:
    """Creates a list of MutateOperations that create new campaign criteria.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.

    Returns:
        a list of MutateOperations that create new campaign criteria.
    """
    campaign_service: CampaignServiceClient = client.get_service(
        "CampaignService"
    )
    geo_target_constant_service: GeoTargetConstantServiceClient = (
        client.get_service("GeoTargetConstantService")
    )
    googleads_service: GoogleAdsServiceClient = client.get_service(
        "GoogleAdsService"
    )

    operations: List[MutateOperation] = []
    # Set the LOCATION campaign criteria.
    # Target all of New York City except Brooklyn.
    # Location IDs are listed here:
    # https://developers.google.com/google-ads/api/reference/data/geotargets
    # and they can also be retrieved using the GeoTargetConstantService as shown
    # here: https://developers.google.com/google-ads/api/docs/targeting/location-targeting
    mutate_operation_nyc: MutateOperation = client.get_type("MutateOperation")
    campaign_criterion_nyc: CampaignCriterion = (
        mutate_operation_nyc.campaign_criterion_operation.create
    )
    campaign_criterion_nyc.campaign = campaign_service.campaign_path(
        customer_id, _PERFORMANCE_MAX_CAMPAIGN_TEMPORARY_ID
    )
    # Adds one positive location target for New York City (ID=1023191),
    # specifically adding the positive criteria before the negative one.
    campaign_criterion_nyc.location.geo_target_constant = (
        geo_target_constant_service.geo_target_constant_path("1023191")
    )
    campaign_criterion_nyc.negative = False
    operations.append(mutate_operation_nyc)

    # Next add the negative target for Brooklyn (ID=1022762).
    mutate_operation_brooklyn: MutateOperation = client.get_type(
        "MutateOperation"
    )
    campaign_criterion_brooklyn: CampaignCriterion = (
        mutate_operation_brooklyn.campaign_criterion_operation.create
    )
    campaign_criterion_brooklyn.campaign = campaign_service.campaign_path(
        customer_id, _PERFORMANCE_MAX_CAMPAIGN_TEMPORARY_ID
    )
    campaign_criterion_brooklyn.location.geo_target_constant = (
        geo_target_constant_service.geo_target_constant_path("1022762")
    )
    campaign_criterion_brooklyn.negative = True
    operations.append(mutate_operation_brooklyn)

    # Set the LANGUAGE campaign criterion.
    mutate_operation_lang: MutateOperation = client.get_type("MutateOperation")
    campaign_criterion_lang: CampaignCriterion = (
        mutate_operation_lang.campaign_criterion_operation.create
    )
    campaign_criterion_lang.campaign = campaign_service.campaign_path(
        customer_id, _PERFORMANCE_MAX_CAMPAIGN_TEMPORARY_ID
    )
    # Set the language.
    # For a list of all language codes, see:
    # https://developers.google.com/google-ads/api/reference/data/codes-formats#expandable-7
    campaign_criterion_lang.language.language_constant = (
        googleads_service.language_constant_path("1000")
    )  # English
    operations.append(mutate_operation_lang)

    return operations
    # [END add_performance_max_retail_campaign_4]


# [START add_performance_max_retail_campaign_5]
def create_multiple_text_assets(
    client: GoogleAdsClient, customer_id: str, texts: List[str]
) -> List[str]:
    """Creates multiple text assets and returns the list of resource names.

    These repeated assets must be created in a separate request prior to
    creating the campaign.

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
    googleads_service: GoogleAdsServiceClient = client.get_service(
        "GoogleAdsService"
    )

    operations: List[MutateOperation] = []
    for text_content in texts:
        mutate_operation: MutateOperation = client.get_type("MutateOperation")
        asset: Asset = mutate_operation.asset_operation.create
        asset.text_asset.text = text_content
        operations.append(mutate_operation)

    # Send the operations in a single Mutate request.
    response: MutateGoogleAdsResponse = googleads_service.mutate(
        customer_id=customer_id,
        mutate_operations=operations,
    )
    asset_resource_names: List[str] = []
    for result in response.mutate_operation_responses:
        if result._pb.HasField("asset_result"):
            asset_resource_names.append(result.asset_result.resource_name)
    print_response_details(response)
    return asset_resource_names
    # [END add_performance_max_retail_campaign_5]


# [START add_performance_max_retail_campaign_10]
def create_asset_group_operation(
    client: GoogleAdsClient, customer_id: str, final_url: str
) -> MutateOperation:
    """Creates a MutateOperation that creates a new asset group.

    A temporary ID will be assigned to this asset group so that it can
    be referenced by other objects being created in the same Mutate request.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        final_url: the final URL.

    Returns:
        a MutateOperation that creates a new asset group.
    """
    campaign_service: CampaignServiceClient = client.get_service(
        "CampaignService"
    )
    asset_group_service: AssetGroupServiceClient = client.get_service(
        "AssetGroupService"
    )
    # Create the AssetGroup.
    mutate_operation: MutateOperation = client.get_type("MutateOperation")
    asset_group: AssetGroup = mutate_operation.asset_group_operation.create
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

    return mutate_operation
    # [END add_performance_max_retail_campaign_10]


# [START add_performance_max_retail_campaign_11]
def create_listing_group_filter_operation(
    client: GoogleAdsClient, customer_id: str
) -> MutateOperation:
    """Creates a MutateOperation that creates a new listing group filter.

    A temporary ID will be assigned to this listing group filter so that it
    can be referenced by other objects being created in the same Mutate request.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.

    Returns:
        a MutateOperation that creates a new listing group filter.
    """
    asset_group_service: AssetGroupServiceClient = client.get_service(
        "AssetGroupService"
    )
    # Creates a new ad group criterion containing the "default" listing
    # group (All products).
    mutate_operation: MutateOperation = client.get_type("MutateOperation")
    asset_group_listing_group: AssetGroupListingGroupFilter = (
        mutate_operation.asset_group_listing_group_filter_operation.create
    )
    asset_group_listing_group.asset_group = (
        asset_group_service.asset_group_path(
            customer_id,
            _ASSET_GROUP_TEMPORARY_ID,
        )
    )
    asset_group_listing_group.type_ = (
        client.enums.ListingGroupFilterTypeEnum.UNIT_INCLUDED
    )
    # Because this is a Performance Max campaign for retail, we need to specify
    # that this is in the shopping listing source.
    asset_group_listing_group.listing_source = (
        client.enums.ListingGroupFilterListingSourceEnum.SHOPPING
    )

    return mutate_operation
    # [END add_performance_max_retail_campaign_11]


# [START add_performance_max_retail_campaign_6]
def create_asset_and_asset_group_asset_operations(
    client: GoogleAdsClient,
    customer_id: str,
    headline_asset_resource_names: List[str],
    description_asset_resource_names: List[str],
    brand_guidelines_enabled: bool,
) -> List[MutateOperation]:
    """Creates a list of MutateOperations that create a new asset_group.

    A temporary ID will be assigned to this asset group so that it can
    be referenced by other objects being created in the same Mutate request.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        headline_asset_resource_names: a list of headline resource names.
        description_asset_resource_names: a list of description resource names.
        brand_guidelines_enabled: a boolean value indicating if the campaign is
          enabled for brand guidelines.

    Returns:
        MutateOperations that create a new asset group and related assets.
    """
    asset_group_service: AssetGroupServiceClient = client.get_service(
        "AssetGroupService"
    )

    operations: List[MutateOperation] = []

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
        mutate_operation: MutateOperation = client.get_type("MutateOperation")
        asset_group_asset: AssetGroupAsset = (
            mutate_operation.asset_group_asset_operation.create
        )
        asset_group_asset.field_type = client.enums.AssetFieldTypeEnum.HEADLINE
        asset_group_asset.asset_group = asset_group_service.asset_group_path(
            customer_id,
            _ASSET_GROUP_TEMPORARY_ID,
        )
        asset_group_asset.asset = resource_name
        operations.append(mutate_operation)

    #  Link the description assets.
    for resource_name in description_asset_resource_names:
        mutate_operation: MutateOperation = client.get_type("MutateOperation")
        asset_group_asset: AssetGroupAsset = (
            mutate_operation.asset_group_asset_operation.create
        )
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
    mutate_operations_long_headline: List[MutateOperation] = (
        create_and_link_text_asset(
            client,
            customer_id,
            "Travel the World",
            client.enums.AssetFieldTypeEnum.LONG_HEADLINE,
        )
    )
    operations.extend(mutate_operations_long_headline)

    # Create and link the business name and logo asset.
    mutate_operations_brand: List[MutateOperation] = (
        create_and_link_brand_assets(
            client,
            customer_id,
            brand_guidelines_enabled,
            "Interplanetary Cruises",
            "https://gaagl.page.link/1Crm",
            "Logo Image",
        )
    )
    operations.extend(mutate_operations_brand)

    # Create and link the image assets.

    # Create and link the Marketing Image Asset.
    mutate_operations_marketing_image: List[MutateOperation] = (
        create_and_link_image_asset(
            client,
            customer_id,
            "https://gaagl.page.link/Eit5",
            client.enums.AssetFieldTypeEnum.MARKETING_IMAGE,
            "Marketing Image",
        )
    )
    operations.extend(mutate_operations_marketing_image)

    # Create and link the Square Marketing Image Asset.
    mutate_operations_square_image: List[MutateOperation] = (
        create_and_link_image_asset(
            client,
            customer_id,
            "https://gaagl.page.link/bjYi",
            client.enums.AssetFieldTypeEnum.SQUARE_MARKETING_IMAGE,
            "Square Marketing Image",
        )
    )
    operations.extend(mutate_operations_square_image)

    # After being created the list must be sorted so that all asset
    # operations come before all the asset group asset operations,
    # otherwise the API will reject the request.
    return sort_asset_and_asset_group_asset_operations(operations)
    # [END add_performance_max_retail_campaign_6]


# [START add_performance_max_retail_campaign_7]
def create_and_link_text_asset(
    client: GoogleAdsClient,
    customer_id: str,
    text: str,
    field_type: AssetFieldTypeEnum.AssetFieldType,
) -> List[MutateOperation]:
    """Creates a list of MutateOperations that create a new linked text asset.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        text: the text of the asset to be created.
        field_type: the field_type of the new asset in the AssetGroupAsset.

    Returns:
        MutateOperations that create a new linked text asset.
    """
    global _next_temp_id
    operations: List[MutateOperation] = []
    asset_service: AssetServiceClient = client.get_service("AssetService")
    asset_group_service: AssetGroupServiceClient = client.get_service(
        "AssetGroupService"
    )

    # Create the Text Asset.
    asset_temp_resource_name = asset_service.asset_path(
        customer_id, str(_next_temp_id)
    )
    mutate_operation_asset: MutateOperation = client.get_type("MutateOperation")
    asset: Asset = mutate_operation_asset.asset_operation.create
    asset.resource_name = asset_temp_resource_name
    asset.text_asset.text = text
    operations.append(mutate_operation_asset)

    # Create an AssetGroupAsset to link the Asset to the AssetGroup.
    mutate_operation_group_asset: MutateOperation = client.get_type(
        "MutateOperation"
    )
    asset_group_asset: AssetGroupAsset = (
        mutate_operation_group_asset.asset_group_asset_operation.create
    )
    asset_group_asset.field_type = field_type
    asset_group_asset.asset_group = asset_group_service.asset_group_path(
        customer_id,
        _ASSET_GROUP_TEMPORARY_ID,
    )
    asset_group_asset.asset = asset_temp_resource_name
    operations.append(mutate_operation_group_asset)

    _next_temp_id -= 1
    return operations
    # [END add_performance_max_retail_campaign_7]


# [START add_performance_max_retail_campaign_8]
def create_and_link_image_asset(
    client: GoogleAdsClient,
    customer_id: str,
    url: str,
    field_type: AssetFieldTypeEnum.AssetFieldType,
    asset_name: str,
) -> List[MutateOperation]:
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
    global _next_temp_id
    operations: List[MutateOperation] = []
    asset_service: AssetServiceClient = client.get_service("AssetService")
    asset_group_service: AssetGroupServiceClient = client.get_service(
        "AssetGroupService"
    )

    # Create the Image Asset.
    asset_temp_resource_name = asset_service.asset_path(
        customer_id, str(_next_temp_id)
    )
    mutate_operation_asset: MutateOperation = client.get_type("MutateOperation")
    asset: Asset = mutate_operation_asset.asset_operation.create
    asset.resource_name = asset_temp_resource_name
    asset.type_ = client.enums.AssetTypeEnum.IMAGE
    # Provide a unique friendly name to identify your asset.
    # When there is an existing image asset with the same content but a different
    # name, the new name will be dropped silently.
    asset.name = asset_name
    asset.image_asset.data = get_image_bytes_from_url(url)
    operations.append(mutate_operation_asset)

    # Create an AssetGroupAsset to link the Asset to the AssetGroup.
    mutate_operation_group_asset: MutateOperation = client.get_type(
        "MutateOperation"
    )
    asset_group_asset: AssetGroupAsset = (
        mutate_operation_group_asset.asset_group_asset_operation.create
    )
    asset_group_asset.field_type = field_type
    asset_group_asset.asset_group = asset_group_service.asset_group_path(
        customer_id,
        _ASSET_GROUP_TEMPORARY_ID,
    )
    asset_group_asset.asset = asset_temp_resource_name
    operations.append(mutate_operation_group_asset)

    _next_temp_id -= 1
    return operations
    # [END add_performance_max_retail_campaign_8]


# [START add_performance_max_retail_campaign_12]
def sort_asset_and_asset_group_asset_operations(
    operations: List[MutateOperation],
) -> List[MutateOperation]:
    """Sorts a list of asset and asset group asset operations.

    This sorts the list such that all asset operations precede
    all asset group asset operations. If asset group assets are
    created before assets then an error will be returned by
    the API.

    Args:
        operations: a list of asset and asset group asset operations.

    Returns:
        a sorted list of asset and asset group asset operations.
    """

    def sorter(operation: MutateOperation) -> bool:
        """Determines whether the operation creates an asset group asset.

        Args:
            operation: a MutateOperation instance.

        Returns:
            True if the MutateOperation creates an asset group asset.
        """
        # Check if the oneof field 'asset_group_asset_operation' is set.
        return (
            operation.asset_group_asset_operation
            != type(operation.asset_group_asset_operation)()
        )

    return sorted(operations, key=sorter)
    # [END add_performance_max_retail_campaign_12]


# [START add_performance_max_retail_campaign_9]
def get_customer_conversion_goals(
    client: GoogleAdsClient, customer_id: str
) -> List[
    Dict[
        str,
        Union[
            ConversionActionCategoryEnum.ConversionActionCategory,
            ConversionOriginEnum.ConversionOrigin,
        ],
    ]
]:
    """Retrieves the list of customer conversion goals.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.

    Returns:
        a list of dicts containing the category and origin of customer
        conversion goals.
    """
    ga_service: GoogleAdsServiceClient = client.get_service("GoogleAdsService")
    customer_conversion_goals: List[
        Dict[
            str,
            Union[
                ConversionActionCategoryEnum.ConversionActionCategory,
                ConversionOriginEnum.ConversionOrigin,
            ],
        ]
    ] = []
    query: str = """
            SELECT
              customer_conversion_goal.category,
              customer_conversion_goal.origin
            FROM customer_conversion_goal
            """
    # The number of conversion goals is typically less than 50 so we use
    # GoogleAdsService.search instead of search_stream.
    search_request: SearchGoogleAdsRequest = client.get_type(
        "SearchGoogleAdsRequest"
    )
    search_request.customer_id = customer_id
    search_request.query = query
    results: SearchGoogleAdsResponse = ga_service.search(request=search_request)

    # Iterate over the results and build the list of conversion goals.
    for row in results:
        customer_conversion_goals.append(
            {
                "category": row.customer_conversion_goal.category,
                "origin": row.customer_conversion_goal.origin,
            }
        )
    return customer_conversion_goals


def create_conversion_goal_operations(
    client: GoogleAdsClient,
    customer_id: str,
    customer_conversion_goals: List[
        Dict[
            str,
            Union[
                ConversionActionCategoryEnum.ConversionActionCategory,
                ConversionOriginEnum.ConversionOrigin,
            ],
        ]
    ],
) -> List[MutateOperation]:
    """Creates a list of MutateOperations that override customer conversion goals.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        customer_conversion_goals: the list of customer conversion goals that
          will be overridden.

    Returns:
        MutateOperations that update campaign conversion goals.
    """
    campaign_conversion_goal_service: CampaignConversionGoalServiceClient = (
        client.get_service("CampaignConversionGoalService")
    )
    operations: List[MutateOperation] = []

    # To override the customer conversion goals, we will change the
    # biddability of each of the customer conversion goals so that only
    # the desired conversion goal is biddable in this campaign.
    for customer_goal_dict in customer_conversion_goals:
        mutate_operation: MutateOperation = client.get_type("MutateOperation")
        campaign_conversion_goal: CampaignConversionGoal = (
            mutate_operation.campaign_conversion_goal_operation.update
        )

        category_enum_value: (
            ConversionActionCategoryEnum.ConversionActionCategory
        ) = customer_goal_dict["category"]
        origin_enum_value: ConversionOriginEnum.ConversionOrigin = (
            customer_goal_dict["origin"]
        )

        campaign_conversion_goal.resource_name = (
            campaign_conversion_goal_service.campaign_conversion_goal_path(
                customer_id,
                _PERFORMANCE_MAX_CAMPAIGN_TEMPORARY_ID,
                category_enum_value.name,
                origin_enum_value.name,
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
            category_enum_value
            == client.enums.ConversionActionCategoryEnum.PURCHASE
            and origin_enum_value == client.enums.ConversionOriginEnum.WEBSITE
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


def create_and_link_brand_assets(
    client: GoogleAdsClient,
    customer_id: str,
    brand_guidelines_enabled: bool,
    business_name: str,
    logo_url: str,
    logo_name: str,
) -> List[MutateOperation]:
    """Creates a list of MutateOperations that create linked brand assets.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        brand_guidelines_enabled: a boolean value indicating if the campaign is
          enabled for brand guidelines.
        business_name: the business name text to be put into an asset.
        logo_url: the url of the logo to be retrieved and put into an asset.
        logo_name: the asset name of the logo.

    Returns:
        MutateOperations that create linked brand assets.
    """
    global _next_temp_id
    operations: List[MutateOperation] = []
    asset_service: AssetServiceClient = client.get_service("AssetService")

    # Create the Text Asset.
    text_asset_temp_id: int = _next_temp_id
    _next_temp_id -= 1
    text_asset_resource_name = asset_service.asset_path(
        customer_id, str(text_asset_temp_id)
    )

    text_mutate_operation: MutateOperation = client.get_type("MutateOperation")
    text_asset_obj: Asset = text_mutate_operation.asset_operation.create
    text_asset_obj.resource_name = text_asset_resource_name
    text_asset_obj.text_asset.text = business_name
    operations.append(text_mutate_operation)

    # Create the Image Asset.
    image_asset_temp_id: int = _next_temp_id
    _next_temp_id -= 1
    image_asset_resource_name = asset_service.asset_path(
        customer_id, str(image_asset_temp_id)
    )

    image_mutate_operation: MutateOperation = client.get_type("MutateOperation")
    image_asset_obj: Asset = image_mutate_operation.asset_operation.create
    image_asset_obj.resource_name = image_asset_resource_name
    # Provide a unique friendly name to identify your asset.
    # When there is an existing image asset with the same content but a different
    # name, the new name will be dropped silently.
    image_asset_obj.name = logo_name
    image_asset_obj.type_ = client.enums.AssetTypeEnum.IMAGE
    image_asset_obj.image_asset.data = get_image_bytes_from_url(logo_url)
    operations.append(image_mutate_operation)

    if brand_guidelines_enabled:
        # Create CampaignAsset resources to link the Asset resources to the Campaign.
        campaign_service: CampaignServiceClient = client.get_service(
            "CampaignService"
        )

        business_name_ca_mutate_op: MutateOperation = client.get_type(
            "MutateOperation"
        )
        business_name_campaign_asset: CampaignAsset = (
            business_name_ca_mutate_op.campaign_asset_operation.create
        )
        business_name_campaign_asset.field_type = (
            client.enums.AssetFieldTypeEnum.BUSINESS_NAME
        )
        business_name_campaign_asset.campaign = campaign_service.campaign_path(
            customer_id, _PERFORMANCE_MAX_CAMPAIGN_TEMPORARY_ID
        )
        business_name_campaign_asset.asset = text_asset_resource_name
        operations.append(business_name_ca_mutate_op)

        logo_ca_mutate_op: MutateOperation = client.get_type("MutateOperation")
        logo_campaign_asset: CampaignAsset = (
            logo_ca_mutate_op.campaign_asset_operation.create
        )
        logo_campaign_asset.field_type = client.enums.AssetFieldTypeEnum.LOGO
        logo_campaign_asset.campaign = campaign_service.campaign_path(
            customer_id, _PERFORMANCE_MAX_CAMPAIGN_TEMPORARY_ID
        )
        logo_campaign_asset.asset = image_asset_resource_name
        operations.append(logo_ca_mutate_op)

    else:
        # Create AssetGroupAsset resources to link the Asset resources to the AssetGroup.
        asset_group_service: AssetGroupServiceClient = client.get_service(
            "AssetGroupService"
        )

        business_name_aga_mutate_op: MutateOperation = client.get_type(
            "MutateOperation"
        )
        business_name_asset_group_asset: AssetGroupAsset = (
            business_name_aga_mutate_op.asset_group_asset_operation.create
        )
        business_name_asset_group_asset.field_type = (
            client.enums.AssetFieldTypeEnum.BUSINESS_NAME
        )
        business_name_asset_group_asset.asset_group = (
            asset_group_service.asset_group_path(
                customer_id,
                _ASSET_GROUP_TEMPORARY_ID,
            )
        )
        business_name_asset_group_asset.asset = text_asset_resource_name
        operations.append(business_name_aga_mutate_op)

        logo_aga_mutate_op: MutateOperation = client.get_type("MutateOperation")
        logo_asset_group_asset: AssetGroupAsset = (
            logo_aga_mutate_op.asset_group_asset_operation.create
        )
        logo_asset_group_asset.field_type = client.enums.AssetFieldTypeEnum.LOGO
        logo_asset_group_asset.asset_group = (
            asset_group_service.asset_group_path(
                customer_id,
                _ASSET_GROUP_TEMPORARY_ID,
            )
        )
        logo_asset_group_asset.asset = image_asset_resource_name
        operations.append(logo_aga_mutate_op)

    return operations


def print_response_details(response: MutateGoogleAdsResponse) -> None:
    """Prints the details of a MutateGoogleAdsResponse.

    Parses the "response" oneof field name and uses it to extract the new
    entity's name and resource name.

    Args:
        response: a MutateGoogleAdsResponse object.
    """
    # Parse the Mutate response to print details about the entities that
    # were created by the request.
    suffix: str = "_result"
    for result_item in response.mutate_operation_responses:
        # Ensure result_item is MutateOperationResponse, not just Any
        result_pb: MutateOperationResponse = result_item
        for field_descriptor, value in result_pb._pb.ListFields():
            field_name_str: str = field_descriptor.name
            if field_name_str.endswith(suffix):
                name = field_name_str[: -len(suffix)]
            else:
                name = field_name_str
            print(
                f"Created a(n) {convert_snake_case_to_upper_case(name)} with "
                f"{str(value).strip()}."
            )


# [END add_performance_max_retail_campaign]

if __name__ == "__main__":
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
        "-u",
        "--final_url",
        type=str,
        required=False,
        default="http://www.example.com",
        help="The final URL for the asset group of the campaign.",
    )
    parser.add_argument(
        "-b",
        "--brand_guidelines_enabled",
        type=bool,
        default=False,
        help=(
            "A boolean value indicating if the created campaign is enabled "
            "for brand guidelines."
        ),
    )

    args: argparse.Namespace = parser.parse_args()

    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client: GoogleAdsClient = GoogleAdsClient.load_from_storage(
        version="v22"
    )

    try:
        main(
            googleads_client,
            args.customer_id,
            args.merchant_center_account_id,
            args.final_url,
            args.brand_guidelines_enabled,
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
