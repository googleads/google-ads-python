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
"""This example lists the resource names for the customers that the
authenticating user has access to.

The customer IDs retrieved from the resource names can be used to set
the login-customer-id configuration. For more information see this
documentation: https://developers.google.com/google-ads/api/docs/concepts/call-structure#login-customer-id
"""

from __future__ import absolute_import

import sys

import google.ads.google_ads.client


def main(client):
    customer_service = client.get_service('CustomerService')

    try:
        accessible_customers = customer_service.list_accessible_customers()
        result_total = len(accessible_customers.resource_names)
        print('Total results: %i' % result_total)

        resource_names = accessible_customers.resource_names
        for resource_name in resource_names:
            print('Customer resource name: "%s"' % resource_name)
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

    main(google_ads_client)
