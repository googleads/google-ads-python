#!/usr/bin/env python
# Copyright 2019 Google LLC
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
"""This code example adds a new dynamic search ad (DSA).

It also creates a webpage targeting criteria for the DSA.
"""


import argparse
from datetime import datetime, timedelta
import sys
from uuid import uuid4

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.ads.googleads.v22.common.types.criteria import WebpageConditionInfo
from google.ads.googleads.v22.resources.types.ad_group import AdGroup
from google.ads.googleads.v22.resources.types.ad_group_ad import AdGroupAd
from google.ads.googleads.v22.resources.types.ad_group_criterion import (
    AdGroupCriterion,
)
from google.ads.googleads.v22.resources.types.campaign import Campaign
from google.ads.googleads.v22.resources.types.campaign_budget import (
    CampaignBudget,
)
from google.ads.googleads.v22.services.services.ad_group_ad_service import (
    AdGroupAdServiceClient,
)
from google.ads.googleads.v22.services.services.ad_group_criterion_service import (
    AdGroupCriterionServiceClient,
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
from google.ads.googleads.v22.services.types.ad_group_criterion_service import (
    AdGroupCriterionOperation,
    MutateAdGroupCriteriaResponse,
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


def main(client: GoogleAdsClient, customer_id: str) -> None:
    """The main method that creates all necessary entities for the example.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID str.
    """
    budget_resource_name: str = create_budget(client, customer_id)
    campaign_resource_name: str = create_campaign(
        client, customer_id, budget_resource_name
    )
    ad_group_resource_name: str = create_ad_group(
        client, customer_id, campaign_resource_name
    )
    create_expanded_dsa(client, customer_id, ad_group_resource_name)
    add_webpage_criterion(client, customer_id, ad_group_resource_name)


def create_budget(client: GoogleAdsClient, customer_id: str) -> str:
    """Creates a budget under the given customer ID.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID str.

    Returns:
        A resource_name str for the newly created Budget.
    """
    # Retrieve the campaign budget service.
    campaign_budget_service: CampaignBudgetServiceClient = client.get_service(
        "CampaignBudgetService"
    )
    # Creates a campaign budget operation.
    campaign_budget_operation: CampaignBudgetOperation = client.get_type(
        "CampaignBudgetOperation"
    )
    # Issues a mutate request to add campaign budgets.
    campaign_budget: CampaignBudget = campaign_budget_operation.create
    campaign_budget.name = f"Interplanetary Cruise #{uuid4()}"
    campaign_budget.amount_micros = 50000000
    campaign_budget.delivery_method = (
        client.enums.BudgetDeliveryMethodEnum.STANDARD
    )

    # Submit the campaign budget operation to add the campaign budget.
    response: MutateCampaignBudgetsResponse = (
        campaign_budget_service.mutate_campaign_budgets(
            customer_id=customer_id, operations=[campaign_budget_operation]
        )
    )
    resource_name: str = response.results[0].resource_name

    print(f'Created campaign budget with resource_name: "{resource_name}"')

    return resource_name


# [START add_dynamic_search_ads]
def create_campaign(
    client: GoogleAdsClient, customer_id: str, budget_resource_name: str
) -> str:
    """Creates a Dynamic Search Ad Campaign under the given customer ID.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID str.
        budget_resource_name: a resource_name str for a Budget

    Returns:
        A resource_name str for the newly created Campaign.
    """
    # Retrieve a new campaign operation object.
    campaign_operation: CampaignOperation = client.get_type("CampaignOperation")
    campaign: Campaign = campaign_operation.create
    campaign.name = f"Interplanetary Cruise #{uuid4()}"
    campaign.advertising_channel_type = (
        client.enums.AdvertisingChannelTypeEnum.SEARCH
    )
    # Recommendation: Set the campaign to PAUSED when creating it to prevent the
    # ads from immediately serving. Set to ENABLED once you've added targeting
    # and the ads are ready to serve.
    campaign.status = client.enums.CampaignStatusEnum.PAUSED
    campaign.manual_cpc.enhanced_cpc_enabled = True
    campaign.campaign_budget = budget_resource_name
    # Required: Enable the campaign for DSAs by setting the campaign's dynamic
    # search ads setting domain name and language.
    campaign.dynamic_search_ads_setting.domain_name = "example.com"
    campaign.dynamic_search_ads_setting.language_code = "en"

    # Declare whether or not this campaign serves political ads targeting the
    # EU. Valid values are:
    #   CONTAINS_EU_POLITICAL_ADVERTISING
    #   DOES_NOT_CONTAIN_EU_POLITICAL_ADVERTISING
    campaign.contains_eu_political_advertising = (
        client.enums.EuPoliticalAdvertisingStatusEnum.DOES_NOT_CONTAIN_EU_POLITICAL_ADVERTISING
    )

    # Optional: Sets the start and end dates for the campaign, beginning one day
    # from now and ending a month from now.
    campaign.start_date = (datetime.now() + timedelta(days=1)).strftime(
        "%Y%m%d"
    )
    campaign.end_date = (datetime.now() + timedelta(days=30)).strftime("%Y%m%d")

    # Retrieve the campaign service.
    campaign_service: CampaignServiceClient = client.get_service(
        "CampaignService"
    )

    # Issues a mutate request to add campaign.
    response: MutateCampaignsResponse = campaign_service.mutate_campaigns(
        customer_id=customer_id, operations=[campaign_operation]
    )
    resource_name: str = response.results[0].resource_name

    print(f'Created campaign with resource_name: "{resource_name}"')
    # [END add_dynamic_search_ads]

    return resource_name


# [START add_dynamic_search_ads_1]
def create_ad_group(
    client: GoogleAdsClient, customer_id: str, campaign_resource_name: str
) -> str:
    """Creates a Dynamic Search Ad Group under the given Campaign.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID str.
        campaign_resource_name: a resource_name str for a Campaign.

    Returns:
        A resource_name str for the newly created Ad Group.
    """
    # Retrieve a new ad group operation object.
    ad_group_operation: AdGroupOperation = client.get_type("AdGroupOperation")
    # Create an ad group.
    ad_group: AdGroup = ad_group_operation.create
    # Required: set the ad group's type to Dynamic Search Ads.
    ad_group.type_ = client.enums.AdGroupTypeEnum.SEARCH_DYNAMIC_ADS
    ad_group.name = f"Earth to Mars Cruises {uuid4()}"
    ad_group.campaign = campaign_resource_name
    ad_group.status = client.enums.AdGroupStatusEnum.PAUSED
    # Recommended: set a tracking URL template for your ad group if you want to
    # use URL tracking software.
    ad_group.tracking_url_template = (
        "http://tracker.example.com/traveltracker/{escapedlpurl}"
    )
    # Optional: Set the ad group bid value.
    ad_group.cpc_bid_micros = 10000000

    # Retrieve the ad group service.
    ad_group_service: AdGroupServiceClient = client.get_service(
        "AdGroupService"
    )

    # Issues a mutate request to add the ad group.
    response: MutateAdGroupsResponse = ad_group_service.mutate_ad_groups(
        customer_id=customer_id, operations=[ad_group_operation]
    )
    resource_name: str = response.results[0].resource_name

    print(f'Created Ad Group with resource_name: "{resource_name}"')
    # [END add_dynamic_search_ads_1]

    return resource_name


# [START add_dynamic_search_ads_2]
def create_expanded_dsa(
    client: GoogleAdsClient, customer_id: str, ad_group_resource_name: str
) -> None:
    """Creates a dynamic search ad under the given ad group.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID str.
        ad_group_resource_name: a resource_name str for an Ad Group.
    """
    # Retrieve a new ad group ad operation object.
    ad_group_ad_operation: AdGroupAdOperation = client.get_type(
        "AdGroupAdOperation"
    )
    # Create and expanded dynamic search ad. This ad will have its headline,
    # display URL and final URL auto-generated at serving time according to
    # domain name specific information provided by DynamicSearchAdSetting at
    # the campaign level.
    ad_group_ad: AdGroupAd = ad_group_ad_operation.create
    # Optional: set the ad status.
    ad_group_ad.status = client.enums.AdGroupAdStatusEnum.PAUSED
    # Set the ad description.
    ad_group_ad.ad.expanded_dynamic_search_ad.description = "Buy tickets now!"
    ad_group_ad.ad_group = ad_group_resource_name

    # Retrieve the ad group ad service.
    ad_group_ad_service: AdGroupAdServiceClient = client.get_service(
        "AdGroupAdService"
    )

    # Submit the ad group ad operation to add the ad group ad.
    response: MutateAdGroupAdsResponse = (
        ad_group_ad_service.mutate_ad_group_ads(
            customer_id=customer_id, operations=[ad_group_ad_operation]
        )
    )
    resource_name: str = response.results[0].resource_name

    print(f'Created Ad Group Ad with resource_name: "{resource_name}"')
    # [END add_dynamic_search_ads_2]


def add_webpage_criterion(
    client: GoogleAdsClient, customer_id: str, ad_group_resource_name: str
) -> None:
    """Creates a web page criterion to the given ad group.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID str.
        ad_group_resource_name: a resource_name str for an Ad Group.
    """
    # Retrieve a new ad group criterion operation.
    ad_group_criterion_operation: AdGroupCriterionOperation = client.get_type(
        "AdGroupCriterionOperation"
    )
    # Create an ad group criterion for special offers for Mars Cruise.
    criterion: AdGroupCriterion = ad_group_criterion_operation.create
    criterion.ad_group = ad_group_resource_name
    # Optional: set custom bid amount.
    criterion.cpc_bid_micros = 10000000
    # Optional: set the status.
    criterion.status = client.enums.AdGroupCriterionStatusEnum.PAUSED

    # Sets the criterion to match a specific page URL and title.
    criterion.webpage.criterion_name = "Special Offers"
    # First condition info - URL
    webpage_condition_info_url: WebpageConditionInfo = client.get_type(
        "WebpageConditionInfo"
    )
    webpage_condition_info_url.operand = (
        client.enums.WebpageConditionOperandEnum.URL
    )
    webpage_condition_info_url.argument = "/specialoffers"
    # Second condition info - Page title
    webpage_condition_info_page_title: WebpageConditionInfo = client.get_type(
        "WebpageConditionInfo"
    )
    webpage_condition_info_page_title.operand = (
        client.enums.WebpageConditionOperandEnum.PAGE_TITLE
    )
    webpage_condition_info_page_title.argument = "Special Offer"
    # Add first and second condition info
    criterion.webpage.conditions.extend(
        [webpage_condition_info_url, webpage_condition_info_page_title]
    )

    # Retrieve the ad group criterion service.
    ad_group_criterion_service: AdGroupCriterionServiceClient = (
        client.get_service("AdGroupCriterionService")
    )

    # Issues a mutate request to add the ad group criterion.
    response: MutateAdGroupCriteriaResponse = (
        ad_group_criterion_service.mutate_ad_group_criteria(
            customer_id=customer_id, operations=[ad_group_criterion_operation]
        )
    )
    resource_name: str = response.results[0].resource_name

    print(f'Created Ad Group Criterion with resource_name: "{resource_name}"')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=(
            "Adds a dynamic search ad under the specified customer ID."
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
    args: argparse.Namespace = parser.parse_args()

    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client: GoogleAdsClient = GoogleAdsClient.load_from_storage(
        version="v22"
    )

    try:
        main(googleads_client, args.customer_id)
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
