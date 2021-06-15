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
"""This example illustrates how to apply a specified recommendation.

To retrieve recommendations for text ads, run get_text_ad_recommendations.py.
"""


import argparse
import sys

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


# [START apply_recommendation]
def main(client, customer_id, recommendation_id):
    recommendation_service = client.get_service("RecommendationService")

    apply_recommendation_operation = client.get_type(
        "ApplyRecommendationOperation"
    )

    apply_recommendation_operation.resource_name = recommendation_service.recommendation_path(
        customer_id, recommendation_id
    )

    recommendation_response = recommendation_service.apply_recommendation(
        customer_id=customer_id, operations=[apply_recommendation_operation]
    )

    print(
        "Applied recommendation with resource name: "
        f"'{recommendation_response.results[0].resource_name}'"
    )
    # [END apply_recommendation]


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v8")

    parser = argparse.ArgumentParser(
        description=("Applies a specified recommendation.")
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
    args = parser.parse_args()

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
