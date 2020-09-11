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

from google.ads.google_ads.client import GoogleAdsClient
from google.ads.google_ads.errors import GoogleAdsException


def main(client, customer_id):
    """Uses Customer Match to create and add users to a new user list.

    Args:
        client: The Google Ads client.
        customer_id: The customer ID for which to add the user list.
    """
    try:
        user_list_resource_name = _create_customer_match_user_list(
            client, customer_id
        )
        _add_users_to_customer_match_user_list(
            client, customer_id, user_list_resource_name
        )
        _print_customer_match_user_list_info(
            client, customer_id, user_list_resource_name
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


def _create_customer_match_user_list(client, customer_id):
    """Creates a Customer Match user list.

    Args:
        client: The Google Ads client.
        customer_id: The customer ID for which to add the user list.

    Returns:
        The string resource name of the newly created user list.
    """
    # Creates the UserListService client.
    user_list_service_client = client.get_service(
        "UserListService", version="v5"
    )

    # Creates the user list operation.
    user_list_operation = client.get_type("UserListOperation", version="v5")

    # Creates the new user list.
    user_list = user_list_operation.create
    user_list.name.value = f"Customer Match list #{uuid.uuid4()}"
    user_list.description.value = (
        "A list of customers that originated from email and physical addresses"
    )
    user_list.crm_based_user_list.upload_key_type = client.get_type(
        "CustomerMatchUploadKeyTypeEnum", version="v5"
    ).CONTACT_INFO
    # Customer Match user lists can set an unlimited membership life span;
    # to do so, use the special life span value 10000. Otherwise, membership
    # life span must be between 0 and 540 days inclusive. See:
    # https://developers.devsite.corp.google.com/google-ads/api/reference/rpc/latest/UserList#membership_life_span
    # Sets the membership life span to 30 days.
    user_list.membership_life_span.value = 30

    response = user_list_service_client.mutate_user_lists(
        customer_id, operations=[user_list_operation]
    )
    user_list_resource_name = response.results[0].resource_name
    print(
        f"User list with resource name '{user_list_resource_name}' was created."
    )

    return user_list_resource_name


def _add_users_to_customer_match_user_list(
    client, customer_id, user_list_resource_name
):
    """Uses Customer Match to create and add users to a new user list.

    Args:
        client: The Google Ads client.
        customer_id: The customer ID for which to add the user list.
        user_list_resource_name: The resource name of the user list to which to
            add users.
    """
    # Creates the OfflineUserDataJobService client.
    offline_user_data_job_service_client = client.get_service(
        "OfflineUserDataJobService", version="v5"
    )

    # Creates a new offline user data job.
    offline_user_data_job = client.get_type("OfflineUserDataJob", version="v5")
    offline_user_data_job.type = client.get_type(
        "OfflineUserDataJobTypeEnum", version="v5"
    ).CUSTOMER_MATCH_USER_LIST
    offline_user_data_job.customer_match_user_list_metadata.user_list.value = (
        user_list_resource_name
    )

    # Issues a request to create an offline user data job.
    create_offline_user_data_job_response = offline_user_data_job_service_client.create_offline_user_data_job(
        customer_id, offline_user_data_job
    )
    offline_user_data_job_resource_name = (
        create_offline_user_data_job_response.resource_name
    )
    print(
        "Created an offline user data job with resource name: "
        f"'{offline_user_data_job_resource_name}'."
    )

    true_value = client.get_type("BoolValue", version="v5")
    true_value.value = True

    # Issues a request to add the operations to the offline user data job.
    response = (
        offline_user_data_job_service_client.add_offline_user_data_job_operations(
            resource_name=offline_user_data_job_resource_name,
            operations=_build_offline_user_data_job_operations(client),
            enable_partial_failure=true_value,
        )
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
            failure_message = client.get_type("GoogleAdsFailure", version="v5")
            failure_object = failure_message.FromString(error_detail.value)

            for error in failure_object.errors:
                print(
                    "A partial failure at index {} occurred.\n"
                    "Error message: {}\nError code: {}".format(
                        error.location.field_path_elements[0].index.value,
                        error.message,
                        error.error_code,
                    )
                )

    print("The operations are added to the offline user data job.")

    # Issues an request to run the offline user data job for executing all
    # added operations.
    operation_response = offline_user_data_job_service_client.run_offline_user_data_job(
        offline_user_data_job_resource_name
    )

    # Wait until the operation has finished.
    print("Request to execute the added operations started.")
    print("Waiting until operation completes...")
    operation_response.result()

    print(
        "Offline user data job with resource name "
        f"'{offline_user_data_job_resource_name}' has finished."
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
        "OfflineUserDataJobOperation", version="v5"
    )
    user_data_with_email_address = user_data_with_email_address_operation.create
    user_identifier_with_hashed_email = client.get_type(
        "UserIdentifier", version="v5"
    )
    # Hash normalized email addresses based on SHA-256 hashing algorithm.
    user_identifier_with_hashed_email.hashed_email.value = _normalize_and_hash(
        "customer@example.com"
    )
    user_data_with_email_address.user_identifiers.append(
        user_identifier_with_hashed_email
    )

    # Creates a second user data based on a physical address.
    user_data_with_physical_address_operation = client.get_type(
        "OfflineUserDataJobOperation", version="v5"
    )
    user_data_with_physical_address = (
        user_data_with_physical_address_operation.create
    )
    user_identifier_with_address = client.get_type(
        "UserIdentifier", version="v5"
    )
    # First and last name must be normalized and hashed.
    user_identifier_with_address.address_info.hashed_first_name.value = _normalize_and_hash(
        "John"
    )
    user_identifier_with_address.address_info.hashed_last_name.value = _normalize_and_hash(
        "Doe"
    )
    # Country and zip codes are sent in plain text.
    user_identifier_with_address.address_info.country_code.value = "US"
    user_identifier_with_address.address_info.postal_code.value = "10011"
    user_data_with_physical_address.user_identifiers.append(
        user_identifier_with_address
    )

    return [
        user_data_with_email_address_operation,
        user_data_with_physical_address_operation,
    ]


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
    google_ads_service_client = client.get_service(
        "GoogleAdsService", version="v5"
    )

    # Creates a query that retrieves the user list.
    query = f"""
        SELECT user_list.size_for_display, user_list.size_for_search
        FROM user_list
        WHERE user_list.resource_name = '{user_list_resource_name}'"""

    # Issues a search request.
    search_results = google_ads_service_client.search(customer_id, query)

    # Prints out some information about the user list.
    user_list = next(iter(search_results)).user_list
    print(
        "The estimated number of users that the user list "
        f"'{user_list.resource_name}' has is "
        f"{user_list.size_for_display.value} for Display and "
        f"{user_list.size_for_search.value} for Search."
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


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    google_ads_client = GoogleAdsClient.load_from_storage()

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
    args = parser.parse_args()

    main(google_ads_client, args.customer_id)
