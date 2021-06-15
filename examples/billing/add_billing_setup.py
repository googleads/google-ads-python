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
"""This example creates a billing setup for a customer.

A billing setup is a link between a payments account and a customer. The new
billing setup can either reuse an existing payments account, or create a new
payments account with a given payments profile. Billing setups are applicable
for clients on monthly invoicing only. See here for details about applying for
monthly invoicing: https://support.google.com/google-ads/answer/2375377.
In the case of consolidated billing, a payments account is linked to the
manager account and is linked to a customer account via a billing setup.
"""


import argparse
from datetime import datetime, timedelta
import sys
from uuid import uuid4

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


def main(
    client, customer_id, payments_account_id=None, payments_profile_id=None
):
    """The main method that creates all necessary entities for the example.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        payments_account_id: payments account ID to attach to the new billing
            setup. If provided it must be formatted as "1234-5678-9012-3456".
        payments_profile_id: payments profile ID to attach to a new payments
            account and to the new billing setup. If provided it must be
            formatted as "1234-5678-9012".
    """
    billing_setup = _create_billing_setup(
        client, customer_id, payments_account_id, payments_profile_id
    )
    _set_billing_setup_date_times(client, customer_id, billing_setup)
    billing_setup_operation = client.get_type("BillingSetupOperation")
    client.copy_from(billing_setup_operation.create, billing_setup)
    billing_setup_service = client.get_service("BillingSetupService")
    response = billing_setup_service.mutate_billing_setup(
        customer_id=customer_id, operation=billing_setup_operation
    )
    print(
        "Added new billing setup with resource name "
        f"{response.result.resource_name}"
    )


def _create_billing_setup(
    client, customer_id, payments_account_id=None, payments_profile_id=None
):
    """Creates and returns a new billing setup instance.

    The new billing setup will have its payment details populated. One of the
    payments_account_id or payments_profile_id must be provided.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        payments_account_id: payments account ID to attach to the new billing
            setup. If provided it must be formatted as "1234-5678-9012-3456".
        payments_profile_id: payments profile ID to attach to a new payments
            account and to the new billing setup. If provided it must be
            formatted as "1234-5678-9012".

    Returns:
        A newly created BillingSetup instance.
    """
    billing_setup = client.get_type("BillingSetup")

    # Sets the appropriate payments account field.
    if payments_account_id != None:
        # If a payments account ID has been provided, set the payments_account
        # field to the full resource name of the given payments account ID.
        # You can list available payments accounts via the
        # PaymentsAccountService's ListPaymentsAccounts method.
        billing_setup.payments_account = client.get_service(
            "BillingSetupService"
        ).payments_account_path(customer_id, payments_account_id)
    elif payments_profile_id != None:
        # Otherwise, create a new payments account by setting the
        # payments_account_info field
        # See https://support.google.com/google-ads/answer/7268503
        # for more information about payments profiles.
        billing_setup.payments_account_info.payments_account_name = (
            f"Payments Account #{uuid4()}"
        )
        billing_setup.payments_account_info.payments_profile_id = (
            payments_profile_id
        )

    return billing_setup


def _set_billing_setup_date_times(client, customer_id, billing_setup):
    """Sets the starting and ending date times for the new billing setup.

    Queries the customer's account to see if there are any approved billing
    setups. If there are any, the new billing setup starting date time is set to
    one day after the last. If not, the billing setup is set to start
    immediately. The ending date is set to one day after the starting date time.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        billing_setup: the billing setup whose starting and ending date times
            will be set.
    """
    # The query to search existing approved billing setups in the end date time
    # descending order. See get_billing_setup.py for a more detailed example of
    # how to retrieve billing setups.
    query = """
      SELECT
        billing_setup.end_date_time
      FROM billing_setup
      WHERE billing_setup.status = APPROVED
      ORDER BY billing_setup.end_date_time DESC
      LIMIT 1"""

    ga_service = client.get_service("GoogleAdsService")
    response = ga_service.search_stream(customer_id=customer_id, query=query)
    # Coercing the response iterator to a list causes the stream to be fully
    # consumed so that we can easily access the last row in the request.
    batches = list(response)
    # Checks if any results were included in the response.
    if batches:
        # Retrieves the ending_date_time of the last BillingSetup.
        last_batch = batches[0]
        last_row = last_batch.results[0]
        last_ending_date_time = last_row.billing_setup.end_date_time

        if not last_ending_date_time:
            # A null ending date time indicates that the current billing setup
            # is set to run indefinitely. Billing setups cannot overlap, so
            # throw an exception in this case.
            raise Exception(
                "Cannot set starting and ending date times for the new billing "
                "setup; the latest existing billing setup is set to run "
                "indefinitely."
            )

        try:
            # BillingSetup.end_date_time is a string that can be in the format
            # %Y-%m-%d or %Y-%m-%d %H:%M:%S. This checks for the first format.
            end_date_time_obj = datetime.strptime(
                last_ending_date_time, "%Y-%m-%d"
            )
        except ValueError:
            # If a ValueError is raised then the end_date_time string is in the
            # second format that includes hours, minutes and seconds.
            end_date_time_obj = datetime.strptime(
                last_ending_date_time, "%Y-%m-%d %H:%M:%S"
            )

        # Sets the new billing setup start date to one day after the end date.
        start_date = end_date_time_obj + timedelta(days=1)
    else:
        # If there are no BillingSetup objecst to retrieve, the only acceptable
        # start date time is today.
        start_date = datetime.now()

    billing_setup.start_date_time = start_date.strftime("%Y-%m-%d %H:%M:%S")
    billing_setup.end_date_time = (start_date + timedelta(days=1)).strftime(
        "%Y-%m-%d %H:%M:%S"
    )


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v8")

    parser = argparse.ArgumentParser(
        description=("Creates a billing setup for a given customer.")
    )
    # The following argument(s) should be provided to run the example.
    parser.add_argument(
        "-c",
        "--customer_id",
        type=str,
        required=True,
        help="The Google Ads customer ID.",
    )
    # Creates a mutually exclusive argument group to ensure that only one of the
    # following two arguments are given, otherwise it will raise an error.
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-a",
        "--payments_account_id",
        type=str,
        help="Either a payments account ID or a payments profile ID must be "
        "provided for the example to run successfully. "
        "See: https://developers.google.com/google-ads/api/docs/billing/billing-setups#creating_new_billing_setups. "
        "Provide an existing payments account ID to link to the new "
        "billing setup. Must be formatted as '1234-5678-9012-3456'.",
    )
    group.add_argument(
        "-p",
        "--payments_profile_id",
        type=str,
        help="Either a payments account ID or a payments profile ID must be "
        "provided for the example to run successfully. "
        "See: https://developers.google.com/google-ads/api/docs/billing/billing-setups#creating_new_billing_setups. "
        "Provide an existing payments profile ID to link to a new payments "
        "account and the new billing setup. Must be formatted as: "
        "'1234-5678-9012-3456'.",
    )
    args = parser.parse_args()

    try:
        main(
            googleads_client,
            args.customer_id,
            args.payments_account_id,
            args.payments_profile_id,
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
