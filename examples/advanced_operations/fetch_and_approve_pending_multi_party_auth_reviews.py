#!/usr/bin/env python
# Copyright 2026 Google LLC
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
"""This example fetches pending multi-party approvals and approves the first one.

Multi-party authorization (MPA) reviews can only be resolved one at a time.
In this code example, we illustrate approving the first pending review request.
"""

import argparse
import sys
from typing import List

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


def main(client: GoogleAdsClient, customer_id: str) -> None:
    """The main method that retrieves and approves pending MPA reviews.

    Args:
        client: An initialized GoogleAdsClient instance.
        customer_id: The client customer ID.
    """
    # Retrieve the list of pending MPA reviews.
    pending_reviews = fetch_pending_mpa_reviews(client, customer_id)

    if pending_reviews:
        # Multi-party auth reviews can only be resolved one at a time. In this
        # code example, we illustrate approving the first pending review request.
        approve_mpa_review(client, customer_id, pending_reviews[0])


# [START fetch_mpa_review]
def fetch_pending_mpa_reviews(
    client: GoogleAdsClient, customer_id: str
) -> List[str]:
    """Fetches the pending MPA reviews.

    Args:
        client: An initialized GoogleAdsClient instance.
        customer_id: The client customer ID.

    Returns:
        A list of resource names for the pending multi-party auth reviews.
    """
    pending_reviews: List[str] = []
    ga_service = client.get_service("GoogleAdsService")

    # Create a query that will retrieve all the pending MPA reviews.
    query = """
        SELECT
          multi_party_auth_review.resource_name,
          multi_party_auth_review.multi_party_auth_review_id,
          multi_party_auth_review.creation_date_time,
          multi_party_auth_review.request_user_email,
          multi_party_auth_review.operation_type,
          multi_party_auth_review.justification,
          multi_party_auth_review.target_resource,
          multi_party_auth_review.customer_user_access_review.old_customer_user_access,
          multi_party_auth_review.customer_user_access_review.new_customer_user_access,
          multi_party_auth_review.customer_user_access_invitation_review.new_customer_user_access_invitation
        FROM multi_party_auth_review
        WHERE multi_party_auth_review.review_status = 'PENDING'"""

    stream = ga_service.search_stream(customer_id=customer_id, query=query)

    for batch in stream:
        for row in batch.results:
            mpa_review = row.multi_party_auth_review
            print(
                f"{mpa_review.request_user_email} created a pending "
                f"multi-party auth review with ID {mpa_review.multi_party_auth_review_id} "
                f"at {mpa_review.creation_date_time}. This request is for target "
                f"resource type = {mpa_review.target_resource.name} and operation type = "
                f"{mpa_review.operation_type.name}. The justification is "
                f'"{mpa_review.justification}".'
            )

            if (
                mpa_review.target_resource
                == client.enums.MultiPartyAuthReviewTargetResourceEnum.CUSTOMER_USER_ACCESS
            ):
                access_review = mpa_review.customer_user_access_review
                if (
                    mpa_review.operation_type
                    == client.enums.MultiPartyAuthOperationTypeEnum.UPDATE
                ):
                    # When updating a customer user access, only the new access level
                    # is populated.
                    print(
                        f"Old resource name: {access_review.old_customer_user_access}, "
                        f"new access role: {access_review.new_customer_user_access.access_role.name}."
                    )
                elif (
                    mpa_review.operation_type
                    == client.enums.MultiPartyAuthOperationTypeEnum.REMOVE
                ):
                    print(
                        f"Old resource name: {access_review.old_customer_user_access}."
                    )
            elif (
                mpa_review.target_resource
                == client.enums.MultiPartyAuthReviewTargetResourceEnum.CUSTOMER_USER_ACCESS_INVITATION
            ):
                new_invite = (
                    mpa_review.customer_user_access_invitation_review.new_customer_user_access_invitation
                )
                print(
                    f"Invitation email address: {new_invite.email_address}, "
                    f"Role: {new_invite.access_role.name}."
                )

            pending_reviews.append(mpa_review.resource_name)

    return pending_reviews
    # [END fetch_mpa_review]


# [START approve_mpa_review]
def approve_mpa_review(
    client: GoogleAdsClient, customer_id: str, pending_review: str
) -> None:
    """Approves the MPA auth review.

    Args:
        client: An initialized GoogleAdsClient instance.
        customer_id: The client customer ID.
        pending_review: The resource name of the pending review.
    """
    mpa_review_service = client.get_service("MultiPartyAuthReviewService")

    # Currently, you can only approve one request at a time. In addition, the approvals
    # can only be done by a second administrator.
    request = client.get_type("ResolveMultiPartyAuthReviewRequest")
    request.customer_id = customer_id
    operation = client.get_type("ResolveMultiPartyAuthReviewOperation")
    operation.multi_party_auth_review = pending_review
    operation.new_status = client.enums.MultiPartyAuthReviewStatusEnum.APPROVED
    request.operations.append(operation)

    response = mpa_review_service.resolve_multi_party_auth_review(
        request=request
    )

    result_or_error = response.result_or_error[0]

    if "result" in result_or_error:
        result = result_or_error.result
        print(
            f"Approved multi-party auth review: {result.multi_party_auth_review}."
        )
        if result.customer_user_access_invitation:
            print(
                f"New user invitation created: {result.customer_user_access_invitation}"
            )
        elif result.customer_user_access:
            print(
                f"Affected customer user access resource: {result.customer_user_access}"
            )
    else:
        # Partial failure error
        failure_message = client.get_type("GoogleAdsFailure")
        GoogleAdsFailure = type(failure_message)
        errors_count = 0
        for error_detail in result_or_error.partial_failure_error.details:
            failure_object = GoogleAdsFailure.deserialize(error_detail.value)
            for error in failure_object.errors:
                print(f"\tError with message '{error.message}'.")
                errors_count += 1
        print(f"{errors_count} partial failure error(s) occurred")
        # [END approve_mpa_review]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=(
            "Fetches pending multi-party approvals and approves the first one."
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
    googleads_client = GoogleAdsClient.load_from_storage(version="v24")

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
