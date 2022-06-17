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
"""This example retrieves keywords for a customer for a specific ad group.

It also demonstrates how to use the omit_unselected_resource_names option in
GAQL to reduce payload size.
"""


import argparse
import sys

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


_DEFAULT_PAGE_SIZE = 1000


def main(
    client, customer_id, page_size, ad_group_id, omit_unselected_resource_names
):
    ga_service = client.get_service("GoogleAdsService")

    query = """
        SELECT
          ad_group.id,
          ad_group_criterion.type,
          ad_group_criterion.criterion_id,
          ad_group_criterion.keyword.text,
          ad_group_criterion.keyword.match_type
        FROM ad_group_criterion
        WHERE ad_group_criterion.type = KEYWORD"""

    if ad_group_id:
        query += f" AND ad_group.id = {ad_group_id}"

    # Adds omit_unselected_resource_names=true to the PARAMETERS clause of the
    # Google Ads Query Language (GAQL) query, which excludes the resource names
    # of all resources that aren't explicitly requested in the SELECT clause.
    # Enabling this option reduces payload size, but if you plan to use a
    # returned object in subsequent mutate operations, make sure you explicitly
    # request its "resource_name" field in the SELECT clause.
    #
    # Read more about PARAMETERS:
    # https://developers.google.com/google-ads/api/docs/query/structure#parameters
    if omit_unselected_resource_names:
        query += " PARAMETERS omit_unselected_resource_names=true"

    search_request = client.get_type("SearchGoogleAdsRequest")
    search_request.customer_id = customer_id
    search_request.query = query
    search_request.page_size = page_size

    results = ga_service.search(request=search_request)

    for row in results:
        ad_group = row.ad_group
        ad_group_criterion = row.ad_group_criterion
        keyword = row.ad_group_criterion.keyword

        if omit_unselected_resource_names:
            resource_name_log_statement = ""
        else:
            resource_name_log_statement = (
                f" and resource name '{ad_group.resource_name}'"
            )

        print(
            f'Keyword with text "{keyword.text}", match type '
            f"{keyword.match_type}, criteria type "
            f"{ad_group_criterion.type_}, and ID "
            f"{ad_group_criterion.criterion_id} was found in ad group "
            f"with ID {ad_group.id}{resource_name_log_statement}."
        )


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v10")

    parser = argparse.ArgumentParser(
        description=(
            "Retrieves keywords for the specified customer, or "
            "optionally for a specific ad group."
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
        "-a", "--ad_group_id", type=str, help="The ad group ID."
    )
    parser.add_argument(
        "-o",
        "--omit-unselected-resource-names",
        type=bool,
        default=False,
        help="Whether or not the response should omit resource names.",
    )
    args = parser.parse_args()

    try:
        main(
            googleads_client,
            args.customer_id,
            _DEFAULT_PAGE_SIZE,
            args.ad_group_id,
            args.omit_unselected_resource_names,
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
