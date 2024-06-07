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
"""Uploads an enhanced conversion for leads by uploading a ClickConversion.

The click conversion has hashed, first-party user-provided data from your
website lead forms. This includes user identifiers, and optionally, a click ID
and order ID. With this information, Google can tie the conversion to the ad
that drove the lead.
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
    conversion_date_time,
    conversion_value,
    order_id,
    gclid,
    ad_user_data_consent,
):
    """The main method that creates all necessary entities for the example.

    Args:
        client: An initialized GoogleAdsClient instance.
        customer_id: The client customer ID string.
        conversion_action_id: The ID of the conversion action to upload to.
        conversion_date_time: The date and time of the conversion.
        conversion_value: The value of the conversion.
        order_id: The unique ID (transaction ID) of the conversion.
        gclid: The Google click ID for the click.
        ad_user_data_consent: The consent status for ad user data for all
            members in the job.
    """
    # [START add_user_identifiers]
    # Extract user email and phone from the raw data, normalize and hash it,
    # then wrap it in UserIdentifier objects. Create a separate UserIdentifier
    # object for each. The data in this example is hardcoded, but in your
    # application you might read the raw data from an input file.

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
        # Phone number to be converted to E.164 format, with a leading '+' as
        # required.
        "phone": "+1 800 5550102",
        # This example lets you input conversion details as arguments,
        # but in reality you might store this data alongside other user data,
        # so we include it in this sample user record.
        "order_id": order_id,
        "gclid": gclid,
        "conversion_action_id": conversion_action_id,
        "conversion_date_time": conversion_date_time,
        "conversion_value": conversion_value,
        "currency_code": "USD",
        "ad_user_data_consent": ad_user_data_consent,
    }

    # Constructs the click conversion.
    click_conversion = client.get_type("ClickConversion")
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
    # Adds the user identifier to the conversion.
    click_conversion.user_identifiers.append(email_identifier)

    # Checks if the record has a phone number, and if so, adds a UserIdentifier
    # for it.
    if raw_record.get("phone") is not None:
        phone_identifier = client.get_type("UserIdentifier")
        phone_identifier.hashed_phone_number = normalize_and_hash(
            raw_record["phone"]
        )
        # Adds the phone identifier to the conversion adjustment.
        click_conversion.user_identifiers.append(phone_identifier)
        # [END add_user_identifiers]

    # [START add_conversion_details]
    # Add details of the conversion.
    # Gets the conversion action resource name.
    conversion_action_service = client.get_service("ConversionActionService")
    click_conversion.conversion_action = (
        conversion_action_service.conversion_action_path(
            customer_id, raw_record["conversion_action_id"]
        )
    )
    click_conversion.conversion_date_time = raw_record["conversion_date_time"]
    click_conversion.conversion_value = raw_record["conversion_value"]
    click_conversion.currency_code = raw_record["currency_code"]

    # Sets the order ID if provided.
    if raw_record.get("order_id"):
        click_conversion.order_id = raw_record["order_id"]

    # Sets the gclid if provided.
    if raw_record.get("gclid"):
        click_conversion.gclid = raw_record["gclid"]

    # Specifies whether user consent was obtained for the data you are
    # uploading. For more details, see:
    # https://www.google.com/about/company/user-consent-policy
    if raw_record["ad_user_data_consent"]:
        click_conversion.consent.ad_user_data = client.enums.ConsentStatusEnum[
            raw_record["ad_user_data_consent"]
        ]
        # [END add_conversion_details]

    # [START upload_conversion]
    # Creates the conversion upload service client.
    conversion_upload_service = client.get_service("ConversionUploadService")
    # Uploads the click conversion. Partial failure should always be set to
    # True.
    # NOTE: This request only uploads a single conversion, but if you have
    # multiple conversions to upload, it's most efficient to upload them in a
    # single request. See the following for per-request limits for reference:
    # https://developers.google.com/google-ads/api/docs/best-practices/quotas#conversion_upload_service
    response = conversion_upload_service.upload_click_conversions(
        customer_id=customer_id,
        conversions=[click_conversion],
        # Enables partial failure (must be true).
        partial_failure=True,
    )
    # [END upload_conversion]

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
            "Uploaded conversion that occurred at "
            f"{result.conversion_data_time} "
            f"to {result.conversion_action}."
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

    return normalize_and_hash(normalized_email)


def normalize_and_hash(s):
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
    parser.add_argument(
        "-g",
        "--gclid",
        type=str,
        help="the Google click ID (gclid) for the click.",
    )
    parser.add_argument(
        "-d",
        "--ad_user_data_consent",
        type=str,
        choices=[e.name for e in googleads_client.enums.ConsentStatusEnum],
        help=(
            "The data consent status for ad user data for all members in "
            "the job."
        ),
    )
    args = parser.parse_args()

    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v17")

    try:
        main(
            googleads_client,
            args.customer_id,
            args.conversion_action_id,
            args.conversion_date_time,
            args.conversion_value,
            args.order_id,
            args.gclid,
            args.ad_user_data_consent,
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
