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
"""Enhances a web conversion by uploading a ConversionAdjustment.

The conversion adjustment contains hashed user identifiers and an order ID.
"""


import argparse
import hashlib
import re
import sys

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


def main(
    client,
    customer_id,
    conversion_action_id,
    order_id,
    conversion_date_time,
    user_agent,
):
    """The main method that creates all necessary entities for the example.

    Args:
        client: An initialized GoogleAdsClient instance.
        customer_id: The client customer ID string.
        conversion_action_id: The ID of the conversion action to upload to.
        order_id: The unique ID (transaction ID) of the conversion.
        conversion_date_time: The date and time of the conversion.
        user_agent: The HTTP user agent of the conversion.
    """
    # [START add_user_identifiers]
    # Extracts user email, phone, and address info from the raw data, normalizes
    # and hashes it, then wraps it in UserIdentifier objects. Creates a separate
    # UserIdentifier object for each. The data in this example is hardcoded, but
    # in your application you might read the raw data from an input file.

    # IMPORTANT: Since the identifier attribute of UserIdentifier
    # (https://developers.google.com/google-ads/api/reference/rpc/latest/UserIdentifier)
    # is a oneof
    # (https://protobuf.dev/programming-guides/proto3/#oneof-features), you must
    # set only ONE of hashed_email, hashed_phone_number, mobile_id,
    # third_party_user_id, or address_info. Setting more than one of these
    # attributes on the same UserIdentifier will clear all the other members of
    # the oneof. For example, the following code is INCORRECT and will result in
    # a UserIdentifier with ONLY a hashed_phone_number:
    #
    # incorrectly_populated_user_identifier = client.get_type("UserIdentifier")
    # incorrectly_populated_user_identifier.hashed_email = "...""
    # incorrectly_populated_user_identifier.hashed_phone_number = "...""

    raw_record = {
        # Email address that includes a period (.) before the Gmail domain.
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
        # This example lets you input conversion details as arguments, but in
        # reality you might store this data alongside other user data, so we
        # include it in this sample user record.
        "order_id": order_id,
        "conversion_action_id": conversion_action_id,
        "conversion_date_time": conversion_date_time,
        "currency_code": "USD",
        "user_agent": user_agent,
    }

    # Constructs the enhancement adjustment.
    conversion_adjustment = client.get_type("ConversionAdjustment")
    conversion_adjustment.adjustment_type = (
        client.enums.ConversionAdjustmentTypeEnum.ENHANCEMENT
    )

    # Creates a user identifier using the hashed email address, using the
    # normalize and hash method specifically for email addresses.
    email_identifier = client.get_type("UserIdentifier")
    # Optional: Specifies the user identifier source.
    email_identifier.user_identifier_source = (
        client.enums.UserIdentifierSourceEnum.FIRST_PARTY
    )
    # Uses the normalize and hash method specifically for email addresses.
    email_identifier.hashed_email = normalize_and_hash_email_address(
        raw_record["email"]
    )
    # Adds the email identifier to the conversion adjustment.
    conversion_adjustment.user_identifiers.append(email_identifier)

    # Checks if the record has a phone number, and if so, adds a UserIdentifier
    # for it.
    if raw_record.get("phone") is not None:
        phone_identifier = client.get_type("UserIdentifier")
        phone_identifier.hashed_phone_number = normalize_and_hash(
            raw_record["phone"]
        )
        # Adds the phone identifier to the conversion adjustment.
        conversion_adjustment.user_identifiers.append(phone_identifier)

    # Checks if the record has all the required mailing address elements, and if
    # so, adds a UserIdentifier for the mailing address.
    if raw_record.get("first_name") is not None:
        # Checks if the record contains all the other required elements of a
        # mailing address.
        required_keys = ["last_name", "country_code", "postal_code"]
        # Builds a new list of the required keys that are missing from
        # raw_record.
        missing_keys = [
            key for key in required_keys if key not in raw_record.keys()
        ]
        if len(missing_keys) > 0:
            print(
                "Skipping addition of mailing address information because the"
                f"following required keys are missing: {missing_keys}"
            )
        else:
            # Creates a user identifier using sample values for the user address,
            # hashing where required.
            address_identifier = client.get_type("UserIdentifier")
            address_info = address_identifier.address_info
            address_info.hashed_first_name = normalize_and_hash(
                raw_record["first_name"]
            )
            address_info.hashed_last_name = normalize_and_hash(
                raw_record["last_name"]
            )
            address_info.country_code = raw_record["country_code"]
            address_info.postal_code = raw_record["postal_code"]
            # Adds the address identifier to the conversion adjustment.
            conversion_adjustment.user_identifiers.append(address_identifier)
            # [END add_user_identifiers]

    # [START add_conversion_details]
    conversion_action_service = client.get_service("ConversionActionService")
    # Sets the conversion action.
    conversion_adjustment.conversion_action = (
        conversion_action_service.conversion_action_path(
            customer_id, raw_record["conversion_action_id"]
        )
    )

    # Sets the order ID. Enhancements MUST use order ID instead of GCLID
    # date/time pair.
    conversion_adjustment.order_id = order_id

    # Sets the conversion date and time if provided. Providing this value is
    # optional but recommended.
    if raw_record.get("conversion_date_time"):
        conversion_adjustment.gclid_date_time_pair.conversion_date_time = (
            raw_record["conversion_date_time"]
        )

    # Sets optional fields where a value was provided
    if raw_record.get("user_agent"):
        # Sets the user agent. This should match the user agent of the request
        # that sent the original conversion so the conversion and its
        # enhancement are either both attributed as same-device or both
        # attributed as cross-device.
        conversion_adjustment.user_agent = user_agent
        # [END add_conversion_details]

    # [START upload_enhancement]
    # Creates the conversion adjustment upload service client.
    conversion_adjustment_upload_service = client.get_service(
        "ConversionAdjustmentUploadService"
    )
    # Uploads the enhancement adjustment. Partial failure should always be set
    # to true.
    # NOTE: This request only uploads a single conversion, but if you have
    # multiple conversions to upload, it's still best to upload them in a single
    # request. See the following for per-request limits for reference:
    # https://developers.google.com/google-ads/api/docs/best-practices/quotas#conversion_upload_service
    response = conversion_adjustment_upload_service.upload_conversion_adjustments(
        customer_id=customer_id,
        conversion_adjustments=[conversion_adjustment],
        # Enables partial failure (must be true).
        partial_failure=True,
    )
    # [END upload_enhancement]

    # Prints any partial errors returned.
    # To review the overall health of your recent uploads, see:
    # https://developers.google.com/google-ads/api/docs/conversions/upload-summaries
    if response.partial_failure_error:
        print(
            "Partial error encountered: "
            f"{response.partial_failure_error.message}"
        )
    else:
        # Prints the result.
        result = response.results[0]
        print(
            f"Uploaded conversion adjustment of {result.conversion_action} for "
            f"order ID {result,order_id}."
        )


# [START normalize_and_hash]
def normalize_and_hash_email_address(email_address):
    """Returns the result of normalizing and hashing an email address.

    For this use case, Google Ads requires removal of any '.' characters
    preceding "gmail.com" or "googlemail.com"

    Args:
        email_address: An email address to normalize.

    Returns:
        A normalized (lowercase, removed whitespace) and SHA-265 hashed string.
    """
    normalized_email = email_address.strip().lower()
    email_parts = normalized_email.split("@")

    # Check that there are at least two segments
    if len(email_parts) > 1:
        # Checks whether the domain of the email address is either "gmail.com"
        # or "googlemail.com". If this regex does not match then this statement
        # will evaluate to None.
        if re.match(r"^(gmail|googlemail)\.com$", email_parts[1]):
            # Removes any '.' characters from the portion of the email address
            # before the domain if the domain is gmail.com or googlemail.com.
            email_parts[0] = email_parts[0].replace(".", "")
            normalized_email = "@".join(email_parts)

    return normalize_and_hash(normalized_email)


def normalize_and_hash(s):
    """Normalizes and hashes a string with SHA-256.

    Private customer data must be hashed during upload, as described at:
    https://support.google.com/google-ads/answer/9888656

    Args:
        s: The string to perform this operation on.

    Returns:
        A normalized (lowercase, removed whitespace) and SHA-256 hashed string.
    """
    return hashlib.sha256(s.strip().lower().encode()).hexdigest()
    # [END normalize_and_hash]


if __name__ == "__main__":
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
    args = parser.parse_args()

    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v22")

    try:
        main(
            googleads_client,
            args.customer_id,
            args.conversion_action_id,
            args.order_id,
            args.conversion_date_time,
            args.user_agent,
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
