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
"""This example removes a billing setup with the specified ID.

To get available billing setups, run get_billing_setups.py.
"""


import argparse
import sys

import google.ads.google_ads.client


def main(client, customer_id, billing_setup_id):
    billing_setup_service = client.get_service('BillingSetupService',
                                               version='v4')

    # Create billing setup operation.
    billing_setup_operation = client.get_type('BillingSetupOperation',
                                              version='v4')
    billing_setup_operation.remove = billing_setup_service.billing_setup_path(
        customer_id, billing_setup_id)

    # Remove the billing setup.
    try:
        billing_setup_response = billing_setup_service.mutate_billing_setup(
            customer_id, billing_setup_operation)
    except google.ads.google_ads.errors.GoogleAdsException as ex:
        print('Request with ID "%s" failed with status "%s" and includes the '
              'following errors:' % (ex.request_id, ex.error.code().name))
        for error in ex.failure.errors:
            print('\tError with message "%s".' % error.message)
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print('\t\tOn field: %s' % field_path_element.field_name)
        sys.exit(1)

    print('Removed billing setup %s.'
          % billing_setup_response.results[0].resource_name)


if __name__ == '__main__':
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    google_ads_client = (google.ads.google_ads.client.GoogleAdsClient
                         .load_from_storage())

    parser = argparse.ArgumentParser(
        description=('Removes billing setup for specified customer and billing '
                     'setup ID.'))
    # The following argument(s) should be provided to run the example.
    parser.add_argument('-c', '--customer_id', type=str,
                        required=True, help='The Google Ads customer ID.')
    parser.add_argument('-b', '--billing_setup_id', type=str,
                        required=True, help='The billing setup ID.')
    args = parser.parse_args()

    main(google_ads_client, args.customer_id, args.billing_setup_id)
