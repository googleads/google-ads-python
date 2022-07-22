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
"""This example adds a page feed with URLs for a Dynamic Search Ads campaign."""


import argparse
from datetime import datetime
import sys

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


def main(client, customer_id, campaign_id, ad_group_id):
    """The main method that creates all necessary entities for the example.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        campaign_id: a campaign ID.
        ad_group_id: an ad group ID.
    """
    # The label for the DSA page URLs.
    dsa_page_url_label = "discounts"

    # Creates a list of assets.
    asset_resource_names = _create_assets(
        client, dsa_page_url_label, customer_id
    )

    # Creates an AssetSet - this is a collection of assets that can be
    # associated with a campaign. Note: do not confuse this with an AssetGroup.
    # An AssetGroup replaces AdGroups in some types of campaigns.
    asset_set_resource_name = _create_asset_set(client, customer_id)

    # Adds the Assets to the AssetSet.
    _add_assets_to_asset_set(
        client, asset_resource_names, asset_set_resource_name, customer_id
    )

    # Links the AssetSet to the Campaign.
    _link_asset_set_to_campaign(
        client, asset_set_resource_name, customer_id, campaign_id
    )

    # Optional: Targets web pages matching the feed's label in the ad group.
    _add_dsa_target(client, dsa_page_url_label, customer_id, ad_group_id)


# [START add_asset]
def _create_assets(client, dsa_page_url_label, customer_id):
    """Creates Assets to be used in a DSA page feed.

    Args:
        client: an initialized GoogleAdsClient instance.
        dsa_page_url_label: a label for the DSA page URLs.
        customer_id: a client customer ID.

    Returns:
        a list of asset resource names.
    """
    urls = [
        "http://www.example.com/discounts/rental-cars",
        "http://www.example.com/discounts/hotel-deals",
        "http://www.example.com/discounts/flight-deals",
    ]

    operations = []
    for url in urls:
        operation = client.get_type("AssetOperation")
        page_feed_asset = operation.create.page_feed_asset
        page_feed_asset.page_url = url
        page_feed_asset.labels.append(dsa_page_url_label)
        operations.append(operation)

    asset_service = client.get_service("AssetService")
    response = asset_service.mutate_assets(
        customer_id=customer_id, operations=operations
    )

    resource_names = []
    for result in response.results:
        resource_name = result.resource_name
        print(f"Created asset with resource name '{resource_name}'")
        resource_names.append(resource_name)

    return resource_names
    # [END add_asset]


# [START add_asset_set]
def _create_asset_set(client, customer_id):
    """Creates an AssetSet.

    The AssetSet will be used to link the dynamic page feed assets to a
    campaign.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.

    Returns:
        an asset set resource name.
    """
    operation = client.get_type("AssetSetOperation")
    asset_set = operation.create
    asset_set.name = f"My dynamic page feed {datetime.now()}"
    asset_set.type_ = client.enums.AssetSetTypeEnum.PAGE_FEED

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
    client, asset_resource_names, asset_set_resource_name, customer_id
):
    """Adds an Asset to an AssetSet by creating an AssetSetAsset link.

    Args:
        client: an initialized GoogleAdsClient instance.
        asset_resource_names: a list of asset resource names.
        asset_set_resource_name: a resource name for an asset set.
        customer_id: a client customer ID.
    """
    operations = []
    for asset_resource_name in asset_resource_names:
        operation = client.get_type("AssetSetAssetOperation")
        asset_set_asset = operation.create
        asset_set_asset.asset = asset_resource_name
        asset_set_asset.asset_set = asset_set_resource_name
        operations.append(operation)

    asset_set_asset_service = client.get_service("AssetSetAssetService")
    response = asset_set_asset_service.mutate_asset_set_assets(
        customer_id=customer_id, operations=operations
    )
    resource_name = response.results[0].resource_name
    print(f"Created asset set asset with resource name '{resource_name}'")
    # [END add_asset_set_asset]


# [START add_campaign_asset_set]
def _link_asset_set_to_campaign(
    client, asset_set_resource_name, customer_id, campaign_id
):
    """Links an AssetSet to a Campaign by creating a CampaignAssetSet.

    Args:
        client: an initialized GoogleAdsClient instance.
        asset_set_resource_name: a resource name for an asset set.
        customer_id: a client customer ID.
        campaign_id: a campaign ID.
    """
    googleads_service = client.get_service("GoogleAdsService")
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


# [START add_dsa_target]
def _add_dsa_target(client, dsa_page_url_label, customer_id, ad_group_id):
    """Creates an ad group criterion targeting the DSA label.

    Args:
        client: an initialized GoogleAdsClient instance.
        dsa_page_url_label: a label for the DSA page URLs.
        customer_id: a client customer ID.
        ad_group_id: an ad group ID.
    """
    googleads_service = client.get_service("GoogleAdsService")
    operation = client.get_type("AdGroupCriterionOperation")
    # Creates the ad group criterion.
    ad_group_criterion = operation.create
    ad_group_criterion.ad_group = googleads_service.ad_group_path(
        customer_id, ad_group_id
    )
    ad_group_criterion.cpc_bid_micros = 1500000

    # Creates the webpage info, or criterion for targeting webpages of an
    # advertiser's website.
    webpage = ad_group_criterion.webpage
    webpage.criterion_name = "Test Criterion"
    # Creates the webpage condition info that targets an advertiser's webpages
    # based on the custom label specified by the dsaPageUrlLabel
    # (e.g. "discounts").
    webpage_condition = client.get_type("WebpageConditionInfo")
    webpage_condition.operand = (
        client.enums.WebpageConditionOperandEnum.CUSTOM_LABEL
    )
    webpage_condition.argument = dsa_page_url_label
    webpage.conditions.append(webpage_condition)

    ad_group_criterion_service = client.get_service("AdGroupCriterionService")
    response = ad_group_criterion_service.mutate_ad_group_criteria(
        customer_id=customer_id, operations=[operation]
    )
    resource_name = response.results[0].resource_name
    print(f"Created ad group criterion with resource name '{resource_name}'")
    # [END add_dsa_target]


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v11")

    parser = argparse.ArgumentParser(
        description=(
            "Adds a page feed with URLs for a Dynamic Search Ads Campaign."
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
        "-i", "--campaign_id", type=str, required=True, help="The campaign ID."
    )
    parser.add_argument(
        "-a", "--ad_group_id", type=str, required=True, help="The ad group ID."
    )
    args = parser.parse_args()

    try:
        main(
            googleads_client,
            args.customer_id,
            args.campaign_id,
            args.ad_group_id,
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
