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

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


# [START upload_conversion_adjustment]
def main(
    client,
    customer_id,
    conversion_action_id,
    gclid,
    adjustment_type,
    conversion_date_time,
    adjustment_date_time,
    restatement_value,
):
    conversion_adjustment_type_enum = client.get_type(
        "ConversionAdjustmentTypeEnum"
    )
    # Determine the adjustment type.
    conversion_adjustment_type = conversion_adjustment_type_enum._pb.ConversionAdjustmentType.Value(
        adjustment_type
    )

    # Associates conversion adjustments with the existing conversion action.
    # The GCLID should have been uploaded before with a conversion
    conversion_adjustment = client.get_type("ConversionAdjustment")
    conversion_action_service = client.get_service("ConversionActionService")
    conversion_adjustment.conversion_action = conversion_action_service.conversion_action_path(
        customer_id, conversion_action_id
    )
    conversion_adjustment.adjustment_type = conversion_adjustment_type
    conversion_adjustment.adjustment_date_time = adjustment_date_time

    # Set the Gclid Date
    conversion_adjustment.gclid_date_time_pair.gclid = gclid
    conversion_adjustment.gclid_date_time_pair.conversion_date_time = (
        conversion_date_time
    )

    # Sets adjusted value for adjustment type RESTATEMENT.
    if (
        restatement_value
        and conversion_adjustment_type
        == conversion_adjustment_type_enum.ConversionAdjustmentType.RESTATEMENT
    ):
        conversion_adjustment.restatement_value.adjusted_value = float(
            restatement_value
        )

    conversion_adjustment_upload_service = client.get_service(
        "ConversionAdjustmentUploadService"
    )
    request = client.get_type("UploadConversionAdjustmentsRequest")
    request.customer_id = customer_id
    request.conversion_adjustments = [conversion_adjustment]
    request.partial_failure = True
    response = conversion_adjustment_upload_service.upload_conversion_adjustments(
        request=request,
    )
    conversion_adjustment_result = response.results[0]
    print(
        f"Uploaded conversion that occurred at "
        f'"{conversion_adjustment_result.adjustment_date_time}" '
        f"from Gclid "
        f'"{conversion_adjustment_result.gclid_date_time_pair.gclid}"'
        f' to "{conversion_adjustment_result.conversion_action}"'
    )
    # [END upload_conversion_adjustment]


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v8")

    parser = argparse.ArgumentParser(
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
        help="The conversion action ID to be " "uploaded to.",
    )
    parser.add_argument(
        "-g",
        "--gclid",
        type=str,
        required=True,
        help="The Google Click Identifier ID.",
    )
    parser.add_argument(
        "-d",
        "--adjustment_type",
        type=str,
        required=True,
        choices=googleads_client.get_type(
            "ConversionAdjustmentTypeEnum"
        )._pb.ConversionAdjustmentType.keys(),
        help="The Adjustment type, e.g. " "RETRACTION, RESTATEMENT",
    )
    parser.add_argument(
        "-t",
        "--conversion_date_time",
        type=str,
        required=True,
        help="The the date and time of the "
        "conversion. The format is "
        '"yyyy-mm-dd hh:mm:ss+|-hh:mm", e.g. '
        "“2019-01-01 12:32:45-08:00”",
    )
    parser.add_argument(
        "-v",
        "--adjustment_date_time",
        type=str,
        required=True,
        help="The the date and time of the "
        "adjustment. The format is "
        '"yyyy-mm-dd hh:mm:ss+|-hh:mm", e.g. '
        "“2019-01-01 12:32:45-08:00”",
    )
    # Optional: Specify an adjusted value for adjustment type RESTATEMENT.
    # This value will be ignored if you specify RETRACTION as adjustment type.
    parser.add_argument(
        "-r",
        "--restatement_value",
        type=str,
        required=False,
        help="The adjusted value for " "adjustment type RESTATEMENT.",
    )
    args = parser.parse_args()

    try:
        main(
            googleads_client,
            args.customer_id,
            args.conversion_action_id,
            args.gclid,
            args.adjustment_type,
            args.conversion_date_time,
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
