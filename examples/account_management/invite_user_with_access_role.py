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
"""This code example sends an invitation email to a user.

The invitation is to manage a customer account with a desired access role.
"""


import argparse
import sys

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.ads.googleads.v20.services.services.customer_user_access_invitation_service.client import (
    CustomerUserAccessInvitationServiceClient,
)
from google.ads.googleads.v20.services.types.customer_user_access_invitation_service import (
    CustomerUserAccessInvitationOperation,
    MutateCustomerUserAccessInvitationResponse,
)
from google.ads.googleads.v20.resources.types.customer_user_access_invitation import (
    CustomerUserAccessInvitation,
)

# AccessRoleEnum is part of google.ads.googleads.v19.enums.types.access_role
# but it's accessed via client.enums.AccessRoleEnum, so direct import for type hint might not be strictly needed for the parameter.
# The field invitation.access_role expects an int (the enum value).


def main(
    client: GoogleAdsClient,
    customer_id: str,
    email_address: str,
    access_role: str,
) -> None:
    """The main method that creates all necessary entities for the example.

    Args:
        client: An initialized GoogleAdsClient instance.
        customer_id: The client customer ID str.
        email_address: The email address for the user receiving the invitation.
        access_role: The desired access role for the invitee (e.g., "ADMIN", "STANDARD").
    """
    service: CustomerUserAccessInvitationServiceClient = client.get_service(
        "CustomerUserAccessInvitationService"
    )
    # [START invite_user_with_access_role]
    invitation_operation: CustomerUserAccessInvitationOperation = (
        client.get_type("CustomerUserAccessInvitationOperation")
    )
    invitation: CustomerUserAccessInvitation = invitation_operation.create
    invitation.email_address = email_address
    # The access_role field in the CustomerUserAccessInvitation message expects
    # an AccessRoleEnum value (which is an int).
    invitation.access_role = client.enums.AccessRoleEnum[access_role].value

    response: MutateCustomerUserAccessInvitationResponse = (
        service.mutate_customer_user_access_invitation(
            customer_id=customer_id, operation=invitation_operation
        )
    )
    print(
        "Customer user access invitation was sent for "
        f"customer ID: '{customer_id}', "
        f"email address {email_address}, and "
        f"access role {access_role}. The invitation resource name is: "
        f"{response.result.resource_name}"
    )
    # [END invite_user_with_access_role]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=(
            "Sends an invitation email to a user to manage a customer "
            "account with a desired access role."
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
    parser.add_argument(
        "-e",
        "--email_address",
        type=str,
        required=True,
        help="The email address of the user to send the invitation to.",
    )
    parser.add_argument(
        "-a",
        "--access_role",
        type=str,
        required=True,
        choices=[e.name for e in googleads_client.enums.AccessRoleEnum],
        help="The updated user access role.",
    )
    args = parser.parse_args()

    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v20")

    try:
        main(
            googleads_client,
            args.customer_id,
            args.email_address,
            args.access_role,
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
