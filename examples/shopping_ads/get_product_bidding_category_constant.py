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
"""This example fetches the set of valid ProductBiddingCategories."""


import argparse
import collections
import sys
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


def _display_categories(categories, prefix=""):
    """Recursively prints out each category and its children.

    Args:
      categories: the map of categories to print
      prefix: the string to print at the beginning of each line of output

    Returns: None
    """
    for category in categories:
        print(f"{prefix}{category.name} [{category.category_id}]")
        if not category.children:
            _display_categories(
                category.children, prefix=prefix + category.name
            )


def main(client, customer_id):
    """Fetches the set of valid ProductBiddingCategories."""

    class Category:
        def __init__(self, name=None, category_id=None, children=None):
            self.name = name
            self.category_id = category_id
            if children is None:
                self.children = []
            else:
                self.children = children

    ga_service = client.get_service("GoogleAdsService")
    query = """
        SELECT product_bidding_category_constant.localized_name,
        product_bidding_category_constant.product_bidding_category_constant_parent
        FROM product_bidding_category_constant WHERE
        product_bidding_category_constant.country_code IN ("US")"""

    search_request = client.get_type("SearchGoogleAdsStreamRequest")
    search_request.customer_id = customer_id
    search_request.query = query
    response = ga_service.search_stream(search_request)

    all_categories = collections.defaultdict(lambda: Category())

    # Creates a map of top level categories.
    root_categories = []

    for batch in response:
        for row in batch.results:
            product_bidding_category = row.product_bidding_category_constant

            category = Category(
                product_bidding_category.localized_name,
                product_bidding_category.resource_name,
            )

            all_categories[category.category_id] = category
            parent = (
                product_bidding_category.product_bidding_category_constant_parent
            )
            parent_id = getattr(parent, "value", None)

            # Links the category to the parent category if any.
            if parent_id:
                # Adds the category as a child category of the parent
                # category.
                all_categories[parent_id].children.append(category)
            else:
                # Otherwise adds the category as a root category.
                root_categories.append(category)

    _display_categories(root_categories)


if __name__ == "__main__":
    googleads_client = GoogleAdsClient.load_from_storage(version="v8")

    parser = argparse.ArgumentParser(
        description="Get Product Bidding Category Constant"
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
