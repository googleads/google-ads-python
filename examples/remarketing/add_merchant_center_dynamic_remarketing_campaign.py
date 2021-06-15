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
"""Creates a campaign associated with an existing Merchant Center account.

Creates a shopping campaign, related ad group and dynamic display ad, and
targets a user list for remarketing purposes.
"""


import argparse
import requests
import sys
from uuid import uuid4

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


def main(
    client,
    customer_id,
    merchant_center_account_id,
    campaign_budget_id,
    user_list_id,
):
    """Creates a campaign associated with an existing Merchant Center account.

    Args:
        client: An initialized GoogleAds client.
        customer_id: The Google Ads customer ID.
        merchant_center_account_id: The target Merchant Center account ID.
        campaign_budget_id: The ID of the campaign budget to utilize.
        user_list_id: The ID of the user list to target for remarketing.
    """
    # Create a shopping campaign associated with a given Merchant Center
    # account.
    campaign_resource_name = _create_campaign(
        client, customer_id, merchant_center_account_id, campaign_budget_id
    )

    # Create an ad group for the campaign.
    ad_group_resource_name = _create_ad_group(
        client, customer_id, campaign_resource_name
    )

    # Create a dynamic display ad in the ad group.
    _create_ad(client, customer_id, ad_group_resource_name)

    # Target a specific user list for remarketing.
    _attach_user_list(client, customer_id, ad_group_resource_name, user_list_id)


# [START add_merchant_center_dynamic_remarketing_campaign_2]
def _create_campaign(
    client, customer_id, merchant_center_account_id, campaign_budget_id
):
    """Creates a campaign linked to a Merchant Center product feed.

    Args:
        client: An initialized GoogleAds client.
        customer_id: The Google Ads customer ID.
        merchant_center_account_id: The target Merchant Center account ID.
        campaign_budget_id: The ID of the campaign budget to utilize.
    Returns:
        The string resource name of the newly created campaign.
    """
    # Gets the CampaignService client.
    campaign_service = client.get_service("CampaignService")

    # Creates a campaign operation and configures the new campaign.
    campaign_operation = client.get_type("CampaignOperation")
    campaign = campaign_operation.create
    campaign.name = f"Shopping campaign #{uuid4()}"
    # Configures the settings for the shopping campaign.
    campaign.shopping_setting.campaign_priority = 0
    # This connects the campaign to the Merchant Center account.
    campaign.shopping_setting.merchant_id = merchant_center_account_id
    # Display Network campaigns do not support partition by country. The only
    # supported value is "ZZ". This signals that products from all countries are
    # available in the campaign. The actual products which serve are based on
    # the products tagged in the user list entry.
    campaign.shopping_setting.sales_country = "ZZ"
    campaign.shopping_setting.enable_local = True
    # Dynamic remarketing campaigns are only available on the Google Display
    # Network.
    campaign.advertising_channel_type = client.get_type(
        "AdvertisingChannelTypeEnum"
    ).AdvertisingChannelType.DISPLAY
    campaign.status = client.get_type(
        "CampaignStatusEnum"
    ).CampaignStatus.PAUSED
    campaign.campaign_budget = client.get_service(
        "CampaignBudgetService"
    ).campaign_budget_path(customer_id, campaign_budget_id)
    client.copy_from(campaign.manual_cpc, client.get_type("ManualCpc"))

    # Issues a mutate request to add the campaign.
    campaign_response = campaign_service.mutate_campaigns(
        customer_id=customer_id, operations=[campaign_operation]
    )
    campaign_resource_name = campaign_response.results[0].resource_name
    print(f"Created campaign with resource name '{campaign_resource_name}'.")

    return campaign_resource_name
    # [END add_merchant_center_dynamic_remarketing_campaign_2]


# [START add_merchant_center_dynamic_remarketing_campaign_1]
def _create_ad_group(client, customer_id, campaign_resource_name):
    """Creates an ad group for the remarketing campaign.

    Args:
        client: An initialized GoogleAds client.
        customer_id: The Google Ads customer ID.
        campaign_resource_name: The resource name of the target campaign.
    Returns:
        The string resource name of the newly created ad group.
    """
    # Gets the AdGroupService.
    ad_group_service = client.get_service("AdGroupService")

    # Creates an ad group operation and configures the new ad group.
    ad_group_operation = client.get_type("AdGroupOperation")
    ad_group = ad_group_operation.create
    ad_group.name = "Dynamic remarketing ad group"
    ad_group.campaign = campaign_resource_name
    ad_group.status = client.get_type("AdGroupStatusEnum").AdGroupStatus.ENABLED

    # Issues a mutate request to add the ad group.
    ad_group_response = ad_group_service.mutate_ad_groups(
        customer_id=customer_id, operations=[ad_group_operation]
    )
    ad_group_resource_name = ad_group_response.results[0].resource_name

    return ad_group_resource_name
    # [END add_merchant_center_dynamic_remarketing_campaign_1]


# [START add_merchant_center_dynamic_remarketing_campaign]
def _create_ad(client, customer_id, ad_group_resource_name):
    """Creates the responsive display ad.

    Args:
        client: An initialized GoogleAds client.
        customer_id: The Google Ads customer ID.
        ad_group_resource_name: The resource name of the target ad group.
    """
    # Get the AdGroupAdService client.
    ad_group_ad_service = client.get_service("AdGroupAdService")

    # Upload image assets for the ad.
    marketing_image_resource_name = _upload_image_asset(
        client, customer_id, "https://goo.gl/3b9Wfh", "Marketing Image"
    )
    square_marketing_image_resource_name = _upload_image_asset(
        client, customer_id, "https://goo.gl/mtt54n", "Square Marketing Image"
    )

    # Create the relevant asset objects for the ad.
    marketing_image = client.get_type("AdImageAsset")
    marketing_image.asset = marketing_image_resource_name
    square_marketing_image = client.get_type("AdImageAsset")
    square_marketing_image.asset = square_marketing_image_resource_name
    headline = client.get_type("AdTextAsset")
    headline.text = "Travel"
    description = client.get_type("AdTextAsset")
    description.text = "Take to the air!"

    # Create an ad group ad operation and set the ad group ad values.
    ad_group_ad_operation = client.get_type("AdGroupAdOperation")
    ad_group_ad = ad_group_ad_operation.create
    ad_group_ad.ad_group = ad_group_resource_name
    ad_group_ad.ad.final_urls.append("http://www.example.com/")

    # Configure the responsive display ad info object.
    responsive_display_ad_info = ad_group_ad.ad.responsive_display_ad
    responsive_display_ad_info.marketing_images.append(marketing_image)
    responsive_display_ad_info.square_marketing_images.append(
        square_marketing_image
    )
    responsive_display_ad_info.headlines.append(headline)
    responsive_display_ad_info.long_headline.text = "Travel the World"
    responsive_display_ad_info.descriptions.append(description)
    responsive_display_ad_info.business_name = "Interplanetary Cruises"
    # Optional: Call to action text.
    # Valid texts: https://support.google.com/google-ads/answer/7005917
    responsive_display_ad_info.call_to_action_text = "Apply Now"
    # Optional: Set the ad colors.
    responsive_display_ad_info.main_color = "#0000ff"
    responsive_display_ad_info.accent_color = "#ffff00"
    # Optional: Set to false to strictly render the ad using the colors.
    responsive_display_ad_info.allow_flexible_color = False
    # Optional: Set the format setting that the ad will be served in.
    responsive_display_ad_info.format_setting = client.get_type(
        "DisplayAdFormatSettingEnum"
    ).DisplayAdFormatSetting.NON_NATIVE
    # Optional: Create a logo image and set it to the ad.
    # logo_image = client.get_type("AdImageAsset")
    # logo_image.asset = "INSERT_LOGO_IMAGE_RESOURCE_NAME_HERE"
    # responsive_display_ad_info.logo_images.append(logo_image)
    # Optional: Create a square logo image and set it to the ad.
    # square_logo_image = client.get_type("AdImageAsset")
    # square_logo_image.asset = "INSERT_SQUARE_LOGO_IMAGE_RESOURCE_NAME_HERE"
    # responsive_display_ad_info.square_logo_images.append(square_logo_image)

    # Issue a mutate request to add the ad group ad.
    ad_group_ad_response = ad_group_ad_service.mutate_ad_group_ads(
        customer_id=customer_id, operations=[ad_group_ad_operation]
    )
    print(
        "Created ad group ad with resource name "
        f"'{ad_group_ad_response.results[0].resource_name}'."
    )
    # [END add_merchant_center_dynamic_remarketing_campaign]


def _upload_image_asset(client, customer_id, image_url, asset_name):
    """Adds an image asset to the Google Ads account.

    Args:
        client: An initialized GoogleAds client.
        customer_id: The Google Ads customer ID.
        image_url: The URL of the image source.
        asset_name: The string label for this image asset.
    Returns:
        The string resource name of the newly uploaded image asset.
    """
    # Get the AssetService client.
    asset_service = client.get_service("AssetService")

    # Fetch the image data.
    image_data = requests.get(image_url).content

    # Create an asset operation and set the image asset values.
    asset_operation = client.get_type("AssetOperation")
    asset = asset_operation.create
    asset.type_ = client.get_type("AssetTypeEnum").AssetType.IMAGE
    asset.image_asset.data = image_data
    asset.name = asset_name

    mutate_asset_response = asset_service.mutate_assets(
        customer_id=customer_id, operations=[asset_operation]
    )
    image_asset_resource_name = mutate_asset_response.results[0].resource_name
    print(
        "Created image asset with resource name "
        f"'{image_asset_resource_name}'."
    )

    return image_asset_resource_name


# [START add_merchant_center_dynamic_remarketing_campaign_3]
def _attach_user_list(
    client, customer_id, ad_group_resource_name, user_list_id
):
    """Targets a user list with an ad group.

    Args:
        client: An initialized GoogleAds client.
        customer_id: The Google Ads customer ID.
        ad_group_resource_name: The resource name of the target ad group.
        user_list_id: The ID of the user list to target for remarketing.
    """
    # Get the AdGroupCriterionService client.
    ad_group_criterion_service = client.get_service("AdGroupCriterionService")

    # Create an ad group criterion operation and set the ad group criterion
    # values.
    ad_group_criterion_operation = client.get_type("AdGroupCriterionOperation")
    ad_group_criterion = ad_group_criterion_operation.create
    ad_group_criterion.ad_group = ad_group_resource_name
    ad_group_criterion.user_list.user_list = client.get_service(
        "UserListService"
    ).user_list_path(customer_id, user_list_id)

    # Issue a mutate request to add the ad group criterion.
    ad_group_criterion_response = ad_group_criterion_service.mutate_ad_group_criteria(
        customer_id=customer_id, operations=[ad_group_criterion_operation]
    )
    print(
        "Created ad group criterion with resource name "
        f"'{ad_group_criterion_response.results[0].resource_name}'."
    )
    # [END add_merchant_center_dynamic_remarketing_campaign_3]


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v8")

    parser = argparse.ArgumentParser(
        description=(
            "Creates a shopping campaign associated with an existing "
            "Merchant Center acconut."
        )
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
        help="The target Merchant Center account ID.",
    )
    parser.add_argument(
        "-b",
        "--campaign_budget_id",
        type=int,
        required=True,
        help="The campaign budget ID to apply to the campaign.",
    )
    parser.add_argument(
        "-u",
        "--user_list_id",
        type=int,
        required=True,
        help="The user list ID to target.",
    )
    args = parser.parse_args()

    try:
        main(
            googleads_client,
            args.customer_id,
            args.merchant_center_account_id,
            args.campaign_budget_id,
            args.user_list_id,
        )
    except GoogleAdsException as ex:
        print(
            f"Request with ID '{ex.request_id}' failed with status "
            f"'{ex.error.code().name}' and includes the following errors:"
        )
        for error in ex.failure.errors:
            print(f"\tError with message '{error.message}'.")
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print(f"\t\tOn field: {field_path_element.field_name}")
        sys.exit(1)
