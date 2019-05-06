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
"""This example retrieves keywords for a customer."""

from __future__ import absolute_import

import argparse
import six
import sys

import google.ads.google_ads.client


_DEFAULT_PAGE_SIZE = 1000


def main(client, customer_id, page_size, ad_group_id=None):
    ga_service = client.get_service('GoogleAdsService', version='v1')

    query = ('SELECT ad_group.id, ad_group_criterion.type, '
             'ad_group_criterion.criterion_id, '
             'ad_group_criterion.keyword.text, '
             'ad_group_criterion.keyword.match_type FROM ad_group_criterion '
             'WHERE ad_group_criterion.type = KEYWORD')

    if ad_group_id:
        query = '%s AND ad_group.id = %s' % (query, ad_group_id)

    results = ga_service.search(customer_id, query=query, page_size=page_size)

    try:
        for row in results:
            ad_group = row.ad_group
            ad_group_criterion = row.ad_group_criterion
            keyword = row.ad_group_criterion.keyword

            print('Keyword with text "%s", match type %s, criteria type %s, '
                  'and ID %s was found in ad group with ID %s.'
                  % (keyword.text.value, keyword.match_type,
                     ad_group_criterion.type,
                     ad_group_criterion.criterion_id.value, ad_group.id.value))
    except google.ads.google_ads.errors.GoogleAdsException as ex:
        print('Request with ID "%s" failed with status "%s" and includes the '
              'following errors:' % (ex.request_id, ex.error.code().name))
        for error in ex.failure.errors:
            print('\tError with message "%s".' % error.message)
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print('\t\tOn field: %s' % field_path_element.field_name)
        sys.exit(1)


if __name__ == '__main__':
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    google_ads_client = (google.ads.google_ads.client.GoogleAdsClient
                         .load_from_storage())

    parser = argparse.ArgumentParser(
        description=('Retrieves keywords for the specified customer, or '
                     'optionally for a specific ad group.'))
    # The following argument(s) should be provided to run the example.
    parser.add_argument('-c', '--customer_id', type=six.text_type,
                        required=True, help='The Google Ads customer ID.')
    parser.add_argument('-a', '--ad_group_id', type=six.text_type,
                        required=False, help='The ad group ID.')
    args = parser.parse_args()

    main(google_ads_client, args.customer_id, _DEFAULT_PAGE_SIZE,
         ad_group_id=args.ad_group_id)
