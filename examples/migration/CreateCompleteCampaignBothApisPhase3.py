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
"""This example creates serach campaign with the help of Adwords Api and Google Ads API

This code example is the fourth in a series of code examples that shows how to create
a Search campaign using the AdWords API, and then migrate it to the Google Ads API one
functionality at a time. See other examples in this directory for code examples in various
stages of migration.



In this code example, the functionality to create campaign budget, search campaigns and
ad groups have been migrated to the Google Ads API. The rest of the functionality -
creating keywords and expanded text ads are done using the AdWords API.
"""


import datetime
import uuid
from googleads import adwords
import argparse
import collections
import sys
import six
import urllib.parse
from google.ads.google_ads.client import GoogleAdsClient
from google.ads.google_ads.errors import GoogleAdsException
#Number of ads being added/updated in this code example.
NUMBER_OF_ADS = 5
#The list of keywords being added in this code example.
KEYWORDS_TO_ADD = ["mars cruise", "space hotel" ]
PAGE_SIZE = 1000


def createCampaignBudget(client, customer_id):
    """Creates a new campaign budget and returns it 

    Args:
        client: An instance of the Google Ads client
        customer_id: (str)Customer id associated with the account

    Returns:
        CampaignBudget message class instance of the newly created Buget, 
    """
    campaign_service = client.get_service('CampaignBudgetService')
    operation = client.get_type("CampaignBudgetOperation")
    criterion = operation.create
    criterion.name.value = 'Interplanetary Cruise Budget #{}'.format(
                            uuid.uuid4())
    criterion.delivery_method = client.get_type("BudgetDeliveryMethodEnum").\
                                                STANDARD
    criterion.amount_micros.value = 500000
    response = campaign_service.mutate_campaign_budgets(customer_id, 
                                                        [operation])
    campaignBudgetResourceName = response.results[0].resource_name
    newCampaignBudget = getCampaignBudget(client, customer_id, 
                                          campaignBudgetResourceName)
    print("Added budget named {}".format(newCampaignBudget.name.value))
    return newCampaignBudget


def getCampaignBudget(client, customerId, resource_name):
    """Retrives an instance of CampaignBudget message class associated with
       a given resource name

    Args:
        client: An instance of the Google Ads client
        customer_id: (str)Customer id associated with the account
        resource_name: (str)Resource Name associated with the newly created campaign. 

    Returns:
        CampaignBudget message class instance of the newly created Buget, 
    """
    ga_service = client.get_service("GoogleAdsService")
    query = ("SELECT campaign_budget.id, campaign_budget.name, "
             "campaign_budget.resource_name FROM campaign_budget WHERE "
             "campaign_budget.resource_name = '%s' "%resource_name)
    response = ga_service.search(customerId, query, PAGE_SIZE)
    budget = list(response)[0].campaign_budget
    return budget


def createCampaign(client, customerId, campaignBudget): 
    """Creates a new campaign and returns it.

    Args:
        client: An instance of the Google Ads client
        customer_id: (str)Customer id associated with the account
        campaignBudget: An instance of CampaignBudget message class

    Returns:
        Campaign message class instance of the newly created Campaign 
    """
    operation = client.get_type("CampaignOperation")
    campaign = operation.create
    campaign_service = client.get_service("CampaignService")
    campaign.name.value = 'Interplanetary Cruise#{}'.format(uuid.uuid4())
    campaign.advertising_channel_type = client.get_type(
                                       "AdvertisingChannelTypeEnum").SEARCH
    # Recommendation: Set the campaign to PAUSED when creating it to stop the
    # ads from immediately serving. Set to ENABLED once you've added
    # targeting and the ads are ready to serve.
    campaign.status = client.get_type("CampaignStatusEnum").PAUSED
    campaign.manual_cpc.enhanced_cpc_enabled.value = True
    campaign.campaign_budget.value = campaignBudget.resource_name
    campaign.network_settings.target_google_search.value = True
    campaign.network_settings.target_search_network.value = True
    campaign.network_settings.target_content_network.value = False
    campaign.network_settings.target_partner_search_network.value = False
    campaign.start_date.value =  (datetime.datetime.now() + \
                                    datetime.timedelta(1)).strftime('%Y%m%d')
    campaign.end_date.value = (datetime.datetime.now() + \
                              datetime.timedelta(365)).strftime('%Y%m%d')
    response = campaign_service.mutate_campaigns(customerId, [operation])
    campaignResourceName = response.results[0].resource_name
    newCampaign = getCampaign(client, customerId, campaignResourceName)
    print("Added campaign named {}".format(newCampaign.name.value))
    return newCampaign


def getCampaign(client, customerId, campaignResourceName):
    """Retrives an instance of Campaign message class associated with
       a given resource name

    Args:
        client: An instance of the Google Ads client
        customer_id: (str)Customer id associated with the account
        campaignBudget: An instance of CampaignBudget message class
        resource_name: (str)Resource Name associated with the newly created campaign budget. 


    Returns:
        Campaign message class instance of the newly created Campaign 
    """
    ga_service = client.get_service("GoogleAdsService")
    query = ("SELECT campaign.id, campaign.name, campaign.resource_name "
            "FROM campaign WHERE campaign.resource_name = '%s' "%
            campaignResourceName)
    response = ga_service.search(customerId, query, PAGE_SIZE)
    campaign = list(response)[0].campaign
    return campaign


def createAdGroup(client, customerId, campaign):
    """Creates a new Adgroup and returns it.

    Args:
        client: An instance of the Google Ads client
        customer_id: (str)Customer id associated with the account
        campaign: An instance of Campaign message class

    Returns:
        Adgroup message class instance of the newly created Adgroup 
    """
    operation = client.get_type("AdGroupOperation")
    adgroup = operation.create
    adgroup_service = client.get_service("AdGroupService")
    adgroup.name.value  = 'Earth to Mars Cruises #{}'.format(uuid.uuid4())
    adgroup.campaign.value = campaign.resource_name 
    adgroup.status = client.get_type("AdGroupStatusEnum").ENABLED
    adgroup.type = client.get_type("AdGroupTypeEnum").SEARCH_STANDARD
    adgroup.cpc_bid_micros.value = 10000000  
    response = adgroup_service.mutate_ad_groups(customerId, [operation])
    adGroupResourceName = response.results[0].resource_name
    adGroup = getAdGroup(client, customerId, adGroupResourceName)
    print("Added AdGroup named {}".format(adGroup.name.value))
    return adGroup


def getAdGroup(client, customerId, adGroupResourceName):
    """Retrives an instance of Adgroup message class associated with
       a given resource name

    Args:
        client: An instance of the Google Ads client
        customer_id: (str)Customer id associated with the account
        adGroupResourceName: (str)Resource Name associated with the newly created campaign Ad group. 

    Returns:
        Adgroup message class instance of the newly created Adgroup 
    """
    ga_service = client.get_service("GoogleAdsService")
    query = ("SELECT ad_group.id, ad_group.name, ad_group.resource_name "
             "FROM ad_group WHERE ad_group.resource_name = '{}' ".format(
             adGroupResourceName))
    response = ga_service.search(customerId, query, PAGE_SIZE)
    adGroup = list(response)[0].ad_group
    return adGroup


def createTextAds(client, adGroupId):
    """Creates TextAds on the given Adgroup ID.

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
  #It will read the config file. Default file path is the Home Directory
  google_ads_client = GoogleAdsClient.load_from_storage()
  adwords_client = adwords.AdWordsClient.LoadFromStorage()

  parser = argparse.ArgumentParser(
        description='Lists all campaigns for specified customer.')
    # The following argument(s) should be provided to run the example.
  parser.add_argument('-c', '--customer_id', type=six.text_type,
                        required=True, help='The Google Ads customer ID.')
  args = parser.parse_args()
  budget = createCampaignBudget(google_ads_client, args.customer_id)
  campaign = createCampaign(google_ads_client, args.customer_id, budget)
  adGroup = createAdGroup(google_ads_client, args.customer_id, campaign)
  createTextAds(adwords_client, adGroup.id.value)
  createKeywords(adwords_client, adGroup.id.value, KEYWORDS_TO_ADD)
