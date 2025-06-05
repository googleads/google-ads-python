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
from typing import Dict, Mapping, Any

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.ads.googleads.v20.enums.types import (
    flight_placeholder_field as flight_placeholder_field_enum_type,
)
from google.ads.googleads.v20.resources.types import (
    feed as feed_type,
    feed_item as feed_item_type,
)
from google.ads.googleads.v20.services.types import (
    feed_service as feed_service_type,
    feed_item_service as feed_item_service_type,
    google_ads_service as google_ads_service_type,
)
from google.ads.googleads.v20.common.types import (
    feed_item as feed_item_common_type,
)
from google.ads.googleads.v20.services.types import (
    feed_item_operation as feed_item_operation_type,
)

from google.api_core import protobuf_helpers


# [START update_flights_feed_item_string_attribute_value]
def main(
    client: GoogleAdsClient,
    customer_id: str,
    feed_id: str,
    feed_item_id: str,
    flight_placeholder_field_name: str,
    attribute_value: str,
) -> None:
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
    feed_service: feed_service_type.FeedServiceClient = client.get_service(
        "FeedService"
    )
    # Gets a map of the placeholder values to feed attributes.
    placeholders_to_feed_attribute_map: Mapping[
        flight_placeholder_field_enum_type.FlightPlaceholderFieldEnum,
        feed_type.FeedAttribute,
    ] = flight_placeholder_fields_map(
        client, customer_id, feed_service.feed_path(customer_id, feed_id)
    )
    # Gets the ID of the feed attribute for the placeholder field. This is
    # needed to specify which feed item attribute value will be updated in
    # the given feed item.
    flight_placeholder_field_enum: Any = client.enums.FlightPlaceholderFieldEnum
    flight_placeholder_enum_value: flight_placeholder_field_enum_type.FlightPlaceholderFieldEnum = getattr(
        flight_placeholder_field_enum, flight_placeholder_field_name
    )
    attribute_id: int = placeholders_to_feed_attribute_map[
        flight_placeholder_enum_value
    ].id

    # Creates the updated feed item attribute value.
    updated_feed_item_attribute_value: feed_item_common_type.FeedItemAttributeValue = client.get_type(
        "FeedItemAttributeValue"
    )
    updated_feed_item_attribute_value.feed_attribute_id = attribute_id
    updated_feed_item_attribute_value.string_value = attribute_value

    # Retrieves the feed item and its associated attributes based on the
    # resource name.
    feed_item_service: feed_item_service_type.FeedItemServiceClient = client.get_service(
        "FeedItemService"
    )
    feed_item: feed_item_type.FeedItem = get_feed_item(
        client,
        customer_id,
        feed_item_service.feed_item_path(customer_id, feed_id, feed_item_id),
    )

    # Gets the index of the attribute value that will be updated in the
    # feed item.
    attribute_index: int = get_attribute_index(
        updated_feed_item_attribute_value, feed_item
    )
    # Any feed item attribute values that are not included in the updated
    # feed item will be removed from the feed item, which is why you must
    # create the feed item from the existing feed item and its attribute
    # values. Then, update only the attribute that you want.
    feed_item_operation: feed_item_operation_type.FeedItemOperation = client.get_type(
        "FeedItemOperation"
    )
    client.copy_from(feed_item_operation.update, feed_item)
    updated_feed_item: feed_item_type.FeedItem = feed_item_operation.update
    client.copy_from(
        updated_feed_item.attribute_values[attribute_index],
        updated_feed_item_attribute_value,
    )

    # Create a field mask using the old feed_item and the updated_feed_item.
    client.copy_from(
        feed_item_operation.update_mask,
        protobuf_helpers.field_mask(feed_item._pb, updated_feed_item._pb),
    )

    response: feed_item_service_type.MutateFeedItemsResponse = feed_item_service.mutate_feed_items(
        customer_id=customer_id, operations=[feed_item_operation]
    )
    print(
        "Feed item with resource name: "
        f"'{response.results[0].resource_name}' was updated."
    )
    # [END update_flights_feed_item_string_attribute_value]


def flight_placeholder_fields_map(
    client: GoogleAdsClient, customer_id: str, feed_resource_name: str
) -> Mapping[
    flight_placeholder_field_enum_type.FlightPlaceholderFieldEnum,
    feed_type.FeedAttribute,
]:
    """Maps place holder fields and feed attributes for a flights feed.

    See FlightPlaceholderField.php for all available placeholder field values.

    Args:
        client: an initialized GoogleAdsClient instance
        customer_id: a client customer ID
        feed_resource_name: a resource name for a Feed

    Returns:
        a dict mapping placeholder fields to feed attributes
    """
    flight_placeholder_field_enum: Any = client.enums.FlightPlaceholderFieldEnum

    return placeholder_field_maps(
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


def placeholder_field_maps(
    client: GoogleAdsClient,
    customer_id: str,
    feed_resource_name: str,
    feed_attribute_names_map: Mapping[
        str, flight_placeholder_field_enum_type.FlightPlaceholderFieldEnum
    ],
) -> Mapping[
    flight_placeholder_field_enum_type.FlightPlaceholderFieldEnum,
    feed_type.FeedAttribute,
]:
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
    googleads_service: google_ads_service_type.GoogleAdsServiceClient = client.get_service(
        "GoogleAdsService"
    )
    # Constructs the query to get the feed attributes for the specified feed
    # resource name.
    query: str = f"""
        SELECT
          feed.attributes
        FROM feed
        WHERE feed.resource_name = '{feed_resource_name}'"""
    search_request: google_ads_service_type.SearchGoogleAdsRequest = client.get_type(
        "SearchGoogleAdsRequest"
    )
    search_request.customer_id = customer_id
    search_request.query = query

    response: google_ads_service_type.SearchGoogleAdsResponse = googleads_service.search(
        request=search_request
    )
    row: google_ads_service_type.GoogleAdsRow = list(response)[0]
    # Gets the attributes list from the feed and creates a map with keys of
    # placeholder fields and values of feed attributes.
    feed_attributes: "list[feed_type.FeedAttribute]" = row.feed.attributes
    # Creates map with keys of placeholder fields and values of feed
    # attributes.
    return {
        feed_attribute_names_map[feed_attribute.name]: feed_attribute
        for feed_attribute in feed_attributes
    }


def get_feed_item(
    client: GoogleAdsClient, customer_id: str, feed_item_resource_name: str
) -> feed_item_type.FeedItem:
    """Retrieves a feed item and its attribute values given a resource name.

    Args:
        client: an initialized GoogleAdsClient instance
        customer_id: a client customer ID
        feed_resource_name: a resource name for a FeedItem

    Returns:
        a FeedItem instance
    """
    googleads_service: google_ads_service_type.GoogleAdsServiceClient = client.get_service(
        "GoogleAdsService"
    )
    # Constructs the query to get the feed item with attribute values.
    query: str = f"""
        SELECT
          feed_item.attribute_values
        FROM feed_item
        WHERE feed_item.resource_name = '{feed_item_resource_name}'"""

    search_request: google_ads_service_type.SearchGoogleAdsRequest = client.get_type(
        "SearchGoogleAdsRequest"
    )
    search_request.customer_id = customer_id
    search_request.query = query
    response: google_ads_service_type.SearchGoogleAdsResponse = googleads_service.search(
        request=search_request
    )

    # Returns the feed item attribute values, which belongs to the first item.
    # We can ensure it belongs to the first one because we specified the feed
    # item resource name in the query.
    return list(response)[0].feed_item


def get_attribute_index(
    target_feed_item_attribute_value: feed_item_common_type.FeedItemAttributeValue,
    feed_item: feed_item_type.FeedItem,
) -> int:
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
    attribute_index: int = -1

    # Loops through attribute values to find the index of the feed item
    # attribute value to update.
    for i, feed_item_attribute_value in enumerate(feed_item.attribute_values):
        # Checks if the current feedItemAttributeValue is the one we are
        # updating.
        if (
            feed_item_attribute_value.feed_attribute_id
            == target_feed_item_attribute_value.feed_attribute_id
        ):
            attribute_index = i
            break

    if attribute_index == -1:
        # This condition should not be met if the feed attribute ID is valid.
        # If it's met, it means target_feed_item_attribute_value was not found
        # in feed_item.attribute_values. In this case, we raise an error.
        # The original code had a subtle bug here: if the loop completed without
        # finding the attribute, feed_item_attribute_value would be the last
        # element from the loop, not the one we were searching for.
        raise ValueError(
            "No matching feed attribute for feed item attribute "
            f"ID: {target_feed_item_attribute_value.feed_attribute_id}"
        )

    return attribute_index


if __name__ == "__main__":
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
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
    args: argparse.Namespace = parser.parse_args()

    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client: GoogleAdsClient = GoogleAdsClient.load_from_storage(
        version="v20"
    )

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
            print(f'\tError with message "{error.message}".')
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print(f"\t\tOn field: {field_path_element.field_name}")
        sys.exit(1)
