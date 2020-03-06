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
"""This example adds an expanded text ad.

To get expanded text ads, run get_expanded_text_ads.py.
"""


import argparse
import sys
import uuid

import google.ads.google_ads.client


def main(client, customer_id, ad_group_id, number_of_ads):
    ad_group_ad_service = client.get_service('AdGroupAdService', version='v3')
    ad_group_service = client.get_service('AdGroupService', version='v3')

    ad_group_ad_operations = []

    for i in range(number_of_ads):

        # Create ad group ad.
        ad_group_ad_operation = client.get_type('AdGroupAdOperation', version='v3')
        ad_group_ad = ad_group_ad_operation.create
        ad_group_ad.ad_group.value = ad_group_service.ad_group_path(
            customer_id, ad_group_id)
        ad_group_ad.status = client.get_type('AdGroupAdStatusEnum',
                                             version='v3').PAUSED

        # Set expanded text ad info
        final_url = ad_group_ad.ad.final_urls.add()
        final_url.value = 'http://www.example.com'
        ad_group_ad.ad.expanded_text_ad.description.value = 'Buy your tickets now!'
        ad_group_ad.ad.expanded_text_ad.headline_part1.value = (
            'Cruise {} to Mars {}'.format(i, str(uuid.uuid4())[:8]))
        ad_group_ad.ad.expanded_text_ad.headline_part2.value = (
            'Best space cruise line')
        ad_group_ad.ad.expanded_text_ad.path1.value = 'all-inclusive'
        ad_group_ad.ad.expanded_text_ad.path2.value = 'deals'

        ad_group_ad_operations.append(ad_group_ad_operation)

    try:
        ad_group_ad_response = ad_group_ad_service.mutate_ad_group_ads(
            customer_id, ad_group_ad_operations)
    except google.ads.google_ads.errors.GoogleAdsException as ex:
        print('Request with ID "{}" failed with status "{}" and includes the '
              'following errors:'.format(ex.request_id, ex.error.code().name))
        for error in ex.failure.errors:
            print('\tError with message "{}".'.format(error.message))
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print('\t\tOn field: {}'.format(field_path_element.field_name))
        sys.exit(1)

    for result in ad_group_ad_response.results:
        print('Created ad group ad {}.'.format(result.resource_name))


if __name__ == '__main__':
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    google_ads_client = (google.ads.google_ads.client.GoogleAdsClient
                         .load_from_storage())

    parser = argparse.ArgumentParser(
        description=('Adds an expanded text ad to the specified ad group ID, '
                     'for the given customer ID.'))
    # The following argument(s) should be provided to run the example.
    parser.add_argument('-c', '--customer_id', type=str,
                        required=True, help='The Google Ads customer ID.')
    parser.add_argument('-a', '--ad_group_id', type=str,
                        required=True, help='The ad group ID.')
    parser.add_argument('-n', '--number_of_ads', type=int,
                        required=False, default=1, help='The number of ads.')
    args = parser.parse_args()

    main(google_ads_client, args.customer_id, args.ad_group_id, args.number_of_ads)
