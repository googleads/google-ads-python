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
"""Adds a real estate feed, creates the field mapping, and adds items to feed.
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
    # Creates a new feed, but you can fetch and re-use an existing feed by
    # skipping the _create_feed method and inserting the feed resource name of
    # the existing feed.
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

    # Creates the feed item and adds it to the feed.
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
    """Creates a feed that will be used as a real estate feed.

    Args:
        client: An initialized GoogleAds client.
        customer_id: The Google Ads customer ID.

    Returns:
        A str resource name of the newly created feed.
    """
    feed_service = client.get_service("FeedService")

    # Creates the feed operation.
    feed_operation = client.get_type("FeedOperation")

    # Create the feed with feed attributes defined below.
    feed = feed_operation.create
    feed.name = f"Real Estate Feed #{uuid4()}"

    feed_attribute_type_enum = client.get_type(
        "FeedAttributeTypeEnum"
    ).FeedAttributeType

    # Creates a listing ID attribute.
    listing_id_attribute = client.get_type("FeedAttribute")
    listing_id_attribute.name = "Listing ID"
    listing_id_attribute.type_ = feed_attribute_type_enum.STRING

    # Creates a listing name attribute.
    listing_name_attribute = client.get_type("FeedAttribute")
    listing_name_attribute.name = "Listing Name"
    listing_name_attribute.type_ = feed_attribute_type_enum.STRING

    # Creates a final URLs attribute.
    final_urls_attribute = client.get_type("FeedAttribute")
    final_urls_attribute.name = "Final URLs"
    final_urls_attribute.type_ = feed_attribute_type_enum.URL_LIST

    # Creates an image URL attribute.
    image_url_attribute = client.get_type("FeedAttribute")
    image_url_attribute.name = "Image URL"
    image_url_attribute.type_ = feed_attribute_type_enum.URL

    # Creates a contextual keywords attribute.
    contextual_keywords_attribute = client.get_type("FeedAttribute")
    contextual_keywords_attribute.name = "Contextual Keywords"
    contextual_keywords_attribute.type_ = feed_attribute_type_enum.STRING_LIST

    feed.attributes.extend(
        [
            listing_id_attribute,
            listing_name_attribute,
            final_urls_attribute,
            image_url_attribute,
            contextual_keywords_attribute,
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
    """Creates a feed mapping for a given real estate feed.

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

    # Creates the feed mapping.
    feed_mapping = feed_mapping_operation.create
    feed_mapping.feed = feed_resource_name
    feed_mapping.placeholder_type = client.get_type(
        "PlaceholderTypeEnum"
    ).PlaceholderType.DYNAMIC_REAL_ESTATE

    # Returns a new instance of AttributeFieldMapping when called.
    # This prevents the need to repeat these lines every time we need a new
    # AttributeFieldMapping. Instead, we call attribute_field_mapping()
    attribute_field_mapping = lambda: client.get_type("AttributeFieldMapping")

    # Maps the feed attribute IDs to the placeholder values. The feed attribute
    # ID is the ID of the feed attribute created in the created_feed method.
    # This can be thought of as the generic ID of the column of the new feed.
    # The placeholder value specifies the type of column this is in the context
    # of a real estate feed (e.g. a LISTING_ID or LISTING_NAME). The feed
    # mapping associates the feed column by ID to this type and controls how
    # the feed attributes are presented in dynamic content.
    placeholder_field_enum = client.get_type(
        "RealEstatePlaceholderFieldEnum"
    ).RealEstatePlaceholderField
    listing_id_enum_value = placeholder_field_enum.LISTING_ID
    listing_id_mapping = attribute_field_mapping()
    listing_id_mapping.feed_attribute_id = placeholders_to_feed_attribute_map[
        listing_id_enum_value
    ].id
    listing_id_mapping.real_estate_field = listing_id_enum_value

    listing_name_enum_value = placeholder_field_enum.LISTING_NAME
    listing_name_mapping = attribute_field_mapping()
    listing_name_mapping.feed_attribute_id = placeholders_to_feed_attribute_map[
        listing_name_enum_value
    ].id
    listing_name_mapping.real_estate_field = listing_name_enum_value

    final_urls_enum_value = placeholder_field_enum.FINAL_URLS
    final_urls_mapping = attribute_field_mapping()
    final_urls_mapping.feed_attribute_id = placeholders_to_feed_attribute_map[
        final_urls_enum_value
    ].id
    final_urls_mapping.real_estate_field = final_urls_enum_value

    image_url_enum_value = placeholder_field_enum.IMAGE_URL
    image_url_mapping = attribute_field_mapping()
    image_url_mapping.feed_attribute_id = placeholders_to_feed_attribute_map[
        image_url_enum_value
    ].id
    image_url_mapping.real_estate_field = image_url_enum_value

    contextual_keywords_enum_value = placeholder_field_enum.CONTEXTUAL_KEYWORDS
    contextual_keywords_mapping = attribute_field_mapping()
    contextual_keywords_mapping.feed_attribute_id = placeholders_to_feed_attribute_map[
        contextual_keywords_enum_value
    ].id
    contextual_keywords_mapping.real_estate_field = (
        contextual_keywords_enum_value
    )

    feed_mapping.attribute_field_mappings.extend(
        [
            listing_id_mapping,
            listing_name_mapping,
            final_urls_mapping,
            image_url_mapping,
            contextual_keywords_mapping,
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


# [START add_real_estate_feed_1]
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
        "RealEstatePlaceholderFieldEnum"
    ).RealEstatePlaceholderField

    # Creates the listing ID feed attribute value.
    listing_id_enum_value = placeholder_field_enum.LISTING_ID
    listing_id_mapping = client.get_type("FeedItemAttributeValue")
    listing_id_mapping.feed_attribute_id = placeholders_to_feed_attribute_map[
        listing_id_enum_value
    ].id
    listing_id_mapping.string_value = "ABC123DEF"

    # Creates the listing name feed attribute value.
    listing_name_enum_value = placeholder_field_enum.LISTING_NAME
    listing_name_mapping = client.get_type("FeedItemAttributeValue")
    listing_name_mapping.feed_attribute_id = placeholders_to_feed_attribute_map[
        listing_name_enum_value
    ].id
    listing_name_mapping.string_value = "Two bedroom with magnificent views"

    # Creates the final URLs feed attribute value.
    final_urls_enum_value = placeholder_field_enum.FINAL_URLS
    final_urls_mapping = client.get_type("FeedItemAttributeValue")
    final_urls_mapping.feed_attribute_id = placeholders_to_feed_attribute_map[
        final_urls_enum_value
    ].id
    final_urls_mapping.string_values.append("http://www.example.com/listings/")

    # Creates the image URL feed attribute value.
    image_url_enum_value = placeholder_field_enum.IMAGE_URL
    image_url_mapping = client.get_type("FeedItemAttributeValue")
    image_url_mapping.feed_attribute_id = placeholders_to_feed_attribute_map[
        image_url_enum_value
    ].id
    image_url_mapping.string_value = (
        "http://www.example.com/listings/images?listing_id=ABC123DEF"
    )

    # Creates the contextual keywords feed attribute value.
    contextual_keywords_enum_value = placeholder_field_enum.CONTEXTUAL_KEYWORDS
    contextual_keywords_mapping = client.get_type("FeedItemAttributeValue")
    contextual_keywords_mapping.feed_attribute_id = placeholders_to_feed_attribute_map[
        contextual_keywords_enum_value
    ].id
    contextual_keywords_mapping.string_values.extend(
        ["beach community", "ocean view", "two bedroom"]
    )

    feed_item.attribute_values.extend(
        [
            listing_id_mapping,
            listing_name_mapping,
            final_urls_mapping,
            image_url_mapping,
            contextual_keywords_mapping,
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
    # [END add_real_estate_feed_1]


# [START add_real_estate_feed]
def _get_placeholder_fields_map(client, customer_id, feed_resource_name):
    """Get mapping of placeholder fields to feed attributes.

    Note that this is only intended to produce a mapping for real estate feeds.

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

        real_estate_placeholder_field_enum = client.get_type(
            "RealEstatePlaceholderFieldEnum"
        ).RealEstatePlaceholderField
        feed_attribute_names_map = {
            "Listing ID": real_estate_placeholder_field_enum.LISTING_ID,
            "Listing Name": real_estate_placeholder_field_enum.LISTING_NAME,
            "Final URLs": real_estate_placeholder_field_enum.FINAL_URLS,
            "Image URL": real_estate_placeholder_field_enum.IMAGE_URL,
            "Contextual Keywords": real_estate_placeholder_field_enum.CONTEXTUAL_KEYWORDS,
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
    # [END add_real_estate_feed]


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v8")

    parser = argparse.ArgumentParser(
        description="Adds a real estate feed for specified customer."
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
