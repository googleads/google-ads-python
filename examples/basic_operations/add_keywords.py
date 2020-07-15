#!/usr/bin/env python
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


import argparse
import sys

from google.ads.google_ads.client import GoogleAdsClient
from google.ads.google_ads.errors import GoogleAdsException


def main(client, customer_id, ad_group_id, keyword_text):
    ad_group_service = client.get_service('AdGroupService', version='v4')
    ad_group_criterion_service = client.get_service('AdGroupCriterionService',
                                                    version='v4')

    # Create keyword.
    ad_group_criterion_operation = client.get_type('AdGroupCriterionOperation',
                                                   version='v4')
    ad_group_criterion = ad_group_criterion_operation.create
    ad_group_criterion.ad_group.value = ad_group_service.ad_group_path(
        customer_id, ad_group_id)
    ad_group_criterion.status = client.get_type(
        'AdGroupCriterionStatusEnum', version='v4').ENABLED
    ad_group_criterion.keyword.text.value = keyword_text
    ad_group_criterion.keyword.match_type = client.get_type(
        'KeywordMatchTypeEnum', version='v4').EXACT

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
    except GoogleAdsException as ex:
        print(f'Request with ID "{ex.request_id}" failed with status '
              f'"{ex.error.code().name}" and includes the following errors:')
        for error in ex.failure.errors:
            print(f'\tError with message "{error.message}".')
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print('\t\tOn field: {field_path_element.field_name}')
        sys.exit(1)

    print('Created keyword '
          f'{ad_group_criterion_response.results[0].resource_name}.')


if __name__ == '__main__':
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    google_ads_client = GoogleAdsClient.load_from_storage()

    parser = argparse.ArgumentParser(
        description=('Adds a keyword to the provided ad group, for the '
                     'specified customer.'))
    # The following argument(s) should be provided to run the example.
    parser.add_argument('-c', '--customer_id', type=str,
                        required=True, help='The Google Ads customer ID.')
    parser.add_argument('-a', '--ad_group_id', type=str,
                        required=True, help='The ad group ID.')
    parser.add_argument('-k', '--keyword_text', type=str, required=False,
                        default='mars cruise',
                        help=('The keyword to be added to the ad group. Note '
                              'that you will receive an error response if you '
                              'attempt to create a duplicate keyword.'))
    args = parser.parse_args()

    main(google_ads_client, args.customer_id, args.ad_group_id,
         args.keyword_text)
