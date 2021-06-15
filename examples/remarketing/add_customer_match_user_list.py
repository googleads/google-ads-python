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
"""Uses Customer Match to create and add users to a new user (audience) list.

Note: It may take up to several hours for the list to be populated with users.
Email addresses must be associated with a Google account.
For privacy purposes, the user list size will show as zero until the list has
at least 1,000 users. After that, the size will be rounded to the two most
significant digits.
"""

import argparse
import hashlib
import sys
import uuid

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


def main(client, customer_id, skip_polling):
    """Uses Customer Match to create and add users to a new user list.

    Args:
        client: The Google Ads client.
        customer_id: The customer ID for which to add the user list.
        skip_polling: A bool dictating whether to poll the API for completion.
    """
    user_list_resource_name = _create_customer_match_user_list(
        client, customer_id
    )
    _add_users_to_customer_match_user_list(
        client, customer_id, user_list_resource_name, skip_polling
    )


def _create_customer_match_user_list(client, customer_id):
    """Creates a Customer Match user list.

    Args:
        client: The Google Ads client.
        customer_id: The customer ID for which to add the user list.

    Returns:
        The string resource name of the newly created user list.
    """
    # Creates the UserListService client.
    user_list_service_client = client.get_service("UserListService")

    # Creates the user list operation.
    user_list_operation = client.get_type("UserListOperation")

    # Creates the new user list.
    user_list = user_list_operation.create
    user_list.name = f"Customer Match list #{uuid.uuid4()}"
    user_list.description = (
        "A list of customers that originated from email and physical addresses"
    )
    user_list.crm_based_user_list.upload_key_type = client.get_type(
        "CustomerMatchUploadKeyTypeEnum"
    ).CustomerMatchUploadKeyType.CONTACT_INFO
    # Customer Match user lists can set an unlimited membership life span;
    # to do so, use the special life span value 10000. Otherwise, membership
    # life span must be between 0 and 540 days inclusive. See:
    # https://developers.devsite.corp.google.com/google-ads/api/reference/rpc/latest/UserList#membership_life_span
    # Sets the membership life span to 30 days.
    user_list.membership_life_span = 30

    response = user_list_service_client.mutate_user_lists(
        customer_id=customer_id, operations=[user_list_operation]
    )
    user_list_resource_name = response.results[0].resource_name
    print(
        f"User list with resource name '{user_list_resource_name}' was created."
    )

    return user_list_resource_name


# [START add_customer_match_user_list]
def _add_users_to_customer_match_user_list(
    client, customer_id, user_list_resource_name, skip_polling
):
    """Uses Customer Match to create and add users to a new user list.

    Args:
        client: The Google Ads client.
        customer_id: The customer ID for which to add the user list.
        user_list_resource_name: The resource name of the user list to which to
            add users.
        skip_polling: A bool dictating whether to poll the API for completion.
    """
    # Creates the OfflineUserDataJobService client.
    offline_user_data_job_service_client = client.get_service(
        "OfflineUserDataJobService"
    )

    # Creates a new offline user data job.
    offline_user_data_job = client.get_type("OfflineUserDataJob")
    offline_user_data_job.type_ = client.get_type(
        "OfflineUserDataJobTypeEnum"
    ).OfflineUserDataJobType.CUSTOMER_MATCH_USER_LIST
    offline_user_data_job.customer_match_user_list_metadata.user_list = (
        user_list_resource_name
    )

    # Issues a request to create an offline user data job.
    create_offline_user_data_job_response = offline_user_data_job_service_client.create_offline_user_data_job(
        customer_id=customer_id, job=offline_user_data_job
    )
    offline_user_data_job_resource_name = (
        create_offline_user_data_job_response.resource_name
    )
    print(
        "Created an offline user data job with resource name: "
        f"'{offline_user_data_job_resource_name}'."
    )

    request = client.get_type("AddOfflineUserDataJobOperationsRequest")
    request.resource_name = offline_user_data_job_resource_name
    request.operations = _build_offline_user_data_job_operations(client)
    request.enable_partial_failure = True

    # Issues a request to add the operations to the offline user data job.
    response = offline_user_data_job_service_client.add_offline_user_data_job_operations(
        request=request
    )

    # Prints the status message if any partial failure error is returned.
    # Note: the details of each partial failure error are not printed here.
    # Refer to the error_handling/handle_partial_failure.py example to learn
    # more.
    # Extracts the partial failure from the response status.
    partial_failure = getattr(response, "partial_failure_error", None)
    if getattr(partial_failure, "code", None) != 0:
        error_details = getattr(partial_failure, "details", [])
        for error_detail in error_details:
            failure_message = client.get_type("GoogleAdsFailure")
            # Retrieve the class definition of the GoogleAdsFailure instance
            # in order to use the "deserialize" class method to parse the
            # error_detail string into a protobuf message object.
            failure_object = type(failure_message).deserialize(error_detail)

            for error in failure_object.errors:
                print(
                    "A partial failure at index "
                    f"{error.location.field_path_elements[0].index} occurred.\n"
                    f"Error message: {error.message}\n"
                    f"Error code: {error.error_code}"
                )

    print("The operations are added to the offline user data job.")

    # Issues an request to run the offline user data job for executing all
    # added operations.
    operation_response = offline_user_data_job_service_client.run_offline_user_data_job(
        resource_name=offline_user_data_job_resource_name
    )

    if skip_polling:
        _check_job_status(
            client,
            customer_id,
            offline_user_data_job_resource_name,
            user_list_resource_name,
        )
    else:
        # Wait until the operation has finished.
        print("Request to execute the added operations started.")
        print("Waiting until operation completes...")
        operation_response.result()
        _print_customer_match_user_list_info(
            client, customer_id, user_list_resource_name
        )


def _build_offline_user_data_job_operations(client):
    """Builds and returns two sample offline user data job operations.

    Args:
        client: The Google Ads client.

    Returns:
        A list containing the operations.
    """
    # Creates a first user data based on an email address.
    user_data_with_email_address_operation = client.get_type(
        "OfflineUserDataJobOperation"
    )
    user_data_with_email_address = user_data_with_email_address_operation.create
    user_identifier_with_hashed_email = client.get_type("UserIdentifier")
    # Hash normalized email addresses based on SHA-256 hashing algorithm.
    user_identifier_with_hashed_email.hashed_email = _normalize_and_hash(
        "customer@example.com"
    )
    user_data_with_email_address.user_identifiers.append(
        user_identifier_with_hashed_email
    )

    # Creates a second user data based on a physical address.
    user_data_with_physical_address_operation = client.get_type(
        "OfflineUserDataJobOperation"
    )
    user_data_with_physical_address = (
        user_data_with_physical_address_operation.create
    )
    user_identifier_with_address = client.get_type("UserIdentifier")
    # First and last name must be normalized and hashed.
    user_identifier_with_address.address_info.hashed_first_name = _normalize_and_hash(
        "John"
    )
    user_identifier_with_address.address_info.hashed_last_name = _normalize_and_hash(
        "Doe"
    )
    # Country and zip codes are sent in plain text.
    user_identifier_with_address.address_info.country_code = "US"
    user_identifier_with_address.address_info.postal_code = "10011"
    user_data_with_physical_address.user_identifiers.append(
        user_identifier_with_address
    )

    return [
        user_data_with_email_address_operation,
        user_data_with_physical_address_operation,
    ]


def _check_job_status(
    client,
    customer_id,
    offline_user_data_job_resource_name,
    user_list_resource_name,
):
    """Retrieves, checks, and prints the status of the offline user data job.

    Args:
        client: The Google Ads client.
        customer_id: The customer ID for which to add the user list.
        offline_user_data_job_resource_name: The resource name of the offline
            user data job to get the status of.
        user_list_resource_name: The resource name of the customer match user
            list
    """
    query = f"""
        SELECT
          offline_user_data_job.resource_name,
          offline_user_data_job.id,
          offline_user_data_job.status,
          offline_user_data_job.type,
          offline_user_data_job.failure_reason
        FROM offline_user_data_job
        WHERE offline_user_data_job.resource_name =
          '{offline_user_data_job_resource_name}'
        LIMIT 1"""

    # Issues a search request using streaming.
    google_ads_service = client.get_service("GoogleAdsService")
    results = google_ads_service.search(customer_id=customer_id, query=query)
    offline_user_data_job = next(iter(results)).offline_user_data_job
    status_name = offline_user_data_job.status.name

    print(
        f"Offline user data job ID '{offline_user_data_job.id}' with type "
        f"'{offline_user_data_job.type_.name}' has status: {status_name}"
    )

    if status_name == "SUCCESS":
        _print_customer_match_user_list_info(
            client, customer_id, user_list_resource_name
        )
    elif status_name == "FAILED":
        print(f"\tFailure Reason: {offline_user_data_job.failure_reason}")
    elif status_name in ("PENDING", "RUNNING"):
        print(
            "To check the status of the job periodically, use the following "
            f"GAQL query with GoogleAdsService.Search: {query}"
        )


def _print_customer_match_user_list_info(
    client, customer_id, user_list_resource_name
):
    """Prints information about the Customer Match user list.

    Args:
        client: The Google Ads client.
        customer_id: The customer ID for which to add the user list.
        user_list_resource_name: The resource name of the user list to which to
            add users.
    """
    googleads_service_client = client.get_service("GoogleAdsService")

    # Creates a query that retrieves the user list.
    query = f"""
        SELECT
          user_list.size_for_display,
          user_list.size_for_search
        FROM user_list
        WHERE user_list.resource_name = '{user_list_resource_name}'"""

    # Issues a search request.
    search_results = googleads_service_client.search(
        customer_id=customer_id, query=query
    )

    # Prints out some information about the user list.
    user_list = next(iter(search_results)).user_list
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


def _normalize_and_hash(s):
    """Normalizes and hashes a string with SHA-256.

    Args:
        s: The string to perform this operation on.

    Returns:
        A normalized (lowercase, remove whitespace) and SHA-256 hashed string.
    """
    return hashlib.sha256(s.strip().lower().encode()).hexdigest()
    # [END add_customer_match_user_list]


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v8")

    parser = argparse.ArgumentParser(
        description="Adds a customer match user list for specified customer."
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
        "-s",
        "--skip_polling",
        action="store_true",
        help="Whether the example should skip polling the API for completion, "
        "which can take several hours. If the '-s' flag is set the example "
        "will demonstrate how to use a search query to check the status of "
        "the uploaded user list.",
    )

    args = parser.parse_args()

    try:
        main(googleads_client, args.customer_id, args.skip_polling)
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
