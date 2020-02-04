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
"""This adds a smart display campaign, an ad group, and a responsive display ad.

More information about Smart Display campaigns can be found at:
https://support.google.com/google-ads/answer/7020281
"""


import argparse
import sys

import google.ads.google_ads.client


_marketing_image_url = 'https://goo.gl/3b9Wfh'
_marketing_image_width = 600
_marketing_image_height = 315

_square_marketing_image_url = 'https://goo.gl/mtt54n'
_square_marketing_image_size = 512


def main(client, customer_id, ad_group_id):
    pass


def _create_budget(client, customer_id):
    pass


def _create_smart_display_campaign(client, customer_id, campaign_resource_name):
    pass


def _create_ad_group(client, customer_id, campaign_resource_name):
    ad_group_service = client.get_service('AdGroupService', version='v2')


def _upload_image_asset(client, customer_id, image_url, image_width,
                        image_height):
    pass


def _create_responsive_display_ad(client, customer_id, ad_group_resource_name,
                                  marketing_image_asset_resource_name,
                                  square_marketing_image_asset_resource_name):
    ad_group_ad_service = client.get_service('AdGroupAdService', version='v2')

    # Create ad group ad.
    ad_group_ad_operation = client.get_type('AdGroupAdOperation', version='v2')
    ad_group_ad = ad_group_ad_operation.create
    ad_group_ad.ad_group.value = ad_group_service.ad_group_path(
        customer_id, ad_group_id)
    ad_group_ad.status = client.get_type('AdGroupAdStatusEnum',
                                         version='v2').PAUSED

    final_url = ad_group_ad.ad.final_urls.add()
    final_url.value = 'http://www.example.com/cruise/space/'
    final_url = ad_group_ad.ad.final_urls.add()
    final_url.value = 'http://www.example.com/locations/mars/'

    # Add the ad group ad.
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

    print('Created responsive display ad %s.'
          % ad_group_ad_response.results[0].resource_name)


if __name__ == '__main__':
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    google_ads_client = (google.ads.google_ads.client.GoogleAdsClient
                         .load_from_storage())

    parser = argparse.ArgumentParser(
        description=('Creates a Smart Display campaign, and an ad group that '
                     'are then used to create a responsive display ad.'))
    # The following argument(s) should be provided to run the example.
    parser.add_argument('-c', '--customer_id', type=str,
                        required=True, help='The Google Ads customer ID.')
    parser.add_argument('-a', '--ad_group_id', type=str,
                        required=True, help='The ad group ID.')
    args = parser.parse_args()

    main(google_ads_client, args.customer_id, args.ad_group_id)
