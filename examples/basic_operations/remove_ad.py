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
"""This example removes an existing ad."""

from __future__ import absolute_import

import argparse
import six
import sys

from google.ads.google_ads.client import GoogleAdsClient
from google.ads.google_ads.util import ResourceName

def main(client, customer_id, ad_group_id, ad_id):
    ad_group_ad_service = client.get_service('AdGroupAdService', version='v1')
    ad_group_ad_operation = client.get_type('AdGroupAdOperation', version='v1')

    resource_name = ad_group_ad_service.ad_group_ad_path(
        customer_id, ResourceName.format_composite(ad_group_id, ad_id))
    ad_group_ad_operation.remove = resource_name

    try:
        ad_group_ad_response = ad_group_ad_service.mutate_ad_group_ads(
            customer_id, [ad_group_ad_operation])
    except google.ads.google_ads.errors.GoogleAdsException as ex:
        print('Request with ID "%s" failed with status "%s" and includes the '
              'following errors:' % (ex.request_id, ex.error.code().name))
        for error in ex.failure.errors:
            print('\tError with message "%s".' % error.message)
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print('\t\tOn field: %s' % field_path_element.field_name)
        sys.exit(1)

    print('Removed ad group ad %s.'
          % ad_group_ad_response.results[0].resource_name)


if __name__ == '__main__':
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    google_ads_client = GoogleAdsClient.load_from_storage()
    parser = argparse.ArgumentParser(
        description=('Removes an ad from the specified customer\'s ad group.'))
    # The following argument(s) should be provided to run the example.
    parser.add_argument('-c', '--customer_id', type=six.text_type,
                        required=True, help='The Google Ads customer ID.')
    parser.add_argument('-a', '--ad_group_id', type=six.text_type,
                        required=True, help='The ad group ID.')
    parser.add_argument('-i', '--ad_id', type=six.text_type, required=True,
                        help='The ad ID.')
    args = parser.parse_args()

    main(google_ads_client, args.customer_id, args.ad_group_id, args.ad_id)
