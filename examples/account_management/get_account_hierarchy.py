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
"""Gets the account hierarchy of the given MCC and login customer ID.

If you don't specify manager ID and login customer ID, the example will instead
print the hierarchies of all accessible customer accounts for your
authenticated Google account. Note that if the list of accessible customers for
your authenticated Google account includes accounts within the same hierarchy,
this example will retrieve and print the overlapping portions of the hierarchy
for each accessible customer.
"""

import argparse
import sys

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


def main(client, login_customer_id=None):
    """Gets the account hierarchy of the given MCC and login customer ID.

    Args:
      client: The Google Ads client.
      login_customer_id: Optional manager account ID. If none provided, this
      method will instead list the accounts accessible from the
      authenticated Google Ads account.
    """

    # Gets instances of the GoogleAdsService and CustomerService clients.
    googleads_service = client.get_service("GoogleAdsService")
    customer_service = client.get_service("CustomerService")

    # A collection of customer IDs to handle.
    seed_customer_ids = []

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

    # If a Manager ID was provided in the customerId parameter, it will be
    # the only ID in the list. Otherwise, we will issue a request for all
    # customers accessible by this authenticated Google account.
    if login_customer_id is not None:
        seed_customer_ids = [login_customer_id]
    else:
        print(
            "No manager ID is specified. The example will print the "
            "hierarchies of all accessible customer IDs."
        )

        customer_resource_names = (
            customer_service.list_accessible_customers().resource_names
        )

        for customer_resource_name in customer_resource_names:
            customer = customer_service.get_customer(
                resource_name=customer_resource_name
            )
            print(customer.id)
            seed_customer_ids.append(customer.id)

    for seed_customer_id in seed_customer_ids:
        # Performs a breadth-first search to build a Dictionary that maps
        # managers to their child accounts (customerIdsToChildAccounts).
        unprocessed_customer_ids = [seed_customer_id]
        customer_ids_to_child_accounts = dict()
        root_customer_client = None

        while unprocessed_customer_ids:
            customer_id = int(unprocessed_customer_ids.pop(0))
            response = googleads_service.search(
                customer_id=str(customer_id), query=query
            )

            # Iterates over all rows in all pages to get all customer
            # clients under the specified customer's hierarchy.
            for googleads_row in response:
                customer_client = googleads_row.customer_client

                # The customer client that with level 0 is the specified
                # customer.
                if customer_client.level == 0:
                    if root_customer_client is None:
                        root_customer_client = customer_client
                    continue

                # For all level-1 (direct child) accounts that are a
                # manager account, the above query will be run against them
                # to create a Dictionary of managers mapped to their child
                # accounts for printing the hierarchy afterwards.
                if customer_id not in customer_ids_to_child_accounts:
                    customer_ids_to_child_accounts[customer_id] = []

                customer_ids_to_child_accounts[customer_id].append(
                    customer_client
                )

                if customer_client.manager:
                    # A customer can be managed by multiple managers, so to
                    # prevent visiting the same customer many times, we
                    # need to check if it's already in the Dictionary.
                    if (
                        customer_client.id not in customer_ids_to_child_accounts
                        and customer_client.level == 1
                    ):
                        unprocessed_customer_ids.append(customer_client.id)

        if root_customer_client is not None:
            print(
                "The hierarchy of customer ID "
                f"{root_customer_client.id} is printed below:"
            )
            _print_account_hierarchy(
                root_customer_client, customer_ids_to_child_accounts, 0
            )
        else:
            print(
                f"Customer ID {login_customer_id} is likely a test "
                "account, so its customer client information cannot be "
                "retrieved."
            )


def _print_account_hierarchy(
    customer_client, customer_ids_to_child_accounts, depth
):
    """Prints the specified account's hierarchy using recursion.

    Args:
      customer_client: The customer cliant whose info will be printed; its
      child accounts will be processed if it's a manager.
      customer_ids_to_child_accounts: A dictionary mapping customer IDs to
      child accounts.
      depth: The current integer depth we are printing from in the account
      hierarchy.
    """
    if depth == 0:
        print("Customer ID (Descriptive Name, Currency Code, Time Zone)")

    customer_id = customer_client.id
    print("-" * (depth * 2), end="")
    print(
        f"{customer_id} ({customer_client.descriptive_name}, "
        f"{customer_client.currency_code}, "
        f"{customer_client.time_zone})"
    )

    # Recursively call this function for all child accounts of customer_client.
    if customer_id in customer_ids_to_child_accounts:
        for child_account in customer_ids_to_child_accounts[customer_id]:
            _print_account_hierarchy(
                child_account, customer_ids_to_child_accounts, depth + 1
            )


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v8")

    parser = argparse.ArgumentParser(
        description="This example gets the account hierarchy of the specified "
        "manager account and login customer ID."
    )
    # The following argument(s) should be provided to run the example.
    parser.add_argument(
        "-l",
        "--login_customer_id",
        "--manager_customer_id",
        type=str,
        required=False,
        help="Optional manager "
        "account ID. If none provided, the example will "
        "instead list the accounts accessible from the "
        "authenticated Google Ads account.",
    )
    args = parser.parse_args()
    try:
        main(googleads_client, args.login_customer_id)
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
