#!/usr/bin/env python
# Copyright 2018 Google LLC
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
"""This example constructs a campaign with a Portfolio Bidding Strategy."""


import argparse
import sys
import uuid

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


def main(client, customer_id):
    campaign_budget_service = client.get_service("CampaignBudgetService")
    bidding_strategy_service = client.get_service("BiddingStrategyService")
    campaign_service = client.get_service("CampaignService")

    # [START use_portfolio_bidding_strategy]
    # Create a budget, which can be shared by multiple campaigns.
    campaign_budget_operation = client.get_type("CampaignBudgetOperation")
    campaign_budget = campaign_budget_operation.create
    campaign_budget.name = f"Interplanetary Budget {uuid.uuid4()}"
    campaign_budget.delivery_method = client.get_type(
        "BudgetDeliveryMethodEnum"
    ).BudgetDeliveryMethod.STANDARD
    campaign_budget.amount_micros = 500000
    campaign_budget.explicitly_shared = True

    # Add budget.
    try:
        campaign_budget_response = campaign_budget_service.mutate_campaign_budgets(
            customer_id=customer_id, operations=[campaign_budget_operation]
        )
        campaign_budget_id = campaign_budget_response.results[0].resource_name
        print(f'Budget "{campaign_budget_id}" was created.')
    except GoogleAdsException as ex:
        _handle_googleads_exception(ex)
        # [END use_portfolio_bidding_strategy]

    # [START use_portfolio_bidding_strategy_1]
    # Create a portfolio bidding strategy.
    bidding_strategy_operation = client.get_type("BiddingStrategyOperation")
    bidding_strategy = bidding_strategy_operation.create
    bidding_strategy.name = f"Enhanced CPC {uuid.uuid4()}"
    target_spend = bidding_strategy.target_spend
    target_spend.cpc_bid_ceiling_micros = 2000000

    # Add portfolio bidding strategy.
    try:
        bidding_strategy_response = bidding_strategy_service.mutate_bidding_strategies(
            customer_id=customer_id, operations=[bidding_strategy_operation]
        )
        bidding_strategy_id = bidding_strategy_response.results[0].resource_name
        print(f'Created portfolio bidding strategy "{bidding_strategy_id}".')
    except GoogleAdsException as ex:
        _handle_googleads_exception(ex)
        # [END use_portfolio_bidding_strategy_1]

    # [START use_portfolio_bidding_strategy_2]
    # Create campaign.
    campaign_operation = client.get_type("CampaignOperation")
    campaign = campaign_operation.create
    campaign.name = f"Interplanetary Cruise {uuid.uuid4()}"
    campaign.advertising_channel_type = client.get_type(
        "AdvertisingChannelTypeEnum"
    ).AdvertisingChannelType.SEARCH

    # Recommendation: Set the campaign to PAUSED when creating it to prevent the
    # ads from immediately serving. Set to ENABLED once you've added targeting
    # and the ads are ready to serve.
    campaign.status = client.get_type(
        "CampaignStatusEnum"
    ).CampaignStatus.PAUSED

    # Set the bidding strategy and budget.
    campaign.bidding_strategy = bidding_strategy_id
    campaign.manual_cpc.enhanced_cpc_enabled = True
    campaign.campaign_budget = campaign_budget_id

    # Set the campaign network options.
    campaign.network_settings.target_google_search = True
    campaign.network_settings.target_search_network = True
    campaign.network_settings.target_content_network = False
    campaign.network_settings.target_partner_search_network = False
    # [END use_portfolio_bidding_strategy_2]

    # Add the campaign.
    try:
        campaign_response = campaign_service.mutate_campaigns(
            customer_id=customer_id, operations=[campaign_operation]
        )
        print(f"Created campaign {campaign_response.results[0].resource_name}.")
    except GoogleAdsException as ex:
        _handle_googleads_exception(ex)


def _handle_googleads_exception(exception):
    print(
        f'Request with ID "{exception.request_id}" failed with status '
        f'"{exception.error.code().name}" and includes the following errors:'
    )
    for error in exception.failure.errors:
        print(f'\tError with message "{error.message}".')
        if error.location:
            for field_path_element in error.location.field_path_elements:
                print(f"\t\tOn field: {field_path_element.field_name}")
    sys.exit(1)


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v8")

    parser = argparse.ArgumentParser(
        description="Adds a campaign for specified customer."
    )
    # The following argument(s) should be provided to run the example.
    parser.add_argument(
        "-c",
        "--customer_id",
        type=str,
        required=True,
        help="The Google Ads customer ID.",
    )
    args = parser.parse_args()

    main(googleads_client, args.customer_id)
