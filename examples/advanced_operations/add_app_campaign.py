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
To upload image assets for this campaign, run misc/upload_image_asset.py.
"""


import argparse
from datetime import datetime, timedelta
import sys
from uuid import uuid4

from google.ads.google_ads.client import GoogleAdsClient
from google.ads.google_ads.errors import GoogleAdsException


def main(client, customer_id):
    """Main function for running this example."""
    try:
        # Create the budget for the campaign.
        budget_resource_name = _create_budget(client, customer_id)

        # Create the campaign.
        campaign_resource_name = _create_campaign(client, customer_id,
            budget_resource_name)

        # Set campaign targeting.
        _set_campaign_targeting_criteria(client, customer_id,
            campaign_resource_name)

        # Create Ad Group and App Ad.
        _create_app_ad(client, customer_id, campaign_resource_name)
    except GoogleAdsException as ex:
        print(f'Request with ID "{ex.request_id}" failed with status '
              f'"{ex.error.code().name}" and includes the following errors:')
        for error in ex.failure.errors:
            print(f'\tError with message "{error.message}".')
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print(f'\t\tOn field: {field_path_element.field_name}')
        sys.exit(1)
    return


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
        budget_resource_name: the budget to associate with the campaign

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
    campaign.status = client.get_type(
        'CampaignStatusEnum', version='v2').PAUSED
    # All App campaigns have an advertising_channel_type of
    # MULTI_CHANNEL to reflect the fact that ads from these campaigns are
    # eligible to appear on multiple channels.
    campaign.advertising_channel_type = client.get_type(
        'AdvertisingChannelTypeEnum', version='v2').MULTI_CHANNEL
    campaign.advertising_channel_sub_type = client.get_type(
        'AdvertisingChannelSubTypeEnum', version='v2').APP_CAMPAIGN
    # Set the target CPA to $1 / app install.
    #
    # campaign_bidding_strategy is a 'oneof' message so setting target_cpa
    # is mutually exclusive with other bidding strategies such as
    # manual_cpc, commission, maximize_conversions, etc.
    # See https://developers.google.com/google-ads/api/reference/rpc
    # under current version / resources / Campaign
    campaign.target_cpa.target_cpa_micros.value = 1000000
    # Set the App Campaign Settings.
    campaign.app_campaign_setting.app_id.value = (
        'com.google.android.apps.adwords')
    campaign.app_campaign_setting.app_store = client.get_type(
        'AppCampaignAppStoreEnum', version='v2').GOOGLE_APP_STORE
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
    # selective_optimization1.value = (
    #     'INSERT_CONVERSION_ACTION_RESOURCE_NAME_HERE')
    # campaign.selective_optimization.conversion_actions.extend(
    #     [selective_optimization1])

    # Submit the campaign operation and print the results.
    campaign_response = campaign_service.mutate_campaigns(customer_id,
        [campaign_operation])
    resource_name = campaign_response.results[0].resource_name
    print(f'Created App campaign {resource_name}.')
    return resource_name


def _set_campaign_targeting_criteria(client, customer_id,
        campaign_resource_name):
    """Sets campaign targeting criteria for a given campaign.

    Both location and language targeting are illustrated.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID str.
        campaign_resource_name: the campaign to apply targeting to

    Returns:
        None.
    """
    campaign_criterion_service = client.get_service(
        'CampaignCriterionService', version='v2')
    campaign_criterion_operation = client.get_type(
        'CampaignCriterionOperation', version='v2')
    geo_target_constant_service = client.get_service(
        'GeoTargetConstantService', version='v2')
    language_constant_service = client.get_service(
        'LanguageConstantService', version='v2')
    location_type = client.get_type(
        'CriterionTypeEnum', version='v2').LOCATION
    language_type = client.get_type(
        'CriterionTypeEnum', version='v2').LANGUAGE

    campaign_criterion_operations = []
    # Create the location campaign criteria.
    # Besides using location_id, you can also search by location names from
    # GeoTargetConstantService.suggest_geo_target_constants() and directly
    # apply GeoTargetConstant.resource_name here. An example can be found
    # in targeting/get_geo_target_constant_by_names.py.
    for location_id in ['21137',  # California
                        '2484']:  # Mexico
        campaign_criterion = campaign_criterion_operation.create
        campaign_criterion.campaign.value = campaign_resource_name
        campaign_criterion.type = location_type
        campaign_criterion.location.geo_target_constant.value = (
            geo_target_constant_service.geo_target_constant_path(location_id))
        campaign_criterion_operations.append(campaign_criterion_operation)

    # Create the language campaign criteria.
    for language_id in ['1000',   # English
                        '1003']:  # Spanish
        campaign_criterion = campaign_criterion_operation.create
        campaign_criterion.campaign.value = campaign_resource_name
        campaign_criterion.type = language_type
        campaign_criterion.language.language_constant.value = (
            language_constant_service.language_constant_path(language_id))
        campaign_criterion_operations.append(campaign_criterion_operation)

    # Submit the criteria operations. All four criteria will have the same
    # resource name.
    resource_name = campaign_criterion_service.mutate_campaign_criteria(
        customer_id, campaign_criterion_operations).results[0].resource_name
    print(f'Created Campaign Criteria {resource_name}.')
    return


def _create_app_ad(client, customer_id, campaign_resource_name):
    """Creates an ad group and associated App ad for a given campaign.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID str.
        campaign_resource_name: the campaign to be modified

    Returns:
        None.
    """
    ad_group_service = client.get_service('AdGroupService', version='v2')

    # Create ad group.
    # Note that the ad group type must not be set.
    # Since the advertising_channel_sub_type is APP_CAMPAIGN,
    #   1- you cannot override bid settings at the ad group level.
    #   2- you cannot add ad group criteria.
    ad_group_operation = client.get_type('AdGroupOperation', version='v2')
    ad_group = ad_group_operation.create
    ad_group.name.value = f'Earth to Mars cruises {uuid4()}'
    ad_group.status = client.get_type(
        'AdGroupStatusEnum', version='v2').ENABLED
    ad_group.campaign.value = campaign_resource_name

    ad_group_response = ad_group_service.mutate_ad_groups(
        customer_id, [ad_group_operation])

    ad_group_resource_name = ad_group_response.results[0].resource_name
    print(f'Ad Group created {ad_group_resource_name}.')

    # Create the ad group ad
    ad_group_ad_service = client.get_service('AdGroupAdService', version='v2')
    ad_group_ad_operation = client.get_type('AdGroupAdOperation', version='v2')
    ad_group_ad = ad_group_ad_operation.create
    ad_group_ad.status = client.get_type(
        'AdGroupAdStatusEnum', version='v2').ENABLED
    ad_group_ad.ad_group.value = ad_group_resource_name
    # ad_data is a 'oneof' message so setting app_ad
    # is mutually exclusive with ad data fields such as
    # text_ad, gmail_ad, etc.
    ad_group_ad.ad.app_ad.headlines.extend([
        _create_ad_text_asset(client, 'A cool puzzle game'),
        _create_ad_text_asset(client, 'Remove connected blocks')])
    ad_group_ad.ad.app_ad.descriptions.extend([
        _create_ad_text_asset(client, '3 difficulty levels'),
        _create_ad_text_asset(client, '4 colorful fun skins')])
    # Optional: You can set up to 20 image assets for your campaign.
    # ad_group_ad.ad.app_ad.images.extend(
    #     [INSERT_AD_IMAGE_RESOURCE_NAME(s)_HERE])

    ad_group_ad_response = ad_group_ad_service.mutate_ad_group_ads(
        customer_id, [ad_group_ad_operation])
    ad_group_ad_resource_name = ad_group_ad_response.results[0].resource_name
    print(f'Ad Group App Ad created {ad_group_ad_resource_name}.')
    return


def _create_ad_text_asset(client, text):
    ad_text_asset = client.get_type('AdTextAsset', version='v2')
    ad_text_asset.text.value = text
    return ad_text_asset


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
