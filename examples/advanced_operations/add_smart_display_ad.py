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
"""This adds a smart display campaign, an ad group, and a responsive display ad.

More information about Smart Display campaigns can be found at:
https://support.google.com/google-ads/answer/7020281

IMPORTANT: The AssetService requires you to reuse what you've uploaded
previously. Therefore, you cannot create an image asset with the exactly same
bytes. In case you want to run this example more than once, note down the
created assets' resource names and specify them as command-line arguments for
marketing and square marketing images.

Alternatively, you can modify the image URLs' constants directly to use other
images. You can find image specifications in the pydoc for
ResponsiveDisplayAdInfo in common/ad_type_infos_pb2.py.
"""


import argparse
import datetime
import requests
import sys
from uuid import uuid4

from google.ads.google_ads.client import GoogleAdsClient
from google.ads.google_ads.errors import GoogleAdsException


_DATE_FORMAT = "%Y%m%d"
_MARKETING_IMAGE_URL = "https://goo.gl/3b9Wfh"
_MARKETING_IMAGE_WIDTH = 600
_MARKETING_IMAGE_HEIGHT = 315
_SQUARE_MARKETING_IMAGE_URL = "https://goo.gl/mtt54n"
_SQUARE_MARKETING_IMAGE_SIZE = 512


def main(
    client,
    customer_id,
    marketing_image_asset_id=None,
    square_marketing_image_asset_id=None,
):
    budget_resource_name = _create_budget(client, customer_id)
    print(f'Created budget with resource name "{budget_resource_name}".')

    campaign_resource_name = _create_smart_display_campaign(
        client, customer_id, budget_resource_name
    )
    print(
        "Created smart display campaign with resource name "
        f'"{campaign_resource_name}".'
    )

    ad_group_resource_name = _create_ad_group(
        client, customer_id, campaign_resource_name
    )
    print(f'Created ad group with resource name "{ad_group_resource_name}"')

    if marketing_image_asset_id:
        print(
            "Using existing marketing image asset with resource name "
            f'"{marketing_image_asset_id}".'
        )
    else:
        marketing_image_asset_id = _upload_image_asset(
            client,
            customer_id,
            _MARKETING_IMAGE_URL,
            _MARKETING_IMAGE_WIDTH,
            _MARKETING_IMAGE_HEIGHT,
        )
        print(
            "Created marketing image asset with resource name "
            f'"{marketing_image_asset_id}".'
        )

    if square_marketing_image_asset_id:
        print(
            "Using existing square marketing image asset with resource name "
            f'"{square_marketing_image_asset_id}".'
        )
    else:
        square_marketing_image_asset_id = _upload_image_asset(
            client,
            customer_id,
            _SQUARE_MARKETING_IMAGE_URL,
            _SQUARE_MARKETING_IMAGE_SIZE,
            _SQUARE_MARKETING_IMAGE_SIZE,
        )
        print(
            "Created square marketing image asset with resource name "
            f'"{square_marketing_image_asset_id}".'
        )

    responsive_display_ad_resource_name = _create_responsive_display_ad(
        client,
        customer_id,
        ad_group_resource_name,
        marketing_image_asset_id,
        square_marketing_image_asset_id,
    )

    print(
        "Created responsive display ad with resource name "
        f'"{responsive_display_ad_resource_name}".'
    )


# [START add_smart_display_ad_3]
def _create_budget(client, customer_id):
    campaign_budget_operation = client.get_type(
        "CampaignBudgetOperation", version="v6"
    )
    campaign_budget = campaign_budget_operation.create
    campaign_budget.name = f"Interplanetary Cruise Budget #{uuid4()}"
    campaign_budget.delivery_method = client.get_type(
        "BudgetDeliveryMethodEnum"
    ).STANDARD
    campaign_budget.amount_micros = 500000

    campaign_budget_service = client.get_service(
        "CampaignBudgetService", version="v6"
    )

    try:
        campaign_budget_response = campaign_budget_service.mutate_campaign_budgets(
            customer_id, [campaign_budget_operation]
        )
        return campaign_budget_response.results[0].resource_name
    except GoogleAdsException as ex:
        _handle_google_ads_exception(ex)
        # [END add_smart_display_ad_3]


# [START add_smart_display_ad_4]
def _create_smart_display_campaign(client, customer_id, budget_resource_name):
    campaign_operation = client.get_type("CampaignOperation", version="v6")
    campaign = campaign_operation.create
    campaign.name = f"Smart Display Campaign #{uuid4()}"
    advertising_channel_type_enum = client.get_type(
        "AdvertisingChannelTypeEnum", version="v6"
    )
    campaign.advertising_channel_type = advertising_channel_type_enum.DISPLAY
    advertising_channel_sub_type_enum = client.get_type(
        "AdvertisingChannelSubTypeEnum", version="v6"
    )
    # Smart Display campaign requires the advertising_channel_sub_type as
    # "DISPLAY_SMART_CAMPAIGN".
    campaign.advertising_channel_sub_type = (
        advertising_channel_sub_type_enum.DISPLAY_SMART_CAMPAIGN
    )
    campaign_status_enum = client.get_type("CampaignStatusEnum", version="v6")
    campaign.status = campaign_status_enum.PAUSED
    # Smart Display campaign requires the TargetCpa bidding strategy.
    campaign.target_cpa.target_cpa_micros = 5000000
    campaign.campaign_budget = budget_resource_name
    # Optional: Set the start and end date.
    start_date = datetime.date.today() + datetime.timedelta(days=1)
    campaign.start_date = start_date.strftime(_DATE_FORMAT)
    end_date = start_date + datetime.timedelta(days=365)
    campaign.end_date = end_date.strftime(_DATE_FORMAT)

    campaign_service = client.get_service("CampaignService", version="v6")

    try:
        campaign_response = campaign_service.mutate_campaigns(
            customer_id, [campaign_operation]
        )
        return campaign_response.results[0].resource_name
    except GoogleAdsException as ex:
        _handle_google_ads_exception(ex)
        # [END add_smart_display_ad_4]


# [START add_smart_display_ad]
def _create_ad_group(client, customer_id, campaign_resource_name):
    ad_group_operation = client.get_type("AdGroupOperation", version="v6")
    ad_group = ad_group_operation.create
    ad_group.name = f"Earth to Mars Cruises #{uuid4()}"
    ad_group_status_enum = client.get_type("AdGroupStatusEnum", version="v6")
    ad_group.status = ad_group_status_enum.PAUSED
    ad_group.campaign = campaign_resource_name

    ad_group_service = client.get_service("AdGroupService", version="v6")

    try:
        ad_group_response = ad_group_service.mutate_ad_groups(
            customer_id, [ad_group_operation]
        )
        return ad_group_response.results[0].resource_name
    except GoogleAdsException as ex:
        _handle_google_ads_exception(ex)
        # [END add_smart_display_ad]


# [START add_smart_display_ad_2]
def _upload_image_asset(
    client, customer_id, image_url, image_width, image_height
):
    # Download image from URL
    image_content = requests.get(image_url).content

    asset_operation = client.get_type("AssetOperation", version="v6")
    asset = asset_operation.create
    # Optional: Provide a unique friendly name to identify your asset. If you
    # specify the name field, then both the asset name and the image being
    # uploaded should be unique, and should not match another ACTIVE asset in
    # this customer account.
    # asset.name = f'Jupiter Trip #{uuid4()}'
    asset_type_enum = client.get_type("AssetTypeEnum", version="v6")
    asset.type = asset_type_enum.IMAGE
    image_asset = asset.image_asset
    image_asset.data = image_content
    image_asset.file_size = len(image_content)
    image_asset.mime_type = client.get_type("MimeTypeEnum").IMAGE_JPEG
    image_asset.full_size.width_pixels = image_width
    image_asset.full_size.height_pixels = image_height
    image_asset.full_size.url = image_url

    asset_service = client.get_service("AssetService", version="v6")
    content_type_enum = client.get_type("ResponseContentTypeEnum", version="v6")

    try:
        mutate_asset_response = asset_service.mutate_assets(
            customer_id,
            [asset_operation],
            # Setting this parameter tells the API to return the Asset
            # object in the response, allowing us to easily retrieve
            # its ID.
            response_content_type=content_type_enum.MUTABLE_RESOURCE,
        )
        return mutate_asset_response.results[0].asset.id
    except GoogleAdsException as ex:
        _handle_google_ads_exception(ex)
        # [END add_smart_display_ad_2]


# [START add_smart_display_ad_1]
def _create_responsive_display_ad(
    client,
    customer_id,
    ad_group_resource_name,
    marketing_image_asset_id,
    square_marketing_image_asset_id,
):
    ad_group_ad_operation = client.get_type("AdGroupAdOperation", version="v6")
    ad_group_ad = ad_group_ad_operation.create
    ad_group_ad.ad_group = ad_group_resource_name
    ad_group_ad.status = client.get_type(
        "AdGroupAdStatusEnum", version="v6"
    ).PAUSED
    ad = ad_group_ad.ad
    ad.final_urls.append("https://www.example.com")
    responsive_display_ad = ad.responsive_display_ad
    headline = responsive_display_ad.headlines.add()
    headline.text = "Travel"
    responsive_display_ad.long_headline.text = "Travel the World"
    description = responsive_display_ad.descriptions.add()
    description.text = "Take to the air!"
    responsive_display_ad.business_name = "Google"

    asset_service = client.get_service("AssetService", version="v6")
    marketing_image = responsive_display_ad.marketing_images.add()
    marketing_image.asset = asset_service.asset_path(
        customer_id, marketing_image_asset_id
    )
    square_marketing_image = responsive_display_ad.square_marketing_images.add()
    square_marketing_image.asset = asset_service.asset_path(
        customer_id, square_marketing_image_asset_id
    )
    responsive_display_ad.call_to_action_text = "Shop Now"
    responsive_display_ad.price_prefix = "as low as"
    responsive_display_ad.promo_text = "Free shipping!"

    ad_group_ad_service = client.get_service("AdGroupAdService", version="v6")

    try:
        ad_group_ad_response = ad_group_ad_service.mutate_ad_group_ads(
            customer_id, [ad_group_ad_operation]
        )
    except GoogleAdsException as ex:
        _handle_google_ads_exception(ex)
        # [END add_smart_display_ad_1]


def _handle_google_ads_exception(exception):
    """Prints the details of a GoogleAdsException object.

    Args:
        exception: an instance of GoogleAdsException.
    """
    print(
        f'Request with ID "{exception.request_id}" failed with status '
        f'"{exception.error.code().name}" and includes the following errors:'
    )
    for error in exception.failure.errors:
        print(f'\tError with message "{error.message}".')
        if error.location:
            for field_path_element in error.location.field_path_elements:
                print(f"\t\tOn field: {field_path_element.field_name}")
    sys.exit(1)


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    google_ads_client = GoogleAdsClient.load_from_storage()

    parser = argparse.ArgumentParser(
        description=(
            "Creates a Smart Display campaign, and an ad group that "
            "are then used to create a responsive display ad."
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
        "--marketing_image_asset_id",
        type=str,
        required=False,
        help=("The ID for an image asset to be used as a marketing image."),
    )
    parser.add_argument(
        "-s",
        "--square_marketing_image_asset_id",
        type=str,
        required=False,
        help=(
            "The resource name for an image asset to be used as a square "
            "marketing image."
        ),
    )
    args = parser.parse_args()

    main(
        google_ads_client,
        args.customer_id,
        args.marketing_image_asset_id,
        args.square_marketing_image_asset_id,
    )
