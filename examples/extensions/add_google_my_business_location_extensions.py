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
"""Adds a feed that syncs feed items from a Google My Business (GMB) account.

The feed will also be associated with a customer.
"""


import argparse
import sys
import time
from uuid import uuid4

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

MAX_CUSTOMER_FEED_ADD_ATTEMPTS = 9
DEFAULT_OAUTH2_SCOPE = "https://www.googleapis.com/auth/adwords"


def main(
    client,
    customer_id,
    gmb_email_address,
    business_account_id,
    gmb_access_token,
):
    """Adds a feed that syncs feed items from a Google My Business (GMB) account.

    The feed will also be associated with a customer.

    Args:
        client: An initialized GoogleAdsClient instance.
        customer_id: The Google Ads customer ID.
        gmb_email_address: The email address associated with the GMB account.
        business_account_id: The account ID of the managed business.
        gmb_access_token: The access token created using the 'AdWords' scope
            and the client ID and client secret of with the Cloud project
            associated with the GMB account.
    """
    # Get the FeedService and CustomerFeedService clients.
    feed_service = client.get_service("FeedService")
    customer_feed_service = client.get_service("CustomerFeedService")

    # Create a feed operation and configure the new feed.
    # The feed will sync to the Google My Business account specified by
    # gmb_email_address. Do not add FeedAttributes to this object as Google Ads
    # will add them automatically because this will be a system generated feed.
    # See here for more details:
    # https://developers.google.com/google-ads/api/docs/location-extensions/google-ads-location-extensions
    # [START add_google_my_business_location_extensions]
    feed_operation = client.get_type("FeedOperation")
    gmb_feed = feed_operation.create
    gmb_feed.name = f"Google My Business Feed #{uuid4()}"
    # Configure the location feed populated from Google My Business Locations.
    gmb_feed.places_location_feed_data.email_address = gmb_email_address

    if business_account_id is not None:
        gmb_feed.places_location_feed_data.business_account_id = (
            business_account_id
        )

    # Used to filter Google My Business listings by labels. If entries exist in
    # label_filters, only listings that have at least one of the labels set are
    # candidates to be synchronized into FeedItems. If no entries exist in
    # label_filters, then all listings are candidates for syncing.
    gmb_feed.places_location_feed_data.label_filters.append(
        "Stores in New York"
    )

    # Set the authentication info to be able to connect Google Ads to the GMB
    # account.
    gmb_feed.places_location_feed_data.oauth_info.http_method = "GET"
    gmb_feed.places_location_feed_data.oauth_info.http_request_url = (
        DEFAULT_OAUTH2_SCOPE
    )
    gmb_feed.places_location_feed_data.oauth_info.http_authorization_header = (
        f"Bearer {gmb_access_token}"
    )
    # Since this feed's feed items will be managed by Google, you must set its
    # origin to GOOGLE.
    gmb_feed.origin = client.get_type("FeedOriginEnum").FeedOrigin.GOOGLE

    # Optional: Delete all existing location extension feeds. This is an
    # optional step, and is required for this code example to run correctly
    # more than once; Google Ads only allows one location extension feed
    # per email address, and a Google Ads account cannot have a location
    # extension feed and an affiliate location extension feed at the same
    # time.
    _delete_location_extension_feeds(client, customer_id)

    # [START add_google_my_business_location_extensions_1]
    # Add the feed. Since it is a system generated feed, Google Ads will
    # automatically:
    # 1. Set up the FeedAttributes on the feed.
    # 2. Set up a FeedMapping that associates the FeedAttributes of the feed
    #   with the placeholder fields of the LOCATION placeholder type.
    feed_response = feed_service.mutate_feeds(
        customer_id=customer_id, operations=[feed_operation]
    )
    feed_resource_name = feed_response.results[0].resource_name
    print(f"GMB feed created with resource name '{feed_resource_name}'.")
    # [END add_google_my_business_location_extensions_1]
    # [END add_google_my_business_location_extensions]

    # [START add_google_my_business_location_extensions_2]
    # After the completion of the Feed ADD operation above the added feed
    # will not be available for usage in a CustomerFeed until the sync
    # between the Google Ads and GMB accounts completes.
    # This process is asynchronous, so we wait until the feed mapping is
    # created, performing exponential backoff.
    customer_feed_resource_name = None
    number_of_attempts = 0

    while number_of_attempts < MAX_CUSTOMER_FEED_ADD_ATTEMPTS:
        feed_mapping = _get_gmb_feed_mapping(
            client, customer_id, feed_resource_name
        )

        if feed_mapping is None:
            number_of_attempts += 1
            sleep_seconds = 5 * (2 ** number_of_attempts)

            print(
                f"Attempt #{number_of_attempts} was not successful. "
                f"Waiting {sleep_seconds}s before trying again."
            )

            time.sleep(sleep_seconds)
        else:
            customer_feed_resource_name = feed_mapping.resource_name
            print(f"GMB feed {feed_resource_name} is now ready.")
            break
            # [END add_google_my_business_location_extensions_2]

    if customer_feed_resource_name is None:
        print(
            "Could not create the CustomerFeed after "
            f"{MAX_CUSTOMER_FEED_ADD_ATTEMPTS} attempts. Please retry "
            "the CustomerFeed ADD operation later."
        )
        sys.exit(1)
    else:
        # [START add_google_my_business_location_extensions_3]
        # Create a CustomerFeed operation and configure the CustomerFeed to
        # associate the feed with this customer for the LOCATION placeholder
        # type.

        # OPTIONAL: Create a CampaignFeed to specify which FeedItems to use at
        # the Campaign level.

        # OPTIONAL: Create an AdGroupFeed for even more fine grained control
        # over which feed items are used at the AdGroup level.
        customer_feed_operation = client.get_type("CustomerFeedOperation")
        customer_feed = customer_feed_operation.create
        customer_feed.feed = feed_resource_name
        customer_feed.placeholder_types.append(
            client.get_type("PlaceholderTypeEnum").PlaceholderType.LOCATION
        )
        # The function string "IDENTITY(true)" will enable this feed.
        true_operand = client.get_type("Operand")
        true_operand.constant_operand.boolean_value = True
        customer_feed.matching_function.left_operands.append(true_operand)
        customer_feed.matching_function.function_string = "IDENTITY(true)"
        customer_feed.matching_function.operator = client.get_type(
            "MatchingFunctionOperatorEnum"
        ).MatchingFunctionOperator.IDENTITY

        customer_feed_response = customer_feed_service.mutate_customer_feeds(
            customer_id=customer_id, operations=[customer_feed_operation]
        )
        print(
            "Customer feed created with resource name "
            f"'{customer_feed_response.results[0].resource_name}'."
        )
        # [END add_google_my_business_location_extensions_3]


def _delete_location_extension_feeds(client, customer_id):
    """Deletes the existing location extension feeds.

    Args:
        client: An initialized Google Ads API client.
        customer_id: The Google Ads customer ID.
    """
    # To delete a location extension feed, you need to:
    # 1. Delete the CustomerFeed so that the location extensions from the feed
    # stop serving.
    # 2. Delete the feed so that Google Ads will no longer sync from the GMB
    # account.
    old_customer_feeds = _get_location_extension_customer_feeds(
        client, customer_id
    )
    if old_customer_feeds:
        _delete_customer_feeds(client, customer_id, old_customer_feeds)

    old_feeds = _get_location_extension_feeds(client, customer_id)
    if old_feeds:
        _delete_feeds(client, customer_id, old_feeds)


def _get_location_extension_customer_feeds(client, customer_id):
    """Gets the existing location extension customer feeds.

    Args:
        client: An initialized Google Ads API client.
        customer_id: The Google Ads customer ID.
    Returns:
        A list of location extension feeds.
    """
    googleads_service = client.get_service("GoogleAdsService")

    # Create the query. A location extension customer feed can be identified by
    # filtering for placeholder_types=LOCATION (location extension feeds) or
    # placeholder_types=AFFILIATE_LOCATION (affiliate location extension feeds).
    query = """
        SELECT
          customer_feed.resource_name,
          customer_feed.feed,
          customer_feed.status,
          customer_feed.matching_function.function_string
        FROM customer_feed
        WHERE
          customer_feed.placeholder_types CONTAINS ANY(LOCATION, AFFILIATE_LOCATION)
          AND customer_feed.status = ENABLED"""

    result = googleads_service.search(customer_id=customer_id, query=query)

    return [row.customer_feed for row in result]


def _get_location_extension_feeds(client, customer_id):
    """Gets the existing location extension feeds.

    Args:
        client: An initialized Google Ads API client.
        customer_id: The Google Ads customer ID.
    Returns:
        A list of location extension feeds.
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

    result = googleads_service.search(customer_id=customer_id, query=query)

    # A location extension feed can be identified by checking whether the
    # places_location_feed_data field is set or the
    # affiliate_location_feed_data field is set.
    return [
        row.feed
        for row in result
        if row.feed.places_location_feed_data
        or row.feed.affiliate_location_feed_data
    ]


def _delete_customer_feeds(client, customer_id, old_customer_feeds):
    """Removes the customer feeds.

    Args:
        client: An initialized Google Ads API client.
        customer_id: The Google Ads customer ID.
        old_customer_feeds: The list of customer feeds to delete.
    """
    operations = []
    customer_feed_service = client.get_service("CustomerFeedService")

    for customer_feed in old_customer_feeds:
        operation = client.get_type("CustomerFeedOperation")
        operation.remove = customer_feed.resource_name
        operations.append(operation)

    customer_feed_service.mutate_customer_feeds(
        customer_id=customer_id, operations=operations
    )


def _delete_feeds(client, customer_id, old_feeds):
    """Removes the specified feeds.

    Args:
        client: An initialized Google Ads API client.
        customer_id: The Google Ads customer ID.
        old_feeds: The list of feeds to delete.
    """
    operations = []
    feed_service = client.get_service("FeedService")

    for feed in old_feeds:
        operation = client.get_type("FeedOperation")
        operation.remove = feed.resource_name
        operations.append(operation)

    feed_service.mutate_feeds(customer_id=customer_id, operations=operations)


def _get_gmb_feed_mapping(client, customer_id, feed_resource_name):
    """Gets a Google My Business Feed mapping.

    Args:
        client: An initialized Google Ads client.
        customer_id: The customer ID for which the call is made.
        feed_resource_name: The string Google My Business feed resource name.

    Returns:
        The requested FeedMapping, or None if it is not available.
    """
    googleads_service = client.get_service("GoogleAdsService")

    query = f"""
        SELECT feed_mapping.resource_name, feed_mapping.status
        FROM feed_mapping
        WHERE
          feed_mapping.feed = '{feed_resource_name}'
          AND feed_mapping.status = ENABLED
          AND feed_mapping.placeholder_type = LOCATION
        LIMIT 1"""

    result = googleads_service.search(customer_id=customer_id, query=query)

    try:
        return next(iter(result)).feed_mapping
    except StopIteration:
        return None


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v8")

    parser = argparse.ArgumentParser(
        description="Adds a feed that syncs feed items from a Google My "
        "Business (GMB) account."
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
        "-e",
        "--gmb_email_address",
        type=str,
        required=True,
        help="The email address associated with the GMB account.",
    )
    parser.add_argument(
        "-b",
        "--business_account_id",
        type=str,
        required=False,
        help="The account ID of the managed business.\n"
        "If the email_address is for a GMB manager instead of the GMB account "
        "owner, then set business_account_id to the Google+ Page ID of a "
        "location for which the manager has access. This information is "
        "available through the Google My Business API. See "
        "https://developers.google.com/my-business/reference/rest/v4/accounts.locations#locationkey"
        "for details.",
    )
    parser.add_argument(
        "-t",
        "--gmb_access_token",
        type=str,
        required=False,
        default=googleads_client.credentials.token,
        help="If the gmb_email_address above is the same user you used to "
        "generate your Google Ads API refresh token, do not pass a value to "
        "this argument.\nOtherwise, to obtain an access token for your GMB "
        "account, run the authenticate_in_standalone_application code example "
        "while logged in as the same user as gmb_email_address. Pass the "
        "Access Token value to this argument.",
    )

    args = parser.parse_args()

    try:
        main(
            googleads_client,
            args.customer_id,
            args.gmb_email_address,
            args.business_account_id,
            args.gmb_access_token,
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
