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
"""Demonstrates how to create a shared list of negative broad match keywords.

Note that the keywords will be attached to the specified campaign.
"""

from __future__ import absolute_import

import argparse
import six
import sys
import uuid

import google.ads.google_ads.client


def main(client, customer_id, campaign_id):
    campaign_service = client.get_service('CampaignService')
    shared_set_service = client.get_service('SharedSetService')
    shared_criterion_service = client.get_service('SharedCriterionService')
    campaign_shared_set_service = client.get_service('CampaignSharedSetService')

    # Create shared negative keyword set.
    shared_set_operation = client.get_type('SharedSetOperation')
    shared_set = shared_set_operation.create
    shared_set.name.value = 'API Negative keyword list - %s' % uuid.uuid4()
    shared_set.type = client.get_type('SharedSetTypeEnum').NEGATIVE_KEYWORDS

    try:
        shared_set_resource_name = shared_set_service.mutate_shared_sets(
            customer_id, [shared_set_operation]).results[0].resource_name
    except google.ads.google_ads.errors.GoogleAdsException as ex:
        print('Request with ID "%s" failed with status "%s" and includes the '
              'following errors:' % (ex.request_id, ex.error.code().name))
        for error in ex.failure.errors:
            print('\tError with message "%s".' % error.message)
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print('\t\tOn field: %s' % field_path_element.field_name)
        sys.exit(1)

    print('Created shared set "%s".' % shared_set_resource_name)

    # Keywords to create a shared set of.
    keywords = ['mars cruise', 'mars hotels']

    shared_criteria_operations = []
    for keyword in keywords:
        shared_criterion_operation = client.get_type('SharedCriterionOperation')
        shared_criterion = shared_criterion_operation.create
        keyword_info = shared_criterion.keyword
        keyword_info.text.value = keyword
        keyword_info.match_type = client.get_type('KeywordMatchTypeEnum').BROAD
        shared_criterion.shared_set.value = shared_set_resource_name
        shared_criteria_operations.append(shared_criterion_operation)

    try:
        response = shared_criterion_service.mutate_shared_criteria(
            customer_id, shared_criteria_operations)
    except google.ads.google_ads.errors.GoogleAdsException as ex:
        print('Request with ID "%s" failed with status "%s" and includes the '
              'following errors:' % (ex.request_id, ex.error.code().name))
        for error in ex.failure.errors:
            print('\tError with message "%s".' % error.message)
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print('\t\tOn field: %s' % field_path_element.field_name)
        sys.exit(1)

    for shared_criterion in response.results:
        print('Created shared criterion "%s".' % shared_criterion.resource_name)

    campaign_set_operation = client.get_type('CampaignSharedSetOperation')
    campaign_set = campaign_set_operation.create
    campaign_set.campaign.value = campaign_service.campaign_path(
        customer_id, campaign_id)
    campaign_set.shared_set.value = shared_set_resource_name

    try:
        campaign_shared_set_resource_name = (
            campaign_shared_set_service.mutate_campaign_shared_sets(
                customer_id, [campaign_set_operation]).results[0].resource_name)
    except google.ads.google_ads.errors.GoogleAdsException as ex:
        print('Request with ID "%s" failed with status "%s" and includes the '
              'following errors:' % (ex.request_id, ex.error.code().name))
        for error in ex.failure.errors:
            print('\tError with message "%s".' % error.message)
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print('\t\tOn field: %s' % field_path_element.field_name)
        sys.exit(1)

    print('Created campaign shared set "%s".'
          % campaign_shared_set_resource_name)


if __name__ == '__main__':
    # GoogleAdsClient will read a google-ads.yaml configuration file in the
    # home directory if none is specified.
    google_ads_client = (google.ads.google_ads.client.GoogleAdsClient
                         .load_from_storage())

    parser = argparse.ArgumentParser(
        description=('Adds a list of negative broad match keywords to the '
                     'provided campaign, for the specified customer.'))
    # The following argument(s) should be provided to run the example.
    parser.add_argument('-c', '--customer_id', type=six.text_type,
                        required=True, help='The AdWords customer ID.')
    parser.add_argument('-i', '--campaign_id', type=six.text_type,
                        required=True, help='The campaign ID.')
    args = parser.parse_args()

    main(google_ads_client, args.customer_id, args.campaign_id)
