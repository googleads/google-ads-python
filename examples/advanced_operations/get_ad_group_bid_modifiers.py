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
"""This example illustrates how to retrieve ad group bid modifiers."""

import argparse
import sys
from typing import Optional

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.ads.googleads.v26.resources.types.ad_group_bid_modifier import (
    AdGroupBidModifier,
)
from google.ads.googleads.v26.services.services.google_ads_service import (
    GoogleAdsServiceClient,
)
from google.ads.googleads.v26.services.types.google_ads_service import (
    GoogleAdsRow,
    SearchGoogleAdsRequest,
    SearchGoogleAdsResponse,
)


def main(
    client: GoogleAdsClient, customer_id: str, ad_group_id: Optional[str] = None
) -> None:
    ga_service: GoogleAdsServiceClient = client.get_service("GoogleAdsService")

    query: str = """
        SELECT
          campaign.id,
          ad_group.id,
          ad_group_bid_modifier.criterion_id,
          ad_group_bid_modifier.bid_modifier,
          ad_group_bid_modifier.device.type,
          ad_group_bid_modifier.user_set_dates.type,
          ad_group_bid_modifier.advance_booking_window.min_days,
          ad_group_bid_modifier.advance_booking_window.max_days,
          ad_group_bid_modifier.length_of_booking.min_days,
          ad_group_bid_modifier.length_of_booking.max_days,
          ad_group_bid_modifier.start_day_of_week.day_of_week,
          ad_group_bid_modifier.start_date_range.start_date,
          ad_group_bid_modifier.start_date_range.end_date
        FROM ad_group_bid_modifier"""

    if ad_group_id:
        query += f" WHERE ad_group.id = {ad_group_id}"

    # Limit results to 10,000 rows as the number of bid modifiers can be large.
    query += " LIMIT 10000"

    search_request: SearchGoogleAdsRequest = client.get_type(
        "SearchGoogleAdsRequest"
    )
    search_request.customer_id = customer_id
    search_request.query = query

    results: SearchGoogleAdsResponse = ga_service.search(request=search_request)

    row: GoogleAdsRow
    for row in results:
        modifier: AdGroupBidModifier = row.ad_group_bid_modifier
        print(
            "Ad group bid modifier with criterion ID "
            f"'{modifier.criterion_id}', bid modifier value "
            f"'{modifier.bid_modifier or 0.00}', device type "
            f"'{modifier.device.type_.name}' was found in ad group with ID "
            f"'{row.ad_group.id}' of campaign with ID '{row.campaign.id}'."
        )

        criterion_field: str = (
            type(modifier).pb(modifier).WhichOneof("criterion")
        )
        criterion_details: str = f"  - Criterion type: {criterion_field}, "

        if criterion_field == "device":
            criterion_details += f"Type: {modifier.device.type_}"
        elif criterion_field == "advance_booking_window":
            criterion_details += (
                f"Min Days: {modifier.advance_booking_window.min_days}, "
                f"Max Days: {modifier.advance_booking_window.max_days}"
            )
        elif criterion_field == "start_day_of_week":
            criterion_details += (
                f"Day of the week: {modifier.start_day_of_week.day_of_week}"
            )
        elif criterion_field == "user_set_dates":
            criterion_details += (
                f"Date selection type: {modifier.user_set_dates.type_}"
            )
        elif criterion_field == "length_of_booking":
            criterion_details += (
                f"Min Days: {modifier.length_of_booking.min_days}, "
                f"Max Days: {modifier.length_of_booking.max_days}"
            )
        elif criterion_field == "start_date_range":
            criterion_details += (
                f"Start Date: {modifier.start_date_range.start_date}, "
                f"End Date: {modifier.start_date_range.end_date}"
            )
        else:
            criterion_details = "  - No Criterion type found."

        print(criterion_details)


if __name__ == "__main__":
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="List ad group bid modifiers for specified customer."
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
        required=False,
        help=(
            "The ad group ID. Specify this to list ad group "
            "bid modifiers solely for this ad group ID."
        ),
    )
    args: argparse.Namespace = parser.parse_args()

    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client: GoogleAdsClient = GoogleAdsClient.load_from_storage(
        version="v26"
    )

    try:
        main(
            googleads_client,
            args.customer_id,
            ad_group_id=args.ad_group_id,
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
