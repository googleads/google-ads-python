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
"""This example creates a search campaign with the help of AdWords Api.

This code example is the first in a series of code examples that shows how to
create a Search campaign using the AdWords API, and then migrate it to Google
Ads API one functionality at a time. See other examples in this directory for
code examples in various stages of migration.

This code example represents the initial state, where the AdWords API is used
to create a campaign budget, a Search campaign, ad groups, keywords and expanded
text ads. None of the functionality has yet been migrated to the Google Ads API.
"""


import datetime
import urllib.parse
import uuid

from googleads import adwords

# Number of ads being added/updated in this code example.
NUMBER_OF_ADS = 5
# The list of keywords being added in this code example.
KEYWORDS_TO_ADD = ["mars cruise", "space hotel"]


def _create_campaign_budget(client):
    """Creates a new budget and returns the newly created budget ID.

    Args:
        client: An instance of the google.ads.googleads.client.GoogleAdsClient
        class.

    Returns:
        (str) Budget ID of the newly created budget.
    """
    budget_service = client.GetService("BudgetService", version="v201809")
    budget = {
        "name": "Interplanetary Cruise Budget #{}".format(uuid.uuid4()),
        "amount": {"microAmount": "50000000"},
        "deliveryMethod": "STANDARD",
    }
    budget_operations = [{"operator": "ADD", "operand": budget}]
    # Add budget.
    results = budget_service.mutate(budget_operations)
    created_budget = results["value"][0]
    print(
        "Budget with ID {} and name {} was created".format(
            created_budget["budgetId"], created_budget["name"]
        )
    )
    return created_budget["budgetId"]


def _create_campaign(client, budget_id):
    """Creates a new campaign and returns the newly created campaign ID.

    Args:
        client: A google.ads.googleads.client.GoogleAdsClient instance.
        budget_id: (str) Budget ID to be referenced while creating Campaign.

    Returns:
        (str) Campaign ID of the newly created Campaign.
    """
    campaign_service = client.GetService("CampaignService", version="v201809")
    campaign = {
        "name": "Interplanetary Cruise #{}".format(uuid.uuid4()),
        "advertisingChannelType": "SEARCH",
        # Recommendation: Set the campaign to PAUSED when creating it to stop the
        # ads from immediately serving. Set to ENABLED once you've added
        # targeting and the ads are ready to serve.
        "status": "PAUSED",
        "biddingStrategyConfiguration": {
            "biddingStrategyType": "MANUAL_CPC",
        },
        "startDate": (datetime.datetime.now() + datetime.timedelta(1)).strftime(
            "%Y%m%d"
        ),
        "endDate": (datetime.datetime.now() + datetime.timedelta(365)).strftime(
            "%Y%m%d"
        ),
        # Budget (required) - note only the budget ID is required.
        "budget": {"budgetId": budget_id},
        "networkSetting": {
            "targetGoogleSearch": "true",
            "targetSearchNetwork": "true",
        },
    }
    campaign_operations = [{"operator": "ADD", "operand": campaign}]
    results = campaign_service.mutate(campaign_operations)
    created_campaign = results["value"][0]
    print(
        "CreatedCampign with ID {} and name {} was created".format(
            created_campaign["id"], created_campaign["name"]
        )
    )
    return created_campaign["id"]


def _create_ad_group(client, campaign_id):
    """Creates a new ad group and returns the new created ad group ID.

    Args:
        client: A google.ads.googleads.client.GoogleAdsClient instance.
        campaign_id: (str) The ID of the campaign under which to create a new
          ad group.

    Returns:
        (str) Ad group ID of the newly created ad group.
    """
    ad_group_service = client.GetService("AdGroupService", "v201809")
    ad_group = {
        "name": "Earth to Mars Cruise #{}".format(uuid.uuid4()),
        "campaignId": campaign_id,
        "status": "ENABLED",
        "biddingStrategyConfiguration": {
            "bids": [
                {
                    # The 'xsi_type' field allows you to specify the xsi:type of the
                    # object being created. It's only necessary when you must provide
                    # an explicit type that the client library can't infer.
                    "xsi_type": "CpcBid",
                    "bid": {"microAmount": 10000000},
                }
            ]
        },
        "adGroupAdRotationMode": "OPTIMIZE",
    }

    adgroup_operations = [{"operator": "ADD", "operand": ad_group}]
    results = ad_group_service.mutate(adgroup_operations)
    created_ad_group = results["value"][0]
    print(
        "Ad group with ID {} and name {} was created".format(
            created_ad_group["id"], created_ad_group["name"]
        )
    )
    return created_ad_group["id"]


def _create_text_ads(client, ad_group_id):
    """Creates text ads using the given ad group ID.

    Args:
        client: A google.ads.googleads.client.GoogleAdsClient instance.
        ad_group_id: (str) Ad group ID to be referenced when creating text ads.
    """
    ad_group_service = client.GetService("AdGroupAdService", "v201809")
    operations = []
    for i in range(NUMBER_OF_ADS):
        operation = {
            "xsi_type": "AdGroupAd",
            "adGroupId": ad_group_id,
            # Additional properties (non-required).
            "status": "PAUSED",
            "ad": {
                "xsi_type": "ExpandedTextAd",
                "headlinePart1": "Cruise #{} to Mars".format(
                    str(uuid.uuid4())[:8]
                ),
                "headlinePart2": "Best Space Cruise Line",
                "headlinePart3": "For Your Loved Ones",
                "description": "Buy your tickets now!",
                "description2": "Discount ends soon",
                "finalUrls": ["http://www.example.com/"],
            },
        }
        adgroup_operations = {"operator": "ADD", "operand": operation}
        operations.append(adgroup_operations)

    results = ad_group_service.mutate(operations)
    for result in results["value"]:
        print(
            "Expanded text ad with ID {} and "
            "headline {}-{} {} was created".format(
                result["ad"]["id"],
                result["ad"]["headlinePart1"],
                result["ad"]["headlinePart2"],
                result["ad"]["headlinePart3"],
            )
        )


def _create_keywords(client, ad_group_id, keywords_to_add):
    """Populates keywords on a given ad group ID.

    Args:
        client: A google.ads.googleads.client.GoogleAdsClient instance.
        ad_group_id: (str) Ad group ID to be referenced when creating text ads.
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
                "http://www.example.com/mars/cruise/?kw={}".format(
                    urllib.parse.quote(keyword)
                )
            ],
        }
        create_keyword = {"operator": "ADD", "operand": operation}
        operations.append(create_keyword)

    results = ad_group_criterion_service.mutate(operations)
    for result in results["value"]:
        print(
            "Keyword with ad group ID {}, keyword ID {}, text {} and match"
            "type {} was created".format(
                result["adGroupId"],
                result["criterion"]["id"],
                result["criterion"]["text"],
                result["criterion"]["matchType"],
            )
        )


if __name__ == "__main__":
    # Initialize the client object.
    # By default, it will read the config file from the Home Directory.
    adwords_client = adwords.AdWordsClient.LoadFromStorage()
    budget_id = _create_campaign_budget(adwords_client)
    campaign_id = _create_campaign(adwords_client, budget_id)
    ad_group_id = _create_ad_group(adwords_client, campaign_id)
    _create_text_ads(adwords_client, ad_group_id)
    _create_keywords(adwords_client, ad_group_id, KEYWORDS_TO_ADD)
