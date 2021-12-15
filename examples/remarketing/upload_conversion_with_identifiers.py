#!/usr/bin/env python
# Copyright 2021 Google LLC
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
"""Uploads a conversion using hashed email address instead of GCLID."""


import argparse
import hashlib
import re
import sys

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


# [START upload_conversion_with_identifiers]
def main(
    client,
    customer_id,
    conversion_action_id,
    email_address,
    conversion_date_time,
    conversion_value,
    order_id,
):
    """The main method that creates all necessary entities for the example.

    Args:
        client: An initialized GoogleAdsClient instance.
        customer_id: The client customer ID string.
        conversion_action_id: The ID of the conversion action to upload to.
        email_address: The email address for the conversion.
        conversion_date_time: The date and time of the conversion.
        conversion_value: The value of the conversion.
        order_id: The unique ID (transaction ID) of the conversion.
    """
    # [START create_conversion]
    conversion_action_service = client.get_service("ConversionActionService")
    # Gets the conversion action resource name.
    conversion_action_resource_name = conversion_action_service.conversion_action_path(
        customer_id, conversion_action_id
    )
    click_conversion = client.get_type("ClickConversion")
    click_conversion.conversion_action = conversion_action_resource_name
    click_conversion.conversion_date_time = conversion_date_time
    click_conversion.conversion_value = conversion_value
    click_conversion.currency_code = "USD"

    # Sets the order ID if provided.
    if order_id:
        click_conversion.order_id = order_id

    # Creates a user identifier using the hashed email address, using the
    # normalize and hash method specifically for email addresses. If using a
    # phone number, use the "_normalize_and_hash" method instead.
    user_identifier = client.get_type("UserIdentifier")
    # Creates a SHA256 hashed string using the given email address, as
    # described at https://support.google.com/google-ads/answer/9888656.
    user_identifier.hashed_email = _normalize_and_hash_email_address(
        email_address
    )
    # Optional: Specifies the user identifier source.
    user_identifier.user_identifier_source = (
        client.enums.UserIdentifierSourceEnum.FIRST_PARTY
    )
    # Adds the user identifier to the conversion.
    click_conversion.user_identifiers.append(user_identifier)
    # [END create_conversion]

    # Creates the conversion upload service client.
    conversion_upload_service = client.get_service("ConversionUploadService")
    # Uploads the click conversion. Partial failure should always be set to
    # True.
    response = conversion_upload_service.upload_click_conversions(
        customer_id=customer_id,
        conversions=[click_conversion],
        # Enables partial failure (must be true).
        partial_failure=True,
    )

    # Prints any partial errors returned.
    if response.partial_failure_error:
        print(
            "Partial error encountered: "
            f"{response.partial_failure_error.message}"
        )

    # Prints the result.
    result = response.results[0]
    # Only prints valid results. If the click conversion failed then this
    # result will be returned as an empty message and will be falsy.
    if result:
        print(
            "Uploaded conversion that occurred at "
            f"{result.conversion_data_time} from Google Click ID "
            f"{result.gclid} to {result.conversion_action}."
        )
    # [END upload_conversion_with_identifiers]


# [START normalize_and_hash]
def _normalize_and_hash_email_address(email_address):
    """Returns the result of normalizing and hashing an email address.

    For this use case, Google Ads requires removal of any '.' characters
    preceding "gmail.com" or "googlemail.com"

    Args:
        email_address: An email address to normalize.

    Returns:
        A normalized (lowercase, removed whitespace) and SHA-265 hashed string.
    """
    normalized_email = email_address.lower()
    email_parts = normalized_email.split("@")
    # Checks whether the domain of the email address is either "gmail.com"
    # or "googlemail.com". If this regex does not match then this statement
    # will evaluate to None.
    is_gmail = re.match(r"^(gmail|googlemail)\.com$", email_parts[1])

    # Check that there are at least two segments and the second segment
    # matches the above regex expression validating the email domain name.
    if len(email_parts) > 1 and is_gmail:
        # Removes any '.' characters from the portion of the email address
        # before the domain if the domain is gmail.com or googlemail.com.
        email_parts[0] = email_parts[0].replace(".", "")
        normalized_email = "@".join(email_parts)

    return _normalize_and_hash(normalized_email)


def _normalize_and_hash(s):
    """Normalizes and hashes a string with SHA-256.

    Private customer data must be hashed during upload, as described at:
    https://support.google.com/google-ads/answer/7474263

    Args:
        s: The string to perform this operation on.

    Returns:
        A normalized (lowercase, removed whitespace) and SHA-256 hashed string.
    """
    return hashlib.sha256(s.strip().lower().encode()).hexdigest()
    # [END normalize_and_hash]


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v9")

    parser = argparse.ArgumentParser(
        description="Imports offline call conversion values for calls related "
        "to your ads."
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
        "--conversion_action_id",
        type=str,
        required=True,
        help="The ID of the conversion action to upload to.",
    )
    parser.add_argument(
        "-e",
        "--email_address",
        type=str,
        required=True,
        help="The email address for the conversion.",
    )
    parser.add_argument(
        "-d",
        "--conversion_date_time",
        type=str,
        required=True,
        help="The date time at which the conversion occurred. Must be after "
        "the click time, and must include the time zone offset.  The format is "
        "'yyyy-mm-dd hh:mm:ss+|-hh:mm', e.g. '2019-01-01 12:32:45-08:00'.",
    )
    parser.add_argument(
        "-v",
        "--conversion_value",
        type=float,
        required=True,
        help="The value of the conversion.",
    )
    parser.add_argument(
        "-o",
        "--order_id",
        type=str,
        help="the unique ID (transaction ID) of the conversion.",
    )
    args = parser.parse_args()

    try:
        main(
            googleads_client,
            args.customer_id,
            args.conversion_action_id,
            args.email_address,
            args.conversion_date_time,
            args.conversion_value,
            args.order_id,
        )
    except GoogleAdsException as ex:
        print(
            f"Request with ID '{ex.request_id}'' failed with status "
            f"'{ex.error.code().name}' and includes the following errors:"
        )
        for error in ex.failure.errors:
            print(f"\tError with message '{error.message}'.")
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print(f"\t\tOn field: {field_path_element.field_name}")
        sys.exit(1)
