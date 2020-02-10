#!/usr/bin/env python
# Copyright 2020 Google LLC
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
"""This example adds an App campaign.

For guidance regarding App Campaigns, see:
https://developers.google.com/google-ads/api/docs/app-campaigns/overview

To get campaigns, run basic_operations/get_campaigns.py.
To upload image assets for this campaign, run misc/upload_image.py.
"""


import argparse
import sys
from uuid import uuid4
from datetime import datetime, timedelta

from google.ads.google_ads.client import GoogleAdsClient
from google.ads.google_ads.errors import GoogleAdsException


def main(client, customer_id):

    try:
        # Create the budget for the campaign.
        budget_resource_name = _create_budget(client, customer_id)

        # Create the campaign.
        campaign_resource_name = _create_campaign(client, customer_id,
            budget_resource_name)

        # Set campaign targeting
        _set_campaign_targeting_criteria(client, customer_id,
            campaign_resource_name)
        
        # TODO: set campaign targeting criteria
        # Set the campaign's assets and ad text ideas. These values will
        # be used to generate ads.


        # TODO: set AppAdInfo

        return
        ad_group_resource_name = create_ad_group(client, customer_id,
            campaign_resource_name)
        create_expanded_dsa(client, customer_id, ad_group_resource_name)
        add_webpage_criteria(client, customer_id, ad_group_resource_name)
    except GoogleAdsException as ex:
        print(f'Request with ID "{ex.request_id}" failed with status '
              f'"{ex.error.code().name}" and includes the following errors:')
        for error in ex.failure.errors:
            print(f'\tError with message "{error.message}".')
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print(f'\t\tOn field: {field_path_element.field_name}')
        sys.exit(1)


def _create_budget(client, customer_id):
    """Creates a budget under the given customer ID.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID str.

    Returns:
        A resource_name str for the newly created Budget.
    """
    # Retrieve a new campaign budget operation object.
    campaign_budget_operation = client.get_type('CampaignBudgetOperation',
                                                version='v2')
    # Create a campaign budget.
    campaign_budget = campaign_budget_operation.create
    campaign_budget.name.value = f'Interplanetary Cruise #{uuid4()}'
    campaign_budget.amount_micros.value = 50000000
    campaign_budget.delivery_method = client.get_type(
        'BudgetDeliveryMethodEnum', version='v2').STANDARD
    # An App campaign cannot use a shared campaign budget.
    # explicitly_shared must be set to false.
    campaign_budget.explicitly_shared.value = False

    # Retrieve the campaign budget service.
    campaign_budget_service = client.get_service('CampaignBudgetService',
                                                 version='v2')
    # Submit the campaign budget operation to add the campaign budget.
    response = campaign_budget_service.mutate_campaign_budgets(
        customer_id, [campaign_budget_operation])
    resource_name = response.results[0].resource_name
    print(f'Created campaign budget with resource_name: {resource_name}')
    return resource_name

def _create_campaign(client, customer_id, budget_resource_name):
    """Creates an app campaign under the given customer ID.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID str.
        buddget_resource_name: the budget to associate with the campaign

    Returns:
        A resource_name str for the newly created app campaign.
    """
    campaign_service = client.get_service('CampaignService', version='v2')
    campaign_operation = client.get_type('CampaignOperation', version='v2')
    campaign = campaign_operation.create
    campaign.name.value = f'Interplanetary Cruise App #{uuid4()}'
    campaign.campaign_budget.value = budget_resource_name
    # Recommendation: Set the campaign to PAUSED when creating it to 
    # prevent the ads from immediately serving. Set to ENABLED once you've
    # added targeting and the ads are ready to serve.
    campaign.status = (client.get_type('CampaignStatusEnum', version='v2')
        .PAUSED)
    # All App campaigns have an advertising_channel_type of
    # MULTI_CHANNEL to reflect the fact that ads from these campaigns are
    # eligible to appear on multiple channels.
    campaign.advertising_channel_type = client.get_type(
        'AdvertisingChannelTypeEnum', version='v2').MULTI_CHANNEL
    campaign.advertising_channel_sub_type = client.get_type(
        'AdvertisingChannelSubTypeEnum', version='v2').APP_CAMPAIGN
    # Define the bidding strategy during campaign creation. An App campaign
    # cannot use a portfolio bidding strategy.
    # App campaigns only support the TARGET_CPA bidding strategy.
    campaign.bidding_strategy_type = (client
        .get_type('BiddingStrategyTypeEnum', version='v2').TARGET_CPA)
    # Set the target CPA to $1 / app install.
    #
    # campaign_bidding_strategy is a 'oneof' message so setting target_cpa
    # is mutually exclusive with other bidding strategies such as
    # manual_cpc, commission, maximize_conversions, etc.
    # See https://developers.google.com/google-ads/api/reference/rpc
    # under current version / resources / Campaign
    campaign.target_cpa.target_cpa_micros.value  = 1000000
    # Set the App Campaign Settings. Other settings are on a per-ad basis.
    campaign.app_campaign_setting.app_id.value = 'com.labpixies.colordrips'
    campaign.app_campaign_setting.app_store = (client.get_type(
        'AppCampaignAppStoreEnum', version='v2').GOOGLE_APP_STORE)
    # Optional fields
    campaign.start_date.value = (datetime.now() +
        timedelta(1)).strftime('%Y%m%d')
    campaign.end_date.value = (datetime.now() +
        timedelta(365)).strftime('%Y%m%d')
    # Optimize this campaign for getting new users for your app.
    campaign.app_campaign_setting.bidding_strategy_goal_type = (client
        .get_type('AppCampaignBiddingStrategyGoalTypeEnum',
                  version='v2').OPTIMIZE_INSTALLS_TARGET_INSTALL_COST)
    # Optional: If you select the 
    # OPTIMIZE_IN_APP_CONVERSIONS_TARGET_INSTALL_COST goal type, then also
    # specify your in-app conversion types so the Google Ads API can focus 
    # your campaign on people who are most likely to complete the 
    # corresponding in-app actions.
    # selective_optimization1 = (client.get_type('StringValue',
    #                            version='v2'))
    # selective_optimization1.value = 'INSERT_CONVERSION_TYPE_ID_HERE'
    # campaign.selective_optimization.conversion_actions.extend(
    #     [selective_optimization1])

    # TODO: set advanced location options

    # Submit the campaign operation and print the results.
    campaign_response = campaign_service.mutate_campaigns(customer_id,
        [campaign_operation])
    resource_name = campaign_response.results[0].resource_name
    print(f'Created App campaign {resource_name}.')
    return resource_name


def _set_campaign_targeting_criteria(client, customer_id,
        campaign_resource_name):
    campaign_criterion_service = client.get_service('CampaignCriterionService',
                                                    version='v2')
    campaign_criterion_operation = (client.get_type(
        'CampaignCriterionOperation', version='v2'))
    geo_target_constant_service = (client.get_service(
        'GeoTargetConstantService', version='v2'))
    language_constant_service = (client.get_service('LanguageConstantService',
        version='v2'))
    location_type = (client.get_type('CriterionTypeEnum',version='v2')
        .LOCATION)
    language_type = (client.get_type('CriterionTypeEnum',version='v2')
        .LANGUAGE)

    campaign_criterion_operations = []
    # Create the location campaign criteria.
    # Besides using location_id, you can also search by location names from
    # GeoTargetConstantService.suggest_geo_target_constants() and directly
    # apply GeoTargetConstant.resource_name here. An example can be found
    # in get_geo_target_constant_by_names.py.
    for location_id in ['21137', # California
                        '2484']: # Mexico
        campaign_criterion = campaign_criterion_operation.create
        campaign_criterion.campaign.value = campaign_resource_name
        campaign_criterion.type = location_type
        campaign_criterion.location.geo_target_constant.value = (
            geo_target_constant_service.geo_target_constant_path(location_id))
        campaign_criterion_operations.append(campaign_criterion_operation)

    # Create the language campaign criteria.
    for language_id in ['1000', # English
                        '1003']: # Spanish
        campaign_criterion = campaign_criterion_operation.create
        campaign_criterion.campaign.value = campaign_resource_name
        campaign_criterion.type = language_type
        campaign_criterion.language.language_constant.value = (
            language_constant_service.language_constant_path(language_id))
        campaign_criterion_operations.append(campaign_criterion_operation)

    # Submit the criteria operations
    campaign_criterion_response = (
            campaign_criterion_service.mutate_campaign_criteria(
                customer_id, campaign_criterion_operations))
    return
    """Creates a Web Page Criteria to the given Ad Group.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID str.
        campaign_resource_name: a resource_name str for an Ad Group.
    """
    # Retrieve a new ad group criterion operation.
    ad_group_criterion_operation = client.get_type(
        'AdGroupCriterionOperation', version='v2')
    # Create an ad group criterion for special offers for Mars Cruise.
    criterion = ad_group_criterion_operation.create
    criterion.ad_group.value = ad_group_resource_name
    # Optional: set custom bid amount.
    criterion.cpc_bid_micros.value = 10000000
    # Optional: set the status.
    criterion.status = client.get_type(
        'AdGroupCriterionStatusEnum', version='v2').PAUSED
    criterion.webpage.criterion_name.value = 'Special Offers'

    webpage_info_url = criterion.webpage.conditions.add()
    webpage_info_url.operand = client.get_type(
        'WebpageConditionOperandEnum', version='v2').URL
    webpage_info_url.argument.value = '/specialoffers'

    webpage_info_page_title = criterion.webpage.conditions.add()
    webpage_info_page_title.operand = client.get_type(
        'WebpageConditionOperandEnum', version='v2').PAGE_TITLE
    webpage_info_page_title.argument.value = 'Special Offer'

    # Retrieve the ad group criterion service.
    ad_group_criterion_service = client.get_service('AdGroupCriterionService',
                                                    version='v2')
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
        description=('Adds a App Ad campaign under the specified '
                     'customer ID.'))
    # The following argument(s) should be provided to run the example.
    parser.add_argument('-c', '--customer_id', type=str,
                        required=True, help='The Google Ads customer ID.')
    args = parser.parse_args()

    main(google_ads_client, args.customer_id)
