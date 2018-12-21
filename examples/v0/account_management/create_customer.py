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
"""This example illustrates how to create a new customer under a given
manager account.

Note by default this account will only be accessible via its parent Google Ads
manager account.
"""

from __future__ import absolute_import

import argparse
import six
import sys

import google.ads.google_ads.client


def main(client, customer_id):
    customer_service = client.get_service('CustomerService')
    resource_name = customer_service.customer_path(customer_id)
    customer = client.get_type('Customer')
    customer.resource_name = resource_name
    customer.descriptive_name.value = 'A new customer.'
    # For a list of valid currency codes and time zones see this documentation:
    # https://developers.google.com/adwords/api/docs/appendix/codes-formats
    customer.currency_code.value = 'USD'
    customer.time_zone.value = 'America/New_York'
    # The below values are optional. For more information about tracking url
    # templates see: https://support.google.com/google-ads/answer/6305348
    customer.tracking_url_template.value = '{lpurl}?device={device}'
    customer.final_url_suffix.value = ('keyword={keyword}&matchtype={matchtype}'
                                       '&adgroupid={adgroupid}')
    customer.has_partners_badge.value = False

    try:
      response = customer_service.create_customer_client(
        customer_id, customer)
      print(('Customer created with resource name "%s" under manager account'
             ' with CID %s') % (response.resource_name, customer_id))
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
        description=('Creates a new client under the given manager.'))
    # The following argument(s) should be provided to run the example.
    parser.add_argument('-c', '--customer_id', type=six.text_type,
                        required=True, help='The Google Ads customer ID.')
    args = parser.parse_args()

    main(google_ads_client, args.customer_id)
