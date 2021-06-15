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
"""Gets available ad group criterion CPC bid simulations for a given ad group.

To get ad groups, run get_ad_groups.py.
"""


import argparse
import sys

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


# [START get_ad_group_criterion_cpc_bid_simulations]
def main(client, customer_id, ad_group_id):
    googleads_service = client.get_service("GoogleAdsService")

    query = f"""
        SELECT
          ad_group_criterion_simulation.ad_group_id,
          ad_group_criterion_simulation.criterion_id,
          ad_group_criterion_simulation.start_date,
          ad_group_criterion_simulation.end_date,
          ad_group_criterion_simulation.cpc_bid_point_list.points
        FROM ad_group_criterion_simulation
        WHERE
          ad_group_criterion_simulation.type = CPC_BID
          AND ad_group_criterion_simulation.ad_group_id = {ad_group_id}"""

    # Issues a search request using streaming.
    response = googleads_service.search_stream(
        customer_id=customer_id, query=query
    )

    # Iterates over all rows in all messages and prints the requested field
    # values for the ad group criterion CPC bid simulation in each row.
    for batch in response:
        for row in batch.results:
            simulation = row.ad_group_criterion_simulation

            print(
                "found ad group criterion CPC bid simulation for "
                f"ad group ID {simulation.ad_group_id}, "
                f"criterion ID {simulation.criterion_id}, "
                f"start date {simulation.start_date}, "
                f"end date {simulation.end_date}"
            )

            for point in simulation.cpc_bid_point_list.points:
                print(
                    f"\tbid: {point.cpc_bid_micros} => "
                    f"clicks: {point.clicks}",
                    f"cost: {point.cost_micros}, "
                    f"impressions: {point.impressions},"
                    "biddable conversions: "
                    f"{point.biddable_conversions},"
                    f"biddable conversions value: "
                    f"{point.biddable_conversions_value}",
                )

            print()
            # [END get_ad_group_criterion_cpc_bid_simulations]


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v8")

    parser = argparse.ArgumentParser(
        description="Gets all available ad group criterion CPC bid "
        "simulations for a given ad group."
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
        help="The ad group ID for which to get available bid simulations.",
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
