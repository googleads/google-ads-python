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
"""Imports offline call conversion values for calls related to your ads.

To set up a conversion action, run the add_conversion_action.py example.
"""


import argparse
import sys

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


# [START upload_call_conversion]
def main(
    client,
    customer_id,
    conversion_action_id,
    caller_id,
    call_start_date_time,
    conversion_date_time,
    conversion_value,
):
    """Imports offline call conversion values for calls related to your ads.

    Args:
        client: An initialized GoogleAdsClient instance.
        customer_id: The client customer ID string.
        conversion_action_id: The ID of the conversion action to upload to.
        caller_id: The caller ID from which this call was placed. Caller ID is
            expected to be in E.164 format with preceding '+' sign,
            e.g. '+16502531234'.
        call_start_date_time: The date and time at which the call occurred. The
            format is 'yyyy-mm-dd hh:mm:ss+|-hh:mm',
            e.g. '2021-01-01 12:32:45-08:00'.
        conversion_date_time: The the date and time of the conversion (should be
            after the click time). The format is 'yyyy-mm-dd hh:mm:ss+|-hh:mm',
            e.g. '2021-01-01 12:32:45-08:00'.
        conversion_value: The conversion value in the desired currency.
    """
    # Get the ConversionUploadService client.
    conversion_upload_service = client.get_service("ConversionUploadService")

    # Create a call conversion in USD currency.
    call_conversion = client.get_type("CallConversion")
    call_conversion.conversion_action = client.get_service(
        "ConversionActionService"
    ).conversion_action_path(customer_id, conversion_action_id)
    call_conversion.caller_id = caller_id
    call_conversion.call_start_date_time = call_start_date_time
    call_conversion.conversion_date_time = conversion_date_time
    call_conversion.conversion_value = conversion_value
    call_conversion.currency_code = "USD"

    # Issue a request to upload the call conversion.
    request = client.get_type("UploadCallConversionsRequest")
    request.customer_id = customer_id
    request.conversions = [call_conversion]
    request.partial_failure = True
    upload_call_conversions_response = conversion_upload_service.upload_call_conversions(
        request=request
    )

    # Print any partial errors returned.
    if upload_call_conversions_response.partial_failure_error:
        print(
            "Partial error ocurred: "
            f"'{upload_call_conversions_response.partial_failure_error.message}'"
        )

    # Print the result if valid.
    uploaded_call_conversion = upload_call_conversions_response.results[0]
    if uploaded_call_conversion.call_start_date_time:
        print(
            "Uploaded call conversion that occurred at "
            f"'{uploaded_call_conversion.call_start_date_time}' "
            f"for caller ID '{uploaded_call_conversion.caller_id}' "
            "to the conversion action with resource name "
            f"'{uploaded_call_conversion.conversion_action}'."
        )
    # [END upload_call_conversion]


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v8")

    parser = argparse.ArgumentParser(
        description="Imports offline call conversion values for calls related "
        "to your ads."
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
        help="The ID of the conversion action to upload to.",
    )
    parser.add_argument(
        "-i",
        "--caller_id",
        type=str,
        required=True,
        help="The caller ID from which this call was placed. Caller ID is "
        "expected to be in E.164 format with preceding '+' sign, "
        "e.g. '+16502531234'.",
    )
    parser.add_argument(
        "-s",
        "--call_start_date_time",
        type=str,
        required=True,
        help="The date and time at which the call occurred. The format is "
        "'yyyy-mm-dd hh:mm:ss+|-hh:mm', e.g. '2019-01-01 12:32:45-08:00'.",
    )
    parser.add_argument(
        "-t",
        "--conversion_date_time",
        type=str,
        required=True,
        help="The the date and time of the conversion (should be after the "
        "click time). The format is 'yyyy-mm-dd hh:mm:ss+|-hh:mm', e.g. "
        "'2019-01-01 12:32:45-08:00'.",
    )
    parser.add_argument(
        "-v",
        "--conversion_value",
        type=float,
        required=True,
        help="The conversion value in the desired currency.",
    )
    args = parser.parse_args()

    try:
        main(
            googleads_client,
            args.customer_id,
            args.conversion_action_id,
            args.caller_id,
            args.call_start_date_time,
            args.conversion_date_time,
            args.conversion_value,
        )
    except GoogleAdsException as ex:
        print(
            f"Request with ID '{ex.request_id}'' failed with status "
            f"'{ex.error.code().name}' and includes the following errors:"
        )
        for error in ex.failure.errors:
            print(f"\tError with message '{error.message}'.")
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print(f"\t\tOn field: {field_path_element.field_name}")
        sys.exit(1)
