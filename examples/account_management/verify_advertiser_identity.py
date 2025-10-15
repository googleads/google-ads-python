#!/usr/bin/env python
# Copyright 2024 Google LLC
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
"""Retrieves the status of the advertiser identity verification program.

If required and not already started, it also starts the verification process.
"""


import argparse
import sys
from typing import Optional

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.ads.googleads.v22.enums.types.identity_verification_program_status import (
    IdentityVerificationProgramStatusEnum,
)
from google.ads.googleads.v22.services.services.identity_verification_service.client import (
    IdentityVerificationServiceClient,
)
from google.ads.googleads.v22.services.types.identity_verification_service import (
    GetIdentityVerificationResponse,
    IdentityVerification,
    IdentityVerificationProgress,
)


def main(client: GoogleAdsClient, customer_id: str) -> None:
    """The main method that creates all necessary entities for the example.

    Args:
        client: An initialized GoogleAdsClient instance.
        customer_id: The client customer ID str.
    """
    # Retrieve the current advertiser identity verification status.
    identity_verification: Optional[IdentityVerification] = (
        get_identity_verification(client, customer_id)
    )

    if identity_verification:
        # Type for status is the enum itself, not int, as it's used for direct comparison.
        status: (
            IdentityVerificationProgramStatusEnum.IdentityVerificationProgramStatus
        ) = identity_verification.verification_progress.program_status
        status_enum = (
            client.enums.IdentityVerificationProgramStatusEnum
        )  # This is an EnumTypeWrapper

        if status == status_enum.UNSPECIFIED:
            # Starts an identity verification session.
            start_identity_verification(client, customer_id)
            # Call get_identity_verification again to retrieve the verification
            # progress after starting an identity verification session.
            # The result of this call isn't used here, but if it were, it'd be Optional[IdentityVerification]
            get_identity_verification(client, customer_id)
        elif status == status_enum.PENDING_USER_ACTION:
            # If there is an identity verification session in progress, there
            # is no need to start another one by calling
            # StartIdentityVerification.
            verification_progress: IdentityVerificationProgress = (
                identity_verification.verification_progress
            )
            print(
                "There is an advertiser identity verification session in "
                "progress. The URL for the verification process is: "
                f"{verification_progress.action_url} and it will expire at "
                f"{verification_progress.invitation_link_expiration_time}."
            )
        elif status == status == status_enum.PENDING_REVIEW:
            print("The verification is under review.")
        elif status == status == status_enum.SUCCESS:
            print("The verification completed successfully.")
        else:
            print("The verification has an unknown state.")
    else:
        # If get_identity_verification returned None, the account is not
        # enrolled in mandatory identity verification.
        print(
            f"Account {customer_id} is not required to perform advertiser "
            "identity verification. See "
            "https://support.google.com/adspolicy/answer/9703665 for details "
            "on how and when an account is required to undergo the advertiser "
            "identity verification program."
        )


# [START verify_advertiser_identity_1]
def get_identity_verification(
    client: GoogleAdsClient, customer_id: str
) -> Optional[IdentityVerification]:
    """Retrieves the status of the advertiser identity verification process.

    Args:
        client: An initialized GoogleAdsClient instance.
        customer_id: The client customer ID str.

    Returns:
        either an IdentityVerification instance, or None
    """
    service: IdentityVerificationServiceClient = client.get_service(
        "IdentityVerificationService"
    )
    response: GetIdentityVerificationResponse = (
        service.get_identity_verification(customer_id=customer_id)
    )

    # Check if the response contains any indentity verifications. If not, then
    # None will be returned.
    if response.identity_verification:
        identity_verification_data: IdentityVerification = (
            response.identity_verification[0]
        )
        deadline: str = (
            identity_verification_data.identity_verification_requirement.verification_completion_deadline_time
        )
        # progress is an enum member
        progress: (
            IdentityVerificationProgramStatusEnum.IdentityVerificationProgramStatus
        ) = identity_verification_data.verification_progress.program_status

        print(
            f"Account {customer_id} has a verification completion deadline "
            "of {deadline} and status {progress.name} for advertiser identity "  # Use .name for string representation of enum
            "verification."
        )

        return identity_verification_data
        # [END verify_advertiser_identity_1]
    return None  # Explicitly return None if no identity_verification found


# [START verify_advertiser_identity_2]
def start_identity_verification(
    client: GoogleAdsClient, customer_id: str
) -> None:
    """Starts the identity verification process.

    Args:
        client: An initialized GoogleAdsClient instance.
        customer_id: The client customer ID str.
    """
    service: IdentityVerificationServiceClient = client.get_service(
        "IdentityVerificationService"
    )
    # Sends a request to start the identity verification process.
    # The verification_program argument expects an IdentityVerificationProgramEnum value (int).
    service.start_identity_verification(
        customer_id=customer_id,
        verification_program=client.enums.IdentityVerificationProgramEnum.ADVERTISER_IDENTITY_VERIFICATION.value,
    )
    # [END verify_advertiser_identity_2]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=(
            "Retrieves the status of the advertiser identity verification "
            "program. If required and not already started, it also starts the "
            "verification process."
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
