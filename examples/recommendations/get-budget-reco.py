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
"""This example is to get budget recommendations for Performance Max; 

The response includes weekly impact metrics for the recommended budgets.

Example uses: 
1) Performance Max for the campaign type
2) United States for the geo targeting 
3) Maximize Conversions Value for the bidding strategy.

To get impact metrics for a custom budget, run get_impact_metrics.py.
"""


import argparse
import sys

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


def main(client, customer_id):
    """The main method that creates all necessary entities for the example.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
    """
    # Start Recommendation Service.
    reco_service = client.get_service("RecommendationService")

    # Build Request.
    reco_request = client.get_type("GenerateRecommendationsRequest")

    reco_request.customer_id = customer_id
    reco_request.recommendation_types = ["CAMPAIGN_BUDGET"]
    reco_request.advertising_channel_type = "PERFORMANCE_MAX"
    reco_request.bidding_info.bidding_strategy_type = "MAXIMIZE_CONVERSION_VALUE"
    reco_request.positive_locations_ids = [2840]  # 2840 is for United States
    reco_request.asset_group_info = [{ "final_url": "https://www.your-company.com/" }]

    # Send Request.
    results = reco_service.generate_recommendations(reco_request)

    recommendations = results.recommendations

    budget_recommendations_list = []    # List to store budget recos with impact metrics
    budget_amounts =  [] # List to store budget reco amounts

    for reco in recommendations:
        if hasattr(reco, 'campaign_budget_recommendation'):
            campaign_budget_reco = reco.campaign_budget_recommendation

            if hasattr(campaign_budget_reco, 'budget_options'):
                for budget_option in campaign_budget_reco.budget_options:
                    if hasattr(budget_option, 'impact') and hasattr(budget_option, 'budget_amount_micros'): # Check if both exist
                        impact = budget_option.impact
                        budget_amount = budget_option.budget_amount_micros

                        if hasattr(impact, 'potential_metrics'):
                            if budget_amount > 0:
                                budget_data = {
                                    "budget_amount": round((budget_amount/1000000), 2),
                                    "potential_metrics": impact.potential_metrics
                                }
                                budget_recommendations_list.append(budget_data)
                                budget_amounts.append(round((budget_amount/1000000), 2))  
                        else:
                            print("potential_metrics not found for this budget option.")
                    else:
                        print("impact or budget_amount_micros not found for this budget option.")
            else:
                print("budget_options not found for this recommendation.")
        else:
            print("campaign_budget_recommendation not found for this recommendation.")
    print("budget_recommendations_list:")
    print(budget_recommendations_list)
    """
    budget_recommendations_list:
    [{'budget_amount': 44.56, 'potential_metrics': cost_micros: 311920000
    conversions: 2.1
    conversions_value: 82.537178980480363
    }, {'budget_amount': 55.7, 'potential_metrics': cost_micros: 389900000
    conversions: 2.1
    conversions_value: 82.537178980480363
    }, {'budget_amount': 66.84, 'potential_metrics': cost_micros: 467880000
    conversions: 2.1
    conversions_value: 82.537178980480363
    }]
    """
    print("budget_amounts:")
    print(budget_amounts)
    """
    budget_amounts:
    [44.56, 55.7, 66.84]
    """


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=("Get impact metrics for Performance Max budget."))
    # The following argument(s) should be provided to run the example.
    parser.add_argument(
        "-c",
        "--customer_id",
        type=str,
        required=True,
        help="The Google Ads customer ID.",
    )

    args = parser.parse_args()

    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v18")

    try:
        main(googleads_client, args.customer_id)
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