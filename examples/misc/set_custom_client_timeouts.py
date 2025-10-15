#!/usr/bin/env python
# Copyright 2020 Google LLC
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
"""This example illustrates the use of custom client timeouts.

Even though this example demonstrates custom client timeouts in the context of
streaming and unary calls separately, the behavior can be applied to any request
method exposed by this library.

For more information about the concepts, see this documentation:
https://grpc.io/docs/what-is-grpc/core-concepts/#rpc-life-cycle
"""


import argparse
from collections.abc import Iterator
import sys
from typing import List

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.ads.googleads.v22.services.services.google_ads_service.client import (
    GoogleAdsServiceClient,
)
from google.ads.googleads.v22.services.types.google_ads_service import (
    GoogleAdsRow,
    SearchGoogleAdsRequest,
    SearchGoogleAdsStreamRequest,
    SearchGoogleAdsStreamResponse,
)
from google.api_core.exceptions import DeadlineExceeded
from google.api_core.retry import Retry


_CLIENT_TIMEOUT_SECONDS = 5 * 60  # 5 minutes.
_QUERY: str = "SELECT campaign.id FROM campaign"


def main(client: GoogleAdsClient, customer_id: str) -> None:
    """Main method, to run this code example as a standalone application."""
    make_server_streaming_call(client, customer_id)
    make_unary_call(client, customer_id)


# [START set_custom_client_timeouts]
def make_server_streaming_call(
    client: GoogleAdsClient, customer_id: str
) -> None:
    """Makes a server streaming call using a custom client timeout.

    Args:
        client: An initialized GoogleAds client.
        customer_id: The str Google Ads customer ID.
    """
    ga_service: GoogleAdsServiceClient = client.get_service("GoogleAdsService")
    campaign_ids: List[str] = []

    try:
        search_request: SearchGoogleAdsStreamRequest = client.get_type(
            "SearchGoogleAdsStreamRequest"
        )
        search_request.customer_id = customer_id
        search_request.query = _QUERY
        stream: Iterator[SearchGoogleAdsStreamResponse] = (
            ga_service.search_stream(
                request=search_request,
                # When making any request, an optional "timeout" parameter can be
                # provided to specify a client-side response deadline in seconds.
                # If not set, then no timeout will be enforced by the client and
                # the channel will remain open until the response is completed or
                # severed, either manually or by the server.
                timeout=_CLIENT_TIMEOUT_SECONDS,
            )
        )

        batch: SearchGoogleAdsStreamResponse
        for batch in stream:
            row: GoogleAdsRow
            for row in batch.results:
                campaign_ids.append(row.campaign.id)

        print("The server streaming call completed before the timeout.")
    except DeadlineExceeded:
        print("The server streaming call did not complete before the timeout.")
        sys.exit(1)
    except GoogleAdsException as ex:
        print(
            f"Request with ID '{ex.request_id}' failed with status "
            f"'{ex.error.code().name}' and includes the following errors:"
        )
        for error in ex.failure.errors:
            print(f"\tError with message '{error.message}'.")
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print(f"\t\tOn field: {field_path_element.field_name}")
        sys.exit(1)

    print(f"Total # of campaign IDs retrieved: {len(campaign_ids)}")
    # [END set_custom_client_timeouts]


# [START set_custom_client_timeouts_1]
def make_unary_call(client: GoogleAdsClient, customer_id: str) -> None:
    """Makes a unary call using a custom client timeout.

    Args:
        client: An initialized GoogleAds client.
        customer_id: The Google Ads customer ID.
    """
    ga_service: GoogleAdsServiceClient = client.get_service("GoogleAdsService")
    campaign_ids: List[str] = []

    try:
        search_request: SearchGoogleAdsRequest = client.get_type(
            "SearchGoogleAdsRequest"
        )
        search_request.customer_id = customer_id
        search_request.query = _QUERY
        results: Iterator[GoogleAdsRow] = ga_service.search(
            request=search_request,
            # When making any request, an optional "retry" parameter can be
            # provided to specify its retry behavior. Complete information about
            # these settings can be found here:
            # https://googleapis.dev/python/google-api-core/latest/retry.html
            retry=Retry(
                # Sets the maximum accumulative timeout of the call; it
                # includes all tries.
                deadline=_CLIENT_TIMEOUT_SECONDS,
                # Sets the timeout that is used for the first try to one tenth
                # of the maximum accumulative timeout of the call.
                # Note: This overrides the default value and can lead to
                # RequestError.RPC_DEADLINE_TOO_SHORT errors when too small. We
                # recommend changing the value only if necessary.
                initial=_CLIENT_TIMEOUT_SECONDS / 10,
                # Sets the maximum timeout that can be used for any given try
                # to one fifth of the maximum accumulative timeout of the call
                # (two times greater than the timeout that is needed for the
                # first try).
                maximum=_CLIENT_TIMEOUT_SECONDS / 5,
            ),
        )

        row: GoogleAdsRow
        for row in results:
            campaign_ids.append(row.campaign.id)

        print("The unary call completed before the timeout.")
    except DeadlineExceeded:
        print("The unary call did not complete before the timeout.")
        sys.exit(1)
    except GoogleAdsException as ex:
        print(
            f"Request with ID '{ex.request_id}' failed with status "
            f"'{ex.error.code().name}' and includes the following errors:"
        )
        for error in ex.failure.errors:
            print(f"\tError with message '{error.message}'.")
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print(f"\t\tOn field: {field_path_element.field_name}")
        sys.exit(1)

    print(f"Total # of campaign IDs retrieved: {len(campaign_ids)}")
    # [END set_custom_client_timeouts_1]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=(
            "Demonstrates custom client timeouts in the context of "
            "server streaming and unary calls."
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
    args = parser.parse_args()

    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v22")

    main(googleads_client, args.customer_id)
