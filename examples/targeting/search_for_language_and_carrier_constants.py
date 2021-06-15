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
"""Demonstrates how to search for language and mobile carrier constants.

Specifically, this example illustrates how to:
1. Search for language constants where the name includes a given string.
2. Search for all the available mobile carrier constants with a given country
    code.
"""


import argparse
import sys

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


def main(client, customer_id, language_name, carrier_country_code):
    """Demonstrates how to search for language and mobile carrier constants.

    Args:
        client: An initialized Google Ads API client.
        customer_id: The Google Ads customer ID.
        language_name: String included in the language name to search for.
        carrier_country_code: String code of the country where the mobile
            carriers are located.
    """
    _search_for_language_constants(client, customer_id, language_name)
    _search_for_carrier_constants(client, customer_id, carrier_country_code)


def _search_for_language_constants(client, customer_id, language_name):
    """Searches for language constants where the name includes a given string.

    Args:
        client: An initialized Google Ads API client.
        customer_id: The Google Ads customer ID.
        language_name: String included in the language name to search for.
    """
    # Get the GoogleAdsService client.
    googleads_service = client.get_service("GoogleAdsService")

    # Create a query that retrieves the language constants where the name
    # includes a given string.
    query = f"""
        SELECT
          language_constant.id,
          language_constant.code,
          language_constant.name,
          language_constant.targetable
        FROM language_constant
        WHERE language_constant.name LIKE '%{language_name}%'"""

    # Issue a search request and process the stream response to print the
    # requested field values for the carrier constant in each row.
    response = googleads_service.search_stream(
        customer_id=customer_id, query=query
    )

    for batch in response:
        for row in batch.results:
            print(
                f"Language with ID {row.language_constant.id}, "
                f"code '{row.language_constant.code}', "
                f"name '{row.language_constant.name}', "
                f"and targetable '{row.language_constant.targetable}' "
                "was found."
            )


def _search_for_carrier_constants(client, customer_id, carrier_country_code):
    """Searches for mobile carrier constants with a given country code.

    Args:
        client: An initialized Google Ads API client.
        customer_id: The Google Ads customer ID.
        carrier_country_code: String code of the country where the mobile
            carriers are located.
    """
    # Get the GoogleAdsService client.
    googleads_service = client.get_service("GoogleAdsService")

    # Create a query that retrieves the targetable carrier constants by country
    # code.
    query = f"""
        SELECT
          carrier_constant.id,
          carrier_constant.name,
          carrier_constant.country_code
        FROM carrier_constant
        WHERE carrier_constant.country_code = '{carrier_country_code}'"""

    # Issue a search request and process the stream response to print the
    # requested field values for the carrier constant in each row.
    response = googleads_service.search_stream(
        customer_id=customer_id, query=query
    )

    for batch in response:
        for row in batch.results:
            print(
                f"Carrier with ID {row.carrier_constant.id}, "
                f"name '{row.carrier_constant.name}', "
                f"and country code '{row.carrier_constant.country_code}' "
                "was found."
            )


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v8")

    parser = argparse.ArgumentParser(
        description=(
            "Demonstrates how to search for language and mobile carrier "
            "constants."
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
    parser.add_argument(
        "-l",
        "--language_name",
        type=str,
        required=False,
        default="eng",
        help="Optional, string included in the language name to search for.",
    )
    parser.add_argument(
        "-p",
        "--carrier_country_code",
        type=str,
        required=False,
        default="US",
        help=(
            "Optional, string code of the country where the mobile carriers "
            "are located, e.g. 'US', 'ES', etc. "
            "A list of country codes can be referenced here: "
            "https://developers.google.com/google-ads/api/reference/data/geotargets"
        ),
    )
    args = parser.parse_args()

    try:
        main(
            googleads_client,
            args.customer_id,
            args.language_name,
            args.carrier_country_code,
        )
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
