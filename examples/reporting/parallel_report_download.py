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
"""Shows how to download a set of reports from a list of accounts in parallel.

If you need to obtain a list of accounts, please see the
account_management/get_account_hierarchy.py or
account_management/list_accessible_customers.py examples.
"""

import argparse
from itertools import product
import multiprocessing
import sys
import time

from google.ads.google_ads.client import GoogleAdsClient
from google.ads.google_ads.errors import GoogleAdsException

# Maximum number of processes to spawn
MAX_PROCESSES = multiprocessing.cpu_count()
# Timeout between retries in seconds
BACKOFF_FACTOR = 5
# Maximum number of retries for 500 errors
MAX_RETRIES = 5


def main(client, customer_ids):
    """The main method that creates all necessary entities for the example.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_ids: an array of client customer IDs.
    """

    # Define the GAQL query strings to run for each customer ID.
    campaign_query = """
        SELECT campaign.id, metrics.impressions, metrics.clicks
        FROM campaign
        WHERE segments.date DURING LAST_30_DAYS"""
    ad_group_query = """
        SELECT campaign.id, ad_group.id, metrics.impressions, metrics.clicks
        FROM ad_group
        WHERE segments.date DURING LAST_30_DAYS"""

    inputs = _generate_inputs(
        client, customer_ids, [campaign_query, ad_group_query]
    )
    with multiprocessing.Pool(MAX_PROCESSES) as pool:
        results = pool.starmap(_issue_search_request, inputs)
        print(results)


def _issue_search_request(client, customer_id, query):
    """Issues a search request using streaming.

    If a 500 error is received, retries until MAX_RETRIES is reached.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID str.
        query: a GAQL query str.
    """
    ga_service = client.get_service("GoogleAdsService", version="v6")
    retry_count = 0
    # A while loop allows us to retry until we've reached MAX_RETRIES or
    # have successfully received a response.
    while True:
        try:
            response = ga_service.search_stream(customer_id, query)
            # Returning a list of GoogleAdsRows will result in a
            # PicklingError, so instead we put the GoogleAdsRow data
            # into a list of str results and return that.
            result_strings = []
            for batch in response:
                for row in batch.results:
                    ad_group_id = (
                        f"Ad Group ID {row.ad_group.id} in "
                        if "ad_group.id" in query
                        else ""
                    )
                    result_string = (
                        f"{ad_group_id}"
                        f"Campaign ID {row.campaign.id} "
                        f"had {row.metrics.impressions} impressions "
                        f"and {row.metrics.clicks} clicks"
                    )
                    result_strings.append(result_string)
            return result_strings
        except GoogleAdsException as ex:
            if ex.error_code() == 500 and retry_count < MAX_RETRIES:
                retry_count += 1
                time.sleep(retry_count * BACKOFF_FACTOR)
            else:
                print(
                    f"Request for customer ID {customer_id} with request ID "
                    f"{ex.request_id} failed with status "
                    f"{ex.error.code().name} after {retry_count + 1} "
                    "retries and includes the following errors:"
                )
                for error in ex.failure.errors:
                    print(f'\tError with message "{error.message}".')
                    if error.location:
                        for (
                            field_path_element
                        ) in error.location.field_path_elements:
                            print(
                                f"\t\tOn field: {field_path_element.field_name}"
                            )
                sys.exit(1)


def _generate_inputs(client, customer_ids, queries):
    """Generates all inputs to feed into search requests.

    A GoogleAdsService instance cannot be serialized with pickle for parallel
    processing, but a GoogleAdsClient can be, so we pass the client to the
    pool task which will then get the GoogleAdsService instance.

    Args:
        client: An initialized GoogleAdsClient instance.
        customer_ids: A list of str client customer IDs.
        queries: A list of str GAQL queries.
    """
    return product([client], customer_ids, queries)


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    google_ads_client = GoogleAdsClient.load_from_storage()

    parser = argparse.ArgumentParser(
        description="Download a set of reports from a list of accounts in "
        "parallel."
    )
    # The following argument(s) should be provided to run the example.
    parser.add_argument(
        "-c",
        "--customer_ids",
        nargs="+",
        type=str,
        required=True,
        help="The Google Ads customer IDs.",
    )
    args = parser.parse_args()

    main(google_ads_client, args.customer_ids)
