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
"""This code example adds a Dynamic Search Ads Campaign.

To get campaigns, run basic_operations/get_campaigns.py
"""

from __future__ import absolute_import

import argparse
import six
import sys
import uuid
from datetime import datetime, timedelta

from google.ads.google_ads.client import GoogleAdsClient
from google.ads.google_ads.errors import GoogleAdsException


def main(client, customer_id):
    try:
        budget_resource_name = create_budget(client, customer_id)
        campaign_resource_name = create_campaign(client, customer_id,
                                                 budget_resource_name)
        ad_group_resource_name = create_ad_group(client, customer_id,
                                                 campaign_resource_name)
        create_exapanded_dsa(client, customer_id, ad_group_resource_name)
        add_webpage_criteria(client, customer_id, ad_group_resource_name)
    except GoogleAdsException as ex:
        print('Request with ID "{}" failed with status "{}" and includes the '
              'following errors:'.format(ex.request_id, ex.error.code().name))
        for error in ex.failure.errors:
            print('\tError with message "{}".'.format(error.message))
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print('\t\tOn field: {}'.format(
                        field_path_element.field_name))
        sys.exit(1)


def create_budget(client, customer_id):
    """Creates a budget under the given customer ID.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID str.

    Returns:
        A resource_name str for the newly created Budget.
    """
    campaign_budget_operation = client.get_type(
        'CampaignBudgetOperation', version='v1')
    campaign_budget = campaign_budget_operation.create
    campaign_budget.name.value = 'Interplanetary Cruise #{}'.format(
        uuid.uuid4())
    campaign_budget.amount_micros.value = 50000000
    campaign_budget.delivery_method = client.get_type(
        'BudgetDeliveryMethodEnum', version='v1').STANDARD

    campaign_budget_service = client.get_service(
        'CampaignBudgetService', version='v1')
    response = campaign_budget_service.mutate_campaign_budgets(
        customer_id, [campaign_budget_operation])
    resource_name = response.results[0].resource_name

    print('Created campaign budget with resource_name: {}'.format(
        resource_name))

    return resource_name


def create_campaign(client, customer_id, budget_resource_name):
    """Creates a Dynamic Search Ad Campaign under the given customer ID.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID str.
        budget_resource_name: a resource_name str for a Budget

    Returns:
        A resource_name str for the newly created Campaign.
    """
    campaign_operation = client.get_type('CampaignOperation', version='v1')
    campaign = campaign_operation.create
    campaign.name.value = 'Interplanetary Cruise #{}'.format(uuid.uuid4())
    campaign.advertising_channel_type = client.get_type(
        'AdvertisingChannelTypeEnum', version='v1').SEARCH
    campaign.status = client.get_type('CampaignStatusEnum',
                                      version='v1').PAUSED
    campaign.manual_cpc.enhanced_cpc_enabled.value = True
    campaign.campaign_budget.value = budget_resource_name
    campaign.dynamic_search_ads_setting.domain_name.value = 'example.com'
    campaign.dynamic_search_ads_setting.language_code.value = 'en'
    campaign.start_date.value = datetime.now().strftime('%Y%m%d')
    campaign.end_date.value = (
        datetime.now() + timedelta(days=365)).strftime('%Y%m%d')

    campaign_service = client.get_service('CampaignService', version='v1')
    response = campaign_service.mutate_campaigns(
        customer_id, [campaign_operation])
    resource_name = response.results[0].resource_name
    print('Created campaign with resource_name: {}'.format(resource_name))

    return resource_name


def create_ad_group(client, customer_id, campaign_resource_name):
    """Creates a Dynamic Search Ad Group under the given Campaign.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID str.
        campaign_resource_name: a resource_name str for a Campaign.

    Returns:
        A resource_name str for the newly created Ad Group.
    """
    ad_group_operation = client.get_type('AdGroupOperation', version='v1')
    ad_group = ad_group_operation.create
    ad_group.type = client.get_type('AdGroupTypeEnum',
                                    version='v1').SEARCH_DYNAMIC_ADS
    ad_group.name.value = 'Earth to Mars Cruises {}'.format(uuid.uuid4())
    ad_group.campaign.value = campaign_resource_name
    ad_group.status = client.get_type('AdGroupStatusEnum', version='v1').PAUSED
    ad_group.tracking_url_template.value = (
        'http://tracker.example.com/traveltracker/{escapedlpurl}')

    ad_group_service = client.get_service('AdGroupService', version='v1')
    response = ad_group_service.mutate_ad_groups(customer_id,
                                                 [ad_group_operation])
    resource_name = response.results[0].resource_name
    print('Created Ad Group with resource_name: {}'.format(resource_name))

    return resource_name


def create_exapanded_dsa(client, customer_id, ad_group_resource_name):
    """Creates a Dynamic Search Ad under the given Ad Group.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID str.
        campaign_resource_name: a resource_name str for an Ad Group.
    """
    ad_group_ad_operation = client.get_type('AdGroupAdOperation', version='v1')
    ad_group_ad = ad_group_ad_operation.create
    ad_group_ad.status = client.get_type('AdGroupAdStatusEnum',
                                         version='v1').PAUSED
    ad_group_ad.ad.expanded_dynamic_search_ad.description.value = (
        'Buy tickets now!')
    ad_group_ad.ad_group.value = ad_group_resource_name

    ad_group_ad_service = client.get_service('AdGroupAdService', version='v1')
    response = ad_group_ad_service.mutate_ad_group_ads(customer_id,
                                                    [ad_group_ad_operation])
    resource_name = response.results[0].resource_name
    print('Created Ad Group Ad with resource_name: {}'.format(resource_name))


def add_webpage_criteria(client, customer_id, ad_group_resource_name):
    """Creates a Web Page Criteria to the given Ad Group.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID str.
        campaign_resource_name: a resource_name str for an Ad Group.
    """
    ad_group_criterion_operation = client.get_type(
        'AdGroupCriterionOperation', version='v1')
    criterion = ad_group_criterion_operation.create
    criterion.ad_group.value = ad_group_resource_name
    criterion.cpc_bid_micros.value = 10000000
    criterion.status = client.get_type(
        'AdGroupCriterionStatusEnum', version='v1').PAUSED
    criterion.webpage.criterion_name.value = 'Special Offers'

    webpage_info_url = criterion.webpage.conditions.add()
    webpage_info_url.operand = client.get_type(
        'WebpageConditionOperandEnum', version='v1').URL
    webpage_info_url.argument.value = '/specialoffers'

    webpage_info_page_title = criterion.webpage.conditions.add()
    webpage_info_page_title.operand = client.get_type(
        'WebpageConditionOperandEnum', version='v1').PAGE_TITLE
    webpage_info_page_title.argument.value = 'Special Offer'

    ad_group_criterion_service = client.get_service('AdGroupCriterionService',
                                                 version='v1')
    response = ad_group_criterion_service.mutate_ad_group_criteria(
        customer_id, [ad_group_criterion_operation])
    resource_name = response.results[0].resource_name
    print('Created Ad Group Criterion with resource_name: {}'.format(
        resource_name))


if __name__ == '__main__':
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    google_ads_client = GoogleAdsClient.load_from_storage()

    parser = argparse.ArgumentParser(
        description=('Adds a Dynamic Search Ad campaign under the specified '
                     'customer ID.'))
    # The following argument(s) should be provided to run the example.
    parser.add_argument('-c', '--customer_id', type=six.text_type,
                        required=True, help='The Google Ads customer ID.')
    args = parser.parse_args()

    main(google_ads_client, args.customer_id)
