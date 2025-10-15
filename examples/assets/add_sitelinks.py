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
"""Adds sitelinks to a campaign using Assets.

Run basic_operations/add_campaigns.py to create a campaign.
"""

import argparse
from typing import List
import sys

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.ads.googleads.v22.services.types.asset_service import AssetOperation
from google.ads.googleads.v22.resources.types.asset import Asset
from google.ads.googleads.v22.services.types.campaign_asset_service import (
    CampaignAssetOperation,
)
from google.ads.googleads.v22.resources.types.campaign_asset import (
    CampaignAsset,
)


def main(client: GoogleAdsClient, customer_id: str, campaign_id: str) -> None:
    """Adds sitelinks to a campaign using assets.

    Args:
        client: The Google Ads client.
        customer_id: The customer ID for which to add the keyword.
        campaign_id: The campaign to which sitelinks will be added.
    """
    # Creates sitelink assets.
    resource_names: List[str] = create_sitelink_assets(client, customer_id)
    # Associates the sitelinks at the campaign level.
    link_sitelinks_to_campaign(client, customer_id, campaign_id, resource_names)


def create_sitelink_assets(
    client: GoogleAdsClient, customer_id: str
) -> List[str]:
    """Creates sitelink assets, which can be added to campaigns.

    Args:
        client: The Google Ads client.
        customer_id: The customer ID for which to add the keyword.

    Returns:
        a list of sitelink asset resource names.
    """
    store_locator_operation: AssetOperation = client.get_type("AssetOperation")
    store_locator_asset: Asset = store_locator_operation.create
    store_locator_asset.final_urls.append(
        "http://example.com/contact/store-finder"
    )
    store_locator_asset.final_mobile_urls.append(
        "http://example.com/mobile/contact/store-finder"
    )
    store_locator_asset.sitelink_asset.description1 = "Get in touch"
    store_locator_asset.sitelink_asset.description2 = "Find your local store"
    store_locator_asset.sitelink_asset.link_text = "Store locator"

    store_asset_operation: AssetOperation = client.get_type("AssetOperation")
    store_asset: Asset = store_asset_operation.create
    store_asset.final_urls.append("http://example.com/store")
    store_asset.final_mobile_urls.append("http://example.com/mobile/store")
    store_asset.sitelink_asset.description1 = "Buy some stuff"
    store_asset.sitelink_asset.description2 = "It's really good"
    store_asset.sitelink_asset.link_text = "Store"

    store_addnl_asset_operation: AssetOperation = client.get_type(
        "AssetOperation"
    )
    store_addnl_asset: Asset = store_addnl_asset_operation.create
    store_addnl_asset.final_urls.append("http://example.com/store/more")
    store_addnl_asset.final_mobile_urls.append(
        "http://example.com/mobile/store/more"
    )
    store_addnl_asset.sitelink_asset.description1 = "Buy some stuff"
    store_addnl_asset.sitelink_asset.description2 = "It's really good"
    store_addnl_asset.sitelink_asset.link_text = "Store"

    asset_service = client.get_service("AssetService")
    response = asset_service.mutate_assets(
        customer_id=customer_id,
        operations=[
            store_locator_operation,
            store_asset_operation,
            store_addnl_asset_operation,
        ],
    )

    resource_names: List[str] = [
        result.resource_name for result in response.results
    ]

    for resource_name in resource_names:
        print(f"Created sitelink asset with resource name '{resource_name}'.")

    return resource_names


def link_sitelinks_to_campaign(
    client: GoogleAdsClient,
    customer_id: str,
    campaign_id: str,
    resource_names: List[str],
) -> None:
    """Creates sitelink assets, which can be added to campaigns.

    Args:
        client: The Google Ads client.
        customer_id: The customer ID for which to add the keyword.
        campaign_id: The campaign to which sitelinks will be added.
        resource_names: a list of sitelink asset resource names.
    """
    campaign_service = client.get_service("CampaignService")
    operations: List[CampaignAssetOperation] = []
    for resource_name in resource_names:
        operation: CampaignAssetOperation = client.get_type(
            "CampaignAssetOperation"
        )
        campaign_asset: CampaignAsset = operation.create
        campaign_asset.asset = resource_name
        campaign_asset.campaign = campaign_service.campaign_path(
            customer_id, campaign_id
        )
        campaign_asset.field_type = client.enums.AssetFieldTypeEnum.SITELINK
        operations.append(operation)

    campaign_asset_service = client.get_service("CampaignAssetService")
    response = campaign_asset_service.mutate_campaign_assets(
        customer_id=customer_id, operations=operations
    )

    for result in response.results:
        print(
            "Linked sitelink to campaign with resource name '{result.resource_name}'."
        )


if __name__ == "__main__":
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Adds sitelinks to a campaign using feed services."
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
        "-i",
        "--campaign_id",
        type=str,
        required=True,
        default=None,
        help="ID of the campaign to which sitelinks will be added.",
    )
    args: argparse.Namespace = parser.parse_args()

    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client: GoogleAdsClient = GoogleAdsClient.load_from_storage(
        version="v22"
    )

    try:
        main(googleads_client, args.customer_id, args.campaign_id)
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
