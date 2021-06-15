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
"""Handles RateExceededError in an application.

This code example runs 5 requests sequentially, each request attempting to
validate 100 keywords. While it is unlikely that running these requests would
trigger a rate exceeded error, substantially increasing the number of requests
may have that effect. Note that this example is for illustrative purposes only,
and you shouldn't intentionally try to trigger a rate exceed error in your
application.
"""


import argparse
from time import sleep

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

# Number of requests to be run.
NUM_REQUESTS = 5
# Number of keywords to be validated in each API call.
NUM_KEYWORDS = 100
# Number of retries to be run in case of a RateExceededError.
NUM_RETRIES = 3
# Minimum number of seconds to wait before a retry.
RETRY_SECONDS = 10


def main(client, customer_id, ad_group_id):
    """Runs the example code, which shows how to handle rate exceeded errors.

    Args:
        client:  An initialized GoogleAdsClient instance.
        customer_id: A valid customer account ID.
        ad_group_id: The ad group ID to validate keywords from.
    """
    quota_error_enum = client.get_type("QuotaErrorEnum").QuotaError
    resource_exhausted = quota_error_enum.RESOURCE_EXHAUSTED
    temp_resource_exhausted = quota_error_enum.RESOURCE_TEMPORARILY_EXHAUSTED

    for i in range(NUM_REQUESTS):
        operations = _create_ad_group_criterion_operations(
            client, customer_id, ad_group_id, i
        )

        try:
            retry_count = 0
            retry_seconds = RETRY_SECONDS

            while retry_count < NUM_RETRIES:
                try:
                    _request_mutate_and_display_result(
                        client, customer_id, operations
                    )
                    break
                except GoogleAdsException as ex:
                    has_rate_exceeded_error = False
                    for googleads_error in ex.failure.errors:
                        # Checks if any of the errors are
                        # QuotaError.RESOURCE_EXHAUSTED or
                        # QuotaError.RESOURCE_TEMPORARILY_EXHAUSTED.
                        quota_error = googleads_error.error_code.quota_error
                        if (
                            quota_error == resource_exhausted
                            or quota_error == temp_resource_exhausted
                        ):
                            print(
                                "Received rate exceeded error, retry after"
                                f"{retry_seconds} seconds."
                            )
                            sleep(retry_seconds)
                            has_rate_exceeded_error = True
                            retry_count += 1
                            # Here exponential backoff is employed to ensure
                            # the account doesn't get rate limited by making
                            # too many requests too quickly. This increases the
                            # time to wait between requests by a factor of 2.
                            retry_seconds *= 2
                            break
                    # Bubbles up when there is not a RateExceededError
                    if not has_rate_exceeded_error:
                        raise ex
                finally:
                    if retry_count == NUM_RETRIES:
                        raise Exception(
                            "Could not recover after making "
                            f"{retry_count} attempts."
                        )
        except Exception as ex:
            # Prints any unhandled exception and bubbles up.
            print(f"Failed to validate keywords: {ex}")
            raise ex


def _create_ad_group_criterion_operations(
    client, customer_id, ad_group_id, request_index
):
    """Creates ad group criterion operations.

    The number of operations created depends on the number of keywords this
    example should remove. That value is configurable via the NUM_KEYWORDS
    variable.

    Args:
        client:  An initialized GoogleAdsClient instance.
        customer_id: A valid customer account ID.
        ad_group_id: An ID for an AdGroup.
        request_index: The number from a sequence of requests in which these
            operations will be sent.

    Returns:
        A list of AdGroupCriterionOperation instances.
    """
    ad_group_service = client.get_service("AdGroupService")
    status = client.get_type(
        "AdGroupCriterionStatusEnum"
    ).AdGroupCriterionStatus.ENABLED
    match_type = client.get_type("KeywordMatchTypeEnum").KeywordMatchType.EXACT

    operations = []
    for i in range(NUM_KEYWORDS):
        ad_group_criterion_operation = client.get_type(
            "AdGroupCriterionOperation"
        )
        ad_group_criterion = ad_group_criterion_operation.create
        ad_group_criterion.ad_group = ad_group_service.ad_group_path(
            customer_id, ad_group_id
        )
        ad_group_criterion.status = status
        ad_group_criterion.keyword.text = (
            f"mars cruise req {request_index} seed {i}"
        )
        ad_group_criterion.keyword.match_type = match_type
        operations.append(ad_group_criterion_operation)

    return operations


def _request_mutate_and_display_result(client, customer_id, operations):
    """Mutates a set of ad group criteria as a dry-run and displays the results.

    The request is sent with validate_only set to true, so no actual mutations
    will be made in the API.

    Args:
        client:  An initialized GoogleAdsClient instance.
        customer_id: A valid customer account ID.
        operations: a list of AdGroupCriterionOperation instances.
    """
    ad_group_criterion_service = client.get_service("AdGroupCriterionService")
    request = client.get_type("MutateAdGroupCriteriaRequest")
    request.customer_id = customer_id
    request.operations = operations
    request.validate_only = True
    response = ad_group_criterion_service.mutate_ad_group_criteria(
        request=request
    )
    print(f"Added {len(response.results)} ad group criteria:")
    for ad_group_criterion in response.results:
        print(f"Resource name: '{ad_group_criterion.resource_name}'")


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v8")

    parser = argparse.ArgumentParser(
        description="Handles RateExceededError in an application.."
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
        "-a",
        "--ad_group_id",
        type=str,
        required=True,
        help="The ID of an ad group belonging to the given customer.",
    )
    args = parser.parse_args()

    main(googleads_client, args.customer_id, args.ad_group_id)
