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
"""This example adds a campaign group, and then adds campaigns to the group.

To get campaigns, run get_campaigns.py.
"""

from __future__ import absolute_import

import argparse
import six
import sys
import uuid

import google.ads.google_ads.client
from google.api_core import protobuf_helpers


def add_campaigns_to_group(client, customer_id, campaign_group_resource_name,
                           campaign_ids):
    campaign_service = client.get_service('CampaignService')

    campaign_operations = []

    for campaign_id in campaign_ids:
        # Create the campaign operation.
        campaign_operation = client.get_type('CampaignOperation')

        # Create a campaign, and set its resource name and campaign group.
        campaign = campaign_operation.update
        campaign.resource_name = campaign_service.campaign_path(
            customer_id, campaign_id)
        campaign.campaign_group.value = campaign_group_resource_name

        # Retrieve a FieldMask for the fields configured in the campaign.
        fm = protobuf_helpers.field_mask(None, campaign)
        campaign_operation.update_mask.CopyFrom(fm)

        campaign_operations.append(campaign_operation)

    try:
        # Associate the campaigns with the campaign group.
        response = campaign_service.mutate_campaigns(
            customer_id, campaign_operations)
    except google.ads.google_ads.errors.GoogleAdsException as ex:
        print('Request with ID "%s" failed with status "%s" and includes the '
              'following errors:' % (ex.request_id, ex.error.code().name))
        for error in ex.failure.errors:
            print('\tError with message "%s".' % error.message)
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print('\t\tOn field: %s' % field_path_element.field_name)
        sys.exit(1)

    print('Added %d campaigns to campaign group with resource name "%s":'
          % (len(response.results), campaign_group_resource_name))

    for updated_campaign in response.results:
        print('\t%s' % updated_campaign.resource_name)


def add_campaign_group(client, customer_id):
    campaign_group_service = client.get_service('CampaignGroupService')

    # Create the operation.
    campaign_group_operation = client.get_type('CampaignGroupOperation')

    # Create a campaign group and set its name.
    campaign_group = campaign_group_operation.create
    campaign_group.name.value = 'Mars campaign group #%s' % uuid.uuid4()

    try:
        # Add the campaign group.
        cg_resource_name = campaign_group_service.mutate_campaign_groups(
            customer_id, [campaign_group_operation]).results[0].resource_name
    except google.ads.google_ads.errors.GoogleAdsException as ex:
        print('Request with ID "%s" failed with status "%s" and includes the '
              'following errors:' % (ex.request_id, ex.error.code().name))
        for error in ex.failure.errors:
            print('\tError with message "%s".' % error.message)
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print('\t\tOn field: %s' % field_path_element.field_name)
        sys.exit(1)

    print('Added campaign group with resource name: %s' % cg_resource_name)
    return cg_resource_name


def main(client, customer_id, campaign_ids):
    cg_resource_name = add_campaign_group(client, customer_id)
    add_campaigns_to_group(client, customer_id, cg_resource_name, campaign_ids)


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
    parser.add_argument('-i', '--campaign_ids', type=six.text_type,
                        required=True, nargs='+',
                        help='A list of campaign IDs separated by spaces.')
    args = parser.parse_args()

    main(google_ads_client, args.customer_id, args.campaign_ids)
