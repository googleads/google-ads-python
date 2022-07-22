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


# [START upload_conversion_enhancement]
def main(
    client,
    customer_id,
    conversion_action_id,
    order_id,
    conversion_date_time,
    user_agent,
    restatement_value,
    currency_code,
):
    """The main method that creates all necessary entities for the example.

    Args:
        client: An initialized GoogleAdsClient instance.
        customer_id: The client customer ID string.
        conversion_action_id: The ID of the conversion action to upload to.
        order_id: The unique ID (transaction ID) of the conversion.
        conversion_date_time: The date and time of the conversion.
        user_agent: The HTTP user agent of the conversion.
        restatement_value: The enhancement value.
        currency_code: The currency of the enhancement value.
    """
    # [START create_adjustment]
    conversion_action_service = client.get_service("ConversionActionService")
    conversion_adjustment = client.get_type("ConversionAdjustment")
    conversion_adjustment.conversion_action = (
        conversion_action_service.conversion_action_path(
            customer_id, conversion_action_id
        )
    )
    conversion_adjustment.adjustment_type = (
        client.enums.ConversionAdjustmentTypeEnum.ENHANCEMENT
    )
    # Enhancements MUST use order ID instead of GCLID date/time pair.
    conversion_adjustment.order_id = order_id

    # Sets the conversion date and time if provided. Providing this value is
    # optional but recommended.
    if conversion_date_time:
        conversion_adjustment.gclid_date_time_pair.conversion_date_time = (
            conversion_date_time
        )

    # Creates a user identifier using sample values for the user address,
    # hashing where required.
    address_identifier = client.get_type("UserIdentifier")
    address_identifier.address_info.hashed_first_name = _normalize_and_hash(
        "Joanna"
    )
    address_identifier.address_info.hashed_last_name = _normalize_and_hash(
        "Joanna"
    )
    address_identifier.address_info.hashed_street_address = _normalize_and_hash(
        "1600 Amphitheatre Pkwy"
    )
    address_identifier.address_info.city = "Mountain View"
    address_identifier.address_info.state = "CA"
    address_identifier.address_info.postal_code = "94043"
    address_identifier.address_info.country_code = "US"
    # Optional: Specifies the user identifier source.
    address_identifier.user_identifier_source = (
        client.enums.UserIdentifierSourceEnum.FIRST_PARTY
    )

    # Creates a user identifier using the hashed email address.
    email_identifier = client.get_type("UserIdentifier")
    # Optional: Specifies the user identifier source.
    email_identifier.user_identifier_source = (
        client.enums.UserIdentifierSourceEnum.FIRST_PARTY
    )
    # Uses the normalize and hash method specifically for email addresses.
    email_identifier.hashed_email = _normalize_and_hash_email_address(
        "joannasmith@gmail.com"
    )

    # Adds both user identifiers to the conversion adjustment.
    conversion_adjustment.user_identifiers.extend(
        [address_identifier, email_identifier]
    )

    # Sets optional fields where a value was provided
    if user_agent:
        # Sets the user agent. This should match the user agent of the request
        # that sent the original conversion so the conversion and its
        # enhancement are either both attributed as same-device or both
        # attributed as cross-device.
        conversion_adjustment.user_agent = user_agent

    if restatement_value:
        # Sets the new value of the conversion.
        conversion_adjustment.restatement_value.adjusted_value = (
            restatement_value
        )
        if currency_code:
            # Sets the currency of the new value, if provided. Otherwise, the
            # default currency from the conversion action is used, and if that
            # is not set then the account currency is used.
            conversion_adjustment.restatement_value.currency_code = (
                currency_code
            )
    # [END create_conversion]

    # Creates the conversion adjustment upload service client.
    conversion_adjustment_upload_service = client.get_service(
        "ConversionAdjustmentUploadService"
    )
    # Uploads the enhancement adjustment. Partial failure should always be set
    # to true.
    response = conversion_adjustment_upload_service.upload_conversion_adjustments(
        customer_id=customer_id,
        conversion_adjustments=[conversion_adjustment],
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
            f"Uploaded conversion adjustment of {result.conversion_action} for "
            f"order ID {result,order_id}."
        )
        # [END upload_conversion_enhancement]


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
    googleads_client = GoogleAdsClient.load_from_storage(version="v11")

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
        "-o",
        "--order_id",
        type=str,
        required=True,
        help="the unique ID (transaction ID) of the conversion.",
    )
    parser.add_argument(
        "-d",
        "--conversion_date_time",
        type=str,
        help="The date time at which the conversion with the specified order "
        "ID occurred. Must be after the click time, and must include the time "
        "zone offset.  The format is 'yyyy-mm-dd hh:mm:ss+|-hh:mm', "
        "e.g. '2019-01-01 12:32:45-08:00'. Setting this field is optional, "
        "but recommended",
    )
    parser.add_argument(
        "-u",
        "--user_agent",
        type=str,
        help="The HTTP user agent of the conversion.",
    )
    parser.add_argument(
        "-v",
        "--restatement_value",
        type=float,
        help="The enhancement value.",
    )
    parser.add_argument(
        "-y",
        "--currency_code",
        type=str,
        required=True,
        help="The currency of the conversion value.",
    )
    args = parser.parse_args()

    try:
        main(
            googleads_client,
            args.customer_id,
            args.conversion_action_id,
            args.order_id,
            args.conversion_date_time,
            args.user_agent,
            args.restatement_value,
            args.currency_code,
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
