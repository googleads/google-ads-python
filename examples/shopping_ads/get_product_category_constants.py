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
"""This example fetches the set of all ProductCategoryConstants."""


import argparse
import collections
import sys
from typing import DefaultDict, List, Optional

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.ads.googleads.v22.resources.types.product_category_constant import (
    ProductCategoryConstant,
)
from google.ads.googleads.v22.services.services.google_ads_service import (
    GoogleAdsServiceClient,
)
from google.ads.googleads.v22.services.types.google_ads_service import (
    SearchGoogleAdsStreamRequest,
    SearchGoogleAdsStreamResponse,
)


class Category:
    def __init__(
        self,
        localized_name: Optional[str] = None,
        resource_name: Optional[str] = None,
        children: Optional[List["Category"]] = None,
    ) -> None:
        self.localized_name: Optional[str] = localized_name
        self.resource_name: Optional[str] = resource_name
        if children is None:
            self.children: List["Category"] = []
        else:
            self.children: List["Category"] = children


def display_categories(categories: List[Category], prefix: str = "") -> None:
    """Recursively prints out each category and its children.

    Args:
      categories: the map of categories to print
      prefix: the string to print at the beginning of each line of output

    Returns: None
    """
    for category in categories:
        print(f"{prefix} {category.localized_name} [{category.resource_name}]")
        if category.children:
            display_categories(
                category.children, prefix=f"{prefix} {category.localized_name}"
            )


def main(client: GoogleAdsClient, customer_id: str) -> None:
    """Fetches the set of valid ProductBiddingCategories."""

    ga_service: GoogleAdsServiceClient = client.get_service("GoogleAdsService")
    query: str = """
        SELECT
            product_category_constant.localizations,
            product_category_constant.product_category_constant_parent
        FROM product_category_constant"""

    search_request: SearchGoogleAdsStreamRequest = client.get_type(
        "SearchGoogleAdsStreamRequest"
    )
    search_request.customer_id = customer_id
    search_request.query = query
    stream: SearchGoogleAdsStreamResponse = ga_service.search_stream(
        search_request
    )

    all_categories: DefaultDict[str, Category] = collections.defaultdict(
        lambda: Category()
    )

    # Creates a map of top level categories.
    root_categories: List[Category] = []

    for batch in stream:
        for row in batch.results:
            # Gets the product category constant from the row.
            product_category: ProductCategoryConstant = (
                row.product_category_constant
            )

            localized_name: str = ""
            for localization in product_category.localizations:
                region: str = localization.region_code
                lang: str = localization.language_code
                if region == "US" and lang == "en":
                    # Gets the name from the product category localization.
                    localized_name = localization.value
                    break

            category: Category = Category(
                localized_name=localized_name,
                resource_name=product_category.resource_name,
            )

            # Ensure resource_name is not None before using as a dict key
            if category.resource_name:
                all_categories[category.resource_name] = category

            parent_resource_name: Optional[str] = None
            if product_category.product_category_constant_parent:
                parent_resource_name = (
                    product_category.product_category_constant_parent
                )

            # Links the category to the parent category if any.
            if parent_resource_name:
                # Adds the category as a child category of the parent
                # category.
                all_categories[parent_resource_name].children.append(category)
            elif (
                category.resource_name
            ):  # Ensure it's not None before adding to root
                # Otherwise adds the category as a root category.
                root_categories.append(category)

    display_categories(root_categories)


if __name__ == "__main__":
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
    args: argparse.Namespace = parser.parse_args()

    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client: GoogleAdsClient = GoogleAdsClient.load_from_storage(
        version="v22"
    )

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
