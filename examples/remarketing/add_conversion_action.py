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


import argparse
import sys
import uuid

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.ads.googleads.v22.resources.types.conversion_action import (
    ConversionAction,
)
from google.ads.googleads.v22.services.services.conversion_action_service import (
    ConversionActionServiceClient,
)
from google.ads.googleads.v22.services.types.conversion_action_service import (
    ConversionActionOperation,
    MutateConversionActionsResponse,
)


# [START add_conversion_action]
def main(client: GoogleAdsClient, customer_id: str) -> None:
    conversion_action_service: ConversionActionServiceClient = (
        client.get_service("ConversionActionService")
    )

    # Create the operation.
    conversion_action_operation: ConversionActionOperation = client.get_type(
        "ConversionActionOperation"
    )

    # Create conversion action.
    conversion_action: ConversionAction = conversion_action_operation.create

    # Note that conversion action names must be unique. If a conversion action
    # already exists with the specified conversion_action_name, the create
    # operation will fail with a ConversionActionError.DUPLICATE_NAME error.
    conversion_action.name = f"Earth to Mars Cruises Conversion {uuid.uuid4()}"
    conversion_action.type_ = (
        client.enums.ConversionActionTypeEnum.UPLOAD_CLICKS
    )
    conversion_action.category = (
        client.enums.ConversionActionCategoryEnum.DEFAULT
    )
    conversion_action.status = client.enums.ConversionActionStatusEnum.ENABLED
    conversion_action.view_through_lookback_window_days = 15

    # Create a value settings object.
    value_settings: ConversionAction.ValueSettings = (
        conversion_action.value_settings
    )
    value_settings.default_value = 15.0
    value_settings.always_use_default_value = True

    # Add the conversion action.
    conversion_action_response: MutateConversionActionsResponse = (
        conversion_action_service.mutate_conversion_actions(
            customer_id=customer_id,
            operations=[conversion_action_operation],
        )
    )

    print(
        "Created conversion action "
        f'"{conversion_action_response.results[0].resource_name}".'
    )
    # [END add_conversion_action]


if __name__ == "__main__":
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Adds a conversion action for specified customer."
    )
    # The following argument(s) should be provided to run the example.
    parser.add_argument(
        "-c",
        "--customer_id",
        type=str,
        required=True,
        help="The Google Ads customer ID.",
    )
    args: argparse.Namespace = parser.parse_args()

    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client: GoogleAdsClient = GoogleAdsClient.load_from_storage(
        version="v22"
    )

    try:
        main(googleads_client, args.customer_id)
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
