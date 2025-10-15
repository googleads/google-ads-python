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
"""This example adds a hotel campaign, ad group, and ad group ad.

Prerequisite: You need to have access to the Hotel Ads Center, which can be
granted during integration with Google Hotels. The integration instructions can
be found at:
https://support.google.com/hotelprices/answer/6101897.
"""


import argparse
import sys
import uuid

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.ads.googleads.v22.resources.types.ad_group import AdGroup
from google.ads.googleads.v22.resources.types.ad_group_ad import AdGroupAd
from google.ads.googleads.v22.resources.types.campaign import Campaign
from google.ads.googleads.v22.resources.types.campaign_budget import (
    CampaignBudget,
)
from google.ads.googleads.v22.services.services.ad_group_ad_service import (
    AdGroupAdServiceClient,
)
from google.ads.googleads.v22.services.services.ad_group_service import (
    AdGroupServiceClient,
)
from google.ads.googleads.v22.services.services.campaign_budget_service import (
    CampaignBudgetServiceClient,
)
from google.ads.googleads.v22.services.services.campaign_service import (
    CampaignServiceClient,
)
from google.ads.googleads.v22.services.types.ad_group_ad_service import (
    AdGroupAdOperation,
    MutateAdGroupAdsResponse,
)
from google.ads.googleads.v22.services.types.ad_group_service import (
    AdGroupOperation,
    MutateAdGroupsResponse,
)
from google.ads.googleads.v22.services.types.campaign_budget_service import (
    CampaignBudgetOperation,
    MutateCampaignBudgetsResponse,
)
from google.ads.googleads.v22.services.types.campaign_service import (
    CampaignOperation,
    MutateCampaignsResponse,
)


def main(
    client: GoogleAdsClient,
    customer_id: str,
    hotel_center_account_id: int,
    cpc_bid_ceiling_micro_amount: int,
) -> None:
    budget_resource_name: str = add_budget(client, customer_id)

    campaign_resource_name: str = add_hotel_campaign(
        client,
        customer_id,
        budget_resource_name,
        hotel_center_account_id,
        cpc_bid_ceiling_micro_amount,
    )

    ad_group_resource_name: str = add_hotel_ad_group(
        client, customer_id, campaign_resource_name
    )

    add_hotel_ad(client, customer_id, ad_group_resource_name)


def add_budget(client: GoogleAdsClient, customer_id: str) -> str:
    campaign_budget_service: CampaignBudgetServiceClient = client.get_service(
        "CampaignBudgetService"
    )

    # Create a budget, which can be shared by multiple campaigns.
    campaign_budget_operation: CampaignBudgetOperation = client.get_type(
        "CampaignBudgetOperation"
    )
    campaign_budget: CampaignBudget = campaign_budget_operation.create
    campaign_budget.name = f"Interplanetary Budget {uuid.uuid4()}"
    campaign_budget.delivery_method = (
        client.enums.BudgetDeliveryMethodEnum.STANDARD
    )
    campaign_budget.amount_micros = 500000

    # Add budget.
    campaign_budget_response: MutateCampaignBudgetsResponse = (
        campaign_budget_service.mutate_campaign_budgets(
            customer_id=customer_id, operations=[campaign_budget_operation]
        )
    )

    budget_resource_name: str = campaign_budget_response.results[
        0
    ].resource_name

    print(f"Created budget with resource name '{budget_resource_name}'.")

    return budget_resource_name


# [START add_hotel_ad_3]
def add_hotel_ad(
    client: GoogleAdsClient, customer_id: str, ad_group_resource_name: str
) -> str:
    ad_group_ad_service: AdGroupAdServiceClient = client.get_service(
        "AdGroupAdService"
    )

    # Creates a new ad group ad and sets the hotel ad to it.
    ad_group_ad_operation: AdGroupAdOperation = client.get_type(
        "AdGroupAdOperation"
    )
    ad_group_ad: AdGroupAd = ad_group_ad_operation.create
    ad_group_ad.ad_group = ad_group_resource_name
    # Set the ad group ad to enabled.  Setting this to paused will cause an error
    # for hotel campaigns.  For hotels pausing should happen at either the ad group or
    # campaign level.
    ad_group_ad.status = client.enums.AdGroupAdStatusEnum.ENABLED
    client.copy_from(ad_group_ad.ad.hotel_ad, client.get_type("HotelAdInfo"))

    # Add the ad group ad.
    ad_group_ad_response: MutateAdGroupAdsResponse = (
        ad_group_ad_service.mutate_ad_group_ads(
            customer_id=customer_id, operations=[ad_group_ad_operation]
        )
    )

    ad_group_ad_resource_name: str = ad_group_ad_response.results[
        0
    ].resource_name

    print(f"Created hotel ad with resource name '{ad_group_ad_resource_name}'.")

    return ad_group_resource_name
    # [END add_hotel_ad_3]


# [START add_hotel_ad_2]
def add_hotel_ad_group(
    client: GoogleAdsClient, customer_id: str, campaign_resource_name: str
) -> str:
    ad_group_service: AdGroupServiceClient = client.get_service(
        "AdGroupService"
    )

    # Create ad group.
    ad_group_operation: AdGroupOperation = client.get_type("AdGroupOperation")
    ad_group: AdGroup = ad_group_operation.create
    ad_group.name = f"Earth to Mars cruise {uuid.uuid4()}"
    ad_group.status = client.enums.AdGroupStatusEnum.ENABLED
    ad_group.campaign = campaign_resource_name
    # Sets the ad group type to HOTEL_ADS. This cannot be set to other types.
    ad_group.type_ = client.enums.AdGroupTypeEnum.HOTEL_ADS
    ad_group.cpc_bid_micros = 10000000

    # Add the ad group.
    ad_group_response: MutateAdGroupsResponse = (
        ad_group_service.mutate_ad_groups(
            customer_id=customer_id, operations=[ad_group_operation]
        )
    )

    ad_group_resource_name: str = ad_group_response.results[0].resource_name

    print(
        "Added a hotel ad group with resource name '{ad_group_resource_name}'."
    )

    return ad_group_resource_name
    # [END add_hotel_ad_2]


# [START add_hotel_ad]
def add_hotel_campaign(
    client: GoogleAdsClient,
    customer_id: str,
    budget_resource_name: str,
    hotel_center_account_id: int,
    cpc_bid_ceiling_micro_amount: int,
) -> str:
    campaign_service: CampaignServiceClient = client.get_service(
        "CampaignService"
    )

    # [START add_hotel_ad_1]
    # Create campaign.
    campaign_operation: CampaignOperation = client.get_type("CampaignOperation")
    campaign: Campaign = campaign_operation.create
    campaign.name = f"Interplanetary Cruise Campaign {uuid.uuid4()}"

    # Configures settings related to hotel campaigns including advertising
    # channel type and hotel setting info.
    campaign.advertising_channel_type = (
        client.enums.AdvertisingChannelTypeEnum.HOTEL
    )
    campaign.hotel_setting.hotel_center_id = hotel_center_account_id

    # Recommendation: Set the campaign to PAUSED when creating it to prevent the
    # ads from immediately serving. Set to ENABLED once you've added targeting
    # and the ads are ready to serve.
    campaign.status = client.enums.CampaignStatusEnum.PAUSED

    # Set the bidding strategy to PercentCpc. Only Manual CPC and Percent CPC
    # can be used for hotel campaigns.
    campaign.percent_cpc.cpc_bid_ceiling_micros = cpc_bid_ceiling_micro_amount

    # Sets the budget.
    campaign.campaign_budget = budget_resource_name

    # Set the campaign network options. Only Google Search is allowed for hotel
    # campaigns.
    campaign.network_settings.target_google_search = True

    # Declare whether or not this campaign serves political ads targeting the
    # EU. Valid values are:
    #   CONTAINS_EU_POLITICAL_ADVERTISING
    #   DOES_NOT_CONTAIN_EU_POLITICAL_ADVERTISING
    campaign.contains_eu_political_advertising = (
        client.enums.EuPoliticalAdvertisingStatusEnum.DOES_NOT_CONTAIN_EU_POLITICAL_ADVERTISING
    )
    # [END add_hotel_ad_1]

    # Add the campaign.
    campaign_response: MutateCampaignsResponse = (
        campaign_service.mutate_campaigns(
            customer_id=customer_id, operations=[campaign_operation]
        )
    )

    campaign_resource_name: str = campaign_response.results[0].resource_name

    print(
        "Added a hotel campaign with resource name '{campaign_resource_name}'."
    )

    return campaign_resource_name
    # [END add_hotel_ad]


if __name__ == "__main__":
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description=(
            "Adds an expanded text ad to the specified ad group ID, "
            "for the given customer ID."
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
        "-b",
        "--cpc_bid_ceiling_micro_amount",
        type=int,
        required=True,
        help=("The cpc bid ceiling micro amount for the hotel campaign."),
    )
    parser.add_argument(
        "-a",
        "--hotel_center_account_id",
        type=int,
        required=True,
        help="The hotel center account ID.",
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
            args.hotel_center_account_id,
            args.cpc_bid_ceiling_micro_amount,
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
