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
"""This example generates forecast metrics for a keyword plan.

To create a keyword plan, run the add_keyword_plan.py example.
"""


import argparse
import sys

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


# [START generate_forecast_metrics]
def main(client, customer_id, keyword_plan_id):
    keyword_plan_service = client.get_service("KeywordPlanService")
    resource_name = keyword_plan_service.keyword_plan_path(
        customer_id, keyword_plan_id
    )

    response = keyword_plan_service.generate_forecast_metrics(
        keyword_plan=resource_name
    )

    for i, forecast in enumerate(response.keyword_forecasts):
        print(f"#{i+1} Keyword ID: {forecast.keyword_plan_ad_group_keyword}")

        metrics = forecast.keyword_forecast

        click_val = metrics.clicks
        clicks = f"{click_val:.2f}" if click_val else "unspecified"
        print(f"Estimated daily clicks: {clicks}")

        imp_val = metrics.impressions
        impressions = f"{imp_val:.2f}" if imp_val else "unspecified"
        print(f"Estimated daily impressions: {impressions}")

        cpc_val = metrics.average_cpc
        cpc = f"{cpc_val:.2f}" if cpc_val else "unspecified"
        print(f"Estimated average cpc: {cpc}\n")
        # [END generate_forecast_metrics]


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v6")

    parser = argparse.ArgumentParser(
        description="Generates forecast metrics for a keyword plan."
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
        "-k",
        "--keyword_plan_id",
        type=str,
        required=True,
        help="A Keyword Plan ID.",
    )
    args = parser.parse_args()

    try:
        main(googleads_client, args.customer_id, args.keyword_plan_id)
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
