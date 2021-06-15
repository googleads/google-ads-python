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

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.api_core import protobuf_helpers


def main(
    client, customer_id, feed_id, feed_item_id, flight_placeholder_field_name
):
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
    feed_item_service = client.get_service("FeedItemService")

    # Create the FeedItemOperation.
    feed_item_operation = client.get_type("FeedItemOperation")

    # Get a map of the FlightPlaceholderFields to FeedAttributes.
    placeholders_to_feed_attributes_map = _get_feed(
        client, customer_id, feed_id
    )

    # Remove the attribute from the feed item.
    flight_placeholder_field = (
        client.get_type("FlightPlaceholderFieldEnum")
        .FlightPlaceholderField[flight_placeholder_field_name]
        .value
    )
    feed_item = _remove_attribute_value_from_feed_item(
        client,
        customer_id,
        feed_id,
        feed_item_id,
        placeholders_to_feed_attributes_map,
        flight_placeholder_field,
    )
    client.copy_from(feed_item_operation.update, feed_item)
    # Configure the operation.
    client.copy_from(
        feed_item_operation.update_mask,
        protobuf_helpers.field_mask(None, feed_item._pb),
    )

    # Update the feed item and print the results.
    response = feed_item_service.mutate_feed_items(
        customer_id=customer_id, operations=[feed_item_operation]
    )
    # [END remove_flights_feed_item_attribute_value]

    for result in response.results:
        print(
            "Updated feed item with resource name: "
            f"'{result.resource_name}'."
        )


def _get_feed(client, customer_id, feed_id):
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
    googleads_service = client.get_service("GoogleAdsService")

    feed_resource_name = client.get_service("FeedService").feed_path(
        customer_id, feed_id
    )

    # Construct the query.
    query = f"""
        SELECT feed.attributes
        FROM feed
        WHERE feed.resource_name = '{feed_resource_name}'"""

    # Issue the search request and get the first result, since we only need the
    # single feed item we created previously.
    search_request = client.get_type("SearchGoogleAdsRequest")
    search_request.customer_id = customer_id
    search_request.query = query
    row = next(iter(googleads_service.search(request=search_request)))

    # Get the attributes list from the feed and create a map with keys of each
    # attribute and values of each corresponding ID.
    flight_placeholder_field_enum = client.get_type(
        "FlightPlaceholderFieldEnum"
    ).FlightPlaceholderField
    feed_attributes = dict()

    # Loop through the feed attributes to populate the map.
    # The full list of FlightPlaceholderFields can be found here:
    # https://developers.google.com/google-ads/api/reference/rpc/latest/FlightPlaceholderFieldEnum.FlightPlaceholderField
    for feed_attribute in row.feed.attributes:
        if feed_attribute.name == "Flight Description":
            feed_attributes[
                flight_placeholder_field_enum.FLIGHT_DESCRIPTION
            ] = feed_attribute
        elif feed_attribute.name == "Destination ID":
            feed_attributes[
                flight_placeholder_field_enum.DESTINATION_ID
            ] = feed_attribute
        elif feed_attribute.name == "Flight Price":
            feed_attributes[
                flight_placeholder_field_enum.FLIGHT_PRICE
            ] = feed_attribute
        elif feed_attribute.name == "Flight Sale Price":
            feed_attributes[
                flight_placeholder_field_enum.FLIGHT_SALE_PRICE
            ] = feed_attribute
        elif feed_attribute.name == "Final URLs":
            feed_attributes[
                flight_placeholder_field_enum.FINAL_URLS
            ] = feed_attribute
        else:
            raise ValueError("Invalid attribute name.")

    return feed_attributes


def _remove_attribute_value_from_feed_item(
    client,
    customer_id,
    feed_id,
    feed_item_id,
    placeholders_to_feed_attributes_map,
    flight_placeholder_field_name,
):
    """Removes an attribute value from the specified feed item.

    Args:
        client:
        customer_id:
        feed_id:
        feed_item_id:
        placeholders_to_feed_attributes_map:
        flight_placeholder_field_name:
    Returns:
        The modified FeedItem.
    """
    # [START remove_flights_feed_item_attribute_value_1]
    # Gets the ID of the FeedAttribute for the placeholder field.
    attribute_id = placeholders_to_feed_attributes_map[
        flight_placeholder_field_name
    ].id

    # Retrieve the feed item and its associated attributes based on its resource
    # name.
    feed_item = _get_feed_item(client, customer_id, feed_id, feed_item_id)

    # Create the FeedItemAttributeValue that will be updated.
    feed_item_attribute_value = client.get_type("FeedItemAttributeValue")
    feed_item_attribute_value.feed_attribute_id = attribute_id

    # Loop through the attribute values to find the index of the
    # FeedItemAttributeValue to update.
    attribute_index = -1
    for attribute_value in feed_item.attribute_values:
        attribute_index += 1
        if (
            attribute_value.feed_attribute_id
            == feed_item_attribute_value.feed_attribute_id
        ):
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


def _get_feed_item(client, customer_id, feed_id, feed_item_id):
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
    googleads_service = client.get_service("GoogleAdsService")

    # Construct the resource name for the feed item.
    feed_item_resource_name = client.get_service(
        "FeedItemService"
    ).feed_item_path(customer_id, feed_id, feed_item_id)

    # Construct the query.
    query = f"""
        SELECT feed_item.attribute_values
        FROM feed_item
        WHERE feed_item.resource_name = '{feed_item_resource_name}'"""

    # Issue the search request and return the first result, since the query will
    # match only a single feed item.
    search_request = client.get_type("SearchGoogleAdsRequest")
    search_request.customer_id = customer_id
    search_request.query = query

    return next(
        iter(googleads_service.search(request=search_request))
    ).feed_item


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v8")

    parser = argparse.ArgumentParser(
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
        "--feed_id",
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
    args = parser.parse_args()

    try:
        main(
            googleads_client,
            args.customer_id,
            args.feed_id,
            args.feed_item_id,
            args.flight_placeholder_field_name,
        )
    except GoogleAdsException as ex:
        print(
            f'Request with ID "{ex.request_id}" failed with status '
            f'"{ex.error.code().name}" and includes the following errors:'
        )
        for error in ex.failure.errors:
            print(f'	Error with message "{error.message}".')
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print(f"\t\tOn field: {field_path_element.field_name}")
        sys.exit(1)
