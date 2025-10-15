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
"""Creates operations to add members to a user list (a.k.a. audience).

The example uses an OfflineUserDataJob, and if requested, runs the job. If a
job ID is specified, the example adds operations to that job. Otherwise, it
creates a new job for the operations.

IMPORTANT: Your application should create a single job containing all of the
operations for a user list. This will be far more efficient than creating and
running multiple jobs that each contain a small set of operations.

This feature is only available to accounts that meet the requirements described
at: https://support.google.com/adspolicy/answer/6299717.
"""

import argparse
import hashlib
import sys
import uuid
from typing import List, Dict, Optional, Union, Iterable

from google.protobuf.any_pb2 import Any
from google.rpc import status_pb2

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.ads.googleads.v22.services.services.google_ads_service import (
    GoogleAdsServiceClient,
)
from google.ads.googleads.v22.services.services.user_list_service import (
    UserListServiceClient,
)
from google.ads.googleads.v22.services.services.offline_user_data_job_service import (
    OfflineUserDataJobServiceClient,
)
from google.ads.googleads.v22.services.types.google_ads_service import (
    SearchGoogleAdsStreamResponse,
)
from google.ads.googleads.v22.services.types.user_list_service import (
    UserListOperation,
    MutateUserListsResponse,
)
from google.ads.googleads.v22.resources.types.user_list import UserList
from google.ads.googleads.v22.services.types.offline_user_data_job_service import (
    AddOfflineUserDataJobOperationsRequest,
    OfflineUserDataJobOperation,
    AddOfflineUserDataJobOperationsResponse,
    CreateOfflineUserDataJobResponse,
)
from google.ads.googleads.v22.resources.types.offline_user_data_job import (
    OfflineUserDataJob,
)
from google.ads.googleads.v22.common.types.criteria import (
    AddressInfo,
)
from google.ads.googleads.v22.common.types.offline_user_data import (
    UserData,
    UserIdentifier,
)
from google.ads.googleads.v22.errors.types.errors import (
    GoogleAdsFailure,
    GoogleAdsError,
)


def main(
    client: GoogleAdsClient,
    customer_id: str,
    run_job: bool,
    user_list_id: Optional[str],
    offline_user_data_job_id: Optional[str],
    ad_user_data_consent: Optional[str],
    ad_personalization_consent: Optional[str],
) -> None:
    """Uses Customer Match to create and add users to a new user list.

    Args:
        client: The Google Ads client.
        customer_id: The ID for the customer that owns the user list.
        run_job: if True, runs the OfflineUserDataJob after adding operations.
            Otherwise, only adds operations to the job.
        user_list_id: ID of an existing user list. If None, a new user list is
            created.
        offline_user_data_job_id: ID of an existing OfflineUserDataJob in the
            PENDING state. If None, a new job is created.
        ad_user_data_consent: The consent status for ad user data for all
            members in the job.
        ad_personalization_consent: The personalization consent status for ad
            user data for all members in the job.
    """
    googleads_service: GoogleAdsServiceClient = client.get_service(
        "GoogleAdsService"
    )
    user_list_resource_name: str

    if not offline_user_data_job_id:
        if user_list_id:
            # Uses the specified Customer Match user list.
            user_list_resource_name = googleads_service.user_list_path(
                customer_id, user_list_id
            )
        else:
            # Creates a Customer Match user list.
            user_list_resource_name = create_customer_match_user_list(
                client, customer_id
            )

    add_users_to_customer_match_user_list(
        client,
        customer_id,
        user_list_resource_name,
        run_job,
        offline_user_data_job_id,
        ad_user_data_consent,
        ad_personalization_consent,
    )


# [START add_customer_match_user_list_3]
def create_customer_match_user_list(
    client: GoogleAdsClient, customer_id: str
) -> str:
    """Creates a Customer Match user list.

    Args:
        client: The Google Ads client.
        customer_id: The ID for the customer that owns the user list.

    Returns:
        The string resource name of the newly created user list.
    """
    # Creates the UserListService client.
    user_list_service_client: UserListServiceClient = client.get_service(
        "UserListService"
    )

    # Creates the user list operation.
    user_list_operation: UserListOperation = client.get_type(
        "UserListOperation"
    )

    # Creates the new user list.
    user_list: UserList = user_list_operation.create
    user_list.name = f"Customer Match list #{uuid.uuid4()}"
    user_list.description = (
        "A list of customers that originated from email and physical addresses"
    )
    # Sets the upload key type to indicate the type of identifier that is used
    # to add users to the list. This field is immutable and required for a
    # CREATE operation.
    user_list.crm_based_user_list.upload_key_type = (
        client.enums.CustomerMatchUploadKeyTypeEnum.CONTACT_INFO
    )
    # Membership life span must be between 0 and 540 days inclusive. See:
    # https://developers.google.com/google-ads/api/reference/rpc/latest/UserList#membership_life_span
    # Sets the membership life span to 30 days.
    user_list.membership_life_span = 30

    response: MutateUserListsResponse = (
        user_list_service_client.mutate_user_lists(
            customer_id=customer_id, operations=[user_list_operation]
        )
    )
    user_list_resource_name: str = response.results[0].resource_name
    print(
        f"User list with resource name '{user_list_resource_name}' was created."
    )

    return user_list_resource_name
    # [END add_customer_match_user_list_3]


# [START add_customer_match_user_list]
def add_users_to_customer_match_user_list(
    client: GoogleAdsClient,
    customer_id: str,
    user_list_resource_name: str,
    run_job: bool,
    offline_user_data_job_id: Optional[str],
    ad_user_data_consent: Optional[str],
    ad_personalization_consent: Optional[str],
) -> None:
    """Uses Customer Match to create and add users to a new user list.

    Args:
        client: The Google Ads client.
        customer_id: The ID for the customer that owns the user list.
        user_list_resource_name: The resource name of the user list to which to
            add users.
        run_job: If true, runs the OfflineUserDataJob after adding operations.
            Otherwise, only adds operations to the job.
        offline_user_data_job_id: ID of an existing OfflineUserDataJob in the
            PENDING state. If None, a new job is created.
        ad_user_data_consent: The consent status for ad user data for all
            members in the job.
        ad_personalization_consent: The personalization consent status for ad
            user data for all members in the job.
    """
    # Creates the OfflineUserDataJobService client.
    offline_user_data_job_service_client: OfflineUserDataJobServiceClient = (
        client.get_service("OfflineUserDataJobService")
    )
    offline_user_data_job_resource_name: str

    if offline_user_data_job_id:
        # Reuses the specified offline user data job.
        offline_user_data_job_resource_name = (
            offline_user_data_job_service_client.offline_user_data_job_path(
                customer_id, offline_user_data_job_id
            )
        )
    else:
        # Creates a new offline user data job.
        offline_user_data_job: OfflineUserDataJob = client.get_type(
            "OfflineUserDataJob"
        )
        offline_user_data_job.type_ = (
            client.enums.OfflineUserDataJobTypeEnum.CUSTOMER_MATCH_USER_LIST
        )
        offline_user_data_job.customer_match_user_list_metadata.user_list = (
            user_list_resource_name
        )

        # Specifies whether user consent was obtained for the data you are
        # uploading. For more details, see:
        # https://www.google.com/about/company/user-consent-policy
        if ad_user_data_consent:
            offline_user_data_job.customer_match_user_list_metadata.consent.ad_user_data = client.enums.ConsentStatusEnum[
                ad_user_data_consent
            ]
        if ad_personalization_consent:
            offline_user_data_job.customer_match_user_list_metadata.consent.ad_personalization = client.enums.ConsentStatusEnum[
                ad_personalization_consent
            ]

        # Issues a request to create an offline user data job.
        create_offline_user_data_job_response: (
            CreateOfflineUserDataJobResponse
        ) = offline_user_data_job_service_client.create_offline_user_data_job(
            customer_id=customer_id, job=offline_user_data_job
        )
        offline_user_data_job_resource_name = (
            create_offline_user_data_job_response.resource_name
        )
        print(
            "Created an offline user data job with resource name: "
            f"'{offline_user_data_job_resource_name}'."
        )

    # Issues a request to add the operations to the offline user data job.

    # Best Practice: This example only adds a few operations, so it only sends
    # one AddOfflineUserDataJobOperations request. If your application is adding
    # a large number of operations, split the operations into batches and send
    # multiple AddOfflineUserDataJobOperations requests for the SAME job. See
    # https://developers.google.com/google-ads/api/docs/remarketing/audience-types/customer-match#customer_match_considerations
    # and https://developers.google.com/google-ads/api/docs/best-practices/quotas#user_data
    # for more information on the per-request limits.
    request: AddOfflineUserDataJobOperationsRequest = client.get_type(
        "AddOfflineUserDataJobOperationsRequest"
    )
    request.resource_name = offline_user_data_job_resource_name
    request.operations = build_offline_user_data_job_operations(client)
    request.enable_partial_failure = True

    # Issues a request to add the operations to the offline user data job.
    response: AddOfflineUserDataJobOperationsResponse = (
        offline_user_data_job_service_client.add_offline_user_data_job_operations(
            request=request
        )
    )

    # Prints the status message if any partial failure error is returned.
    # Note: the details of each partial failure error are not printed here.
    # Refer to the error_handling/handle_partial_failure.py example to learn
    # more.
    # Extracts the partial failure from the response status.
    partial_failure: Union[status_pb2.Status, None] = getattr(
        response, "partial_failure_error", None
    )
    if getattr(partial_failure, "code", None) != 0:
        error_details: Iterable[Any, None] = getattr(
            partial_failure, "details", []
        )
        for error_detail in error_details:
            failure_message: GoogleAdsFailure = client.get_type(
                "GoogleAdsFailure"
            )
            # Retrieve the class definition of the GoogleAdsFailure instance
            # in order to use the "deserialize" class method to parse the
            # error_detail string into a protobuf message object.
            failure_object: GoogleAdsFailure = type(
                failure_message
            ).deserialize(error_detail.value)
            errors: Iterable[GoogleAdsError] = failure_object.errors

            for error in errors:
                print(
                    "A partial failure at index "
                    f"{error.location.field_path_elements[0].index} occurred.\n"
                    f"Error message: {error.message}\n"
                    f"Error code: {error.error_code}"
                )

    print("The operations are added to the offline user data job.")

    if not run_job:
        print(
            "Not running offline user data job "
            f"'{offline_user_data_job_resource_name}', as requested."
        )
        return

    # Issues a request to run the offline user data job for executing all
    # added operations.
    offline_user_data_job_service_client.run_offline_user_data_job(
        resource_name=offline_user_data_job_resource_name
    )

    # Retrieves and displays the job status.
    check_job_status(client, customer_id, offline_user_data_job_resource_name)
    # [END add_customer_match_user_list]


# [START add_customer_match_user_list_2]
def build_offline_user_data_job_operations(
    client: GoogleAdsClient,
) -> List[OfflineUserDataJobOperation]:
    """Creates a raw input list of unhashed user information.

    Each element of the list represents a single user and is a dict containing a
    separate entry for the keys "email", "phone", "first_name", "last_name",
    "country_code", and "postal_code". In your application, this data might come
    from a file or a database.

    Args:
        client: The Google Ads client.

    Returns:
        A list containing the operations.
    """
    # The first user data has an email address and a phone number.
    raw_record_1: Dict[str, str] = {
        "email": "dana@example.com",
        # Phone number to be converted to E.164 format, with a leading '+' as
        # required. This includes whitespace that will be removed later.
        "phone": "+1 800 5550101",
    }

    # The second user data has an email address, a mailing address, and a phone
    # number.
    raw_record_2: Dict[str, str] = {
        # Email address that includes a period (.) before the email domain.
        "email": "alex.2@example.com",
        # Address that includes all four required elements: first name, last
        # name, country code, and postal code.
        "first_name": "Alex",
        "last_name": "Quinn",
        "country_code": "US",
        "postal_code": "94045",
        # Phone number to be converted to E.164 format, with a leading '+' as
        # required.
        "phone": "+1 800 5550102",
    }

    # The third user data only has an email address.
    raw_record_3: Dict[str, str] = {"email": "charlie@example.com"}

    # Adds the raw records to a raw input list.
    raw_records: List[Dict[str, str]] = [
        raw_record_1,
        raw_record_2,
        raw_record_3,
    ]

    operations: List[OfflineUserDataJobOperation] = []
    # Iterates over the raw input list and creates a UserData object for each
    # record.
    for record in raw_records:
        # Creates a UserData object that represents a member of the user list.
        user_data: UserData = client.get_type("UserData")

        # Checks if the record has email, phone, or address information, and
        # adds a SEPARATE UserIdentifier object for each one found. For example,
        # a record with an email address and a phone number will result in a
        # UserData with two UserIdentifiers.

        # IMPORTANT: Since the identifier attribute of UserIdentifier
        # (https://developers.google.com/google-ads/api/reference/rpc/latest/UserIdentifier)
        # is a oneof
        # (https://protobuf.dev/programming-guides/proto3/#oneof-features), you
        # must set only ONE of hashed_email, hashed_phone_number, mobile_id,
        # third_party_user_id, or address-info. Setting more than one of these
        # attributes on the same UserIdentifier will clear all the other members
        # of the oneof. For example, the following code is INCORRECT and will
        # result in a UserIdentifier with ONLY a hashed_phone_number:

        # incorrect_user_identifier = client.get_type("UserIdentifier")
        # incorrect_user_identifier.hashed_email = "..."
        # incorrect_user_identifier.hashed_phone_number = "..."

        # The separate 'if' statements below demonstrate the correct approach
        # for creating a UserData object for a member with multiple
        # UserIdentifiers.

        # Checks if the record has an email address, and if so, adds a
        # UserIdentifier for it.
        if "email" in record:
            user_identifier: UserIdentifier = client.get_type("UserIdentifier")
            user_identifier.hashed_email = normalize_and_hash(
                record["email"], True
            )
            # Adds the hashed email identifier to the UserData object's list.
            user_data.user_identifiers.append(user_identifier)

        # Checks if the record has a phone number, and if so, adds a
        # UserIdentifier for it.
        if "phone" in record:
            user_identifier: UserIdentifier = client.get_type("UserIdentifier")
            user_identifier.hashed_phone_number = normalize_and_hash(
                record["phone"], True
            )
            # Adds the hashed phone number identifier to the UserData object's
            # list.
            user_data.user_identifiers.append(user_identifier)

        # Checks if the record has all the required mailing address elements,
        # and if so, adds a UserIdentifier for the mailing address.
        if "first_name" in record:
            required_keys = ("last_name", "country_code", "postal_code")
            # Checks if the record contains all the other required elements of
            # a mailing address.
            if not all(key in record for key in required_keys):
                # Determines which required elements are missing from the
                # record.
                missing_keys = record.keys() - required_keys
                print(
                    "Skipping addition of mailing address information "
                    "because the following required keys are missing: "
                    f"{missing_keys}"
                )
            else:
                user_identifier: UserIdentifier = client.get_type(
                    "UserIdentifier"
                )
                address_info: AddressInfo = user_identifier.address_info
                address_info.hashed_first_name = normalize_and_hash(
                    record["first_name"], False
                )
                address_info.hashed_last_name = normalize_and_hash(
                    record["last_name"], False
                )
                address_info.country_code = record["country_code"]
                address_info.postal_code = record["postal_code"]
                user_data.user_identifiers.append(user_identifier)

        # If the user_identifiers repeated field is not empty, create a new
        # OfflineUserDataJobOperation and add the UserData to it.
        if user_data.user_identifiers:
            operation: OfflineUserDataJobOperation = client.get_type(
                "OfflineUserDataJobOperation"
            )
            operation.create = user_data
            operations.append(operation)
        # [END add_customer_match_user_list_2]

    return operations


# [START add_customer_match_user_list_4]
def check_job_status(
    client: GoogleAdsClient,
    customer_id: str,
    offline_user_data_job_resource_name: str,
) -> None:
    """Retrieves, checks, and prints the status of the offline user data job.

    If the job is completed successfully, information about the user list is
    printed. Otherwise, a GAQL query will be printed, which can be used to
    check the job status at a later date.

    Offline user data jobs may take 6 hours or more to complete, so checking the
    status periodically, instead of waiting, can be more efficient.

    Args:
        client: The Google Ads client.
        customer_id: The ID for the customer that owns the user list.
        offline_user_data_job_resource_name: The resource name of the offline
            user data job to get the status of.
    """
    query: str = f"""
        SELECT
          offline_user_data_job.resource_name,
          offline_user_data_job.id,
          offline_user_data_job.status,
          offline_user_data_job.type,
          offline_user_data_job.failure_reason,
          offline_user_data_job.customer_match_user_list_metadata.user_list
        FROM offline_user_data_job
        WHERE offline_user_data_job.resource_name =
          '{offline_user_data_job_resource_name}'
        LIMIT 1"""

    # Issues a search request using streaming.
    google_ads_service: GoogleAdsServiceClient = client.get_service(
        "GoogleAdsService"
    )
    results: SearchGoogleAdsStreamResponse = google_ads_service.search(
        customer_id=customer_id, query=query
    )
    offline_user_data_job_result: OfflineUserDataJob = next(
        iter(results)
    ).offline_user_data_job
    status_name: str = offline_user_data_job_result.status.name
    user_list_resource_name: str = (
        offline_user_data_job_result.customer_match_user_list_metadata.user_list
    )

    print(
        f"Offline user data job ID '{offline_user_data_job_result.id}' with type "
        f"'{offline_user_data_job_result.type_.name}' has status: {status_name}"
    )

    if status_name == "SUCCESS":
        print_customer_match_user_list_info(
            client, customer_id, user_list_resource_name
        )
    elif status_name == "FAILED":
        print(
            f"\tFailure Reason: {offline_user_data_job_result.failure_reason}"
        )
    elif status_name in ("PENDING", "RUNNING"):
        print(
            "To check the status of the job periodically, use the following "
            f"GAQL query with GoogleAdsService.Search: {query}"
        )
    # [END add_customer_match_user_list_4]


def print_customer_match_user_list_info(
    client: GoogleAdsClient, customer_id: str, user_list_resource_name: str
) -> None:
    """Prints information about the Customer Match user list.

    Args:
        client: The Google Ads client.
        customer_id: The ID for the customer that owns the user list.
        user_list_resource_name: The resource name of the user list to which to
            add users.
    """
    # [START add_customer_match_user_list_5]
    googleads_service_client: GoogleAdsServiceClient = client.get_service(
        "GoogleAdsService"
    )

    # Creates a query that retrieves the user list.
    query: str = f"""
        SELECT
          user_list.size_for_display,
          user_list.size_for_search
        FROM user_list
        WHERE user_list.resource_name = '{user_list_resource_name}'"""

    # Issues a search request.
    search_results: SearchGoogleAdsStreamResponse = (
        googleads_service_client.search(customer_id=customer_id, query=query)
    )
    # [END add_customer_match_user_list_5]

    # Prints out some information about the user list.
    user_list: UserList = next(iter(search_results)).user_list
    print(
        "The estimated number of users that the user list "
        f"'{user_list.resource_name}' has is "
        f"{user_list.size_for_display} for Display and "
        f"{user_list.size_for_search} for Search."
    )
    print(
        "Reminder: It may take several hours for the user list to be "
        "populated. Estimates of size zero are possible."
    )


def normalize_and_hash(s: str, remove_all_whitespace: bool) -> str:
    """Normalizes and hashes a string with SHA-256.

    Args:
        s: The string to perform this operation on.
        remove_all_whitespace: If true, removes leading, trailing, and
            intermediate spaces from the string before hashing. If false, only
            removes leading and trailing spaces from the string before hashing.

    Returns:
        A normalized (lowercase, remove whitespace) and SHA-256 hashed string.
    """
    # Normalizes by first converting all characters to lowercase, then trimming
    # spaces.
    if remove_all_whitespace:
        # Removes leading, trailing, and intermediate whitespace.
        s = "".join(s.split())
    else:
        # Removes only leading and trailing spaces.
        s = s.strip().lower()

    # Hashes the normalized string using the hashing algorithm.
    return hashlib.sha256(s.encode()).hexdigest()


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client: GoogleAdsClient = GoogleAdsClient.load_from_storage(
        version="v22"
    )

    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Adds a customer match user list for specified customer."
    )
    # The following argument(s) should be provided to run the example.
    parser.add_argument(
        "-c",
        "--customer_id",
        type=str,
        required=True,
        help="The ID for the customer that owns the user list.",
    )
    parser.add_argument(
        "-r",
        "--run_job",
        type=bool,
        required=True,
        help=(
            "If true, runs the OfflineUserDataJob after adding operations. "
            "The default value is False."
        ),
    )
    parser.add_argument(
        "-u",
        "--user_list_id",
        type=str,
        required=False,
        help=(
            "The ID of an existing user list. If not specified, this example "
            "will create a new user list."
        ),
    )
    parser.add_argument(
        "-j",
        "--offline_user_data_job_id",
        type=str,
        required=False,
        help=(
            "The ID of an existing OfflineUserDataJob in the PENDING state. If "
            "not specified, this example will create a new job."
        ),
    )
    parser.add_argument(
        "-d",
        "--ad_user_data_consent",
        type=str,
        choices=[
            e.name
            for e in googleads_client.enums.ConsentStatusEnum
            if e.name not in ("UNSPECIFIED", "UNKNOWN")
        ],
        help=(
            "The data consent status for ad user data for all members in "
            "the job."
        ),
    )
    parser.add_argument(
        "-p",
        "--ad_personalization_consent",
        type=str,
        choices=[
            e.name
            for e in googleads_client.enums.ConsentStatusEnum
            if e.name not in ("UNSPECIFIED", "UNKNOWN")
        ],
        help=(
            "The personalization consent status for ad user data for all "
            "members in the job."
        ),
    )

    args: argparse.Namespace = parser.parse_args()

    try:
        main(
            googleads_client,
            args.customer_id,
            args.run_job,
            args.user_list_id,
            args.offline_user_data_job_id,
            args.ad_user_data_consent,
            args.ad_personalization_consent,
        )
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
