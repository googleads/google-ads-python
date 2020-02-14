#!/usr/bin/env python
# Copyright 2020 Google LLC
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
"""This example imports conversion adjustments for existing conversions.

To set up a conversion action, run the add_conversion_action.py example.
"""


import argparse
import sys

from google.ads.google_ads.client import GoogleAdsClient
from google.ads.google_ads.errors import GoogleAdsException


def main(client, customer_id, conversion_action_id, gclid, adjustment_type,
         conversion_date_time, adjustment_date_time, restatement_value):
    # Determine the adjustment type.
    conversion_adjustment_type_enum = (
        client.get_type('ConversionAdjustmentTypeEnum'))
    if adjustment_type.lower() == 'retraction':
        conversion_adjustment_type = conversion_adjustment_type_enum.RETRACTION
    elif adjustment_type.lower() == 'restatement':
        conversion_adjustment_type = (
            conversion_adjustment_type_enum.RESTATEMENT)
    else:
        raise ValueError('Invalid adjustment type specified.')

    # Associates conversion adjustments with the existing conversion action.
    # The GCLID should have been uploaded before with a conversion
    conversion_adjustment = (client.get_type('ConversionAdjustment',
                                             version='v2'))
    conversion_action_service = (client.get_service('ConversionActionService',
                                                    version='v2'))
    conversion_adjustment.conversion_action.value = (
        conversion_action_service.conversion_action_path(
            customer_id, conversion_action_id))
    conversion_adjustment.adjustment_type = conversion_adjustment_type
    conversion_adjustment.adjustment_date_time.value = adjustment_date_time

    # Set the Gclid Date
    conversion_adjustment.gclid_date_time_pair.gclid.value = gclid
    conversion_adjustment.gclid_date_time_pair.conversion_date_time.value = (
        conversion_date_time)

    # Sets adjusted value for adjustment type RESTATEMENT.
    if (restatement_value and
        conversion_adjustment_type ==
        conversion_adjustment_type_enum.RESTATEMENT):
        conversion_adjustment.restatement_value.adjusted_value.value = (
            float(restatement_value))

    conversion_adjustment_upload_service = (
        client.get_service('ConversionAdjustmentUploadService', version='v2'))
    try:
        response = (
            conversion_adjustment_upload_service.
            upload_conversion_adjustments(customer_id,
                                          [conversion_adjustment],
                                          partial_failure=True))
        conversion_adjustment_result = response.results[0]
        print(f'Uploaded conversion that occurred at '
              f'"{conversion_adjustment_result.adjustment_date_time.value}" '
              f'from Gclid '
              f'"{conversion_adjustment_result.gclid_date_time_pair.gclid.value}"'
              f' to "{conversion_adjustment_result.conversion_action.value}"')

    except GoogleAdsException as ex:
        print(f'Request with ID "{ex.request_id}" failed with status '
              f'"{ex.error.code().name}" and includes the following errors:')
        for error in ex.failure.errors:
            print(f'\tError with message "{error.message}".')
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print(f'\t\tOn field: {field_path_element.field_name}')
        sys.exit(1)


if __name__ == '__main__':
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    google_ads_client = GoogleAdsClient.load_from_storage()

    parser = argparse.ArgumentParser(
        description='Uploads a conversion adjustment.')
    # The following argument(s) should be provided to run the example.
    parser.add_argument('-c', '--customer_id', type=str,
                        required=True, help='The Google Ads customer ID.')
    parser.add_argument('-a', '--conversion_action_id', type=str,
                        required=True, help='The conversion action ID to be '
                        'uploaded to.')
    parser.add_argument('-g', '--gclid', type=str,
                        required=True, help='The Google Click Identifier ID.')
    parser.add_argument('-d', '--adjustment_type', type=str,
                        required=True, help='The Adjustment type, e.g. '
                        'RETRACTION, RESTATEMENT')
    parser.add_argument('-t', '--conversion_date_time', type=str,
                        required=True, help='The the date and time of the '
                        'conversion. The format is '
                        '"yyyy-mm-dd hh:mm:ss+|-hh:mm", e.g. '
                        '“2019-01-01 12:32:45-08:00”')
    parser.add_argument('-v', '--adjustment_date_time', type=str,
                        required=True, help='The the date and time of the '
                        'adjustment. The format is '
                        '"yyyy-mm-dd hh:mm:ss+|-hh:mm", e.g. '
                        '“2019-01-01 12:32:45-08:00”')
    # Optional: Specify an adjusted value for adjustment type RESTATEMENT.
    # This value will be ignored if you specify RETRACTION as adjustment type.
    parser.add_argument('-r', '--restatement_value', type=str,
                        required=False, help='The adjusted value for '
                        'adjustment type RESTATEMENT.')
    args = parser.parse_args()

    main(google_ads_client, args.customer_id, args.conversion_action_id,
         args.gclid, args.adjustment_type, args.conversion_date_time,
         args.adjustment_date_time, args.restatement_value)
