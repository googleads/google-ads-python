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
from typing import Optional

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.ads.googleads.v22.services.services.conversion_action_service import (
    ConversionActionServiceClient,
)
from google.ads.googleads.v22.services.services.conversion_upload_service import (
    ConversionUploadServiceClient,
)
from google.ads.googleads.v22.services.types.conversion_upload_service import (
    ClickConversion,
    ClickConversionResult,
    CustomVariable,
    UploadClickConversionsRequest,
    UploadClickConversionsResponse,
)


# [START upload_offline_conversion]
def main(
    client: GoogleAdsClient,
    customer_id: str,
    conversion_action_id: str,
    gclid: Optional[str],
    conversion_date_time: str,
    conversion_value: str,
    conversion_custom_variable_id: Optional[str],
    conversion_custom_variable_value: Optional[str],
    gbraid: Optional[str],
    wbraid: Optional[str],
    order_id: Optional[str],
    ad_user_data_consent: Optional[str],
) -> None:
    """Creates a click conversion with a default currency of USD.

    Args:
        client: An initialized GoogleAdsClient instance.
        customer_id: The client customer ID string.
        conversion_action_id: The ID of the conversion action to upload to.
        gclid: The Google Click Identifier ID. If set, the wbraid and gbraid
            parameters must be None.
        conversion_date_time: The the date and time of the conversion (should be
            after the click time). The format is 'yyyy-mm-dd hh:mm:ss+|-hh:mm',
            e.g. '2021-01-01 12:32:45-08:00'.
        conversion_value: The conversion value in the desired currency.
        conversion_custom_variable_id: The ID of the conversion custom
            variable to associate with the upload.
        conversion_custom_variable_value: The str value of the conversion custom
            variable to associate with the upload.
        gbraid: The GBRAID for the iOS app conversion. If set, the gclid and
            wbraid parameters must be None.
        wbraid: The WBRAID for the iOS app conversion. If set, the gclid and
            gbraid parameters must be None.
        order_id: The order ID for the click conversion.
        ad_user_data_consent: The ad user data consent for the click.
    """
    click_conversion: ClickConversion = client.get_type("ClickConversion")
    conversion_upload_service: ConversionUploadServiceClient = (
        client.get_service("ConversionUploadService")
    )
    conversion_action_service: ConversionActionServiceClient = (
        client.get_service("ConversionActionService")
    )
    click_conversion.conversion_action = (
        conversion_action_service.conversion_action_path(
            customer_id, conversion_action_id
        )
    )

    # Sets the single specified ID field.
    if gclid:
        click_conversion.gclid = gclid
    elif gbraid:
        click_conversion.gbraid = gbraid
    else:
        click_conversion.wbraid = wbraid

    click_conversion.conversion_value = float(conversion_value)
    click_conversion.conversion_date_time = conversion_date_time
    click_conversion.currency_code = "USD"

    if conversion_custom_variable_id and conversion_custom_variable_value:
        conversion_custom_variable: CustomVariable = client.get_type(
            "CustomVariable"
        )
        conversion_custom_variable.conversion_custom_variable = (
            conversion_upload_service.conversion_custom_variable_path(
                customer_id, conversion_custom_variable_id
            )
        )
        conversion_custom_variable.value = conversion_custom_variable_value
        click_conversion.custom_variables.append(conversion_custom_variable)

    if order_id:
        click_conversion.order_id = order_id

    # Sets the consent information, if provided.
    if ad_user_data_consent:
        # Specifies whether user consent was obtained for the data you are
        # uploading. For more details, see:
        # https://www.google.com/about/company/user-consent-policy
        click_conversion.consent.ad_user_data = client.enums.ConsentStatusEnum[
            ad_user_data_consent
        ]

    # Uploads the click conversion. Partial failure must be set to True here.
    #
    # NOTE: This request only uploads a single conversion, but if you have
    # multiple conversions to upload, it's most efficient to upload them in a
    # single request. See the following for per-request limits for reference:
    # https://developers.google.com/google-ads/api/docs/best-practices/quotas#conversion_upload_service
    request: UploadClickConversionsRequest = client.get_type(
        "UploadClickConversionsRequest"
    )
    request.customer_id = customer_id
    request.conversions.append(click_conversion)
    request.partial_failure = True
    conversion_upload_response: UploadClickConversionsResponse = (
        conversion_upload_service.upload_click_conversions(
            request=request,
        )
    )
    uploaded_click_conversion: ClickConversionResult = (
        conversion_upload_response.results[0]
    )
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
    googleads_client: GoogleAdsClient = GoogleAdsClient.load_from_storage(
        version="v22"
    )

    parser: argparse.ArgumentParser = argparse.ArgumentParser(
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
        "-t",
        "--conversion_date_time",
        type=str,
        required=True,
        help="The date and time of the "
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
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-g",
        "--gclid",
        type=str,
        help="The Google Click Identifier (gclid) which should be newer than "
        "the number of days set on the conversion window of the conversion "
        "action. Only one of either a gclid, WBRAID, or GBRAID identifier can "
        "be passed into this example. See the following for more details: "
        "https://developers.google.com/google-ads/api/docs/conversions/upload-clicks",
    )
    group.add_argument(
        "-b",
        "--gbraid",
        type=str,
        help="The GBRAID identifier for an iOS app conversion. Only one of "
        "either a gclid, WBRAID, or GBRAID identifier can be passed into this "
        "example. See the following for more details: "
        "https://developers.google.com/google-ads/api/docs/conversions/upload-clicks",
    )
    group.add_argument(
        "-d",
        "--wbraid",
        type=str,
        help="The WBRAID identifier for an iOS app conversion. Only one of "
        "either a gclid, WBRAID, or GBRAID identifier can be passed into this "
        "example. See the following for more details: "
        "https://developers.google.com/google-ads/api/docs/conversions/upload-clicks",
    )
    parser.add_argument(
        "-o",
        "--order_id",
        type=str,
        help="The order ID for the click conversion.",
    )
    parser.add_argument(
        "-s",
        "--ad_user_data_consent",
        type=str,
        choices=[
            e.name
            for e in googleads_client.enums.ConsentStatusEnum
            if e.name not in ("UNSPECIFIED", "UNKNOWN")
        ],
        help=("The ad user data consent for the click."),
    )
    args: argparse.Namespace = parser.parse_args()

    try:
        main(
            googleads_client,
            args.customer_id,
            args.conversion_action_id,
            args.gclid,
            args.conversion_date_time,
            args.conversion_value,
            args.conversion_custom_variable_id,
            args.conversion_custom_variable_value,
            args.gbraid,
            args.wbraid,
            args.order_id,
            args.ad_user_data_consent,
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
