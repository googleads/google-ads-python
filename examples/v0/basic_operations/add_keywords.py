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
"""This example demonstrates how to add a keyword to an ad group."""

from __future__ import absolute_import

import argparse
import six
import sys

import google.ads.google_ads.client


def main(client, customer_id, ad_group_id, keyword):
    ad_group_service = client.get_service('AdGroupService')
    ad_group_criterion_service = client.get_service('AdGroupCriterionService')

    # Create keyword.
    ad_group_criterion_operation = client.get_type('AdGroupCriterionOperation')
    ad_group_criterion = ad_group_criterion_operation.create
    ad_group_criterion.ad_group.value = ad_group_service.ad_group_path(
        customer_id, ad_group_id)
    ad_group_criterion.status = client.get_type(
        'AdGroupCriterionStatusEnum').ENABLED
    ad_group_criterion.keyword.text.value = keyword
    ad_group_criterion.keyword.match_type = client.get_type(
        'KeywordMatchTypeEnum').EXACT

    # Optional field
    # All fields can be referenced from the protos directly.
    # The protos are located in subdirectories under
    # google/ads/googleads/v0/proto.
    # ad_group_criterion.negative.value = True

    # Optional repeated field
    # final_url = ad_group_criterion.final_urls.add()
    # final_url.value = 'https://www.example.com'

    # Add keyword
    try:
        ad_group_criterion_response = (
            ad_group_criterion_service.mutate_ad_group_criteria(
                customer_id, [ad_group_criterion_operation]))
    except google.ads.google_ads.errors.GoogleAdsException as ex:
        print('Request with ID "%s" failed with status "%s" and includes the '
              'following errors:' % (ex.request_id, ex.error.code().name))
        for error in ex.failure.errors:
            print('\tError with message "%s".' % error.message)
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print('\t\tOn field: %s' % field_path_element.field_name)
        sys.exit(1)

    print('Created keyword %s.'
          % ad_group_criterion_response.results[0].resource_name)


if __name__ == '__main__':
    # GoogleAdsClient will read a google-ads.yaml configuration file in the
    # home directory if none is specified.
    google_ads_client = (google.ads.google_ads.client.GoogleAdsClient
                         .load_from_storage())

    parser = argparse.ArgumentParser(
        description=('Adds a keyword to the provided ad group, for the '
                     'specified customer.'))
    # The following argument(s) should be provided to run the example.
    parser.add_argument('-c', '--customer_id', type=six.text_type,
                        required=True, help='The AdWords customer ID.')
    parser.add_argument('-a', '--ad_group_id', type=six.text_type,
                        required=True, help='The ad group ID.')
    parser.add_argument('-k', '--keyword', type=six.text_type, required=False,
                        default='mars cruise',
                        help=('The keyword to be added to the ad group. Note '
                              'that you will receive an error response if you '
                              'attempt to create a duplicate keyword.'))
    args = parser.parse_args()

    main(google_ads_client, args.customer_id, args.ad_group_id, args.keyword)
