#!/usr/bin/env python
# Copyright 2022 Google LLC
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
"""This example generates historical metrics for a keyword plan.

To create a keyword plan, run the add_keyword_plan.py example.
"""


import argparse
import sys

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


# [START generate_historical_metrics]
def main(client, customer_id, keyword_plan_id):
    """The main method that creates all necessary entities for the example.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        keyword_plan_id: the ID for a keyword plan.
    """
    keyword_plan_service = client.get_service("KeywordPlanService")
    resource_name = keyword_plan_service.keyword_plan_path(
        customer_id, keyword_plan_id
    )

    response = keyword_plan_service.generate_historical_metrics(
        keyword_plan=resource_name
    )

    for metric in response.metrics:
        # These metrics include those for both the search query and any close
        # variants included in the response.
        print(
            f"The search query, '{metric.search_query}', (and the following "
            f"variants: {', '.join(metric.close_variants)}), generated the "
            "following historical metrics:"
        )

        # Approximate number of monthly searches on this query averaged for
        # the past 12 months.
        print(
            f"\tApproximate monthly searches: {metric.keyword_metrics.avg_monthly_searches}."
        )

        # The competition level for this search query.
        print(
            f"\tCompetition level: {metric.keyword_metrics.competition.name}."
        )

        # The competition index for the query in the range [0, 100]. This shows
        # how competitive ad placement is for a keyword. The level of
        # competition from 0-100 is determined by the number of ad slots filled
        # divided by the total number of ad slots available. If not enough data
        # is available, None will be returned.
        print(
            f"\tCompetition index: {metric.keyword_metrics.competition_index}."
        )

        # Top of page bid low range (20th percentile) in micros for the keyword.
        print(
            f"\tTop of page bid low range: {metric.keyword_metrics.low_top_of_page_bid_micros}."
        )

        # Top of page bid high range (80th percentile) in micros for the keyword.
        print(
            f"\tTop of page bid high range: {metric.keyword_metrics.high_top_of_page_bid_micros}."
        )

        # Approximate number of searches on this query for the past twelve months.
        for month in metric.keyword_metrics.monthly_search_volumes:
            print(
                f"\tApproximately {month.monthly_searches} searches in {month.month.name}, {month.year}."
            )
        # [END generate_historical_metrics]


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v10")

    parser = argparse.ArgumentParser(
        description="Generates historical metrics for a keyword plan."
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
            print(f'\tError with message "{error.message}".')
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print(f"\t\tOn field: {field_path_element.field_name}")
        sys.exit(1)
