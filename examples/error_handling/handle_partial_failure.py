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
"""This shows how to handle responses that may include partial_failure errors."""


import argparse
import sys
import uuid
from typing import Any, List

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.ads.googleads.v22.services.services.ad_group_service import (
    AdGroupServiceClient,
)
from google.ads.googleads.v22.services.services.campaign_service import (
    CampaignServiceClient,
)
from google.ads.googleads.v22.services.types.ad_group_service import (
    AdGroupOperation,
    MutateAdGroupsResponse,
    MutateAdGroupsRequest,
)


def main(client: GoogleAdsClient, customer_id: str, campaign_id: str) -> None:
    """Runs the example code, which demonstrates how to handle partial failures.

    The example creates three Ad Groups, two of which intentionally fail in
    order to generate a partial failure error. It also demonstrates how to
    properly identify a partial error and how to log the error messages.

    Args:
        client:  An initialized GoogleAdsClient instance.
        customer_id: A valid customer account ID.
        campaign_id: The ID for a campaign to create Ad Groups under.
    """
    try:
        ad_group_response: MutateAdGroupsResponse = create_ad_groups(
            client, customer_id, campaign_id
        )
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
    else:
        print_results(client, ad_group_response)


# [START handle_partial_failure]
def create_ad_groups(
    client: GoogleAdsClient, customer_id: str, campaign_id: str
) -> MutateAdGroupsResponse:
    """Creates three Ad Groups, two of which intentionally generate errors.

    Args:
        client: An initialized GoogleAdsClient instance.
        customer_id: A valid customer account ID.
        campaign_id: The ID for a campaign to create Ad Groups under.

    Returns: A MutateAdGroupsResponse message instance.
    """
    ad_group_service: AdGroupServiceClient = client.get_service(
        "AdGroupService"
    )
    campaign_service: CampaignServiceClient = client.get_service(
        "CampaignService"
    )
    resource_name: str = campaign_service.campaign_path(
        customer_id, campaign_id
    )

    invalid_resource_name: str = campaign_service.campaign_path(customer_id, 0)
    ad_group_operations: List[AdGroupOperation] = []

    # This AdGroup should be created successfully - assuming the campaign in
    # the params exists.
    ad_group_op1: AdGroupOperation = client.get_type("AdGroupOperation")
    ad_group_op1.create.name = f"Valid AdGroup: {uuid.uuid4()}"
    ad_group_op1.create.campaign = resource_name
    ad_group_operations.append(ad_group_op1)

    # This AdGroup will always fail - campaign ID 0 in resource names is
    # never valid.
    ad_group_op2: AdGroupOperation = client.get_type("AdGroupOperation")
    ad_group_op2.create.name = f"Broken AdGroup: {uuid.uuid4()}"
    ad_group_op2.create.campaign = invalid_resource_name
    ad_group_operations.append(ad_group_op2)

    # This AdGroup will always fail - duplicate ad group names are not allowed.
    ad_group_op3: AdGroupOperation = client.get_type("AdGroupOperation")
    ad_group_op3.create.name = ad_group_op1.create.name
    ad_group_op3.create.campaign = resource_name
    ad_group_operations.append(ad_group_op3)

    # Issue a mutate request, setting partial_failure=True.
    request: MutateAdGroupsRequest = client.get_type("MutateAdGroupsRequest")
    request.customer_id = customer_id
    request.operations = ad_group_operations
    request.partial_failure = True
    return ad_group_service.mutate_ad_groups(request=request)
    # [END handle_partial_failure]


# [START handle_partial_failure_1]
def is_partial_failure_error_present(response: MutateAdGroupsResponse) -> bool:
    """Checks whether a response message has a partial failure error.

    In Python the partial_failure_error attr is always present on a response
    message and is represented by a google.rpc.Status message. So we can't
    simply check whether the field is present, we must check that the code is
    non-zero. Error codes are represented by the google.rpc.Code proto Enum:
    https://github.com/googleapis/googleapis/blob/master/google/rpc/code.proto

    Args:
        response:  A MutateAdGroupsResponse message instance.

    Returns: A boolean, whether or not the response message has a partial
        failure error.
    """
    partial_failure: Any = getattr(response, "partial_failure_error", None)
    code: int = int(getattr(partial_failure, "code", 0))  # Default to 0 if None
    return code != 0
    # [END handle_partial_failure_1]


# [START handle_partial_failure_2]
def print_results(
    client: GoogleAdsClient, response: MutateAdGroupsResponse
) -> None:
    """Prints partial failure errors and success messages from a response.

    This function shows how to retrieve partial_failure errors from a response
    message (in the case of this example the message will be of type
    MutateAdGroupsResponse) and how to unpack those errors to GoogleAdsFailure
    instances. It also shows that a response with partial failures may still
    contain successful requests, and that those messages should be parsed
    separately. As an example, a GoogleAdsFailure object from this example will
    be structured similar to:

    error_code {
      range_error: TOO_LOW
    }
    message: "Too low."
    trigger {
      string_value: ""
    }
    location {
      field_path_elements {
        field_name: "operations"
        index {
          value: 1
        }
      }
      field_path_elements {
        field_name: "create"
      }
      field_path_elements {
        field_name: "campaign"
      }
    }

    Args:
        client: an initialized GoogleAdsClient.
        response: a MutateAdGroupsResponse instance.
    """
    # Check for existence of any partial failures in the response.
    if is_partial_failure_error_present(response):
        print("Partial failures occurred. Details will be shown below.\n")
        # Prints the details of the partial failure errors.
        partial_failure: Any = getattr(response, "partial_failure_error", None)
        # partial_failure_error.details is a repeated field and iterable
        error_details: List[Any] = getattr(partial_failure, "details", [])

        for error_detail in error_details:
            # Retrieve an instance of the GoogleAdsFailure class from the client
            failure_message: Any = client.get_type("GoogleAdsFailure")
            # Parse the string into a GoogleAdsFailure message instance.
            # To access class-only methods on the message we retrieve its type.
            GoogleAdsFailure: Any = type(failure_message)
            failure_object: Any = GoogleAdsFailure.deserialize(
                error_detail.value
            )

            for error in failure_object.errors:
                # Construct and print a string that details which element in
                # the above ad_group_operations list failed (by index number)
                # as well as the error message and error code.
                print(
                    "A partial failure at index "
                    f"{error.location.field_path_elements[0].index} occurred "
                    f"\nError message: {error.message}\nError code: "
                    f"{error.error_code}"
                )
    else:
        print(
            "All operations completed successfully. No partial failure "
            "to show."
        )

    # In the list of results, operations from the ad_group_operation list
    # that failed will be represented as empty messages. This loop detects
    # such empty messages and ignores them, while printing information about
    # successful operations.
    for message in response.results:
        if not message:
            continue

        print(f"Created ad group with resource_name: {message.resource_name}.")
        # [END handle_partial_failure_2]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Adds an ad group for specified customer and campaign id."
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
        "-i", "--campaign_id", type=str, required=True, help="The campaign ID."
    )
    args = parser.parse_args()

    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client: GoogleAdsClient = GoogleAdsClient.load_from_storage(
        version="v22"
    )

    main(googleads_client, args.customer_id, args.campaign_id)
