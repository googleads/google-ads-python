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
"""Demonstrates how to find and remove shared sets, and shared set criteria."""

from __future__ import absolute_import

import argparse
import six
import sys

import google.ads.google_ads.client


_DEFAULT_PAGE_SIZE = 1000


def main(client, customer_id, page_size, campaign_id):
    ga_service = client.get_service('GoogleAdsService')
    shared_criterion_service = client.get_service('SharedCriterionService')

    # First, retrieve all shared sets associated with the campaign.
    shared_sets_query = (
        'SELECT shared_set.id, shared_set.name FROM campaign_shared_set '
        'WHERE campaign.id = %s' % campaign_id)

    try:
        shared_set_response = ga_service.search(
            customer_id, query=shared_sets_query, page_size=page_size)
    except google.ads.google_ads.errors.GoogleAdsException as ex:
        print('Request with ID "%s" failed with status "%s" and includes the '
              'following errors:' % (ex.request_id, ex.error.code().name))
        for error in ex.failure.errors:
            print('\tError with message "%s".' % error.message)
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print('\t\tOn field: %s' % field_path_element.field_name)
        sys.exit(1)

    shared_set_ids = []
    for row in shared_set_response:
        shared_set = row.shared_set
        shared_set_id = str(shared_set.id.value)
        shared_set_ids.append(shared_set_id)
        print('Campaign shared set ID "%s" and name "%s" was found.'
              % (shared_set_id, shared_set.name.value))

    # Next, retrieve shared criteria for all found shared sets.
    shared_criteria_query = (
        'SELECT shared_criterion.type, shared_criterion.keyword.text, '
        'shared_criterion.keyword.match_type, shared_set.id '
        'FROM shared_criterion WHERE shared_set.id IN (%s)'
        % ', '.join(shared_set_ids))

    try:
        shared_criteria_response = ga_service.search(
            customer_id, query=shared_criteria_query, page_size=page_size)
    except google.ads.google_ads.errors.GoogleAdsException as ex:
        print('Request with ID "%s" failed with status "%s" and includes the '
              'following errors:' % (ex.request_id, ex.error.code().name))
        for error in ex.failure.errors:
            print('\tError with message "%s".' % error.message)
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print('\t\tOn field: %s' % field_path_element.field_name)
        sys.exit(1)

    # Use the enum type to determine the enum name from the value.
    keyword_match_type_enum = (
        client.get_type('KeywordMatchTypeEnum').KeywordMatchType)

    criterion_ids = []
    for row in shared_criteria_response:
        shared_criterion = row.shared_criterion
        shared_criterion_resource_name = shared_criterion.resource_name
        if (shared_criterion.type ==
                client.get_type('CriterionTypeEnum').KEYWORD):
            keyword = shared_criterion.keyword
            print('Shared criterion with resource name "%s" for negative '
                  'keyword with text "%s" and match type "%s" was found.'
                  % (shared_criterion_resource_name, keyword.text.value,
                     keyword_match_type_enum.Name(keyword.match_type)))
        criterion_ids.append(shared_criterion_resource_name)

    operations = []

    # Finally, remove the criteria.
    for criteria_id in criterion_ids:
        shared_criterion_operation = client.get_type('SharedCriterionOperation')
        shared_criterion_operation.remove = criteria_id
        operations.append(shared_criterion_operation)

    try:
        response = shared_criterion_service.mutate_shared_criteria(
            customer_id, operations)
    except google.ads.google_ads.errors.GoogleAdsException as ex:
        print('Request with ID "%s" failed with status "%s" and includes the '
              'following errors:' % (ex.request_id, ex.error.code().name))
        for error in ex.failure.errors:
            print('\tError with message "%s".' % error.message)
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print('\t\tOn field: %s' % field_path_element.field_name)
        sys.exit(1)

    for result in response.results:
        print('Removed shared criterion "%s".' % result.resource_name)


if __name__ == '__main__':
    # GoogleAdsClient will read a google-ads.yaml configuration file in the
    # home directory if none is specified.
    google_ads_client = (google.ads.google_ads.client.GoogleAdsClient
                         .load_from_storage())

    parser = argparse.ArgumentParser(
        description=('Finds shared sets, then finds and removes shared set '
                     'criteria under them.'))
    # The following argument(s) should be provided to run the example.
    parser.add_argument('-c', '--customer_id', type=six.text_type,
                        required=True, help='The AdWords customer ID.')
    parser.add_argument('-i', '--campaign_id', type=six.text_type,
                        required=True, help='The campaign ID.')
    args = parser.parse_args()

    main(google_ads_client, args.customer_id, _DEFAULT_PAGE_SIZE,
         args.campaign_id)
