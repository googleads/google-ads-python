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


import argparse
import sys
from uuid import uuid4
from datetime import datetime, timedelta

from google.ads.google_ads.client import GoogleAdsClient
from google.ads.google_ads.errors import GoogleAdsException


def main(client, customer_id):
    """The main method that creates all necessary entities for the example.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID str.
    """
    try:
        budget_resource_name = create_budget(client, customer_id)
        campaign_resource_name = create_campaign(client, customer_id,
                                                 budget_resource_name)
        ad_group_resource_name = create_ad_group(client, customer_id,
                                                 campaign_resource_name)
        create_expanded_dsa(client, customer_id, ad_group_resource_name)
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
    # Retrieve a new campaign budget operation object.
    campaign_budget_operation = client.get_type('CampaignBudgetOperation',
                                                version='v3')
    # Create a campaign budget.
    campaign_budget = campaign_budget_operation.create
    campaign_budget.name.value = 'Interplanetary Cruise #{}'.format(uuid4())
    campaign_budget.amount_micros.value = 50000000
    campaign_budget.delivery_method = client.get_type(
        'BudgetDeliveryMethodEnum', version='v3').STANDARD

    # Retrieve the campaign budget service.
    campaign_budget_service = client.get_service('CampaignBudgetService',
                                                 version='v3')
    # Submit the campaign budget operation to add the campaign budget.
    response = campaign_budget_service.mutate_campaign_budgets(
        customer_id, [campaign_budget_operation])
    resource_name = response.results[0].resource_name

    # Display the results
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
    # Retrieve a new campaign operation object.
    campaign_operation = client.get_type('CampaignOperation', version='v3')
    # Create a campaign.
    campaign = campaign_operation.create
    campaign.name.value = 'Interplanetary Cruise #{}'.format(uuid4())
    campaign.advertising_channel_type = client.get_type(
        'AdvertisingChannelTypeEnum', version='v3').SEARCH
    # Recommendation: Set the campaign to PAUSED when creating it to prevent the
    # ads from immediately serving. Set to ENABLED once you've added targeting
    # and the ads are ready to serve.
    campaign.status = client.get_type('CampaignStatusEnum',
                                      version='v3').PAUSED
    campaign.manual_cpc.enhanced_cpc_enabled.value = True
    campaign.campaign_budget.value = budget_resource_name
    # Required: set the campaign's Dynamic Search Ads domain name and language.
    campaign.dynamic_search_ads_setting.domain_name.value = 'example.com'
    campaign.dynamic_search_ads_setting.language_code.value = 'en'
    # Optional: set the start date.
    campaign.start_date.value = datetime.now().strftime('%Y%m%d')
    # Optional: set the end date.
    campaign.end_date.value = (
        datetime.now() + timedelta(days=365)).strftime('%Y%m%d')

    # Retrieve the campaign service.
    campaign_service = client.get_service('CampaignService', version='v3')
    # Submit the campaign operation to add the campaign.
    response = campaign_service.mutate_campaigns(
        customer_id, [campaign_operation])
    resource_name = response.results[0].resource_name

    # Display the results
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
    # Retrieve a new ad group operation object.
    ad_group_operation = client.get_type('AdGroupOperation', version='v3')
    # Create an ad group.
    ad_group = ad_group_operation.create
    # Required: set the ad group's type to Dynamic Search Ads.
    ad_group.type = client.get_type('AdGroupTypeEnum',
                                    version='v3').SEARCH_DYNAMIC_ADS
    ad_group.name.value = 'Earth to Mars Cruises {}'.format(uuid4())
    ad_group.campaign.value = campaign_resource_name
    ad_group.status = client.get_type('AdGroupStatusEnum', version='v3').PAUSED
    # Recommended: set a tracking URL template for your ad group if you want to
    # use URL tracking software.
    ad_group.tracking_url_template.value = (
        'http://tracker.example.com/traveltracker/{escapedlpurl}')
    # Set the ad group bids.
    ad_group.cpc_bid_micros.value = 3000000

    # Retrieve the ad group service.
    ad_group_service = client.get_service('AdGroupService', version='v3')
    # Submit the ad group ad operation to add an ad group.
    response = ad_group_service.mutate_ad_groups(customer_id,
                                                 [ad_group_operation])
    resource_name = response.results[0].resource_name

    # Display the results.
    print('Created Ad Group with resource_name: {}'.format(resource_name))

    return resource_name


def create_expanded_dsa(client, customer_id, ad_group_resource_name):
    """Creates a Dynamic Search Ad under the given Ad Group.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID str.
        campaign_resource_name: a resource_name str for an Ad Group.
    """
    # Retrieve a new ad group ad operation object.
    ad_group_ad_operation = client.get_type('AdGroupAdOperation', version='v3')
    # Create and Expanded Dynamic Search Ad. This ad will have its headline,
    # display URL and final URL auto-generated at serving time according to
    # domain name specific information provided by DynamicSearchAdSetting at
    # the campaign level.
    ad_group_ad = ad_group_ad_operation.create
    # Optional: set the ad status.
    ad_group_ad.status = client.get_type('AdGroupAdStatusEnum',
                                         version='v3').PAUSED
    # Set the ad description.
    ad_group_ad.ad.expanded_dynamic_search_ad.description.value = (
        'Buy tickets now!')
    ad_group_ad.ad_group.value = ad_group_resource_name

    # Retrieve the ad group ad service.
    ad_group_ad_service = client.get_service('AdGroupAdService', version='v3')
    # Submit the ad group ad operation to add the ad group ad.
    response = ad_group_ad_service.mutate_ad_group_ads(customer_id,
                                                    [ad_group_ad_operation])
    resource_name = response.results[0].resource_name

    # Display the results.
    print('Created Ad Group Ad with resource_name: {}'.format(resource_name))


def add_webpage_criteria(client, customer_id, ad_group_resource_name):
    """Creates a Web Page Criteria to the given Ad Group.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID str.
        campaign_resource_name: a resource_name str for an Ad Group.
    """
    # Retrieve a new ad group criterion operation.
    ad_group_criterion_operation = client.get_type(
        'AdGroupCriterionOperation', version='v3')
    # Create an ad group criterion for special offers for Mars Cruise.
    criterion = ad_group_criterion_operation.create
    criterion.ad_group.value = ad_group_resource_name
    # Optional: set custom bid amount.
    criterion.cpc_bid_micros.value = 10000000
    # Optional: set the status.
    criterion.status = client.get_type(
        'AdGroupCriterionStatusEnum', version='v3').PAUSED
    criterion.webpage.criterion_name.value = 'Special Offers'

    webpage_info_url = criterion.webpage.conditions.add()
    webpage_info_url.operand = client.get_type(
        'WebpageConditionOperandEnum', version='v3').URL
    webpage_info_url.argument.value = '/specialoffers'

    webpage_info_page_title = criterion.webpage.conditions.add()
    webpage_info_page_title.operand = client.get_type(
        'WebpageConditionOperandEnum', version='v3').PAGE_TITLE
    webpage_info_page_title.argument.value = 'Special Offer'

    # Retrieve the ad group criterion service.
    ad_group_criterion_service = client.get_service('AdGroupCriterionService',
                                                    version='v3')
    # Submit the ad group criterion operation to add the ad group criterion.
    response = ad_group_criterion_service.mutate_ad_group_criteria(
        customer_id, [ad_group_criterion_operation])
    resource_name = response.results[0].resource_name

    # Display the results.
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
    parser.add_argument('-c', '--customer_id', type=str,
                        required=True, help='The Google Ads customer ID.')
    args = parser.parse_args()

    main(google_ads_client, args.customer_id)
