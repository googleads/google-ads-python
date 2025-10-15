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
"""Shows how to add product partitions to a Performance Max retail campaign.

For Performance Max campaigns, product partitions are represented using the
AssetGroupListingGroupFilter resource. This resource can be combined with
itself to form a hierarchy that creates a product partition tree.

For more information about Performance Max retail campaigns, see the
shopping_ads/add_performance_max_retail_campaign.py example.
"""


import argparse
import sys
from typing import Dict, List, Optional

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.ads.googleads.v22.resources.types.asset_group_listing_group_filter import (
    ListingGroupFilterDimension,
)
from google.ads.googleads.v22.resources.types.asset_group_listing_group_filter import (
    AssetGroupListingGroupFilter,
)
from google.ads.googleads.v22.services.services.google_ads_service import (
    GoogleAdsServiceClient,
)
from google.ads.googleads.v22.services.types.google_ads_service import (
    MutateGoogleAdsResponse,
    SearchGoogleAdsRequest,
    SearchGoogleAdsResponse,
)
from google.ads.googleads.v22.services.types.google_ads_service import (
    MutateOperation,
)


# We specify temporary IDs that are specific to a single mutate request.
# Temporary IDs are always negative and unique within one mutate request.
#
# See https://developers.google.com/google-ads/api/docs/mutating/best-practices
# for further details.
#
# These temporary IDs are fixed because they are used in multiple places.
_TEMPORARY_ID_LISTING_GROUP_ROOT: int = -1


class AssetGroupListingGroupFilterRemoveOperationFactory:
    def __init__(
        self,
        client: GoogleAdsClient,
        listing_group_filters: List[AssetGroupListingGroupFilter],
    ):
        """Factory class for creating sorted list of MutateOperations.

        The operations remove the given tree of AssetGroupListingGroupFilters,
        When removing these listing group filters, the remove operations must be
        sent in a specific order that removes leaf nodes before removing parent
        nodes.

        Args:
            client: an initialized GoogleAdsClient instance.
            listing_group_filters: a list of AssetGroupListingGroupFilters.
        """
        if not listing_group_filters:
            raise ValueError("No listing group filters to remove.")

        self.client: GoogleAdsClient = client
        self.root_resource_name: Optional[str] = None
        self.parents_to_children: Dict[str, List[str]] = {}

        # Process the given list of listing group filters to identify the root
        # node and any parent to child edges in the tree.
        for listing_group_filter_node in listing_group_filters:
            resource_name: str = listing_group_filter_node.resource_name
            parent_resource_name: Optional[str] = (
                listing_group_filter_node.parent_listing_group_filter
            )

            # When the node has no parent, it means it's the root node.
            if not parent_resource_name:
                if self.root_resource_name:
                    # Check if another root node has already been detected and
                    # raise an error if so, as only one root node can exist for
                    # a given tree.
                    raise ValueError("More than one listing group parent node.")
                else:
                    self.root_resource_name = resource_name
            else:
                # Check if we've already visited a sibling in this group, and
                # either update it or create a new branch accordingly.
                if parent_resource_name in self.parents_to_children:
                    # If we've visited a sibling already, add this resource
                    # name to the existing list.
                    self.parents_to_children[parent_resource_name].append(
                        resource_name
                    )
                else:
                    # If we haven't visited any siblings, then create a new list
                    # for this parent node and add this resource name to it.
                    self.parents_to_children[parent_resource_name] = [
                        resource_name
                    ]

    # [START add_performance_max_product_listing_group_tree_2]
    def remove_all(self) -> List[MutateOperation]:
        """Creates a list of MutateOperations for the listing group filter tree.

        Returns:
            A list of MutateOperations that remove each specified
            AssetGroupListingGroupFilter in the tree passed in when this
            class was initialized.
        """
        if not self.root_resource_name:
            # This case should ideally be prevented by the __init__ check,
            # but as a safeguard for type checking remove_descendants_and_filter.
            return []
        return self.remove_descendants_and_filter(self.root_resource_name)
        # [END add_performance_max_product_listing_group_tree_2]

    # [START add_performance_max_product_listing_group_tree_3]
    def remove_descendants_and_filter(
        self, resource_name: str
    ) -> List[MutateOperation]:
        """Builds a post-order sorted list of MutateOperations.

        Creates a list of MutateOperations that remove all the descendents of
        the specified AssetGroupListingGroupFilter resource name. The order of
        removal is post-order, where all the children (and their children,
        recursively) are removed first. Then, the root node itself is removed.

        Args:
            resource_name: an AssetGroupListingGroupFilter resource name.

        Returns:
            a sorted list of MutateOperations.
        """
        operations: List[MutateOperation] = []

        # Check if resource name is a parent.
        if resource_name in self.parents_to_children:
            # If this resource name is a parent, call this method recursively
            # on each of its children.
            for child_resource_name in self.parents_to_children[resource_name]:
                operations.extend(
                    self.remove_descendants_and_filter(child_resource_name)
                )

        mutate_operation: MutateOperation = self.client.get_type(
            "MutateOperation"
        )
        mutate_operation.asset_group_listing_group_filter_operation.remove = (
            resource_name
        )
        operations.append(mutate_operation)

        return operations
        # [END add_performance_max_product_listing_group_tree_3]


class AssetGroupListingGroupFilterCreateOperationFactory:
    def __init__(
        self,
        client: GoogleAdsClient,
        customer_id: str,
        asset_group_id: int,  # Will be str for path construction
        root_listing_id: int,
    ):
        """A factory class for creating MutateOperations.

        These operations create new AssetGroupListingGroupFilterMutateOperation
        instances using the given customer ID and asset group ID.

        Args:
            client: an initialized GoogleAdsClient instance.
            customer_id: a client customer ID.
            asset_group_id: the asset group id for the Performance Max campaign.
            root_listing_id: a temporary ID to use as the listing group root.
        """
        self.client: GoogleAdsClient = client
        self.customer_id: str = customer_id
        # asset_group_id is used as a string in path construction.
        self.asset_group_id: str = str(asset_group_id)
        self.root_listing_id: int = root_listing_id
        self.next_temp_id: int = self.root_listing_id - 1

    def next_id(self) -> int:
        """Returns the next temporary ID for use in a sequence.

        The temporary IDs are used in the list of MutateOperations in order to
        refer to objects in the request that aren't in the API yet. For more
        details see:
        https://developers.google.com/google-ads/api/docs/mutating/best-practices#temporary_resource_names

        Returns:
            A new temporary ID.
        """
        self.next_temp_id -= 1
        return self.next_temp_id

    # [START add_performance_max_product_listing_group_tree_4]
    def create_root(self) -> MutateOperation:
        """Creates a MutateOperation to add a root AssetGroupListingGroupFilter.

        Returns:
            A MutateOperation for a new AssetGroupListingGroupFilter.
        """
        googleads_service: GoogleAdsServiceClient = self.client.get_service(
            "GoogleAdsService"
        )

        mutate_operation: MutateOperation = self.client.get_type(
            "MutateOperation"
        )
        asset_group_listing_group_filter: AssetGroupListingGroupFilter = (
            mutate_operation.asset_group_listing_group_filter_operation.create
        )

        asset_group_listing_group_filter.resource_name = (
            googleads_service.asset_group_listing_group_filter_path(
                self.customer_id,
                self.asset_group_id,
                str(self.root_listing_id),
            )
        )
        asset_group_listing_group_filter.asset_group = (
            googleads_service.asset_group_path(
                self.customer_id, self.asset_group_id
            )
        )
        # Since this is the root node, do not set the
        # parent_listing_group_filter field. For all other nodes, this would
        # refer to the parent listing group filter resource name.
        # asset_group_listing_group_filter.parent_listing_group_filter = "<PARENT FILTER NAME>"

        # Unlike the add_performance_max_retail_campaign example, the type for
        # the root node here must be a subdivision because we add child
        # partitions under it.
        asset_group_listing_group_filter.type_ = (
            self.client.enums.ListingGroupFilterTypeEnum.SUBDIVISION
        )

        # Because this is a Performance Max campaign for retail, we need to
        # specify that this is a shopping listing source.
        asset_group_listing_group_filter.listing_source = (
            self.client.enums.ListingGroupFilterListingSourceEnum.SHOPPING
        )

        return mutate_operation
        # [END add_performance_max_product_listing_group_tree_4]

    # [START add_performance_max_product_listing_group_tree_5]
    def create_subdivision(
        self,
        parent_id: int,
        temporary_id: int,
        dimension: ListingGroupFilterDimension,
    ) -> MutateOperation:
        """Creates a MutateOperation to add an AssetGroupListingGroupFilter.

        Use this method if the filter will have child filters. Otherwise use
        the create_unit method.

        Args:
            parent_id: the ID of the parent AssetGroupListingGroupFilter.
            temporary_id: a temporary ID for the operation being created.
            dimension: The dimension to associate with this new
                AssetGroupListingGroupFilter.

        Returns:
            a MutateOperation for a new AssetGroupListingGroupFilter
        """
        googleads_service: GoogleAdsServiceClient = self.client.get_service(
            "GoogleAdsService"
        )

        mutate_operation: MutateOperation = self.client.get_type(
            "MutateOperation"
        )
        asset_group_listing_group_filter: AssetGroupListingGroupFilter = (
            mutate_operation.asset_group_listing_group_filter_operation.create
        )

        asset_group_listing_group_filter.resource_name = (
            googleads_service.asset_group_listing_group_filter_path(
                self.customer_id, self.asset_group_id, str(temporary_id)
            )
        )
        asset_group_listing_group_filter.asset_group = (
            googleads_service.asset_group_path(
                self.customer_id, self.asset_group_id
            )
        )
        asset_group_listing_group_filter.parent_listing_group_filter = (
            googleads_service.asset_group_listing_group_filter_path(
                self.customer_id, self.asset_group_id, str(parent_id)
            )
        )
        # We must use the Subdivision type to indicate that the
        # AssetGroupListingGroupFilter will have children.
        asset_group_listing_group_filter.type_ = (
            self.client.enums.ListingGroupFilterTypeEnum.SUBDIVISION
        )
        # Because this is a Performance Max campaign for retail, we need to
        # specify that this is in the shopping listing source.
        asset_group_listing_group_filter.listing_source = (
            self.client.enums.ListingGroupFilterListingSourceEnum.SHOPPING
        )
        asset_group_listing_group_filter.case_value = dimension

        return mutate_operation
        # [END add_performance_max_product_listing_group_tree_5]

    # [START add_performance_max_product_listing_group_tree_6]
    def create_unit(
        self,
        parent_id: int,
        temporary_id: int,
        dimension: ListingGroupFilterDimension,
    ) -> MutateOperation:
        """Creates a MutateOperation to add an AssetGroupListingGroupFilter.

        Use this method if the filter will not have child filters. Otherwise use
        the create_subdivision method.

        Args:
            parent_id: the ID of the parent AssetGroupListingGroupFilter.
            temporary_id: a temporary ID for the operation being created.
            dimension: The dimension to associate with this new
                AssetGroupListingGroupFilter.

        Returns:
            a MutateOperation for a new AssetGroupListingGroupFilter
        """
        googleads_service: GoogleAdsServiceClient = self.client.get_service(
            "GoogleAdsService"
        )

        mutate_operation: MutateOperation = self.client.get_type(
            "MutateOperation"
        )
        asset_group_listing_group_filter: AssetGroupListingGroupFilter = (
            mutate_operation.asset_group_listing_group_filter_operation.create
        )

        asset_group_listing_group_filter.resource_name = (
            googleads_service.asset_group_listing_group_filter_path(
                self.customer_id, self.asset_group_id, str(temporary_id)
            )
        )
        asset_group_listing_group_filter.asset_group = (
            googleads_service.asset_group_path(
                self.customer_id, self.asset_group_id
            )
        )
        asset_group_listing_group_filter.parent_listing_group_filter = (
            googleads_service.asset_group_listing_group_filter_path(
                self.customer_id, self.asset_group_id, str(parent_id)
            )
        )
        # We must use the UnitIncluded type to indicate that the
        # AssetGroupListingGroupFilter won't have children.
        asset_group_listing_group_filter.type_ = (
            self.client.enums.ListingGroupFilterTypeEnum.UNIT_INCLUDED
        )
        # Because this is a Performance Max campaign for retail, we need to
        # specify that this is in the shopping listing source.
        asset_group_listing_group_filter.listing_source = (
            self.client.enums.ListingGroupFilterListingSourceEnum.SHOPPING
        )
        asset_group_listing_group_filter.case_value = dimension

        return mutate_operation
        # [END add_performance_max_product_listing_group_tree_6]


# [START add_performance_max_product_listing_group_tree]
def main(
    client: GoogleAdsClient,
    customer_id: str,
    asset_group_id: int,  # Will be str for path construction
    replace_existing_tree: bool,
) -> None:
    """The main method that creates all necessary entities for the example.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        asset_group_id: the asset group id for the Performance Max campaign.
        replace_existing_tree: option to remove existing product tree from the
            passed in asset group.
    """
    googleads_service: GoogleAdsServiceClient = client.get_service(
        "GoogleAdsService"
    )
    # asset_group_id is used as a string in path construction.
    asset_group_resource_name: str = googleads_service.asset_group_path(
        customer_id, str(asset_group_id)
    )
    operations: List[MutateOperation] = []

    if replace_existing_tree:
        # Retrieve a list of existing AssetGroupListingGroupFilters
        existing_listing_group_filters: List[AssetGroupListingGroupFilter] = (
            get_all_existing_listing_group_filter_assets_in_asset_group(
                client, customer_id, asset_group_resource_name
            )
        )

        # If present, create MutateOperations to remove each
        # AssetGroupListingGroupFilter and add them to the list of operations.
        if existing_listing_group_filters:
            remove_operation_factory = (
                AssetGroupListingGroupFilterRemoveOperationFactory(
                    client, existing_listing_group_filters
                )
            )
            operations.extend(remove_operation_factory.remove_all())

    create_operation_factory = (
        AssetGroupListingGroupFilterCreateOperationFactory(
            client,
            customer_id,
            asset_group_id,  # Pass as int, will be converted to str in __init__
            _TEMPORARY_ID_LISTING_GROUP_ROOT,
        )
    )

    operations.append(create_operation_factory.create_root())

    new_dimension: ListingGroupFilterDimension = client.get_type(
        "ListingGroupFilterDimension"
    )
    new_dimension.product_condition.condition = (
        client.enums.ListingGroupFilterProductConditionEnum.NEW
    )
    operations.append(
        create_operation_factory.create_unit(
            _TEMPORARY_ID_LISTING_GROUP_ROOT,
            create_operation_factory.next_id(),
            new_dimension,
        )
    )

    used_dimension: ListingGroupFilterDimension = client.get_type(
        "ListingGroupFilterDimension"
    )
    used_dimension.product_condition.condition = (
        client.enums.ListingGroupFilterProductConditionEnum.USED
    )
    operations.append(
        create_operation_factory.create_unit(
            _TEMPORARY_ID_LISTING_GROUP_ROOT,
            create_operation_factory.next_id(),
            used_dimension,
        )
    )

    # We save this ID because create child nodes underneath it.
    subdivision_id_condition_other: int = create_operation_factory.next_id()

    # All sibling nodes must have the same dimension type. We use an empty
    # product_condition to indicate that this is an "Other" partition.
    other_dimension: ListingGroupFilterDimension = client.get_type(
        "ListingGroupFilterDimension"
    )
    # This triggers the presence of the product_condition field without
    # specifying any field values. This is important in order to tell the API
    # that this is an "other" node.
    other_dimension.product_condition._pb.SetInParent()
    # We're calling create_subdivision because this listing group will have
    # children.
    operations.append(
        create_operation_factory.create_subdivision(
            _TEMPORARY_ID_LISTING_GROUP_ROOT,
            subdivision_id_condition_other,
            other_dimension,
        )
    )

    cool_dimension: ListingGroupFilterDimension = client.get_type(
        "ListingGroupFilterDimension"
    )
    cool_dimension.product_brand.value = "CoolBrand"
    operations.append(
        create_operation_factory.create_unit(
            subdivision_id_condition_other,
            create_operation_factory.next_id(),
            cool_dimension,
        )
    )

    cheap_dimension: ListingGroupFilterDimension = client.get_type(
        "ListingGroupFilterDimension"
    )
    cheap_dimension.product_brand.value = "CheapBrand"
    operations.append(
        create_operation_factory.create_unit(
            subdivision_id_condition_other,
            create_operation_factory.next_id(),
            cheap_dimension,
        )
    )

    empty_dimension: ListingGroupFilterDimension = client.get_type(
        "ListingGroupFilterDimension"
    )
    # This triggers the presence of the product_brand field without specifying
    # any field values. This is important in order to tell the API
    # that this is an "other" node.
    empty_dimension.product_brand._pb.SetInParent()
    operations.append(
        create_operation_factory.create_unit(
            subdivision_id_condition_other,
            create_operation_factory.next_id(),
            empty_dimension,
        )
    )

    response: MutateGoogleAdsResponse = googleads_service.mutate(
        customer_id=customer_id, mutate_operations=operations
    )

    print_response_details(operations, response)
    # [END add_performance_max_product_listing_group_tree]


# [START add_performance_max_product_listing_group_tree_7]
def get_all_existing_listing_group_filter_assets_in_asset_group(
    client: GoogleAdsClient,
    customer_id: str,
    asset_group_resource_name: str,
) -> List[AssetGroupListingGroupFilter]:
    """Fetches all of the listing group filters in an asset group.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        asset_group_resource_name: the asset group resource name for the
            Performance Max campaign.

    Returns:
        a list of AssetGroupListingGroupFilters.
    """
    query: str = f"""
        SELECT
          asset_group_listing_group_filter.resource_name,
          asset_group_listing_group_filter.parent_listing_group_filter
        FROM asset_group_listing_group_filter
        WHERE asset_group_listing_group_filter.asset_group = '{asset_group_resource_name}'"""

    request: SearchGoogleAdsRequest = client.get_type("SearchGoogleAdsRequest")
    request.customer_id = customer_id
    request.query = query

    googleads_service: GoogleAdsServiceClient = client.get_service(
        "GoogleAdsService"
    )
    response: SearchGoogleAdsResponse = googleads_service.search(
        request=request
    )

    return [
        result.asset_group_listing_group_filter
        for result in response
        if result.asset_group_listing_group_filter
    ]
    # [END add_performance_max_product_listing_group_tree_7]


def print_response_details(
    mutate_operations: List[MutateOperation], response: MutateGoogleAdsResponse
) -> None:
    """Prints the details of the GoogleAdsService.Mutate request.

    This uses the original list of mutate operations to map the operation
    result to what was sent. It can be assumed that the initial set of
    operations and the list returned in the response are in the same order.

    Args:
        mutate_operations: a list of MutateOperation instances.
        response: a GoogleAdsMutateResponse instance.
    """
    # Parse the Mutate response to print details about the entities that were
    # created in the request.
    for i, result_operation in enumerate(response.mutate_operation_responses):
        requested_operation: MutateOperation = mutate_operations[i]
        resource_name: str = (
            result_operation.asset_group_listing_group_filter_result.resource_name
        )

        # Check the operation type for the requested operation in order to
        # log whether it was a remove or a create request.
        if (
            requested_operation.asset_group_listing_group_filter_operation.remove
        ):
            print(
                "Removed an AssetGroupListingGroupFilter with resource name: "
                f"'{resource_name}'."
            )
        elif (
            requested_operation.asset_group_listing_group_filter_operation.create
        ):
            print(
                "Created an AssetGroupListingGroupFilter with resource name: "
                f"'{resource_name}'."
            )
        else:
            print("An unknown operation was returned.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=(
            "Adds product partitions to a Performance Max retail campaign."
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
        "-a",
        "--asset_group_id",
        type=int,  # Keep as int for argparse, convert to str for API usage
        required=True,
        help="The asset group id for the Performance Max campaign.",
    )
    parser.add_argument(
        "-r",
        "--replace_existing_tree",
        action="store_true",
        help=(
            "Whether or not to replace the existing product partition tree. "
            "If the current AssetGroup already has a tree of "
            "ListingGroupFilters, attempting to add a new set of "
            "ListingGroupFilters including a root filter will result in an "
            "ASSET_GROUP_LISTING_GROUP_FILTER_ERROR_MULTIPLE_ROOTS error. "
            "Setting this option to true will remove the existing tree and "
            "prevent this error."
        ),
    )

    args: argparse.Namespace = parser.parse_args()

    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client: GoogleAdsClient = GoogleAdsClient.load_from_storage(
        version="v22"
    )

    try:
        main(
            googleads_client,
            args.customer_id,
            args.asset_group_id,  # Pass as int, main will handle conversion
            args.replace_existing_tree,
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
