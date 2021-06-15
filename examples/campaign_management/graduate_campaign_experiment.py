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
"""Illustrates how to graduate a campaign experiment."""


import argparse
import sys
import uuid
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


def main(client, customer_id, campaign_experiment_id):
    """Illustrates how to graduate a campaign experiment.

    Args:
      client: The Google Ads client.
      customer_id: The customer ID for which to graduate the experiment.
      campaign_experiment_id: The campaign experiment ID to graduate.
    """
    campaign_experiment_service = client.get_service(
        "CampaignExperimentService"
    )

    # Graduating a campaign experiment requires a new budget. Since the
    # budget for the base campaign has explicitly_shared set to false, the
    # budget cannot be shared with the campaign after it is made
    # independent by graduation.
    budget_resource_name = _create_budget(client, customer_id)

    # Prints out some information about the created campaign budget.
    print(
        f"Created new budget with resource name '{budget_resource_name} '"
        "for adding to the experiment campaign during graduation."
    )

    # Graduates the experiment campaign using the newly created budget.
    response = campaign_experiment_service.graduate_campaign_experiment(
        campaign_experiment=campaign_experiment_service.campaign_experiment_path(
            customer_id, campaign_experiment_id
        ),
        campaign_budget=budget_resource_name,
    )
    print(
        f"Campaign with resource name {response.graduated_campaign} is "
        "now graduated."
    )


def _create_budget(client, customer_id):
    """Creates the budget for the campaign.

    Args:
      client: The Google Ads client.
      customer_id: The customer ID to which the new budget will be added.

    Returns:
        The resource name of the newly created campaign budget.
    """
    # Gets the CampaignBudgetService.
    campaign_budget_service = client.get_service("CampaignBudgetService")

    # Creates the campaign budget.
    campaign_budget_operation = client.get_type("CampaignBudgetOperation")
    campaign_budget = campaign_budget_operation.create
    campaign_budget.name = f"Interplanetary Cruise Budget {uuid.uuid4()}"
    campaign_budget.delivery_method = client.get_type(
        "BudgetDeliveryMethodEnum"
    ).BudgetDeliveryMethod.STANDARD
    campaign_budget.amount_micros = 5000000

    campaign_budget_response = campaign_budget_service.mutate_campaign_budgets(
        customer_id=customer_id, operations=[campaign_budget_operation]
    )

    return campaign_budget_response.results[0].resource_name


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v8")

    parser = argparse.ArgumentParser(
        description="Gets all available ad group criterion CPC bid "
        "simulations for a given ad group."
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
        "-i",
        "--campaign_experiment_id",
        type=str,
        required=True,
        help="ID of the campaign experiment to graduate.",
    )
    args = parser.parse_args()

    try:
        main(googleads_client, args.customer_id, args.campaign_experiment_id)
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
