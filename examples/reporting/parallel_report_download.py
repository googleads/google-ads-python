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
"""Shows how to download in parallel a set of reports from a list of accounts.

If you need to obtain a list of accounts, please see the
account_management/get_account_hierarchy.py or
account_management/list_accessible_customers.py examples.
"""

import argparse
from itertools import product
import multiprocessing
import time

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

# Maximum number of processes to spawn.
MAX_PROCESSES = multiprocessing.cpu_count()
# Timeout between retries in seconds.
BACKOFF_FACTOR = 5
# Maximum number of retries for errors.
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
        # Call _issue_search_request on each input, parallelizing the work
        # across processes in the pool.
        results = pool.starmap(_issue_search_request, inputs)

        # Partition our results into successful and failed results.
        successes = []
        failures = []
        for res in results:
            if res[0]:
                successes.append(res[1])
            else:
                failures.append(res[1])

        # Output results.
        print(
            f"Total successful results: {len(successes)}\n"
            f"Total failed results: {len(failures)}\n"
        )

        print("Successes:") if len(successes) else None
        for success in successes:
            # success["results"] represents an array of result strings for one
            # customer ID / query combination.
            result_str = "\n".join(success["results"])
            print(result_str)

        print("Failures:") if len(failures) else None
        for failure in failures:
            ex = failure["exception"]
            print(
                f'Request with ID "{ex.request_id}" failed with status '
                f'"{ex.error.code().name}" for customer_id '
                f'{failure["customer_id"]} and query "{failure["query"]}" and '
                "includes the following errors:"
            )
            for error in ex.failure.errors:
                print(f'\tError with message "{error.message}".')
                if error.location:
                    for (
                        field_path_element
                    ) in error.location.field_path_elements:
                        print(f"\t\tOn field: {field_path_element.field_name}")


def _issue_search_request(client, customer_id, query):
    """Issues a search request using streaming.

    Retries if a GoogleAdsException is caught, until MAX_RETRIES is reached.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID str.
        query: a GAQL query str.
    """
    ga_service = client.get_service("GoogleAdsService")
    retry_count = 0
    # Retry until we've reached MAX_RETRIES or have successfully received a
    # response.
    while True:
        try:
            response = ga_service.search_stream(
                customer_id=customer_id, query=query
            )
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
                        f"and {row.metrics.clicks} clicks."
                    )
                    result_strings.append(result_string)
            return (True, {"results": result_strings})
        except GoogleAdsException as ex:
            # This example retries on all GoogleAdsExceptions. In practice,
            # developers might want to limit retries to only those error codes
            # they deem retriable.
            if retry_count < MAX_RETRIES:
                retry_count += 1
                time.sleep(retry_count * BACKOFF_FACTOR)
            else:
                return (
                    False,
                    {
                        "exception": ex,
                        "customer_id": customer_id,
                        "query": query,
                    },
                )


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
    googleads_client = GoogleAdsClient.load_from_storage(version="v8")

    parser = argparse.ArgumentParser(
        description="Download a set of reports in parallel from a list of "
        "accounts."
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
    parser.add_argument(
        "-l",
        "--login_customer_id",
        type=str,
        help="The login customer ID (optional).",
    )
    args = parser.parse_args()
    # Override the login_customer_id on the GoogleAdsClient, if specified.
    if args.login_customer_id is not None:
        googleads_client.login_customer_id = args.login_customer_id

    main(googleads_client, args.customer_ids)
