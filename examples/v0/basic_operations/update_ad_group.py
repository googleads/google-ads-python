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
"""This example updates an ad group.

To get ad groups, run get_ad_groups.py.
"""

from __future__ import absolute_import

import argparse
import six
import sys

import google.ads.google_ads.client
from google.api_core import protobuf_helpers


def main(client, customer_id, ad_group_id, bid_micro_amount):
    ad_group_service = client.get_service('AdGroupService')

    # Create ad group operation.
    ad_group_operation = client.get_type('AdGroupOperation')
    ad_group = ad_group_operation.update
    ad_group.resource_name = ad_group_service.ad_group_path(
        customer_id, ad_group_id)
    ad_group.status = client.get_type('AdGroupStatusEnum').PAUSED
    ad_group.cpc_bid_micros.value = bid_micro_amount
    fm = protobuf_helpers.field_mask(None, ad_group)
    ad_group_operation.update_mask.CopyFrom(fm)

    # Update the ad group.
    try:
        ad_group_response = ad_group_service.mutate_ad_groups(
            customer_id, [ad_group_operation])
    except google.ads.google_ads.errors.GoogleAdsException as ex:
        print('Request with ID "%s" failed with status "%s" and includes the '
              'following errors:' % (ex.request_id, ex.error.code().name))
        for error in ex.failure.errors:
            print('\tError with message "%s".' % error.message)
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print('\t\tOn field: %s' % field_path_element.field_name)
        sys.exit(1)

    print('Updated ad group %s.' % ad_group_response.results[0].resource_name)


if __name__ == '__main__':
    # GoogleAdsClient will read a google-ads.yaml configuration file in the
    # home directory if none is specified.
    google_ads_client = (google.ads.google_ads.client.GoogleAdsClient
                         .load_from_storage())

    parser = argparse.ArgumentParser(
        description=('Updates an ad group for specified customer and campaign '
                     'id with the given bid micro amount.'))
    # The following argument(s) should be provided to run the example.
    parser.add_argument('-c', '--customer_id', type=six.text_type,
                        required=True, help='The AdWords customer ID.')
    parser.add_argument('-a', '--ad_group_id', type=six.text_type,
                        required=True, help='The ad group ID.')
    parser.add_argument('-b', '--bid_micro_amount', type=int,
                        required=True, help='The bid micro amount.')
    args = parser.parse_args()

    main(google_ads_client, args.customer_id, args.ad_group_id,
         args.bid_micro_amount)
