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
"""This adds an expanded text ad using advanced features of upgraded URLs."""

from __future__ import absolute_import

import argparse
import six
import sys

import google.ads.google_ads.client


def main(client, customer_id, ad_group_id):
    ad_group_ad_service = client.get_service('AdGroupAdService')
    ad_group_service = client.get_service('AdGroupService')

    # Create ad group ad.
    ad_group_ad_operation = client.get_type('AdGroupAdOperation')
    ad_group_ad = ad_group_ad_operation.create
    ad_group_ad.ad_group.value = ad_group_service.ad_group_path(
        customer_id, ad_group_id)
    ad_group_ad.status = client.get_type('AdGroupAdStatusEnum').PAUSED

    # Set expanded text ad info
    final_url = ad_group_ad.ad.final_urls.add()
    final_url.value = 'http://www.example.com/cruise/space/'
    final_url = ad_group_ad.ad.final_urls.add()
    final_url.value = 'http://www.example.com/locations/mars/'

    ad_group_ad.ad.expanded_text_ad.description.value = (
        'Low-gravity fun for everyone!')
    ad_group_ad.ad.expanded_text_ad.headline_part1.value = (
        'Luxury cruise to Mars')
    ad_group_ad.ad.expanded_text_ad.headline_part2.value = (
        'Visit the Red Planet in Style.')

    # Specify a tracking URL for 3rd party tracking provider. You may specify
    # one at customer, campaign, ad group, ad, criterion, or feed item levels.
    ad_group_ad.ad.tracking_url_template.value = (
        'http://tracker.example.com/?season={_season}&promocode={_promocode}&'
        'u={lpurl}'
    )

    # Since your tracking URL has two custom parameters, provide their values
    # too. This can be provided at campaign, ad group, ad, criterion, or feed
    # item levels.
    param_1 = ad_group_ad.ad.url_custom_parameters.add()
    param_1.key.value = 'season'
    param_1.value.value = 'easter123'

    param_2 = ad_group_ad.ad.url_custom_parameters.add()
    param_2.key.value = 'promocode'
    param_2.value.value = 'nj123'

    # Specify a list of final mobile URLs. This field cannot be set if URL field
    # is set, or finalUrls is unset. This may be specified at ad, criterion, and
    # feed item levels.
    final_mobile_url = ad_group_ad.ad.final_mobile_urls.add()
    final_mobile_url.value = 'http://mobile.example.com/cruise/space/'
    final_mobile_url = ad_group_ad.ad.final_mobile_urls.add()
    final_mobile_url.value = 'http://mobile.example.com/locations/mars/'

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

    print('Created expanded text ad %s.'
          % ad_group_ad_response.results[0].resource_name)


if __name__ == '__main__':
    # GoogleAdsClient will read a google-ads.yaml configuration file in the
    # home directory if none is specified.
    google_ads_client = (google.ads.google_ads.client.GoogleAdsClient
                         .load_from_storage())

    parser = argparse.ArgumentParser(
        description=('Adds an expanded text ad to the specified ad group ID, '
                     'for the given customer ID.'))
    # The following argument(s) should be provided to run the example.
    parser.add_argument('-c', '--customer_id', type=six.text_type,
                        required=True, help='The AdWords customer ID.')
    parser.add_argument('-a', '--ad_group_id', type=six.text_type,
                        required=True, help='The ad group ID.')
    args = parser.parse_args()

    main(google_ads_client, args.customer_id, args.ad_group_id)
