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
"""This example updates a campaign.

To get campaigns, run get_campaigns.py.
"""

from __future__ import absolute_import

import argparse
import six
import sys

import google.ads.google_ads.errors
import google.ads.google_ads.client
from google.api_core import protobuf_helpers


def main(client, customer_id, campaign_id):
    campaign_service = client.get_service('CampaignService')
    # Create campaign operation.
    campaign_operation = client.get_type('CampaignOperation')
    campaign = campaign_operation.update
    campaign.resource_name = campaign_service.campaign_path(
        customer_id, campaign_id)
    campaign.status = client.get_type('CampaignStatusEnum').PAUSED
    campaign.network_settings.target_search_network.value = False
    # Retrieve a FieldMask for the fields configured in the campaign.
    fm = protobuf_helpers.field_mask(None, campaign)
    campaign_operation.update_mask.CopyFrom(fm)

    # Update the campaign.
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

    print('Updated campaign %s.' % campaign_response.results[0].resource_name)


if __name__ == '__main__':
    # GoogleAdsClient will read a google-ads.yaml configuration file in the
    # home directory if none is specified.
    google_ads_client = (google.ads.google_ads.client.GoogleAdsClient
                         .load_from_storage())

    parser = argparse.ArgumentParser(
        description='Updates the given campaign for the specified customer.')
    # The following argument(s) should be provided to run the example.
    parser.add_argument('-c', '--customer_id', type=six.text_type,
                        required=True, help='The AdWords customer ID.')
    parser.add_argument('-i', '--campaign_id', type=six.text_type,
                        required=True, help='The campaign ID.')
    args = parser.parse_args()

    main(google_ads_client, args.customer_id, args.campaign_id)
