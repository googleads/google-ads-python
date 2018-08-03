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
"""This example illustrates how to add a campaign.

To get campaigns, run get_campaigns.py.
"""

from __future__ import absolute_import

import argparse
import datetime
import six
import sys
import uuid

import google.ads.google_ads.client


_DATE_FORMAT = '%Y%m%d'


def main(client, customer_id):
    campaign_budget_service = client.get_service('CampaignBudgetService')
    campaign_service = client.get_service('CampaignService')

    # Create a budget, which can be shared by multiple campaigns.
    campaign_budget_operation = client.get_type('CampaignBudgetOperation')
    campaign_budget = campaign_budget_operation.create
    campaign_budget.name.value = 'Interplanetary Budget %s' % uuid.uuid4()
    campaign_budget.delivery_method = client.get_type(
        'BudgetDeliveryMethodEnum').STANDARD
    campaign_budget.amount_micros.value = 500000

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
    campaign.manual_cpc.enhanced_cpc_enabled.value = True
    campaign.campaign_budget.value = (
        campaign_budget_response.results[0].resource_name)

    # Set the campaign network options.
    campaign.network_settings.target_google_search.value = True
    campaign.network_settings.target_search_network.value = True
    campaign.network_settings.target_content_network.value = False
    campaign.network_settings.target_partner_search_network.value = False

    # Optional: Set the start date.
    start_time = datetime.date.today() + datetime.timedelta(days=1)
    campaign.start_date.value = datetime.date.strftime(start_time, _DATE_FORMAT)

    # Optional: Set the end date.
    end_time = start_time + datetime.timedelta(weeks=4)
    campaign.end_date.value = datetime.date.strftime(end_time, _DATE_FORMAT)

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
