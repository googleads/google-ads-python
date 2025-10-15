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
from typing import Optional

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.ads.googleads.v22.services.services.conversion_upload_service import (
    ConversionUploadServiceClient,
)
from google.ads.googleads.v22.services.types.conversion_upload_service import (
    CallConversion,
    CustomVariable,
    UploadCallConversionsResponse,
    UploadCallConversionsRequest,
    CallConversionResult,
)

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


# [START upload_call_conversion]
def main(
    client: GoogleAdsClient,
    customer_id: str,
    conversion_action_id: str,
    caller_id: str,
    call_start_date_time: str,
    conversion_date_time: str,
    conversion_value: float,
    conversion_custom_variable_id: Optional[str],
    conversion_custom_variable_value: Optional[str],
    ad_user_data_consent: Optional[str],
):
    """Imports offline call conversion values for calls related to your ads.

    Args:
        client: An initialized GoogleAdsClient instance.
        customer_id: The client customer ID string.
        conversion_action_id: The ID of the conversion action to upload to.
        caller_id: The caller ID from which this call was placed. Caller ID is
            expected to be in E.164 format with preceding '+' sign,
            e.g. '+18005550100'.
        call_start_date_time: The date and time at which the call occurred. The
            format is 'yyyy-mm-dd hh:mm:ss+|-hh:mm',
            e.g. '2021-01-01 12:32:45-08:00'.
        conversion_date_time: The the date and time of the conversion (should be
            after the click time). The format is 'yyyy-mm-dd hh:mm:ss+|-hh:mm',
            e.g. '2021-01-01 12:32:45-08:00'.
        conversion_value: The conversion value in the desired currency.
        conversion_custom_variable_id: The ID of the conversion custom
            variable to associate with the upload.
        conversion_custom_variable_value: The str value of the conversion custom
            variable to associate with the upload.
        ad_user_data_consent: The consent status for ad user data for all
            members in the job.
    """
    # Get the ConversionUploadService client.
    conversion_upload_service: ConversionUploadServiceClient = (
        client.get_service("ConversionUploadService")
    )

    # Create a call conversion in USD currency.
    call_conversion: CallConversion = client.get_type("CallConversion")
    call_conversion.conversion_action = client.get_service(
        "ConversionActionService"
    ).conversion_action_path(customer_id, conversion_action_id)
    call_conversion.caller_id = caller_id
    call_conversion.call_start_date_time = call_start_date_time
    call_conversion.conversion_date_time = conversion_date_time
    call_conversion.conversion_value = conversion_value
    call_conversion.currency_code = "USD"

    if conversion_custom_variable_id and conversion_custom_variable_value:
        conversion_custom_variable: CustomVariable = client.get_type(
            "CustomVariable"
        )
        conversion_custom_variable.conversion_custom_variable = (
            conversion_custom_variable_id
        )
        conversion_custom_variable.value = conversion_custom_variable_value
        call_conversion.custom_variables.append(conversion_custom_variable)

    # Specifies whether user consent was obtained for the data you are
    # uploading. For more details. see:
    # https://www.google.com/about/company/user-consent-policy
    if ad_user_data_consent:
        call_conversion.consent.ad_user_data = client.enums.ConsentStatusEnum[
            ad_user_data_consent
        ]

    # Issue a request to upload the call conversion.
    # Partial failure MUST be enabled for this request.
    request: UploadCallConversionsRequest = client.get_type(
        "UploadCallConversionsRequest"
    )
    request.customer_id = customer_id
    request.conversions = [call_conversion]
    request.partial_failure = True
    # NOTE: This request only uploads a single conversion, but if you have
    # multiple conversions to upload, it's most efficient to upload them in a
    # single request. See the following for per-request limits for reference:
    # https://developers.google.com/google-ads/api/docs/best-practices/quotas#conversion_upload_service
    upload_call_conversions_response: UploadCallConversionsResponse = (
        conversion_upload_service.upload_call_conversions(request=request)
    )

    # Print any partial errors returned.
    if upload_call_conversions_response.partial_failure_error:
        print(
            "Partial error occurred: "
            f"'{upload_call_conversions_response.partial_failure_error.message}'"
        )

    # Print the result if valid.
    uploaded_call_conversion: CallConversionResult = (
        upload_call_conversions_response.results[0]
    )
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
    googleads_client: GoogleAdsClient = GoogleAdsClient.load_from_storage(
        version="v22"
    )

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
        "e.g. '+18005550100'.",
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
        help="The date and time of the conversion (should be after the "
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
    parser.add_argument(
        "-w",
        "--conversion_custom_variable_id",
        type=str,
        help="The ID of the conversion custom variable to associate with the upload.",
    )
    parser.add_argument(
        "-x",
        "--conversion_custom_variable_value",
        type=str,
        help="The value of the conversion custom variable to associate with the upload.",
    )
    parser.add_argument(
        "-d",
        "--ad_user_data_consent",
        type=str,
        choices=[
            e.name
            for e in googleads_client.enums.ConsentStatusEnum
            if e.name not in ("UNSPECIFIED", "UNKNOWN")
        ],
        help=(
            "The data consent status for ad user data for all members in "
            "the job."
        ),
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
            args.conversion_custom_variable_id,
            args.conversion_custom_variable_value,
            args.ad_user_data_consent,
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
