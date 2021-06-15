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
"""Adds a shopping listing scope to a shopping campaign.

The example will construct and add a new listing scope which will act as the
inventory filter for the campaign. The campaign will only advertise products
that match the following requirements:

* Brand is "google".
* Custom label 0 is "top_selling_products".
* Product type (level 1) is "electronics".
* Product type (level 2) is "smartphones".

Only one listing scope is allowed per campaign. Remove any existing listing
scopes before running this example.
"""

import argparse
import sys

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


def main(client, customer_id, campaign_id):
    campaign_service = client.get_service("CampaignService")
    campaign_criterion_operation = client.get_type("CampaignCriterionOperation")
    campaign_criterion = campaign_criterion_operation.create
    campaign_criterion.campaign = campaign_service.campaign_path(
        customer_id, campaign_id
    )

    # A listing scope allows you to filter the products that will be included in
    # a given campaign. You can specify multiple dimensions with conditions that
    # must be met for a product to be included in a campaign.
    # A typical listing scope might only have a few dimensions. This example
    # demonstrates a range of different dimensions you could use.
    dimensions = campaign_criterion.listing_scope.dimensions

    product_brand_dimension = client.get_type("ListingDimensionInfo")
    product_brand_dimension.product_brand.value = "google"
    dimensions.append(product_brand_dimension)

    product_custom_attribute_index_enum = client.get_type(
        "ProductCustomAttributeIndexEnum"
    ).ProductCustomAttributeIndex
    product_custom_attribute_dimension = client.get_type("ListingDimensionInfo")
    product_custom_attribute = (
        product_custom_attribute_dimension.product_custom_attribute
    )
    product_custom_attribute.index = product_custom_attribute_index_enum.INDEX0
    product_custom_attribute.value = "top_selling_products"
    dimensions.append(product_custom_attribute_dimension)

    product_type_level_enum = client.get_type(
        "ProductTypeLevelEnum"
    ).ProductTypeLevel
    product_type_dimension_1 = client.get_type("ListingDimensionInfo")
    product_type = product_type_dimension_1.product_type
    product_type.level = product_type_level_enum.LEVEL1
    product_type.value = "electronics"
    dimensions.append(product_type_dimension_1)

    product_type_dimension_2 = client.get_type("ListingDimensionInfo")
    product_type = product_type_dimension_2.product_type
    product_type.level = product_type_level_enum.LEVEL2
    product_type.value = "smartphones"
    dimensions.append(product_type_dimension_2)

    campaign_criterion_service = client.get_service("CampaignCriterionService")

    campaign_criterion_response = campaign_criterion_service.mutate_campaign_criteria(
        customer_id=customer_id, operations=[campaign_criterion_operation]
    )

    print(
        f"Added {len(campaign_criterion_response.results)} campaign "
        "criteria:"
    )
    for campaign_criterion in campaign_criterion_response.results:
        print(campaign_criterion.resource_name)


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v8")

    parser = argparse.ArgumentParser(
        description=("Adds a shopping listing scope to a shopping campaign.")
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
        "-i", "--campaign_id", type=str, required=True, help="The campaign ID."
    )
    args = parser.parse_args()

    try:
        main(googleads_client, args.customer_id, args.campaign_id)
    except GoogleAdsException as ex:
        print(
            f'Request with ID "{ex.request_id}" failed with status'
            f'"{ex.error.code().name}" and includes the following errors:'
        )
        for error in ex.failure.errors:
            print(f'\tError with message "{error.message}".')
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print(f"\t\tOn field: {field_path_element.field_name}")
        sys.exit(1)
