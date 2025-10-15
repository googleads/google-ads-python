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
from typing import Optional, Iterable

from google.protobuf.any_pb2 import Any

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.ads.googleads.v22.enums.types.conversion_adjustment_type import (
    ConversionAdjustmentTypeEnum,
)
from google.ads.googleads.v22.errors.types.errors import (
    GoogleAdsError,
    GoogleAdsFailure,
)
from google.ads.googleads.v22.services.services.conversion_action_service import (
    ConversionActionServiceClient,
)
from google.ads.googleads.v22.services.services.conversion_adjustment_upload_service import (
    ConversionAdjustmentUploadServiceClient,
)
from google.ads.googleads.v22.services.types.conversion_adjustment_upload_service import (
    ConversionAdjustment,
    ConversionAdjustmentResult,
    UploadConversionAdjustmentsRequest,
    UploadConversionAdjustmentsResponse,
)


# [START upload_conversion_adjustment]
def main(
    client: GoogleAdsClient,
    customer_id: str,
    conversion_action_id: str,
    adjustment_type: str,
    order_id: str,
    adjustment_date_time: str,
    restatement_value: Optional[str] = None,
) -> None:
    """The main method that creates all necessary entities for the example.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        conversion_action_id: the ID of the conversion action to upload the
            adjustment to.
        adjustment_type: the adjustment type, e.g. " "RETRACTION, RESTATEMENT.
        order_id: the transaction ID of the conversion to adjust. Strongly
            recommended instead of using gclid and conversion_date_time.
        adjustment_date_time: the date and time of the adjustment.
        restatement_value: the adjusted value for adjustment type RESTATEMENT.
    """
    conversion_adjustment_type_enum: ConversionAdjustmentTypeEnum = (
        client.enums.ConversionAdjustmentTypeEnum
    )
    # Determine the adjustment type.
    conversion_adjustment_type: int = conversion_adjustment_type_enum[
        adjustment_type
    ].value

    # Applies the conversion adjustment to the existing conversion.
    conversion_adjustment: ConversionAdjustment = client.get_type(
        "ConversionAdjustment"
    )
    conversion_action_service: ConversionActionServiceClient = (
        client.get_service("ConversionActionService")
    )
    conversion_adjustment.conversion_action = (
        conversion_action_service.conversion_action_path(
            customer_id, conversion_action_id
        )
    )
    conversion_adjustment.adjustment_type = conversion_adjustment_type
    conversion_adjustment.adjustment_date_time = adjustment_date_time

    # Sets the order_id to identify the conversion to adjust.
    conversion_adjustment.order_id = order_id

    # As an alternative to setting order_id, you can provide a
    # gclid_date_time_pair, but setting order_id instead is strongly recommended.
    # conversion_adjustment.gclid_date_time_pair.gclid = gclid
    # conversion_adjustment.gclid_date_time_pair.conversion_date_time = (
    #     conversion_date_time
    # )

    # Sets adjusted value for adjustment type RESTATEMENT.
    if (
        restatement_value
        and conversion_adjustment_type
        == conversion_adjustment_type_enum.RESTATEMENT.value
    ):
        conversion_adjustment.restatement_value.adjusted_value = float(
            restatement_value
        )

    # Uploads the click conversion. Partial failure should always be set to
    # true.
    service: ConversionAdjustmentUploadServiceClient = client.get_service(
        "ConversionAdjustmentUploadService"
    )
    request: UploadConversionAdjustmentsRequest = client.get_type(
        "UploadConversionAdjustmentsRequest"
    )
    request.customer_id = customer_id
    request.conversion_adjustments.append(conversion_adjustment)
    # Enables partial failure (must be true)
    request.partial_failure = True

    response: UploadConversionAdjustmentsResponse = (
        service.upload_conversion_adjustments(request=request)
    )

    # Extracts the partial failure error if present on the response.
    error_details = None
    if response.partial_failure_error:
        error_details: Iterable[Any] = response.partial_failure_error.details

    i: int
    conversion_adjustment_result: ConversionAdjustmentResult
    for i, conversion_adjustment_result in enumerate(response.results):
        # If there's a GoogleAdsFailure in error_details at this position then
        # the uploaded operation failed and we print the error message.
        if error_details and error_details[i]:
            error_detail: Any = error_details[i]
            failure_message: GoogleAdsFailure = client.get_type(
                "GoogleAdsFailure"
            )
            # Parse the string into a GoogleAdsFailure message instance.
            # To access class-only methods on the message we retrieve its type.
            google_ads_failure_class: GoogleAdsFailure = type(failure_message)
            failure_object: GoogleAdsFailure = (
                google_ads_failure_class.deserialize(error_detail.value)
            )

            error: GoogleAdsError
            for error in failure_object.errors:
                # Construct and print a string that details which element in
                # the operation list failed (by index number) as well as the
                # error message and error code.
                print(
                    "A partial failure at index "
                    f"{error.location.field_path_elements[0].index} occurred "
                    f"\nError message: {error.message}\nError code: "
                    f"{error.error_code}"
                )
        else:
            print(
                "Uploaded conversion adjustment for conversion action "
                f"'{conversion_adjustment_result.conversion_action}' and order "
                f"ID '{conversion_adjustment_result.order_id}'."
            )
            # [END upload_conversion_adjustment]


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client: GoogleAdsClient = GoogleAdsClient.load_from_storage(
        version="v22"
    )

    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Uploads a conversion adjustment."
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
        help="The ID of the conversion action to upload the adjustment to.",
    )
    parser.add_argument(
        "-d",
        "--adjustment_type",
        type=str,
        required=True,
        choices=[
            e.name
            for e in googleads_client.enums.ConversionAdjustmentTypeEnum
            if e.name not in ("UNSPECIFIED", "UNKNOWN")
        ],
        help="The adjustment type, e.g. " "RETRACTION, RESTATEMENT",
    )
    parser.add_argument(
        "-o",
        "--order_id",
        type=str,
        required=True,
        help=(
            "The transaction ID of the conversion to adjust. Required if the "
            "conversion being adjusted meets the criteria described at: "
            "https://developers.google.com/google-ads/api/docs/conversions/upload-adjustments#requirements."
        ),
    )
    parser.add_argument(
        "-v",
        "--adjustment_date_time",
        type=str,
        required=True,
        help=(
            "The date and time of the adjustment. The format is "
            "'yyyy-mm-dd hh:mm:ss+|-hh:mm', e.g. '2019-01-01 12:32:45-08:00'"
        ),
    )
    # Optional: Specify an adjusted value for adjustment type RESTATEMENT.
    # This value will be ignored if you specify RETRACTION as adjustment type.
    parser.add_argument(
        "-r",
        "--restatement_value",
        type=str,
        required=False,
        help="The adjusted value for adjustment type RESTATEMENT.",
    )
    args: argparse.Namespace = parser.parse_args()

    try:
        main(
            googleads_client,
            args.customer_id,
            args.conversion_action_id,
            args.adjustment_type,
            args.order_id,
            args.adjustment_date_time,
            args.restatement_value,
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
