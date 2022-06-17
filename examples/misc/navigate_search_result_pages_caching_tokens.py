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
"""This example illustrates how to cache page tokens in paged search requests.

GoogleAdsService.Search results are paginated but they can only be retrieved in
sequence starting with the first page. More details at:
https://developers.google.com/google-ads/api/docs/reporting/paging.

This example searches campaigns illustrating how GoogleAdsService.Search result
page tokens can be cached and reused to retrieve previous pages. This is useful
when you need to request pages that were already requested in the past without
starting over from the first page. For example, it can be used to implement an
interactive application that displays a page of results at a time without
caching all the results first.

To add campaigns, run the basic_examples/add_campaigns.py example.
"""


import argparse
import math
import sys

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


# The maximum number of results to retrieve in the query.
_RESULTS_LIMIT = 10
# The number of results to return per page.
_PAGE_SIZE = 3


def main(client, customer_id):
    """The main method that creates all necessary entities for the example.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
    """
    # The cache of page tokens which is stored in-memory with the page numbers
    # as keys. The first page's token is always an empty string.
    page_tokens = {1: ""}

    print("\n--- 0. Fetch page #1 to get metadata:\n")

    # Creates a query that retrieves the campaigns.
    query = f"""
        SELECT
          campaign.id,
          campaign.name
        FROM campaign
        ORDER BY campaign.name
        LIMIT {_RESULTS_LIMIT}"""

    request = client.get_type("SearchGoogleAdsRequest")
    request.customer_id = customer_id
    request.query = query
    # Sets the number of results to return per page.
    request.page_size = _PAGE_SIZE
    # Requests to return the total results count. This is necessary to determine
    # how many pages of results there are.
    request.return_total_results_count = True

    googleads_service = client.get_service("GoogleAdsService")
    response = googleads_service.search(request=request)
    _cache_next_page_token(page_tokens, response, 1)

    # Determines the total number of results and prints it. The total results
    # count does not take into consideration the LIMIT clause of the query so
    # we need to find the minimal value between the limit and the total results
    # count.
    total_number_of_results = min(_RESULTS_LIMIT, response.total_results_count)
    print(f"Total number of campaigns found: {total_number_of_results}.")

    # Determines the total number of pages and prints it.
    total_number_of_pages = math.ceil(total_number_of_results / _PAGE_SIZE)
    print(f"Total number of pages: {total_number_of_pages}.")
    if not total_number_of_pages:
        print("Could not find any campaigns.")
        sys.exit(1)

    # Demonstrates how the logic works when iterating pages forward. We select
    # a page that is in the middle of the result set so that only a subset of
    # the page tokens will be cached.
    middle_page_number = math.ceil(total_number_of_pages / 2)
    print(f"\n--- 1. Print results of the page {middle_page_number}\n")
    _fetch_and_print_results(
        client, customer_id, query, middle_page_number, page_tokens
    )


# [START navigate_search_result_pages_caching_tokens]
def _fetch_and_print_results(
    client, customer_id, query, page_number, page_tokens
):
    """Fetches and prints the results of a page using a cache of page tokens.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        query: the search query.
        page_number: the number of the page to fetch and print results for.
        page_tokens: the cache of page tokens to use and update.
    """
    current_page_number = None
    # There is no need to fetch the pages we already know the page tokens for.
    if page_tokens.get(page_number, None):
        print(
            "The token of the request page was cached, we will use it to get "
            "the results."
        )
        current_page_number = page_number
    else:
        count = len(page_tokens.keys())
        print(
            "The token of the requested page was never cached, we will use "
            f"the closest page we know the token for (page {count}) and "
            "sequentially get pages from there."
        )
        current_page_number = count

    googleads_service = client.get_service("GoogleAdsService")
    # Fetches next pages in sequence and caches their tokens until the requested
    # page results are returned.
    while current_page_number <= page_number:
        # Fetches the next page.
        print(f"Fetching page {current_page_number}...")
        request = client.get_type("SearchGoogleAdsRequest")
        request.customer_id = customer_id
        request.query = query
        request.page_size = _PAGE_SIZE
        request.return_total_results_count = True
        # Uses the page token cached for the current page number.
        request.page_token = page_tokens[current_page_number]

        response = googleads_service.search(request=request)
        _cache_next_page_token(page_tokens, response, current_page_number)
        current_page_number += 1

    # Prints the results of the requested page.
    print(f"Printing results found for the page {page_number}.")
    for row in response.results:
        print(
            f" - Campaign with ID {row.campaign.id} and name "
            f"{row.campaign.name}."
        )
        # [END navigate_search_result_pages_caching_tokens]


def _cache_next_page_token(page_tokens, page, page_number):
    """Updates the cache of page tokens based on a page that was retrieved.

    Args:
        page_tokens: a cache of page tokens to update.
        page: the search results page that was retrieved.
        page_number: the number of the page that was retrieved.
    """
    # Check if the page_token exists and that it hasn't already been cached.
    if page.next_page_token and not page_tokens.get(page_number, None):
        page_tokens[page_number + 1] = page.next_page_token
        print(f"Cached token for page #{page_number + 1}.")


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v10")

    parser = argparse.ArgumentParser(
        description=(
            "Demonstrates how to cache and reuse page tokens in a "
            "GoogleAdService.Search request."
        )
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
        main(
            googleads_client,
            args.customer_id,
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
