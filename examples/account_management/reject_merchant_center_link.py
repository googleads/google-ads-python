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
"""Demonstrates how to reject or unlink a Merchant Center link request.

Prerequisite: You need to have access to a Merchant Center account. You can find
instructions to create a Merchant Center account here:
https://support.google.com/merchants/answer/188924.

To run this example, you must use the Merchant Center UI or the Content API for
Shopping to send a link request between your Merchant Center and Google Ads
accounts. You can find detailed instructions to link your Merchant Center and
Google Ads accounts here: https://support.google.com/merchants/answer/6159060.
"""

import argparse
import sys

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


def main(client, customer_id, merchant_center_account_id):
    """Demonstrates how to reject a Merchant Center link request.

    Args:
        client: An initialized Google Ads client.
        customer_id: The Google Ads customer ID.
        merchant_center_account_id: The Merchant Center account ID for the
            account requesting to link.
    """
    # Get the MerchantCenterLinkService client.
    merchant_center_link_service = client.get_service(
        "MerchantCenterLinkService"
    )
    # Get the extant customer account to Merchant Center account links.
    list_merchant_center_links_response = merchant_center_link_service.list_merchant_center_links(
        customer_id=customer_id
    )

    number_of_links = len(
        list_merchant_center_links_response.merchant_center_links
    )

    if number_of_links == 0:
        print(
            "There are no current merchant center links to Google Ads "
            f"account {customer_id}. This example will now exit."
        )
        return

    print(
        f"{number_of_links} Merchant Center link(s) found with the "
        "following details:"
    )

    for (
        merchant_center_link
    ) in list_merchant_center_links_response.merchant_center_links:
        print(
            f"\tLink '{merchant_center_link.resource_name}' has status "
            f"'{merchant_center_link.status.name}'."
        )

        # Check if this is the link to the target Merchant Center account.
        if merchant_center_link.id == merchant_center_account_id:
            # A Merchant Center link can be pending or enabled; in both
            # cases, we reject it by removing the link.
            _remove_merchant_center_link(
                client,
                merchant_center_link_service,
                customer_id,
                merchant_center_link,
            )

            # We can terminate early since this example concerns only one
            # Google Ads account to Merchant Center account link.
            return

    # Raise an exception if no matching Merchant Center link was found.
    raise ValueError(
        "No link could was found between Google Ads account "
        f"{customer_id} and Merchant Center account "
        f"{merchant_center_account_id}."
    )


# [START reject_merchant_center_link]
def _remove_merchant_center_link(
    client, merchant_center_link_service, customer_id, merchant_center_link
):
    """Removes a Merchant Center link from a Google Ads client customer account.

    Args:
        client: An initialized Google Ads client.
        merchant_center_link_service: An initialized
            MerchantCenterLinkService client.
        customer_id: The Google Ads customer ID of the account that has the link
            request.
        merchant_center_link: The MerchantCenterLink object to remove.
    """
    # Create a single remove operation, specifying the Merchant Center link
    # resource name.
    operation = client.get_type("MerchantCenterLinkOperation")
    operation.remove = merchant_center_link.resource_name

    # Send the operation in a mutate request.
    response = merchant_center_link_service.mutate_merchant_center_link(
        customer_id=customer_id, operation=operation
    )
    print(
        "Removed Merchant Center link with resource name "
        f"'{response.result.resource_name}'."
    )
    # [END reject_merchant_center_link]


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v8")

    parser = argparse.ArgumentParser(
        description=(
            "Demonstrates how to reject a Merchant Center link request."
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
        "-m",
        "--merchant_center_account_id",
        type=int,
        required=True,
        help="The Merchant Center account ID for the account requesting to "
        "link.",
    )
    args = parser.parse_args()

    try:
        main(
            googleads_client, args.customer_id, args.merchant_center_account_id
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
