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
"""This example adds an ad group bid modifier to a hotel ad group.

The bid modifiers will be based on hotel check-in day and length of stay.
"""


import argparse
import sys

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


# [START add_hotel_ad_group_bid_modifiers]
def main(client, customer_id, ad_group_id):
    ad_group_service = client.get_service("AdGroupService")
    ag_bm_service = client.get_service("AdGroupBidModifierService")

    # Create ad group bid modifier based on hotel check-in day.
    check_in_ag_bm_operation = client.get_type("AdGroupBidModifierOperation")
    check_in_ag_bid_modifier = check_in_ag_bm_operation.create
    check_in_ag_bid_modifier.hotel_check_in_day.day_of_week = client.get_type(
        "DayOfWeekEnum"
    ).DayOfWeek.MONDAY
    check_in_ag_bid_modifier.ad_group = ad_group_service.ad_group_path(
        customer_id, ad_group_id
    )
    # Sets the bid modifier value to 150%.
    check_in_ag_bid_modifier.bid_modifier = 1.5

    # Create ad group bid modifier based on hotel length of stay info.
    los_ag_bm_operation = client.get_type("AdGroupBidModifierOperation")
    los_ag_bid_modifier = los_ag_bm_operation.create
    los_ag_bid_modifier.ad_group = ad_group_service.ad_group_path(
        customer_id, ad_group_id
    )
    # Creates the hotel length of stay info.
    hotel_length_of_stay_info = los_ag_bid_modifier.hotel_length_of_stay
    hotel_length_of_stay_info.min_nights = 3
    hotel_length_of_stay_info.max_nights = 7
    # Sets the bid modifier value to 170%.
    los_ag_bid_modifier.bid_modifier = 1.7

    # Add the bid modifiers
    ag_bm_response = ag_bm_service.mutate_ad_group_bid_modifiers(
        customer_id=customer_id,
        operations=[check_in_ag_bm_operation, los_ag_bm_operation],
    )

    # Print out resource names of the added ad group bid modifiers.
    print(f"Added {len(ag_bm_response.results)} hotel ad group bid modifiers:")

    for result in ag_bm_response.results:
        print(result.resource_name)
        # [END add_hotel_ad_group_bid_modifiers]


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v8")

    parser = argparse.ArgumentParser(
        description=("Adds an ad group bid modifier to a hotel ad group.")
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
        "--ad_group_id",
        type=str,
        required=True,
        help="The ad group ID of the hotel ad group.",
    )
    args = parser.parse_args()

    try:
        main(googleads_client, args.customer_id, args.ad_group_id)
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
