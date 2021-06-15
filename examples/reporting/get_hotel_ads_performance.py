#!/usr/bin/env python
# Copyright 2019 Google LLC
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
"""Demonstrates how to request Hotel ad performance statistics.

This example gets Hotel ads performance statistics for the 50 Hotel ad
groups with the most impressions over the last 7 days.
"""


import argparse
import sys

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


def main(client, customer_id):
    ga_service = client.get_service("GoogleAdsService")

    query = """
        SELECT
          campaign.id,
          campaign.advertising_channel_type,
          ad_group.id,
          ad_group.status,
          metrics.impressions,
          metrics.hotel_average_lead_value_micros,
          segments.hotel_check_in_day_of_week,
          segments.hotel_length_of_stay
        FROM hotel_performance_view
        WHERE segments.date DURING LAST_7_DAYS
        AND campaign.advertising_channel_type = 'HOTEL'
        AND ad_group.status = 'ENABLED'
        ORDER BY metrics.impressions DESC
        LIMIT 50"""

    search_request = client.get_type("SearchGoogleAdsStreamRequest")
    search_request.customer_id = customer_id
    search_request.query = query

    response = ga_service.search_stream(search_request)

    for batch in response:
        for row in batch.results:
            campaign = row.campaign
            ad_group = row.ad_group
            hotel_check_in_day_of_week = row.segments.hotel_check_in_day_of_week
            hotel_length_of_stay = row.segments.hotel_length_of_stay
            metrics = row.metrics

            print(
                f'Ad group ID "{ad_group.id}" '
                f'in campaign ID "{campaign.id}" '
            )
            print(
                f'with hotel check-in on "{hotel_check_in_day_of_week}" '
                f'and "{hotel_length_of_stay}" day(s) stay '
            )
            print(
                f"had {metrics.impressions:d} impression(s) and "
                f"{metrics.hotel_average_lead_value_micros:d} average "
                "lead value (in micros) during the last 7 days.\n"
            )


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v8")

    parser = argparse.ArgumentParser(
        description=("Retrieves Hotel-ads performance statistics.")
    )
    # The following argument(s) should be provided to run the example.
    parser.add_argument(
        "-c",
        "--customer_id",
        type=str,
        required=True,
        help="The Google Ads customer ID.",
    )
    args = parser.parse_args()

    try:
        main(googleads_client, args.customer_id)
    except GoogleAdsException as ex:
        print(
            f'Request with ID "{ex.request_id}" failed with status '
            f'"{ex.error.code().name}" and includes the following errors:'
        )
        for error in ex.failure.errors:
            print(f'	Error with message "{error.message}".')
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print(f"\t\tOn field: {field_path_element.field_name}")
        sys.exit(1)
