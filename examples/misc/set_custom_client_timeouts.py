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

This demonstrates custom client timeouts in the context of server streaming and
unary calls.

For more information about the concepts, see this documentation:
https://grpc.io/docs/what-is-grpc/core-concepts/#rpc-life-cycle
"""


import argparse
import sys

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.api_core.exceptions import DeadlineExceeded
from google.api_core.retry import Retry


_CLIENT_TIMEOUT_SECONDS = 5 * 60  # 5 minutes.
_QUERY = "SELECT campaign.id FROM campaign"


def main(client, customer_id):
    """Main method, to run this code example as a standalone application."""
    _make_server_streaming_call(client, customer_id)
    _make_unary_call(client, customer_id)


def _make_server_streaming_call(client, customer_id):
    """Makes a server streaming call using a custom client timeout.

    Args:
        client: An initialized GoogleAds client.
        customer_id: The str Google Ads customer ID.
    """
    ga_service = client.get_service("GoogleAdsService")
    campaign_ids = []

    try:
        search_request = client.get_type("SearchGoogleAdsStreamRequest")
        search_request.customer_id = customer_id
        search_request.query = _QUERY
        stream = ga_service.search_stream(
            request=search_request,
            # As of v5, any server streaming call has a default timeout
            # setting. For this particular call, the default setting can be
            # found in the following file:
            # https://github.com/googleads/google-ads-python/blob/master/google/ads/google_ads/v6/services/google_ads_service_client_config.py
            #
            # When making a server streaming call, an optional argument is
            # provided and can be used to override the default timeout setting
            # with a given value.
            timeout=_CLIENT_TIMEOUT_SECONDS,
        )

        for batch in stream:
            for row in batch.results:
                campaign_ids.append(row.campaign.id)

        print("The server streaming call completed before the timeout.")
    except DeadlineExceeded as ex:
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


def _make_unary_call(client, customer_id):
    """Makes a unary call using a custom client timeout.

    Args:
        client: An initialized GoogleAds client.
        customer_id: The Google Ads customer ID.
    """
    ga_service = client.get_service("GoogleAdsService")
    campaign_ids = []

    try:
        search_request = client.get_type("SearchGoogleAdsRequest")
        search_request.customer_id = customer_id
        search_request.query = _QUERY
        results = ga_service.search(
            request=search_request,
            # As of v5, any unary call is retryable and has default retry
            # settings. Complete information about these settings can be found
            # here: https://googleapis.dev/python/google-api-core/latest/retry.html
            #
            # For this particular call, the default retry settings can be found
            # in the following file:
            # https://github.com/googleads/google-ads-python/blob/master/google/ads/google_ads/v6/services/google_ads_service_client_config.py
            #
            # When making a unary call, an optional argument is provided and
            # can be used to override the default retry settings with given
            # values.
            retry=Retry(
                # Sets the maximum accumulative timeout of the call; it
                # includes all tries.
                deadline=_CLIENT_TIMEOUT_SECONDS,
                # Sets the timeout that is used for the first try to one tenth
                # of the maximum accumulative timeout of the call.
                initial=_CLIENT_TIMEOUT_SECONDS / 10,
                # Sets the maximum timeout that can be used for any given try
                # to one fifth of the maximum accumulative timeout of the call
                # (two times greater than the timeout that is needed for the
                # first try).
                maximum=_CLIENT_TIMEOUT_SECONDS / 5,
            ),
        )

        for row in results:
            campaign_ids.append(row.campaign.id)

        print("The unary call completed before the timeout.")
    except DeadlineExceeded as ex:
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


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v8")

    parser = argparse.ArgumentParser(
        description="Demonstrates custom client timeouts in the context of "
        "server streaming and unary calls."
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

    main(googleads_client, args.customer_id)
