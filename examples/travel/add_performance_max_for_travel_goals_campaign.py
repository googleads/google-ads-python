#!/usr/bin/env python
# Copyright 2023 Google LLC
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
"""This example shows how to create a Performance Max for travel goals campaign.

It also uses TravelAssetSuggestionService to fetch suggested assets for creating
an asset group. In case there are not enough assets for the asset group
(required by Performance Max), this example will create more assets to fulfill
the requirements.

For more information about Performance Max campaigns, see
https://developers.google.com/google-ads/api/docs/performance-max/overview.

Prerequisites:
- You must have at least one conversion action in the account. For more about
  conversion actions, see
  https://developers.google.com/google-ads/api/docs/conversions/overview#conversion_actions.

Notes:
- This example uses the default customer conversion goals. For an example of
  setting campaign-specific conversion goals, see
  shopping_ads/add_performance_max_retail_campaign.py.
- To learn how to create asset group signals, see
  advanced_operations/add_performance_max_campaign.py.
"""


import argparse
import sys


from examples.utils.example_helpers import (
    get_printable_datetime,
    get_image_bytes_from_url,
)
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


MIN_REQUIRED_TEXT_ASSET_COUNTS = {
    "HEADLINE": 3,
    "LONG_HEADLINE": 1,
    "DESCRIPTION": 2,
    "BUSINESS_NAME": 1,
}

MIN_REQUIRED_IMAGE_ASSET_COUNTS = {
    "MARKETING_IMAGE": 1,
    "SQUARE_MARKETING_IMAGE": 1,
    "LOGO": 1,
}

DEFAULT_TEXT_ASSETS_INFO = {
    "HEADLINE": ["Hotel", "Travel Reviews", "Book travel"],
    "LONG_HEADLINE": ["Travel the World"],
    "DESCRIPTION": [
        "Great deal for your beloved hotel",
        "Best rate guaranteed",
    ],
    "BUSINESS_NAME": ["Interplanetary Cruises"],
}

DEFAULT_IMAGE_ASSETS_INFO = {
    "MARKETING_IMAGE": ["https://gaagl.page.link/Eit5"],
    "SQUARE_MARKETING_IMAGE": ["https://gaagl.page.link/bjYi"],
    "LOGO": ["https://gaagl.page.link/bjYi"],
}

# We specify temporary IDs that are specific to a single mutate request.
# Temporary IDs are always negative and unique within one mutate request.

# For further details, see:
# https://developers.google.com/google-ads/api/docs/mutating/best-practices

# These temporary IDs are global because they are used throughout the module.
ASSET_TEMPORARY_ID = -1
BUDGET_TEMPORARY_ID = -2
CAMPAIGN_TEMPORARY_ID = -3
ASSET_GROUP_TEMPORARY_ID = -4

# There are also entities that will be created in the same request but do not
# need to be fixed temporary IDs because they are referenced only once.
next_temp_id = ASSET_GROUP_TEMPORARY_ID - 1


def main(client, customer_id, place_id):
    """The main method that creates all necessary entities for the example.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        place_id: a place ID identifying a place in the Google Places database.
    """
    # Gets hotel asset suggestion using the TravelAssetSuggestionService.
    hotel_asset_suggestion = get_hotel_asset_suggestion(
        client, customer_id, place_id
    )

    # Performance Max campaigns require that repeated assets such as headlines
    # and descriptions be created before the campaign. For the list of required
    # assets for a Performance Max campaign, see:
    # https://developers.google.com/google-ads/api/docs/performance-max/assets.

    # This step is the same for all types of Performance Max campaigns.

    # Creates the headlines using the hotel asset suggestion.
    headline_asset_resource_names = create_multiple_text_assets(
        client,
        customer_id,
        client.enums.AssetFieldTypeEnum.HEADLINE,
        hotel_asset_suggestion,
    )

    # Creates the descriptions using the hotel asset suggestion.
    description_asset_resource_names = create_multiple_text_assets(
        client,
        customer_id,
        client.enums.AssetFieldTypeEnum.DESCRIPTION,
        hotel_asset_suggestion,
    )

    # Creates a hotel property asset set, which will be used later to link with
    # a newly created campaign.
    hotel_property_asset_set_resource_name = create_hotel_asset_set(
        client, customer_id
    )

    # Creates a hotel property asset and links it with the previously created
    # hotel property asset set. This asset will also be linked to an asset group
    # in the later steps. In a real-world scenario, you'd need to create assets
    # for each of your hotel properties. We use one hotel property here for
    # simplicity. Both asset and asset set need to be created before creating a
    # campaign, so we cannot bundle them with other mutate operations below.
    hotel_property_asset_resource_name = create_hotel_asset(
        client, customer_id, place_id, hotel_property_asset_set_resource_name
    )

    # It's important to create the below entities in this order because they
    # depend on each other.
    # The below methods create and return mutate operations that we later
    # provide to the GoogleAdsService.Mutate method in order to create the
    # entities in a single request. Since the entities for a Performance Max
    # campaign are closely tied to one-another, it's considered a best practice
    # to create them in a single Mutate request so they all complete
    # successfully or fail entirely, leaving no orphaned entities. See:
    # https://developers.google.com/google-ads/api/docs/mutating/overview.
    campaign_budget_operation = create_campaign_budget_operation(
        client, customer_id
    )
    campaign_operation = create_campaign_operation(
        client, customer_id, hotel_property_asset_set_resource_name
    )
    asset_group_operations = create_asset_group_operations(
        client,
        customer_id,
        hotel_property_asset_resource_name,
        headline_asset_resource_names,
        description_asset_resource_names,
        hotel_asset_suggestion,
    )

    # Issues a mutate request to create everything.
    googleads_service = client.get_service("GoogleAdsService")
    response = googleads_service.mutate(
        customer_id=customer_id,
        mutate_operations=[
            campaign_budget_operation,
            campaign_operation,
            *asset_group_operations,
        ],
    )

    print(
        "Created the following entities for a campaign budget, a campaign, and "
        "an asset group for Performance Max for travel goals:"
    )

    print_response_details(response)


# [START get_hotel_asset_suggestion]
def get_hotel_asset_suggestion(client, customer_id, place_id):
    """Returns hotel asset suggestion from TravelAssetsSuggestionService.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        place_id: a place ID identifying a place in the Google Places database.
    """
    request = client.get_type("SuggestTravelAssetsRequest")
    request.customer_id = customer_id
    # Uses 'en-US' as an example. It can be any language specifications in
    # BCP 47 format.
    request.language_option = "en-US"
    # In this example we only use a single place ID for the purpose of
    # demonstration, but it's possible to append more than one here if needed.
    request.place_ids.append(place_id)
    # Send a request to suggest assets to be created as an asset group for the
    # Performance Max for travel goals campaign.
    travel_asset_suggestion_service = client.get_service(
        "TravelAssetSuggestionService"
    )
    response = travel_asset_suggestion_service.suggest_travel_assets(
        request=request
    )
    print(f"Fetched a hotel asset suggestion for the place ID: '{place_id}'.")

    # Since we sent a single operation in the request, it's guaranteed that
    # there will only be a single item in the response.
    return response.hotel_asset_suggestions[0]
    # [END get_hotel_asset_suggestion]


def create_multiple_text_assets(
    client, customer_id, asset_field_type, hotel_asset_suggestion
):
    """Creates multiple text assets and returns the list of resource names.

    The hotel asset suggestion is used to create a text asset first. If the
    number of created text assets is still fewer than the minimum required
    number of assets of the specified asset field type, adds more text assets to
    fulfill the requirement.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        asset_field_type: the asset field type enum that the new assets will be
            created as.
        hotel_asset_suggestion: the hotel asset suggestion.

    Returns:
        a list of asset resource names.
    """
    # We use the GoogleAdService to create multiple text assets in a single
    # request. First, adds all the text assets of the specified asset field
    # type.
    operations = []
    success_status = client.enums.HotelAssetSuggestionStatusEnum.SUCCESS

    if hotel_asset_suggestion.status == success_status:
        for text_asset in hotel_asset_suggestion.text_assets:
            # If the suggested text asset is not of the type specified, then
            # we skip it and move on to the next text asset.
            if text_asset.asset_field_type != asset_field_type:
                continue

            # If the suggested text asset is of the type specified, then we
            # build a mutate operation that creates a new text asset using
            # the text from the suggestion.
            operation = client.get_type("MutateOperation")
            asset = operation.asset_operation.create
            asset.text_asset.text = text_asset.text
            operations.append(operation)

    # If the current number of operations is still less than the minimum
    # required assets for the asset field type, add more operations using the
    # default texts.
    minimum_required_text_asset_count = MIN_REQUIRED_TEXT_ASSET_COUNTS[
        asset_field_type.name
    ]

    if len(operations) < minimum_required_text_asset_count:
        # Calculate the number of additional operations that need to be created.
        difference = minimum_required_text_asset_count - len(operations)
        # Retrieve the list of default texts for the given asset type.
        default_texts = DEFAULT_TEXT_ASSETS_INFO[asset_field_type.name]
        for i in range(difference):
            operation = client.get_type("MutateOperation")
            asset = operation.asset_operation.create
            asset.text_asset.text = default_texts[i]
            operations.append(operation)

    # Issues a mutate request to add all assets.
    googleads_service = client.get_service("GoogleAdsService")
    response = googleads_service.mutate(
        customer_id=customer_id, mutate_operations=operations
    )

    print(
        "The following assets were created for the asset field type "
        f"'{asset_field_type.name}'"
    )
    print_response_details(response)

    return [
        result.asset_result.resource_name
        for result in response.mutate_operation_responses
    ]


# [START create_hotel_asset_set]
def create_hotel_asset_set(client, customer_id):
    """Creates a hotel property asset set.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.

    Returns:
        the created hotel property asset set's resource name.
    """
    # Creates an asset set operation for a hotel property asset set.
    operation = client.get_type("AssetSetOperation")
    # Creates a hotel property asset set.
    asset_set = operation.create
    asset_set.name = f"My hotel property asset set #{get_printable_datetime()}"
    asset_set.type_ = client.enums.AssetSetTypeEnum.HOTEL_PROPERTY

    # Issues a mutate request to add a hotel asset set.
    asset_set_service = client.get_service("AssetSetService")
    response = asset_set_service.mutate_asset_sets(
        customer_id=customer_id, operations=[operation]
    )
    resource_name = response.results[0].resource_name
    print(f"Created an asset set with resource name: '{resource_name}'")

    return resource_name
    # [END create_hotel_asset_set]


# [START create_hotel_asset]
def create_hotel_asset(client, customer_id, place_id, asset_set_resource_name):
    """Creates a hotel property asset using the specified place ID.

    The place ID must belong to a hotel property. Then, links it to the
    specified asset set.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        place_id: a place ID identifying a place in the Google Places database.
        asset_set_resource_name: an asset set resource name

    Returns:
        the created hotel property asset's resource name.
    """
    # We use the GoogleAdService to create an asset and asset set asset in a
    # single request.
    googleads_service = client.get_service("GoogleAdsService")
    asset_resource_name = googleads_service.asset_path(
        customer_id, ASSET_TEMPORARY_ID
    )

    # Creates a mutate operation for a hotel property asset.
    asset_mutate_operation = client.get_type("MutateOperation")
    # Creates a hotel property asset.
    asset = asset_mutate_operation.asset_operation.create
    asset.resource_name = asset_resource_name
    # Creates a hotel property asset for the place ID.
    asset.hotel_property_asset.place_id = place_id

    # Creates a mutate operation for an asset set asset.
    asset_set_asset_mutate_operation = client.get_type("MutateOperation")
    # Creates an asset set asset.
    asset_set_asset = (
        asset_set_asset_mutate_operation.asset_set_asset_operation.create
    )
    asset_set_asset.asset = asset_resource_name
    asset_set_asset.asset_set = asset_set_resource_name

    # Issues a mutate request to create all entities.
    response = googleads_service.mutate(
        customer_id=customer_id,
        mutate_operations=[
            asset_mutate_operation,
            asset_set_asset_mutate_operation,
        ],
    )
    print("Created the following entities for the hotel asset:")
    print_response_details(response)

    return response.mutate_operation_responses[0].asset_result.resource_name
    # [END create_hotel_asset]


def create_campaign_budget_operation(client, customer_id):
    """Creates a mutate operation that creates a new campaign budget.

    A temporary ID will be assigned to this campaign budget so that it can be
    referenced by other objects being created in the same mutate request.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.

    Returns:
        a MutateOperation message that creates a new campaign budget
    """
    googleads_service = client.get_service("GoogleAdsService")
    # Creates a mutate operation that creates a campaign budget.
    operation = client.get_type("MutateOperation")
    budget = operation.campaign_budget_operation.create
    # Sets a temporary ID in the budget's resource name so it can be referenced
    # by the campaign in later steps.
    budget.resource_name = googleads_service.campaign_budget_path(
        customer_id, BUDGET_TEMPORARY_ID
    )
    budget.name = (
        "Performance Max for travel goals campaign budget "
        f"#{get_printable_datetime()}"
    )
    # The budget period already defaults to DAILY.
    budget.amount_micros = 50000000
    budget.delivery_method = client.enums.BudgetDeliveryMethodEnum.STANDARD
    # A Performance Max campaign cannot use a shared campaign budget.
    budget.explicitly_shared = False

    return operation


# [START create_campaign]
def create_campaign_operation(
    client, customer_id, hotel_property_asset_set_resource_name
):
    """Creates a mutate operation that creates a new Performance Max campaign.

    Links the specified hotel property asset set to this campaign.

    A temporary ID will be assigned to this campaign budget so that it can be
    referenced by other objects being created in the same mutate request.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        hotel_property_asset_set_resource_name: the resource name for a hotel
            property asset set.

    Returns:
        a MutateOperation message that creates a new Performance Max campaign.
    """
    googleads_service = client.get_service("GoogleAdsService")
    # Creates a mutate operation that creates a campaign.
    operation = client.get_type("MutateOperation")
    campaign = operation.campaign_operation.create
    campaign.name = (
        f"Performance Max for travel goals campaign #{get_printable_datetime}"
    )
    # Assigns the resource name with a temporary ID.
    campaign.resource_name = googleads_service.campaign_path(
        customer_id, CAMPAIGN_TEMPORARY_ID
    )
    # Sets the budget using the given budget resource name.
    campaign.campaign_budget = googleads_service.campaign_budget_path(
        customer_id, BUDGET_TEMPORARY_ID
    )
    # The campaign is the only entity in the mutate request that should have its
    # status set.
    # Recommendation: Set the campaign to PAUSED when creating it to prevent
    # the ads from immediately serving.
    campaign.status = client.enums.CampaignStatusEnum.PAUSED
    # Performance Max campaigns have an advertising_channel_type of
    # PERFORMANCE_MAX. The advertising_channel_sub_type should not be set.
    campaign.advertising_channel_type = (
        client.enums.AdvertisingChannelTypeEnum.PERFORMANCE_MAX
    )
    # To create a Performance Max for travel goals campaign, you need to set
    # the `hotel_property_asset_set` field.
    campaign.hotel_property_asset_set = hotel_property_asset_set_resource_name
    # Bidding strategy must be set directly on the campaign.
    # Setting a portfolio bidding strategy by resource name is not supported.
    # Max Conversion and Maximize Conversion Value are the only strategies
    # supported for Performance Max campaigns.
    # An optional ROAS (Return on Advertising Spend) can be set for
    # maximize_conversion_value. The ROAS value must be specified as a ratio in
    # the API. It is calculated by dividing "total value" by "total spend".
    # For more information on Maximize Conversion Value, see the support
    # article: https://support.google.com/google-ads/answer/7684216.
    # A target_roas of 3.5 corresponds to a 350% return on ad spend.
    campaign.maximize_conversion_value.target_roas = 3.5

    return operation
    # [END create_campaign]


def create_asset_group_operations(
    client,
    customer_id,
    hotel_property_asset_resource_name,
    headline_asset_resource_names,
    description_asset_resource_names,
    hotel_asset_suggestion,
):
    """Creates a list of mutate operations that create a new asset group.

    The asset group is composed of suggested assets. In case the number of
    suggested assets is not enough for the requirements, it will create more
    assets to meet the requirement.

    For the list of required assets for a Performance Max campaign, see
    https://developers.google.com/google-ads/api/docs/performance-max/assets.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        hotel_property_asset_resource_name: the hotel property asset resource
            name that will be used to create an asset group.
        headline_asset_resource_names: a list of headline asset resource names.
        description_asset_resource_names: a list of description asset resource
            names.
        hotel_asset_suggestion: the hotel asset suggestion.

    Returns:
        a list of mutate operations that create the asset group.
    """
    global next_temp_id
    googleads_service = client.get_service("GoogleAdsService")
    operations = []

    # Creates a new mutate operation that creates an asset group using suggested
    # information when available.
    success_status = client.enums.HotelAssetSuggestionStatusEnum.SUCCESS
    if hotel_asset_suggestion.status == success_status:
        asset_group_name = hotel_asset_suggestion.hotel_name
        asset_group_final_urls = [hotel_asset_suggestion.final_url]
    else:
        asset_group_name = (
            "Performance Max for travel goals asset group "
            f"#{get_printable_datetime()}"
        )
        asset_group_final_urls = ["http://www.example.com"]

    asset_group_resource_name = googleads_service.asset_group_path(
        customer_id, ASSET_GROUP_TEMPORARY_ID
    )
    asset_group_mutate_operation = client.get_type("MutateOperation")
    asset_group = asset_group_mutate_operation.asset_group_operation.create
    asset_group.resource_name = asset_group_resource_name
    asset_group.name = asset_group_name
    asset_group.campaign = googleads_service.campaign_path(
        customer_id, CAMPAIGN_TEMPORARY_ID
    )
    asset_group.final_urls = asset_group_final_urls
    asset_group.status = client.enums.AssetGroupStatusEnum.PAUSED
    # Append the asset group operation to the list of operations.
    operations.append(asset_group_mutate_operation)

    # An asset group is linked to an asset by creating a new asset group asset
    # and providing:
    # -  the resource name of the asset group
    # -  the resource name of the asset
    # -  the field_type of the asset in this asset group

    # To learn more about asset groups, see
    # https://developers.google.com/google-ads/api/docs/performance-max/asset-groups.

    # Headline and description assets were created at the first step of this
    # example. So, we just need to link them with the created asset group.

    # Links the headline assets to the asset group.
    for resource_name in headline_asset_resource_names:
        headline_operation = client.get_type("MutateOperation")
        asset_group_asset = (
            headline_operation.asset_group_asset_operation.create
        )
        asset_group_asset.asset = resource_name
        asset_group_asset.asset_group = asset_group_resource_name
        asset_group_asset.field_type = client.enums.AssetFieldTypeEnum.HEADLINE
        operations.append(headline_operation)

    # Links the description assets to the asset group.
    for resource_name in description_asset_resource_names:
        description_operation = client.get_type("MutateOperation")
        asset_group_asset = (
            description_operation.asset_group_asset_operation.create
        )
        asset_group_asset.asset = resource_name
        asset_group_asset.asset_group = asset_group_resource_name
        asset_group_asset.field_type = (
            client.enums.AssetFieldTypeEnum.DESCRIPTION
        )
        operations.append(description_operation)

    # [START link_hotel_asset]
    # Link the previously created hotel property asset to the asset group. If
    # there are multiple assets, these steps to create a new operation need to
    # be performed for each asset.
    asset_group_asset_mutate_operation = client.get_type("MutateOperation")
    asset_group_asset = (
        asset_group_asset_mutate_operation.asset_group_asset_operation.create
    )
    asset_group_asset.asset = hotel_property_asset_resource_name
    asset_group_asset.asset_group = asset_group_resource_name
    asset_group_asset.field_type = (
        client.enums.AssetFieldTypeEnum.HOTEL_PROPERTY
    )
    operations.append(asset_group_asset_mutate_operation)
    # [END link_hotel_asset]

    # Creates the rest of required text assets and link them to the asset group.
    operations.extend(
        create_text_assets_for_asset_group(
            client, customer_id, hotel_asset_suggestion
        )
    )

    # Creates the image assets and link them to the asset group. Some optional
    # image assets suggested by the TravelAssetSuggestionService might be
    # created too.
    operations.extend(
        create_image_assets_for_asset_group(
            client, customer_id, hotel_asset_suggestion
        )
    )

    if hotel_asset_suggestion.status == success_status:
        # Creates a new mutate operation for a suggested call-to-action asset
        # and link it to the asset group.
        asset_mutate_operation = client.get_type("MutateOperation")
        asset = asset_mutate_operation.asset_operation.create
        asset.resource_name = googleads_service.asset_path(
            customer_id, next_temp_id
        )
        asset.name = (
            f"Suggested call-to-action asset #{get_printable_datetime()}"
        )
        asset.call_to_action_asset.call_to_action = (
            hotel_asset_suggestion.call_to_action
        )

        # Creates a new mutate operation for a call-to-action asset group.
        asset_group_asset_mutate_operation = client.get_type("MutateOperation")
        asset_group_asset = (
            asset_group_asset_mutate_operation.asset_group_asset_operation.create
        )
        asset_group_asset.asset = googleads_service.asset_path(
            customer_id, next_temp_id
        )
        asset_group_asset.asset_group = asset_group_resource_name
        asset_group_asset.field_type = (
            client.enums.AssetFieldTypeEnum.CALL_TO_ACTION_SELECTION
        )

        next_temp_id -= 1

    return operations


def create_text_assets_for_asset_group(
    client, customer_id, hotel_asset_suggestion
):
    """Creates text assets for an asset group using the given hotel text assets.

    It adds more text assets to fulfill the requirements if the suggested hotel
    text assets are not enough.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        hotel_asset_suggestion: the hotel asset suggestion.

    Returns:
        a list of mutate operations that create text assets.
    """
    operations = []

    # Creates mutate operations for the suggested text assets except for
    # headlines and descriptions, which were created previously.
    required_text_asset_counts = {
        key: 0 for key in MIN_REQUIRED_TEXT_ASSET_COUNTS.keys()
    }
    success_status = client.enums.HotelAssetSuggestionStatusEnum.SUCCESS
    if hotel_asset_suggestion.status == success_status:
        for text_asset in hotel_asset_suggestion.text_assets:
            text = text_asset.text
            asset_field_type = text_asset.asset_field_type

            if asset_field_type.name in ("HEADLINE", "DESCRIPTION"):
                # Headlines and descriptions were already created at the first
                # step of this code example
                continue

            print(
                f"A test asset with text {text} is suggested for the asset "
                f"field type `{asset_field_type.name}`"
            )

            operations.extend(
                create_text_asset_and_asset_group_asset_operations(
                    client, customer_id, text, asset_field_type
                )
            )

            required_text_asset_counts[asset_field_type.name] += 1

    # Adds more text assets to fulfill the requirements.
    for field_type_name, min_count in MIN_REQUIRED_TEXT_ASSET_COUNTS.items():
        if field_type_name in ("HEADLINE", "DESCRIPTION"):
            # Headlines and descriptions were already created at the first step
            # of this code example.
            continue

        difference = min_count - required_text_asset_counts[field_type_name]
        if difference > 0:
            for i in range(difference):
                default_text = DEFAULT_TEXT_ASSETS_INFO[field_type_name][i]
                field_type_enum = client.enums.AssetFieldTypeEnum[
                    field_type_name
                ]

                print(
                    f"A default text {default_text} is used to create a "
                    f"text asset for the asset field type {field_type_name}"
                )

                operations.extend(
                    create_text_asset_and_asset_group_asset_operations(
                        client, customer_id, default_text, field_type_enum
                    )
                )

    return operations


def create_text_asset_and_asset_group_asset_operations(
    client, customer_id, text, field_type_enum
):
    """Creates a list of mutate operations that create a new linked text asset.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        text: the text of an asset to be created.
        field_type_enum: the field type enum of a new asset in the asset group
            asset.

    Returns:
        a list of mutate operations that create a new linked text asset.
    """
    global next_temp_id
    googleads_service = client.get_service("GoogleAdsService")
    operations = []

    # Creates a new mutate operation that creates a text asset.
    asset_mutate_operation = client.get_type("MutateOperation")
    asset = asset_mutate_operation.asset_operation.create
    asset.resource_name = googleads_service.asset_path(
        customer_id, next_temp_id
    )
    asset.text_asset.text = text
    operations.append(asset_mutate_operation)

    # Creates an asset group asset operation to link the asset to the asset
    # group.
    asset_group_asset_mutate_operation = client.get_type("MutateOperation")
    asset_group_asset = (
        asset_group_asset_mutate_operation.asset_group_asset_operation.create
    )
    asset_group_asset.asset = googleads_service.asset_path(
        customer_id, next_temp_id
    )
    asset_group_asset.asset_group = googleads_service.asset_group_path(
        customer_id, ASSET_GROUP_TEMPORARY_ID
    )
    asset_group_asset.field_type = field_type_enum
    operations.append(asset_group_asset_mutate_operation)

    next_temp_id -= 1

    return operations


def create_image_assets_for_asset_group(
    client, customer_id, hotel_asset_suggestion
):
    """Creates image assets for an asset group with the given hotel suggestions.

    It adds more image assets to fulfill the requirements if the suggested hotel
    image assets are not enough.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        hotel_asset_suggestion: the hotel asset suggestion.

    Returns:
        a list of mutate operations that create image assets.
    """
    operations = []

    # Creates mutate operations for the suggested image assets.
    required_image_asset_counts = {
        key: 0 for key in MIN_REQUIRED_IMAGE_ASSET_COUNTS.keys()
    }
    for image_asset in hotel_asset_suggestion.image_assets:
        url = image_asset.uri
        field_type_enum = image_asset.asset_field_type
        name = f"Suggested image asset #{get_printable_datetime()}"

        print(
            f"An image asset with URL '{url}' is suggested for the asset field "
            f"type '{field_type_enum.name}'"
        )

        operations.extend(
            create_image_asset_and_image_asset_group_asset_operations(
                client, customer_id, url, field_type_enum, name
            )
        )

        # Keeps track of only required image assets. The
        # TravelAssetSuggestionService may sometimes suggest optional image
        # assets.
        if field_type_enum.name in required_image_asset_counts:
            required_image_asset_counts[field_type_enum.name] += 1

    # Adds more image assets to fulfill the requirements.
    for field_type_name, min_count in MIN_REQUIRED_IMAGE_ASSET_COUNTS.items():
        difference = min_count - required_image_asset_counts[field_type_name]
        if difference > 0:
            for i in range(difference):
                default_url = DEFAULT_IMAGE_ASSETS_INFO[field_type_name][i]
                name = f"{field_type_name.lower()} {get_printable_datetime()}"
                field_type_enum = client.enums.AssetFieldTypeEnum[
                    field_type_name
                ]

                print(
                    f"A default image URL {default_url} is used to create an "
                    f"image asset for the asset field type {field_type_name}"
                )

                operations.extend(
                    create_image_asset_and_image_asset_group_asset_operations(
                        client, customer_id, default_url, field_type_enum, name
                    )
                )

    return operations


def create_image_asset_and_image_asset_group_asset_operations(
    client, customer_id, url, field_type_enum, asset_name
):
    """Creates a list of mutate operations that create a new linked image asset.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        url: the URL of the image to be retrieved and put into an asset.
        field_type_enum: the field type enum of the new asset in the asset group
            asset.
        asset_name: the asset name.

    Returns:
        a list of mutate operations that create a new linked image asset.
    """
    global next_temp_id
    googleads_service = client.get_service("GoogleAdsService")
    operations = []

    # Creates a new mutate operation that creates an image asset.
    asset_mutate_operation = client.get_type("MutateOperation")
    asset = asset_mutate_operation.asset_operation.create
    asset.resource_name = googleads_service.asset_path(
        customer_id, next_temp_id
    )
    # Provide a unique friendly name to identify your asset. When there is an
    # existing image asset with the same content but a different name, the new
    # name will be dropped silently.
    asset.name = asset_name
    asset.image_asset.data = get_image_bytes_from_url(url)
    operations.append(asset_mutate_operation)

    # Creates an asset group asset operation to link the asset to the asset
    # group.
    asset_group_asset_mutate_operation = client.get_type("MutateOperation")
    asset_group_asset = (
        asset_group_asset_mutate_operation.asset_group_asset_operation.create
    )
    asset_group_asset.asset = googleads_service.asset_path(
        customer_id, next_temp_id
    )
    asset_group_asset.asset_group = googleads_service.asset_group_path(
        customer_id, ASSET_GROUP_TEMPORARY_ID
    )
    asset_group_asset.field_type = field_type_enum
    operations.append(asset_group_asset_mutate_operation)

    next_temp_id -= 1

    return operations


def print_response_details(mutate_response):
    """Prints the details of a MutateGoogleAdsResponse message.

    Parses the "response" oneof field name and uses it to extract the new
    entity's name and resource name.

    Args:
        mutate_response: a MutateGoogleAdsResponse message.
    """
    for result in mutate_response.mutate_operation_responses:
        resource_type = "unrecognized"
        resource_name = "not found"

        if "asset_result" in result:
            resource_type = "Asset"
            resource_name = result.asset_result.resource_name
        elif "asset_set_asset_result" in result:
            resource_type = "AssetSetAsset"
            resource_name = result.asset_set_asset_result.resource_name
        elif "campaign_budget_result" in result:
            resource_type = "CampaignBudget"
            resource_name = result.campaign_budget_result.resource_name
        elif "campaign_result" in result:
            resource_type = "Campaign"
            resource_name = result.campaign_result.resource_name
        elif "asset_group_result" in result:
            resource_type = "AssetGroup"
            resource_name = result.asset_group_result.resource_name
        elif "asset_group_asset_result" in result:
            resource_type = "AssetGroupAsset"
            resource_name = result.asset_group_asset_result.resource_name

        print(
            f"Created a(n) {resource_type} with "
            f"resource_name: '{resource_name}'."
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=("Creates a Performance Max for travel goals campaign.")
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
        "-p",
        "--place_id",
        type=str,
        required=True,
        help=(
            "Sets a place ID that uniquely identifies a place in the Google "
            "Places database. The provided place ID must belong to a hotel "
            "property. To learn more, see: "
            "https://developers.google.com/places/web-service/place-id "
        ),
    )

    args = parser.parse_args()

    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v20")

    try:
        main(googleads_client, args.customer_id, args.place_id)
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
