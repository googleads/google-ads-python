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
"""Adds a page feed with URLs for a Dynamic Search Ads campaign."""

import argparse
import sys
from typing import List, Optional

from examples.utils.example_helpers import get_printable_datetime
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.ads.googleads.v22.common.types.asset_types import PageFeedAsset
from google.ads.googleads.v22.common.types.criteria import WebpageConditionInfo
from google.ads.googleads.v22.resources.types.ad_group_criterion import (
    AdGroupCriterion,
)
from google.ads.googleads.v22.resources.types.asset import Asset
from google.ads.googleads.v22.resources.types.asset_set import AssetSet
from google.ads.googleads.v22.resources.types.asset_set_asset import (
    AssetSetAsset,
)
from google.ads.googleads.v22.resources.types.campaign_asset_set import (
    CampaignAssetSet,
)
from google.ads.googleads.v22.services.services.ad_group_criterion_service import (
    AdGroupCriterionServiceClient,
)
from google.ads.googleads.v22.services.services.asset_service import (
    AssetServiceClient,
)
from google.ads.googleads.v22.services.services.asset_set_asset_service import (
    AssetSetAssetServiceClient,
)
from google.ads.googleads.v22.services.services.asset_set_service import (
    AssetSetServiceClient,
)
from google.ads.googleads.v22.services.services.campaign_asset_set_service import (
    CampaignAssetSetServiceClient,
)
from google.ads.googleads.v22.services.services.google_ads_service import (
    GoogleAdsServiceClient,
)
from google.ads.googleads.v22.services.types.ad_group_criterion_service import (
    AdGroupCriterionOperation,
    MutateAdGroupCriteriaResponse,
)
from google.ads.googleads.v22.services.types.asset_service import (
    AssetOperation,
    MutateAssetResult,
    MutateAssetsResponse,
)
from google.ads.googleads.v22.services.types.asset_set_asset_service import (
    AssetSetAssetOperation,
    MutateAssetSetAssetResult,
    MutateAssetSetAssetsResponse,
)
from google.ads.googleads.v22.services.types.asset_set_service import (
    AssetSetOperation,
    MutateAssetSetsResponse,
)
from google.ads.googleads.v22.services.types.campaign_asset_set_service import (
    CampaignAssetSetOperation,
    MutateCampaignAssetSetsResponse,
)


# The label for the DSA page URLs.
DSA_PAGE_URL_LABEL = "discounts"


def main(
    client: GoogleAdsClient,
    customer_id: str,
    campaign_id: str,
    ad_group_id: Optional[str],
) -> None:
    """The main method that creates all necessary entities for the example.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        campaign_id: the ID for a Campaign.
        ad_group_id: the ID for an Ad Group.
    """
    # Creates assets.
    asset_resource_names: List[str] = create_assets(
        client, customer_id, DSA_PAGE_URL_LABEL
    )

    # Creates an asset set - this is a collection of assets that can be
    # associated with a campaign.
    # Note: do not confuse this with an asset group. An asset group replaces ad
    # groups in some types of campaigns.
    asset_set_resource_name: str = create_asset_set(client, customer_id)

    # Adds the assets to the asset set
    add_assets_to_asset_set(
        client, customer_id, asset_resource_names, asset_set_resource_name
    )

    # Links the asset set to the specified campaign.
    link_asset_set_to_campaign(
        client, customer_id, campaign_id, asset_set_resource_name
    )

    # Optional: Targets web pages matching the feed's label in the ad group.
    if ad_group_id:
        add_dsa_target(client, customer_id, ad_group_id, DSA_PAGE_URL_LABEL)


# [START add_asset]
def create_assets(
    client: GoogleAdsClient, customer_id: str, dsa_page_url_label: str
) -> List[str]:
    """Creates assets to be used in a DSA page feed.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        dsa_page_url_label: the label for the DSA page URLs.

    Returns:
        a list of the created assets' resource names.
    """
    urls: List[str] = [
        "http://www.example.com/discounts/rental-cars",
        "http://www.example.com/discounts/hotel-deals",
        "http://www.example.com/discounts/flight-deals",
    ]
    operations: List[AssetOperation] = []

    # Creates one asset per URL.
    for url in urls:
        # Creates an asset operation and adds it to the list of operations.
        operation: AssetOperation = client.get_type("AssetOperation")
        asset: Asset = operation.create
        page_feed_asset: PageFeedAsset = asset.page_feed_asset
        page_feed_asset.page_url = url
        # Recommended: adds labels to the asset. These labels can be used later
        # in ad group targeting to restrict the set of pages that can serve.
        page_feed_asset.labels.append(dsa_page_url_label)
        operations.append(operation)

    # Issues a mutate request to add the assets and prints its information.
    asset_service: AssetServiceClient = client.get_service("AssetService")
    response: MutateAssetsResponse = asset_service.mutate_assets(
        customer_id=customer_id, operations=operations
    )

    print(f"Added {len(response.results)} assets:")

    resource_names: List[str] = []
    result: MutateAssetResult
    for result in response.results:
        resource_name: str = result.resource_name
        print(f"\tCreated an asset with resource name: '{resource_name}'")
        resource_names.append(resource_name)

    return resource_names
    # [END add_asset]


# [START add_asset_set]
def create_asset_set(client: GoogleAdsClient, customer_id: str) -> str:
    """Creates an asset set.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.

    Returns:
        the created asset set's resource name.
    """
    operation: AssetSetOperation = client.get_type("AssetSetOperation")
    # Creates an asset set which will be used to link the dynamic page feed
    # assets to a campaign.
    asset_set: AssetSet = operation.create
    asset_set.name = f"My dynamic page feed {get_printable_datetime()}"
    asset_set.type_ = client.enums.AssetSetTypeEnum.PAGE_FEED

    # Issues a mutate request to add the asset set and prints its information.
    asset_set_service: AssetSetServiceClient = client.get_service(
        "AssetSetService"
    )
    response: MutateAssetSetsResponse = asset_set_service.mutate_asset_sets(
        customer_id=customer_id, operations=[operation]
    )

    resource_name: str = response.results[0].resource_name
    print(f"Created an asset set with resource name: '{resource_name}'")
    return resource_name
    # [END add_asset_set]


# [START add_asset_set_asset]
def add_assets_to_asset_set(
    client: GoogleAdsClient,
    customer_id: str,
    asset_resource_names: List[str],
    asset_set_resource_name: str,
) -> None:
    """Adds assets to an asset set by creating an asset set asset link.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        asset_resource_names: a list of asset resource names.
        asset_set_resource_name: a resource name for an asset set.
    """
    operations: List[AssetSetAssetOperation] = []
    for resource_name in asset_resource_names:
        # Creates an asset set asset operation and adds it to the list of
        # operations.
        operation: AssetSetAssetOperation = client.get_type(
            "AssetSetAssetOperation"
        )
        asset_set_asset: AssetSetAsset = operation.create
        asset_set_asset.asset = resource_name
        asset_set_asset.asset_set = asset_set_resource_name
        operations.append(operation)

    # Issues a mutate request to add the asset set assets and prints its
    # information.
    asset_set_asset_service: AssetSetAssetServiceClient = client.get_service(
        "AssetSetAssetService"
    )
    response: MutateAssetSetAssetsResponse = (
        asset_set_asset_service.mutate_asset_set_assets(
            customer_id=customer_id, operations=operations
        )
    )

    print(f"Added {len(response.results)} asset set assets:")

    result: MutateAssetSetAssetResult
    for result in response.results:
        print(
            "\tCreated an asset set asset link with resource name "
            f"'{result.resource_name}'"
        )
        # [END add_asset_set_asset]


# [START add_campaign_asset_set]
def link_asset_set_to_campaign(
    client: GoogleAdsClient,
    customer_id: str,
    campaign_id: str,
    asset_set_resource_name: str,
) -> None:
    """Links the asset set to the campaign by creating a campaign asset set.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        campaign_id: the ID for a Campaign.
        asset_set_resource_name: a resource name for an asset set.
    """
    googleads_service: GoogleAdsServiceClient = client.get_service(
        "GoogleAdsService"
    )
    # Creates a campaign asset set representing the link between an asset set
    # and a campaign.
    operation: CampaignAssetSetOperation = client.get_type(
        "CampaignAssetSetOperation"
    )
    campaign_asset_set: CampaignAssetSet = operation.create
    campaign_asset_set.asset_set = asset_set_resource_name
    campaign_asset_set.campaign = googleads_service.campaign_path(
        customer_id, campaign_id
    )

    campaign_asset_set_service: CampaignAssetSetServiceClient = (
        client.get_service("CampaignAssetSetService")
    )
    response: MutateCampaignAssetSetsResponse = (
        campaign_asset_set_service.mutate_campaign_asset_sets(
            customer_id=customer_id, operations=[operation]
        )
    )

    resource_name: str = response.results[0].resource_name
    print(f"Created a campaign asset set with resource name: '{resource_name}'")
    # [END add_campaign_asset_set]


# [START add_dsa_target]
def add_dsa_target(
    client: GoogleAdsClient,
    customer_id: str,
    ad_group_id: str,
    dsa_page_url_label: str,
) -> None:
    """Creates an ad group criterion targeting the DSA label.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        ad_group_id: the ID for an Ad Group.
        dsa_page_url_label: the label for the DSA page URLs.
    """
    googleads_service: GoogleAdsServiceClient = client.get_service(
        "GoogleAdsService"
    )
    # Creates the ad group criterion.
    operation: AdGroupCriterionOperation = client.get_type(
        "AdGroupCriterionOperation"
    )
    criterion: AdGroupCriterion = operation.create
    criterion.ad_group = googleads_service.ad_group_path(
        customer_id, ad_group_id
    )
    criterion.cpc_bid_micros = 1500000
    # Creates the webpage info, or criterion for targeting webpages of an
    # advertiser's website.
    criterion.webpage.criterion_name = "Test Criterion"
    # Creates the webpage condition info that targets an advertiser's webpages
    # based on the custom label specified by the DSA page URL label
    # (e.g. "discounts").
    webpage_condition: WebpageConditionInfo = client.get_type(
        "WebpageConditionInfo"
    )
    webpage_condition.operand = (
        client.enums.WebpageConditionOperandEnum.CUSTOM_LABEL
    )
    webpage_condition.argument = dsa_page_url_label
    criterion.webpage.conditions.append(webpage_condition)

    # Issues a mutate request to add the ad group criterion and prints its
    # information.
    ad_group_criterion_service: AdGroupCriterionServiceClient = (
        client.get_service("AdGroupCriterionService")
    )
    response: MutateAdGroupCriteriaResponse = (
        ad_group_criterion_service.mutate_ad_group_criteria(
            customer_id=customer_id, operations=[operation]
        )
    )
    print(
        "Created ad group criterion with resource name: "
        f"'{response.results[0].resource_name}'"
    )
    # [END add_dsa_target]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=(
            "Adds a page feed with URLs for a Dynamic Search Ads campaign"
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
        "-i",
        "--campaign_id",
        type=str,
        required=True,
        help="The Google Ads campaign ID.",
    )

    parser.add_argument(
        "-a", "--ad_group_id", type=str, help="The Google Ads ad group ID."
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
            args.campaign_id,
            args.ad_group_id,
        )
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
