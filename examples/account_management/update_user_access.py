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
"""Updates the access role of a user, given the email address.

This code example should be run as a user who is an Administrator on the Google
Ads account with the specified customer ID.

See https://support.google.com/google-ads/answer/9978556 to learn more about
account access levels.
"""

import argparse
import sys

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

from google.api_core import protobuf_helpers

_ACCESS_ROLES = ["ADMIN", "STANDARD", "READ_ONLY", "EMAIL_ONLY"]


def main(client, customer_id, email_address, access_role):
    """Runs the example.

    Args:
      client: The Google Ads client.
      customer_id: The customer ID.
      email_address: The email address of the user whose access role should
          be updated
      access_role: The updated access role.
    """

    user_id = _get_user_access(client, customer_id, email_address)

    if user_id:
        _modify_user_access(client, customer_id, user_id, access_role)


def _get_user_access(client, customer_id, email_address):
    """Gets the customer user access given an email address.

    Args:
      client: The Google Ads client.
      customer_id: The customer ID.
      email_address: The email address of the user whose access role should
          be updated.

    Returns:
      The user ID integer if a customer is found, otherwise None.
    """
    googleads_service = client.get_service("GoogleAdsService")

    # Creates a query that retrieves all customer user accesses.
    # Use the LIKE query for filtering to ignore the text case for email
    # address when searching for a match.
    query = f"""
        SELECT
          customer_user_access.user_id,
          customer_user_access.email_address,
          customer_user_access.access_role,
          customer_user_access.access_creation_date_time
        FROM customer_user_access
        WHERE customer_user_access.email_address LIKE '{email_address}'"""

    search_request = client.get_type("SearchGoogleAdsRequest")
    search_request.customer_id = customer_id
    search_request.query = query

    response = googleads_service.search(request=search_request)

    try:
        user_access = next(iter(response)).customer_user_access
        print(
            "Customer user access with "
            f"User ID = '{user_access.user_id}', "
            f"Access Role = '{user_access.access_role}', and "
            f"Creation Time = {user_access.access_creation_date_time} "
            f"was found in Customer ID: {customer_id}."
        )
        return user_access.user_id
    except StopIteration:
        # If a StopIteration exception is raised it indicates that the response
        # was empty, no results were found, and this method should return None.
        print("No customer user access with requested email was found.")
        return None


def _modify_user_access(client, customer_id, user_id, access_role):
    """Modifies the user access role to a specified value.

    Args:
      client: The Google Ads client.
      customer_id: The customer ID.
      user_id: ID of the user whose access role is being modified.
      access_role: The updated access role.
    """
    customer_user_access_service = client.get_service(
        "CustomerUserAccessService"
    )
    customer_user_access_op = client.get_type("CustomerUserAccessOperation")
    access_role_enum = client.get_type("AccessRoleEnum").AccessRole
    customer_user_access = customer_user_access_op.update
    customer_user_access.resource_name = customer_user_access_service.customer_user_access_path(
        customer_id, user_id
    )
    customer_user_access.access_role = getattr(access_role_enum, access_role)
    client.copy_from(
        customer_user_access_op.update_mask,
        protobuf_helpers.field_mask(None, customer_user_access._pb),
    )

    response = customer_user_access_service.mutate_customer_user_access(
        customer_id=customer_id, operation=customer_user_access_op
    )

    print(
        "Successfully modified customer user access with resource name: "
        f"{response.result.resource_name}."
    )


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v8")

    parser = argparse.ArgumentParser(
        description="This code example updates the access role of a user, "
        "given the email address."
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
        "-e",
        "--email_address",
        type=str,
        required=True,
        help="The email address of the user whose access role should be "
        "updated.",
    )
    parser.add_argument(
        "-a",
        "--access_role",
        type=str,
        required=True,
        help="The access role that the given email address should be set to.",
        choices=_ACCESS_ROLES,
    )
    args = parser.parse_args()
    try:
        main(
            googleads_client,
            args.customer_id,
            args.email_address,
            args.access_role,
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
