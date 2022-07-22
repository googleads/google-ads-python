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
"""Adds a customizer attribute.

Also links the customizer attribute to a customer, and then adds a responsive
search ad with a description using the ad customizer to the specified ad group.

Customizer attributes and ad group customizers are created for business data
customizers. For more information about responsive search ad customization see:
https://developers.google.com/google-ads/api/docs/ads/customize-responsive-search-ads?hl=en
"""


import argparse
from datetime import date, timedelta
import sys
from uuid import uuid4

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

# The name of the customizer attribute to be used in the ad customizer, which
# must be unique for a given customer account. To run this example multiple
# times, specify a unique value as a command line argument. Note that there is
# a limit for the number of enabled customizer attributes in one account, so
# you shouldn't run this example more than necessary. For more details visit:
# https://developers.google.com/google-ads/api/docs/ads/customize-responsive-search-ads#rules_and_limitations
_CUSTOMIZER_ATTRIBUTE_NAME = "Price"


def main(client, customer_id, ad_group_id, customizer_attribute_name):
    """The main method that creates all necessary entities for the example.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        ad_group_id: an ad group ID.
        customizer_attribute_name: the name for the customizer attribute.
    """
    customizer_attribute_resource_name = _create_customizer_attribute(
        client, customer_id, customizer_attribute_name
    )

    _link_customizer_attribute_to_customer(
        client, customer_id, customizer_attribute_resource_name
    )

    _create_responsive_search_ad_with_customization(
        client, customer_id, ad_group_id, customizer_attribute_name
    )


# [START add_responsive_search_ad_with_ad_customizer_1]
def _create_customizer_attribute(
    client, customer_id, customizer_attribute_name
):
    """Creates a customizer attribute with the given customizer attribute name.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        customizer_attribute_name: the name for the customizer attribute.

    Returns:
        A resource name for a customizer attribute.
    """
    # Creates a customizer attribute operation for creating a customizer
    # attribute.
    operation = client.get_type("CustomizerAttributeOperation")
    # Creates a customizer attribute with the specified name.
    customizer_attribute = operation.create
    customizer_attribute.name = customizer_attribute_name
    # Specifies the type to be 'PRICE' so that we can dynamically customize the
    # part of the ad's description that is a price of a product/service we
    # advertise.
    customizer_attribute.type_ = client.enums.CustomizerAttributeTypeEnum.PRICE

    # Issues a mutate request to add the customizer attribute and prints its
    # information.
    customizer_attribute_service = client.get_service(
        "CustomizerAttributeService"
    )
    response = customizer_attribute_service.mutate_customizer_attributes(
        customer_id=customer_id, operations=[operation]
    )
    resource_name = response.results[0].resource_name

    print(f"Added a customizer attribute with resource name: '{resource_name}'")

    return resource_name
    # [END add_responsive_search_ad_with_ad_customizer_1]


# [START add_responsive_search_ad_with_ad_customizer_2]
def _link_customizer_attribute_to_customer(
    client, customer_id, customizer_attribute_resource_name
):
    """Links the customizer attribute to the customer.

    This is done by providing a value to be used in a responsive search ad
    that will be created in a later step.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        customizer_attribute_resource_name: a resource name for  customizer
            attribute.
    """
    # Creates a customer customizer operation.
    operation = client.get_type("CustomerCustomizerOperation")
    # Creates a customer customizer with the value to be used in the responsive
    # search ad.
    customer_customizer = operation.create
    customer_customizer.customizer_attribute = (
        customizer_attribute_resource_name
    )
    customer_customizer.value.type_ = (
        client.enums.CustomizerAttributeTypeEnum.PRICE
    )
    # Specify '100USD' as a text value. The ad customizer will dynamically
    # replace the placeholder with this value when the ad serves.
    customer_customizer.value.string_value = "100USD"

    customer_customizer_service = client.get_service(
        "CustomerCustomizerService"
    )
    # Issues a mutate request to add the customer customizer and prints its
    # information.
    response = customer_customizer_service.mutate_customer_customizers(
        customer_id=customer_id, operations=[operation]
    )
    resource_name = response.results[0].resource_name

    print(f"Added a customer customizer with resource name: '{resource_name}'")
    # [END add_responsive_search_ad_with_ad_customizer_2]


# [START add_responsive_search_ad_with_ad_customizer_3]
def _create_responsive_search_ad_with_customization(
    client, customer_id, ad_group_id, customizer_attribute_name
):
    """Creates a responsive search ad using the specified customizer attribute.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        ad_group_id: an ad group ID.
        customizer_attribute_name: the name for the customizer attribute.
    """
    # Creates an ad group ad operation.
    operation = client.get_type("AdGroupAdOperation")
    # Creates an ad group ad.
    ad_group_ad = operation.create
    ad_group_service = client.get_service("AdGroupService")
    ad_group_ad.ad_group = ad_group_service.ad_group_path(
        customer_id, ad_group_id
    )
    ad_group_ad.status = client.enums.AdGroupAdStatusEnum.PAUSED
    #  Creates an ad and sets responsive search ad info.
    ad = ad_group_ad.ad
    ad.final_urls.append("http://www.example.com")

    headline_1 = client.get_type("AdTextAsset")
    headline_1.text = "Cruise to Mars"
    headline_2 = client.get_type("AdTextAsset")
    headline_2.text = "Best Space Cruise Line"
    headline_3 = client.get_type("AdTextAsset")
    headline_3.text = "Experience the Stars"
    ad.responsive_search_ad.headlines.extend(
        [headline_1, headline_2, headline_3]
    )

    description_1 = client.get_type("AdTextAsset")
    description_1.text = "Buy your tickets now"
    # Creates this particular description using the ad customizer. Visit
    # https://developers.google.com/google-ads/api/docs/ads/customize-responsive-search-ads#ad_customizers_in_responsive_search_ads
    # for details about the placeholder format. The ad customizer replaces the
    # placeholder with the value we previously created and linked to the
    # customer using CustomerCustomizer.
    description_2 = client.get_type("AdTextAsset")
    description_2.text = (
        f"Just {{CUSTOMIZER.{customizer_attribute_name}:10USD}}"
    )
    ad.responsive_search_ad.descriptions.extend([description_1, description_2])

    ad.responsive_search_ad.path1 = "all-inclusive"
    ad.responsive_search_ad.path2 = "deals"

    # Issues a mutate request to add the ad group ad and prints its information.
    ad_group_ad_service = client.get_service("AdGroupAdService")
    response = ad_group_ad_service.mutate_ad_group_ads(
        customer_id=customer_id, operations=[operation]
    )
    resource_name = response.results[0].resource_name

    print(f"Created responsive search ad with resource name: '{resource_name}'")
    # [END add_responsive_search_ad_with_ad_customizer_3]


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v11")

    parser = argparse.ArgumentParser(
        description=(
            "Creates ad customizers and applies them to a responsive search ad."
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
    parser.add_argument(
        "-n",
        "--customizer_attribute_name",
        type=str,
        default=_CUSTOMIZER_ATTRIBUTE_NAME,
        help=(
            "The name of the customizer attribute to be created. The name must "
            "be unique across a single client account, so be sure not to use "
            "the same value more than once."
        ),
    )
    args = parser.parse_args()

    try:
        main(
            googleads_client,
            args.customer_id,
            args.ad_group_id,
            args.customizer_attribute_name,
        )
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
