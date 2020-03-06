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
"""This example creates a search campaign with the help of Google Ads API only.

This code example is the last in a series of code examples that shows how to
create a Search campaign using the AdWords API, and then migrate it to the
Google Ads API one functionality at a time. See other examples in this directory
for code examples in various stages of migration.

This code example represents the final state, where all the functionality - create a
campaign budget, a Search campaign, ad groups, keywords and expanded text ads have been
migrated to using the Google Ads API. The AdWords API is not used.
"""

import argparse
import collections
import datetime
import sys
import urllib.parse
import uuid


from google.ads.google_ads.client import GoogleAdsClient
from google.ads.google_ads.errors import GoogleAdsException

# Number of ads being added/updated in this code example.
NUMBER_OF_ADS = 5
# The list of keywords being added in this code example.
KEYWORDS_TO_ADD = ['mars cruise', 'space hotel']
PAGE_SIZE = 1000


def create_campaign_budget(client, customer_id):
    """Creates a new campaign budget and returns it.

    Args:
        client: A google.ads.google_ads.client.GoogleAdsClient instance.
        customer_id: (str) Customer ID associated with the account.

    Returns:
        An instance of google.ads.google_ads.v2.types.CampaignBudget for the
            newly created Budget.
    """
    campaign_service = client.get_service('CampaignBudgetService', version='v3')
    operation = client.get_type('CampaignBudgetOperation', version='v3')
    criterion = operation.create
    criterion.name.value = 'Interplanetary Cruise Budget #{}'.format(
                            uuid.uuid4())
    criterion.delivery_method = client.get_type(
                                'BudgetDeliveryMethodEnum',
                                version='v3').STANDARD
    criterion.amount_micros.value = 500000
    response = campaign_service.mutate_campaign_budgets(customer_id,
               [operation])
    campaign_budget_resource_name = response.results[0].resource_name
    new_campaign_budget = get_campaign_budget(client, customer_id,
                          campaign_budget_resource_name)
    print('Added budget named {}'.format(new_campaign_budget.name.value))
    return new_campaign_budget


def get_campaign_budget(client, customer_id, resource_name):
    """Retrieves a google.ads.google_ads.v2.types.CampaignBudget instance.

    Args:
        client: A google.ads.google_ads.client.GoogleAdsClient instance.
        customer_id: (str) Customer ID associated with the account.
        resource_name: (str) Resource name associated with the newly created
            campaign.

    Returns:
        An instance of google.ads.google_ads.v2.types.CampaignBudget for the
            newly created Budget.
    """
    ga_service = client.get_service('GoogleAdsService', version='v3')
    query = ('SELECT campaign_budget.id, campaign_budget.name, '
             'campaign_budget.resource_name FROM campaign_budget WHERE '
             'campaign_budget.resource_name = "{}"'.format(resource_name))
    response = ga_service.search(customer_id, query, PAGE_SIZE)
    budget = list(response)[0].campaign_budget
    return budget


def create_campaign(client, customer_id, campaign_budget):
    """Creates a new campaign and returns it.

    Args:
        client: A google.ads.google_ads.client.GoogleAdsClient instance.
        customer_id: (str) Customer ID associated with the account.
        campaign_budget: A google.ads.google_ads.v2.types.CampaignBudget
            instance.

    Returns:
        A google.ads.google_ads.v2.types.GoogleAdsClient message class instance.
    """
    operation = client.get_type('CampaignOperation', version='v3')
    campaign = operation.create
    campaign_service = client.get_service('CampaignService', version='v3')
    campaign.name.value = 'Interplanetary Cruise#{}'.format(uuid.uuid4())
    campaign.advertising_channel_type = client.get_type(
                                        'AdvertisingChannelTypeEnum',
                                        version='v3').SEARCH
    # Recommendation: Set the campaign to PAUSED when creating it to stop the
    # ads from immediately serving. Set to ENABLED once you've added
    # targeting and the ads are ready to serve.
    campaign.status = client.get_type('CampaignStatusEnum', version='v3').PAUSED
    campaign.manual_cpc.enhanced_cpc_enabled.value = True
    campaign.campaign_budget.value = campaign_budget.resource_name
    campaign.network_settings.target_google_search.value = True
    campaign.network_settings.target_search_network.value = True
    campaign.network_settings.target_content_network.value = False
    campaign.network_settings.target_partner_search_network.value = False
    campaign.start_date.value =  (datetime.datetime.now() + 
                                  datetime.timedelta(1)).strftime('%Y%m%d')
    campaign.end_date.value = (datetime.datetime.now() + 
                               datetime.timedelta(365)).strftime('%Y%m%d')
    response = campaign_service.mutate_campaigns(customer_id, [operation])
    campaign_resource_name = response.results[0].resource_name
    new_campaign = get_campaign(client, customer_id, campaign_resource_name)
    print('Added campaign named {}'.format(new_campaign.name.value))
    return new_campaign


def get_campaign(client, customer_id, campaign_resource_name):
    """Retrieves a google.ads.google_ads.v2.types.Campaign instance.

    Args:
        client: A google.ads.google_ads.client.GoogleAdsClient instance.
        customer_id: (str) Customer ID associated with the account.
        campaign_resource_name: (str) Resource name associated with the newly
            created campaign budget.

    Returns:
        A google.ads.google_ads.v2.types.GoogleAdsClient message class instance.
    """
    ga_service = client.get_service('GoogleAdsService', version='v3')
    query = ('SELECT campaign.id, campaign.name, campaign.resource_name '
             'FROM campaign WHERE campaign.resource_name = "{}" '
             .format(campaign_resource_name))
    response = ga_service.search(customer_id, query, PAGE_SIZE)
    campaign = list(response)[0].campaign
    return campaign


def create_ad_group(client, customer_id, campaign):
    """Creates a new ad group and returns it.

    Args:
        client: A google.ads.google_ads.client.GoogleAdsClient instance.
        customer_id: (str) Customer ID associated with the account.
        campaign: A google.ads.google_ads.v2.types.Campaign instance.

    Returns:
        An instance of the google.ads.google_ads.v2.types.AdGroup message class
            of the newly created ad group.
    """
    operation = client.get_type('AdGroupOperation', version='v3')
    adgroup = operation.create
    adgroup_service = client.get_service('AdGroupService', version='v3')
    adgroup.name.value  = 'Earth to Mars Cruises #{}'.format(uuid.uuid4())
    adgroup.campaign.value = campaign.resource_name
    adgroup.status = client.get_type('AdGroupStatusEnum',
                     version='v3').ENABLED
    adgroup.type = client.get_type('AdGroupTypeEnum',
                   version='v3').SEARCH_STANDARD
    adgroup.cpc_bid_micros.value = 10000000
    response = adgroup_service.mutate_ad_groups(customer_id, [operation])
    ad_group_resource_name = response.results[0].resource_name
    ad_group = get_ad_group(client, customer_id, ad_group_resource_name)
    print('Added AdGroup named {}'.format(ad_group.name.value))
    return ad_group


def get_ad_group(client, customer_id, ad_group_resource_name):
    """Retrieves a google.ads.googleads_v2.types.AdGroup instance.

    Args:
        client: A google.ads.google_ads.client.GoogleAdsClient instance.
        customer_id: (str) Customer ID associated with the account.
        ad_group_resource_name: (str) Resource name associated with the newly
            created Ad group.

    Returns:
        An instance of the google.ads.google_ads.v2.types.AdGroup message class
            of the newly created ad group.
    """
    ga_service = client.get_service('GoogleAdsService', version='v3')
    query = ('SELECT ad_group.id, ad_group.name, ad_group.resource_name '
             'FROM ad_group WHERE ad_group.resource_name = "{}" '
             .format(ad_group_resource_name))
    response = ga_service.search(customer_id, query, PAGE_SIZE)
    adGroup = list(response)[0].ad_group
    return adGroup


def create_text_ads(client, customer_id, ad_group):
    """Creates new text ads in a given ad group.

    Args:
        client: A google.ads.google_ads.client.GoogleAdsClient instance.
        customer_id: (str) Customer ID associated with the account.
        ad_group: A google.ads.google_ads.v2.types.AdGroup instance.
    """
    operations = []
    for i in range(0, NUMBER_OF_ADS):
        operation = client.get_type('AdGroupAdOperation', version='v3')
        ad_group_operation = operation.create
        ad_group_operation.ad_group.value =  ad_group.resource_name
        ad_group_operation.status = client.get_type('AdGroupAdStatusEnum',
                                    version='v3').PAUSED
        ad_group_operation.ad.expanded_text_ad.headline_part1.value = \
            'Cruise to Mars #{}'.format(str(uuid.uuid4())[:4])
        ad_group_operation.ad.expanded_text_ad.headline_part2.value = \
            'Best Space Cruise Line'
        ad_group_operation.ad.expanded_text_ad.description.value = \
            'Buy your tickets now!'
        final_urls =  client.get_type('StringValue', version='v3')
        final_urls.value = 'http://www.example.com'
        ad_group_operation.ad.final_urls.extend([final_urls])
        operations.append(operation)

    adgroup_service = client.get_service('AdGroupAdService', version='v3')
    ad_group_ad_response = adgroup_service.mutate_ad_group_ads(customer_id,
                           operations)
    new_ad_resource_names = []
    for i in range(NUMBER_OF_ADS):
        new_ad_resource_names.append(
        ad_group_ad_response.results[i].resource_name)

    new_ads = get_ads(client, customer_id, new_ad_resource_names)
    for i in range(len(new_ads)):
        print('Created expanded text ad with ID {}, status {} and '
              'headline {}.{}'.format(new_ads[i].ad.id.value,
              new_ads[i].status,
              new_ads[i].ad.expanded_text_ad.headline_part1.value,
              new_ads[i].ad.expanded_text_ad.headline_part2.value))


def get_ads(client, customer_id, new_ad_resource_names):
    """Retrieves a google.ads.google_ads.v2.types.AdGroupAd instance.

    Args:
        client: A google.ads.google_ads.client.GoogleAdsClient instanc  e.
        customer_id: (str) Customer ID associated with the account.
        new_ad_resource_names: (str) Resource name associated with the Ad group.

    Returns:
        An instance of the google.ads.google_ads.v2.types.AdGroupAd message
            class of the newly created ad group ad.
    """
    def formatter(given_string):
        """This helper function is used to assign ' ' to names of resources
        so that this formatted string can be used within an IN clause.

        Args:
            given_string: (str) The string to be formatted.
        """
        results = []
        for i in given_string:
            results.append(repr(i))
        return ','.join(results)
    resouce_names = formatter(new_ad_resource_names)

    ga_service = client.get_service('GoogleAdsService', version='v3')
    query = ('SELECT ad_group_ad.ad.id, '
             'ad_group_ad.ad.expanded_text_ad.headline_part1, '
             'ad_group_ad.ad.expanded_text_ad.headline_part2, '
             'ad_group_ad.status, ad_group_ad.ad.final_urls, '
             'ad_group_ad.resource_name '
             'FROM ad_group_ad '
             'WHERE ad_group_ad.resource_name in ({}) '.
             format(resouce_names))

    response = ga_service.search(customer_id, query, PAGE_SIZE)
    response =iter(response)
    ads = []

    while  response:
        try:
            current_row = next(response)
            ads.append(current_row.ad_group_ad)
        except StopIteration:
            break

    return ads


def create_keywords(client, customer_id, ad_group, keywords_to_add):
    """Creates new keywords on a given ad group.

    Args:
        client: A google.ads.google_ads.client.GoogleAdsClient instance.
        customer_id: (str) Customer ID associated with the account.
        ad_group: A google.ads.google_ads.v2.types.AdGroup instance.
        keywords_to_add: keywords_to_add: (list) A list of keywords which are to
            be added to a given ad group.
    """
    ad_group_criterion_operations = []
    for keyword in keywords_to_add:
        operation = client.get_type('AdGroupCriterionOperation', version='v3')
        ad_group_criterion_operation = operation.create
        ad_group_criterion_operation.ad_group.value = ad_group.resource_name
        ad_group_criterion_operation.status = client.get_type(
                                              'AdGroupCriterionStatusEnum',
                                              version='v3').ENABLED
        ad_group_criterion_operation.keyword.text.value = keyword
        ad_group_criterion_operation.keyword.match_type = client.get_type(
            'KeywordMatchTypeEnum', version='v3').EXACT
        ad_group_criterion_operations.append(operation)

    ad_group_criterion_service_client = client.get_service(
                                        'AdGroupCriterionService', version='v3')
    ad_group_criterion_response = ad_group_criterion_service_client.\
                                  mutate_ad_group_criteria(customer_id,
                                  ad_group_criterion_operations)
    new_ad_resource_names = []

    for i in range(len(keywords_to_add)):
        new_ad_resource_names.append(
        ad_group_criterion_response.results[i].resource_name)

    new_keywords = get_keywords(client, customer_id, new_ad_resource_names)
    for i in range(len(new_keywords)):
        print('Keyword with text {}, id = {} and '
              'match type {} was created'.format(
              new_keywords[i].keyword.text.value,
              new_keywords[i].criterion_id.value,
              new_keywords[i].keyword.match_type))


def get_keywords(client, customer_id, keyword_resource_names):
    """Retrieves a google.ads.google_ads.v2.types.AdGroupCriterion instance.

    Args:
        client: A google.ads.google_ads.client.GoogleAdsClient instance.
        customer_id: (str) Customer ID associated with the account.
        keyword_resource_names: (str) Resource name associated with the newly
            created ad group criterion.

    Returns:
        An instance of the google.ads.google_ads.v2.types.AdGroupCriterion
            message class of the newly created ad group criterion.
    """
    def formatter(given_string):
        """This helper function is used to assign ' ' to names of resources
        so that this formatted string can be used within an IN clause.

        Args:
            given_string: (str) The string to be formatted.
        """
        results =[]
        for i in given_string:
            results.append(repr(i))
        return ','.join(results)

    resouce_names = formatter(keyword_resource_names)
    ga_service = client.get_service('GoogleAdsService', version='v3')
    query = ('SELECT ad_group.id, ad_group.status, '
    'ad_group_criterion.criterion_id, ad_group_criterion.keyword.text, '
    'ad_group_criterion.keyword.match_type FROM ad_group_criterion '
    'WHERE ad_group_criterion.type = "KEYWORD" '
    'AND ad_group.status = "ENABLED" '
    'AND ad_group_criterion.status IN ("ENABLED", "PAUSED") '
    'AND ad_group_criterion.resource_name IN ({})'.format(resouce_names))

    response = ga_service.search(customer_id, query, PAGE_SIZE)
    response = iter(response)
    keywords = []

    while True:
        try:
            current_row = next(response)
            keywords.append(current_row.ad_group_criterion)
        except StopIteration:
            break

    return keywords


if __name__ == '__main__':
    # Initialize client object.
    # It will read the config file. The default file path is the Home Directory.
    google_ads_client = GoogleAdsClient.load_from_storage()

    parser = argparse.ArgumentParser(
    description='Lists all campaigns for specified customer.')
    # The following argument(s) should be provided to run the example.
    parser.add_argument('-c', '--customer_id', type=str,
                    required=True, help='The Google Ads customer ID.')
    args = parser.parse_args()
    budget = create_campaign_budget(google_ads_client, args.customer_id)
    campaign = create_campaign(google_ads_client, args.customer_id, budget)
    ad_group = create_ad_group(google_ads_client, args.customer_id, campaign)
    create_text_ads(google_ads_client, args.customer_id, ad_group)
    create_keywords(google_ads_client, args.customer_id, ad_group,
              KEYWORDS_TO_ADD)
