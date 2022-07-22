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
"""This example adds a hotel callout extension asset to a specific account."""


import argparse
import sys


from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


def main(client, customer_id, language_code):
    """The main method that creates all necessary entities for the example.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        language_code: the language of the hotel callout feed item text.
    """
    # Creates assets for the hotel callout extensions.
    asset_resource_names = _add_extension_assets(
        client, customer_id, language_code
    )

    # Adds the extensions at the account level, so these will serve in all
    # eligible campaigns.
    _link_asset_to_account(client, customer_id, asset_resource_names)


def _add_extension_assets(client, customer_id, language_code):
    """Creates new assets for the hotel callout.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        language_code: the language of the hotel callout feed item text.

    Returns:
        a list of asset resource names.
    """
    operations = []
    # Create a hotel callout asset operation for each of the below texts.
    for text in ["Activities", "Facilities"]:
        operation = client.get_type("AssetOperation")
        asset = operation.create
        asset.hotel_callout_asset.text = text
        asset.hotel_callout_asset.language_code = language_code
        operations.append(operation)

    asset_service = client.get_service("AssetService")
    # Issues the create request to create the assets.
    response = asset_service.mutate_assets(
        customer_id=customer_id, operations=operations
    )
    resource_names = [result.resource_name for result in response.results]

    # Prints information about the result.
    for resource_name in resource_names:
        print(
            "Created hotel callout asset with resource name "
            f"'{resource_name}'."
        )

    return resource_names


def _link_asset_to_account(client, customer_id, resource_names):
    """Links Asset at the Customer level to serve in all eligible campaigns.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        resource_names: a list of asset resource names.
    """
    # Creates a CustomerAsset link for each Asset resource name provided.
    operations = []
    for resource_name in resource_names:
        operation = client.get_type("CustomerAssetOperation")
        asset = operation.create
        asset.asset = resource_name
        asset.field_type = client.enums.AssetFieldTypeEnum.HOTEL_CALLOUT
        operations.append(operation)

    customer_asset_service = client.get_service("CustomerAssetService")
    response = customer_asset_service.mutate_customer_assets(
        customer_id=customer_id, operations=operations
    )

    for result in response.results:
        print(
            "Added an account extension with resource name "
            f"'{result.resource_name}'."
        )


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v11")

    parser = argparse.ArgumentParser(
        description="Adds a hotel callout extension asset to the given account."
    )
    # The following argument(s) should be provided to run the example.
    parser.add_argument(
        "-c",
        "--customer_id",
        type=str,
        required=True,
        help="The Google Ads customer ID",
    )
    parser.add_argument(
        "-l",
        "--language_code",
        type=str,
        required=True,
        help=(
            "The language of the text on the hotel callout feed item. For a "
            "list of supported languages see: "
            "https://developers.google.com/hotels/hotel-ads/api-reference/language-codes."
        ),
    )
    args = parser.parse_args()

    try:
        main(googleads_client, args.customer_id, args.language_code)
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
