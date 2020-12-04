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

from google.ads.google_ads.client import GoogleAdsClient
from google.ads.google_ads.errors import GoogleAdsException


def main(client, customer_id, campaign_id):
    campaign_service = client.get_service("CampaignService", version="v6")

    campaign_resource_name = campaign_service.campaign_path(
        customer_id, campaign_id
    )

    campaign_criterion_operation = client.get_type(
        "CampaignCriterionOperation", version="v6"
    )
    campaign_criterion = campaign_criterion_operation.create
    campaign_criterion.campaign = campaign_resource_name

    # A listing scope allows you to filter the products that will be included in
    # a given campaign. You can specify multiple dimensions with conditions that
    # must be met for a product to be included in a campaign.
    # A typical listing scope might only have a few dimensions. This example
    # demonstrates a range of different dimensions you could use.
    _build_listing_scope_dimensions(
        client, campaign_criterion.listing_scope.dimensions
    )

    campaign_criterion_service = client.get_service(
        "CampaignCriterionService", version="v6"
    )

    try:
        campaign_criterion_response = campaign_criterion_service.mutate_campaign_criteria(
            customer_id, [campaign_criterion_operation]
        )
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

    print(
        f"Added {len(campaign_criterion_response.results)} campaign "
        "criteria:"
    )
    for campaign_criterion in campaign_criterion_response.results:
        print(campaign_criterion.resource_name)


def _build_listing_scope_dimensions(client, dimensions):
    product_brand_dimension = dimensions.add()
    product_brand_dimension.product_brand.value = "google"

    product_custom_attribute_index_enum = client.get_type(
        "ProductCustomAttributeIndexEnum", version="v6"
    )

    dimensions.append(
        product_custom_attribute_dimension.product_custom_attribute
    )
    product_custom_attribute.index = product_custom_attribute_index_enum.INDEX0
    product_custom_attribute = "top_selling_products"

    product_type_level_enum = client.get_type(
        "ProductTypeLevelEnum", version="v6"
    )

    product_type_dimension_1 = dimensions.add()
    product_type = product_type_dimension_1.product_type
    product_type.level = product_type_level_enum.LEVEL1
    product_type.value = "electronics"

    product_type_dimension_2 = dimensions.add()
    product_type = product_type_dimension_2.product_type
    product_type.level = product_type_level_enum.LEVEL2
    product_type.value = "smartphones"


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    google_ads_client = GoogleAdsClient.load_from_storage()

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

    main(google_ads_client, args.customer_id, args.campaign_id)
