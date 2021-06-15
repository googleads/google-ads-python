#!/usr/bin/env python
#
# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Shows how to write data from a basic campaign stats report to a CSV file.

Examples:
    Write to file output.csv in the same directory as script with headers.
        $ python get_campaign_stats_to_csv.py -c 0123456789 -o output.csv -w

    Write to file output.csv in the same directory as script without headers.
        $ python get_campaign_stats_to_csv.py -c 0123456789 -o output.csv
"""

import argparse
import csv
import sys

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


def main(client, customer_id, output_file, write_headers):
    """Writes rows returned from a search_stream request to a CSV file.
    Args:
        client: An initialized GoogleAdsClient instance.
        customer_id (str): The client customer ID string.
        output_file (str): Filename of the file to write the report data to.
        write_headers (bool): From argparse, True if arg is provided.
    """
    ga_service = client.get_service("GoogleAdsService")

    query = """
        SELECT
          customer.descriptive_name,
          segments.date,
          campaign.name,
          metrics.impressions,
          metrics.clicks,
          metrics.cost_micros
        FROM campaign
        WHERE
          segments.date DURING LAST_7_DAYS
        ORDER BY metrics.impressions DESC
        LIMIT 25"""

    # Issues a search request using streaming.
    search_request = client.get_type("SearchGoogleAdsStreamRequest")
    search_request.customer_id = customer_id
    search_request.query = query
    response = ga_service.search_stream(search_request)
    try:
        with open(output_file, "w", newline="") as f:
            writer = csv.writer(f)

            # Define a list of headers for the first row.
            headers = [
                "Account",
                "Date",
                "Campaign",
                "Impressions",
                "Clicks",
                "Cost",
            ]

            # If the write_headers flag was passed, write header row to the CSV
            if write_headers:
                writer.writerow(headers)

            for batch in response:
                for row in batch.results:
                    # Use the CSV writer to write the individual GoogleAdsRow
                    # fields returned in the SearchGoogleAdsStreamResponse.
                    writer.writerow(
                        [
                            row.customer.descriptive_name,
                            row.segments.date,
                            row.campaign.name,
                            row.metrics.impressions,
                            row.metrics.clicks,
                            row.metrics.cost_micros,
                        ]
                    )

            print(f"Customer {customer_id} report written to {output_file}")

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


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    google_ads_client = GoogleAdsClient.load_from_storage(version="v8")

    parser = argparse.ArgumentParser(
        description="Retrieves a campaign stats and writes to CSV file."
    )
    # The following argument(s) should be provided to run the example.
    parser.add_argument(
        "-c",
        "--customer_id",
        type=str,
        required=True,
        help="The Google Ads customer ID of the account you would like to get "
        "the report for to write to CSV.",
    )
    parser.add_argument(
        "-o",
        "--output_file",
        type=str,
        required=True,
        help="Name of the local CSV file to save the report to. File will be "
        "saved in the same directory as the script.",
    )
    # Optional boolean argument for writing headers.
    parser.add_argument(
        "-w",
        "--write_headers",
        action="store_true",
        help="Writes headers to the CSV file if argument is supplied. Simply "
        "add -w if you want the headers defined in the script to be "
        "added as the first row in the CSV file.",
    )
    args = parser.parse_args()

    main(
        google_ads_client,
        args.customer_id,
        args.output_file,
        args.write_headers,
    )
