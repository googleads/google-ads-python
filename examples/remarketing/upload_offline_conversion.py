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
"""This example imports offline conversion values for specific clicks.

To get Google Click ID for a click, use the "click_view" resource:
https://developers.google.com/google-ads/api/fields/latest/click_view.
To set up a conversion action, run the add_conversion_action.py example.
"""


import argparse
import sys

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


# [START upload_offline_conversion]
def main(
    client,
    customer_id,
    conversion_action_id,
    gclid,
    conversion_date_time,
    conversion_value,
):
    """Creates a click conversion with a default currency of USD."""
    click_conversion = client.get_type("ClickConversion")
    conversion_action_service = client.get_service("ConversionActionService")
    click_conversion.conversion_action = conversion_action_service.conversion_action_path(
        customer_id, conversion_action_id
    )
    click_conversion.gclid = gclid
    click_conversion.conversion_value = float(conversion_value)
    click_conversion.conversion_date_time = conversion_date_time
    click_conversion.currency_code = "USD"

    conversion_upload_service = client.get_service("ConversionUploadService")
    request = client.get_type("UploadClickConversionsRequest")
    request.customer_id = customer_id
    request.conversions = [click_conversion]
    request.partial_failure = True
    conversion_upload_response = conversion_upload_service.upload_click_conversions(
        request=request,
    )
    uploaded_click_conversion = conversion_upload_response.results[0]
    print(
        f"Uploaded conversion that occurred at "
        f'"{uploaded_click_conversion.conversion_date_time}" from '
        f'Google Click ID "{uploaded_click_conversion.gclid}" '
        f'to "{uploaded_click_conversion.conversion_action}"'
    )
    # [END upload_offline_conversion]


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v8")

    parser = argparse.ArgumentParser(
        description="Uploads an offline conversion."
    )
    # The following argument(s) should be provided to run the example.
    parser.add_argument(
        "-c",
        "--customer_id",
        type=str,
        required=True,
        help="The Google Ads customer ID.",
    )
    parser.add_argument(
        "-a",
        "--conversion_action_id",
        type=str,
        required=True,
        help="The conversion action ID.",
    )
    parser.add_argument(
        "-g",
        "--gclid",
        type=str,
        required=True,
        help="The Google Click Identifier ID "
        "(gclid) which should be newer than the number of "
        "days set on the conversion window of the conversion "
        "action.",
    )
    parser.add_argument(
        "-t",
        "--conversion_date_time",
        type=str,
        required=True,
        help="The the date and time of the "
        "conversion (should be after the click time). The "
        'format is "yyyy-mm-dd hh:mm:ss+|-hh:mm", e.g. '
        "“2019-01-01 12:32:45-08:00”",
    )
    parser.add_argument(
        "-v",
        "--conversion_value",
        type=str,
        required=True,
        help="The conversion value.",
    )
    args = parser.parse_args()

    try:
        main(
            googleads_client,
            args.customer_id,
            args.conversion_action_id,
            args.gclid,
            args.conversion_date_time,
            args.conversion_value,
        )
    except GoogleAdsException as ex:
        print(
            f'Request with ID "{ex.request_id}" failed with status '
            f'"{ex.error.code().name}" and includes the following errors:'
        )
        for error in ex.failure.errors:
            print(f'\tError with message "{error.message}".')
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print(f"\t\tOn field: {field_path_element.field_name}")
        sys.exit(1)
