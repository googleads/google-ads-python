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
"""Shows how to add a hotel listing group tree with two levels.

The first level is partitioned by the hotel class. The second level is
partitioned by the country region.

Each level is composed of two types of nodes: UNIT and SUBDIVISION.
UNIT nodes serve as a leaf node in a tree and can have bid amount set.
SUBDIVISION nodes serve as an internal node where a subtree will be built. The
SUBDIVISION node can't have bid amount set.
See https://developers.google.com/google-ads/api/docs/hotel-ads/create-listing-groups
for more information.

Note: Only one listing group tree can be added. Attempting to add another
listing group tree to an ad group that already has one will fail.
"""


import argparse
import sys

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

# The next temporary criterion ID to be used, which is a negative integer.
#
# When creating a tree, we need to specify the parent-child relationships
# between nodes. However, until a criterion has been created on the server we do
# not have a criterion ID with which to refer to it.
#
# Instead, we can specify temporary IDs that are specific to a single mutate
# request. Once a criterion is created, it is assigned an ID as normal and the
# temporary ID will no longer refer to it.
#
# See https://developers.google.com/google-ads/api/docs/mutating/best-practices
# for further details.
next_temp_id = -1


def main(client, customer_id, ad_group_id, percent_cpc_bid_micro_amount):
    """Shows how to add a hotel listing group tree with two levels.

    Args:
        client: An initialized GoogleAdsClient instance.
        customer_id: The client customer ID string.
        ad_group_id: The ad group ID for which to the hotel listing will be
            added.
        percent_cpc_bid_micro_amount: The CPC bid micro amount to be set on a
            created ad group criterion.
    """
    # Get the AdGroupCriterionService client.
    ad_group_criterion_service = client.get_service("AdGroupCriterionService")

    operations = []

    # Creates the root of the tree as a SUBDIVISION node.
    root_resource_name = _add_root_node(
        client,
        customer_id,
        ad_group_id,
        operations,
        percent_cpc_bid_micro_amount,
    )

    # Creates child nodes of level 1, partitioned by the hotel class info.
    other_hotel_resource_name = _add_level1_nodes(
        client,
        customer_id,
        ad_group_id,
        root_resource_name,
        operations,
        percent_cpc_bid_micro_amount,
    )

    # Creates child nodes of level 2, partitioned by the hotel country
    # region info.
    _add_level2_nodes(
        client,
        customer_id,
        ad_group_id,
        other_hotel_resource_name,
        operations,
        percent_cpc_bid_micro_amount,
    )

    # Adds the listing group and prints the resulting node resource names.
    mutate_ad_group_criteria_response = ad_group_criterion_service.mutate_ad_group_criteria(
        customer_id=customer_id, operations=operations
    )
    results = mutate_ad_group_criteria_response.results
    print(
        f"Added {len(results)} listing group info entities with resource "
        "names:"
    )
    for ad_group_criterion_result in mutate_ad_group_criteria_response.results:
        print(f"\t'{ad_group_criterion_result.resource_name}'")


def _add_root_node(
    client, customer_id, ad_group_id, operations, percent_cpc_bid_micro_amount
):
    """Creates the root node of the listing group tree.

    Also adds its create operation to the operations list.

    Args:
        client: The Google Ads API client.
        customer_id: The Google Ads customer ID.
        ad_group_id: The ad group ID to which the hotel listing group will be
            added.
        operations: A list of AdGroupCriterionOperations.
        percent_cpc_bid_micro_amount: The CPC bid micro amount to be set on
            created ad group criteria.

    Returns:
        The string resource name of the root of the tree.
    """
    global next_temp_id

    # Create the root of the tree as a SUBDIVISION node.
    root_listing_group_info = _create_listing_group_info(
        client,
        client.get_type("ListingGroupTypeEnum").ListingGroupType.SUBDIVISION,
    )

    root_ad_group_criterion = _create_ad_group_criterion(
        client,
        customer_id,
        ad_group_id,
        root_listing_group_info,
        percent_cpc_bid_micro_amount,
    )

    # Create an operation and add it to the list of operations.
    root_ad_group_criterion_operation = client.get_type(
        "AdGroupCriterionOperation"
    )
    client.copy_from(
        root_ad_group_criterion_operation.create, root_ad_group_criterion
    )
    operations.append(root_ad_group_criterion_operation)

    # Decrement the temp ID for the next ad group criterion.
    next_temp_id -= 1

    return root_ad_group_criterion.resource_name


# [START add_hotel_listing_group_tree]
def _add_level1_nodes(
    client,
    customer_id,
    ad_group_id,
    root_resource_name,
    operations,
    percent_cpc_bid_micro_amount,
):
    """Creates child nodes on level 1, partitioned by the hotel class info.

    Args:
        client: The Google Ads API client.
        customer_id: The Google Ads customer ID.
        ad_group_id: The ad group ID to which the hotel listing group will be
            added.
        root_resource_name: The string resource name of the listing group's root
            node.
        operations: A list of AdGroupCriterionOperations.
        percent_cpc_bid_micro_amount: The CPC bid micro amount to be set on
            created ad group criteria.

    Returns:
        The string resource name of the "other hotel classes" node, which serves
        as the parent node for the next level of the listing tree.
    """
    global next_temp_id

    # Create listing dimension info for 5-star class hotels.
    five_starred_listing_dimension_info = client.get_type(
        "ListingDimensionInfo"
    )
    five_starred_listing_dimension_info.hotel_class.value = 5

    # Create a listing group info for 5-star hotels as a UNIT node.
    five_starred_unit = _create_listing_group_info(
        client,
        client.get_type("ListingGroupTypeEnum").ListingGroupType.UNIT,
        root_resource_name,
        five_starred_listing_dimension_info,
    )

    # Create an ad group criterion for 5-star hotels.
    five_starred_ad_group_criterion = _create_ad_group_criterion(
        client,
        customer_id,
        ad_group_id,
        five_starred_unit,
        percent_cpc_bid_micro_amount,
    )

    # Create an operation and add it to the list of operations.
    five_starred_ad_group_criterion_operation = client.get_type(
        "AdGroupCriterionOperation"
    )
    client.copy_from(
        five_starred_ad_group_criterion_operation.create,
        five_starred_ad_group_criterion,
    )
    operations.append(five_starred_ad_group_criterion_operation)

    # Decrement the temp ID for the next ad group criterion.
    next_temp_id -= 1

    # You can also create more UNIT nodes for other hotel classes by copying the
    # above code in this method and modifying the hotel class value.
    # For instance, passing 4 instead of 5 in the above code will instead create
    # a UNIT node of 4-star hotels.

    # Create hotel class info and dimension info without any specifying
    # attributes. This node will then represent hotel classes other than those
    # already covered by UNIT nodes at this level.
    other_hotels_listing_dimension_info = client.get_type(
        "ListingDimensionInfo"
    )
    # Set "hotel_class" as the oneof field on the ListingDimentionInfo object
    # without specifying the optional hotel_class field.
    client.copy_from(
        other_hotels_listing_dimension_info.hotel_class,
        client.get_type("HotelClassInfo"),
    )

    # Create listing group info for other hotel classes as a SUBDIVISION node,
    # which will be used as a parent node for children nodes of the next level.
    other_hotels_subdivision_listing_group_info = _create_listing_group_info(
        client,
        client.get_type("ListingGroupTypeEnum").ListingGroupType.SUBDIVISION,
        root_resource_name,
        other_hotels_listing_dimension_info,
    )

    # Create an ad group criterion for other hotel classes.
    other_hotels_ad_group_criterion = _create_ad_group_criterion(
        client,
        customer_id,
        ad_group_id,
        other_hotels_subdivision_listing_group_info,
        percent_cpc_bid_micro_amount,
    )

    # Create an operation and add it to the list of operations.
    other_hotels_ad_group_criterion_operation = client.get_type(
        "AdGroupCriterionOperation"
    )
    client.copy_from(
        other_hotels_ad_group_criterion_operation.create,
        other_hotels_ad_group_criterion,
    )
    operations.append(other_hotels_ad_group_criterion_operation)

    # Decrement the temp ID for the next ad group criterion.
    next_temp_id -= 1

    return other_hotels_ad_group_criterion.resource_name
    # [END add_hotel_listing_group_tree]


def _add_level2_nodes(
    client,
    customer_id,
    ad_group_id,
    parent_resource_name,
    operations,
    percent_cpc_bid_micro_amount,
):
    """Creates child nodes on level 2, partitioned by the country region.

    Args:
        client: The Google Ads API client.
        customer_id: The Google Ads customer ID.
        ad_group_id: The ad group ID to which the hotel listing group will be
            added.
        parent_resource_name: The string resource name of the parent criterion
            for the nodes to be added at this level.
        operations: A list of AdGroupCriterionOperations.
        percent_cpc_bid_micro_amount: The CPC bid micro amount to be set on
            created ad group criteria.
    Returns:
        The string resource name of the "other hotel classes" node, which serves
        as the parent node for the next level of the listing tree.
    """
    global next_temp_id

    # Create hotel dimension info for hotels in Japan. The criterion ID for
    # Japan is 2392. See:
    # https://developers.google.com/google-ads/api/reference/data/geotargets for
    # criteria ID of other countries.
    japan_listing_dimension_info = client.get_type("ListingDimensionInfo")
    japan_listing_dimension_info.hotel_country_region.country_region_criterion = client.get_service(
        "GeoTargetConstantService"
    ).geo_target_constant_path(
        2392
    )

    # Create listing group info for hotels in Japan as a UNIT node.
    japan_hotels_unit = _create_listing_group_info(
        client,
        client.get_type("ListingGroupTypeEnum").ListingGroupType.UNIT,
        parent_resource_name,
        japan_listing_dimension_info,
    )

    # Create an ad group criterion for hotels in Japan.
    japan_hotels_ad_group_criterion = _create_ad_group_criterion(
        client,
        customer_id,
        ad_group_id,
        japan_hotels_unit,
        percent_cpc_bid_micro_amount,
    )

    # Create an operation and add it to the list of operations.
    japan_hotels_ad_group_criterion_operation = client.get_type(
        "AdGroupCriterionOperation"
    )
    client.copy_from(
        japan_hotels_ad_group_criterion_operation.create,
        japan_hotels_ad_group_criterion,
    )
    operations.append(japan_hotels_ad_group_criterion_operation)

    # Decrement the temp ID for the next ad group criterion.
    next_temp_id -= 1

    # Create hotel class info and dimension info for hotels in other regions.
    other_hotel_regions_listing_dimension_info = client.get_type(
        "ListingDimensionInfo"
    )
    # Set "hotel_country_region" as the oneof field on the ListingDimensionInfo
    # object without specifying the optional
    # hotel_country_region.country_region_criterion field.
    client.copy_from(
        other_hotel_regions_listing_dimension_info.hotel_country_region,
        client.get_type("HotelCountryRegionInfo"),
    )

    # Create listing group info for hotels in other regions as a UNIT node.
    # The "others" node is always required for every level of the tree.
    other_hotel_regions_unit = _create_listing_group_info(
        client,
        client.get_type("ListingGroupTypeEnum").ListingGroupType.UNIT,
        parent_resource_name,
        other_hotel_regions_listing_dimension_info,
    )

    # Create an ad group criterion for other hotel country regions.
    other_hotel_regions_ad_group_criterion = _create_ad_group_criterion(
        client,
        customer_id,
        ad_group_id,
        other_hotel_regions_unit,
        percent_cpc_bid_micro_amount,
    )

    # Create an operation and add it to the list of operations.
    other_hotel_regions_ad_group_criterion_operation = client.get_type(
        "AdGroupCriterionOperation"
    )
    client.copy_from(
        other_hotel_regions_ad_group_criterion_operation.create,
        other_hotel_regions_ad_group_criterion,
    )
    operations.append(other_hotel_regions_ad_group_criterion_operation)

    # Decrement the temp ID for the next ad group criterion.
    next_temp_id -= 1


def _create_listing_group_info(
    client,
    listing_group_type,
    parent_criterion_resource_name=None,
    case_value=None,
):
    """Creates the listing group info with the provided parameters.

    Args:
        client: The Google Ads API client.
        listing_group_type: The listing group type.
        parent_criterion_resource_name: Optional resource name of the parent
            criterion ID to set for this listing group info.
        case_value: Optional dimension info for the listing group.
    Returns:
        A populated ListingGroupInfo object.
    """
    listing_group_info = client.get_type("ListingGroupInfo")
    listing_group_info.type_ = listing_group_type

    if parent_criterion_resource_name is not None and case_value is not None:
        listing_group_info.parent_ad_group_criterion = (
            parent_criterion_resource_name
        )
        client.copy_from(listing_group_info.case_value, case_value)

    return listing_group_info


def _create_ad_group_criterion(
    client,
    customer_id,
    ad_group_id,
    listing_group_info,
    percent_cpc_bid_micro_amount,
):
    """Creates an ad group criterion from the provided listing group info.

    Bid amount will be set on the created ad group criterion when listing group
    info type is UNIT. Setting bid amount for SUBDIVISION types is not
    allowed.

    Args:
        client: The Google Ads API client.
        customer_id: The Google Ads customer ID.
        ad_group_id: The ad group ID to which the hotel listing group will be
            added.
        listing_group_info: The listing group info to apply to the criterion.
        percent_cpc_bid_micro_amount: The CPC bid micro amount to be set on
            created ad group criteria.
    Returns:
        A populated AdGroupCriterion object.
    """
    ad_group_criterion = client.get_type("AdGroupCriterion")
    ad_group_criterion.status = client.get_type(
        "AdGroupCriterionStatusEnum"
    ).AdGroupCriterionStatus.ENABLED
    client.copy_from(ad_group_criterion.listing_group, listing_group_info)
    ad_group_criterion.resource_name = client.get_service(
        "AdGroupCriterionService"
    ).ad_group_criterion_path(customer_id, ad_group_id, next_temp_id)

    # Bids are only valid for UNIT nodes.
    if (
        listing_group_info.type_
        == client.get_type("ListingGroupTypeEnum").ListingGroupType.UNIT
    ):
        ad_group_criterion.percent_cpc_bid_micros = percent_cpc_bid_micro_amount

    return ad_group_criterion


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v8")

    parser = argparse.ArgumentParser(
        description="Shows how to add a hotel listing group tree with two "
        "levels."
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
        type=int,
        required=True,
        help="The ad group ID to which the hotel listing will be added.",
    )
    parser.add_argument(
        "-p",
        "--percent_cpc_bid_micro_amount",
        type=int,
        required=True,
        help="Specify the CPC bid micro amount to be set on a created ad group "
        "criterion. For simplicity, each ad group criterion will use the below "
        "amount equally. In practice, you probably want to use different "
        "values for each ad group criterion.",
    )
    args = parser.parse_args()

    try:
        main(
            googleads_client,
            args.customer_id,
            args.ad_group_id,
            args.percent_cpc_bid_micro_amount,
        )
    except GoogleAdsException as ex:
        print(
            f"Request with ID '{ex.request_id}'' failed with status "
            f"'{ex.error.code().name}' and includes the following errors:"
        )
        for error in ex.failure.errors:
            print(f"\tError with message '{error.message}'.")
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print(f"\t\tOn field: {field_path_element.field_name}")
        sys.exit(1)
