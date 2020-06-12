#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
"""This example creates a search campaign with the AdWords and Google Ads APIs.

This code example is the fifth in a series of code examples that shows how to
create a Search campaign using the AdWords API, and then migrate it to the
Google Ads API one functionality at a time. See other examples in this directory
for code examples in various stages of migration.

In this code example, the functionality to create campaign budget and search
campaign have been migrated to the Google Ads API. The rest of the functionality
- creating ad groups, keywords and expanded text ads are done using the AdWords
API.
"""

import argparse
import datetime
import sys
import urllib.parse
import uuid

from googleads import adwords

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

# Number of ads being added/updated in this code example.
NUMBER_OF_ADS = 5
# The list of keywords being added in this code example.
KEYWORDS_TO_ADD = ["mars cruise", "space hotel"]
PAGE_SIZE = 1000


def _create_campaign_budget(client, customer_id):
    """Creates a new campaign budget and returns it.

    Args:
        client: A GoogleAdsClient instance.
        customer_id: (str) Customer ID associated with the account.

    Returns:
        A CampaignBudget.
    """
    campaign_service = client.get_service("CampaignBudgetService")
    operation = client.get_type("CampaignBudgetOperation")
    criterion = operation.create
    criterion.name = f"Interplanetary Cruise Budget {uuid.uuid4()}"
    criterion.delivery_method = client.get_type(
        "BudgetDeliveryMethodEnum"
    ).BudgetDeliveryMethod.STANDARD
    criterion.amount_micros = 500000

    try:
        response = campaign_service.mutate_campaign_budgets(
            customer_id=customer_id, operations=[operation]
        )
        campaign_budget_resource_name = response.results[0].resource_name
        new_campaign_budget = _get_campaign_budget(
            client, customer_id, campaign_budget_resource_name
        )
        print(f"Added budget named {new_campaign_budget.name}")
        return new_campaign_budget
    except GoogleAdsClient as ex:
        _handle_googleads_exception(ex)


def _get_campaign_budget(client, customer_id, resource_name):
    """Retrieves the CampaignBudget associated with the given resource name.

    Args:
        client: A GoogleAdsClient instance.
        customer_id: (str) Customer ID associated with the account.
        resource_name: (str) Resource name associated with the newly created
            campaign.

    Returns:
        A CampaignBudget.
    """
    ga_service = client.get_service("GoogleAdsService")
    query = f'''
        SELECT
            campaign_budget.id,
            campaign_budget.name,
            campaign_budget.resource_name
        FROM campaign_budget
        WHERE campaign_budget.resource_name = "{resource_name}"'''

    request = client.get_type("SearchGoogleAdsRequest")
    request.customer_id = customer_id
    request.query = query
    request.page_size = PAGE_SIZE

    try:
        response = ga_service.search(request=request)
        budget = list(response)[0].campaign_budget
        return budget
    except GoogleAdsException as ex:
        _handle_googleads_exception(ex)


def _create_campaign(client, customer_id, campaign_budget):
    """Creates a new campaign and returns it.

    Args:
        client: A GoogleAdsClient instance.
        customer_id: (str) Customer ID associated with the account.
        campaign_budget: A CampaignBudget.

    Returns:
        A Campaign.
    """
    operation = client.get_type("CampaignOperation")
    campaign = operation.create
    campaign_service = client.get_service("CampaignService")
    campaign.name = f"Interplanetary Cruise#{uuid.uuid4()}"
    campaign.advertising_channel_type = client.get_type(
        "AdvertisingChannelTypeEnum"
    ).AdvertisingChannelType.SEARCH
    # Recommendation: Set the campaign to PAUSED when creating it to stop the
    # ads from immediately serving. Set to ENABLED once you've added
    # targeting and the ads are ready to serve.
    campaign.status = client.get_type(
        "CampaignStatusEnum"
    ).CampaignStatus.PAUSED
    campaign.manual_cpc.enhanced_cpc_enabled = True
    campaign.campaign_budget = campaign_budget.resource_name
    campaign.network_settings.target_google_search = True
    campaign.network_settings.target_search_network = True
    campaign.network_settings.target_content_network = False
    campaign.network_settings.target_partner_search_network = False
    campaign.start_date = (
        datetime.datetime.now() + datetime.timedelta(1)
    ).strftime("%Y%m%d")
    campaign.end_date = (
        datetime.datetime.now() + datetime.timedelta(365)
    ).strftime("%Y%m%d")

    try:
        response = campaign_service.mutate_campaigns(
            customer_id=customer_id, operations=[operation]
        )
        campaign_resource_name = response.results[0].resource_name
        new_campaign = _get_campaign(
            client, customer_id, campaign_resource_name
        )
        print(f"Added campaign named {new_campaign.name}")
        return new_campaign
    except GoogleAdsException as ex:
        _handle_googleads_exception(ex)


def _get_campaign(client, customer_id, campaign_resource_name):
    """Retrieves the Campaign associated with the given resource name.

    Args:
        client: A GoogleAdsClient instance.
        customer_id: (str) Customer ID associated with the account.
        campaign_resource_name: (str) Resource name associated with the newly
            created campaign budget.

    Returns:
        A Campaign.
    """
    ga_service = client.get_service("GoogleAdsService")
    query = f'''
        SELECT
              campaign.id,
              campaign.name,
              campaign.resource_name
        FROM campaign
        WHERE campaign.resource_name = "{campaign_resource_name}"'''

    request = client.get_type("SearchGoogleAdsRequest")
    request.customer_id = customer_id
    request.query = query
    request.page_size = PAGE_SIZE

    try:
        response = ga_service.search(request=request)
        campaign = list(response)[0].campaign
        return campaign
    except GoogleAdsException as ex:
        _handle_googleads_exception(ex)


def _create_ad_group(client, customer_id, campaign):
    """Creates a new ad group and returns it.

    Args:
        client: A GoogleAdsClient instance.
        customer_id: (str) Customer ID associated with the account.
        campaign: A Campaign.

    Returns:
        An AdGroup.
    """
    operation = client.get_type("AdGroupOperation")
    adgroup = operation.create
    adgroup_service = client.get_service("AdGroupService")
    adgroup.name = f"Earth to Mars Cruises #{uuid.uuid4()}"
    adgroup.campaign = campaign.resource_name
    adgroup.status = client.get_type("AdGroupStatusEnum").AdGroupStatus.ENABLED
    adgroup.type = client.get_type(
        "AdGroupTypeEnum"
    ).AdGroupType.SEARCH_STANDARD
    adgroup.cpc_bid_micros = 10000000

    try:
        response = adgroup_service.mutate_ad_groups(
            customer_id=customer_id, operations=[operation]
        )
        ad_group_resource_name = response.results[0].resource_name
        ad_group = _get_ad_group(client, customer_id, ad_group_resource_name)
        print(f"Added AdGroup named {ad_group.name}")
        return ad_group
    except GoogleAdsException as ex:
        _handle_googleads_exception(ex)


def _get_ad_group(client, customer_id, ad_group_resource_name):
    """Retrieves an AdGroup associated with the given resource name.

    Args:
        client: A GoogleAdsClient instance.
        customer_id: (str) Customer ID associated with the account.
        ad_group_resource_name: (str) Resource name associated with the newly
            created Ad group.

    Returns:
        An AdGroup.
    """
    ga_service = client.get_service("GoogleAdsService")
    query = f'''
        SELECT
            ad_group.id,
            ad_group.name,
            ad_group.resource_name
        FROM ad_group
        WHERE ad_group.resource_name = "{ad_group_resource_name}"'''

    request = client.get_type("SearchGoogleAdsRequest")
    request.customer_id = customer_id
    request.query = query
    request.page_size = PAGE_SIZE

    try:
        response = ga_service.search(request=request)
        adGroup = list(response)[0].ad_group
        return adGroup
    except GoogleAdsException as ex:
        _handle_googleads_exception(ex)


def _create_text_ads(client, customer_id, ad_group):
    """Creates new text ads in a given ad group.

    Args:
        client: A GoogleAdsClient instance.
        customer_id: (str) Customer ID associated with the account.
        ad_group: A AdGroup instance.
    """
    adgroup_service = client.get_service("AdGroupAdService")

    operations = []
    for i in range(0, NUMBER_OF_ADS):
        operation = client.get_type("AdGroupAdOperation")
        ad_group_operation = operation.create
        ad_group_operation.ad_group = ad_group.resource_name
        ad_group_operation.status = client.get_type(
            "AdGroupAdStatusEnum"
        ).AdGroupAdStatus.PAUSED
        ad_group_operation.ad.expanded_text_ad.headline_part1 = (
            f"Cruise to Mars #{str(uuid.uuid4())[:4]}"
        )
        ad_group_operation.ad.expanded_text_ad.headline_part2 = (
            "Best Space Cruise Line"
        )
        ad_group_operation.ad.expanded_text_ad.description = (
            "Buy your tickets now!"
        )
        ad_group_operation.ad.final_urls.append("http://www.example.com")
        operations.append(operation)

    try:
        ad_group_ad_response = adgroup_service.mutate_ad_group_ads(
            customer_id=customer_id, operations=operations
        )
        new_ad_resource_names = [
            row.resource_name for row in ad_group_ad_response.results
        ]
    except GoogleAdsException as ex:
        _handle_googleads_exception(ex)

    new_ads = _get_ads(client, customer_id, new_ad_resource_names)
    for new_ad in new_ads:
        print(
            f"Created expanded text ad with ID {new_ad.ad.id}, status "
            f"{new_ad.status} and headline "
            f"{new_ad.ad.expanded_text_ad.headline_part1}."
            f"{new_ad.ad.expanded_text_ad.headline_part2}"
        )


def _get_ads(client, customer_id, new_ad_resource_names):
    """Retrieves a list of AdGroupAds.

    Args:
        client: A GoogleAdsClient instance.
        customer_id: (str) Customer ID associated with the account.
        new_ad_resource_names: (str) Resource name associated with the Ad group.

    Returns:
        A list of AdGroupAds.
    """

    def _formatter(given_string):
        """Assigns ' ' to names of resources.

        This produces a formatted string that can be used within an IN clause.
        Args:
            given_string: (str) The string to be formatted.
        Returns:
            The formatted string.
        """
        results = []
        for i in given_string:
            results.append(repr(i))
        return ",".join(results)

    resouce_names = _formatter(new_ad_resource_names)

    ga_service = client.get_service("GoogleAdsService")
    query = f"""
        SELECT
            ad_group_ad.ad.id,
            ad_group_ad.ad.expanded_text_ad.headline_part1,
            ad_group_ad.ad.expanded_text_ad.headline_part2,
            ad_group_ad.status,
            ad_group_ad.ad.final_urls,
            ad_group_ad.resource_name
        FROM ad_group_ad
        WHERE ad_group_ad.resource_name in ({resouce_names})"""

    request = client.get_type("SearchGoogleAdsRequest")
    request.customer_id = customer_id
    request.query = query
    request.page_size = PAGE_SIZE

    try:
        response = ga_service.search(request=request)
        return [row.ad_group_ad for row in response.results]
    except GoogleAdsException as ex:
        _handle_googleads_exception(ex)


def _create_keywords(client, ad_group_id, keywords_to_add):
    """Populates keywords on a given ad group ID.

    Args:
        client: An instance of the googleads.adwords.AdWordsClient class.
        ad_group_id: (str) ad group ID to be referenced while creating text ads.
        keywords_to_add: (list) A list of keywords to be added to a given ad
            group.
    """
    ad_group_criterion_service = client.GetService(
        "AdGroupCriterionService", "v201809"
    )
    operations = []
    for keyword in keywords_to_add:
        operation = {
            "xsi_type": "BiddableAdGroupCriterion",
            "adGroupId": ad_group_id,
            "criterion": {
                "xsi_type": "Keyword",
                "text": keyword,
                "matchType": "BROAD",
            },
            "userStatus": "PAUSED",
            "finalUrls": [
                (
                    "http://www.example.com/mars/cruise/"
                    f"?kw={urllib.parse.quote(keyword)}"
                )
            ],
        }
        create_keyword = {"operator": "ADD", "operand": operation}
        operations.append(create_keyword)

    results = ad_group_criterion_service.mutate(operations)
    for result in results["value"]:
        print(
            f'Keyword with ad group ID {result["adGroupId"]}, keyword ID '
            f'{result["criterion"]["id"]}, text '
            f'{result["criterion"]["text"]} and match'
            f'type {result["criterion"]["matchType"]} was created'
        )


def _handle_googleads_exception(exception):
    print(
        f'Request with ID "{exception.request_id}" failed with status '
        f'"{exception.error.code().name}" and includes the following errors:'
    )
    for error in exception.failure.errors:
        print(f'\tError with message "{error.message}".')
        if error.location:
            for field_path_element in error.location.field_path_elements:
                print(f"\t\tOn field: {field_path_element.field_name}")
    sys.exit(1)


if __name__ == "__main__":
    # Initialize client object.
    # It will read the config file. The default file path is the Home Directory.
    googleads_client = GoogleAdsClient.load_from_storage(version="v6")
    adwords_client = adwords.AdWordsClient.LoadFromStorage()

    parser = argparse.ArgumentParser(
        description="Lists all campaigns for specified customer."
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
    budget = _create_campaign_budget(googleads_client, args.customer_id)
    campaign = _create_campaign(googleads_client, args.customer_id, budget)
    ad_group = _create_ad_group(googleads_client, args.customer_id, campaign)
    _create_text_ads(googleads_client, args.customer_id, ad_group)
    _create_keywords(adwords_client, ad_group.id, KEYWORDS_TO_ADD)
