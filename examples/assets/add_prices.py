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
"""This example adds a price asset and associates it with an account."""


import argparse
from typing import Optional
import sys
from uuid import uuid4

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.ads.googleads.v22.services.types.asset_service import AssetOperation
from google.ads.googleads.v22.resources.types.asset import Asset
from google.ads.googleads.v22.common.types.asset_types import PriceAsset
from google.ads.googleads.v22.common.types.asset_types import PriceOffering
from google.ads.googleads.v22.enums.types.price_extension_price_unit import (
    PriceExtensionPriceUnitEnum,
)
from google.ads.googleads.v22.services.types.customer_asset_service import (
    CustomerAssetOperation,
)
from google.ads.googleads.v22.resources.types.customer_asset import (
    CustomerAsset,
)


def main(client: GoogleAdsClient, customer_id: str) -> None:
    """The main method that creates all necessary entities for the example.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
    """
    # Create a new price asset.
    price_asset_resource_name: str = create_price_asset(client, customer_id)

    # Add the new price asset to the account.
    add_asset_to_account(client, customer_id, price_asset_resource_name)


def create_price_asset(client: GoogleAdsClient, customer_id: str) -> str:
    """Creates a price asset and returns its resource name.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.

    Returns:
        a PriceAsset resource name.
    """
    # Create an asset operation.
    asset_operation: AssetOperation = client.get_type("AssetOperation")
    # Create an asset.
    asset: Asset = asset_operation.create
    asset.name = f"Price Asset #{uuid4()}"
    asset.tracking_url_template = "http://tracker.example.com/?u={lpurl}"

    # Create the price asset.
    price_asset: PriceAsset = asset.price_asset
    price_asset.type_ = client.enums.PriceExtensionTypeEnum.SERVICES
    # Price qualifier is optional.
    price_asset.price_qualifier = (
        client.enums.PriceExtensionPriceQualifierEnum.FROM
    )
    price_asset.language_code = "en"
    price_asset.price_offerings.extend(
        [
            create_price_offering(
                client,
                "Scrubs",
                "Body Scrub, Salt Scrub",
                "http://www.example.com/scrubs",
                "http://m.example.com/scrubs",
                60000000,  # 60 USD
                "USD",
                client.enums.PriceExtensionPriceUnitEnum.PER_HOUR,
            ),
            create_price_offering(
                client,
                "Hair Cuts",
                "Once a month",
                "http://www.example.com/haircuts",
                "http://m.example.com/haircuts",
                75000000,  # 75 USD
                "USD",
                client.enums.PriceExtensionPriceUnitEnum.PER_MONTH,
            ),
            create_price_offering(
                client,
                "Skin Care Package",
                "Four times a month",
                "http://www.example.com/skincarepackage",
                None,
                250000000,  # 250 USD
                "USD",
                client.enums.PriceExtensionPriceUnitEnum.PER_MONTH,
            ),
        ]
    )

    # Issue a mutate request to create the price asset.
    asset_service = client.get_service("AssetService")
    response = asset_service.mutate_assets(
        customer_id=customer_id, operations=[asset_operation]
    )
    resource_name: str = response.results[0].resource_name

    print(f"Created a price asset with resource name '{resource_name}'.")

    return resource_name


def create_price_offering(
    client: GoogleAdsClient,
    header: str,
    description: str,
    final_url: str,
    final_mobile_url: Optional[str],
    price_in_micros: int,
    currency_code: str,
    unit: PriceExtensionPriceUnitEnum.PriceExtensionPriceUnit,
) -> PriceOffering:
    """Creates a PriceOffering instance and returns it.

    Args:
        client: an initialized GoogleAdsClient instance.
        header: The header of the price offering.
        description: The description of the price offering.
        final_url: The final_url of the price offering.
        final_mobile_url: The final_mobile_url of the price offering.
        price_in_micros: The price of the price offering.
        currency_code: The currency_code of the price offering.
        unit: The price unit of the price offering.

    Returns:
        A PriceOffering instance.
    """
    price_offering: PriceOffering = client.get_type("PriceOffering")
    price_offering.header = header
    price_offering.description = description
    price_offering.final_url = final_url
    # Check if this exists, since we pass None for one of the PriceOfferings
    # in the _create_price_asset method and assigning None to this field
    # raises an error.
    if final_mobile_url:
        price_offering.final_mobile_url = final_mobile_url
    price_offering.price.amount_micros = price_in_micros
    price_offering.price.currency_code = currency_code
    price_offering.unit = unit
    return price_offering


def add_asset_to_account(
    client: GoogleAdsClient, customer_id: str, price_asset_resource_name: str
) -> None:
    """Adds a new Asset to the given user account.

    Adding the Asset to an account allows it to serve in all campaigns under
    that account.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        price_asset_resource_name: a resource name for an Asset containing
            a PriceAsset.
    """
    # Create a customer asset operation.
    customer_asset_operation: CustomerAssetOperation = client.get_type(
        "CustomerAssetOperation"
    )
    # Create a customer asset, set its type to PRICE and attach price asset.
    asset: CustomerAsset = customer_asset_operation.create
    asset.field_type = client.enums.AssetFieldTypeEnum.PRICE
    asset.asset = price_asset_resource_name

    # Issue a mutate request to create the customer asset.
    customer_asset_service = client.get_service("CustomerAssetService")
    response = customer_asset_service.mutate_customer_assets(
        customer_id=customer_id, operations=[customer_asset_operation]
    )
    resource_name: str = response.results[0].resource_name

    print(
        "Created customer asset with resource name "
        f"'{response.results[0].resource_name}'."
    )


if __name__ == "__main__":
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Add price asset for the specified customer id."
    )
    # The following argument(s) should be provided to run the example.
    parser.add_argument(
        "-c",
        "--customer_id",
        type=str,
        required=True,
        help="The Google Ads customer ID",
    )
    args: argparse.Namespace = parser.parse_args()

    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client: GoogleAdsClient = GoogleAdsClient.load_from_storage(
        version="v22"
    )

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
