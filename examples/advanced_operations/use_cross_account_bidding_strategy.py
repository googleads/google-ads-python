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
"""Adds a cross-account bidding strategy to a manager account.

Also attaches the bidding strategy to a client customer's campaign and lists
all manager-owned and customer accessible bidding strategies.
"""


import argparse
import sys
from uuid import uuid4

from google.api_core import protobuf_helpers

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


def main(client, customer_id, manager_customer_id, campaign_id):
    """The main method that creates all necessary entities for the example.

    Args:
        client: An initialized GoogleAdsClient instance.
        customer_id: A client customer ID.
        manager_customer_id: A manager customer ID.
        campaign_id: The ID of an existing campaign in the client customer's
            account.
    """
    bidding_strategy_resource_name = _create_bidding_strategy(
        client, manager_customer_id
    )
    _list_manager_owned_bidding_strategies(client, manager_customer_id)
    _list_customer_accessible_bidding_strategies(client, customer_id)
    _attach_cross_account_bidding_strategy_to_campaign(
        client, customer_id, campaign_id, bidding_strategy_resource_name
    )


# [START create_cross_account_strategy]
def _create_bidding_strategy(client, manager_customer_id):
    """Creates a new cross-account bidding strategy in the manager account.

    The cross-account bidding strategy is of type TargetSpend (Maximize Clicks).

    Args:
        client: An initialized GoogleAdsClient instance.
        manager_customer_id: A manager customer ID.

    Returns:
        The ID of the newly created bidding strategy.
    """
    bidding_strategy_service = client.get_service("BiddingStrategyService")
    # Creates a portfolio bidding strategy.
    # [START set_currency_code]
    # Constructs an operation that will create a portfolio bidding strategy.
    bidding_strategy_operation = client.get_type("BiddingStrategyOperation")
    bidding_strategy = bidding_strategy_operation.create
    bidding_strategy.name = f"Maximize Clicks #{uuid4()}"
    # Sets target_spend to an empty TargetSpend object without setting any
    # of its nested fields.
    bidding_strategy.target_spend = client.get_type("TargetSpend")
    # Sets the currency of the new bidding strategy. If not provided, the
    # bidding strategy uses the manager account's default currency.
    bidding_strategy.currency_code = "USD"
    # [END set_currency_code]

    # Sends the operation in a mutate request.
    response = bidding_strategy_service.mutate_bidding_strategies(
        customer_id=manager_customer_id, operations=[bidding_strategy_operation]
    )

    # Prints the resource name of the created cross-account bidding strategy.
    resource_name = response.results[0].resource_name
    print(f"Created cross-account bidding strategy: '{resource_name}'")

    return resource_name
    # [END create_cross_account_strategy]


# [START list_manager_strategies]
def _list_manager_owned_bidding_strategies(client, manager_customer_id):
    """List all cross-account bidding strategies in the manager account.

    Args:
        client: An initialized GoogleAdsClient instance.
        manager_customer_id: A manager customer ID.
    """
    googleads_service = client.get_service("GoogleAdsService")
    query = """
        SELECT
          bidding_strategy.id,
          bidding_strategy.name,
          bidding_strategy.type,
          bidding_strategy.currency_code
        FROM bidding_strategy"""

    # Creates and issues a search Google Ads stream request that will retrieve
    # all bidding strategies.
    stream = googleads_service.search_stream(
        customer_id=manager_customer_id, query=query
    )

    # Iterates through and prints all of the results in the stream response.
    print(
        "Cross-account bid strategies in manager account: "
        f"{manager_customer_id}"
    )
    for response in stream:
        for row in response.results:
            bs = row.bidding_strategy
            print(
                f"\tID: {bs.id}\n"
                f"\tName: {bs.name}\n"
                f"\tStrategy type: {bs.type_}\n"
                f"\tCurrency: {bs.currency_code}\n\n"
            )
            # [END list_manager_strategies]


# [START list_accessible_strategies]
def _list_customer_accessible_bidding_strategies(client, customer_id):
    """Lists all bidding strategies available to the client account.

    This includes both portfolio bidding strategies owned by account and
    cross-account bidding strategies shared by any of its managers.

    Args:
        client: An initialized GoogleAdsClient instance.
        customer_id: A client customer ID.
    """
    googleads_service = client.get_service("GoogleAdsService")
    query = """
        SELECT
          accessible_bidding_strategy.id,
          accessible_bidding_strategy.name,
          accessible_bidding_strategy.type,
          accessible_bidding_strategy.owner_customer_id,
          accessible_bidding_strategy.owner_descriptive_name
        FROM accessible_bidding_strategy"""
    # Uncomment the following WHERE clause to filter results to *only*
    # cross-account bidding strategies shared with the current customer by a
    # manager (and not also include the current customer's portfolio
    # bidding strategies).
    #
    # query += f"WHERE accessible_bidding_strategy.owner_customer_id != {customer_id}"

    # Creates and issues a search Google Ads stream request that will retrieve
    # all bidding strategies.
    stream = googleads_service.search_stream(
        customer_id=customer_id, query=query
    )

    # Iterates through and prints all of the results in the stream response.
    print(f"All bid strategies accessible by account '{customer_id}'\n")
    for response in stream:
        for row in response.results:
            bs = row.accessible_bidding_strategy
            print(
                f"\tID: {bs.id}\n"
                f"\tName: {bs.name}\n"
                f"\tStrategy type: {bs.type_}\n"
                f"\tOwner customer ID: {bs.owner_customer_id}\n"
                f"\tOwner description: {bs.owner_descriptive_name}\n\n"
            )
            # [END list_accessible_strategies]


# [START attach_strategy]
def _attach_cross_account_bidding_strategy_to_campaign(
    client, customer_id, campaign_id, bidding_strategy_resource_name
):
    """Attaches the cross-account bidding strategy to the given campaign.

    Args:
        client: An initialized GoogleAdsClient instance.
        customer_id: A client customer ID.
        campaign_id: The ID of an existing campaign in the client customer's
            account.
        bidding_strategy_resource_name: The ID of a bidding strategy
    """
    campaign_service = client.get_service("CampaignService")
    bidding_strategy_service = client.get_service("BiddingStrategyService")
    campaign_operation = client.get_type("CampaignOperation")
    campaign = campaign_operation.update
    campaign.resource_name = campaign_service.campaign_path(
        customer_id, campaign_id
    )
    campaign.bidding_strategy = bidding_strategy_resource_name
    campaign_operation.update_mask = protobuf_helpers.field_mask(
        None, campaign._pb
    )

    # Sends the operation in a mutate request.
    response = campaign_service.mutate_campaigns(
        customer_id=customer_id, operations=[campaign_operation]
    )

    # Prints the resource name of the updated campaign.
    print(
        "Updated campaign with resource name: "
        f"'{response.results[0].resource_name}'"
    )
    # [END attach_strategy]


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v8")

    parser = argparse.ArgumentParser(description=("Creates a Smart campaign."))
    # The following argument(s) should be provided to run the example.
    parser.add_argument(
        "-c",
        "--customer_id",
        type=str,
        required=True,
        help="The Google Ads customer ID.",
    )
    parser.add_argument(
        "-m",
        "--manager_customer_id",
        type=str,
        required=True,
        help="The Google Ads customer ID for a manager account.",
    )
    parser.add_argument(
        "-i",
        "--campaign_id",
        type=str,
        required=True,
        help="The ID of an existing campaign in the client customer's account",
    )

    args = parser.parse_args()

    try:
        main(
            googleads_client,
            args.customer_id,
            args.manager_customer_id,
            args.campaign_id,
        )
    except GoogleAdsException as ex:
        print(
            f'Request with ID "{ex.request_id}" failed with status '
            f'"{ex.error.code().name}" and includes the following errors:'
        )
        for error in ex.failure.errors:
            print(f'Error with message "{error.message}".')
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print(f"\t\tOn field: {field_path_element.field_name}")
        sys.exit(1)
