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
"""This example illustrate how to retrieve and apply recommendations.

The auto-apply feature, which automatically applies recommendations as they
become eligible, is currently supported by the Google Ads UI but not by the
Google Ads API. See https://support.google.com/google-ads/answer/10279006
for more information on using auto-apply in the Google Ads UI.
"""

import argparse
from re import I
import sys
import time

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

# The maximum number of recommendations to periodically retrieve and apply.  In a real
# application, such a limit would typically not be used.
MAX_RESULT_SIZE = 2

# The number of times to retrieve and apply recommendations. In a real application, such a
# limit would typically not be used.
NUMBER_OF_RUNS = 3

# The time to wait between two runs. In a real application, this would typically be set to
# minutes or hours instead of seconds.
SECONDS_TO_WAIT = 5


# [START detect_and_apply_recommendations]
def main(client, customer_id):
    ga_service = client.get_service("GoogleAdsService")

    query = f"""SELECT recommendation.resource_name
        FROM recommendation
        WHERE recommendation.type = KEYWORD
        LIMIT {MAX_RESULT_SIZE}"""

    recommendation_service = client.get_service("RecommendationService")

    for i in range(NUMBER_OF_RUNS + 1):
        search_request = client.get_type("SearchGoogleAdsStreamRequest")
        search_request.customer_id = customer_id
        search_request.query = query
        stream = ga_service.search_stream(request=search_request)

        apply_recommendation_operations = []

        for batch in stream:
            for row in batch.results:
                recommendation = row.recommendation

                apply_recommendation_operation = client.get_type(
                    "ApplyRecommendationOperation"
                )

                apply_recommendation_operation.resource_name = (
                    recommendation_service.recommendation_path(
                        customer_id, recommendation.id
                    )
                )

                apply_recommendation_operations.append(
                    apply_recommendation_operation
                )

            recommendation_response = (
                recommendation_service.apply_recommendation(
                    customer_id=customer_id,
                    operations=apply_recommendation_operations,
                )
            )

            for resp in recommendation_response:
                for row in resp.results:
                    print(
                        f"Applied recommendation with resource name:  \
                        {recommendation_response.resource_name}"
                    )

        print(
            f"Waiting {SECONDS_TO_WAIT} seconds before checking for additional \
                recommendations."
        )
        time.sleep(float(SECONDS_TO_WAIT))
    # [END detect_and_apply_recommendations]


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v10")

    parser = argparse.ArgumentParser(
        description=("Detectes and applies a specified recommendation.")
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
