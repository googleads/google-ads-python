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
"""This example generates forecast metrics for a keyword plan.

To create a keyword plan, run the add_keyword_plan.py example.
"""

from __future__ import absolute_import

import argparse
import six
import sys

from google.ads.google_ads.client import GoogleAdsClient
from google.ads.google_ads.errors import GoogleAdsException


def main(client, customer_id, keyword_plan_id):
    keyword_plan_service = client.get_service('KeywordPlanService')
    resource_name = keyword_plan_service.keyword_plan_path(customer_id,
                                                           keyword_plan_id)

    try:
        response = keyword_plan_service.generate_forecast_metrics(resource_name)
    except GoogleAdsException as ex:
        print('Request with ID "%s" failed with status "%s" and includes the '
              'following errors:' % (ex.request_id, ex.error.code().name))
        for error in ex.failure.errors:
            print('\tError with message "%s".' % error.message)
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print('\t\tOn field: %s' % field_path_element.field_name)
        sys.exit(1)

    for i, forecast in enumerate(response.keyword_forecasts):
        print('#%s Keyword ID: %s' % (i + 1,
          forecast.keyword_plan_ad_group_keyword.value))

        metrics = forecast.keyword_forecast

        clicks = (f'{metrics.clicks.value:.2f}' if metrics.clicks
                  else 'unspecified')
        print('Estimated daily clicks: %s' % clicks)

        impressions = (f'{metrics.impressions.value:.2f}' if metrics.impressions
                       else 'unspecified')
        print('Estimated daily impressions: %s' % impressions)

        cpc = (f'{metrics.average_cpc.value:.2f}' if metrics.average_cpc
               else 'unspecified')
        print('Estimated average cpc: %s' % cpc, end='\n\n')


if __name__ == '__main__':
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    google_ads_client = GoogleAdsClient.load_from_storage()

    parser = argparse.ArgumentParser(
        description='Generates forecast metrics for a keyword plan.')
    # The following argument(s) should be provided to run the example.
    parser.add_argument('-c', '--customer_id', type=six.text_type,
                        required=True, help='The Google Ads customer ID.')
    parser.add_argument('-k', '--keyword_plan_id', type=six.text_type,
                        required=True, help='A Keyword Plan ID.')
    args = parser.parse_args()

    main(google_ads_client, args.customer_id, args.keyword_plan_id)
