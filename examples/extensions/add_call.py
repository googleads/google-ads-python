#!/usr/bin/env python
# Copyright 2022 Google LLC
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
"""This example adds a call extension to a specific account."""


import argparse
import sys

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

# Country code is a two-letter ISO-3166 code, for a list of all codes see:
# https://developers.google.com/google-ads/api/reference/data/codes-formats#expandable-17
_DEFAULT_PHONE_COUNTRY = "US"


def main(
    client, customer_id, phone_number, phone_country, conversion_action_id
):
    """The main method that creates all necessary entities for the example.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        phone_number: a phone number for your business, e.g. '(123) 456-7890'.
        phone_country: a two-letter ISO-3166 code.
        conversion_action_id: an ID for a conversion action.
    """
    asset_resource_name = _add_extension_asset(
        client, customer_id, phone_number, phone_country, conversion_action_id
    )
    _link_asset_to_account(client, customer_id, asset_resource_name)


def _add_extension_asset(
    client, customer_id, phone_number, phone_country, conversion_action_id
):
    """Creates a new asset for the call.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        phone_number: a phone number for your business, e.g. '(123) 456-7890'.
        phone_country: a two-letter ISO-3166 code.
        conversion_action_id: an ID for a conversion action.

    Returns:
        a resource name for a new call asset.
    """
    operation = client.get_type("AssetOperation")
    # Creates the call asset.
    asset = operation.create.call_asset
    asset.country_code = phone_country
    asset.phone_number = phone_number
    # Optional: Specifies day and time intervals for which the asset may serve.
    ad_schedule = client.get_type("AdScheduleInfo")
    # Sets the day of this schedule as Monday.
    ad_schedule.day_of_week = client.enums.DayOfWeekEnum.MONDAY
    # Sets the start hour to 9am.
    ad_schedule.start_hour = 9
    # Sets the end hour to 5pm.
    ad_schedule.end_hour = 17
    # Sets the start and end minute of zero, for example: 9:00 and 5:00.
    ad_schedule.start_minute = client.enums.MinuteOfHourEnum.ZERO
    ad_schedule.end_minute = client.enums.MinuteOfHourEnum.ZERO
    # Appends the ad schedule to the list of ad schedule targets on the asset.
    asset.ad_schedule_targets.append(ad_schedule)

    # Sets the conversion action ID if provided.
    if conversion_action_id:
        googleads_service = client.get_service("GoogleAdsService")
        asset.call_conversion_action = googleads_service.conversion_action_path(
            customer_id, conversion_action_id
        )
        asset.call_conversion_reporting_state = (
            client.enums.CallConversionReportingStateEnum.USE_RESOURCE_LEVEL_CALL_CONVERSION_ACTION
        )

    # Issues a mutate request to add the asset.
    asset_service = client.get_service("AssetService")
    response = asset_service.mutate_assets(
        customer_id=customer_id, operations=[operation]
    )
    resource_name = response.results[0].resource_name
    print(f"Created a call asset with resource name: '{resource_name}'")

    return resource_name


def _link_asset_to_account(client, customer_id, asset_resource_name):
    """Links the call asset at the account level to serve in eligible campaigns.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        asset_resource_name: a resource name for the call asset.
    """
    operation = client.get_type("CustomerAssetOperation")
    customer_asset = operation.create
    customer_asset.asset = asset_resource_name
    customer_asset.field_type = client.enums.AssetFieldTypeEnum.CALL

    customer_asset_service = client.get_service("CustomerAssetService")
    response = customer_asset_service.mutate_customer_assets(
        customer_id=customer_id, operations=[operation]
    )
    resource_name = response.results[0].resource_name
    print(f"Created a customer asset with resource name: '{resource_name}'")


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v10")

    parser = argparse.ArgumentParser(
        description=("Adds a call extension to a specific account.")
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
        "-n",
        "--phone_number",
        type=str,
        required=True,
        help=("A phone number for your business, e.g. '(123) 456-7890'"),
    )
    parser.add_argument(
        "-p",
        "--phone_country",
        type=str,
        default=_DEFAULT_PHONE_COUNTRY,
        help=(
            "A two-letter ISO-3166 code representing a country code, for a "
            "list of all codes see: "
            "https://developers.google.com/google-ads/api/reference/data/codes-formats#expandable-17"
        ),
    )
    parser.add_argument(
        "-v",
        "--conversion_action_id",
        type=str,
        help=("An optional conversion action ID to attribute conversions to."),
    )

    args = parser.parse_args()

    try:
        main(
            googleads_client,
            args.customer_id,
            args.phone_number,
            args.phone_country,
            args.conversion_action_id,
        )
    except GoogleAdsException as ex:
        print(
            f'Request with ID "{ex.request_id}" failed with status '
            f'"{ex.error.code().name}" and includes the following errors:'
        )
        for error in ex.failure.errors:
            print(f'Error with message "{error.message}".')
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print(f"\t\tOn field: {field_path_element.field_name}")
        sys.exit(1)
