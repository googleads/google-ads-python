#!/usr/bin/env python
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License")
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
"""Demonstrates how to add Affiliate Location extensions.

This example adds a feed that syncs retail addresses for a given retail chain ID
and associates the feed with a campaign for serving affiliate location
extensions.
"""


import argparse
import sys
from time import sleep
from uuid import uuid4

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

# The maximum number of attempts to retrieve the FeedMappings before throwing an
# exception.
MAX_FEEDMAPPING_RETRIEVAL_ATTEMPTS = 10


def main(client, customer_id, chain_id, campaign_id):
    """Demonstrates how to add Affiliate Location extensions.

    Args:
        client: An initialized instance.
        customer_id: The client customer ID.
        chain_id: The retail chain ID. See:
            https://developers.google.com/google-ads/api/reference/data/codes-formats#chain-ids
            for a complete list of valid retail chain IDs.
        campaign_id: The campaign ID for which the affiliate location extensions
            will be added.
    """
    feed_resource_name = _create_affiliate_location_extension_feed(
        client, customer_id, chain_id
    )
    # After the completion of the feed creation operation above, the added
    # feed will not be available for usage in a campaign feed until the feed
    # mappings are created. We will wait with an exponential back-off policy
    # until the feed mappings have been created.
    feed_mapping = _wait_for_feed_to_be_ready(
        client, customer_id, feed_resource_name
    )
    _create_campaign_feed(
        client,
        customer_id,
        campaign_id,
        feed_mapping,
        feed_resource_name,
        chain_id,
    )


# [START add_affiliate_location_extensions]
def _create_affiliate_location_extension_feed(client, customer_id, chain_id):
    """Creates the Affiliate Location Extension feed.

    Args:
        client: The Google Ads API client.
        customer_id: The Google Ads customer ID.
        chain_id: The retail chain ID.

    Returns:
        The string resource name of the newly created Affiliate Location
        Extension feed.
    """
    # Optional: Remove all existing location extension feeds. This is an
    # optional step, and is required for this code example to run correctly more
    # than once.
    # This is because Google Ads only allows one location extension feed per
    # email address, and a Google Ads account cannot have a location extension
    # feed and an affiliate location extension feed at the same time.
    _remove_location_extension_feeds(client, customer_id)

    # Get the FeedServiceClient.
    feed_service = client.get_service("FeedService")

    # Create a feed that will sync to retail addresses for a given retail chain
    # ID. Do not add FeedAttributes to this object as Google Ads will add
    # them automatically as this will be a system generated feed.
    feed_operation = client.get_type("FeedOperation")
    feed = feed_operation.create
    feed.name = f"Affiliate Location Extension feed #{uuid4()}"
    feed.affiliate_location_feed_data.chain_ids.append(chain_id)
    feed.affiliate_location_feed_data.relationship_type = client.get_type(
        "AffiliateLocationFeedRelationshipTypeEnum"
    ).AffiliateLocationFeedRelationshipType.GENERAL_RETAILER
    # Since this feed's contents will be managed by Google, you must set its
    # origin to GOOGLE.
    feed.origin = client.get_type("FeedOriginEnum").FeedOrigin.GOOGLE

    # Add the feed.
    mutate_feeds_response = feed_service.mutate_feeds(
        customer_id=customer_id, operations=[feed_operation]
    )

    # Display the results.
    feed_resource_name = mutate_feeds_response.results[0].resource_name
    print(
        "Affliate location extension feed created with resource name: "
        f"{feed_resource_name}."
    )
    return feed_resource_name
    # [END add_affiliate_location_extensions]


def _remove_location_extension_feeds(client, customer_id):
    """Removes the old location extension feeds.

    Args:
        client: The Google Ads API client.
        customer_id: The Google Ads customer ID.
    """
    # To remove a location extension feed, you need to:
    # 1. Remove the CustomerFeed so that the location extensions from the feed
    # stop serving.
    # 2. Remove the feed so that Google Ads will no longer sync from the GMB
    # account.
    # Optional: You may also want to remove the CampaignFeeds and AdGroupFeeds.
    old_customer_feeds = _get_location_extension_customer_feeds(
        client, customer_id
    )

    if old_customer_feeds:
        _remove_customer_feeds(client, customer_id, old_customer_feeds)

    feeds = _get_location_extension_feeds(client, customer_id)

    if feeds:
        _remove_feeds(client, customer_id, feeds)


def _get_location_extension_feeds(client, customer_id):
    """Gets the location extension feeds.

    Args:
        client: The Google Ads API client.
        customer_id: The Google Ads customer ID.
    Returns:
        The list of location extension feeds.
    """
    googleads_service = client.get_service("GoogleAdsService")

    # Create the query.
    query = """
        SELECT
          feed.resource_name,
          feed.status,
          feed.places_location_feed_data.email_address,
          feed.affiliate_location_feed_data.chain_ids
        FROM feed
        WHERE feed.status = ENABLED"""

    search_results = googleads_service.search(
        customer_id=customer_id, query=query
    )

    # A location extension feed can be identified by checking whether the
    # PlacesLocationFeedData field is set (Location extensions feeds) or
    # AffiliateLocationFeedData field is set (Affiliate location extension
    # feeds)
    return [
        row.feed
        for row in search_results
        if row.feed.places_location_feed_data
        or row.feed.affiliate_location_feed_data
    ]


def _remove_feeds(client, customer_id, feeds):
    """Removes the feeds.

    Args:
        client: The Google Ads API client.
        customer_id: The Google Ads customer ID.
        feeds: The list of feeds to remove.
    """
    operations = []

    for feed in feeds:
        operation = client.get_type("FeedOperation")
        operation.remove = feed.resource_name
        operations.append(operation)

    feed_service = client.get_service("FeedService")
    feed_service.mutate_feeds(customer_id=customer_id, operations=operations)


def _get_location_extension_customer_feeds(client, customer_id):
    """Gets the location extension customer feeds.

    Args:
        client: The Google Ads API client.
        customer_id: The customer ID from which to fetch feeds.
    Returns:
        A list of location extension customer feeds.

    """
    googleads_service = client.get_service("GoogleAdsService")

    # Create the query. A location extension customer feed can be identified by
    # filtering for placeholder_types=LOCATION (location extension feeds) or
    # placeholder_types =AFFILIATE_LOCATION (affiliate location extension feeds)
    query = """
        SELECT
          customer_feed.resource_name,
          customer_feed.feed,
          customer_feed.status,
          customer_feed.matching_function.function_string
        FROM customer_feed
        WHERE
          customer_feed.placeholder_types CONTAINS ANY(LOCATION, AFFILIATE_LOCATION)
          AND customer_feed.status=ENABLED"""

    search_results = googleads_service.search(
        customer_id=customer_id, query=query
    )

    return [row.customer_feed for row in search_results]


def _remove_customer_feeds(client, customer_id, customer_feeds):
    """Removes the customer feeds.

    Args:
        client: The Google Ads API client.
        customer_id: The Google Ads customer ID.
        customer_feeds: The customer feeds to remove.
    """
    operations = []

    for customer_feed in customer_feeds:
        operation = client.get_type("CustomerFeedOperation")
        operation.remove = customer_feed.resource_name
        operations.append(operation)

    customer_feed_service = client.get_service("CustomerFeedService")
    customer_feed_service.mutate_customer_feeds(
        customer_id=customer_id, operations=operations
    )


# [START add_affiliate_location_extensions_1]
def _get_affiliate_location_extension_feed_mapping(
    client, customer_id, feed_resource_name
):
    """Gets the Affiliate Location Extension feed mapping.

    Args:
        client: The Google Ads API client.
        customer_id: The Google Ads customer ID.
        feed_resource_name: The feed resource name.
    Returns:
        The newly created feed mapping.
    """
    # Get the GoogleAdsService.
    googleads_service = client.get_service("GoogleAdsService")

    # Create the query.
    query = f"""
        SELECT
          feed_mapping.resource_name,
          feed_mapping.attribute_field_mappings,
          feed_mapping.status
        FROM feed_mapping
        WHERE
          feed_mapping.feed = '{feed_resource_name}'
          AND feed_mapping.status = ENABLED
          AND feed_mapping.placeholder_type = AFFILIATE_LOCATION
        LIMIT 1"""

    # Issue a search request.
    search_results = googleads_service.search(
        customer_id=customer_id, query=query
    )

    # Return the feed mapping that results from the search.
    # It is possible that the feed is not yet ready, so we catch the exception
    # if the feed mapping is not yet available.
    try:
        row = next(iter(search_results))
    except StopIteration:
        return None
    else:
        return row.feed_mapping
        # [END add_affiliate_location_extensions_1]


# [START add_affiliate_location_extensions_2]
def _wait_for_feed_to_be_ready(client, customer_id, feed_resource_name):
    """Waits for the Affliate location extension feed to be ready.

    Args:
        client: The Google Ads API client.
        customer_id: The Google Ads customer ID.
        feed_resource_name: The resource name of the feed.

    Returns:
        The newly created FeedMapping.

    Raises:
        Exception: if the feed is not ready after the specified number of
            retries.
    """
    num_attempts = 0
    sleep_seconds = 0

    while num_attempts < MAX_FEEDMAPPING_RETRIEVAL_ATTEMPTS:
        # Once you create a feed, Google's servers will setup the feed by
        # creating feed attributes and feed mapping. Once the feed mapping is
        # created, it is ready to be used for creating customer feed.
        # This process is asynchronous, so we wait until the feed mapping is
        # created, peforming exponential backoff.
        feed_mapping = _get_affiliate_location_extension_feed_mapping(
            client, customer_id, feed_resource_name
        )

        if feed_mapping is None:
            num_attempts += 1
            sleep_seconds = 5 * 2 ** num_attempts
            print(
                f"Checked {num_attempts} time(s). Feed is not ready "
                f"yet. Waiting {sleep_seconds} seconds before trying again."
            )
            sleep(sleep_seconds)
        else:
            print(f"Feed {feed_resource_name} is now ready.")
            return feed_mapping

    raise Exception(
        f"Feed is not ready after "
        f"{MAX_FEEDMAPPING_RETRIEVAL_ATTEMPTS} retries."
    )
    # [END add_affiliate_location_extensions_2]


# [START add_affiliate_location_extensions_3]
def _create_campaign_feed(
    client, customer_id, campaign_id, feed_mapping, feed_resource_name, chain_id
):
    """Creates the campaign feed.

    Args:
        client: The Google Ads API client.
        customer_id: The Google Ads customer ID.
        campaign_id: The campaign ID to which the affiliate location extensions
            will be added.
        feed_mapping: The affliate location extension feedmapping for the feed
            resource name.
        feed_resource_name: The feed resource name.
        chain_id: The retail chain ID.
    """
    # Get the CampaignFeedService.
    campaign_feed_service = client.get_service("CampaignFeedService")
    feed_service = client.get_service("FeedService", versions="v6")

    attribute_id_for_chain_id = _get_attribute_id_for_chain_id(
        client, feed_mapping
    )
    feed_id = feed_service.parse_feed_path(feed_resource_name)["feed_id"]

    matching_function = (
        f"IN(FeedAttribute[{feed_id}, {attribute_id_for_chain_id}], {chain_id})"
    )

    # Add a CampaignFeed that associates the feed with this campaign for
    # the AFFILIATE_LOCATION placeholder type.
    campaign_feed_operation = client.get_type("CampaignFeedOperation")
    campaign_feed = campaign_feed_operation.create
    campaign_feed.feed = feed_resource_name
    campaign_feed.placeholder_types.append(
        client.get_type(
            "PlaceholderTypeEnum"
        ).PlaceholderType.AFFILIATE_LOCATION
    )
    campaign_feed.matching_function.function_string = matching_function
    campaign_feed.campaign = client.get_service(
        "CampaignService"
    ).campaign_path(customer_id, campaign_id)

    mutate_campaign_feeds_response = (
        campaign_feed_service.mutate_campaign_feeds(
            customer_id=customer_id, operations=[campaign_feed_operation]
        )
    )

    # Display the result.
    print(
        "Campaign feed created with resource name: "
        f"{mutate_campaign_feeds_response.results[0].resource_name}."
    )
    # [END add_affiliate_location_extensions_3]


# [START add_affiliate_location_extensions_4]
def _get_attribute_id_for_chain_id(client, feed_mapping):
    """Gets the feed attribute ID for the retail chain ID.

    Args:
        client: The Google Ads API client.
        feed_mapping: The FeedMapping in which to search.
    Returns:
        The feed attribute ID.
    Raises:
        Exception: If no AffiliateLocationField with a retail chain ID is found
            in the FeedMapping.
    """
    for field_mapping in feed_mapping.attribute_field_mappings:
        if (
            field_mapping.affiliate_location_field
            == client.get_type(
                "AffiliateLocationPlaceholderFieldEnum"
            ).AffiliateLocationPlaceholderField.CHAIN_ID
        ):
            return field_mapping.feed_attribute_id

    raise Exception(
        "No AffiliateLocationField with a retail chain ID was "
        "found in the FeedMapping."
    )
    # [END add_affiliate_location_extensions_4]


if __name__ == "__main__":
    # will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v8")

    parser = argparse.ArgumentParser(
        description="Demonstrates how to add Affiliate Location extensions."
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
        "--chain_id",
        type=int,
        required=True,
        help="The retail chain ID. See: "
        "https://developers.google.com/google-ads/api/reference/data/codes-formats#chain-ids "
        "for a complete list of valid retail chain IDs.",
    )
    parser.add_argument(
        "-i",
        "--campaign_id",
        type=int,
        required=True,
        help="The campaign ID for which the affiliate location extensions will "
        "be added.",
    )
    args = parser.parse_args()

    try:
        main(
            googleads_client,
            args.customer_id,
            args.chain_id,
            args.campaign_id,
        )
    except GoogleAdsException as ex:
        print(
            f"Request with ID '{ex.request_id}'' failed with status "
            f"'{ex.error.code().name}' and includes the following errors:"
        )
        for error in ex.failure.errors:
            print(f"\tError with message '{error.message}'.")
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print(f"\t\tOn field: {field_path_element.field_name}")
        sys.exit(1)
