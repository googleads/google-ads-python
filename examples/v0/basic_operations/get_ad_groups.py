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
"""This example illustrates how to retrieve ad groups."""

from __future__ import absolute_import

import argparse
import six
import sys
import google.ads.google_ads.client


_DEFAULT_PAGE_SIZE = 1000


def main(client, customer_id, page_size, campaign_id=None):
    ga_service = client.get_service('GoogleAdsService')

    query = 'SELECT campaign.id, ad_group.id, ad_group.name FROM ad_group'

    if campaign_id:
        query = '%s WHERE campaign.id = %s' % (query, campaign_id)

    results = ga_service.search(customer_id, query=query, page_size=page_size)

    try:
        for row in results:
            print('Ad group with ID %d and name "%s" was found in campaign '
                  'with ID %d.'
                  % (row.ad_group.id.value, row.ad_group.name.value,
                     row.campaign.id.value))
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
    # GoogleAdsClient will read a google-ads.yaml configuration file in the
    # home directory if none is specified.
    google_ads_client = (google.ads.google_ads.client.GoogleAdsClient
                         .load_from_storage())

    parser = argparse.ArgumentParser(
        description='List ad groups for specified customer.')
    # The following argument(s) should be provided to run the example.
    parser.add_argument('-c', '--customer_id', type=six.text_type,
                        required=True, help='The AdWords customer ID.')
    parser.add_argument('-i', '--campaign_id', type=six.text_type,
                        required=False,
                        help=('The campaign ID. Specify this to list ad groups '
                              'solely for this campaign ID.'))
    args = parser.parse_args()

    main(google_ads_client, args.customer_id, _DEFAULT_PAGE_SIZE,
         campaign_id=args.campaign_id)
