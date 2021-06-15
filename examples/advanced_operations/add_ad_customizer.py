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
"""Adds an ad customizer feed and associates it with a given customer.

It then adds an ad that uses the feed to populate dynamic data.
"""


import argparse
from datetime import datetime
import sys
from uuid import uuid4

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


def main(client, customer_id, ad_group_ids):
    """The main method that creates all necessary entities for the example.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        ad_group_ids: a list of ad group IDs.
    """
    feed_name = f"Ad customizer example feed {uuid4()}"
    ad_customizer_feed_resource_name = _create_add_customizer_feed(
        client, customer_id, feed_name
    )
    ad_customizer_feed_attributes = _get_feed_attributes(
        client, customer_id, ad_customizer_feed_resource_name
    )

    _create_ad_customizer_mapping(
        client,
        customer_id,
        ad_customizer_feed_resource_name,
        ad_customizer_feed_attributes,
    )

    feed_item_resource_names = _create_feed_items(
        client,
        customer_id,
        ad_customizer_feed_resource_name,
        ad_customizer_feed_attributes,
    )

    _create_feed_item_targets(
        client, customer_id, ad_group_ids, feed_item_resource_names
    )

    _create_ads_with_customizations(
        client, customer_id, ad_group_ids, feed_name
    )


# [START add_ad_customizer]
def _create_add_customizer_feed(client, customer_id, feed_name):
    """Creates a feed to be used for ad customization.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        feed_name: the name of the feed to create.

    Returns:
        A str of a resource name for the newly created feed.
    """
    # Creates three feed attributes: a name, a price and a date.
    # The attribute names are arbitrary choices and will be used as
    # placeholders in the ad text fields.
    feed_attr_type_enum = client.get_type(
        "FeedAttributeTypeEnum"
    ).FeedAttributeType

    name_attr = client.get_type("FeedAttribute")
    name_attr.type_ = feed_attr_type_enum.STRING
    name_attr.name = "Name"

    price_attr = client.get_type("FeedAttribute")
    price_attr.type_ = feed_attr_type_enum.STRING
    price_attr.name = "Price"

    date_attr = client.get_type("FeedAttribute")
    date_attr.type_ = feed_attr_type_enum.DATE_TIME
    date_attr.name = "Date"

    feed_operation = client.get_type("FeedOperation")
    feed = feed_operation.create

    feed.name = feed_name
    feed.attributes.extend([name_attr, price_attr, date_attr])
    feed.origin = client.get_type("FeedOriginEnum").FeedOrigin.USER

    feed_service = client.get_service("FeedService")

    try:
        response = feed_service.mutate_feeds(
            customer_id=customer_id, operations=[feed_operation]
        )
        resource_name = response.results[0].resource_name
        print(f"Added feed with resource name {resource_name}")
        return resource_name
    except GoogleAdsException as ex:
        _handle_googleads_exception(ex)
        # [END add_ad_customizer]


# [START add_ad_customizer_1]
def _get_feed_attributes(client, customer_id, feed_resource_name):
    """Retrieves attributes for a feed.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        feed_resource_name: the resource name of the feed.

    Returns:
        A dict of feed attributes, keyed by attribute name.
    """
    query = f"""
      SELECT
        feed.attributes,
        feed.name
      FROM feed
      WHERE
        feed.resource_name = "{feed_resource_name}"
    """
    ga_service = client.get_service("GoogleAdsService")
    search_request = client.get_type("SearchGoogleAdsRequest")
    search_request.customer_id = customer_id
    search_request.query = query
    search_request.page_size = 1

    try:
        results = ga_service.search(request=search_request)
        feed = list(results)[0].feed
        print(f"Found the following attributes for feed with name {feed.name}")
    except GoogleAdsException as ex:
        _handle_googleads_exception(ex)

    feed_attr_type_enum = client.get_type("FeedAttributeTypeEnum")
    feed_details = {}
    for feed_attribute in feed.attributes:
        name = feed_attribute.name
        feed_attr_id = feed_attribute.id
        feed_type = feed_attribute.type_.name
        feed_details[name] = feed_attr_id
        print(f"\t{name} with id {feed_attr_id} and type {feed_type}.")

    return feed_details
    # [END add_ad_customizer_1]


# [START add_ad_customizer_2]
def _create_ad_customizer_mapping(
    client, customer_id, ad_customizer_feed_resource_name, feed_details,
):
    """Creates a feed mapping for a given feed.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        ad_customizer_feed_resource_name: the resource name of the ad customizer
            feed.
        feed_details: a dict mapping feed attribute names to their IDs.
    """
    placeholder_field_enum = client.get_type(
        "AdCustomizerPlaceholderFieldEnum"
    ).AdCustomizerPlaceholderField

    # Map the feed attributes to ad customizer placeholder fields. For a full
    # list of ad customizer placeholder fields, see:
    # https://developers.google.com/google-ads/api/reference/rpc/latest/AdCustomizerPlaceholderFieldEnum.AdCustomizerPlaceholderField
    name_field_mapping = client.get_type("AttributeFieldMapping")
    name_field_mapping.feed_attribute_id = feed_details["Name"]
    name_field_mapping.ad_customizer_field = placeholder_field_enum.STRING

    price_field_mapping = client.get_type("AttributeFieldMapping")
    price_field_mapping.feed_attribute_id = feed_details["Price"]
    price_field_mapping.ad_customizer_field = placeholder_field_enum.PRICE

    date_field_mapping = client.get_type("AttributeFieldMapping")
    date_field_mapping.feed_attribute_id = feed_details["Date"]
    date_field_mapping.ad_customizer_field = placeholder_field_enum.DATE

    feed_mapping_op = client.get_type("FeedMappingOperation")
    feed_mapping = feed_mapping_op.create
    feed_mapping.feed = ad_customizer_feed_resource_name
    feed_mapping.placeholder_type = client.get_type(
        "PlaceholderTypeEnum"
    ).PlaceholderType.AD_CUSTOMIZER
    feed_mapping.attribute_field_mappings.extend(
        [name_field_mapping, price_field_mapping, date_field_mapping]
    )

    feed_mapping_service = client.get_service("FeedMappingService")

    try:
        response = feed_mapping_service.mutate_feed_mappings(
            customer_id=customer_id, operations=[feed_mapping_op]
        )
        for result in response.results:
            print(
                "Created feed mapping with resource name "
                f"{result.resource_name}"
            )
    except GoogleAdsException as ex:
        _handle_googleads_exception(ex)
        # [END add_ad_customizer_2]


# [START add_ad_customizer_3]
def _create_feed_items(
    client,
    customer_id,
    ad_customizer_feed_resource_name,
    ad_customizer_feed_attributes,
):
    """Creates two feed items to enable two different ad customizations.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        ad_customizer_feed_resource_name: the resource name of the ad customizer
            feed.
        ad_customizer_feed_attributes: a dict mapping feed attribute names to
            their IDs.

    Returns:
        A list of feed item resource name strs.
    """
    feed_item_operations = []
    feed_item_operations.append(
        _create_feed_item_operation(
            client,
            "Mars",
            "$1234.56",
            # Set the date to the 1st of the current month.
            datetime.now().replace(day=1).strftime("%Y%m%d %H%M%S"),
            ad_customizer_feed_resource_name,
            ad_customizer_feed_attributes,
        )
    )
    feed_item_operations.append(
        _create_feed_item_operation(
            client,
            "Venus",
            "$6543.21",
            # Set the date to the 15th of the current month.
            datetime.now().replace(day=15).strftime("%Y%m%d %H%M%S"),
            ad_customizer_feed_resource_name,
            ad_customizer_feed_attributes,
        )
    )

    feed_item_service = client.get_service("FeedItemService")

    try:
        response = feed_item_service.mutate_feed_items(
            customer_id=customer_id, operations=feed_item_operations
        )
        return [feed_item.resource_name for feed_item in response.results]
    except GoogleAdsException as ex:
        _handle_googleads_exception(ex)
        # [END add_ad_customizer_3]


# [START add_ad_customizer_4]
def _create_feed_item_operation(
    client,
    name,
    price,
    date,
    ad_customizer_feed_resource_name,
    ad_customizer_feed_attributes,
):
    """Creates a FeedItemOperation.

    Args:
        client: an initialized GoogleAdsClient instance.
        name: a str value for the name attribute of the feed_item
        price: a str value for the price attribute of the feed_item
        date: a str value for the date attribute of the feed_item
        ad_customizer_feed_resource_name: the resource name of the ad customizer
            feed.
        ad_customizer_feed_attributes: a dict mapping feed attribute names to
            their IDs.

    Returns:
        A FeedItemOperation that creates a FeedItem
    """
    name_attr_value = client.get_type("FeedItemAttributeValue")
    name_attr_value.feed_attribute_id = ad_customizer_feed_attributes["Name"]
    name_attr_value.string_value = name

    price_attr_value = client.get_type("FeedItemAttributeValue")
    price_attr_value.feed_attribute_id = ad_customizer_feed_attributes["Price"]
    price_attr_value.string_value = price

    date_attr_value = client.get_type("FeedItemAttributeValue")
    date_attr_value.feed_attribute_id = ad_customizer_feed_attributes["Date"]
    date_attr_value.string_value = date

    feed_item_op = client.get_type("FeedItemOperation")
    feed_item = feed_item_op.create
    feed_item.feed = ad_customizer_feed_resource_name
    feed_item.attribute_values.extend(
        [name_attr_value, price_attr_value, date_attr_value]
    )

    return feed_item_op
    # [END add_ad_customizer_4]


# [START add_ad_customizer_5]
def _create_feed_item_targets(
    client, customer_id, ad_group_ids, feed_item_resource_names
):
    """Restricts the feed items to work only with a specific ad group.

    This prevents the feed items from being used elsewhere and makes sure they
    are used only for customizing a specific ad group.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        ad_group_ids: a list of ad group IDs.
        feed_item_resource_names: a list of feed item resource name strs.
    """
    ad_group_service = client.get_service("AdGroupService")
    feed_item_target_service = client.get_service("FeedItemTargetService")
    # Bind each feed item to a specific ad group to make sure it will only be
    # used to customize ads inside that ad group; using the feed item elsewhere
    # will result in an error.
    for i, resource_name in enumerate(feed_item_resource_names):
        ad_group_id = ad_group_ids[i]

        feed_item_target_op = client.get_type("FeedItemTargetOperation")
        feed_item_target = feed_item_target_op.create
        feed_item_target.feed_item = resource_name
        feed_item_target.ad_group = ad_group_service.ad_group_path(
            customer_id, ad_group_id
        )

        try:
            response = feed_item_target_service.mutate_feed_item_targets(
                customer_id=customer_id, operations=[feed_item_target_op]
            )
            print(
                "Added feed item target with resource name "
                f"{response.results[0].resource_name}"
            )
        except GoogleAdsException as ex:
            _handle_googleads_exception(ex)
            # [END add_ad_customizer_5]


# [START add_ad_customizer_6]
def _create_ads_with_customizations(
    client, customer_id, ad_group_ids, feed_name
):
    """Creates expanded text ads that use the ad customizer feed.

    The expanded text ads use the ad customizer feed to populate the
    placeholders.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        ad_group_ids: a list of ad group IDs.
        feed_name: the name of the feed to create.
    """
    ad_group_service = client.get_service("AdGroupService")
    ad_group_ad_service = client.get_service("AdGroupAdService")
    ad_group_ad_operations = []

    for ad_group_id in ad_group_ids:
        ad_group_ad_operation = client.get_type("AdGroupAdOperation")
        ad_group_ad = ad_group_ad_operation.create
        ad_group_ad.ad_group = ad_group_service.ad_group_path(
            customer_id, ad_group_id
        )
        ad_group_ad.ad.final_urls.append("http://www.example.com")
        ad_group_ad.ad.expanded_text_ad.headline_part1 = (
            f"Luxury cruise to {{={feed_name}.Name}}"
        )
        ad_group_ad.ad.expanded_text_ad.headline_part2 = (
            f"Only {{={feed_name}.Price}}"
        )
        # See this documentation for an explanation of how countdown ad
        # customizers work: https://support.google.com/google-ads/answer/6193743?hl=en
        ad_group_ad.ad.expanded_text_ad.description = (
            f"Offer ends in {{=countdown({feed_name}.Date)}}!"
        )
        ad_group_ad_operations.append(ad_group_ad_operation)

    try:
        response = ad_group_ad_service.mutate_ad_group_ads(
            customer_id=customer_id, operations=ad_group_ad_operations
        )
        print(f"Added {len(response.results)} ads:")
        for ad in response.results:
            print(f"Added an ad with resource name {ad.resource_name}")
    except GoogleAdsException as ex:
        _handle_googleads_exception(ex)
        # [END add_ad_customizer_6]


def _handle_googleads_exception(exception):
    """Prints the details of a GoogleAdsException object.

    Args:
        exception: an instance of GoogleAdsException.
    """
    print(
        f'Request with ID "{exception.request_id}" failed with status '
        f'"{exception.error.code().name}" and includes the following errors:'
    )
    for error in exception.failure.errors:
        print(f'\tError with message "{error.message}".')
        if error.location:
            for field_path_element in error.location.field_path_elements:
                print(f"\t\tOn field: {field_path_element.field_name}")
    sys.exit(1)


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v8")

    parser = argparse.ArgumentParser(
        description=(
            "Adds an ad customizer feed and associates it with a customer."
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
        "--ad_group_ids",
        nargs=2,
        type=str,
        required=True,
        help="Space-delimited list of ad group IDs.",
    )
    args = parser.parse_args()

    main(googleads_client, args.customer_id, args.ad_group_ids)
