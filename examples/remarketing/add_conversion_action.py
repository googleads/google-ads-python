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
"""This example illustrates adding a conversion action."""

from __future__ import absolute_import

import argparse
import six
import sys
import uuid

import google.ads.google_ads.client


def main(client, customer_id):
    conversion_action_service = client.get_service('ConversionActionService',
                                                   version='v1')

    # Create the operation.
    conversion_action_operation = client.get_type('ConversionActionOperation',
                                                  version='v1')

    # Create conversion action.
    conversion_action = conversion_action_operation.create
    conversion_action.name.value = (
        'Earth to Mars Cruises Conversion %s' % uuid.uuid4())
    conversion_action.type = client.get_type(
        'ConversionActionTypeEnum').UPLOAD_CLICKS
    conversion_action.category = client.get_type(
        'ConversionActionCategoryEnum').DEFAULT
    conversion_action.status = client.get_type(
        'ConversionActionStatusEnum').ENABLED
    conversion_action.view_through_lookback_window_days.value = 15

    # Create a value settings object.
    value_settings = conversion_action.value_settings
    value_settings.default_value.value = 15.0
    value_settings.always_use_default_value.value = True

    # Add the conversion action.
    try:
        conversion_action_response = (
            conversion_action_service.mutate_conversion_actions(
                customer_id, [conversion_action_operation]))
    except google.ads.google_ads.errors.GoogleAdsException as ex:
        print('Request with ID "%s" failed with status "%s" and includes the '
              'following errors:' % (ex.request_id, ex.error.code().name))
        for error in ex.failure.errors:
            print('\tError with message "%s".' % error.message)
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print('\t\tOn field: %s' % field_path_element.field_name)
        sys.exit(1)

    print('Created conversion action "%s".'
          % conversion_action_response.results[0].resource_name)


if __name__ == '__main__':
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    google_ads_client = (google.ads.google_ads.client.GoogleAdsClient
                         .load_from_storage())

    parser = argparse.ArgumentParser(
        description='Adds a conversion action for specified customer.')
    # The following argument(s) should be provided to run the example.
    parser.add_argument('-c', '--customer_id', type=six.text_type,
                        required=True, help='The Google Ads customer ID.')
    args = parser.parse_args()

    main(google_ads_client, args.customer_id)
