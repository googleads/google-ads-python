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
"""Adds a shopping listing group tree to a shopping ad group.

The example will clear an existing listing group tree and rebuild it include the
following tree structure:

ProductCanonicalCondition NEW $0.20
ProductCanonicalCondition USED $0.10
ProductCanonicalCondition null (everything else)
    ProductBrand CoolBrand $0.90
    ProductBrand CheapBrand $0.01
    ProductBrand null (everything else) $0.50
"""

import argparse
import sys

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

last_criterion_id = 0


def _next_id():
    """Returns a decreasing negative number for temporary ad group criteria IDs.

    The ad group criteria will get real IDs when created on the server.
    Returns -1, -2, -3, etc. on subsequent calls.

    Returns:
        The string representation of a negative integer.
    """
    global last_criterion_id
    last_criterion_id -= 1
    return str(last_criterion_id)


# [START add_shopping_product_listing_group_tree]
def main(client, customer_id, ad_group_id, replace_existing_tree):
    """Adds a shopping listing group tree to a shopping ad group.

    Args:
        client: An initialized Google Ads client.
        customer_id: The Google Ads customer ID.
        ad_group_id: The ad group ID to which the node will be added.
        replace_existing_tree: Boolean, whether to replace the existing listing
            group tree on the ad group. Defaults to false.
    """
    # Get the AdGroupCriterionService client.
    ad_group_criterion_service = client.get_service("AdGroupCriterionService")

    # Optional: Remove the existing listing group tree, if it already exists
    # on the ad group. The example will throw a LISTING_GROUP_ALREADY_EXISTS
    # error if a listing group tree already exists and this option is not
    # set to true.
    if replace_existing_tree:
        _remove_listing_group_tree(client, customer_id, ad_group_id)

    # Create a list of ad group criteria operations.
    operations = []

    # Construct the listing group tree "root" node.
    # Subdivision node: (Root node)
    ad_group_criterion_root_operation = _create_listing_group_subdivision(
        client, customer_id, ad_group_id
    )

    # Get the resource name that will be used for the root node.
    # This resource has not been created yet and will include the temporary
    # ID as part of the criterion ID.
    ad_group_criterion_root_resource_name = (
        ad_group_criterion_root_operation.create.resource_name
    )
    operations.append(ad_group_criterion_root_operation)

    # Construct the listing group unit nodes for NEW, USED, and other.
    product_condition_enum = client.get_type(
        "ProductConditionEnum"
    ).ProductCondition
    condition_dimension_info = client.get_type("ListingDimensionInfo")

    # Biddable Unit node: (Condition NEW node)
    # * Product Condition: NEW
    # * CPC bid: $0.20
    condition_dimension_info.product_condition.condition = (
        product_condition_enum.NEW
    )
    operations.append(
        _create_listing_group_unit_biddable(
            client,
            customer_id,
            ad_group_id,
            ad_group_criterion_root_resource_name,
            condition_dimension_info,
            200_000,
        )
    )

    # Biddable Unit node: (Condition USED node)
    # * Product Condition: USED
    # * CPC bid: $0.10
    condition_dimension_info.product_condition.condition = (
        product_condition_enum.USED
    )
    operations.append(
        _create_listing_group_unit_biddable(
            client,
            customer_id,
            ad_group_id,
            ad_group_criterion_root_resource_name,
            condition_dimension_info,
            100_000,
        )
    )

    # Sub-division node: (Condition "other" node)
    # * Product Condition: (not specified)
    # Note that all sibling nodes must have the same dimension type, even if
    # they don't contain a bid.
    client.copy_from(
        condition_dimension_info.product_condition,
        client.get_type("ProductConditionInfo"),
    )
    ad_group_criterion_other_operation = _create_listing_group_subdivision(
        client,
        customer_id,
        ad_group_id,
        ad_group_criterion_root_resource_name,
        condition_dimension_info,
    )
    # Get the resource name that will be used for the condition other node.
    # This resource has not been created yet and will include the temporary
    # ID as part of the criterion ID.
    ad_group_criterion_other_resource_name = (
        ad_group_criterion_other_operation.create.resource_name
    )
    operations.append(ad_group_criterion_other_operation)

    # Build the listing group nodes for CoolBrand, CheapBrand, and other.
    brand_dimension_info = client.get_type("ListingDimensionInfo")

    # Biddable Unit node: (Brand CoolBrand node)
    # * Brand: CoolBrand
    # * CPC bid: $0.90
    brand_dimension_info.product_brand.value = "CoolBrand"
    operations.append(
        _create_listing_group_unit_biddable(
            client,
            customer_id,
            ad_group_id,
            ad_group_criterion_other_resource_name,
            brand_dimension_info,
            900_000,
        )
    )

    # Biddable Unit node: (Brand CheapBrand node)
    # * Brand: CheapBrand
    # * CPC bid: $0.01
    brand_dimension_info.product_brand.value = "CheapBrand"
    operations.append(
        _create_listing_group_unit_biddable(
            client,
            customer_id,
            ad_group_id,
            ad_group_criterion_other_resource_name,
            brand_dimension_info,
            10_000,
        )
    )

    # Biddable Unit node: (Brand other node)
    # * CPC bid: $0.05
    client.copy_from(
        brand_dimension_info.product_brand, client.get_type("ProductBrandInfo"),
    )
    operations.append(
        _create_listing_group_unit_biddable(
            client,
            customer_id,
            ad_group_id,
            ad_group_criterion_other_resource_name,
            brand_dimension_info,
            50_000,
        )
    )

    # Add the ad group criteria.
    mutate_ad_group_criteria_response = ad_group_criterion_service.mutate_ad_group_criteria(
        customer_id=customer_id, operations=operations
    )

    # Print the results of the successful mutates.
    print(
        "Added ad group criteria for the listing group tree with the "
        "following resource names:"
    )
    for result in mutate_ad_group_criteria_response.results:
        print(f"\t{result.resource_name}")

    print(f"{len(mutate_ad_group_criteria_response.results)} criteria added.")
    # [END add_shopping_product_listing_group_tree]


def _remove_listing_group_tree(client, customer_id, ad_group_id):
    """Removes ad group criteria for an ad group's existing listing group tree.

    Args:
        client: An initialized Google Ads client.
        customer_id: The Google Ads customer ID.
        ad_group_id: The ad group ID from which to remove the listing group
            tree.
    """
    # Get the GoogleAdsService client.
    googleads_service = client.get_service("GoogleAdsService")

    print("Removing existing listing group tree...")
    # Create a search Google Ads request that will retrieve all listing groups
    # where the parent ad group criterion is NULL (and hence the root node in
    # the tree) for a given ad group id.
    query = f"""
        SELECT ad_group_criterion.resource_name
        FROM ad_group_criterion
        WHERE
          ad_group_criterion.type = LISTING_GROUP
          AND ad_group_criterion.listing_group.parent_ad_group_criterion IS NULL
          AND ad_group.id = {ad_group_id}"""

    results = googleads_service.search(customer_id=customer_id, query=query)
    ad_group_criterion_operations = []

    # Iterate over all rows to find the ad group criteria to remove.
    for row in results:
        criterion = row.ad_group_criterion
        print(
            "Found an ad group criterion with resource name: "
            f"'{criterion.resource_name}'."
        )
        ad_group_criterion_operation = client.get_type(
            "AdGroupCriterionOperation"
        )
        ad_group_criterion_operation.remove = criterion.resource_name
        ad_group_criterion_operations.append(ad_group_criterion_operation)

    if ad_group_criterion_operations:
        # Remove the ad group criteria that define the listing group tree.
        ad_group_criterion_service = client.get_service(
            "AdGroupCriterionService"
        )
        response = ad_group_criterion_service.mutate_ad_group_criteria(
            customer_id=customer_id, operations=ad_group_criterion_operations
        )
        print(f"Removed {len(response.results)} ad group criteria.")


def _create_listing_group_subdivision(
    client,
    customer_id,
    ad_group_id,
    parent_ad_group_criterion_resource_name=None,
    listing_dimension_info=None,
):
    """Creates a new criterion containing a subdivision listing group node.

    If the parent ad group criterion resource name or listing dimension info are
    not specified, this method creates a root node.

    Args:
        client: An initialized Google Ads client.
        customer_id: The Google Ads customer ID.
        ad_group_id: The ad group ID to which the node will be added.
        parent_ad_group_criterion_resource_name: The string resource name of the
            parent node to which this listing will be attached.
        listing_dimension_info: A ListingDimensionInfo object containing details
            for this listing.

    Returns:
        An AdGroupCriterionOperation containing a populated ad group criterion.
    """
    # Create an ad group criterion operation and populate the criterion.
    operation = client.get_type("AdGroupCriterionOperation")
    ad_group_criterion = operation.create
    # The resource name the criterion will be created with. This will define
    # the ID for the ad group criterion.
    ad_group_criterion.resource_name = client.get_service(
        "AdGroupCriterionService"
    ).ad_group_criterion_path(customer_id, ad_group_id, _next_id())
    ad_group_criterion.status = client.get_type(
        "AdGroupCriterionStatusEnum"
    ).AdGroupCriterionStatus.ENABLED

    listing_group_info = ad_group_criterion.listing_group
    # Set the type as a SUBDIVISION, which will allow the node to be the
    # parent of another sub-tree.
    listing_group_info.type_ = client.get_type(
        "ListingGroupTypeEnum"
    ).ListingGroupType.SUBDIVISION
    # If parent_ad_group_criterion_resource_name and listing_dimension_info
    # are not null, create a non-root division by setting its parent and case
    # value.
    if (
        parent_ad_group_criterion_resource_name
        and listing_dimension_info != None
    ):
        # Set the ad group criterion resource name for the parent listing group.
        # This can include a temporary ID if the parent criterion is not yet
        # created.
        listing_group_info.parent_ad_group_criterion = (
            parent_ad_group_criterion_resource_name
        )

        # Case values contain the listing dimension used for the node.
        client.copy_from(listing_group_info.case_value, listing_dimension_info)

    return operation


def _create_listing_group_unit_biddable(
    client,
    customer_id,
    ad_group_id,
    parent_ad_group_criterion_resource_name,
    listing_dimension_info,
    cpc_bid_micros=None,
):
    """Creates a new criterion containing a biddable unit listing group node.

    Args:
        client: An initialized Google Ads client.
        customer_id: The Google Ads customer ID.
        ad_group_id: The ad group ID to which the node will be added.
        parent_ad_group_criterion_resource_name: The string resource name of the
            parent node to which this listing will be attached.
        listing_dimension_info: A ListingDimensionInfo object containing details
            for this listing.
        cpc_bid_micros: The cost-per-click bid for this listing in micros.

    Returns:
        An AdGroupCriterionOperation with a populated create field.
    """
    # Note: There are two approaches for creating new unit nodes:
    # (1) Set the ad group resource name on the criterion (no temporary ID
    # required).
    # (2) Use a temporary ID to construct the criterion resource name and set
    # it to the 'resourceName' attribute.
    # In both cases you must set the parent ad group criterion's resource name
    # on the listing group for non-root nodes.
    # This example demonstrates method (1).
    operation = client.get_type("AdGroupCriterionOperation")

    criterion = operation.create
    criterion.ad_group = client.get_service("AdGroupService").ad_group_path(
        customer_id, ad_group_id
    )
    criterion.status = client.get_type(
        "AdGroupCriterionStatusEnum"
    ).AdGroupCriterionStatus.ENABLED
    # Set the bid for this listing group unit.
    # This will be used as the CPC bid for items that are included in this
    # listing group.
    if cpc_bid_micros:
        criterion.cpc_bid_micros = cpc_bid_micros

    listing_group = criterion.listing_group
    # Set the type as a UNIT, which will allow the group to be biddable.
    listing_group.type_ = client.get_type(
        "ListingGroupTypeEnum"
    ).ListingGroupType.UNIT
    # Set the ad group criterion resource name for the parent listing group.
    # This can have a temporary ID if the parent criterion is not yet created.
    listing_group.parent_ad_group_criterion = (
        parent_ad_group_criterion_resource_name
    )
    # Case values contain the listing dimension used for the node.
    if listing_dimension_info != None:
        client.copy_from(listing_group.case_value, listing_dimension_info)

    return operation


if __name__ == "__main__":
    googleads_client = GoogleAdsClient.load_from_storage(version="v8")

    parser = argparse.ArgumentParser(
        description="Add shopping product listing group tree to a shopping ad "
        "group."
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
        "-a",
        "--ad_group_id",
        type=str,
        required=True,
        help="The ID of the ad group that will receive the listing group tree.",
    )
    parser.add_argument(
        "-r",
        "--replace_existing_tree",
        action="store_true",
        required=False,
        default=False,
        help="Optional, whether to replace the existing listing group tree on "
        "the ad group if one already exists. Defaults to false.",
    )

    args = parser.parse_args()

    try:
        main(
            googleads_client,
            args.customer_id,
            args.ad_group_id,
            args.replace_existing_tree,
        )
    except GoogleAdsException as ex:
        print(
            f"Request with ID '{ex.request_id}' failed with status "
            f"'{ex.error.code().name}' and includes the following errors:"
        )
        for error in ex.failure.errors:
            print(f"\tError with message '{error.message}'.")
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print(f"\t\tOn field: {field_path_element.field_name}")
        sys.exit(1)
