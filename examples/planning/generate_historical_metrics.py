#!/usr/bin/env python
# Copyright 2023 Google LLC
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
"""This example generates historical metrics for keyword planning.

For more details see this guide:
https://developers.google.com/google-ads/api/docs/keyword-planning/generate-historical-metrics
"""

from typing import Iterable
import argparse
import sys

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.ads.googleads.v22.common.types.keyword_plan_common import (
    KeywordPlanHistoricalMetrics,
    MonthlySearchVolume,
)
from google.ads.googleads.v22.services.services.google_ads_service.client import (
    GoogleAdsServiceClient,
)
from google.ads.googleads.v22.services.services.keyword_plan_idea_service.client import (
    KeywordPlanIdeaServiceClient,
)
from google.ads.googleads.v22.services.types.keyword_plan_idea_service import (
    GenerateKeywordHistoricalMetricsRequest,
    GenerateKeywordHistoricalMetricsResponse,
    GenerateKeywordHistoricalMetricsResult,
)


# [START generate_historical_metrics]
def main(client: GoogleAdsClient, customer_id: str):
    """The main method that creates all necessary entities for the example.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
    """
    generate_historical_metrics(client, customer_id)


def generate_historical_metrics(client: GoogleAdsClient, customer_id: str):
    """Generates historical metrics and prints the results.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
    """
    googleads_service: GoogleAdsServiceClient = client.get_service(
        "GoogleAdsService"
    )
    keyword_plan_idea_service: KeywordPlanIdeaServiceClient = (
        client.get_service("KeywordPlanIdeaService")
    )
    request: GenerateKeywordHistoricalMetricsRequest = client.get_type(
        "GenerateKeywordHistoricalMetricsRequest"
    )
    request.customer_id = customer_id
    request.keywords = ["mars cruise", "cheap cruise", "jupiter cruise"]
    # Geo target constant 2840 is for USA.
    request.geo_target_constants.append(
        googleads_service.geo_target_constant_path("2840")
    )
    request.keyword_plan_network = (
        client.enums.KeywordPlanNetworkEnum.GOOGLE_SEARCH
    )
    # Language criteria 1000 is for English. For the list of language criteria
    # IDs, see:
    # https://developers.google.com/google-ads/api/reference/data/codes-formats#languages
    request.language = googleads_service.language_constant_path("1000")

    response: GenerateKeywordHistoricalMetricsResponse = (
        keyword_plan_idea_service.generate_keyword_historical_metrics(
            request=request
        )
    )

    results: Iterable[GenerateKeywordHistoricalMetricsResult] = response.results
    for result in results:
        metrics: KeywordPlanHistoricalMetrics = result.keyword_metrics
        # These metrics include those for both the search query and any variants
        # included in the response.
        print(
            f"The search query '{result.text}' (and the following variants: "
            f"'{result.close_variants if result.close_variants else 'None'}'), "
            "generated the following historical metrics:\n"
        )

        # Approximate number of monthly searches on this query averaged for the
        # past 12 months.
        print(f"\tApproximate monthly searches: {metrics.avg_monthly_searches}")

        # The competition level for this search query.
        print(f"\tCompetition level: {metrics.competition}")

        # The competition index for the query in the range [0, 100]. This shows
        # how competitive ad placement is for a keyword. The level of
        # competition from 0-100 is determined by the number of ad slots filled
        # divided by the total number of ad slots available. If not enough data
        # is available, undef will be returned.
        print(f"\tCompetition index: {metrics.competition_index}")

        # Top of page bid low range (20th percentile) in micros for the keyword.
        print(
            f"\tTop of page bid low range: {metrics.low_top_of_page_bid_micros}"
        )

        # Top of page bid high range (80th percentile) in micros for the
        # keyword.
        print(
            "\tTop of page bid high range: "
            f"{metrics.high_top_of_page_bid_micros}"
        )

        # Approximate number of searches on this query for the past twelve
        # months.
        months: Iterable[MonthlySearchVolume] = metrics.monthly_search_volumes
        for month in months:
            print(
                f"\tApproximately {month.monthly_searches} searches in "
                f"{month.month.name}, {month.year}"
            )
            # [END generate_historical_metrics]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generates forecast metrics for keyword planning."
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

    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v22")

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
