#!/usr/bin/env python
# Copyright 2021 Google LLC
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
"""Gets the account information of the given MCC and login customer."""


import argparse
import sys
from typing import Optional, Dict, List, Any

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

_DEFAULT_LOG_SPACE_LENGTH = 4


def account_hierarchy_module(google_ads_client: GoogleAdsClient, customer_id: Optional[str]):
    """Print the account hierarchy for the given login customer ID.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: the given customer ID for getting the hierarchy info.
    """
    googleads_service = google_ads_client.get_service("GoogleAdsService")
    customer_service = google_ads_client.get_service("CustomerService")
    # A collection of customer IDs to handle.
    seed_customer_ids = []

    # If a manager ID was provided in the customer ID parameter, it will be
    # the only ID in the list. Otherwise, we will issue a request for all
    # customers accessible by this authenticated Google account.
    if customer_id:
        seed_customer_ids = [customer_id]
    else:
        print(
            "No manager ID is specified. The example will print the "
            "hierarchies of all accessible customer IDs."
        )
        # Starting in v10 this will list all customers, not just customers with
        # ENABLED status. If you wish to only show ENABLED customers, you can
        # further filter by the Customer.status field.
        accessible_customers = customer_service.list_accessible_customers()
        customer_resource_names = accessible_customers.resource_names
        print(f"Total results: {len(customer_resource_names)}")
        for resource_name in customer_resource_names:
            print(f'Customer resource name: "{resource_name}"')
            seed_customer_ids.append(resource_name.split("/")[1])

    # Creates a query that retrieves all child accounts of the manager
    # specified in search calls below.
    query = """
        SELECT
            customer_client.client_customer,
            customer_client.level,
            customer_client.manager,
            customer_client.descriptive_name,
            customer_client.currency_code,
            customer_client.time_zone,
            customer_client.id
        FROM customer_client
        WHERE customer_client.level <= 1"""

    for seed_customer_id in seed_customer_ids:
        # Performs a breadth-first search to build a Dictionary that maps
        # managers to their child accounts (customer_ids_to_child_accounts).
        unprocessed_customer_ids = [seed_customer_id]
        customer_ids_to_child_accounts: Dict[str, List[Any]] = dict()
        root_customer_client = None

        while unprocessed_customer_ids:
            customer_id = unprocessed_customer_ids.pop(0)
            response = googleads_service.search(
                customer_id=customer_id, query=query
            )

            # Iterates over all rows in all pages to get all customer
            # clients under the specified customer's hierarchy.
            for row in response:
                customer_client = row.customer_client

                # The customer client with level 0 is the specified customer.
                if customer_client.level == 0:
                    if root_customer_client is None:
                        root_customer_client = customer_client
                    # If it's level 0, we need to skip this round of loop.
                    continue

                # For all level 1 (direct child) accounts that are a
                # manager account, the above query will be run against them
                # to create a dictionary of managers mapped to their child
                # accounts for printing the hierarchy afterwards.
                if customer_id not in customer_ids_to_child_accounts:
                    customer_ids_to_child_accounts[customer_id] = []

                customer_ids_to_child_accounts[customer_id].append(
                    customer_client
                )

                if customer_client.manager:
                    # A customer can be managed by multiple managers, so to
                    # prevent visiting the same customer many times, we
                    # need to check if it's already in the dictionary.
                    if (
                        customer_client.id not in customer_ids_to_child_accounts
                        and customer_client.level == 1
                    ):
                        unprocessed_customer_ids.append(customer_client.id)

        if root_customer_client is not None:
            print(
                "\nThe hierarchy of customer ID "
                f"{root_customer_client.id} is printed below:"
            )
            print_account_hierarchy(
                root_customer_client, customer_ids_to_child_accounts, 0
            )
        else:
            print(f"No hierarchy info was found for Customer ID {customer_id}.")


def print_account_hierarchy(
    customer_client: Any, customer_ids_to_child_accounts: Dict[str, List[Any]], depth: int
):
    """Prints the specified account's hierarchy using recursion.

    Args:
        customer_client: a customer_client resource that contains current
            account information.
        customer_ids_to_child_accounts: a mapping between customer_ids and
            their child accounts.
        depth: the current depth from the root node.
    """
    if depth == 0:
        print("Customer ID (Descriptive Name, Currency Code, Time Zone)")
    customer_id = str(customer_client.id)
    print("-" * (depth * _DEFAULT_LOG_SPACE_LENGTH + 1), end="")
    print(
        f"{customer_id} ({customer_client.descriptive_name}, "
        f"{customer_client.currency_code}, "
        f"{customer_client.time_zone})"
    )
    # Recursively call this function for all child accounts of customer_client.
    if customer_id in customer_ids_to_child_accounts:
        for child_account in customer_ids_to_child_accounts[customer_id]:
            print_account_hierarchy(
                child_account, customer_ids_to_child_accounts, depth + 1
            )


def get_users_module(google_ads_client: GoogleAdsClient, customer_id: Optional[str]):
    """Prints the user access information for the given customer_id.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: the given customer ID for retrieving customer user access
            info.
    """
    googleads_service = google_ads_client.get_service("GoogleAdsService")
    customer_service = google_ads_client.get_service("CustomerService")
    query = """
    SELECT
      customer_user_access.user_id,
      customer_user_access.email_address,
      customer_user_access.access_role,
      customer_user_access.access_creation_date_time,
      customer_user_access.inviter_user_email_address
    FROM customer_user_access
    """
    response = googleads_service.search(customer_id=customer_id, query=query)

    for customer_user_access in response:
        user_access = customer_user_access.customer_user_access
        print(
            "The given customer ID has access to the client account with ID "
            f"{user_access.user_id}, with an access role of "
            f"'{user_access.access_role.name}', and creation time of "
            f"'{user_access.access_creation_date_time}'."
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="This analyzer will display the account info "
        "according to the input."
    )
    # process argument(s)
    parser.add_argument(
        "-c",
        "--customer_id",
        type=str,
        required=False,
        help="The Google Ads customer ID.",
    )
    args = parser.parse_args()

    try:
        # GoogleAdsClient will read the google-ads.yaml configuration file in
        # the home directory if none is specified.
        googleads_client = GoogleAdsClient.load_from_storage()
        account_hierarchy_module(googleads_client, args.customer_id)
        get_users_module(googleads_client, args.customer_id)
    except GoogleAdsException as ex:
        print(
            f'Request with ID "{ex.request_id}" failed with status '
            f'"{ex.error.code().name}" '
        )
        print("And includes the following errors:")
        for error in ex.failure.errors:
            print(f'\tError with message "{error.message}".')
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print(f"\t\tOn field: {field_path_element.field_name}")
        sys.exit(1)
