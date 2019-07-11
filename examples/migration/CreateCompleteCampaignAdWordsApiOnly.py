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
"""This example creates serach campaign with the help of Adwords Api

This code example is the first in a series of code examples that shows how to create
a Search campaign using the AdWords API, and then migrate it to Google Ads API one
functionality at a time. See other examples in this directory for code examples in various
stages of migration.

This code example represents the initial state, where the AdWords API is used to create a
campaign budget, a Search campaign, ad groups, keywords and expanded text ads. None of the
functionality has yet been migrated to the Google Ads API.
"""


import datetime
import uuid
from googleads import adwords
import urllib.parse
# Number of ads being added/updated in this code example.
NUMBER_OF_ADS = 5
# The list of keywords being added in this code example.
KEYWORDS_TO_ADD = ["mars cruise", "space hotel" ]


def createCampaignBudget(client):
    """Creates a new budget and returns the newly created budget id.

    Args:
        client: An instance of the Adwords client

    Returns:
        (str)Budget id of the newly created budget.
    """
    budget_service = client.GetService('BudgetService', version='v201809')
    budget = {
        'name' : 'Interplanetary Cruise Budget #%s' % uuid.uuid4(),
        'amount': {
            'microAmount' : '50000000'
        },
        'deliveryMethod' : 'STANDARD'
    }
    budget_operations = [{
        'operator': 'ADD',
        'operand': budget
    }]
    # Add budget.
    results = budget_service.mutate(budget_operations)
    createdBudget = results['value'][0]
    print("Budget with ID {} and name {} was created".format(
           createdBudget['budgetId'], createdBudget['name']))
    return createdBudget['budgetId']


def createCampaign(client, budgetId):
    """Creates a new campaign and returns the newly created campaign id.

    Args:
        client: An instance of the Adwords client
        budgetId: (str) Budget id to be referenced while creating Campaign

    Returns:
        (str)Campaign id of the newly created Campaign.
    """
    campaign_service = client.GetService('CampaignService', version='v201809')
    campaign = {
        'name': 'Interplanetary Cruise #{}'.format(uuid.uuid4()),
        'advertisingChannelType': 'SEARCH',
        # Recommendation: Set the campaign to PAUSED when creating it to stop the
        # ads from immediately serving. Set to ENABLED once you've added
        # targeting and the ads are ready to serve.
        'status': 'PAUSED',
        'biddingStrategyConfiguration': {
            'biddingStrategyType': 'MANUAL_CPC',
        },
        'startDate': (datetime.datetime.now() +
        datetime.timedelta(1)).strftime('%Y%m%d'),
        'endDate': (datetime.datetime.now() +
        datetime.timedelta(365)).strftime('%Y%m%d'),
        # Budget (required) - note only the budget ID is required.
        'budget': {
            'budgetId': budgetId
        },
        'networkSetting': {
            'targetGoogleSearch': 'true',
            'targetSearchNetwork': 'true',
        }
    }
    campaign_operations = [{
        'operator': 'ADD',
        'operand': campaign
    }]
    results = campaign_service.mutate(campaign_operations)
    createdCampaign = results['value'][0]
    print("CreatedCampign with ID {} and name {} was created".format(
           createdCampaign['id'], createdCampaign['name']))
    return createdCampaign['id']


def createAdGroup(client, campaign_id):
    """Creates a new adgroup and returns the newly created adgroup id.

    Args:
        client: An instance of the Adwords client
        campaign_id: (str) Campaign id to be referenced while creating Adgroup
        
    Returns:
        (str)Adgroup id of the newly created Adgroup.
    """
    ad_group_service = client.GetService('AdGroupService', 'v201809')
    ad_group = {
        'name': 'Earth to Mars Cruise #{}'.format(uuid.uuid4()),
        'campaignId': campaign_id,
        'status': 'ENABLED',
        'biddingStrategyConfiguration' : {
            'bids': [{
              # The 'xsi_type' field allows you to specify the xsi:type of the
              # object being created. It's only necessary when you must provide
              # an explicit type that the client library can't infer.
                'xsi_type': 'CpcBid',
                'bid': {
                    'microAmount': 10000000
                }
            }]
        },
        'adGroupAdRotationMode': 'OPTIMIZE'
    }

    adgroup_operations = [{
        'operator': 'ADD',
        'operand': ad_group
    }]
    results = ad_group_service.mutate(adgroup_operations)
    createdAdgroup = results['value'][0]
    print("Ad group with ID {} and name {} was created".format(
         createdAdgroup['id'], createdAdgroup['name']))
    return createdAdgroup['id']


def createTextAds(client, adGroupId):
    """Creates nextTextAds on the given Adgroup ID.

    Args:
        client: An instance of the Adwords client
        adGroupId: (str) adGroup id to be referenced while creating text Ads
        
    Returns:
        None
    """
    ad_group_service = client.GetService('AdGroupAdService', 'v201809')
    operations = []
    for i in range(NUMBER_OF_ADS):
        operation = {
            'xsi_type': 'AdGroupAd',
            'adGroupId': adGroupId,
            # Additional properties (non-required).
            'status': 'PAUSED',
            'ad': {
                'xsi_type': 'ExpandedTextAd',
                'headlinePart1': 'Cruise #{} to Mars'.format(
                                  str(uuid.uuid4())[:8]),
                'headlinePart2': 'Best Space Cruise Line',
                'headlinePart3': 'For Your Loved Ones',
                'description': 'Buy your tickets now!',
                'description2': 'Discount ends soon',
                'finalUrls': ['http://www.example.com/']
            }
        }
        adgroup_operations = {
            'operator': 'ADD',
            'operand': operation
         }
        operations.append(adgroup_operations)

    results = ad_group_service.mutate(operations)
    for result in results['value']:
        print("Expanded text ad with ID {} and "
              "headline {}-{} {} was created".format(
               result['ad']['id'], result['ad']['headlinePart1'],
               result['ad']['headlinePart2'], result['ad']['headlinePart3']))


def createKeywords(client, adGroupId, keywordsToAdd):
    """Creates Keywords on the given Adgroup ID.

    Args:
        client: An instance of the Adwords client
        adGroupId: (str) adGroup id to be referenced while creating text Ads
        keywordsToAdd: (list) A list of keywords to be added to a given AdGroup
        
    Returns:
        None
    """
    ad_group_criterion_service = client.GetService('AdGroupCriterionService',
                                                   'v201809')
    operations = []
    for keyword in KEYWORDS_TO_ADD:
        operation = {
            'xsi_type': 'BiddableAdGroupCriterion',
            'adGroupId': adGroupId,
            'criterion': {
                'xsi_type' : 'Keyword',
                'text': keyword,
                'matchType' : 'BROAD'
            },
            'userStatus': 'PAUSED',
            'finalUrls' : ['http://www.example.com/mars/cruise/?kw={}'.format(
                           urllib.parse.quote(keyword))]
        }
        create_keyword = {
            'operator': 'ADD',
            'operand': operation
        }
        operations.append(create_keyword)

    results = ad_group_criterion_service.mutate(operations)
    for result in results['value']:
        print("Keyword with ad group ID {}, keyword ID {}, text {} and match"
              "type {} was created".format(result['adGroupId'], 
               result['criterion']['id'], result['criterion']['text'],
               result['criterion']['matchType']))


if __name__ == '__main__':
  # Initialize client object.
  # It will read the config file from the Home Directory
  adwords_client = adwords.AdWordsClient.LoadFromStorage()
  budgetId = createCampaignBudget(adwords_client)
  campaignId = createCampaign(adwords_client, budgetId)
  adGroupId = createAdGroup(adwords_client, campaignId)
  createTextAds(adwords_client, adGroupId)
  createKeywords(adwords_client, adGroupId, KEYWORDS_TO_ADD)
