# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""This example shows how to create a Demand Gen campaign with a video ad.

For more information about Demand Gen campaigns, see
https://developers.google.com/google-ads/api/docs/demand-gen/overview
"""

import argparse
import sys
from typing import List
from uuid import uuid4

from examples.utils.example_helpers import get_image_bytes_from_url
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.ads.googleads.v22.common.types import (
    AdImageAsset,
    AdTextAsset,
    AdVideoAsset,
    DemandGenVideoResponsiveAdInfo,
)
from google.ads.googleads.v22.resources.types import (
    Ad,
    AdGroup,
    AdGroupAd,
    Asset,
    Campaign,
    CampaignBudget,
)
from google.ads.googleads.v22.services.services.google_ads_service import (
    GoogleAdsServiceClient,
)
from google.ads.googleads.v22.services.types import (
    AdGroupAdOperation,
    AdGroupOperation,
    AssetOperation,
    CampaignBudgetOperation,
    CampaignOperation,
    MutateOperation,
)

# Temporary IDs for resources.
BUDGET_TEMPORARY_ID: int = -1
CAMPAIGN_TEMPORARY_ID: int = -2
AD_GROUP_TEMPORARY_ID: int = -3
VIDEO_ASSET_TEMPORARY_ID: int = -4
LOGO_ASSET_TEMPORARY_ID: int = -5

# URLs for assets
DEFAULT_LOGO_IMAGE_URL: str = "https://gaagl.page.link/bjYi"
DEFAULT_FINAL_URL: str = "http://example.com/demand_gen"


def main(client: GoogleAdsClient, customer_id: str, video_id: str) -> None:
    """The main method that creates all necessary entities for the example.

    Args:
        client: An initialized GoogleAdsClient instance.
        customer_id: The Google Ads customer ID.
        video_id: The YouTube ID of a video to use in an ad.
    """
    googleads_service: GoogleAdsServiceClient = client.get_service(
        "GoogleAdsService"
    )

    budget_resource_name: str = googleads_service.campaign_budget_path(
        customer_id, BUDGET_TEMPORARY_ID
    )
    campaign_resource_name: str = googleads_service.campaign_path(
        customer_id, CAMPAIGN_TEMPORARY_ID
    )
    ad_group_resource_name: str = googleads_service.ad_group_path(
        customer_id, AD_GROUP_TEMPORARY_ID
    )
    video_asset_resource_name: str = googleads_service.asset_path(
        customer_id, VIDEO_ASSET_TEMPORARY_ID
    )
    logo_asset_resource_name: str = googleads_service.asset_path(
        customer_id, LOGO_ASSET_TEMPORARY_ID
    )

    # [START add_demand_gen_campaign_1]
    # The below methods create and return MutateOperations that we later provide
    # to the GoogleAdsService.Mutate method in order to create the entities in a
    # single request. Since the entities for a Demand Gen campaign are closely
    # tied to one-another it's considered a best practice to create them in a
    # single Mutate request; the entities will either all complete successfully
    # or fail entirely, leaving no orphaned entities. See:
    # https://developers.google.com/google-ads/api/docs/mutating/overview
    mutate_operations: List[MutateOperation] = [
        # It's important to create these entities in this order because they
        # depend on each other, for example the ad group depends on the
        # campaign, and the ad group ad depends on the ad group.
        create_campaign_budget_operation(client, budget_resource_name),
        create_demand_gen_campaign_operation(
            client, campaign_resource_name, budget_resource_name
        ),
        create_ad_group_operation(
            client, ad_group_resource_name, campaign_resource_name
        ),
        *create_asset_operations(  # Use iterable unpacking
            client,
            video_asset_resource_name,
            video_id,
            logo_asset_resource_name,
        ),
        create_demand_gen_ad_operation(
            client,
            ad_group_resource_name,
            video_asset_resource_name,
            logo_asset_resource_name,
        ),
    ]

    # Send the operations in a single mutate request.
    googleads_service.mutate(
        customer_id=customer_id, mutate_operations=mutate_operations
    )
    # [END add_demand_gen_campaign_1]


def create_campaign_budget_operation(
    client: GoogleAdsClient, budget_resource_name: str
) -> MutateOperation:
    """Creates a MutateOperation that creates a new CampaignBudget.

    A temporary ID will be assigned to this campaign budget so that it can be
    referenced by other objects being created in the same Mutate request.

    Args:
        client: An initialized GoogleAdsClient instance.
        budget_resource_name: The temporary resource name of the budget.

    Returns:
        A MutateOperation for creating a CampaignBudget.
    """
    mutate_operation: MutateOperation = client.get_type("MutateOperation")
    campaign_budget_operation: CampaignBudgetOperation = (
        mutate_operation.campaign_budget_operation
    )
    campaign_budget: CampaignBudget = campaign_budget_operation.create
    campaign_budget.name = f"Demand Gen campaign budget {uuid4()}"
    # The budget period already defaults to DAILY.
    campaign_budget.amount_micros = 50_000_000
    campaign_budget.delivery_method = (
        client.enums.BudgetDeliveryMethodEnum.STANDARD
    )
    # A Demand Gen campaign cannot use a shared campaign budget.
    campaign_budget.explicitly_shared = False
    # Set a temporary ID in the budget's resource name so it can be referenced
    # by the campaign in later steps.
    campaign_budget.resource_name = budget_resource_name
    # campaign_budget.period = client.enums.BudgetPeriodEnum.DAILY (default)
    return mutate_operation


# [START add_demand_gen_campaign_2]
def create_demand_gen_campaign_operation(
    client: GoogleAdsClient,
    campaign_resource_name: str,
    budget_resource_name: str,
) -> MutateOperation:
    """Creates a MutateOperation that creates a new Campaign.

    A temporary ID will be assigned to this campaign so that it can be
    referenced by other objects being created in the same Mutate request.

    Args:
        client: An initialized GoogleAdsClient instance.
        campaign_resource_name: The temporary resource name of the campaign.
        budget_resource_name: The resource name of the budget to assign.

    Returns:
        A MutateOperation for creating a Campaign.
    """
    mutate_operation: MutateOperation = client.get_type("MutateOperation")
    campaign_operation: CampaignOperation = mutate_operation.campaign_operation
    campaign: Campaign = campaign_operation.create
    campaign.name = f"Demand Gen #{uuid4()}"
    # Set the campaign status as PAUSED. The campaign is the only entity in the
    # mutate request that should have its status set.
    campaign.status = client.enums.CampaignStatusEnum.PAUSED
    # AdvertisingChannelType must be DEMAND_GEN.
    campaign.advertising_channel_type = (
        client.enums.AdvertisingChannelTypeEnum.DEMAND_GEN
    )
    # Assign the resource name with a temporary ID.
    campaign.resource_name = campaign_resource_name
    # Set the budget using the given budget resource name.
    campaign.campaign_budget = budget_resource_name
    # Use the Target CPA bidding strategy.
    campaign.bidding_strategy_type = (
        client.enums.BiddingStrategyTypeEnum.TARGET_CPA
    )
    campaign.target_cpa.target_cpa_micros = 1_000_000
    return mutate_operation
    # [END add_demand_gen_campaign_2]


# [START add_demand_gen_campaign_3]
def create_ad_group_operation(
    client: GoogleAdsClient,
    ad_group_resource_name: str,
    campaign_resource_name: str,
) -> MutateOperation:
    """Creates a MutateOperation that creates a new AdGroup.

    Args:
        client: An initialized GoogleAdsClient instance.
        ad_group_resource_name: The temporary resource name of the ad group.
        campaign_resource_name: The temporary resource name of the campaign the
            ad group will belong to.

    Returns:
        A MutateOperation for creating an AdGroup.
    """
    mutate_operation: MutateOperation = client.get_type("MutateOperation")
    ad_group_operation: AdGroupOperation = mutate_operation.ad_group_operation
    # Creates an ad group.
    ad_group: AdGroup = ad_group_operation.create
    ad_group.resource_name = ad_group_resource_name
    ad_group.name = f"Earth to Mars Cruises #{uuid4()}"
    ad_group.status = client.enums.AdGroupStatusEnum.ENABLED
    ad_group.campaign = campaign_resource_name

    # [START add_demand_gen_campaign_5]
    # Select the specific channels for the ad group. For further information on
    # Demand Gen channel controls, see:
    # https://developers.google.com/google-ads/api/docs/demand-gen/channel-controls
    selected_channel_controls = (
        ad_group.demand_gen_ad_group_settings.channel_controls.selected_channels
    )
    selected_channel_controls.gmail = False
    selected_channel_controls.discover = False
    selected_channel_controls.display = False
    selected_channel_controls.youtube_in_feed = True
    selected_channel_controls.youtube_in_stream = True
    selected_channel_controls.youtube_shorts = True
    # [END add_demand_gen_campaign_5]

    return mutate_operation
    # [END add_demand_gen_campaign_3]


def create_asset_operations(
    client: GoogleAdsClient,
    video_asset_resource_name: str,
    video_id: str,
    logo_asset_resource_name: str,
) -> List[MutateOperation]:
    """Creates a list of MutateOperations that create new Assets.

    Args:
        client: An initialized GoogleAdsClient instance.
        video_asset_resource_name: Temporary resource name for the video asset.
        video_id: YouTube ID of the video asset.
        logo_asset_resource_name: Temporary resource name for the logo asset.

    Returns:
        A list of MutateOperations for creating Assets.
    """
    return [
        create_video_asset_operation(
            client, video_asset_resource_name, video_id, "Video"
        ),
        # Create the logo image asset.
        create_image_asset_operation(
            client,
            logo_asset_resource_name,
            DEFAULT_LOGO_IMAGE_URL,
            "Square Marketing Image",
        ),
    ]


# [START add_demand_gen_campaign_4]
def create_demand_gen_ad_operation(
    client: GoogleAdsClient,
    ad_group_resource_name: str,
    video_asset_resource_name: str,
    logo_asset_resource_name: str,
) -> MutateOperation:
    """Creates a MutateOperation that creates a new Demand Gen Ad.

    Args:
        client: An initialized GoogleAdsClient instance.
        ad_group_resource_name: The ad group the ad will belong to.
        video_asset_resource_name: The video asset resource name.
        logo_asset_resource_name: The logo asset resource name.

    Returns:
        A MutateOperation for creating an AdGroupAd.
    """
    mutate_operation: MutateOperation = client.get_type("MutateOperation")
    ad_group_ad_operation: AdGroupAdOperation = (
        mutate_operation.ad_group_ad_operation
    )
    ad_group_ad: AdGroupAd = ad_group_ad_operation.create
    ad_group_ad.ad_group = ad_group_resource_name
    ad_group_ad.status = client.enums.AdGroupAdStatusEnum.ENABLED

    ad: Ad = ad_group_ad.ad
    ad.name = "Demand gen multi asset ad"
    ad.final_urls.append(DEFAULT_FINAL_URL)

    demand_gen_ad: DemandGenVideoResponsiveAdInfo = (
        ad.demand_gen_video_responsive_ad
    )
    # Ensure business_name is an AssetLink and assign text to its text_asset.text
    demand_gen_ad.business_name.text = "Interplanetary Cruises"
    # If it needs to be an AssetLink to a text asset,
    # that would require creating another asset.

    # Create AssetLink for video
    video_asset_link: AdVideoAsset = client.get_type("AdVideoAsset")
    video_asset_link.asset = video_asset_resource_name
    demand_gen_ad.videos.append(video_asset_link)

    # Create AssetLink for logo
    logo_image_asset_link: AdImageAsset = client.get_type("AdImageAsset")
    logo_image_asset_link.asset = logo_asset_resource_name
    demand_gen_ad.logo_images.append(logo_image_asset_link)

    # Create AssetLink for headline
    headline_asset_link: AdTextAsset = client.get_type("AdTextAsset")
    headline_asset_link.text = "Interplanetary cruises"
    demand_gen_ad.headlines.append(headline_asset_link)

    # Create AssetLink for long headline
    long_headline_asset_link: AdTextAsset = client.get_type("AdTextAsset")
    long_headline_asset_link.text = "Travel the World"
    demand_gen_ad.long_headlines.append(long_headline_asset_link)

    # Create AssetLink for description
    description_asset_link: AdTextAsset = client.get_type("AdTextAsset")
    description_asset_link.text = "Book now for an extra discount"
    demand_gen_ad.descriptions.append(description_asset_link)

    return mutate_operation
    # [END add_demand_gen_campaign_4]


def create_image_asset_operation(
    client: GoogleAdsClient, asset_resource_name: str, url: str, asset_name: str
) -> MutateOperation:
    """Creates a MutateOperation for a new image asset.

    Args:
        client: An initialized GoogleAdsClient instance.
        asset_resource_name: The resource name for the image asset.
        url: The URL of the image.
        asset_name: The name of the asset.

    Returns:
        A MutateOperation for creating an image asset.
    """
    mutate_operation: MutateOperation = client.get_type("MutateOperation")
    asset_operation: AssetOperation = mutate_operation.asset_operation
    asset: Asset = asset_operation.create
    asset.resource_name = asset_resource_name
    # Provide a unique friendly name to identify your asset. When there is an
    # existing image asset with the same content but a different name, the new
    # name will be dropped silently.
    asset.name = asset_name
    asset.type_ = client.enums.AssetTypeEnum.IMAGE
    asset.image_asset.data = get_image_bytes_from_url(url)

    return mutate_operation


def create_video_asset_operation(
    client: GoogleAdsClient,
    asset_resource_name: str,
    video_id: str,
    asset_name: str,
) -> MutateOperation:
    """Creates a MutateOperation for a new video asset.

    Args:
        client: An initialized GoogleAdsClient instance.
        asset_resource_name: The resource name for the video asset.
        video_id: The YouTube ID of the video.
        asset_name: The name of the asset.

    Returns:
        A MutateOperation for creating a video asset.
    """
    mutate_operation: MutateOperation = client.get_type("MutateOperation")
    asset_operation: AssetOperation = mutate_operation.asset_operation
    asset: Asset = asset_operation.create
    asset.resource_name = asset_resource_name
    asset.name = asset_name
    asset.type_ = client.enums.AssetTypeEnum.YOUTUBE_VIDEO
    asset.youtube_video_asset.youtube_video_id = video_id
    return mutate_operation


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Adds a Demand Gen campaign with a video ad."
    )
    parser.add_argument(
        "-c",
        "--customer_id",
        type=str,
        required=True,
        help="The Google Ads customer ID.",
    )
    parser.add_argument(
        "-v",
        "--video_id",
        type=str,
        required=True,
        help="The YouTube ID of a video to use in an ad.",
    )
    args: argparse.Namespace = parser.parse_args()

    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client: GoogleAdsClient = GoogleAdsClient.load_from_storage(
        version="v22"
    )

    try:
        main(googleads_client, args.customer_id, args.video_id)
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
