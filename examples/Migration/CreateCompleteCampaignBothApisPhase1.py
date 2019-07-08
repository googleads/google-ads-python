#!/usr/bin/env python
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

'''
     * Creates a campaign budget.
     * @param adwordsclient 
     * @return Budget the newly created campaign budget
'''
def createCampaignBudget(client, customer_id):
    campaign_service = client.get_service('CampaignBudgetService')
    operation = client.get_type("CampaignBudgetOperation")
    criterion = operation.create
    criterion.name.value = 'Interplanetary Cruise Budget #%s' % uuid.uuid4()
    criterion.delivery_method = client.get_type("BudgetDeliveryMethodEnum").STANDARD
    criterion.amount_micros.value = 500000
    response = campaign_service.mutate_campaign_budgets(customer_id, [operation])
    campaignBudgetResourceName = response.results[0].resource_name
    newCampaignBudget = getCampaignBudget(client, customer_id, campaignBudgetResourceName)



def getCampaignBudget(client, customerId, resource_name):
    ga_service = client.get_service("GoogleAdsService")
    query = ("SELECT campaign_budget.id, campaign_budget.name, campaign_budget.resource_name "
              "FROM campaign_budget WHERE campaign_budget.resource_name = '%s' "%resource_name)
    response = ga_service.search(customerId, query, PAGE_SIZE)
    budgetId = list(response)[0].campaign_budget.id.value
    return budgetId




    
'''
     * Creates a campaign .
     * @param adwordsclient
     * @param budgetId the campaign budget ID
     * @return Campaign the newly created campaign
'''
def createCampaign(client, budgetId):
    campaign_service = client.GetService('CampaignService', version='v201809')
    campaign = {
    'name': 'Interplanetary Cruise #%s' % uuid.uuid4(),
    'advertisingChannelType': 'SEARCH',
    'status': 'PAUSED',

    'biddingStrategyConfiguration': {
    'biddingStrategyType': 'MANUAL_CPC',
    },
    'startDate': (datetime.datetime.now() +
    datetime.timedelta(1)).strftime('%Y%m%d'),

    'endDate': (datetime.datetime.now() +
    datetime.timedelta(365)).strftime('%Y%m%d'),
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
'''
     * Creates an ad group.
     * @param adwordsclient
     * @param int $campaignId the campaign ID
     * @return AdGroup the newly created ad group
'''

def createAdGroup(client, campaign_id):
  ad_group_service = client.GetService('AdGroupService', 'v201809')
  ad_group = {
      'name': 'Earth to Mars Cruise #%s' % uuid.uuid4(),
      'campaignId': campaign_id,
      'status': 'ENABLED',
      'biddingStrategyConfiguration' : {

         'bids': [{
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


'''
     * Creates text ads.
     * @param adwords client
     * @param int adGroupId the ad group ID
 '''
def createTextAds(client, adGroupId):
    ad_group_service = client.GetService('AdGroupAdService', 'v201809')
    operations = []
    for i in range(NUMBER_OF_ADS):
        operation = {
            'xsi_type': 'AdGroupAd',
            'adGroupId': adGroupId,
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
        print('Expanded text ad with ID {} and headline {}-{} {} was created' \
            .format(result['ad']['id'],result['ad']['headlinePart1'],\
                result['ad']['headlinePart2'],result['ad']['headlinePart3']))


'''
     * Creates keywords
     * @param adwords client
     * @param int adGroupId the ad group ID
     * @param list keywordsToAdd the keywords to add
 '''
def createKeywords(client, adGroupId, keywordsToAdd):
    adGroupCriterionService=client.GetService("AdGroupCriterionService", \
                                              'v201809')
    operations = []
    for keyword in KEYWORDS_TO_ADD:
        operation ={

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
    results= adGroupCriterionService.mutate(operations)
    for result in results['value']:
        print('Keyword with ad group ID {}, keyword ID {}, text {} and match\
               type {} was created'.format(result['adGroupId'], \
               result['criterion']['id'],result['criterion']['text'],\
               result['criterion']['matchType']))



if __name__ == '__main__':
  
    google_ads_client = GoogleAdsClient.load_from_storage()
    adwords_client = adwords.AdWordsClient.LoadFromStorage()
    createCampaignBudget(google_ads_client, six.text_type(7502950076))

