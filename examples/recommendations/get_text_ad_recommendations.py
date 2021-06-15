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
"""This example gets all TEXT_AD recommendations.

To add campaigns, run add_campaigns.py.
"""


import argparse
import sys

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


# [START get_text_ad_recommendations]
def main(client, customer_id):
    ga_service = client.get_service("GoogleAdsService")

    query = """
        SELECT
          recommendation.type,
          recommendation.campaign,
          recommendation.text_ad_recommendation
        FROM recommendation
        WHERE recommendation.type = TEXT_AD"""

    search_request = client.get_type("SearchGoogleAdsStreamRequest")
    search_request.customer_id = customer_id
    search_request.query = query
    response = ga_service.search_stream(request=search_request)

    for batch in response:
        for row in batch.results:
            recommendation = row.recommendation
            recommended_ad = recommendation.text_ad_recommendation.ad
            print(
                f'Recommendation ("{recommendation.resource_name}") '
                f'was found for campaign "{recommendation.campaign}".'
            )

            if recommended_ad.display_url:
                print(f'\tDisplay URL = "{recommended_ad.display_url}"')

            for url in recommended_ad.final_urls:
                print(f'\tFinal URL = "{url}"')

            for url in recommended_ad.final_mobile_urls:
                print(f'\tFinal Mobile URL = "{url}"')
    # [END get_text_ad_recommendations]


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v8")

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
            print(f'	Error with message "{error.message}".')
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print(f"\t\tOn field: {field_path_element.field_name}")
        sys.exit(1)
