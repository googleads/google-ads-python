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
"""Demonstrates how to add a campaign-level bid modifier for call interactions.
"""

from __future__ import absolute_import

import argparse
import six
import sys

import google.ads.google_ads.client


def main(client, customer_id, campaign_id, bid_modifier_value):
    campaign_service = client.get_service('CampaignService')
    campaign_bm_service = client.get_service('CampaignBidModifierService')

    # Create campaign bid modifier for call interactions with the specified
    # campaign ID and bid modifier value.
    campaign_bid_modifier_operation = client.get_type(
        'CampaignBidModifierOperation')
    campaign_bid_modifier = campaign_bid_modifier_operation.create

    # Set the campaign.
    campaign_bid_modifier.campaign.value = campaign_service.campaign_path(
        customer_id, campaign_id)

    # Set the bid modifier.
    campaign_bid_modifier.bid_modifier.value = bid_modifier_value

    # Sets the interaction type.
    campaign_bid_modifier.interaction_type.type = (
        client.get_type('InteractionTypeEnum').CALLS)

    # Add the campaign bid modifier.
    try:
        campaign_bm_response = (
            campaign_bm_service.mutate_campaign_bid_modifiers(
                customer_id, [campaign_bid_modifier_operation]))
    except google.ads.google_ads.errors.GoogleAdsException as ex:
        print('Request with ID "%s" failed with status "%s" and includes the '
              'following errors:' % (ex.request_id, ex.error.code().name))
        for error in ex.failure.errors:
            print('\tError with message "%s".' % error.message)
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print('\t\tOn field: %s' % field_path_element.field_name)
        sys.exit(1)

    print('Created campaign bid modifier: %s.'
          % campaign_bm_response.results[0].resource_name)


if __name__ == '__main__':
    # GoogleAdsClient will read a google-ads.yaml configuration file in the
    # home directory if none is specified.
    google_ads_client = (google.ads.google_ads.client.GoogleAdsClient
                         .load_from_storage())

    parser = argparse.ArgumentParser(
        description=('Adds a bid modifier to the specified campaign ID, for '
                     'the given customer ID.'))
    # The following argument(s) should be provided to run the example.
    parser.add_argument('-c', '--customer_id', type=six.text_type,
                        required=True, help='The AdWords customer ID.')
    parser.add_argument('-i', '--campaign_id', type=six.text_type,
                        required=True, help='The campaign ID.')
    parser.add_argument('-b', '--bid_modifier_value', type=float,
                        required=False, default=1.5,
                        help='The bid modifier value.')
    args = parser.parse_args()

    main(google_ads_client, args.customer_id, args.campaign_id,
         args.bid_modifier_value)
