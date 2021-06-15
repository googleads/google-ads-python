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


def main(client, customer_id):
    """The main method that creates all necessary entities for the example.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID str.
    """
    budget_resource_name = _create_budget(client, customer_id)
    campaign_resource_name = _create_campaign(
        client, customer_id, budget_resource_name
    )
    ad_group_resource_name = _create_ad_group(
        client, customer_id, campaign_resource_name
    )
    _create_expanded_dsa(client, customer_id, ad_group_resource_name)
    _add_webpage_criterion(client, customer_id, ad_group_resource_name)


def _create_budget(client, customer_id):
    """Creates a budget under the given customer ID.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID str.

    Returns:
        A resource_name str for the newly created Budget.
    """
    # Retrieve the campaign budget service.
    campaign_budget_service = client.get_service("CampaignBudgetService")
    # Creates a campaign budget operation.
    campaign_budget_operation = client.get_type("CampaignBudgetOperation")
    # Issues a mutate request to add campaign budgets.
    campaign_budget = campaign_budget_operation.create
    campaign_budget.name = f"Interplanetary Cruise #{uuid4()}"
    campaign_budget.amount_micros = 50000000
    campaign_budget.delivery_method = client.get_type(
        "BudgetDeliveryMethodEnum"
    ).BudgetDeliveryMethod.STANDARD

    # Submit the campaign budget operation to add the campaign budget.
    response = campaign_budget_service.mutate_campaign_budgets(
        customer_id=customer_id, operations=[campaign_budget_operation]
    )
    resource_name = response.results[0].resource_name

    print(f'Created campaign budget with resource_name: "{resource_name}"')

    return resource_name


# [START add_dynamic_search_ads]
def _create_campaign(client, customer_id, budget_resource_name):
    """Creates a Dynamic Search Ad Campaign under the given customer ID.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID str.
        budget_resource_name: a resource_name str for a Budget

    Returns:
        A resource_name str for the newly created Campaign.
    """
    # Retrieve a new campaign operation object.
    campaign_operation = client.get_type("CampaignOperation")
    campaign = campaign_operation.create
    campaign.name = f"Interplanetary Cruise #{uuid4()}"
    campaign.advertising_channel_type = client.get_type(
        "AdvertisingChannelTypeEnum"
    ).AdvertisingChannelType.SEARCH
    # Recommendation: Set the campaign to PAUSED when creating it to prevent the
    # ads from immediately serving. Set to ENABLED once you've added targeting
    # and the ads are ready to serve.
    campaign.status = client.get_type(
        "CampaignStatusEnum"
    ).CampaignStatus.PAUSED
    campaign.manual_cpc.enhanced_cpc_enabled = True
    campaign.campaign_budget = budget_resource_name
    # Required: Enable the campaign for DSAs by setting the campaign's dynamic
    # search ads setting domain name and language.
    campaign.dynamic_search_ads_setting.domain_name = "example.com"
    campaign.dynamic_search_ads_setting.language_code = "en"
    # Optional: Sets the start and end dates for the campaign, beginning one day
    # from now and ending a month from now.
    campaign.start_date = (datetime.now() + timedelta(days=1)).strftime(
        "%Y%m%d"
    )
    campaign.end_date = (datetime.now() + timedelta(days=30)).strftime("%Y%m%d")

    # Retrieve the campaign service.
    campaign_service = client.get_service("CampaignService")

    # Issues a mutate request to add campaign.
    response = campaign_service.mutate_campaigns(
        customer_id=customer_id, operations=[campaign_operation]
    )
    resource_name = response.results[0].resource_name

    print(f'Created campaign with resource_name: "{resource_name}"')
    # [END add_dynamic_search_ads]

    return resource_name


# [START add_dynamic_search_ads_1]
def _create_ad_group(client, customer_id, campaign_resource_name):
    """Creates a Dynamic Search Ad Group under the given Campaign.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID str.
        campaign_resource_name: a resource_name str for a Campaign.

    Returns:
        A resource_name str for the newly created Ad Group.
    """
    # Retrieve a new ad group operation object.
    ad_group_operation = client.get_type("AdGroupOperation")
    # Create an ad group.
    ad_group = ad_group_operation.create
    # Required: set the ad group's type to Dynamic Search Ads.
    ad_group.type_ = client.get_type(
        "AdGroupTypeEnum"
    ).AdGroupType.SEARCH_DYNAMIC_ADS
    ad_group.name = f"Earth to Mars Cruises {uuid4()}"
    ad_group.campaign = campaign_resource_name
    ad_group.status = client.get_type("AdGroupStatusEnum").AdGroupStatus.PAUSED
    # Recommended: set a tracking URL template for your ad group if you want to
    # use URL tracking software.
    ad_group.tracking_url_template = (
        "http://tracker.example.com/traveltracker/{escapedlpurl}"
    )
    # Optional: Set the ad group bid value.
    ad_group.cpc_bid_micros = 10000000

    # Retrieve the ad group service.
    ad_group_service = client.get_service("AdGroupService")

    # Issues a mutate request to add the ad group.
    response = ad_group_service.mutate_ad_groups(
        customer_id=customer_id, operations=[ad_group_operation]
    )
    resource_name = response.results[0].resource_name

    print(f'Created Ad Group with resource_name: "{resource_name}"')
    # [END add_dynamic_search_ads_1]

    return resource_name


# [START add_dynamic_search_ads_2]
def _create_expanded_dsa(client, customer_id, ad_group_resource_name):
    """Creates a dynamic search ad under the given ad group.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID str.
        ad_group_resource_name: a resource_name str for an Ad Group.
    """
    # Retrieve a new ad group ad operation object.
    ad_group_ad_operation = client.get_type("AdGroupAdOperation")
    # Create and expanded dynamic search ad. This ad will have its headline,
    # display URL and final URL auto-generated at serving time according to
    # domain name specific information provided by DynamicSearchAdSetting at
    # the campaign level.
    ad_group_ad = ad_group_ad_operation.create
    # Optional: set the ad status.
    ad_group_ad.status = client.get_type(
        "AdGroupAdStatusEnum"
    ).AdGroupAdStatus.PAUSED
    # Set the ad description.
    ad_group_ad.ad.expanded_dynamic_search_ad.description = "Buy tickets now!"
    ad_group_ad.ad_group = ad_group_resource_name

    # Retrieve the ad group ad service.
    ad_group_ad_service = client.get_service("AdGroupAdService")

    # Submit the ad group ad operation to add the ad group ad.
    response = ad_group_ad_service.mutate_ad_group_ads(
        customer_id=customer_id, operations=[ad_group_ad_operation]
    )
    resource_name = response.results[0].resource_name

    print(f'Created Ad Group Ad with resource_name: "{resource_name}"')
    # [END add_dynamic_search_ads_2]


def _add_webpage_criterion(client, customer_id, ad_group_resource_name):
    """Creates a web page criterion to the given ad group.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID str.
        ad_group_resource_name: a resource_name str for an Ad Group.
    """
    # Retrieve a new ad group criterion operation.
    ad_group_criterion_operation = client.get_type("AdGroupCriterionOperation")
    # Create an ad group criterion for special offers for Mars Cruise.
    criterion = ad_group_criterion_operation.create
    criterion.ad_group = ad_group_resource_name
    # Optional: set custom bid amount.
    criterion.cpc_bid_micros = 10000000
    # Optional: set the status.
    criterion.status = client.get_type(
        "AdGroupCriterionStatusEnum"
    ).AdGroupCriterionStatus.PAUSED

    # Sets the criterion to match a specific page URL and title.
    criterion.webpage.criterion_name = "Special Offers"
    # First condition info - URL
    webpage_condition_info_url = client.get_type("WebpageConditionInfo")
    webpage_condition_info_url.operand = client.get_type(
        "WebpageConditionOperandEnum"
    ).WebpageConditionOperand.URL
    webpage_condition_info_url.argument = "/specialoffers"
    # Second condition info - Page title
    webpage_condition_info_page_title = client.get_type("WebpageConditionInfo")
    webpage_condition_info_page_title.operand = client.get_type(
        "WebpageConditionOperandEnum"
    ).WebpageConditionOperand.PAGE_TITLE
    webpage_condition_info_page_title.argument = "Special Offer"
    # Add first and second condition info
    criterion.webpage.conditions.extend(
        [webpage_condition_info_url, webpage_condition_info_page_title]
    )

    # Retrieve the ad group criterion service.
    ad_group_criterion_service = client.get_service("AdGroupCriterionService")

    # Issues a mutate request to add the ad group criterion.
    response = ad_group_criterion_service.mutate_ad_group_criteria(
        customer_id=customer_id, operations=[ad_group_criterion_operation]
    )
    resource_name = response.results[0].resource_name

    print(f'Created Ad Group Criterion with resource_name: "{resource_name}"')


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v8")

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
    args = parser.parse_args()

    try:
        main(googleads_client, args.customer_id)
    except GoogleAdsException as ex:
        print(
            f'Request with ID "{ex.request_id}" failed with status '
            f'"{ex.error.code().name}" and includes the following errors:'
        )
        for error in ex.failure.errors:
            print(f'	Error with message "{error.message}".')
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print(f"\t\tOn field: {field_path_element.field_name}")
        sys.exit(1)
