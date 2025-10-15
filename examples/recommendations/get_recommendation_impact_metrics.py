#!/usr/bin/env python
# Copyright 2025 Google LLC
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
"""This example is to get impact metrics for a custom budget.

Use this example to get impact metrics for a given budget amount.

This example uses the following:
1) Performance Max for the campaign type
2) United States for the geo targeting
3) Maximize Conversions Value for the bidding strategy

To get budget recommendations, run generate_budget_recommendations.py.
"""


import argparse
import sys
from typing import List, Dict, Any

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.ads.googleads.v22.services.services.recommendation_service import (
    RecommendationServiceClient,
)
from google.ads.googleads.v22.services.types.recommendation_service import (
    GenerateRecommendationsRequest,
    GenerateRecommendationsResponse,
)
from google.ads.googleads.v22.resources.types.recommendation import (
    Recommendation,
)


def main(
    client: GoogleAdsClient, customer_id: str, user_provided_budget_amount: int
) -> None:
    """The main method that creates all necessary entities for the example.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        user_provided_budget_amount: a user-provided budget amount (not in micros), to retrieve impact metrics for.
    """
    recommendation_service: RecommendationServiceClient = client.get_service(
        "RecommendationService"
    )
    request: GenerateRecommendationsRequest = client.get_type(
        "GenerateRecommendationsRequest"
    )

    request.customer_id = customer_id
    request.recommendation_types = ["CAMPAIGN_BUDGET"]
    request.advertising_channel_type = (
        client.enums.AdvertisingChannelTypeEnum.PERFORMANCE_MAX
    )
    request.bidding_info.bidding_strategy_type = "MAXIMIZE_CONVERSION_VALUE"
    request.positive_locations_ids = [2840]  # 2840 is for United States
    request.asset_group_info = [{"final_url": "https://www.your-company.com/"}]
    # Multiply the user-provided budget by 1,000,000 to convert to micros, as required for current_budget
    request.budget_info.current_budget = round(
        (user_provided_budget_amount * 1000000), 2
    )

    results: GenerateRecommendationsResponse = (
        recommendation_service.generate_recommendations(request)
    )

    recommendations: List[Recommendation] = results.recommendations

    # List to store impact metrics for user input budget
    budget_impact_metrics: List[Dict[str, Any]] = []

    # Get impact metrics for custom budget.
    for rec in recommendations:
        campaign_budget_rec = rec.campaign_budget_recommendation
        # Loop through the budget options in the campaign budget recommendation
        # to compile a list of budget amounts and their respective potential
        # impact metrics. If you have a campaign creation interface,
        # you could display this information for end users to decide which
        # budget amount best aligns with their goals.
        for budget_option in campaign_budget_rec.budget_options:
            if hasattr(budget_option, "impact"):
                impact = budget_option.impact
                budget_amount_micros = budget_option.budget_amount_micros
                if (
                    budget_amount_micros / 1000000
                    == user_provided_budget_amount
                ):
                    budget_data: Dict[str, Any] = {
                        "budget_amount": round(
                            (budget_amount_micros / 1000000), 2
                        ),
                        "potential_metrics": impact.potential_metrics,
                    }
                    budget_impact_metrics.append(budget_data)
            else:
                print("impact metrics not found for this budget amount.")

    print(f"budget_impact_metrics:\n{budget_impact_metrics}")
    """
    budget_impact_metrics:
    [{'budget_amount': 100.0, 'potential_metrics': cost_micros: 700000000
    conversions: 12
    conversions_value: 481.12592352792007
    }]
    """


if __name__ == "__main__":
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description=("Get impact metrics for Performance Max budget.")
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
        "-b",
        "--user_provided_budget_amount",
        type=int,
        required=True,
        help=("A budget amount (not in micros) advertiser wants to use."),
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
            args.user_provided_budget_amount,
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
