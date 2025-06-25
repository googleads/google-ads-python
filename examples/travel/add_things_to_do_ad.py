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
"""This example creates a Things to do campaign, ad group, and ad.

Prerequisite: You need to have an access to the Things to Do Center. The
integration instructions can be found at:
https://support.google.com/google-ads/answer/13387362
"""


import argparse
import sys

from examples.utils.example_helpers import get_printable_datetime
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


def main(client, customer_id, things_to_do_center_account_id):
    """The main method that creates all necessary entities for the example.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        things_to_do_center_account_id: the Things to Do Center account ID.
    """
    # Creates a budget to be used by the campaign that will be created below.
    budget_resource_name = add_campaign_budget(client, customer_id)
    # Creates a Things to do campaign.
    campaign_resource_name = add_things_to_do_campaign(
        client,
        customer_id,
        budget_resource_name,
        things_to_do_center_account_id,
    )
    # Creates an ad group.
    ad_group_resource_name = add_ad_group(
        client, customer_id, campaign_resource_name
    )
    # Creates an ad group ad.
    add_ad_group_ad(client, customer_id, ad_group_resource_name)


def add_campaign_budget(client, customer_id):
    """Creates a new campaign budget in the specified customer account.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.

    Returns:
        The resource name of the newly created budget.
    """
    # Creates a campaign budget operation.
    operation = client.get_type("CampaignBudgetOperation")
    # Creates a campaign budget.
    campaign_budget = operation.create
    campaign_budget.name = (
        f"Interplanetary Cruise Budget #{get_printable_datetime()}"
    )
    campaign_budget.delivery_method = (
        client.enums.BudgetDeliveryMethodEnum.STANDARD
    )
    # Sets the amount of budget.
    campaign_budget.amount_micros = 50000000
    # Makes the budget explicitly shared. This cannot be set to false for a
    # Things to do campaign.
    campaign_budget.explicitly_shared = True

    # Issues a mutate request.
    campaign_budget_service = client.get_service("CampaignBudgetService")
    response = campaign_budget_service.mutate_campaign_budgets(
        customer_id=customer_id, operations=[operation]
    )

    resource_name = response.results[0].resource_name
    print(f"Added a budget with resource name: '{resource_name}'.")
    return resource_name


# [START add_things_to_do_ad]
def add_things_to_do_campaign(
    client, customer_id, budget_resource_name, things_to_do_center_account_id
):
    """Creates a new Things to do campaign in the specified customer account.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        budget_resource_name: the resource name of a budget for a new campaign.
        things_to_do_center_account_id: the Things to Do Center account ID.

    Returns:
        The resource name of the newly created campaign.
    """
    # [START add_things_to_do_ad_1]
    # Creates a campaign operation.
    operation = client.get_type("CampaignOperation")
    # Creates a campaign.
    campaign = operation.create
    campaign.name = (
        f"Interplanetary Cruise Campaign #{get_printable_datetime()}"
    )
    # Configures settings related to Things to do campaigns including
    # advertising channel type, advertising channel sub type and travel
    # campaign settings.
    campaign.advertising_channel_type = (
        client.enums.AdvertisingChannelTypeEnum.TRAVEL
    )
    campaign.advertising_channel_sub_type = (
        client.enums.AdvertisingChannelSubTypeEnum.TRAVEL_ACTIVITIES
    )
    campaign.travel_campaign_settings.travel_account_id = (
        things_to_do_center_account_id
    )
    # Recommendation: Set the campaign to PAUSED when creating it to prevent
    # the ads from immediately serving. Set to ENABLED once you've added
    # targeting and the ads are ready to serve.
    campaign.status = client.enums.CampaignStatusEnum.PAUSED
    # Sets the bidding strategy to MaximizeConversionValue. Only this type can
    # be used for Things to do campaigns.
    campaign.maximize_conversion_value = client.get_type(
        "MaximizeConversionValue"
    )
    # Sets the budget.
    campaign.campaign_budget = budget_resource_name
    # Configures the campaign network options. Only Google Search is allowed for
    # Things to do campaigns.
    campaign.network_settings.target_google_search = True
    # [END add_things_to_do_ad_1]

    # Issues a mutate request to add campaigns.
    campaign_service = client.get_service("CampaignService")
    response = campaign_service.mutate_campaigns(
        customer_id=customer_id, operations=[operation]
    )

    resource_name = response.results[0].resource_name
    print(
        f"Added a Things to do campaign with resource name: '{resource_name}'."
    )
    return resource_name
    # [END add_things_to_do_ad]


# [START add_things_to_do_ad_2]
def add_ad_group(client, customer_id, campaign_resource_name):
    """Creates a new ad group in the specified Things to do campaign.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        campaign_resource_name: the resource name of campaign that a new ad
            group will belong to.

    Returns:
        The resource name of the newly created ad group.
    """
    # Creates an ad group operation.
    operation = client.get_type("AdGroupOperation")
    # Creates an ad group.
    ad_group = operation.create
    ad_group.name = f"Earth to Mars cruise #{get_printable_datetime()}"
    # Sets the campaign.
    ad_group.campaign = campaign_resource_name
    # Sets the ad group type to TRAVEL_ADS. This is the only value allowed
    # for this field on an ad group for a Things to do campaign.
    ad_group.type_ = client.enums.AdGroupTypeEnum.TRAVEL_ADS
    ad_group.status = client.enums.AdGroupStatusEnum.ENABLED

    # Issues a mutate request to add an ad group.
    ad_group_service = client.get_service("AdGroupService")
    ad_group_response = ad_group_service.mutate_ad_groups(
        customer_id=customer_id, operations=[operation]
    )

    resource_name = ad_group_response.results[0].resource_name
    print(f"Added an ad group with resource name: '{resource_name}'.")
    return resource_name
    # [END add_things_to_do_ad_2]


# [START add_things_to_do_ad_3]
def add_ad_group_ad(client, customer_id, ad_group_resource_name):
    """Creates a new ad group ad in the specified ad group.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        ad_group_resource_name: the resource name of ad group that a new ad
            group ad will belong to.
    """
    # Creates an ad group ad operation.
    operation = client.get_type("AdGroupAdOperation")
    # Creates a new ad group ad and sets a travel ad info.
    ad_group_ad = operation.create
    # Sets the ad group ad to enabled. Setting this to paused will cause an error
    # for Things to do campaigns. Pausing should happen at either the ad group
    # or campaign level.
    ad_group_ad.status = client.enums.AdGroupAdStatusEnum.ENABLED
    ad_group_ad.ad.travel_ad = client.get_type("TravelAdInfo")
    # Sets the ad group.
    ad_group_ad.ad_group = ad_group_resource_name

    # Issues a mutate request to add an ad group ad.
    ad_group_ad_service = client.get_service("AdGroupAdService")
    response = ad_group_ad_service.mutate_ad_group_ads(
        customer_id=customer_id, operations=[operation]
    )

    resource_name = response.results[0].resource_name
    print(f"Added an ad group ad with resource name: '{resource_name}'.")
    # [END add_things_to_do_ad_3]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=(
            "Adds a Things to do campaign, ad group, and a Things to do ad."
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
        "-t",
        "--things_to_do_center_account_id",
        type=int,
        required=True,
        help=("The Things to Do Center account ID."),
    )
    args = parser.parse_args()

    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v20")

    try:
        main(
            googleads_client,
            args.customer_id,
            args.things_to_do_center_account_id,
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
