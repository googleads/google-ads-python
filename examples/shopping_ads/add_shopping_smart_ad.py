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
"""Creates a smart shopping campaign, ad group, ad, and listing group.

These will be created for "All products".

Prerequisites:
- You need to have access to a Merchant Center account. You can find
  instructions to create a Merchant Center account here:
  https://support.google.com/merchants/answer/188924.
  This account must be linked to your Google Ads account. The integration
  instructions can be found at:
  https://developers.google.com/google-ads/api/docs/shopping-ads/merchant-center
- You need your Google Ads account to track conversions. The different ways
  to track conversions can be found here:
  https://support.google.com/google-ads/answer/1722054.
"""


import argparse
import sys
from uuid import uuid4

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


def main(
    client,
    customer_id,
    merchant_center_account_id,
    create_default_listing_group,
):
    """Creates a smart shopping campaign, ad group, ad, and listing group.

    Args:
        client: An initialized Google Ads client.
        customer_id: The Google Ads customer ID.
        merchant_center_account_id: The Merchant Center account ID.
        create_default_listing_group: Boolean, whether to create a default
            listing group.
    """
    # Create a budget to be used by the campaign that will be created below.
    budget_resource_name = _add_campaign_budget(client, customer_id)

    # Create a smart shopping campaign.
    campaign_resource_name = _add_smart_shopping_campaign(
        client, customer_id, budget_resource_name, merchant_center_account_id,
    )

    # Create a smart shopping ad group.
    ad_group_resource_name = _add_smart_shopping_ad_group(
        client, customer_id, campaign_resource_name
    )

    # Creates a smart shopping ad group ad.
    _add_smart_shopping_ad_group_ad(client, customer_id, ad_group_resource_name)

    if create_default_listing_group:
        # A product group is a subset of inventory. Listing groups are the
        # equivalent of product groups in the API and allow you to bid on
        # the chosen group or exclude a group from bidding.
        # This method creates an ad group criterion containing a listing
        # group.
        _add_shopping_listing_group(client, customer_id, ad_group_resource_name)


def _add_campaign_budget(client, customer_id):
    """Creates a campaign budget in the specified client account.

    Args:
        client: An initialized Google Ads client.
        customer_id: The Google Ads customer ID.

    Returns:
        The string resource name of the newly created campaign budget.
    """
    # Get the CampaignBudgetService client.
    campaign_budget_service = client.get_service("CampaignBudgetService")

    # Create a campaign budget operation and configure the smart shopping
    # campaign budget.
    campaign_budget_operation = client.get_type("CampaignBudgetOperation")
    campaign_budget = campaign_budget_operation.create
    campaign_budget.name = f"Interplanetary Cruise Budget #{uuid4()}"
    campaign_budget.delivery_method = client.get_type(
        "BudgetDeliveryMethodEnum"
    ).BudgetDeliveryMethod.STANDARD
    # The budget is specified in the local currency of the account. The amount
    # should be specified in micros; one million is equivalent to one unit.
    campaign_budget.amount_micros = 5000000
    # Budgets for smart shopping campaigns cannot be shared.
    campaign_budget.explicitly_shared = False

    # Add the campaign budget, then print and return the resulting campaign
    # budget's resource name.
    campaign_budget_response = campaign_budget_service.mutate_campaign_budgets(
        customer_id=customer_id, operations=[campaign_budget_operation]
    )
    campaign_budget_resource_name = campaign_budget_response.results[
        0
    ].resource_name
    print(
        "Added a smart shopping campaign budget with resource name: "
        f"'{campaign_budget_resource_name}'."
    )

    return campaign_budget_resource_name


# [START add_shopping_smart_ad_3]
def _add_smart_shopping_campaign(
    client, customer_id, budget_resource_name, merchant_center_account_id
):
    """Creates a new shopping campaign for smart shopping ads.

    Args:
        client: An initialized Google Ads client.
        customer_id: The Google Ads customer ID.
        budget_resource_name: The target campaign budget for the new campaign.
        merchant_center_account_id: The Merchant Center account to which the
            campaign will be linked.

    Returns:
        The string resource name of the newly created ad group.
    """
    # Get the CampaignService client.
    campaign_service = client.get_service("CampaignService")

    # [START add_shopping_smart_ad]
    # Create a campaign operation and configure the smart shopping campaign.
    campaign_operation = client.get_type("CampaignOperation")
    campaign = campaign_operation.create
    campaign.name = f"Interplanetary Cruise Campaign #{uuid4()}"
    campaign.campaign_budget = budget_resource_name
    # Configure settings related to shopping campaigns including advertising
    # channel type, advertising channel sub-type and shopping setting.
    campaign.advertising_channel_type = client.get_type(
        "AdvertisingChannelTypeEnum"
    ).AdvertisingChannelType.SHOPPING
    campaign.advertising_channel_sub_type = client.get_type(
        "AdvertisingChannelSubTypeEnum"
    ).AdvertisingChannelSubType.SHOPPING_SMART_ADS
    campaign.shopping_setting.merchant_id = merchant_center_account_id
    # Set the sales country of products to include in the campaign.
    # Only products from Merchant Center targeting this country will
    # appear in the campaign.
    campaign.shopping_setting.sales_country = "US"
    # Recommendation: Set the campaign to PAUSED when creating it to prevent
    # the ads from immediately serving. Set to ENABLED once you've added
    # targeting and the ads are ready to serve.
    campaign.status = client.get_type(
        "CampaignStatusEnum"
    ).CampaignStatus.PAUSED
    # Bidding strategy must be set directly on the campaign.
    # Setting a portfolio bidding strategy by resource name is not supported.
    # Maximize conversion value is the only strategy supported for smart
    # shopping campaigns. An optional ROAS (Return on Advertising Spend) can be
    # set for maximize_conversion_value. The ROAS value must be specified as a
    # ratio in the API. It is calculated by dividing "total value" by
    # "total spend". For more information on maximize conversion value, see the
    # support article: http://support.google.com/google-ads/answer/7684216.
    campaign.maximize_conversion_value.target_roas = 3.5
    # [END add_shopping_smart_ad]

    # Add the campaign, then print and return the resulting campaign's resource
    # name.
    campaign_response = campaign_service.mutate_campaigns(
        customer_id=customer_id, operations=[campaign_operation]
    )
    campaign_resource_name = campaign_response.results[0].resource_name
    print(
        "Added a smart shopping campaign with resource name: "
        f"'{campaign_resource_name}'."
    )

    return campaign_resource_name
    # [END add_shopping_smart_ad_3]


# [START add_shopping_smart_ad_2]
def _add_smart_shopping_ad_group(client, customer_id, campaign_resource_name):
    """Creates a new ad group in the specified smart shopping campaign.

    Args:
        client: An initialized Google Ads client.
        customer_id: The Google Ads customer ID.
        campaign_resource_name: The target campaign for the new ad group.

    Returns:
        The string resource name of the newly created ad group.
    """
    # Get the AdGroupCriterionService client.
    ad_group_service = client.get_service("AdGroupService")

    # Create an ad group operation and configure the new ad group.
    ad_group_operation = client.get_type("AdGroupOperation")
    ad_group = ad_group_operation.create
    ad_group.name = f"Earth to Mars Cruises #{uuid4()}"
    ad_group.campaign = campaign_resource_name
    # Set the ad group type to SHOPPING_SMART_ADS.
    ad_group.type_ = client.get_type(
        "AdGroupTypeEnum"
    ).AdGroupType.SHOPPING_SMART_ADS
    ad_group.status = client.get_type("AdGroupStatusEnum").AdGroupStatus.ENABLED

    # Add the ad group, then print and return the resulting ad group's resource
    # name.
    ad_group_response = ad_group_service.mutate_ad_groups(
        customer_id=customer_id, operations=[ad_group_operation]
    )
    ad_group_resource_name = ad_group_response.results[0].resource_name
    print(
        "Added a smart shopping ad group with resource name: "
        f"'{ad_group_resource_name}'."
    )

    return ad_group_resource_name
    # [END add_shopping_smart_ad_2]


# [START add_shopping_smart_ad_1]
def _add_smart_shopping_ad_group_ad(
    client, customer_id, ad_group_resource_name
):
    """Creates a new ad group ad in the specified smart shopping ad group.

    Args:
        client: An initialized Google Ads client.
        customer_id: The Google Ads customer ID.
        ad_group_resource_name: The target ad group for the new listing group.

    Returns:
        The string resource name of the newly created ad group ad.
    """
    # Get the AdGroupCriterionService client.
    ad_group_ad_service = client.get_service("AdGroupAdService")

    # Create an ad group ad operation and configure the ad group ad.
    ad_group_ad_operation = client.get_type("AdGroupAdOperation")
    ad_group_ad = ad_group_ad_operation.create
    # Set the ad group.
    ad_group_ad.ad_group = ad_group_resource_name
    # Set a new smart shopping ad.
    client.copy_from(
        ad_group_ad.ad.shopping_smart_ad, client.get_type("ShoppingSmartAdInfo")
    )
    ad_group_ad.status = client.get_type(
        "AdGroupAdStatusEnum"
    ).AdGroupAdStatus.PAUSED

    # Add the ad group ad, then print and return the resulting ad group ad's
    # resource name.
    ad_group_ad_response = ad_group_ad_service.mutate_ad_group_ads(
        customer_id=customer_id, operations=[ad_group_ad_operation]
    )
    ad_group_ad_resource_name = ad_group_ad_response.results[0].resource_name
    print(
        "Added a smart shopping ad group ad with resource name: "
        f"'{ad_group_ad_resource_name}'."
    )

    return ad_group_ad_resource_name
    # [END add_shopping_smart_ad_1]


def _add_shopping_listing_group(client, customer_id, ad_group_resource_name):
    """Creates a new shopping listing group for the specified ad group.

    This is known as a "product group" in the Google Ads user interface. The
    listing group will be added to the ad group using an "ad group criterion".
    See the Google Ads API Shopping guide for more information on listing groups:
    https://developers.google.com/google-ads/api/docs/shopping-ads/overview.

    Args:
        client: An initialized Google Ads client.
        customer_id: The Google Ads customer ID.
        ad_group_resource_name: The target ad group for the new listing group.

    Returns:
        The string resource name of the newly created ad group criterion.
    """
    # Get the AdGroupCriterionService client.
    ad_group_criterion_service = client.get_service("AdGroupCriterionService")

    # Creates a new ad group criterion. This will contain a listing group.
    # This will be the listing group for 'All products' and will contain a
    # single root node.
    ad_group_criterion_operation = client.get_type("AdGroupCriterionOperation")
    ad_group_criterion = ad_group_criterion_operation.create
    ad_group_criterion.ad_group = ad_group_resource_name
    ad_group_criterion.status = client.get_type(
        "AdGroupCriterionStatusEnum"
    ).AdGroupCriterionStatus.ENABLED
    ad_group_criterion.listing_group.type_ = client.get_type(
        "ListingGroupTypeEnum"
    ).ListingGroupType.UNIT

    # Ad the listing group criterion, then display and return the resulting
    # ad group criterion's resource name.
    ad_group_criterion_response = ad_group_criterion_service.mutate_ad_group_criteria(
        customer_id=customer_id, operations=[ad_group_criterion_operation]
    )
    ad_group_criterion_resource_name = ad_group_criterion_response.results[
        0
    ].resource_name
    print(
        "Added an ad group criterion containing a listing group with resource "
        f"name: '{ad_group_criterion_resource_name}'."
    )

    return ad_group_criterion_resource_name


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v8")

    parser = argparse.ArgumentParser(
        description=(
            "Creates a smart shopping campaign, ad group, ad, and listing "
            "group for 'All products'."
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
        help="The Merchant Center account ID.",
    )
    parser.add_argument(
        "-d",
        "--create_default_listing_group",
        action="store_true",
        default=False,
        help="Optional, whether to create a default listing group. "
        "Default is false.",
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
            f"Request with ID '{ex.request_id}' failed with status "
            f"'{ex.error.code().name}' and includes the following errors:"
        )
        for error in ex.failure.errors:
            print(f"\tError with message '{error.message}'.")
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print(f"\t\tOn field: {field_path_element.field_name}")
        sys.exit(1)
