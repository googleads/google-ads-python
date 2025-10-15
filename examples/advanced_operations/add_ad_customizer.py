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
"""This code example adds two ad customizer attributes.

It then associates them with the given ad group and adds an ad that uses the ad
customizer attributes to populate dynamic data.
"""


import argparse
import sys
from uuid import uuid4

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.ads.googleads.v22.common.types import AdTextAsset
from google.ads.googleads.v22.resources.types import (
    AdGroupAd,
    AdGroupCustomizer,
    CustomizerAttribute,
)
from google.ads.googleads.v22.services.services.ad_group_ad_service import (
    AdGroupAdServiceClient,
)
from google.ads.googleads.v22.services.services.ad_group_customizer_service import (
    AdGroupCustomizerServiceClient,
)
from google.ads.googleads.v22.services.services.customizer_attribute_service import (
    CustomizerAttributeServiceClient,
)
from google.ads.googleads.v22.services.services.google_ads_service import (
    GoogleAdsServiceClient,
)
from google.ads.googleads.v22.services.types import (
    AdGroupAdOperation,
    AdGroupCustomizerOperation,
    CustomizerAttributeOperation,
    MutateAdGroupAdsResponse,
    MutateAdGroupCustomizersResponse,
    MutateCustomizerAttributesResponse,
)


def main(client: GoogleAdsClient, customer_id: str, ad_group_id: str) -> None:
    """The main method that creates all necessary entities for the example.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        ad_group_id: an ad group ID.
    """
    text_customizer_name: str = f"Planet_{uuid4().hex[:8]}"
    price_customizer_name: str = f"Price_{uuid4().hex[:8]}"

    text_customizer_resource_name: str = create_text_customizer_attribute(
        client, customer_id, text_customizer_name
    )
    price_customizer_resource_name: str = create_price_customizer_attribute(
        client, customer_id, price_customizer_name
    )
    link_customizer_attributes(
        client,
        customer_id,
        ad_group_id,
        text_customizer_resource_name,
        price_customizer_resource_name,
    )
    create_ad_with_customizations(
        client,
        customer_id,
        ad_group_id,
        text_customizer_name,
        price_customizer_name,
    )


# [START add_ad_customizer]
def create_text_customizer_attribute(
    client: GoogleAdsClient, customer_id: str, customizer_name: str
) -> str:
    """Creates a text customizer attribute and returns its resource name.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        customizer_name: the name of the customizer to create.

    Returns:
        a resource name for a text customizer attribute.
    """
    customizer_attribute_service: CustomizerAttributeServiceClient = (
        client.get_service("CustomizerAttributeService")
    )

    # Creates a text customizer attribute. The customizer attribute name is
    # arbitrary and will be used as a placeholder in the ad text fields.
    operation: CustomizerAttributeOperation = client.get_type(
        "CustomizerAttributeOperation"
    )
    text_attribute: CustomizerAttribute = operation.create
    text_attribute.name = customizer_name
    text_attribute.type_ = client.enums.CustomizerAttributeTypeEnum.TEXT

    response: MutateCustomizerAttributesResponse = (
        customizer_attribute_service.mutate_customizer_attributes(
            customer_id=customer_id, operations=[operation]
        )
    )

    resource_name: str = response.results[0].resource_name
    print(
        f"Added text customizer attribute with resource name '{resource_name}'"
    )
    return resource_name
    # [END add_ad_customizer]


# [START add_ad_customizer_1]
def create_price_customizer_attribute(
    client: GoogleAdsClient, customer_id: str, customizer_name: str
) -> str:
    """Creates a price customizer attribute and returns its resource name.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        customizer_name: the name of the customizer to create.

    Returns:
        a resource name for a text customizer attribute.
    """
    customizer_attribute_service: CustomizerAttributeServiceClient = (
        client.get_service("CustomizerAttributeService")
    )

    # Creates a price customizer attribute. The customizer attribute name is
    # arbitrary and will be used as a placeholder in the ad text fields.
    operation: CustomizerAttributeOperation = client.get_type(
        "CustomizerAttributeOperation"
    )
    price_attribute: CustomizerAttribute = operation.create
    price_attribute.name = customizer_name
    price_attribute.type_ = client.enums.CustomizerAttributeTypeEnum.PRICE

    response: MutateCustomizerAttributesResponse = (
        customizer_attribute_service.mutate_customizer_attributes(
            customer_id=customer_id, operations=[operation]
        )
    )

    resource_name: str = response.results[0].resource_name
    print(
        f"Added price customizer attribute with resource name '{resource_name}'"
    )
    return resource_name
    # [END add_ad_customizer_1]


# [START add_ad_customizer_2]
def link_customizer_attributes(
    client: GoogleAdsClient,
    customer_id: str,
    ad_group_id: str,
    text_customizer_resource_name: str,
    price_customizer_resource_name: str,
) -> None:
    """Restricts the ad customizer attributes to work with a specific ad group.

    This prevents the customizer attributes from being used elsewhere and makes
    sure they are used only for customizing a specific ad group.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        ad_group_id: the ad group ID to bind the customizer attributes to.
        text_customizer_resource_name: the resource name of the text customizer attribute.
        price_customizer_resource_name: the resource name of the price customizer attribute.
    """
    googleads_service: GoogleAdsServiceClient = client.get_service(
        "GoogleAdsService"
    )
    ad_group_customizer_service: AdGroupCustomizerServiceClient = (
        client.get_service("AdGroupCustomizerService")
    )

    # Binds the text attribute customizer to a specific ad group to make sure
    # it will only be used to customize ads inside that ad group.
    mars_operation: AdGroupCustomizerOperation = client.get_type(
        "AdGroupCustomizerOperation"
    )
    mars_customizer: AdGroupCustomizer = mars_operation.create
    mars_customizer.customizer_attribute = text_customizer_resource_name
    mars_customizer.value.type_ = client.enums.CustomizerAttributeTypeEnum.TEXT
    mars_customizer.value.string_value = "Mars"
    mars_customizer.ad_group = googleads_service.ad_group_path(
        customer_id, ad_group_id
    )

    # Binds the price attribute customizer to a specific ad group to make sure
    # it will only be used to customize ads inside that ad group.
    price_operation: AdGroupCustomizerOperation = client.get_type(
        "AdGroupCustomizerOperation"
    )
    price_customizer: AdGroupCustomizer = price_operation.create
    price_customizer.customizer_attribute = price_customizer_resource_name
    price_customizer.value.type_ = (
        client.enums.CustomizerAttributeTypeEnum.PRICE
    )
    price_customizer.value.string_value = "100.0€"
    price_customizer.ad_group = googleads_service.ad_group_path(
        customer_id, ad_group_id
    )

    response: MutateAdGroupCustomizersResponse = (
        ad_group_customizer_service.mutate_ad_group_customizers(
            customer_id=customer_id,
            operations=[mars_operation, price_operation],
        )
    )

    for result in response.results:
        print(
            "Added an ad group customizer with resource name "
            f"'{result.resource_name}'"
        )
        # [END add_ad_customizer_2]


# [START add_ad_customizer_3]
def create_ad_with_customizations(
    client: GoogleAdsClient,
    customer_id: str,
    ad_group_id: str,
    text_customizer_name: str,
    price_customizer_name: str,
) -> None:
    """Creates a responsive search ad (RSA).

    The RSA uses the ad customizer attributes to populate the placeholders.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        ad_group_id: the ad group ID to bind the customizer attributes to.
        text_customizer_name: name of the text customizer.
        price_customizer_name: name of the price customizer.
    """
    googleads_service: GoogleAdsServiceClient = client.get_service(
        "GoogleAdsService"
    )
    ad_group_ad_service: AdGroupAdServiceClient = client.get_service(
        "AdGroupAdService"
    )

    # Creates a responsive search ad using the attribute customizer names as
    # placeholders and default values to be used in case there are no attribute
    # customizer values.
    operation: AdGroupAdOperation = client.get_type("AdGroupAdOperation")
    ad_group_ad: AdGroupAd = operation.create
    ad_group_ad.ad.final_urls.append("https://www.example.com")
    ad_group_ad.ad_group = googleads_service.ad_group_path(
        customer_id, ad_group_id
    )

    headline_1: AdTextAsset = client.get_type("AdTextAsset")
    headline_1.text = (
        f"Luxury cruise to {{CUSTOMIZER.{text_customizer_name}:Venus}}"
    )
    headline_1.pinned_field = client.enums.ServedAssetFieldTypeEnum.HEADLINE_1

    headline_2: AdTextAsset = client.get_type("AdTextAsset")
    headline_2.text = f"Only {{CUSTOMIZER.{price_customizer_name}:10.0€}}"

    headline_3: AdTextAsset = client.get_type("AdTextAsset")
    headline_3.text = f"Cruise to {{CUSTOMIZER.{text_customizer_name}:Venus}} for {{CUSTOMIZER.{price_customizer_name}:10.0€}}"

    ad_group_ad.ad.responsive_search_ad.headlines.extend(
        [headline_1, headline_2, headline_3]
    )

    description_1: AdTextAsset = client.get_type("AdTextAsset")
    description_1.text = (
        f"Tickets are only {{CUSTOMIZER.{price_customizer_name}:10.0€}}!"
    )

    description_2: AdTextAsset = client.get_type("AdTextAsset")
    description_2.text = (
        f"Buy your tickets to {{CUSTOMIZER.{text_customizer_name}:Venus}} now!"
    )

    ad_group_ad.ad.responsive_search_ad.descriptions.extend(
        [description_1, description_2]
    )

    response: MutateAdGroupAdsResponse = (
        ad_group_ad_service.mutate_ad_group_ads(
            customer_id=customer_id, operations=[operation]
        )
    )
    resource_name: str = response.results[0].resource_name
    print(f"Added an ad with resource name '{resource_name}'")
    # [END add_ad_customizer_3]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=(
            "This code example adds two ad customizer attributes and "
            "associates them with the ad group. Then it adds an ad that uses "
            "the customizer attributes to populate dynamic data."
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
        "-a",
        "--ad_group_id",
        type=str,
        required=True,
        help="An ad group ID.",
    )
    args: argparse.Namespace = parser.parse_args()

    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client: GoogleAdsClient = GoogleAdsClient.load_from_storage(
        version="v22"
    )

    try:
        main(googleads_client, args.customer_id, args.ad_group_id)
    except GoogleAdsException as ex:
        print(
            f'Request with ID "{ex.request_id}" failed with status '
            f'"{ex.error.code().name}" and includes the following errors:'
        )
        for error in ex.failure.errors:
            print(f'Error with message "{error.message}".')
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print(f"\t\tOn field: {field_path_element.field_name}")
        sys.exit(1)
