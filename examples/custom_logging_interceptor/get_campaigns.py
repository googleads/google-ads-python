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
"""This example illustrates how to get all campaigns and log details to

Google Cloud Logging using a custom logging interceptor.
"""

import argparse
import sys
from typing import Any, Iterable

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.ads.googleads.v20.services.services.google_ads_service import GoogleAdsServiceClient
from google.ads.googleads.v20.services.types.google_ads_service import SearchGoogleAdsStreamResponse
from google.ads.googleads.v20.types.google_ads_row import GoogleAdsRow

from cloud_logging_interceptor import CloudLoggingInterceptor


def main(client: GoogleAdsClient, customer_id: str) -> None:
    # Instantiate the GoogleAdsService object with a custom interceptor.
    ga_service: GoogleAdsServiceClient = client.get_service(
        "GoogleAdsService",
        interceptors=[CloudLoggingInterceptor(api_version="v20")],
    )

    query: str = """
        SELECT
          campaign.id,
          campaign.name
        FROM campaign
        ORDER BY campaign.id
        LIMIT 10"""

    # Issues a search request using streaming.
    stream: Iterable[SearchGoogleAdsStreamResponse] = ga_service.search_stream(customer_id=customer_id, query=query)

    for batch in stream:
        for row: GoogleAdsRow in batch.results:
            print(
                f"Campaign with ID {row.campaign.id} and name "
                f'"{row.campaign.name}" was found.'
            )


if __name__ == "__main__":
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Lists all campaigns for specified customer."
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
        version="v20"
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
