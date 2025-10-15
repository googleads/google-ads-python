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
"""This example shows how to link a manager customer to a client customer."""

import argparse
import sys

from google.api_core import protobuf_helpers
from google.protobuf.field_mask_pb2 import FieldMask

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.ads.googleads.v22.services.services.customer_client_link_service.client import (
    CustomerClientLinkServiceClient,
)
from google.ads.googleads.v22.services.types.customer_client_link_service import (
    CustomerClientLinkOperation,
    MutateCustomerClientLinkResponse,
)
from google.ads.googleads.v22.resources.types.customer_client_link import (
    CustomerClientLink,
)
from google.ads.googleads.v22.services.services.google_ads_service.client import (
    GoogleAdsServiceClient,
)
from google.ads.googleads.v22.services.types.google_ads_service import (
    SearchPagedResponse,
    GoogleAdsRow,
)
from google.ads.googleads.v22.services.services.customer_manager_link_service.client import (
    CustomerManagerLinkServiceClient,
)
from google.ads.googleads.v22.services.types.customer_manager_link_service import (
    CustomerManagerLinkOperation,
    MutateCustomerManagerLinkResponse,
)
from google.ads.googleads.v22.resources.types.customer_manager_link import (
    CustomerManagerLink,
)

# ManagerLinkStatusEnum is used via client.enums


# [START link_manager_to_client]
def main(
    client: GoogleAdsClient, customer_id: str, manager_customer_id: str
) -> None:
    # This example assumes that the same credentials will work for both
    # customers, but that may not be the case. If you need to use different
    # credentials for each customer, then you may either update the client
    # configuration or instantiate two clients, where at least one points to
    # a specific configuration file so that both clients don't read the same
    # file located in the $HOME dir.
    customer_client_link_service: CustomerClientLinkServiceClient = (
        client.get_service("CustomerClientLinkService")
    )

    # Extend an invitation to the client while authenticating as the manager.
    client_link_operation: CustomerClientLinkOperation = client.get_type(
        "CustomerClientLinkOperation"
    )
    client_link: CustomerClientLink = client_link_operation.create
    client_link.client_customer = customer_client_link_service.customer_path(
        customer_id
    )
    # client_link.status expects an enum value (int)
    client_link.status = client.enums.ManagerLinkStatusEnum.PENDING.value

    response: MutateCustomerClientLinkResponse = (
        customer_client_link_service.mutate_customer_client_link(
            customer_id=manager_customer_id, operation=client_link_operation
        )
    )
    resource_name: str = response.results[0].resource_name

    print(
        f'Extended an invitation from customer "{manager_customer_id}" to '
        f'customer "{customer_id}" with client link resource_name '
        f'"{resource_name}"'
    )

    # Find the manager_link_id of the link we just created, so we can construct
    # the resource name for the link from the client side. Note that since we
    # are filtering by resource_name, a unique identifier, only one
    # customer_client_link resource will be returned in the response
    query = f'''
        SELECT
            customer_client_link.manager_link_id
        FROM
            customer_client_link
        WHERE
            customer_client_link.resource_name = "{resource_name}"'''

    ga_service: GoogleAdsServiceClient = client.get_service("GoogleAdsService")
    manager_link_id: int = -1  # Initialize with a default value

    try:
        search_response: SearchPagedResponse = ga_service.search(
            customer_id=manager_customer_id, query=query
        )
        # Since the googleads_service.search method returns an iterator we need
        # to initialize an iteration in order to retrieve results, even though
        # we know the query will only return a single row.
        row: GoogleAdsRow
        for row in search_response:  # Assuming direct iteration
            manager_link_id = row.customer_client_link.manager_link_id
    except GoogleAdsException as ex:
        # handle_googleads_exception(ex) # This function is not defined here
        print(f"GoogleAdsException: {ex}")  # Basic error handling
        sys.exit(1)

    customer_manager_link_service: CustomerManagerLinkServiceClient = (
        client.get_service("CustomerManagerLinkService")
    )
    manager_link_operation: CustomerManagerLinkOperation = client.get_type(
        "CustomerManagerLinkOperation"
    )
    manager_link: CustomerManagerLink = manager_link_operation.update
    manager_link.resource_name = (
        customer_manager_link_service.customer_manager_link_path(
            customer_id,
            manager_customer_id,
            manager_link_id,  # type: ignore
        )
    )

    # manager_link.status expects an enum value (int)
    manager_link.status = client.enums.ManagerLinkStatusEnum.ACTIVE.value
    # manager_link_operation.update_mask is a FieldMask
    update_mask: FieldMask = protobuf_helpers.field_mask(None, manager_link._pb)
    client.copy_from(
        manager_link_operation.update_mask,
        update_mask,
    )

    mutate_manager_link_response: MutateCustomerManagerLinkResponse = (
        customer_manager_link_service.mutate_customer_manager_link(
            customer_id=customer_id, operations=[manager_link_operation]
        )
    )
    print(
        "Client accepted invitation with resource_name: "
        f'"{mutate_manager_link_response.results[0].resource_name}"'
    )
    # [END link_manager_to_client]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=(
            "Links an existing manager customer to an existing"
            "client customer"
        )
    )
    # The following argument(s) should be provided to run the example.
    parser.add_argument(
        "-c", "--customer_id", type=str, required=True, help="The customer ID."
    )
    parser.add_argument(
        "-m",
        "--manager_customer_id",
        type=str,
        required=True,
        help="The manager customer ID.",
    )
    args = parser.parse_args()

    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v22")
    try:
        main(googleads_client, args.customer_id, args.manager_customer_id)
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
