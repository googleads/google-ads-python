#!/usr/bin/env python
# Copyright 2022 Google LLC
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
"""Adds an asset for use in dynamic remarketing."""


import argparse
from datetime import datetime
import sys
from uuid import uuid4

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


def main(client, customer_id, campaign_id):
    """The main method that creates all necessary entities for the example.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        campaign_id: the ID for a campaign of a type that supports dynamic
            remarketing, such as Display.
    """
    asset_resource_name = _create_asset(client, customer_id)
    asset_set_resource_name = _create_asset_set(client, customer_id)
    _add_assets_to_asset_set(
        client, asset_resource_name, asset_set_resource_name, customer_id
    )
    _link_asset_set_to_campaign(
        client, asset_set_resource_name, customer_id, campaign_id
    )


# [START add_asset]
def _create_asset(client, customer_id):
    """Creates a DynamicEducationAsset.

    See https://support.google.com/google-ads/answer/6053288?#zippy=%2Ceducation
    for a detailed explanation of the field format.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.

    Returns:
        The resource name for an asset.
    """
    # Creates an operation to add the asset.
    operation = client.get_type("AssetOperation")
    asset = operation.create
    # The final_urls list must not be empty
    asset.final_urls.append("https://www.example.com")
    education_asset = asset.dynamic_education_asset
    # Defines meta-information about the school and program.
    education_asset.school_name = "The University of Unknown"
    education_asset.address = "Building 1, New York, 12345, USA"
    education_asset.program_name = "BSc. Computer Science"
    education_asset.subject = "Computer Science"
    education_asset.program_description = "Slinging code for fun and profit!"
    # Sets up the program ID which is the ID that should be specified in the
    # tracking pixel.
    education_asset.program_id = "bsc-cs-uofu"
    # Sets up the location ID which may additionally be specified in the
    # tracking pixel.
    education_asset.location_id = "nyc"
    education_asset.image_url = "https://gaagl.page.link/Eit5"
    education_asset.android_app_link = (
        "android-app://com.example.android/http/example.com/gizmos?1234"
    )
    education_asset.ios_app_link = "exampleApp://content/page"
    education_asset.ios_app_store_id = 123

    asset_service = client.get_service("AssetService")
    response = asset_service.mutate_assets(
        customer_id=customer_id, operations=[operation]
    )
    resource_name = response.results[0].resource_name
    print(
        f"Created a dynamic education asset with resource name '{resource_name}'"
    )

    return resource_name
    # [END add_asset]


# [START add_asset_set]
def _create_asset_set(client, customer_id):
    """Creates an AssetSet.

    The AssetSet will be used to link the dynamic remarketing assets to a
    campaign.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.

    Returns:
        The resource name for an asset set.
    """
    # Creates an operation to create the asset set.
    operation = client.get_type("AssetSetOperation")
    asset_set = operation.create
    asset_set.name = f"My dynamic remarketing assets {datetime.now()}"
    asset_set.type_ = client.enums.AssetSetTypeEnum.DYNAMIC_EDUCATION

    asset_set_service = client.get_service("AssetSetService")
    response = asset_set_service.mutate_asset_sets(
        customer_id=customer_id, operations=[operation]
    )
    resource_name = response.results[0].resource_name
    print(f"Created asset set with resource name '{resource_name}'")

    return resource_name
    # [END add_asset_set]


# [START add_asset_set_asset]
def _add_assets_to_asset_set(
    client, asset_resource_name, asset_set_resource_name, customer_id
):
    """Adds an Asset to an AssetSet by creating an AssetSetAsset link.

    Args:
        client: an initialized GoogleAdsClient instance.
        asset_set_resource_name; the resource name for an asset set.
        asset_resource_name; the resource name for an asset.
        customer_id: a client customer ID.
    """
    # Creates an operation to add the asset set asset.
    operation = client.get_type("AssetSetAssetOperation")
    asset_set_asset = operation.create
    asset_set_asset.asset = asset_resource_name
    asset_set_asset.asset_set = asset_set_resource_name

    asset_set_asset_service = client.get_service("AssetSetAssetService")
    # Note this is the point that the API will enforce uniqueness of the
    # DynamicEducationAsset.program_id field. You can have any number of assets
    # with the same program ID, however, only one asset is allowed per asset set
    # with the same program ID.
    response = asset_set_asset_service.mutate_asset_set_assets(
        customer_id=customer_id, operations=[operation]
    )
    resource_name = response.results[0].resource_name
    print(f"Created asset set asset link with resource name '{resource_name}'")
    # [END add_asset_set_asset]


# [START add_campaign_asset_set]
def _link_asset_set_to_campaign(
    client, asset_set_resource_name, customer_id, campaign_id
):
    """Creates a CampaignAssetSet.

    The CampaignAssetSet represents the link between an AssetSet and a Campaign.

    Args:
        client: an initialized GoogleAdsClient instance.
        asset_set_resource_name; the resource name for an asset set.
        customer_id: a client customer ID.
        campaign_id: the ID for a campaign of a type that supports dynamic
            remarketing, such as Display.
    """
    googleads_service = client.get_service("GoogleAdsService")
    # Creates an operation to add the campaign asset set.
    operation = client.get_type("CampaignAssetSetOperation")
    campaign_asset_set = operation.create
    campaign_asset_set.campaign = googleads_service.campaign_path(
        customer_id, campaign_id
    )
    campaign_asset_set.asset_set = asset_set_resource_name

    campaign_asset_set_service = client.get_service("CampaignAssetSetService")
    response = campaign_asset_set_service.mutate_campaign_asset_sets(
        customer_id=customer_id, operations=[operation]
    )
    resource_name = response.results[0].resource_name
    print(f"Created a campaign asset set with resource name '{resource_name}'")
    # [END add_campaign_asset_set]


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v11")

    parser = argparse.ArgumentParser(
        description="Adds an asset for use in dynamic remarketing."
    )
    # The following argument(s) should be provided to run the example.
    parser.add_argument(
        "-c",
        "--customer_id",
        type=str,
        required=True,
        help="The Google Ads customer ID.",
    )
    # The following argument(s) are optional.
    parser.add_argument(
        "-i",
        "--campaign_id",
        type=str,
        required=True,
        help="The campaign ID. Specify a campaign type which supports dynamic "
        "remarketing, such as Display.",
    )
    args = parser.parse_args()

    try:
        main(googleads_client, args.customer_id, args.campaign_id)
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
