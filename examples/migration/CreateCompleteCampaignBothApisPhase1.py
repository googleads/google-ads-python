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
"""This example creates serach campaign with the help of Adwords Api and Google Ads API"""


"""This code example is the second in a series of code examples that shows how to create
a Search ad_group using the AdWords API, and then migrate it to the Google Ads API one
functionality at a time. See other examples in this directory for code examples in various
stages of migration.

In this code example, the functionality to create ad_group budget has been migrated to
the Google Ads API. The rest of the functionality - creating a Search ad_group, ad groups,
keywords and expanded text ads are done using the AdWords API.
"""

import datetime
import uuid
from googleads import adwords
import argparse
import collections
import sys
import six
from google.ads.google_ads.client import GoogleAdsClient
from google.ads.google_ads.errors import GoogleAdsException
#Number of ads being added/updated in this code example.
NUMBER_OF_ADS = 5
#The list of keywords being added in this code example.
KEYWORDS_TO_ADD = ["mars cruise", "space hotel" ]
import urllib.parse
PAGE_SIZE = 1000


def createCampaignBudget(client, customer_id):
    campaign_service = client.get_service('CampaignBudgetService')
    operation = client.get_type("CampaignBudgetOperation")
    criterion = operation.create
    criterion.name.value = 'Interplanetary Cruise Budget #%s' % uuid.uuid4()
    criterion.delivery_method = client.get_type("BudgetDeliveryMethodEnum").\
                                                STANDARD
    criterion.amount_micros.value = 500000
    response = campaign_service.mutate_campaign_budgets(customer_id, \
                                                        [operation])
    campaignBudgetResourceName = response.results[0].resource_name
    newCampaignBudget = getCampaignBudget(client, customer_id, \
                                          campaignBudgetResourceName)
    print("Added budget named {}".format(newCampaignBudget.name.value))
    return newCampaignBudget


def getCampaignBudget(client, customerId, resource_name):
    ga_service = client.get_service("GoogleAdsService")
    query = ("SELECT campaign_budget.id, campaign_budget.name, "
             "campaign_budget.resource_name FROM campaign_budget WHERE "
             "campaign_budget.resource_name = '%s' "%resource_name)
    response = ga_service.search(customerId, query, PAGE_SIZE)
    budget = list(response)[0].campaign_budget
    return budget


def createCampaign(client, budgetId):
    campaign_service = client.GetService('CampaignService', version='v201809')
    campaign = {
        'name': 'Interplanetary Cruise #%s' % uuid.uuid4(),
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
    print("CreatedCampign with ID {} and name {} was created". \
           format(createdCampaign['id'],createdCampaign['name']))
    return createdCampaign['id']


def createAdGroup(client, campaign_id):
    ad_group_service = client.GetService('AdGroupService', 'v201809')
    ad_group =   {
        'name': 'Earth to Mars Cruise #%s' % uuid.uuid4(),
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
    print("Ad group with ID {} and name {} was created".\
        format(createdAdgroup['id'],createdAdgroup['name']))
    return createdAdgroup['id']


def createTextAds(client, adGroupId):
    ad_group_service = client.GetService('AdGroupAdService', 'v201809')
    operations = []
    for i in range(NUMBER_OF_ADS):
        operation =  {
            'xsi_type': 'AdGroupAd',
            'adGroupId': adGroupId,
            # Additional properties (non-required).
            'status':  'PAUSED',
            'ad': {
                'xsi_type': 'ExpandedTextAd',
                'headlinePart1': ('Cruise #%s to Mars'
                            % str(uuid.uuid4())[:8]),
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
        print('Expanded text ad with ID {} and headline {}-{} {} was created'\
              .format(result['ad']['id'],result['ad']['headlinePart1'],\
               result['ad']['headlinePart2'],result['ad']['headlinePart3']))


def createKeywords(client, adGroupId, keywordsToAdd):
    AdGroupCriterionService = client.GetService("AdGroupCriterionService", \
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
        'finalUrls' : ['http://www.example.com/mars/cruise/?kw=%s'% \
                       urllib.parse.quote(keyword)]
        }
        create_keyword = {
            'operator': 'ADD',
            'operand': operation
        }
        operations.append(create_keyword)
    results = AdGroupCriterionService.mutate(operations)
    for result in results['value']:
        print("Keyword with ad group ID {}, keyword ID {}, text {} and match"
              "type {} was created".format(result['adGroupId'], \
               result['criterion']['id'],result['criterion']['text'],\
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
  campaignId = createCampaign(adwords_client, budget.id.value)
  adGroupId = createAdGroup(adwords_client, campaignId)
  createTextAds(adwords_client, adGroupId)
  createKeywords(adwords_client, adGroupId, KEYWORDS_TO_ADD)

