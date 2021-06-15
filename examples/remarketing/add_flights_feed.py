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
"""Adds a flights feed, creates associated field mapping, and adds feed item.
"""


import argparse
import sys
from uuid import uuid4

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

_DEFAULT_PAGE_SIZE = 10000


def main(client, customer_id):
    """The main method that creates all necessary entities for the example.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
    """
    # Creates a new flights feed.
    feed_resource_name = _create_feed(client, customer_id)

    print(f"Feed with resource name '{feed_resource_name}' was created.")

    # Gets the newly created feed's attributes and packages them into a map.
    # This read operation is required to retrieve the attribute IDs.
    placeholders_to_feed_attributes_map = _get_placeholder_fields_map(
        client, customer_id, feed_resource_name
    )

    # Creates the feed mapping.
    feed_mapping_resource_name = _create_feed_mapping(
        client,
        customer_id,
        feed_resource_name,
        placeholders_to_feed_attributes_map,
    )

    print(
        f"Feed mapping with resource name '{feed_mapping_resource_name}' "
        "was created."
    )

    # Creates a feed item.
    feed_item_resource_name = _create_feed_item(
        client,
        customer_id,
        feed_resource_name,
        placeholders_to_feed_attributes_map,
    )

    print(
        f"Feed item with resource name '{feed_item_resource_name}' was "
        "created."
    )


def _create_feed(client, customer_id):
    """Creates a feed that will be used as a flight feed.

    Args:
        client: An initialized GoogleAds client.
        customer_id: The Google Ads customer ID.

    Returns:
        A str resource name of the newly created feed.
    """
    feed_service = client.get_service("FeedService")
    feed_attribute_type_enum = client.get_type(
        "FeedAttributeTypeEnum"
    ).FeedAttributeType

    # Creates the feed operation.
    feed_operation = client.get_type("FeedOperation")

    # Create the feed with feed attributes defined below.
    feed = feed_operation.create
    feed.name = f"Flights Feed #{uuid4()}"

    # Creates a flight description attribute.
    flight_description_attribute = client.get_type("FeedAttribute")
    flight_description_attribute.name = "Flight Description"
    flight_description_attribute.type_ = feed_attribute_type_enum.STRING

    # Creates a destination ID attribute.
    destination_id_attribute = client.get_type("FeedAttribute")
    destination_id_attribute.name = "Destination ID"
    destination_id_attribute.type_ = feed_attribute_type_enum.STRING

    # Creates a flight price attribute.
    flight_price_attribute = client.get_type("FeedAttribute")
    flight_price_attribute.name = "Flight Price"
    flight_price_attribute.type_ = feed_attribute_type_enum.STRING

    # Creates a flight sale price attribute.
    flight_sale_price_attribute = client.get_type("FeedAttribute")
    flight_sale_price_attribute.name = "Flight Sale Price"
    flight_sale_price_attribute.type_ = feed_attribute_type_enum.STRING

    # Creates a final URLs attribute.
    final_urls_attribute = client.get_type("FeedAttribute")
    final_urls_attribute.name = "Final URLs"
    final_urls_attribute.type_ = feed_attribute_type_enum.URL_LIST

    # append FeedAttributes to feed.attributes
    feed.attributes.extend(
        [
            flight_description_attribute,
            destination_id_attribute,
            flight_price_attribute,
            flight_sale_price_attribute,
            final_urls_attribute,
        ]
    )
    try:
        # Issues a mutate request to add the feed.
        feed_response = feed_service.mutate_feeds(
            customer_id=customer_id, operations=[feed_operation]
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

    return feed_response.results[0].resource_name


def _create_feed_mapping(
    client, customer_id, feed_resource_name, placeholders_to_feed_attribute_map
):
    """Creates a feed mapping for a given feed.

    Args:
        client: An initialized GoogleAds client.
        customer_id: The Google Ads customer ID.
        feed_resource_name: A str feed resource name for creating a feed
            mapping.
        placeholders_to_feed_attribute_map: A dict mapping placeholder feeds to
            feed attributes.

    Returns:
        A str resource name of the newly created feed mapping.
    """
    feed_mapping_service = client.get_service("FeedMappingService")

    # Creates the feed mapping operation.
    feed_mapping_operation = client.get_type("FeedMappingOperation")

    # Create the feed with feed attributes defined below.
    feed_mapping = feed_mapping_operation.create
    feed_mapping.feed = feed_resource_name
    feed_mapping.placeholder_type = client.get_type(
        "PlaceholderTypeEnum"
    ).PlaceholderType.DYNAMIC_FLIGHT

    # Maps the feed attribute IDs to the field ID constants.
    placeholder_field_enum = client.get_type(
        "FlightPlaceholderFieldEnum"
    ).FlightPlaceholderField
    flight_desc_enum_value = placeholder_field_enum.FLIGHT_DESCRIPTION
    desc_mapping = client.get_type("AttributeFieldMapping", "v6")
    desc_mapping.feed_attribute_id = placeholders_to_feed_attribute_map[
        flight_desc_enum_value
    ].id
    desc_mapping.flight_field = flight_desc_enum_value

    flight_dest_id_enum_value = placeholder_field_enum.DESTINATION_ID
    dest_id_mapping = client.get_type("AttributeFieldMapping", "v6")
    dest_id_mapping.feed_attribute_id = placeholders_to_feed_attribute_map[
        flight_dest_id_enum_value
    ].id
    dest_id_mapping.flight_field = flight_dest_id_enum_value

    flight_price_enum_value = placeholder_field_enum.FLIGHT_PRICE
    price_mapping = client.get_type("AttributeFieldMapping", "v6")
    price_mapping.feed_attribute_id = placeholders_to_feed_attribute_map[
        flight_price_enum_value
    ].id
    price_mapping.flight_field = flight_price_enum_value

    flight_sale_price_enum_value = placeholder_field_enum.FLIGHT_SALE_PRICE
    sale_price_mapping = client.get_type("AttributeFieldMapping", "v6")
    sale_price_mapping.feed_attribute_id = placeholders_to_feed_attribute_map[
        flight_sale_price_enum_value
    ].id
    sale_price_mapping.flight_field = flight_sale_price_enum_value

    flight_final_urls_enum_value = placeholder_field_enum.FINAL_URLS
    final_urls_mapping = client.get_type("AttributeFieldMapping", "v6")
    final_urls_mapping.feed_attribute_id = placeholders_to_feed_attribute_map[
        flight_final_urls_enum_value
    ].id
    final_urls_mapping.flight_field = flight_final_urls_enum_value

    feed_mapping.attribute_field_mappings.extend(
        [
            desc_mapping,
            dest_id_mapping,
            price_mapping,
            sale_price_mapping,
            final_urls_mapping,
        ]
    )

    try:
        # Issues a mutate request to add the feed mapping.
        feed_mapping_response = feed_mapping_service.mutate_feed_mappings(
            customer_id=customer_id, operations=[feed_mapping_operation]
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

    return feed_mapping_response.results[0].resource_name


def _create_feed_item(
    client, customer_id, feed_resource_name, placeholders_to_feed_attribute_map
):
    """Adds a new item to the feed.

    Args:
        client: An initialized GoogleAds client.
        customer_id: The Google Ads customer ID.
        feed_resource_name: A str feed resource name for creating a feed item.
        placeholders_to_feed_attribute_map: A dict mapping placeholder feeds to
            feed attributes.

    Returns:
        A str resource name of the newly created feed item.
    """
    feed_item_service = client.get_service("FeedItemService")

    # Creates the feed mapping operation.
    feed_item_operation = client.get_type("FeedItemOperation")

    # Create the feed item, with feed attributes created below.
    feed_item = feed_item_operation.create
    feed_item.feed = feed_resource_name

    placeholder_field_enum = client.get_type(
        "FlightPlaceholderFieldEnum"
    ).FlightPlaceholderField

    # Returns a new instance of FeedItemAttributeValue when called.
    # This prevents the need to repeat these lines every time we need a new
    # FeedItemAttributeValue. Instead, we call feed_item_attribute_value()
    feed_item_attribute_value = lambda: client.get_type(
        "FeedItemAttributeValue"
    )

    # Creates the flight description feed attribute value.
    flight_desc_enum_value = placeholder_field_enum.FLIGHT_DESCRIPTION
    desc_mapping = feed_item_attribute_value()
    desc_mapping.feed_attribute_id = placeholders_to_feed_attribute_map[
        flight_desc_enum_value
    ].id
    desc_mapping.string_value = "Earth to Mars"

    # Creates the destination ID feed attribute value.
    flight_dest_id_enum_value = placeholder_field_enum.DESTINATION_ID
    dest_id_mapping = feed_item_attribute_value()
    dest_id_mapping.feed_attribute_id = placeholders_to_feed_attribute_map[
        flight_dest_id_enum_value
    ].id
    dest_id_mapping.string_value = "Mars"

    # Creates the flight price feed attribute value.
    flight_price_enum_value = placeholder_field_enum.FLIGHT_PRICE
    price_mapping = feed_item_attribute_value()
    price_mapping.feed_attribute_id = placeholders_to_feed_attribute_map[
        flight_price_enum_value
    ].id
    price_mapping.string_value = "499.99 USD"

    # Creates the flight sale price feed attribute value.
    flight_sale_price_enum_value = placeholder_field_enum.FLIGHT_SALE_PRICE
    sale_price_mapping = feed_item_attribute_value()
    sale_price_mapping.feed_attribute_id = placeholders_to_feed_attribute_map[
        flight_sale_price_enum_value
    ].id
    sale_price_mapping.string_value = "299.99 USD"

    # Creates the final URLs feed attribute value.
    flight_final_urls_enum_value = placeholder_field_enum.FINAL_URLS
    final_urls_mapping = feed_item_attribute_value()
    final_urls_mapping.feed_attribute_id = placeholders_to_feed_attribute_map[
        flight_final_urls_enum_value
    ].id
    final_urls_mapping.string_values.append("http://www.example.com/flights")

    feed_item.attribute_values.extend(
        [
            desc_mapping,
            dest_id_mapping,
            price_mapping,
            sale_price_mapping,
            final_urls_mapping,
        ]
    )

    try:
        # Issues a mutate request to add the feed item.
        feed_item_response = feed_item_service.mutate_feed_items(
            customer_id=customer_id, operations=[feed_item_operation]
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

    return feed_item_response.results[0].resource_name


def _get_placeholder_fields_map(client, customer_id, feed_resource_name):
    """Get mapping of placeholder fields to feed attributes for a flights feed.

    Args:
        client: An initialized GoogleAds client.
        customer_id: The Google Ads customer ID.
        feed_resource_name: A str feed resource name to get attributes from.

    Returns:
        A dict mapping placeholder fields to feed attributes.
    """
    googleads_service = client.get_service("GoogleAdsService")

    # Constructs the query to get the feed attributes for the specified
    # resource name.
    query = f"""
        SELECT
          feed.attributes
        FROM
          feed
        WHERE
          feed.resource_name = '{feed_resource_name}'"""

    # Issues a search request by specifying a page size.
    search_request = client.get_type("SearchGoogleAdsRequest")
    search_request.customer_id = customer_id
    search_request.query = query
    search_request.page_size = _DEFAULT_PAGE_SIZE
    response = googleads_service.search(request=search_request)

    try:
        # Gets the first result because we only need the single feed we created
        # previously.
        row = list(response)[0]
        feed_attributes = row.feed.attributes

        flight_placeholder_field_enum = client.get_type(
            "FlightPlaceholderFieldEnum"
        ).FlightPlaceholderField
        feed_attribute_names_map = {
            "Flight Description": flight_placeholder_field_enum.FLIGHT_DESCRIPTION,
            "Destination ID": flight_placeholder_field_enum.DESTINATION_ID,
            "Flight Price": flight_placeholder_field_enum.FLIGHT_PRICE,
            "Flight Sale Price": flight_placeholder_field_enum.FLIGHT_SALE_PRICE,
            "Final URLs": flight_placeholder_field_enum.FINAL_URLS,
        }

        # Creates map with keys of placeholder fields and values of feed
        # attributes.
        placeholder_fields_map = {
            feed_attribute_names_map[feed_attribute.name]: feed_attribute
            for feed_attribute in feed_attributes
        }
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

    return placeholder_fields_map


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v8")

    parser = argparse.ArgumentParser(
        description="Adds a flights feed for specified customer."
    )
    # The following argument(s) should be provided to run the example.
    parser.add_argument(
        "-c",
        "--customer_id",
        type=str,
        required=True,
        help="The Google Ads customer ID.",
    )
    args = parser.parse_args()

    main(googleads_client, args.customer_id)
