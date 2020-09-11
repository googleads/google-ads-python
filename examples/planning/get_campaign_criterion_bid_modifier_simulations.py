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
"""Gets all available criterion bid modifier simulations for a given campaign.

To get campaigns, run get_campaigns.py.
"""


import argparse
import sys

from google.ads.google_ads.client import GoogleAdsClient
from google.ads.google_ads.errors import GoogleAdsException


def main(client, customer_id, campaign_id):
    """Gets all available criterion bid modifier simulations for a campaign.

    Args:
      client: The Google Ads client.
      customer_id: The customer ID for which to get the simulations.
      campaign_id: The campaign ID from which to get the simulations.
    """
    google_ads_service = client.get_service("GoogleAdsService", version="v5")

    query = f"""
        SELECT
          campaign_criterion_simulation.criterion_id,
          campaign_criterion_simulation.start_date,
          campaign_criterion_simulation.end_date,
          campaign_criterion_simulation.bid_modifier_point_list.points
        FROM campaign_criterion_simulation
        WHERE
          campaign_criterion_simulation.type = BID_MODIFIER
          AND campaign_criterion_simulation.campaign_id = {campaign_id}"""

    try:
        # Issues a search request using streaming.
        response = google_ads_service.search_stream(customer_id, query=query)

        # Iterates over all rows in all messages and prints the requested field
        # values for the ad group criterion CPC bid simulation in each row.
        for batch in response:
            for row in batch.results:
                simulation = row.campaign_criterion_simulation

                print(
                    "Found campaign-level criterion bid modifier simulation "
                    f"for criterion with ID {simulation.criterion_id}, start "
                    f"date {simulation.start_date}, end date "
                    f"{simulation.end_date}, and points:"
                )

                for point in simulation.bid_modifier_point_list.points:
                    print(
                        f"\tbid modifier: {'{point.bid_modifier:.2f}'} "
                        f"=> clicks: {point.clicks}, "
                        f"cost: {point.cost_micros}, "
                        f"impressions: {point.impressions}, "
                        f"parent clicks: {point.parent_clicks}, "
                        f"parent cost: {point.parent_cost_micros}, "
                        f"parent impressions: {point.parent_impressions}, "
                        "parent required budget: "
                        f"{point.parent_required_budget_micros}",
                    )

                print()

    except GoogleAdsException as ex:
        print(
            f"Request with ID '{ex.request_id}' failed with status "
            f"'{ex.error.code().name}' and includes the following errors:"
        )
        for error in ex.failure.errors:
            print(f"\tError with message '{error.message}'.")
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print(f"\t\tOn field: {field_path_element.field_name}")
        sys.exit(1)


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    google_ads_client = GoogleAdsClient.load_from_storage()

    parser = argparse.ArgumentParser(
        description="Gets all available criterion bid modifier simulations "
        "for a given campaign."
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
        "-i",
        "--campaign_id",
        type=str,
        required=True,
        help="The campaign ID from which to get available bid simulations.",
    )
    args = parser.parse_args()

    main(google_ads_client, args.customer_id, args.campaign_id)
