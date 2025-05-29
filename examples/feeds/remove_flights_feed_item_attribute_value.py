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
"""Removes a feed item attribute value of a feed item in a flights feed.

To create a flights feed, run the remarketing/add_flights_feed.py example. This
example is specific to feeds of type DYNAMIC_FLIGHT. The attribute you are
removing must be present on the feed.

This example is specifically for removing an attribute of a flights feed item,
but it can also be changed to work with other feed types.

To make this work with other feed types, replace the FlightPlaceholderField enum
with the equivalent one of your feed type, and replace the appropriate attribute
names in the _get_feeds method.
"""


import argparse
import sys
from typing import Dict, Mapping, Any

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
# from google.ads.googleads.v19.enums.types import flight_placeholder_field as flight_placeholder_field_enum # Removed problematic import
# Problematic type imports below are removed/commented. Types will be Any or obtained via client.get_type().
# from google.ads.googleads.v19.types import feed_item as feed_item_type
# from google.ads.googleads.v19.types import (
#     feed_item_operation as feed_item_operation_type,
# )
# from google.ads.googleads.v19.services.types import (
#     feed_item_service as feed_item_service_type,
# )
# from google.ads.googleads.v19.services.types import (
#     google_ads_service as google_ads_service_type,
# )
# from google.ads.googleads.v19.types import feed as feed_type

from google.api_core import protobuf_helpers


def main(
    client: GoogleAdsClient,
    customer_id: str,
    feed_id: str,
    feed_item_id: str,
    flight_placeholder_field_name: str,
) -> None:
    """Removes a feed item attribute value of a feed item in a flights feed.

    Args:
        client: An initialized GoogleAdsClient instance.
        customer_id: The Google Ads customer ID.
        feed_id: The feed ID to which the feed item belongs.
        feed_item_id: The ID of the feed item to be updated.
        flight_placeholder_field_name: The flight placeholder field name for the
            attribute to be removed.
    """
    # [START remove_flights_feed_item_attribute_value]
    # Get the FeedItemService client.
    feed_item_service: Any = client.get_service( # Type hint changed
        "FeedItemService"
    )

    # Create the FeedItemOperation.
    feed_item_operation: Any = client.get_type( # Type hint changed
        "FeedItemOperation"
    )

    # Get a map of the FlightPlaceholderFields to FeedAttributes.
    placeholders_to_feed_attributes_map: Mapping[
        Any, # Was flight_placeholder_field_enum.FlightPlaceholderFieldEnum
        Any, # Was feed_type.FeedAttribute
    ] = get_feed(client, customer_id, feed_id)

    # Remove the attribute from the feed item.
    # The type of flight_placeholder_field is an enum member, which is fine.
    # The type hint for the variable is changed to Any.
    flight_placeholder_field: Any = client.enums.FlightPlaceholderFieldEnum[
        flight_placeholder_field_name
    ] # .value was removed as direct enum member is used as key
    feed_item: Any = remove_attribute_value_from_feed_item( # Type hint changed
        client,
        customer_id,
        feed_id,
        feed_item_id,
        placeholders_to_feed_attributes_map,
        flight_placeholder_field, # Pass the enum member itself
    )
    client.copy_from(feed_item_operation.update, feed_item)
    # Configure the operation.
    client.copy_from(
        feed_item_operation.update_mask,
        protobuf_helpers.field_mask(None, feed_item._pb),
    )

    # Update the feed item and print the results.
    response: Any = feed_item_service.mutate_feed_items( # Type hint changed
        customer_id=customer_id, operations=[feed_item_operation]
    )
    # [END remove_flights_feed_item_attribute_value]

    for result in response.results:
        print(
            "Updated feed item with resource name: "
            f"'{result.resource_name}'."
        )


def get_feed(
    client: GoogleAdsClient, customer_id: str, feed_id: str
) -> Mapping[
    Any, # Was flight_placeholder_field_enum.FlightPlaceholderFieldEnum
    Any, # Was feed_type.FeedAttribute
]:
    """Retrieves details about a feed.

    Args:
        client: An initialized GoogleAdsClient instance.
        customer_id: The Google Ads customer ID.
        feed_id: The feed ID to which the feed item belongs.
    Returns:
        A dictionary that maps FlightPlaceholderFieldEnum values to the
        requested Feed's FeedAttributes.
    """
    # Get the GoogleAdsService client.
    googleads_service: Any = client.get_service( # Type hint changed
        "GoogleAdsService"
    )

    feed_resource_name: str = client.get_service("FeedService").feed_path(
        customer_id, feed_id
    )

    # Construct the query.
    query: str = f"""
        SELECT feed.attributes
        FROM feed
        WHERE feed.resource_name = '{feed_resource_name}'"""

    # Issue the search request and get the first result, since we only need the
    # single feed item we created previously.
    search_request: Any = client.get_type( # Type hint changed
        "SearchGoogleAdsRequest"
    )
    search_request.customer_id = customer_id
    search_request.query = query
    row: Any = next( # Type hint changed
        iter(googleads_service.search(request=search_request))
    )

    # Get the attributes list from the feed and create a map with keys of each
    # attribute and values of each corresponding ID.
    flight_placeholder_field_enum_type: Any = (
        client.enums.FlightPlaceholderFieldEnum
    )
    feed_attributes: Dict[
        Any, # Was flight_placeholder_field_enum.FlightPlaceholderFieldEnum
        Any, # Was feed_type.FeedAttribute
    ] = {}

    # Loop through the feed attributes to populate the map.
    # The full list of FlightPlaceholderFields can be found here:
    # https://developers.google.com/google-ads/api/reference/rpc/latest/FlightPlaceholderFieldEnum.FlightPlaceholderField
    for feed_attribute in row.feed.attributes:
        if feed_attribute.name == "Flight Description":
            feed_attributes[
                flight_placeholder_field_enum_type.FLIGHT_DESCRIPTION
            ] = feed_attribute
        elif feed_attribute.name == "Destination ID":
            feed_attributes[
                flight_placeholder_field_enum_type.DESTINATION_ID
            ] = feed_attribute
        elif feed_attribute.name == "Flight Price":
            feed_attributes[
                flight_placeholder_field_enum_type.FLIGHT_PRICE
            ] = feed_attribute
        elif feed_attribute.name == "Flight Sale Price":
            feed_attributes[
                flight_placeholder_field_enum_type.FLIGHT_SALE_PRICE
            ] = feed_attribute
        elif feed_attribute.name == "Final URLs":
            feed_attributes[
                flight_placeholder_field_enum_type.FINAL_URLS
            ] = feed_attribute
        else:
            # Allow for other attributes not explicitly handled to exist
            # without raising an error, as they might be valid for other feed types
            # or custom setups. The original script raised ValueError here.
            # For robustness, we'll just print a warning or skip.
            print(f"Warning: Unrecognized feed attribute name: {feed_attribute.name}")


    return feed_attributes


def remove_attribute_value_from_feed_item(
    client: GoogleAdsClient,
    customer_id: str,
    feed_id: str,
    feed_item_id: str,
    placeholders_to_feed_attributes_map: Mapping[
        Any, # Was flight_placeholder_field_enum.FlightPlaceholderFieldEnum
        Any, # Was feed_type.FeedAttribute
    ],
    flight_placeholder_field_name_enum_member: Any, # Was flight_placeholder_field_enum.FlightPlaceholderFieldEnum
) -> Any: # Was feed_item_type.FeedItem
    """Removes an attribute value from the specified feed item.

    Args:
        client: An initialized GoogleAdsClient instance.
        customer_id: The Google Ads customer ID.
        feed_id: The feed ID to which the feed item belongs.
        feed_item_id: The ID of the feed item to be updated.
        placeholders_to_feed_attributes_map: A map of placeholder fields to
            feed attributes.
        flight_placeholder_field_name_enum_member: The flight placeholder field enum member
            for the attribute to be removed.
    Returns:
        The modified FeedItem.
    """
    # [START remove_flights_feed_item_attribute_value_1]
    # Gets the ID of the FeedAttribute for the placeholder field.
    # The key for the map is now the enum member itself.
    attribute_id: int = placeholders_to_feed_attributes_map[
        flight_placeholder_field_name_enum_member
    ].id

    # Retrieve the feed item and its associated attributes based on its resource
    # name.
    feed_item: Any = get_feed_item( # Type hint changed
        client, customer_id, feed_id, feed_item_id
    )

    # Create the FeedItemAttributeValue that will be updated.
    feed_item_attribute_value: Any = client.get_type( # Type hint changed
        "FeedItemAttributeValue"
    )
    feed_item_attribute_value.feed_attribute_id = attribute_id

    # Loop through the attribute values to find the index of the
    # FeedItemAttributeValue to update.
    attribute_index: int = -1
    for i, attribute_value in enumerate(feed_item.attribute_values):
        if (
            attribute_value.feed_attribute_id
            == feed_item_attribute_value.feed_attribute_id
        ):
            attribute_index = i
            break

    if attribute_index == -1:
        raise ValueError(
            "No matching feed attribute found for value "
            f"'{feed_item_attribute_value}'."
        )

    # Returns the feed item with the removed FeedItemAttributeValue. Any
    # FeedItemAttributeValues that are not included in the updated FeedItem will
    # be removed from the FeedItem; you can easily accomplish this by removing
    # items from the AttributeValues list.
    feed_item.attribute_values.pop(attribute_index)
    return feed_item
    # [END remove_flights_feed_item_attribute_value_1]


def get_feed_item(
    client: GoogleAdsClient,
    customer_id: str,
    feed_id: str,
    feed_item_id: str,
) -> Any: # Was feed_item_type.FeedItem
    """Retrieves a feed item and its attribute values given a resource name.

    Args:
        client: The Google Ads API client.
        customer_id: The client customer ID.
        feed_id: The feed ID that contains the target feed item.
        feed_item_id: The feed item ID that will be updated.
    Returns:
        A FeedItem with the given resource name.
    """
    # Get the GoogleAdsService client.
    googleads_service: Any = client.get_service( # Type hint changed
        "GoogleAdsService"
    )

    # Construct the resource name for the feed item.
    feed_item_resource_name: str = client.get_service(
        "FeedItemService"
    ).feed_item_path(customer_id, feed_id, feed_item_id)

    # Construct the query.
    query: str = f"""
        SELECT feed_item.attribute_values
        FROM feed_item
        WHERE feed_item.resource_name = '{feed_item_resource_name}'"""

    # Issue the search request and return the first result, since the query will
    # match only a single feed item.
    search_request: Any = client.get_type( # Type hint changed
        "SearchGoogleAdsRequest"
    )
    search_request.customer_id = customer_id
    search_request.query = query

    return next(
        iter(googleads_service.search(request=search_request))
    ).feed_item


if __name__ == "__main__":
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Removes a feed item attribute value of a feed item in a "
        "flights feed."
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
        "-f",
        "--feed__id",  # Corrected from feed__id to feed_id for consistency with other uses
        type=str,
        required=True,
        help="The ID of the feed to which the feed item belongs.",
    )
    parser.add_argument(
        "-i",
        "--feed_item_id",
        type=str,
        required=True,
        help="The ID of the feed item to be updated.",
    )
    parser.add_argument(
        "-p",
        "--flight_placeholder_field_name",
        type=str,
        required=True,
        help="The flight placeholder field name for the attribute to be removed.",
    )
    args: argparse.Namespace = parser.parse_args()

    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client: GoogleAdsClient = GoogleAdsClient.load_from_storage(
        version="v19"
    )

    try:
        main(
            googleads_client,
            args.customer_id,
            args.feed_id, # Corrected from args.feed__id
            args.feed_item_id,
            args.flight_placeholder_field_name,
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
