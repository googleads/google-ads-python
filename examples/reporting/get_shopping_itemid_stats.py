#!/usr/bin/env python
# Copyright 2023 Google LLC
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
"""This example illustrates how to get shopping ItemID performance data.

Retrieves all ItemIDs and associated metrics in a shopping campaign.
"""

import argparse
import sys

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


def main(client, customer_id):
    ga_service = client.get_service("GoogleAdsService")

    query = """
            SELECT
              segments.date,
              segments.product_item_id,
              segments.product_title,
              metrics.all_conversions,
              metrics.all_conversions_from_interactions_rate,
              metrics.all_conversions_value,
              metrics.average_cpc,
              metrics.clicks,
              metrics.conversions,
              metrics.conversions_from_interactions_rate,
              metrics.conversions_value,
              metrics.cost_micros,
              metrics.cost_per_all_conversions,
              metrics.cost_per_conversion,
              metrics.cross_device_conversions,
              metrics.ctr,
              metrics.impressions,
              metrics.value_per_all_conversions,
              metrics.value_per_conversion
            FROM shopping_performance_view
            WHERE segments.date DURING LAST_30_DAYS"""

    # Issues a search request using streaming.
    search_request = client.get_type("SearchGoogleAdsStreamRequest")
    search_request.customer_id = customer_id
    search_request.query = query

    stream = ga_service.search_stream(search_request)

    for batch in stream:
        for row in batch.results:
            metrics = row.metrics

            print(
                f'Product "{row.segments.product_title}" with '
                f'Item ID "{row.segments.product_item_id}" on '
                f"{row.segments.date} "
                f"had {metrics.all_conversions} all conversions, "
                f"{metrics.average_cpc} average CPC, "
                f"{metrics.clicks} click(s), "
                f"{metrics.conversions} conversion(s), "
                f"{metrics.cost_micros} cost (in micros), "
                "and other metrics."
            )


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v13")

    parser = argparse.ArgumentParser(
        description="Retrieves a shopping campaign's ItemIDs and metrics."
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
            print(f'\tError with message "{error.message}".')
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print(f"\t\tOn field: {field_path_element.field_name}")
        sys.exit(1)
