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
"""Gets all billing setup objects available for the specified customer ID."""


import argparse
import sys

import google.ads.google_ads.client


_DEFAULT_PAGE_SIZE = 1000


def main(client, customer_id, page_size):
    ga_service = client.get_service('GoogleAdsService', version='v3')

    query = (
        'SELECT billing_setup.id, billing_setup.status, '
        'billing_setup.payments_account, '
        'billing_setup.payments_account_info.payments_account_id, '
        'billing_setup.payments_account_info.payments_account_name, '
        'billing_setup.payments_account_info.payments_profile_id, '
        'billing_setup.payments_account_info.payments_profile_name, '
        'billing_setup.payments_account_info.secondary_payments_profile_id '
        'FROM billing_setup')

    results = ga_service.search(customer_id, query=query, page_size=page_size)

    try:
        # Use the enum type to determine the enum name from the value.
        billing_setup_status_enum = (
            client.get_type('BillingSetupStatusEnum', version='v3')
                .BillingSetupStatus)

        print('Found the following billing setup results:')
        for row in results:
            billing_setup = row.billing_setup
            payments_account_info = billing_setup.payments_account_info
            print('Billing setup with ID "%s", status "%s", '
                  'payments_account "%s", payments_account_id "%s", '
                  'payments_account_name "%s", payments_profile_id "%s", '
                  'payments_profile_name "%s", '
                  'secondary_payments_profile_id "%s".'
                  % (billing_setup.id.value,
                     billing_setup_status_enum.Name(billing_setup.status),
                     billing_setup.payments_account.value,
                     payments_account_info.payments_account_id.value,
                     payments_account_info.payments_account_name.value,
                     payments_account_info.payments_profile_id.value,
                     payments_account_info.payments_profile_name.value,
                     payments_account_info.secondary_payments_profile_id.value))
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
        description='Lists all billing setup objects for specified customer.')
    # The following argument(s) should be provided to run the example.
    parser.add_argument('-c', '--customer_id', type=str,
                        required=True, help='The Google Ads customer ID.')
    args = parser.parse_args()

    main(google_ads_client, args.customer_id, _DEFAULT_PAGE_SIZE)
