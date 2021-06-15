#!/usr/bin/env python
# Copyright 2018 Google LLC
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
"""This example creates a standard shopping product ad.

In the process of creating a standard shopping campaign and a shopping product
ad group are also created.

Prerequisite: You need to have access to a Merchant Center account. You can find
instructions to create a Merchant Center account here:
https://support.google.com/merchants/answer/188924.

This account must be linked to your Google Ads account.
"""


import argparse
import sys
import uuid

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


def main(
    client,
    customer_id,
    merchant_center_account_id,
    create_default_listing_group,
):
    # Creates a budget to be used by the campaign that will be created below.
    budget_resource_name = _add_campaign_budget(client, customer_id)

    # Create a standard shopping campaign.
    campaign_resource_name = _add_standard_shopping_campaign(
        client, customer_id, budget_resource_name, merchant_center_account_id
    )

    # Create a shoppng product ad group.
    ad_group_resource_name = _add_shopping_product_ad_group(
        client, customer_id, campaign_resource_name
    )

    # Create a shopping product ad group ad.
    _add_shopping_product_ad_group_ad(
        client, customer_id, ad_group_resource_name
    )

    if create_default_listing_group:
        # Creates an ad group criterion containing a listing group.
        # This will be the listing group tree for 'All products' and will
        # contain a single biddable unit node.
        _add_default_shopping_listing_group(
            client, customer_id, ad_group_resource_name
        )


def _add_campaign_budget(client, customer_id):
    """Creates a new campaign budget in the specified client account."""
    campaign_budget_service = client.get_service("CampaignBudgetService")

    # Create a budget, which can be shared by multiple campaigns.
    campaign_budget_operation = client.get_type("CampaignBudgetOperation")
    campaign_budget = campaign_budget_operation.create
    campaign_budget.name = f"Interplanetary Budget {uuid.uuid4()}"
    campaign_budget.delivery_method = client.get_type(
        "BudgetDeliveryMethodEnum"
    ).BudgetDeliveryMethod.STANDARD
    campaign_budget.amount_micros = 500000

    # Add budget.
    campaign_budget_response = campaign_budget_service.mutate_campaign_budgets(
        customer_id=customer_id, operations=[campaign_budget_operation]
    )

    budget_resource_name = campaign_budget_response.results[0].resource_name

    print(f"Added a budget with resource name: '{budget_resource_name}'")

    return budget_resource_name


# [START add_shopping_product_ad]
def _add_shopping_product_ad_group_ad(
    client, customer_id, ad_group_resource_name
):
    """Creates a new shopping product ad group ad in the specified ad group."""
    ad_group_ad_service = client.get_service("AdGroupAdService")

    # Creates a new ad group ad and sets the product ad to it.
    ad_group_ad_operation = client.get_type("AdGroupAdOperation")
    ad_group_ad = ad_group_ad_operation.create
    ad_group_ad.ad_group = ad_group_resource_name
    ad_group_ad.status = client.get_type(
        "AdGroupAdStatusEnum"
    ).AdGroupAdStatus.PAUSED
    client.copy_from(
        ad_group_ad.ad.shopping_product_ad,
        client.get_type("ShoppingProductAdInfo"),
    )

    # Add the ad group ad.
    ad_group_ad_response = ad_group_ad_service.mutate_ad_group_ads(
        customer_id=customer_id, operations=[ad_group_ad_operation]
    )

    ad_group_ad_resource_name = ad_group_ad_response.results[0].resource_name

    print(
        f"Created shopping product ad group ad '{ad_group_ad_resource_name}'."
    )

    return ad_group_resource_name
    # [END add_shopping_product_ad]


# [START add_shopping_product_ad_1]
def _add_shopping_product_ad_group(client, customer_id, campaign_resource_name):
    """Creates a new shopping product ad group in the specified campaign."""
    ad_group_service = client.get_service("AdGroupService")

    # Create ad group.
    ad_group_operation = client.get_type("AdGroupOperation")
    ad_group = ad_group_operation.create
    ad_group.name = f"Earth to Mars cruise {uuid.uuid4()}"
    ad_group.status = client.get_type("AdGroupStatusEnum").AdGroupStatus.ENABLED
    ad_group.campaign = campaign_resource_name
    # Sets the ad group type to SHOPPING_PRODUCT_ADS. This is the only value
    # possible for ad groups that contain shopping product ads.
    ad_group.type_ = client.get_type(
        "AdGroupTypeEnum"
    ).AdGroupType.SHOPPING_PRODUCT_ADS
    ad_group.cpc_bid_micros = 10000000

    # Add the ad group.
    ad_group_response = ad_group_service.mutate_ad_groups(
        customer_id=customer_id, operations=[ad_group_operation]
    )

    ad_group_resource_name = ad_group_response.results[0].resource_name

    print(
        "Added a product shopping ad group with resource name "
        f"'{ad_group_resource_name}'."
    )

    return ad_group_resource_name
    # [END add_shopping_product_ad_1]


# [START add_shopping_product_ad_2]
def _add_standard_shopping_campaign(
    client, customer_id, budget_resource_name, merchant_center_account_id
):
    """Creates a new standard shopping campaign in the specified client account."""
    campaign_service = client.get_service("CampaignService")

    # Create standard shoppping campaign.
    campaign_operation = client.get_type("CampaignOperation")
    campaign = campaign_operation.create
    campaign.name = f"Interplanetary Cruise Campaign {uuid.uuid4()}"

    # Configures settings related to shopping campaigns including advertising
    # channel type and shopping setting.
    campaign.advertising_channel_type = client.get_type(
        "AdvertisingChannelTypeEnum"
    ).AdvertisingChannelType.SHOPPING
    campaign.shopping_setting.merchant_id = merchant_center_account_id

    # Sets the sales country of products to include in the campaign.
    campaign.shopping_setting.sales_country = "US"

    # Sets the priority of the campaign. Higher numbers take priority over lower
    # numbers. For standard shopping campaigns, allowed values are between 0 and
    # 2, inclusive.
    campaign.shopping_setting.campaign_priority = 0

    # Enables local inventory ads for this campaign.
    campaign.shopping_setting.enable_local = True

    # Recommendation: Set the campaign to PAUSED when creating it to prevent the
    # ads from immediately serving. Set to ENABLED once you've added targeting
    # and the ads are ready to serve.
    campaign.status = client.get_type(
        "CampaignStatusEnum"
    ).CampaignStatus.PAUSED

    # Sets the bidding strategy to Manual CPC (with eCPC enabled)
    # Recommendation: Use one of the automated bidding strategies for Shopping
    # campaigns to help you optimize your advertising spend. More information
    # can be found here: https://support.google.com/google-ads/answer/6309029
    campaign.manual_cpc.enhanced_cpc_enabled = True

    # Sets the budget.
    campaign.campaign_budget = budget_resource_name

    # Add the campaign.
    campaign_response = campaign_service.mutate_campaigns(
        customer_id=customer_id, operations=[campaign_operation]
    )

    campaign_resource_name = campaign_response.results[0].resource_name

    print(
        "Added a standard shopping campaign with resource name "
        f"'{campaign_resource_name}'."
    )

    return campaign_resource_name
    # [END add_shopping_product_ad_2]


def _add_default_shopping_listing_group(
    client, customer_id, ad_group_resource_name
):
    """Creates a new default shopping listing group for the specified ad group.

    A listing group is the Google Ads API representation of a "product group"
    described in the Google Ads user interface. The listing group will be added
    to the ad group using an "ad group criterion". The criterion will contain
    the bid for a given listing group.
    """
    ad_group_criterion_service = client.get_service("AdGroupCriterionService")

    # Creates a new ad group criterion. This will contain the "default" listing
    # group (All products).
    ad_group_criterion_operation = client.get_type("AdGroupCriterionOperation")
    ad_group_criterion = ad_group_criterion_operation.create
    ad_group_criterion.ad_group = ad_group_resource_name
    ad_group_criterion.status = client.get_type(
        "AdGroupCriterionStatusEnum"
    ).AdGroupCriterionStatus.ENABLED
    ad_group_criterion.listing_group.type_ = client.get_type(
        "ListingGroupTypeEnum"
    ).ListingGroupType.UNIT
    #  Set the bid for products in this listing group unit.
    ad_group_criterion.cpc_bid_micros = 500000

    ad_group_criterion_response = ad_group_criterion_service.mutate_ad_group_criteria(
        customer_id=customer_id, operations=[ad_group_criterion_operation]
    )

    print(
        "Added an ad group criterion containing a listing group with "
        f"'{ad_group_criterion_response.results[0].resource_name}'."
    )


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v8")

    parser = argparse.ArgumentParser(
        description=(
            "Adds a standard shopping campaign, a shopping product ad "
            "group and a shopping product ad to the specified "
            "merchant account."
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
        help="The merchant center account ID.",
    )
    parser.add_argument(
        "-d",
        "--create_default_listing_group",
        action="store_true",
        default=False,
        help="Create a default listing group.",
    )
    args = parser.parse_args()

    try:
        main(
            googleads_client,
            args.customer_id,
            args.merchant_center_account_id,
            args.create_default_listing_group,
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
