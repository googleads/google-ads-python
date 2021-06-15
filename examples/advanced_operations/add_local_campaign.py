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
"""This example adds a Local campaign.

Prerequisite: To create a Local campaign, you need to define the store locations
you want to promote by linking your Google My Business account or selecting
affiliate locations. More information about Local campaigns can be found at:
https://support.google.com/google-ads/answer/9118422.
"""


import argparse
import requests
import sys
from uuid import uuid4


from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


_MARKETING_IMAGE_URL = "https://goo.gl/3b9Wfh"
_LOGO_IMAGE_URL = "https://goo.gl/mtt54n"
_YOUTUBE_VIDEO_ID = "t1fDo0VyeEo"


def main(client, customer_id):
    """The main method that creates all necessary entities for the example.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID str.
    """
    budget_resource_name = _create_campaign_budget(client, customer_id)
    campaign_resource_name = _create_campaign(
        client, customer_id, budget_resource_name
    )
    ad_group_resource_name = _create_ad_group(
        client, customer_id, campaign_resource_name
    )
    create_local_ad = _create_local_ad(
        client, customer_id, ad_group_resource_name
    )


# [START add_local_campaign]
def _create_campaign_budget(client, customer_id):
    """Adds a campaign budget to the given client account.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID str.

    Returns:
        A str of the resource name for the newly created campaign budget.
    """
    # Create a CampaignBudgetOperation.
    campaign_budget_operation = client.get_type("CampaignBudgetOperation")
    campaign_budget = campaign_budget_operation.create
    campaign_budget.name = f"Interplanetary Cruise Budget #{uuid4()}"
    campaign_budget.amount_micros = 50000000
    campaign_budget.delivery_method = client.get_type(
        "BudgetDeliveryMethodEnum"
    ).BudgetDeliveryMethod.STANDARD
    # A Local campaign cannot use a shared campaign budget.
    campaign_budget.explicitly_shared = False

    # Issue a mutate request to add the campaign budget.
    campaign_budget_service = client.get_service("CampaignBudgetService")
    response = campaign_budget_service.mutate_campaign_budgets(
        customer_id=customer_id, operations=[campaign_budget_operation]
    )
    resource_name = response.results[0].resource_name
    print(f"Created campaign budget with resource name: '{resource_name}'")
    return resource_name
    # [END add_local_campaign]


# [START add_local_campaign_1]
def _create_campaign(client, customer_id, budget_resource_name):
    """Adds a Local campaign to the given client account using the given budget.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID str.
        budget_resource_name: the resource name str for a campaign budget.

    Returns:
        A str of the resource name for the newly created campaign.
    """
    # Create a CampaignOperation.
    campaign_operation = client.get_type("CampaignOperation")
    # Create a Campaign.
    campaign = campaign_operation.create
    campaign.name = f"Interplanetary Cruise Local #{uuid4()}"
    campaign.campaign_budget = budget_resource_name
    # Recommendation: Set the campaign to PAUSED when creating it to prevent
    # the ads from immediately serving. Set to ENABLED once you've added
    # targeting and the ads are ready to serve.
    campaign.status = client.get_type(
        "CampaignStatusEnum"
    ).CampaignStatus.PAUSED
    # All Local campaigns have an advertising_channel_type of LOCAL and
    # advertising_channel_sub_type of LOCAL_CAMPAIGN.
    campaign.advertising_channel_type = client.get_type(
        "AdvertisingChannelTypeEnum"
    ).AdvertisingChannelType.LOCAL
    campaign.advertising_channel_sub_type = client.get_type(
        "AdvertisingChannelSubTypeEnum"
    ).AdvertisingChannelSubType.LOCAL_CAMPAIGN
    # Bidding strategy must be set directly on the campaign.
    # Setting a portfolio bidding strategy by resource name is not supported.
    # Maximize conversion value is the only strategy supported for Local
    # campaigns. An optional ROAS (Return on Advertising Spend) can be set for
    # maximize_conversion_value. The ROAS value must be specified as a ratio in
    # the API. It is calculated by dividing "total value" by "total spend".
    # For more information on maximize conversion value, see the support
    # article: http://support.google.com/google-ads/answer/7684216.
    # A target_roas of 3.5 corresponds to a 350% return on ad spend.
    campaign.maximize_conversion_value.target_roas = 3.5
    # Configure the Local campaign setting. Use the locations associated with
    # the customer's linked Google My Business account.
    campaign.local_campaign_setting.location_source_type = client.get_type(
        "LocationSourceTypeEnum"
    ).LocationSourceType.GOOGLE_MY_BUSINESS
    # Optimization goal setting is mandatory for Local campaigns. This example
    # selects driving directions and call clicks as goals.
    optimization_goal_type_enum = client.get_type(
        "OptimizationGoalTypeEnum"
    ).OptimizationGoalType
    campaign.optimization_goal_setting.optimization_goal_types.extend(
        [
            optimization_goal_type_enum.CALL_CLICKS,
            optimization_goal_type_enum.DRIVING_DIRECTIONS,
        ]
    )

    campaign_service = client.get_service("CampaignService")
    response = campaign_service.mutate_campaigns(
        customer_id=customer_id, operations=[campaign_operation]
    )
    resource_name = response.results[0].resource_name
    print(f"Created Local Campaign with resource name: '{resource_name}'")
    return resource_name
    # [END add_local_campaign_1]


# [START add_local_campaign_2]
def _create_ad_group(client, customer_id, campaign_resource_name):
    """Adds an ad group to the given client account under the given campaign.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID str.
        campaign_resource_name: the resource name str for a campaign.

    Returns:
        A str of the resource name for the newly created ad group.
    """
    ad_group_operation = client.get_type("AdGroupOperation")
    ad_group = ad_group_operation.create
    # Note that the ad group type must not be set.
    # Since the advertising_channel_subType is LOCAL_CAMPAIGN:
    #   1. you cannot override bid settings at the ad group level.
    #   2. you cannot add ad group criteria.
    ad_group.name = f"Earth to Mars Cruises #{uuid4()}"
    ad_group.status = client.get_type("AdGroupStatusEnum").AdGroupStatus.ENABLED
    ad_group.campaign = campaign_resource_name

    ad_group_service = client.get_service("AdGroupService")
    response = ad_group_service.mutate_ad_groups(
        customer_id=customer_id, operations=[ad_group_operation]
    )
    resource_name = response.results[0].resource_name
    print(f"Created AdGroup with resource name: '{resource_name}'")
    return resource_name
    # [END add_local_campaign_2]


# [START add_local_campaign_3]
def _create_local_ad(client, customer_id, ad_group_resource_name):
    """Adds a local ad to the given client account under the given ad group.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID str.
        ad_group_resource_name: the resource name str for a ad group.
    """
    ad_group_ad_operation = client.get_type("AdGroupAdOperation")
    ad_group_ad = ad_group_ad_operation.create
    ad_group_ad.ad_group = ad_group_resource_name
    ad_group_ad.status = client.get_type(
        "AdGroupAdStatusEnum"
    ).AdGroupAdStatus.ENABLED
    ad_group_ad.ad.final_urls.append("https://www.example.com")
    ad_group_ad.ad.local_ad.headlines.extend(
        [
            _create_ad_text_asset(client, "Best Space Cruise Line"),
            _create_ad_text_asset(client, "Experience the Stars"),
        ]
    )
    ad_group_ad.ad.local_ad.descriptions.extend(
        [
            _create_ad_text_asset(client, "Buy your tickets now"),
            _create_ad_text_asset(client, "Visit the Red Planet"),
        ]
    )
    ad_group_ad.ad.local_ad.call_to_actions.append(
        _create_ad_text_asset(client, "Shop Now")
    )
    marketing_image = client.get_type("AdImageAsset")
    marketing_image.asset = _create_image_asset(
        client, customer_id, _MARKETING_IMAGE_URL, "Marketing Image"
    )
    ad_group_ad.ad.local_ad.marketing_images.append(marketing_image)

    logo_image = client.get_type("AdImageAsset")
    logo_image.asset = _create_image_asset(
        client, customer_id, _LOGO_IMAGE_URL, "Square Marketing Image"
    )
    ad_group_ad.ad.local_ad.logo_images.append(logo_image)

    video = client.get_type("AdVideoAsset")
    video.asset = _create_youtube_video_asset(
        client, customer_id, _YOUTUBE_VIDEO_ID, "Local Campaigns"
    )
    ad_group_ad.ad.local_ad.videos.append(video)

    ad_group_ad_service = client.get_service("AdGroupAdService")
    response = ad_group_ad_service.mutate_ad_group_ads(
        customer_id=customer_id, operations=[ad_group_ad_operation]
    )
    resource_name = response.results[0].resource_name
    print(f"Created ad group ad with resource name: '{resource_name}'")


def _create_ad_text_asset(client, text):
    """Creates an ad text asset with the given text value.

    Args:
        client: an initialized GoogleAdsClient instance.
        text: a str for the text value of the ad text asset.

    Returns:
        an ad text asset.
    """
    ad_text_asset = client.get_type("AdTextAsset")
    ad_text_asset.text = text
    return ad_text_asset
    # [END add_local_campaign_3]


# [START add_local_campaign_4]
def _create_image_asset(client, customer_id, image_url, image_name):
    """Creates an asset with the given image URL and name.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID str.
        image_url: a str URL to download an image.
        image_name: a str to use to name the image.

    Returns:
        an asset.
    """
    asset_operation = client.get_type("AssetOperation")
    asset = asset_operation.create
    asset.name = image_name
    asset.type_ = client.get_type("AssetTypeEnum").AssetType.IMAGE
    asset.image_asset.data = _get_image_bytes(image_url)
    asset_service = client.get_service("AssetService")
    response = asset_service.mutate_assets(
        customer_id=customer_id, operations=[asset_operation]
    )
    resource_name = response.results[0].resource_name
    print(
        "A new image asset has been added with resource name: "
        f"'{resource_name}'"
    )
    return resource_name


def _get_image_bytes(url):
    """Loads image data from a URL.

    Args:
        url: a URL str.

    Returns:
        Images bytes loaded from the given URL.
    """
    response = requests.get(url)
    return response.content
    # [END add_local_campaign_4]


# [START add_local_campaign_5]
def _create_youtube_video_asset(
    client, customer_id, youtube_video_id, youtube_video_name
):
    """Creates a asset with the given YouTube video ID and name.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID str.
        youtube_video_id: a str of a YouTube video ID.
        youtube_video_name: a str to use for the name of the video asset.

    Returns:
        an Asset.
    """
    asset_operation = client.get_type("AssetOperation")
    asset = asset_operation.create
    asset.name = youtube_video_name
    asset.type_ = client.get_type("AssetTypeEnum").AssetType.YOUTUBE_VIDEO
    asset.youtube_video_asset.youtube_video_id = youtube_video_id

    asset_service = client.get_service("AssetService")
    response = asset_service.mutate_assets(
        customer_id=customer_id, operations=[asset_operation]
    )
    resource_name = response.results[0].resource_name
    print(
        "A new YouTube video asset has been added with resource name: "
        f"'{resource_name}'"
    )
    return resource_name
    # [END add_local_campaign_5]


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v8")

    parser = argparse.ArgumentParser(
        description="Adds a Local Campaign to the given account."
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
        main(googleads_client, args.customer_id)
    except GoogleAdsException as ex:
        print(
            f'Request with ID "{ex.request_id}" failed with status '
            f'"{ex.error.code().name}" and includes the following errors:'
        )
        for error in ex.failure.errors:
            print(f'	Error with message "{error.message}".')
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print(f"\t\tOn field: {field_path_element.field_name}")
        sys.exit(1)
