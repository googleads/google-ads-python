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
"""This example uploads offline conversion data for store sales transactions.

This feature is only available to allowlisted accounts.
See https://support.google.com/google-ads/answer/7620302 for more details.
"""

import argparse
from datetime import datetime
import hashlib
import sys

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


def main(
    client,
    customer_id,
    conversion_action_id,
    offline_user_data_job_type,
    external_id,
    advertiser_upload_date_time,
    bridge_map_version_id,
    partner_id,
    custom_key,
    custom_value,
    item_id,
    merchant_center_account_id,
    country_code,
    language_code,
    quantity,
):
    """Uploads offline conversion data for store sales transactions.

    Args:
        client: An initialized Google Ads client.
        customer_id: The Google Ads customer ID.
        conversion_action_id: The ID of a store sales conversion action.
        offline_user_data_job_type: Optional type of offline user data in the
            job (first party or third party). If you have an official store
            sales partnership with Google, use STORE_SALES_UPLOAD_THIRD_PARTY.
            Otherwise, use STORE_SALES_UPLOAD_FIRST_PARTY.
        external_id: Optional, but recommended, external ID for the offline
            user data job.
        advertiser_upload_date_time: Optional date and time the advertiser
            uploaded data to the partner. Only required for third party uploads.
            The format is 'yyyy-mm-dd hh:mm:ss+|-hh:mm', e.g.
            '2019-01-01 12:32:45-08:00'.
        bridge_map_version_id: Optional version of partner IDs to be used for
            uploads. Only required for third party uploads.
        partner_id: Optional ID of the third party partner. Only required for
            third party uploads.
        custom_key: A custom key str to segment store sales conversions. Only
            required after creating a custom key and custom values in the
            account.
        custom_value: A custom value str to segment store sales conversions.
            Only required after creating a custom key and custom values in the
            account.
        item_id: Optional str ID of the product. Either the Merchant Center Item
            ID or the Global Trade Item Number (GTIN). Only required if
            uploading with item attributes.
        merchant_center_account_id: Optional Merchant Center Account ID. Only
            required if uploading with item attributes.
        country_code: Optional two-letter country code of the location associated
            with the feed where your items are uploaded. Only required if
            uploading with item attributes.
        language_code: Optional two-letter country code of the language
            associated with the feed where your items are uploaded. Only
            required if uploading with item attributes.
        quantity: Optional number of items sold. Only required if uploading with
            item attributes.
    """
    # Get the OfflineUserDataJobService and OperationService clients.
    offline_user_data_job_service = client.get_service(
        "OfflineUserDataJobService"
    )

    # Create an offline user data job for uploading transactions.
    offline_user_data_job_resource_name = _create_offline_user_data_job(
        client,
        offline_user_data_job_service,
        customer_id,
        offline_user_data_job_type,
        external_id,
        advertiser_upload_date_time,
        bridge_map_version_id,
        partner_id,
        custom_key,
    )

    # Add transactions to the job.
    _add_transactions_to_offline_user_data_job(
        client,
        offline_user_data_job_service,
        customer_id,
        offline_user_data_job_resource_name,
        conversion_action_id,
        custom_value,
    )

    # Issue an asynchronous request to run the offline user data job.
    offline_user_data_job_service.run_offline_user_data_job(
        resource_name=offline_user_data_job_resource_name
    )

    # Offline user data jobs may take up to 24 hours to complete, so
    # instead of waiting for the job to complete, retrieves and displays
    # the job status once and then prints the query to use to check the job
    # again later.
    _check_job_status(client, customer_id, offline_user_data_job_resource_name)


def _create_offline_user_data_job(
    client,
    offline_user_data_job_service,
    customer_id,
    offline_user_data_job_type,
    external_id,
    advertiser_upload_date_time,
    bridge_map_version_id,
    partner_id,
    custom_key,
):
    """Creates an offline user data job for uploading store sales transactions.

    Args:
        client: An initialized Google Ads API client.
        offline_user_data_job_service: The offline user data job service client.
        customer_id: The Google Ads customer ID.
        offline_user_data_job_type: Optional type of offline user data in the
            job (first party or third party).
        external_id: Optional external ID for the offline user data job.
        advertiser_upload_date_time: Optional date and time the advertiser
            uploaded data to the partner. Only required for third party uploads.
        bridge_map_version_id: Optional version of partner IDs to be used for
            uploads. Only required for third party uploads.
        partner_id: Optional ID of the third party partner. Only required for
            third party uploads.
        custom_key: A custom key str to segment store sales conversions. Only
            required after creating a custom key and custom values in the
            account.

    Returns:
        The string resource name of the created job.
    """
    # TIP: If you are migrating from the AdWords API, please note that Google
    # Ads API uses the term "fraction" instead of "rate". For example,
    # loyalty_rate in the AdWords API is called loyalty_fraction in the Google
    # Ads API.

    # Create a new offline user data job.
    offline_user_data_job = client.get_type("OfflineUserDataJob")
    offline_user_data_job.type_ = offline_user_data_job_type
    if external_id is not None:
        offline_user_data_job.external_id = external_id

    # Please refer to https://support.google.com/google-ads/answer/7506124 for
    # additional details.
    store_sales_metadata = offline_user_data_job.store_sales_metadata
    # Set the fraction of your overall sales that you (or the advertiser,
    # in the third party case) can associate with a customer (email, phone
    # number, address, etc.) in your database or loyalty program.
    # For example, set this to 0.7 if you have 100 transactions over 30
    # days, and out of those 100 transactions, you can identify 70 by an
    # email address or phone number.
    store_sales_metadata.loyalty_fraction = 0.7
    # Set the fraction of sales you're uploading out of the overall sales
    # that you (or the advertiser, in the third party case) can associate
    # with a customer. In most cases, you will set this to 1.0.
    # Continuing the example above for loyalty fraction, a value of 1.0 here
    # indicates that you are uploading all 70 of the transactions that can
    # be identified by an email address or phone number.
    store_sales_metadata.transaction_upload_fraction = 1.0

    if custom_key:
        store_sales_metadata.custom_key = custom_key

    if (
        offline_user_data_job_type
        == client.get_type(
            "OfflineUserDataJobTypeEnum"
        ).OfflineUserDataJobType.STORE_SALES_UPLOAD_THIRD_PARTY
    ):
        # Create additional metadata required for uploading third party data.
        store_sales_third_party_metadata = (
            store_sales_metadata.third_party_metadata
        )
        # The date/time must be in the format "yyyy-MM-dd hh:mm:ss".
        store_sales_third_party_metadata.advertiser_upload_date_time = (
            advertiser_upload_date_time
        )
        # Set the fraction of transactions you received from the advertiser
        # that have valid formatting and values. This captures any transactions
        # the advertiser provided to you but which you are unable to upload to
        # Google due to formatting errors or missing data.
        # In most cases, you will set this to 1.0.
        store_sales_third_party_metadata.valid_transaction_fraction = 1.0
        # Set the fraction of valid transactions (as defined above) you
        # received from the advertiser that you (the third party) have matched
        # to an external user ID on your side.
        # In most cases, you will set this to 1.0.
        store_sales_third_party_metadata.partner_match_fraction = 1.0
        # Set the fraction of transactions you (the third party) are uploading
        # out of the transactions you received from the advertiser that meet
        # both of the following criteria:
        # 1. Are valid in terms of formatting and values. See valid transaction
        # fraction above.
        # 2. You matched to an external user ID on your side. See partner match
        # fraction above.
        # In most cases, you will set this to 1.0.
        store_sales_third_party_metadata.partner_upload_fraction = 1.0
        # Set the version of partner IDs to be used for uploads.
        # Please speak with your Google representative to get the values to use
        # for the bridge map version and partner IDs.
        store_sales_third_party_metadata.bridge_map_version_id = (
            bridge_map_version_id
        )
        # Set the third party partner ID uploading the transactions.
        store_sales_third_party_metadata.partner_id = partner_id

    create_offline_user_data_job_response = offline_user_data_job_service.create_offline_user_data_job(
        customer_id=customer_id, job=offline_user_data_job
    )
    offline_user_data_job_resource_name = (
        create_offline_user_data_job_response.resource_name
    )
    print(
        "Created an offline user data job with resource name "
        f"'{offline_user_data_job_resource_name}'."
    )
    return offline_user_data_job_resource_name


def _add_transactions_to_offline_user_data_job(
    client,
    offline_user_data_job_service,
    customer_id,
    offline_user_data_job_resource_name,
    conversion_action_id,
    custom_value,
    item_id,
    merchant_center_account_id,
    country_code,
    language_code,
    quantity,
):
    """Add operations to the job for a set of sample transactions.

    Args:
        client: An initialized Google Ads API client.
        offline_user_data_job_service: The offline user data job service client.
        customer_id: The Google Ads customer ID.
        offline_user_data_job_resource_name: The string resource name of the
            offline user data job that will receive the transactions.
        conversion_action_id: The ID of a store sales conversion action.
        custom_value: A custom value str to segment store sales conversions.
            Only required after creating a custom key and custom values in the
            account.
        item_id: Optional str ID of the product. Either the Merchant Center Item
            ID or the Global Trade Item Number (GTIN). Only required if
            uploading with item attributes.
        merchant_center_account_id: Optional Merchant Center Account ID. Only
            required if uploading with item attributes.
        country_code: Optional two-letter country code of the location associated
            with the feed where your items are uploaded. Only required if
            uploading with item attributes.
        language_code: Optional two-letter country code of the language
            associated with the feed where your items are uploaded. Only
            required if uploading with item attributes.
        quantity: Optional number of items sold. Only required if uploading with
            item attributes.
    """
    # Construct some sample transactions.
    operations = _build_offline_user_data_job_operations(
        client,
        customer_id,
        conversion_action_id,
        item_id,
        merchant_center_account_id,
        country_code,
        language_code,
        quantity,
    )

    # Issue a request to add the operations to the offline user data job.
    request = client.get_type("AddOfflineUserDataJobOperationsRequest")
    request.resource_name = offline_user_data_job_resource_name
    request.enable_partial_failure = True
    request.operations = operations
    response = offline_user_data_job_service.add_offline_user_data_job_operations(
        request=request,
    )

    # Print the status message if any partial failure error is returned.
    # Note: The details of each partial failure error are not printed here, you
    # can refer to the example handle_partial_failure.py to learn more.
    num_partial_failures = len(response.partial_failure_error.details)
    if response.partial_failure_error:
        print(
            f"{num_partial_failures} partial failure error(s) occurred: "
            f"{response.partial_failure_error.message}."
        )

    print(
        f"{len(operations) - num_partial_failures} operations were "
        "successfully added to the offline user data job."
    )


def _build_offline_user_data_job_operations(
    client,
    customer_id,
    conversion_action_id,
    custom_value,
    item_id,
    merchant_center_account_id,
    country_code,
    language_code,
    quantity,
):
    """Create offline user data job operations for sample transactions.

    Args:
        client: An initialized Google Ads API client.
        customer_id: The Google Ads customer ID.
        conversion_action_id: The ID of a store sales conversion action.
        custom_value: A custom value str to segment store sales conversions.
            Only required after creating a custom key and custom values in the
            account.
        item_id: Optional str ID of the product. Either the Merchant Center Item
            ID or the Global Trade Item Number (GTIN). Only required if
            uploading with item attributes.
        merchant_center_account_id: Optional Merchant Center Account ID. Only
            required if uploading with item attributes.
        country_code: Optional two-letter country code of the location associated
            with the feed where your items are uploaded. Only required if
            uploading with item attributes.
        language_code: Optional two-letter country code of the language
            associated with the feed where your items are uploaded. Only
            required if uploading with item attributes.
        quantity: Optional number of items sold. Only required if uploading with
            item attributes.

    Returns:
        A list of OfflineUserDataJobOperations.
    """
    # Create the first transaction for upload with an email address and state.
    user_data_with_email_address_operation = client.get_type(
        "OfflineUserDataJobOperation"
    )
    user_data_with_email_address = user_data_with_email_address_operation.create
    email_identifier = client.get_type("UserIdentifier")
    # Hash normalized email addresses based on SHA-256 hashing algorithm.
    email_identifier.hashed_email = _normalize_and_hash("customer@example.com")
    state_identifier = client.get_type("UserIdentifier")
    state_identifier.address_info.state = "NY"
    user_data_with_email_address.user_identifiers.extend(
        [email_identifier, state_identifier]
    )
    user_data_with_email_address.transaction_attribute.conversion_action = client.get_service(
        "ConversionActionService"
    ).conversion_action_path(
        customer_id, conversion_action_id
    )
    user_data_with_email_address.transaction_attribute.currency_code = "USD"
    # Convert the transaction amount from $200 USD to micros.
    user_data_with_email_address.transaction_attribute.transaction_amount_micros = (
        200000000
    )
    # Specify the date and time of the transaction. The format is
    # "YYYY-MM-DD HH:MM:SS[+HH:MM]", where [+HH:MM] is an optional timezone
    # offset from UTC. If the offset is absent, the API will use the account's
    # timezone as default. Examples: "2018-03-05 09:15:00" or
    # "2018-02-01 14:34:30+03:00".
    user_data_with_email_address.transaction_attribute.transaction_date_time = (
        datetime.now() - datetime.timedelta(months=1)
    ).strftime("%Y-%m-%d %H:%M:%S")

    # Create the second transaction for upload based on a physical address.
    user_data_with_physical_address_operation = client.get_type(
        "OfflineUserDataJobOperation"
    )
    user_data_with_physical_address = (
        user_data_with_physical_address_operation.create
    )
    address_identifier = client.get_type("UserIdentifier")
    # First and last name must be normalized and hashed.
    address_identifier.address_info.hashed_first_name = _normalize_and_hash(
        "John"
    )
    address_identifier.address_info.hashed_last_name = _normalize_and_hash(
        "Doe"
    )
    # Country and zip codes are sent in plain text.
    address_identifier.address_info.country_code = "US"
    address_identifier.address_info.postal_code = "10011"
    user_data_with_physical_address.user_identifiers.append(address_identifier)
    user_data_with_physical_address.transaction_attribute.conversion_action = client.get_service(
        "ConversionActionService"
    ).conversion_action_path(
        customer_id, conversion_action_id
    )
    user_data_with_physical_address.transaction_attribute.currency_code = "EUR"
    # Convert the transaction amount from 450 EUR to micros.
    user_data_with_physical_address.transaction_attribute.transaction_amount_micros = (
        450000000
    )
    # Specify the date and time of the transaction. This date and time
    # will be interpreted by the API using the Google Ads customer's
    # time zone. The date/time must be in the format
    # "yyyy-MM-dd hh:mm:ss".
    user_data_with_physical_address.transaction_attribute.transaction_date_time = (
        datetime.now() - datetime.timedelta(days=1)
    ).strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    if custom_value:
        user_data_with_email_address.transaction_attribute.custom_value = (
            custom_value
        )
        user_data_with_physical_address.transaction_attribute.custom_value = (
            custom_value
        )

    # Optional: If uploading data with item attributes, also assign these
    # values in the transaction attribute
    if item_id:
        item_attribute = (
            user_data_with_physical_address.transaction_attribute.item_attribute
        )
        item_attribute.item_id = item_id
        item_attribute.merchant_id = merchant_center_account_id
        item_attribute.country_code = country_code
        item_attribute.language_code = language_code
        item_attribute.quantity = quantity

    return [
        user_data_with_email_address_operation,
        user_data_with_physical_address_operation,
    ]


def _normalize_and_hash(s):
    """Normalizes and hashes a string with SHA-256.

    Args:
        s: The string to perform this operation on.

    Returns:
        A normalized (lowercase, remove whitespace) and SHA-256 hashed string.
    """
    return hashlib.sha256(s.strip().lower().encode()).hexdigest()


def _check_job_status(client, customer_id, offline_user_data_job_resource_name):
    """Retrieves, checks, and prints the status of the offline user data job.

    Args:
        client: An initialized Google Ads API client.
        customer_id: The Google Ads customer ID.
        offline_user_data_job_resource_name: The resource name of the job whose
            status you wish to check.
    """
    # Get the GoogleAdsService client.
    googleads_service = client.get_service("GoogleAdsService")

    # Construct a query to fetch the job status.
    query = f"""
        SELECT
          offline_user_data_job.resource_name,
          offline_user_data_job.id,
          offline_user_data_job.status,
          offline_user_data_job.type,
          offline_user_data_job.failure_reason
        FROM offline_user_data_job
        WHERE offline_user_data_job.resource_name =
          '{offline_user_data_job_resource_name}'"""

    # Issue the query and get the GoogleAdsRow containing the job.
    googleads_row = next(
        iter(googleads_service.search(customer_id=customer_id, query=query))
    )
    offline_user_data_job = googleads_row.offline_user_data_job

    offline_user_data_job_type_enum = client.get_type(
        "OfflineUserDataJobTypeEnum"
    ).OfflineUserDataJobType.OfflineUserDataJobType
    offline_user_data_job_status_enum = client.get_type(
        "OfflineUserDataJobStatusEnum"
    ).OfflineUserDataJobStatus.OfflineUserDataJobStatus

    job_status = offline_user_data_job.status
    print(
        f"Offline user data job ID {offline_user_data_job.id} with type "
        f"'{offline_user_data_job_type_enum.Name(offline_user_data_job.type)}' "
        f"has status {offline_user_data_job_status_enum.Name(job_status)}."
    )

    offline_user_data_job_status_enum = client.get_type(
        "OfflineUserDataJobStatusEnum"
    ).OfflineUserDataJobStatus
    if job_status == offline_user_data_job_status_enum.FAILED:
        print(f"\tFailure reason: {offline_user_data_job.failure_reason}")
    elif (
        job_status == offline_user_data_job_status_enum.PENDING
        or job_status == offline_user_data_job_status_enum.RUNNING
    ):
        print(
            "\nTo check the status of the job periodically, use the "
            f"following GAQL query with GoogleAdsService.Search:\n{query}\n"
        )
    elif job_status == offline_user_data_job_status_enum.SUCCESS:
        print("\nThe requested job has completed successfully.")
    else:
        raise ValueError("Requested job has UNKNOWN or UNSPECIFIED status.")


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v8")

    parser = argparse.ArgumentParser(
        description="This example uploads offline data for store sales "
        "transactions."
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
        type=int,
        required=True,
        help="The ID of a store sales conversion action.",
    )
    parser.add_argument(
        "-k",
        "--custom_key",
        type=str,
        required=False,
        help="Only required after creating a custom key and custom values in "
        "the account. Custom key and values are used to segment store sales "
        "conversions. This measurement can be used to provide more advanced "
        "insights. If provided, a custom value must also be provided",
    )
    parser.add_argument(
        "-v",
        "--custom_value",
        type=str,
        required=False,
        help="Only required after creating a custom key and custom values in "
        "the account. Custom key and values are used to segment store sales "
        "conversions. This measurement can be used to provide more advanced "
        "insights. If provided, a custom key must also be provided",
    )
    parser.add_argument(
        "-o",
        "--offline_user_data_job_type",
        type=int,
        required=False,
        default=googleads_client.get_type(
            "OfflineUserDataJobTypeEnum"
        ).OfflineUserDataJobType.STORE_SALES_UPLOAD_FIRST_PARTY,
        help="Optional type of offline user data in the job (first party or "
        "third party). If you have an official store sales partnership with "
        "Google, use STORE_SALES_UPLOAD_THIRD_PARTY. Otherwise, defaults to "
        "STORE_SALES_UPLOAD_FIRST_PARTY.",
    )
    parser.add_argument(
        "-e",
        "--external_id",
        type=int,
        required=False,
        default=None,
        help="Optional, but recommended, external ID for the offline user data "
        "job.",
    )
    parser.add_argument(
        "-d",
        "--advertiser_upload_date_time",
        type=str,
        required=False,
        default=None,
        help="Optional date and time the advertiser uploaded data to the "
        "partner. Only required for third party uploads. The format is "
        "'yyyy-mm-dd hh:mm:ss+|-hh:mm', e.g. '2021-01-01 12:32:45-08:00'.",
    )
    parser.add_argument(
        "-b",
        "--bridge_map_version_id",
        type=str,
        required=False,
        default=None,
        help="Optional version of partner IDs to be used for uploads. Only "
        "required for third party uploads.",
    )
    parser.add_argument(
        "-p",
        "--partner_id",
        type=int,
        required=False,
        default=None,
        help="Optional ID of the third party partner. Only required for third "
        "party uploads.",
    )
    parser.add_argument(
        "-i",
        "--item_id",
        type=str,
        required=False,
        default=None,
        help="Optional ID of the product. Either the Merchant Center Item ID "
        "or the Global Trade Item Number (GTIN). Only required if uploading "
        "with item attributes.",
    )
    parser.add_argument(
        "-m",
        "--merchant_center_account_id",
        type=int,
        required=False,
        default=None,
        help="Optional Merchant Center Account ID. Only required if uploading "
        "with item attributes.",
    )
    parser.add_argument(
        "-r",
        "--country_code",
        type=str,
        required=False,
        default=None,
        help="Optional two-letter country code of the location associated with "
        "the feed where your items are uploaded. Only required if uploading "
        "with item attributes.",
    )
    parser.add_argument(
        "-l",
        "--language_code",
        type=str,
        required=False,
        default=None,
        help="Optional two-letter language code of the language associated "
        "with the feed where your items are uploaded. Only required if "
        "uploading with item attributes.",
    )
    parser.add_argument(
        "-q",
        "--quantity",
        type=int,
        required=False,
        default=1,
        help="Optional number of items sold. Only required if uploading with "
        "item attributes.",
    )
    args = parser.parse_args()

    # Additional check to make sure that custom_key and custom_value are either
    # not provided or both provided together.
    required_together = ("custom_key", "custom_value")
    required_custom_vals = [
        getattr(args, field, None) for field in required_together
    ]
    if any(required_custom_vals) and not all(required_custom_vals):
        parser.error(
            "--custom_key (-k) and --custom_value (-v) must be passed "
            "in together"
        )

    try:
        main(
            googleads_client,
            args.customer_id,
            args.conversion_action_id,
            args.offline_user_data_job_type,
            args.external_id,
            args.advertiser_upload_date_time,
            args.bridge_map_version_id,
            args.partner_id,
            args.custom_key,
            args.custom_value,
            args.item_id,
            args.merchant_center_account_id,
            args.country_code,
            args.language_code,
            args.quantity,
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
