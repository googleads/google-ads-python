# Copyright 2019 Google LLC
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
"""This example gets Hotel ads performance statistics for the 50 Hotel ad
groups with the most impressions over the last 7 days.
"""

from __future__ import absolute_import

import argparse
import six
import sys

import google.ads.google_ads.client


_DEFAULT_PAGE_SIZE = 50


def main(client, customer_id, page_size):
    ga_service = client.get_service('GoogleAdsService', version='v1')

    query = ('SELECT campaign.id, campaign.advertising_channel_type, '
             'ad_group.id, ad_group.status, metrics.impressions, '
             'metrics.hotel_average_lead_value_micros, '
             'segments.hotel_check_in_day_of_week, '
             'segments.hotel_length_of_stay '
             'FROM hotel_performance_view '
             'WHERE segments.date DURING LAST_7_DAYS '
             'AND campaign.advertising_channel_type = \'HOTEL\' '
             'AND ad_group.status = \'ENABLED\' '
             'ORDER BY metrics.impressions DESC '
             'LIMIT 50')

    response = ga_service.search(customer_id, query, page_size=page_size)

    try:
        for row in response:
            campaign = row.campaign
            ad_group = row.ad_group
            hotel_check_in_day_of_week = row.hotel_check_in_day_of_week
            hotel_length_of_stay = row.hotel_length_of_stay
            metrics = row.metrics

            print('Ad group ID "%s" in campaign ID "%s" ' % (ad_group.id.value,
                  campaign.id.value))
            print('with hotel check-in on "%s" and "%s" day(s) stay ' % (
                  hotel_check_in_day_of_week, hotel_length_of_stay.value))
            print('had %d impression(s) and %d average lead value (in micros) '
                  'during the last 7 days.\n' % (metrics.impressions.value,
                  metrics.hotel_average_lead_value_micros.value))

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
        description=('Retrieves Hotel-ads performance statistics.'))
    # The following argument(s) should be provided to run the example.
    parser.add_argument('-c', '--customer_id', type=six.text_type,
                        required=True, help='The Google Ads customer ID.')
    args = parser.parse_args()

    main(google_ads_client, args.customer_id, _DEFAULT_PAGE_SIZE)
