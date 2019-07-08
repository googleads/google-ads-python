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
    print("Added budget named {}".format(newCampaignBudget.name.value))
    return newCampaignBudget
    #return newCampaignBudget



def getCampaignBudget(client, customerId, resource_name):
    ga_service = client.get_service("GoogleAdsService")
    query = ("SELECT campaign_budget.id, campaign_budget.name, campaign_budget.resource_name "
              "FROM campaign_budget WHERE campaign_budget.resource_name = '%s' "%resource_name)
    response = ga_service.search(customerId, query, PAGE_SIZE)
    budget = list(response)[0].campaign_budget
    return budget




    
'''
     * Creates a campaign .
     * @param adwordsclient
     * @param budgetId the campaign budget ID
     * @return Campaign the newly created campaign
'''


def createCampaign(client, customerId, campaignBudget): 
    operation = client.get_type("CampaignOperation")
    campaign = operation.create
    campaign_service = client.get_service("CampaignService")
    campaign.name.value = 'Interplanetary Cruise#%s' % uuid.uuid4()
    campaign.advertising_channel_type = client.get_type("AdvertisingChannelTypeEnum").SEARCH
    campaign.status = client.get_type("CampaignStatusEnum").PAUSED
    campaign.manual_cpc.enhanced_cpc_enabled.value = True
    campaign.campaign_budget.value = campaignBudget.resource_name
    campaign.network_settings.target_google_search.value = True
    campaign.network_settings.target_search_network.value =True
    campaign.network_settings.target_content_network.value =False
    campaign.network_settings.target_partner_search_network.value =False
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
    ga_service = client.get_service("GoogleAdsService")
    query = ("SELECT campaign.id,campaign.name, campaign.resource_name "
          "FROM campaign WHERE campaign.resource_name = '%s' "%campaignResourceName)
    response = ga_service.search(customerId, query, PAGE_SIZE)
    campaign = list(response)[0].campaign
    return campaign


def createAdGroup(client, customerId, campaign):
    operation = client.get_type("AdGroupOperation")
    adgroup = operation.create
    adgroup_service = client.get_service("AdGroupService")
    adgroup.name.value  = 'Earth to Mars Cruises #%s'% uuid.uuid4()
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
    ga_service = client.get_service("GoogleAdsService")
    query = ("SELECT ad_group.id, ad_group.name, ad_group.resource_name "
          "FROM ad_group WHERE ad_group.resource_name = '%s' "%adGroupResourceName)
    response = ga_service.search(customerId, query, PAGE_SIZE)
    adGroup = list(response)[0].ad_group
    return adGroup



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
    budget = createCampaignBudget(google_ads_client, six.text_type(7502950076))
    campaign = createCampaign(google_ads_client, six.text_type(7502950076), budget)
    adgroup = createAdGroup(google_ads_client, six.text_type(7502950076),campaign)

   

