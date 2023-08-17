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
"""
This example shows how to create a complete Responsive Search ad.

Includes creation of: budget, campaign, ad group, ad group ad,
keywords, geo targeting, and image extensions.

More details on Responsive Search ads can be found here:
https://support.google.com/google-ads/answer/7684791
"""

import argparse
import sys
import uuid
import requests

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


# Keywords from user.
_KEYWORD_TEXT_EXACT_1 = "example of exact match"
_KEYWORD_TEXT_PHRASE_1 = "example of phrase match"
_KEYWORD_TEXT_BROAD_1 = "example of broad match"

# Geo targeting from user.
_GEO_LOCATION_1 = "Buenos aires"
_GEO_LOCATION_2 = "San Isidro"
_GEO_LOCATION_3 = "Mar del Plata"

# _LOCALE and _COUNTRY_CODE are used for geo targeting.
# _LOCALE is using ISO 639-1 format. If an invalid _LOCALE is given,
# 'es' is used by default.
_LOCALE = "es"

# A list of country codes can be referenced here:
# https://developers.google.com/google-ads/api/reference/data/geotargets
_COUNTRY_CODE = "AR"


def create_ad_text_asset(client, text, pinned_field=None):
    """Create an AdTextAsset.
    Args:
        client: an initialized GoogleAdsClient instance.
        text: text for headlines and descriptions.
        pinned_field: to pin a text asset so it always shows in the ad.

    Returns:
        An ad text asset.
    """
    ad_text_asset = client.get_type("AdTextAsset")
    ad_text_asset.text = text
    if pinned_field:
        ad_text_asset.pinned_field = pinned_field
    return ad_text_asset


def main(client, customer_id, omit_image_extensions):
    """
    The main method that creates all necessary entities for the example.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.

    Returns:
        A responsive search ad with all settings required to run campaign.
    """
    # Create a budget, which can be shared by multiple campaigns.
    campaign_budget = create_campaign_budget(client, customer_id)

    campaign_resource_name = create_campaign(
        client, customer_id, campaign_budget
    )

    ad_group_resource_name = create_ad_group(
        client, customer_id, campaign_resource_name
    )

    create_ad_group_ad(client, customer_id, ad_group_resource_name)

    add_keywords(client, customer_id, ad_group_resource_name)

    add_geo_targeting(client, customer_id, campaign_resource_name)

    # This is optional but recommended for RSA.
    # To add image extensions, the account has to follow these requirements:
    # https://support.google.com/google-ads/answer/9566341
    # If the account meets the requirements, set below variable to True.
    if omit_image_extensions:
        add_images(client, customer_id, campaign_resource_name)


def create_campaign_budget(client, customer_id):
    """Creates campaign budget resource.

    Args:
      client: an initialized GoogleAdsClient instance.
      customer_id: a client customer ID.

    Returns:
      Campaign budget resource name.
    """
    # Create a budget, which can be shared by multiple campaigns.
    campaign_budget_service = client.get_service("CampaignBudgetService")
    campaign_budget_operation = client.get_type("CampaignBudgetOperation")
    campaign_budget = campaign_budget_operation.create
    campaign_budget.name = f"Campaign budget {uuid.uuid4()}"
    campaign_budget.delivery_method = (
        client.enums.BudgetDeliveryMethodEnum.STANDARD
    )
    campaign_budget.amount_micros = 500000

    # Add budget.
    campaign_budget_response = campaign_budget_service.mutate_campaign_budgets(
        customer_id=customer_id, operations=[campaign_budget_operation]
    )

    return campaign_budget_response.results[0].resource_name


def create_campaign(client, customer_id, campaign_budget):
    """Creates campaign resource.

    Args:
      client: an initialized GoogleAdsClient instance.
      customer_id: a client customer ID.
      campaign_budget: a budget resource name.

    Returns:
      Campaign resource name.
    """
    campaign_service = client.get_service("CampaignService")
    campaign_operation = client.get_type("CampaignOperation")
    campaign = campaign_operation.create
    campaign.name = f"Testing RSA via API {uuid.uuid4()}"
    campaign.advertising_channel_type = (
        client.enums.AdvertisingChannelTypeEnum.SEARCH
    )

    # Recommendation: Set the campaign to PAUSED when creating it to prevent
    # the ads from immediately serving. Set to ENABLED once you've added
    # targeting and the ads are ready to serve.
    campaign.status = client.enums.CampaignStatusEnum.PAUSED

    # Set the bidding strategy and budget.
    # The bidding strategy for Maximize Clicks is TargetSpend.
    # The target_spend_micros is deprecated so don't put any value.
    # See other bidding strategies you can select in the link below.
    # https://developers.google.com/google-ads/api/reference/rpc/v11/Campaign#campaign_bidding_strategy
    campaign.target_spend.target_spend_micros = 0
    campaign.campaign_budget = campaign_budget

    # Set the campaign network options.
    campaign.network_settings.target_google_search = True
    campaign.network_settings.target_search_network = True
    campaign.network_settings.target_partner_search_network = False
    # Enable Display Expansion on Search campaigns. For more details see:
    # https://support.google.com/google-ads/answer/7193800
    campaign.network_settings.target_content_network = True

    # # Optional: Set the start date.
    # start_time = datetime.date.today() + datetime.timedelta(days=1)
    # campaign.start_date = datetime.date.strftime(start_time, _DATE_FORMAT)

    # # Optional: Set the end date.
    # end_time = start_time + datetime.timedelta(weeks=4)
    # campaign.end_date = datetime.date.strftime(end_time, _DATE_FORMAT)

    # Add the campaign.
    campaign_response = campaign_service.mutate_campaigns(
        customer_id=customer_id, operations=[campaign_operation]
    )
    resource_name = campaign_response.results[0].resource_name
    print(f"Created campaign {resource_name}.")
    return resource_name


def create_ad_group(client, customer_id, campaign_resource_name):
    """Creates ad group.

    Args:
      client: an initialized GoogleAdsClient instance.
      customer_id: a client customer ID.
      campaign_resource_name: a campaign resource name.

    Returns:
      Ad group ID.
    """
    ad_group_service = client.get_service("AdGroupService")

    ad_group_operation = client.get_type("AdGroupOperation")
    ad_group = ad_group_operation.create
    ad_group.name = f"Testing RSA via API {uuid.uuid4()}"
    ad_group.status = client.enums.AdGroupStatusEnum.ENABLED
    ad_group.campaign = campaign_resource_name
    ad_group.type_ = client.enums.AdGroupTypeEnum.SEARCH_STANDARD

    # If you want to set up a max CPC bid uncomment line below.
    # ad_group.cpc_bid_micros = 10000000

    # Add the ad group.
    ad_group_response = ad_group_service.mutate_ad_groups(
        customer_id=customer_id, operations=[ad_group_operation]
    )
    ad_group_resource_name = ad_group_response.results[0].resource_name
    print(f"Created ad group {ad_group_resource_name}.")
    return ad_group_resource_name


def create_ad_group_ad(client, customer_id, ad_group_resource_name):
    """Creates ad group ad.

    Args:
      client: an initialized GoogleAdsClient instance.
      customer_id: a client customer ID.
      ad_group_resource_name: an ad group resource name.

    Returns:
      Ad group ad resource name.
    """
    ad_group_ad_service = client.get_service("AdGroupAdService")

    ad_group_ad_operation = client.get_type("AdGroupAdOperation")
    ad_group_ad = ad_group_ad_operation.create
    ad_group_ad.status = client.enums.AdGroupAdStatusEnum.ENABLED
    ad_group_ad.ad_group = ad_group_resource_name

    # Set responsive search ad info.
    # https://developers.google.com/google-ads/api/reference/rpc/v11/ResponsiveSearchAdInfo

    # The list of possible final URLs after all cross-domain redirects for the ad.
    ad_group_ad.ad.final_urls.append("https://www.example.com/")

    # Set a pinning to always choose this asset for HEADLINE_1. Pinning is
    # optional; if no pinning is set, then headlines and descriptions will be
    # rotated and the ones that perform best will be used more often.

    # Headline 1
    served_asset_enum = client.enums.ServedAssetFieldTypeEnum.HEADLINE_1
    pinned_headline = create_ad_text_asset(
        client, "Headline 1 testing", served_asset_enum
    )

    # Headline 2 and 3
    ad_group_ad.ad.responsive_search_ad.headlines.extend(
        [
            pinned_headline,
            create_ad_text_asset(client, "Headline 2 testing"),
            create_ad_text_asset(client, "Headline 3 testing"),
        ]
    )

    # Description 1 and 2
    ad_group_ad.ad.responsive_search_ad.descriptions.extend(
        [
            create_ad_text_asset(client, "Desc 1 testing"),
            create_ad_text_asset(client, "Desc 2 testing"),
        ]
    )

    # Paths
    # First and second part of text that can be appended to the URL in the ad.
    # If you use the examples below, the ad will show
    # https://www.example.com/all-inclusive/deals
    ad_group_ad.ad.responsive_search_ad.path1 = "all-inclusive"
    ad_group_ad.ad.responsive_search_ad.path2 = "deals"

    # Send a request to the server to add a responsive search ad.
    ad_group_ad_response = ad_group_ad_service.mutate_ad_group_ads(
        customer_id=customer_id, operations=[ad_group_ad_operation]
    )

    for result in ad_group_ad_response.results:
        print(
            f"Created responsive search ad with resource name "
            f'"{result.resource_name}".'
        )


def add_keywords(client, customer_id, ad_group_resource_name):
    """Creates keywords.

    Creates 3 keyword match types: EXACT, PHRASE, and BROAD.

    EXACT: ads may show on searches that ARE the same meaning as your keyword.
    PHRASE: ads may show on searches that INCLUDE the meaning of your keyword.
    BROAD: ads may show on searches that RELATE to your keyword.
    For smart bidding, BROAD is the recommended one.

    Args:
      client: an initialized GoogleAdsClient instance.
      customer_id: a client customer ID.
      ad_group_resource_name: an ad group resource name.
    """
    ad_group_criterion_service = client.get_service("AdGroupCriterionService")

    operations = []
    # Create keyword 1.
    ad_group_criterion_operation = client.get_type("AdGroupCriterionOperation")
    ad_group_criterion = ad_group_criterion_operation.create
    ad_group_criterion.ad_group = ad_group_resource_name
    ad_group_criterion.status = client.enums.AdGroupCriterionStatusEnum.ENABLED
    ad_group_criterion.keyword.text = _KEYWORD_TEXT_EXACT_1
    ad_group_criterion.keyword.match_type = (
        client.enums.KeywordMatchTypeEnum.EXACT
    )

    # Uncomment the below line if you want to change this keyword to a negative target.
    # ad_group_criterion.negative = True

    # Optional repeated field
    # ad_group_criterion.final_urls.append('https://www.example.com')

    # Add operation
    operations.append(ad_group_criterion_operation)

    # Create keyword 2.
    ad_group_criterion_operation = client.get_type("AdGroupCriterionOperation")
    ad_group_criterion = ad_group_criterion_operation.create
    ad_group_criterion.ad_group = ad_group_resource_name
    ad_group_criterion.status = client.enums.AdGroupCriterionStatusEnum.ENABLED
    ad_group_criterion.keyword.text = _KEYWORD_TEXT_PHRASE_1
    ad_group_criterion.keyword.match_type = (
        client.enums.KeywordMatchTypeEnum.PHRASE
    )

    # Uncomment the below line if you want to change this keyword to a negative target.
    # ad_group_criterion.negative = True

    # Optional repeated field
    # ad_group_criterion.final_urls.append('https://www.example.com')

    # Add operation
    operations.append(ad_group_criterion_operation)

    # Create keyword 3.
    ad_group_criterion_operation = client.get_type("AdGroupCriterionOperation")
    ad_group_criterion = ad_group_criterion_operation.create
    ad_group_criterion.ad_group = ad_group_resource_name
    ad_group_criterion.status = client.enums.AdGroupCriterionStatusEnum.ENABLED
    ad_group_criterion.keyword.text = _KEYWORD_TEXT_BROAD_1
    ad_group_criterion.keyword.match_type = (
        client.enums.KeywordMatchTypeEnum.BROAD
    )

    # Uncomment the below line if you want to change this keyword to a negative target.
    # ad_group_criterion.negative = True

    # Optional repeated field
    # ad_group_criterion.final_urls.append('https://www.example.com')

    # Add operation
    operations.append(ad_group_criterion_operation)

    # Set all operations together.
    campaign_criterion_operations = operations

    # Add keywords
    ad_group_criterion_response = ad_group_criterion_service.mutate_ad_group_criteria(
        customer_id=customer_id, operations=[*campaign_criterion_operations],
    )
    for result in ad_group_criterion_response.results:
        print("Created keyword " f"{result.resource_name}.")


def add_geo_targeting(client, customer_id, campaign_resource_name):
    """Creates geo targets.

    Args:
      client: an initialized GoogleAdsClient instance.
      customer_id: a client customer ID.
      campaign_resource_name: an campaign resource name.

    Returns:
      Geo targets.
    """
    geo_target_constant_service = client.get_service("GeoTargetConstantService")

    # Search by location names from
    # GeoTargetConstantService.suggest_geo_target_constants() and directly
    # apply GeoTargetConstant.resource_name.
    gtc_request = client.get_type("SuggestGeoTargetConstantsRequest")
    gtc_request.locale = _LOCALE
    gtc_request.country_code = _COUNTRY_CODE

    # The location names to get suggested geo target constants.
    gtc_request.location_names.names.extend(
        [_GEO_LOCATION_1, _GEO_LOCATION_2, _GEO_LOCATION_3]
    )

    results = geo_target_constant_service.suggest_geo_target_constants(
        gtc_request
    )

    operations = []
    for suggestion in results.geo_target_constant_suggestions:
        geo_target_constant = suggestion.geo_target_constant
        print(
            f"{geo_target_constant.resource_name} "
            f"({geo_target_constant.name}, "
            f"{geo_target_constant.country_code}, "
            f"{geo_target_constant.target_type}, "
            f"{geo_target_constant.status.name}) "
            f"is found in _LOCALE ({suggestion.locale}) "
            f"with reach ({suggestion.reach}) "
            f"from search term ({suggestion.search_term})."
        )
        # Create the campaign criterion for location targeting.
        campaign_criterion_operation = client.get_type(
            "CampaignCriterionOperation"
        )
        campaign_criterion = campaign_criterion_operation.create
        campaign_criterion.campaign = campaign_resource_name
        campaign_criterion.location.geo_target_constant = (
            geo_target_constant.resource_name
        )
        operations.append(campaign_criterion_operation)

    campaign_criterion_service = client.get_service("CampaignCriterionService")
    campaign_criterion_response = campaign_criterion_service.mutate_campaign_criteria(
        customer_id=customer_id, operations=[*operations]
    )

    for result in campaign_criterion_response.results:
        print(f'Added campaign criterion "{result.resource_name}".')


def add_images(client, customer_id, campaign_resource_name):
    # Step 6.1 - Add Image Asset.

    # Download PNG image from URL.
    url = "https://gaagl.page.link/bjYi"
    image_content = requests.get(url).content

    asset_service = client.get_service("AssetService")
    asset_operation = client.get_type("AssetOperation")
    asset = asset_operation.create
    asset.type_ = client.enums.AssetTypeEnum.IMAGE

    # Data field is the raw bytes data of an image.
    asset.image_asset.data = image_content
    asset.image_asset.file_size = len(image_content)

    # MIME type of the image (IMAGE_JPEG, IMAGE_PNG, etc.).
    # See more types on the link below.
    # https://developers.google.com/google-ads/api/reference/rpc/v11/MimeTypeEnum.MimeType
    asset.image_asset.mime_type = client.enums.MimeTypeEnum.IMAGE_PNG
    # Use your favorite image library to determine dimensions
    asset.image_asset.full_size.height_pixels = 1200
    asset.image_asset.full_size.width_pixels = 1200
    asset.image_asset.full_size.url = url
    # Provide a unique friendly name to identify your asset.
    # When there is an existing image asset with the same content but a different
    # name, the new name will be dropped silently.
    asset.name = f"Testing Image via API {uuid.uuid4()}"

    mutate_asset_response = asset_service.mutate_assets(
        customer_id=customer_id, operations=[asset_operation]
    )
    print("Uploaded file(s):")
    for row in mutate_asset_response.results:
        print(f"\tResource name: {row.resource_name}")

    image_asset_resource_name = mutate_asset_response.results[0].resource_name

    # Step 6.2 - Create Image Extension
    extension_feed_item_service = client.get_service("ExtensionFeedItemService")
    extension_feed_item_operation = client.get_type(
        "ExtensionFeedItemOperation"
    )
    extension_feed_item = extension_feed_item_operation.create
    extension_feed_item.image_feed_item.image_asset = image_asset_resource_name

    extension_feed_response = extension_feed_item_service.mutate_extension_feed_items(
        customer_id=customer_id, operations=[extension_feed_item_operation]
    )
    image_resource_name = extension_feed_response.results[0].resource_name

    print(
        "Created an image extension with resource name: "
        f"'{image_resource_name}'"
    )

    # Step 6.3 - Link Image Extension to RSA
    campaign_extension_setting_service = client.get_service(
        "CampaignExtensionSettingService"
    )
    campaign_extension_setting_operation = client.get_type(
        "CampaignExtensionSettingOperation"
    )
    ces = campaign_extension_setting_operation.create
    ces.campaign = campaign_resource_name
    ces.extension_type = client.enums.ExtensionTypeEnum.IMAGE
    ces.extension_feed_items.append(image_resource_name)

    campaign_extension_response = campaign_extension_setting_service.mutate_campaign_extension_settings(
        customer_id=customer_id,
        operations=[campaign_extension_setting_operation],
    )

    print(
        "Created a campaign extension setting with resource name: "
        f"'{campaign_extension_response.results[0].resource_name}'"
    )


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v14")

    parser = argparse.ArgumentParser(
        description=("Creates a Responsive Search Ad for specified customer.")
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
        "-o",
        "--omit_image_extensions",
        type=bool,
        default=False,
        help="Whether or not the campaign will use image extensions.",
    )

    args = parser.parse_args()

    try:
        main(googleads_client, args.customer_id)
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
