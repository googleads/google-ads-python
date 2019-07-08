#!/usr/bin/env python
import datetime
import uuid
from googleads import adwords
#Number of ads being added/updated in this code example.
NUMBER_OF_ADS = 5
#The list of keywords being added in this code example.
KEYWORDS_TO_ADD = ["mars cruise", "space hotel" ]
import urllib.parse

'''
     * Creates a campaign budget.
     * @param adwordsclient 
     * @return Budget the newly created campaign budget
'''
def createCampaignBudget(client):
    budget_service = client.GetService('BudgetService', version='v201809')
    budget = {
    'name': 'Interplanetary Cruise Budget #%s' % uuid.uuid4(),
    'amount': {
      'microAmount': '50000000'
    },
    'deliveryMethod': 'STANDARD'
    }

    budget_operations = [{
    'operator': 'ADD',
    'operand': budget
    }]
    results = budget_service.mutate(budget_operations)
    createdBudget = results['value'][0]
    print("Budget with ID {} and name {} was created".format(\
            createdBudget['budgetId'],createdBudget['name']))
    return createdBudget['budgetId']

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
  # Initialize client object.
  adwords_client = adwords.AdWordsClient.LoadFromStorage()
  budgetId = createCampaignBudget(adwords_client)
  campaignId = createCampaign(adwords_client, budgetId)
  adgroupid = createAdGroup(adwords_client, campaignId)
  createTextAds(adwords_client, adgroupid)
  createKeywords(adwords_client, adgroupid, KEYWORDS_TO_ADD)



