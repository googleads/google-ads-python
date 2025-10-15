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
"""This example shows how to retrieve recommendations and apply them in a batch.

Recommendations should be applied shortly after they're retrieved. Depending on
the recommendation type, a recommendation can become obsolete quickly, and
obsolete recommendations throw an error when applied. For more details, see:
https://developers.google.com/google-ads/api/docs/recommendations#take_action

As of Google Ads API v15 users can subscribe to certain recommendation types to
apply them automatically. For more details, see:
https://developers.google.com/google-ads/api/docs/recommendations#auto-apply

As of Google Ads API v16 users can proactively generate certain recommendation
types during the campaign construction process. For more details see:
https://developers.google.com/google-ads/api/docs/recommendations#recommendations-in-campaign-construction
"""


import argparse
import sys
from typing import List, Iterable

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.ads.googleads.v22.services.types.google_ads_service import (
    GoogleAdsRow,
)
from google.ads.googleads.v22.services.types.recommendation_service import (
    ApplyRecommendationOperation,
    ApplyRecommendationResult,
)


def main(client: GoogleAdsClient, customer_id: str) -> None:
    """The main method that creates all necessary entities for the example.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
    """
    detect_and_apply_recommendations(client, customer_id)


def detect_and_apply_recommendations(
    client: GoogleAdsClient, customer_id: str
) -> None:
    """Detects recommendations and applies them.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
    """

    # [START detect_keyword_recommendations]
    googleads_service = client.get_service("GoogleAdsService")
    query: str = """
        SELECT
          recommendation.campaign,
          recommendation.keyword_recommendation
        FROM recommendation
        WHERE
          recommendation.type = KEYWORD"""

    # Detects keyword recommendations that exist for the customer account.
    response: Iterable[GoogleAdsRow] = googleads_service.search(
        customer_id=customer_id, query=query
    )

    operations: List[ApplyRecommendationOperation] = []
    for row in response:
        recommendation = row.recommendation
        print(
            f"Keyword recommendation ('{recommendation.resource_name}') "
            f"was found for campaign '{recommendation.campaign}."
        )

        keyword = recommendation.keyword_recommendation.keyword
        print(
            f"\tKeyword = '{keyword.text}'\n" f"\tType = '{keyword.match_type}'"
        )

        # Create an ApplyRecommendationOperation that will be used to apply
        # this recommendation, and add it to the list of operations.
        operations.append(
            build_recommendation_operation(client, recommendation.resource_name)
        )
    # [END detect_keyword_recommendations]

    # If there are operations present, send a request to apply the
    # recommendations.
    if operations:
        apply_recommendations(client, customer_id, operations)


# [START build_apply_recommendation_operation]
def build_recommendation_operation(
    client: GoogleAdsClient, recommendation: str
) -> ApplyRecommendationOperation:
    """Creates a ApplyRecommendationOperation to apply the given recommendation.

    Args:
        client: an initialized GoogleAdsClient instance.
        recommendation: a resource name for the recommendation to be applied.
    """
    # If you have a recommendation ID instead of a resource name, you can create
    # a resource name like this:
    #
    # googleads_service = client.get_service("GoogleAdsService")
    # resource_name = googleads_service.recommendation_path(
    #   customer_id, recommendation.id
    # )

    operation: ApplyRecommendationOperation = client.get_type(
        "ApplyRecommendationOperation"
    )

    # Each recommendation type has optional parameters to override the
    # recommended values. Below is an example showing how to override a
    # recommended ad when a TextAdRecommendation is applied.
    #
    # operation.text_ad.ad.resource_name = "INSERT_AD_RESOURCE_NAME"
    #
    # For more details, see:
    # https://developers.google.com/google-ads/api/reference/rpc/latest/ApplyRecommendationOperation#apply_parameters

    operation.resource_name = recommendation
    return operation
    # [END build_apply_recommendation_operation]


# [START apply_recommendation]
def apply_recommendations(
    client: GoogleAdsClient,
    customer_id: str,
    operations: List[ApplyRecommendationOperation],
) -> None:
    """Applies a batch of recommendations.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        operations: a list of ApplyRecommendationOperation messages.
    """
    # Issues a mutate request to apply the recommendations.
    recommendation_service = client.get_service("RecommendationService")
    response: ApplyRecommendationResult = (
        recommendation_service.apply_recommendation(
            customer_id=customer_id, operations=operations
        )
    )

    for result in response.results:
        print(
            "Applied a recommendation with resource name: "
            f"'{result.resource_name}'."
        )
        # [END apply_recommendation]


if __name__ == "__main__":
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description=(
            "Retrieves keyword recommendations for specified customer and "
            "applies them."
        )
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
        version="v22"
    )

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
