# Copyright 2018 Google LLC
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
"""This example constructs a campaign with a Portfolio Bidding Strategy."""

from __future__ import absolute_import

import argparse
import six
import sys
import uuid

import google.ads.google_ads.client


def main(client, customer_id):
    campaign_budget_service = client.get_service('CampaignBudgetService')
    bidding_strategy_service = client.get_service('BiddingStrategyService')
    campaign_service = client.get_service('CampaignService')

    # Create a budget, which can be shared by multiple campaigns.
    campaign_budget_operation = client.get_type('CampaignBudgetOperation')
    campaign_budget = campaign_budget_operation.create
    campaign_budget.name.value = 'Interplanetary Budget %s' % uuid.uuid4()
    campaign_budget.delivery_method = client.get_type(
        'BudgetDeliveryMethodEnum').STANDARD
    campaign_budget.amount_micros.value = 500000
    campaign_budget.explicitly_shared.value = True

    # Add budget.
    try:
        campaign_budget_response = (
          campaign_budget_service.mutate_campaign_budgets(
              customer_id, [campaign_budget_operation]))
    except google.ads.google_ads.errors.GoogleAdsException as ex:
        print('Request with ID "%s" failed with status "%s" and includes the '
              'following errors:' % (ex.request_id, ex.error.code().name))
        for error in ex.failure.errors:
            print('\tError with message "%s".' % error.message)
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print('\t\tOn field: %s' % field_path_element.field_name)
        sys.exit(1)

    campaign_budget_id = campaign_budget_response.results[0].resource_name

    print('Budget "%s" was created.' % campaign_budget_id)

    # Create a portfolio bidding strategy.
    bidding_strategy_operation = client.get_type('BiddingStrategyOperation')
    bidding_strategy = bidding_strategy_operation.create
    bidding_strategy.name.value = 'Enhanced CPC %s' % uuid.uuid4()
    target_spend = bidding_strategy.target_spend
    target_spend.cpc_bid_ceiling_micros.value = 2000000
    target_spend.target_spend_micros.value = 20000000

    # Add portfolio bidding strategy.
    try:
        bidding_strategy_response = (
            bidding_strategy_service.mutate_bidding_strategies(
                customer_id, [bidding_strategy_operation]))
    except google.ads.google_ads.errors.GoogleAdsException as ex:
        print('Request with ID "%s" failed with status "%s" and includes the '
              'following errors:' % (ex.request_id, ex.error.code().name))
        for error in ex.failure.errors:
            print('\tError with message "%s".' % error.message)
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print('\t\tOn field: %s' % field_path_element.field_name)
        sys.exit(1)

    bidding_strategy_id = bidding_strategy_response.results[0].resource_name

    print('Portfolio bidding strategy "%s" was created.' % bidding_strategy_id)

    # Create campaign.
    campaign_operation = client.get_type('CampaignOperation')
    campaign = campaign_operation.create
    campaign.name.value = 'Interplanetary Cruise %s' % uuid.uuid4()
    campaign.advertising_channel_type = client.get_type(
        'AdvertisingChannelTypeEnum').SEARCH

    # Recommendation: Set the campaign to PAUSED when creating it to prevent the
    # ads from immediately serving. Set to ENABLED once you've added targeting
    # and the ads are ready to serve.
    campaign.status = client.get_type('CampaignStatusEnum').PAUSED

    # Set the bidding strategy and budget.
    campaign.bidding_strategy.value = bidding_strategy_id
    campaign.manual_cpc.enhanced_cpc_enabled.value = True
    campaign.campaign_budget.value = campaign_budget_id

    # Set the campaign network options.
    campaign.network_settings.target_google_search.value = True
    campaign.network_settings.target_search_network.value = True
    campaign.network_settings.target_content_network.value = False
    campaign.network_settings.target_partner_search_network.value = False

    # Add the campaign.
    try:
        campaign_response = campaign_service.mutate_campaigns(
            customer_id, [campaign_operation])
    except google.ads.google_ads.errors.GoogleAdsException as ex:
        print('Request with ID "%s" failed with status "%s" and includes the '
              'following errors:' % (ex.request_id, ex.error.code().name))
        for error in ex.failure.errors:
            print('\tError with message "%s".' % error.message)
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print('\t\tOn field: %s' % field_path_element.field_name)
        sys.exit(1)

    print('Created campaign %s.' % campaign_response.results[0].resource_name)


if __name__ == '__main__':
    # GoogleAdsClient will read a google-ads.yaml configuration file in the
    # home directory if none is specified.
    google_ads_client = (google.ads.google_ads.client.GoogleAdsClient
                         .load_from_storage())

    parser = argparse.ArgumentParser(
        description='Adds a campaign for specified customer.')
    # The following argument(s) should be provided to run the example.
    parser.add_argument('-c', '--customer_id', type=six.text_type,
                        required=True, help='The AdWords customer ID.')
    args = parser.parse_args()

    main(google_ads_client, args.customer_id)
