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
"""This example dismisses a given recommendation.

To retrieve recommendations for text ads, run get_text_ad_recommendations.py.
"""


import argparse
import sys

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.ads.googleads.v22.services.services.recommendation_service import (
    RecommendationServiceClient,
)
from google.ads.googleads.v22.services.types.recommendation_service import (
    DismissRecommendationRequest,
    DismissRecommendationResponse,
)


def main(
    client: GoogleAdsClient, customer_id: str, recommendation_id: str
) -> None:
    recommendation_service: RecommendationServiceClient = client.get_service(
        "RecommendationService"
    )
    request: DismissRecommendationRequest = client.get_type(
        "DismissRecommendationRequest"
    )
    operation = request.DismissRecommendationOperation()
    operation.resource_name = recommendation_service.recommendation_path(
        customer_id, recommendation_id
    )
    request.customer_id = customer_id
    request.operations.append(operation)

    response: DismissRecommendationResponse = (
        recommendation_service.dismiss_recommendation(request=request)
    )

    print(
        "Dismissed recommendation with resource name: "
        f"'{response.results[0].resource_name}'."
    )


if __name__ == "__main__":
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description=("Dismisses a recommendation with the given ID.")
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
        "-r",
        "--recommendation_id",
        type=str,
        required=True,
        help="The recommendation ID.",
    )
    args: argparse.Namespace = parser.parse_args()

    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client: GoogleAdsClient = GoogleAdsClient.load_from_storage(
        version="v22"
    )

    try:
        main(googleads_client, args.customer_id, args.recommendation_id)
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
