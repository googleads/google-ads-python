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
"""Adds sitelinks to a campaign using feed services.

Run add_campaigns.py to create a campaign.
"""

import argparse
import sys
import uuid

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


def main(client, customer_id, campaign_id, ad_group_id):
    """Adds sitelinks to a campaign using feed services.

    Args:
        client: The Google Ads client.
        customer_id: The customer ID for which to add the keyword.
        campaign_id: The campaign to which sitelinks will be added.
        ad_group_id: ID of the ad group to which sitelinks will be added. Set
            to None if you do not wish to limit targeting to a specific ad
            group.
    """
    # Create a feed, which acts as a table to store data.
    feed = _create_feed(client, customer_id)

    # Create feed items, which fill out the feed table with data.
    feed_items = _create_feed_items(client, customer_id, feed)

    # Create a feed mapping, which tells Google Ads how to interpret this
    # data to display additional sitelink information on ads.
    _create_feed_mapping(client, customer_id, feed)

    # Create a campaign feed, which tells Google Ads which campaigns to
    # use the provided data with.
    _create_campaign_feed(client, customer_id, campaign_id, feed)

    # If an ad group is specified, limit targeting only to the given ad
    # group. You must set targeting on a per-feed-item basis. This will
    # restrict the first feed item we added to only serve for the given
    # ad group.
    if ad_group_id is not None:
        _create_ad_group_targeting(
            client, customer_id, ad_group_id, feed_items[0]
        )


def _create_feed(client, customer_id):
    """Creates a feed, which acts as a table to store data.

    Args:
        client: The Google Ads client.
        customer_id: The customer ID for which the call is made.

    Returns:
        The newly created feed.
    """
    feed_service = client.get_service("FeedService")
    googleads_service = client.get_service("GoogleAdsService")

    feed_operation = client.get_type("FeedOperation")
    feed = feed_operation.create
    feed.name = f"Sitelinks Feed {uuid.uuid4()}"
    feed.origin = client.get_type("FeedOriginEnum").FeedOrigin.USER
    # Specify the column name and data type. This is just raw data at this
    # point, and not yet linked to any particular purpose. The names are used
    # to help us remember what they are intended for later.
    feed_attribute_type_enum = client.get_type(
        "FeedAttributeTypeEnum"
    ).FeedAttributeType
    feed.attributes.extend(
        [
            _create_feed_attribute(
                client, "Link Text", feed_attribute_type_enum.STRING
            ),
            _create_feed_attribute(
                client, "Link Final URL", feed_attribute_type_enum.URL_LIST
            ),
            _create_feed_attribute(
                client, "Line 1", feed_attribute_type_enum.STRING
            ),
            _create_feed_attribute(
                client, "Line 2", feed_attribute_type_enum.STRING
            ),
        ]
    )

    response = feed_service.mutate_feeds(
        customer_id=customer_id, operations=[feed_operation]
    )
    feed_resource_name = response.results[0].resource_name
    print(f"Created feed with resource name '{feed_resource_name}'.")

    # After we create the feed, we need to fetch it so we can determine the
    # attribute IDs, which will be required when populating feed items.
    search_response = googleads_service.search(
        customer_id=customer_id,
        query=f"""
        SELECT
          feed.attributes
        FROM feed
        WHERE feed.resource_name = '{feed_resource_name}'""",
    )
    return next(iter(search_response)).feed


def _create_feed_attribute(client, name, attribute_type):
    """Helper method to construct a single FeedAttribute.

    Args:
        client: The Google Ads API client instance.
        name: The string attribute name to set on the new attribute.
        attribute_type: The FeedAttributeType to set on the new attribute.

    Returns:
        A new FeedAttribute instance.
    """
    feed_attribute = client.get_type("FeedAttribute")
    feed_attribute.name = name
    feed_attribute.type_ = attribute_type
    return feed_attribute


def _create_feed_items(client, customer_id, feed):
    """Creates feed items, which fill out the feed table with data.

    Args:
        client: The Google Ads client.
        customer_id: The customer ID for which the call is made.
        feed: The feed for which the operation will be created.

    Returns:
        A list of string Feed Item Resource Names.
    """
    feed_item_service = client.get_service("FeedItemService")
    operations = [
        _new_feed_item_operation(
            client,
            feed,
            "Home",
            "http://www.example.com",
            "Home line 1",
            "Home line 2",
        ),
        _new_feed_item_operation(
            client,
            feed,
            "Stores",
            "http://www.example.com/stores",
            "Stores line 1",
            "Stores line 2",
        ),
        _new_feed_item_operation(
            client,
            feed,
            "On Sale",
            "http://www.example.com/sale",
            "On Sale line 1",
            "On Sale line 2",
        ),
        _new_feed_item_operation(
            client,
            feed,
            "Support",
            "http://www.example.com/support",
            "Support line 1",
            "Support line 2",
        ),
        _new_feed_item_operation(
            client,
            feed,
            "Products",
            "http://www.example.com/catalogue",
            "Products line 1",
            "Products line 2",
        ),
        _new_feed_item_operation(
            client,
            feed,
            "About Us",
            "http://www.example.com/about",
            "About Us line 1",
            "About Us line 2",
        ),
    ]

    response = feed_item_service.mutate_feed_items(
        customer_id=customer_id, operations=operations
    )

    # We will need the resource name of each feed item to use in targeting.
    feed_item_resource_names = []

    print("Created the following feed items:")

    for feed_item_result in response.results:
        print(f"\t{feed_item_result.resource_name}")
        feed_item_resource_names.append(feed_item_result.resource_name)

    return feed_item_resource_names


def _new_feed_item_operation(client, feed, text, final_url, line1, line2):
    """Helper method to construct a single FeedAttribute.

    Args:
        client: The Google Ads API client instance.
        feed: The feed for which the operation will be created.
        text: The link text for the feed item.
        final_url: The final URL for the feed item.
        line1: Line 1 of the feed item.
        line2: Line 2 of the feed item.

    Returns:
        The newly created FeedItemOperation instance.
    """
    feed_item_operation = client.get_type("FeedItemOperation")
    feed_item = feed_item_operation.create
    feed_item.feed = feed.resource_name

    for i in range(0, 4):
        attribute_value = client.get_type("FeedItemAttributeValue")
        attribute_value.feed_attribute_id = feed.attributes[i].id

        feed_item.attribute_values.append(attribute_value)

    # The attribute IDs come back in the same order that they were added.
    feed_item.attribute_values[0].string_value = text
    feed_item.attribute_values[1].string_values.append(final_url)
    feed_item.attribute_values[2].string_value = line1
    feed_item.attribute_values[3].string_value = line2

    return feed_item_operation


def _create_feed_mapping(client, customer_id, feed):
    """Creates a feed mapping.

    Feed mappings tell Google Ads how to interpret this data to display
    additional sitelink information on ads.

    Args:
        client: The Google Ads client.
        customer_id: The customer ID for which the call is made.
        feed: The feed for which the operation will be created.
    """
    feed_mapping_service = client.get_service("FeedMappingService")

    feed_mapping_operation = client.get_type("FeedMappingOperation")
    feed_mapping = feed_mapping_operation.create
    feed_mapping.placeholder_type = client.get_type(
        "PlaceholderTypeEnum"
    ).PlaceholderType.SITELINK
    feed_mapping.feed = feed.resource_name

    sitelink_placeholder_field_enum = client.get_type(
        "SitelinkPlaceholderFieldEnum"
    ).SitelinkPlaceholderField
    field_names_map = {
        "Link Text": sitelink_placeholder_field_enum.TEXT,
        "Link Final URL": sitelink_placeholder_field_enum.FINAL_URLS,
        "Line 1": sitelink_placeholder_field_enum.LINE_1,
        "Line 2": sitelink_placeholder_field_enum.LINE_2,
    }

    for feed_attribute in feed.attributes:
        attribute_field_mapping = client.get_type("AttributeFieldMapping")
        attribute_field_mapping.feed_attribute_id = feed_attribute.id

        attribute_field_mapping.sitelink_field = field_names_map[
            feed_attribute.name
        ]

        feed_mapping.attribute_field_mappings.append(attribute_field_mapping)

    response = feed_mapping_service.mutate_feed_mappings(
        customer_id=customer_id, operations=[feed_mapping_operation]
    )
    print(f"Created feed mapping '{response.results[0].resource_name}'.")


def _create_campaign_feed(client, customer_id, campaign_id, feed):
    """Creates a campaign feed.

    Campaign feeds tell Google Ads which campaigns to use the provided data
    with.

    Args:
        client: The Google Ads client.
        customer_id: The customer ID for which the call is made.
        campaign_id: The campaign to receive the feed.
        feed: The feed to connect to the campaign.
    """
    campaign_feed_service = client.get_service("CampaignFeedService")

    # Fetch the feed item IDs and collapse into a single comma-separated string.
    aggregated_feed_item_ids = ",".join(
        [str(attribute.id) for attribute in feed.attributes]
    )

    campaign_feed_operation = client.get_type("CampaignFeedOperation")
    campaign_feed = campaign_feed_operation.create
    campaign_feed.feed = feed.resource_name
    campaign_feed.campaign = client.get_service(
        "CampaignService"
    ).campaign_path(customer_id, campaign_id)
    campaign_feed.matching_function.function_string = (
        f"AND(IN(FEED_ITEM_ID,{{ {aggregated_feed_item_ids} }})"
        ",EQUALS(CONTEXT.DEVICE,'Mobile'))"
    )
    campaign_feed.placeholder_types.append(
        client.get_type("PlaceholderTypeEnum").PlaceholderType.SITELINK
    )

    response = campaign_feed_service.mutate_campaign_feeds(
        customer_id=customer_id, operations=[campaign_feed_operation]
    )
    print(f"Created campaign feed '{response.results[0].resource_name}'.")


def _create_ad_group_targeting(client, customer_id, ad_group_id, feed_item):
    """Targets the feed items to the given ad group.

    Args:
        client: The Google Ads client.
        customer_id: The customer ID for which the call is made.
        ad_group_id: The ID of the Ad Group being targeted.
        feed_item: The feed item that was added to the feed.
    """
    feed_item_target_service = client.get_service("FeedItemTargetService")

    feed_item_target_operation = client.get_type("FeedItemTargetOperation")
    feed_item_target = feed_item_target_operation.create
    feed_item_target.feed_item = feed_item
    feed_item_target.ad_group = client.get_service(
        "AdGroupService"
    ).ad_group_path(customer_id, ad_group_id)

    response = feed_item_target_service.mutate_feed_item_targets(
        customer_id=customer_id, operations=[feed_item_target_operation]
    )
    print(
        f"Created feed item target '{response.results[0].resource_name}' "
        f"for feed item '{feed_item}'."
    )


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v8")

    parser = argparse.ArgumentParser(
        description="Adds sitelinks to a campaign using feed services."
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
        "-i",
        "--campaign_id",
        type=str,
        required=True,
        default=None,
        help="ID of the campaign to which sitelinks will be added.",
    )
    parser.add_argument(
        "-a",
        "--ad_group_id",
        type=str,
        required=False,
        help="The ID of the ad group to which sitelinks will be added.",
    )
    args = parser.parse_args()

    try:
        main(
            googleads_client,
            args.customer_id,
            args.campaign_id,
            args.ad_group_id,
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
