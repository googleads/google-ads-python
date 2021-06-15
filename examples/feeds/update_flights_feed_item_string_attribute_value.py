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
"""Updates a feed item attribute value in a flights feed.

To create a flights feed, run the remarketing/add_flights_feed.py example.
This example is specific to feeds of type DYNAMIC_FLIGHT. The attribute you are
updating must be present on the feed.

This example is specifically for updating the string attribute of a flights feed
item, but it can also be changed to work with other data types of an attribute
and feed types.

To make this work with other data types, replace `string_value` with the type of
an attribute you wish to update, when creating a FeedItemAttributeValue instance
in this example. To make this work with other feed types, replace the
FlightPlaceholderField enum with the equivalent one of your feed type, and
replace Feeds::flightPlaceholderFieldsMapFor() with the method that can return
a similar value for your feed type. Check the flightPlaceholderFieldsMapFor()
method for details.
"""

import argparse
import sys

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.api_core import protobuf_helpers


# [START update_flights_feed_item_string_attribute_value]
def main(
    client,
    customer_id,
    feed_id,
    feed_item_id,
    flight_placeholder_field_name,
    attribute_value,
):
    """The main method that creates all necessary entities for the example.

    Args:
        client: an initialized GoogleAdsClient instance
        customer_id: a client customer ID
        feed_id: the ID of feed containing the feed item to be updated
        feed_item_id: The ID of the feed item to be updated
        flight_placeholder_field_name: the flight placeholder field name for
            the attribute to be updated
        attribute_value: the new value to set the feed attribute to
    """
    feed_service = client.get_service("FeedService")
    # Gets a map of the placeholder values to feed attributes.
    placeholders_to_feed_attribute_map = _flight_placeholder_fields_map(
        client, customer_id, feed_service.feed_path(customer_id, feed_id)
    )
    # Gets the ID of the feed attribute for the placeholder field. This is
    # needed to specify which feed item attribute value will be updated in
    # the given feed item.
    flight_placeholder_field_enum = client.get_type(
        "FlightPlaceholderFieldEnum"
    ).FlightPlaceholderField
    flight_placeholder_enum_value = getattr(
        flight_placeholder_field_enum, flight_placeholder_field_name
    )
    attribute_id = placeholders_to_feed_attribute_map[
        flight_placeholder_enum_value
    ].id

    # Creates the updated feed item attribute value.
    updated_feed_item_attribute_value = client.get_type(
        "FeedItemAttributeValue"
    )
    updated_feed_item_attribute_value.feed_attribute_id = attribute_id
    updated_feed_item_attribute_value.string_value = attribute_value

    # Retrieves the feed item and its associated attributes based on the
    # resource name.
    feed_item_service = client.get_service("FeedItemService")
    feed_item = _get_feed_item(
        client,
        customer_id,
        feed_item_service.feed_item_path(customer_id, feed_id, feed_item_id),
    )

    # Gets the index of the attribute value that will be updated in the
    # feed item.
    attribute_index = _get_attribute_index(
        updated_feed_item_attribute_value, feed_item
    )
    # Any feed item attribute values that are not included in the updated
    # feed item will be removed from the feed item, which is why you must
    # create the feed item from the existing feed item and its attribute
    # values. Then, update only the attribute that you want.
    feed_item_operation = client.get_type("FeedItemOperation")
    client.copy_from(feed_item_operation.update, feed_item)
    updated_feed_item = feed_item_operation.update
    client.copy_from(
        updated_feed_item.attribute_values[attribute_index],
        updated_feed_item_attribute_value,
    )

    # Create a field mask using the old feed_item and the updated_feed_item.
    client.copy_from(
        feed_item_operation.update_mask,
        protobuf_helpers.field_mask(feed_item._pb, updated_feed_item._pb),
    )

    # Create a field mask using the old feed_item and the updated_feed_item.
    feed_item_operation.update_mask.CopyFrom(
        protobuf_helpers.field_mask(feed_item._pb, updated_feed_item._pb)
    )

    response = feed_item_service.mutate_feed_items(
        customer_id=customer_id, operations=[feed_item_operation]
    )
    print(
        "Feed item with resource name: "
        f"'{response.results[0].resource_name}' was updated."
    )
    # [END update_flights_feed_item_string_attribute_value]


def _flight_placeholder_fields_map(client, customer_id, feed_resource_name):
    """Maps place holder fields and feed attributes for a flights feed.

    See FlightPlaceholderField.php for all available placeholder field values.

    Args:
        client: an initialized GoogleAdsClient instance
        customer_id: a client customer ID
        feed_resource_name: a resource name for a Feed

    Returns:
        a dict mapping placeholder fields to feed attributes
    """
    flight_placeholder_field_enum = client.get_type(
        "FlightPlaceholderFieldEnum"
    ).FlightPlaceholderField

    return _placeholder_field_maps(
        client,
        customer_id,
        feed_resource_name,
        {
            "Flight Description": flight_placeholder_field_enum.FLIGHT_DESCRIPTION,
            "Destination ID": flight_placeholder_field_enum.DESTINATION_ID,
            "Flight Price": flight_placeholder_field_enum.FLIGHT_PRICE,
            "Flight Sale Price": flight_placeholder_field_enum.FLIGHT_SALE_PRICE,
            "Final URLs": flight_placeholder_field_enum.FINAL_URLS,
        },
    )


def _placeholder_field_maps(
    client, customer_id, feed_resource_name, feed_attribute_names_map
):
    """Retrieves the placeholder fields to feed attributes map for a feed.

    The initial query retrieves the feed attributes, or columns, of the feed.
    Each feed attribute will also include the feed attribute ID, which will be
    used in a subsequent step.

    Then a map is created for the feed attributes (columns) and returned:
      - The keys are the placeholder types that the columns will be.
      - The values are the feed attributes.

    Args:
        client: an initialized GoogleAdsClient instance
        customer_id: a client customer ID
        feed_resource_name: a resource name for a Feed
        feed_attribute_names_map: the associative array mapping from feed
            attribute names to placeholder fields

    Returns:
        a dict mapping placeholder fields to feed attributes
    """
    googleads_service = client.get_service("GoogleAdsService")
    # Constructs the query to get the feed attributes for the specified feed
    # resource name.
    query = f"""
        SELECT
          feed.attributes
        FROM feed
        WHERE feed.resource_name = '{feed_resource_name}'"""
    # Issues a search request. The page_size is set to 1 because we're only
    # requesting a single result.
    search_request = client.get_type("SearchGoogleAdsRequest")
    search_request.customer_id = customer_id
    search_request.query = query
    search_request.page_size = 1

    response = googleads_service.search(request=search_request)
    row = list(response)[0]
    # Gets the attributes list from the feed and creates a map with keys of
    # placeholder fields and values of feed attributes.
    feed_attributes = row.feed.attributes
    # Creates map with keys of placeholder fields and values of feed
    # attributes.
    return {
        feed_attribute_names_map[feed_attribute.name]: feed_attribute
        for feed_attribute in feed_attributes
    }


def _get_feed_item(client, customer_id, feed_item_resource_name):
    """Retrieves a feed item and its attribute values given a resource name.

    Args:
        client: an initialized GoogleAdsClient instance
        customer_id: a client customer ID
        feed_resource_name: a resource name for a FeedItem

    Returns:
        a FeedItem instance
    """
    googleads_service = client.get_service("GoogleAdsService")
    # Constructs the query to get the feed item with attribute values.
    query = f"""
        SELECT
          feed_item.attribute_values
        FROM feed_item
        WHERE feed_item.resource_name = '{feed_item_resource_name}'"""

    search_request = client.get_type("SearchGoogleAdsRequest")
    search_request.customer_id = customer_id
    search_request.query = query
    search_request.page_size = 1
    response = googleads_service.search(request=search_request)

    # Returns the feed item attribute values, which belongs to the first item.
    # We can ensure it belongs to the first one because we specified the feed
    # item resource name in the query.
    return list(response)[0].feed_item


def _get_attribute_index(target_feed_item_attribute_value, feed_item):
    """Gets the index of the target feed item attribute value.

    This is needed to specify which feed item attribute value will be updated
    in the given feed item.

    Args:
        target_feed_item_attribute_value: the new feed item attribute value that
            will be updated
        feed_item: the feed item that will be updated. It should be populated
            with the current attribute values

    Returns:
        the index number of the attribute
    """
    attribute_index = -1

    # Loops through attribute values to find the index of the feed item
    # attribute value to update.
    for feed_item_attribute_value in feed_item.attribute_values:
        attribute_index += 1
        # Checks if the current feedItemAttributeValue is the one we are
        # updating.
        if (
            feed_item_attribute_value.feed_attribute_id
            == target_feed_item_attribute_value.feed_attribute_id
        ):
            break

    if attribute_index == -1:
        raise ValueError(
            "No matching feed attribute for feed item attribute "
            f"ID: {feed_item_attribute_value.feed_attribute_id}"
        )

    return attribute_index


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v8")

    parser = argparse.ArgumentParser(
        description="Updates a feed item attribute value in a flights feed."
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
        help="The ID of feed containing the feed item to be updated.",
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
        help=(
            "The flight placeholder field name for the attribute to be "
            "updated.",
        ),
    )
    parser.add_argument(
        "-a",
        "--attribute_value",
        type=str,
        required=True,
        help="The new value to set the feed attribute to.",
    )
    args = parser.parse_args()

    try:
        main(
            googleads_client,
            args.customer_id,
            args.feed_id,
            args.feed_item_id,
            args.flight_placeholder_field_name,
            args.attribute_value,
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
