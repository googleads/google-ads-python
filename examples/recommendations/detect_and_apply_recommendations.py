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
"""This example shows how to retrieve recommendations and apply them.

The auto-apply feature, which automatically applies recommendations as they
become eligible, is supported by the Google Ads UI but not by the Google Ads
API. See https://support.google.com/google-ads/answer/10279006 for more
information on using auto-apply in the Google Ads UI.

This example demonstrates how an alternative can be implemented with the
features that are currently supported by the Google Ads API. It periodically
retrieves and applies `KEYWORD` recommendations with default parameters.
"""


import argparse
import sys
from time import sleep

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

MAX_RESULT_SIZE = 2
NUMBER_OF_RUNS = 2
SECONDS_TO_SLEEP = 5
PAGE_SIZE = 1000


def main(client, customer_id):
    """The main method that creates all necessary entities for the example.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
    """
    detect_and_apply_recommendations(client, customer_id)


def detect_and_apply_recommendations(client, customer_id):
    """Detects recommendations and applies them.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
    """
    googleads_service = client.get_service("GoogleAdsService")
    query = f"""
        SELECT
          recommendation.campaign,
          recommendation.keyword_recommendation
        FROM recommendation
        WHERE
          recommendation.type = KEYWORD
        LIMIT {MAX_RESULT_SIZE}"""

    for i in range(NUMBER_OF_RUNS):
        request = client.get_type("SearchGoogleAdsRequest")
        request.customer_id = customer_id
        request.query = query
        request.page_size = PAGE_SIZE

        response = googleads_service.search(request=request)

        for row in response.results:
            recommendation = row.recommendation
            print(
                f"Keyword recommendation ('{recommendation.resource_name}') "
                f"was found for campaign '{recommendation.campaign}"
            )

            if "keyword_recommendation" in recommendation:
                keyword = recommendation.keyword_recommendation.keyword
                print(
                    f"\tKeyword = '{keyword.text}'\n"
                    f"\tType = '{keyword.match_type}'"
                )

            apply_recommendation(
                client, customer_id, recommendation.resource_name
            )

        print(
            f"Waiting {SECONDS_TO_SLEEP} seconds before applying more "
            "recommendations."
        )
        sleep(SECONDS_TO_SLEEP)


# [START apply_recommendation]
def apply_recommendation(client, customer_id, recommendation):
    """Applies a recommendation.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        recommendation: a resource name for the recommendation to be applied.
    """
    # If you have a recommendation_id instead of the resournce_name
    # you can create a resource name from it like this:
    #
    # googleads_service = client.get_service("GoogleAdsService")
    # resource_name = googleads_service.recommendation_path(
    #   customer_id, recommendation.id
    # )

    operation = client.get_type("ApplyRecommendationOperation")
    operation.resource_name = recommendation

    # Each recommendation type has optional parameters to override the
    # recommended values. This is an example to override a recommended ad when a
    # TextAdRecommendation is applied.
    # For details, please read:
    # https://developers.google.com/google-ads/api/reference/rpc/google.ads.google_ads.v1.services#google.ads.google_ads.v1.services.ApplyRecommendationOperation
    #
    # operation.text_ad.ad = "INSERT_AD_ID_AS_INTEGER_HERE"

    # Issues a mutate request to apply the recommendation.
    recommendation_service = client.get_service("RecommendationService")
    response = recommendation_service.apply_recommendation(
        customer_id=customer_id, operations=[operation]
    )

    applied_recommendation = response.results[0].resource_name

    print(
        "Applied recommendation with resource name: '{applied_recommendation}'."
    )
    # [END apply_recommendation]


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v16")

    parser = argparse.ArgumentParser(
        description="Lists TEXT_AD recommendations for specified customer."
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

    try:
        main(googleads_client, args.customer_id)
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
