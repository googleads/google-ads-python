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
"""This example illustrates how to add a campaign using asyncio."""


import argparse
import asyncio
import datetime
import sys
from typing import List
import uuid

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.ads.googleads.v23.resources.types.campaign import Campaign
from google.ads.googleads.v23.resources.types.campaign_budget import (
    CampaignBudget,
)
from google.ads.googleads.v23.services.types.campaign_budget_service import (
    CampaignBudgetOperation,
)
from google.ads.googleads.v23.services.types.campaign_service import (
    CampaignOperation,
)
from google.ads.googleads.v23.services.types.google_ads_service import (
    MutateGoogleAdsResponse,
    MutateOperation,
)


_START_DATE_FORMAT: str = "%Y%m%d 00:00:00"
_END_DATE_FORMAT: str = "%Y%m%d 23:59:59"


async def main(client: GoogleAdsClient, customer_id: str) -> None:
    # Gets the GoogleAdsService client.
    googleads_service = client.get_service("GoogleAdsService", is_async=True)

    # We are creating both the budget and the campaign in the same request, so
    # we need to use a temporary resource name for the budget to reference it
    # in the campaign.
    # Temporary resource names must be negative integers formatted as strings.
    # https://developers.google.com/google-ads/api/docs/batch-processing/temporary-ids
    budget_resource_name: str = f"customers/{customer_id}/campaignBudgets/-1"

    mutate_operations: List[MutateOperation] = []

    # Create a budget, which can be shared by multiple campaigns.
    campaign_budget_operation: CampaignBudgetOperation = client.get_type(
        "CampaignBudgetOperation"
    )
    campaign_budget: CampaignBudget = campaign_budget_operation.create
    campaign_budget.resource_name = budget_resource_name
    campaign_budget.name = f"Interplanetary Budget {uuid.uuid4()}"
    campaign_budget.delivery_method = (
        client.enums.BudgetDeliveryMethodEnum.STANDARD
    )
    campaign_budget.amount_micros = 500000

    mutate_operation_budget: MutateOperation = client.get_type("MutateOperation")
    mutate_operation_budget.campaign_budget_operation = campaign_budget_operation
    mutate_operations.append(mutate_operation_budget)

    # Create campaign.
    campaign_operation: CampaignOperation = client.get_type("CampaignOperation")
    campaign: Campaign = campaign_operation.create
    campaign.name = f"Interplanetary Cruise {uuid.uuid4()}"
    campaign.advertising_channel_type = (
        client.enums.AdvertisingChannelTypeEnum.SEARCH
    )

    # Recommendation: Set the campaign to PAUSED when creating it to prevent
    # the ads from immediately serving. Set to ENABLED once you've added
    # targeting and the ads are ready to serve.
    campaign.status = client.enums.CampaignStatusEnum.PAUSED

    # Set the bidding strategy and budget.
    campaign.manual_cpc = client.get_type("ManualCpc")
    # Reference the budget created in the same request.
    campaign.campaign_budget = budget_resource_name

    # Set the campaign network options.
    campaign.network_settings.target_google_search = True
    campaign.network_settings.target_search_network = True
    campaign.network_settings.target_partner_search_network = False
    # Enable Display Expansion on Search campaigns. For more details see:
    # https://support.google.com/google-ads/answer/7193800
    campaign.network_settings.target_content_network = True

    # Declare whether or not this campaign serves political ads targeting the
    # EU. Valid values are:
    #   CONTAINS_EU_POLITICAL_ADVERTISING
    #   DOES_NOT_CONTAIN_EU_POLITICAL_ADVERTISING
    campaign.contains_eu_political_advertising = (
        client.enums.EuPoliticalAdvertisingStatusEnum.DOES_NOT_CONTAIN_EU_POLITICAL_ADVERTISING
    )

    # Optional: Set the start date.
    start_time: datetime.date = datetime.date.today() + datetime.timedelta(
        days=1
    )
    campaign.start_date_time = datetime.date.strftime(start_time, _START_DATE_FORMAT)

    # Optional: Set the end date.
    end_time: datetime.date = start_time + datetime.timedelta(weeks=4)
    campaign.end_date_time = datetime.date.strftime(end_time, _END_DATE_FORMAT)
    # [END add_campaigns_1]

    mutate_operation_campaign: MutateOperation = client.get_type(
        "MutateOperation"
    )
    mutate_operation_campaign.campaign_operation = campaign_operation
    mutate_operations.append(mutate_operation_campaign)

    # Issue a mutate request to add the budget and campaign.
    response: MutateGoogleAdsResponse = await googleads_service.mutate(
        customer_id=customer_id, mutate_operations=mutate_operations
    )

    # Check the result for the campaign (index 1 in the operations list).
    # The response returns results in the same order as operations.
    campaign_result = response.mutate_operation_responses[1].campaign_result
    print(f"Created campaign {campaign_result.resource_name}.")


if __name__ == "__main__":
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
    args: argparse.Namespace = parser.parse_args()

    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client: GoogleAdsClient = GoogleAdsClient.load_from_storage(
        version="v23"
    )

    try:
        asyncio.run(main(googleads_client, args.customer_id))
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
