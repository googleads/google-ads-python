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
"""Gets specific details about the most recent changes in the given account.

Changes include the name of the field that changed, and both the old and new
values.
"""

import argparse
from datetime import datetime, timedelta
import sys

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.ads.googleads.util import get_nested_attr


_DEFAULT_PAGE_SIZE = 1000


# [START get_change_details]
def main(client, customer_id):
    """Gets specific details about the most recent changes in the given account.

    Args:
      client: The Google Ads client.
      customer_id: The Google Ads customer ID.
    """
    googleads_service = client.get_service("GoogleAdsService")

    # Construct a query to find details for recent changes in your account.
    # The LIMIT clause is required for the change_event resource.
    # The maximum size is 10000, but a low limit was set here for demonstrative
    # purposes. For more information see:
    # https://developers.google.com/google-ads/api/docs/change-event#getting_changes
    # The WHERE clause on change_date_time is also required. It must specify a
    # window within the past 30 days.
    tomorrow = (datetime.now() + timedelta(1)).strftime("%Y-%m-%d")
    two_weeks_ago = (datetime.now() + timedelta(-14)).strftime("%Y-%m-%d")
    query = f"""
        SELECT
          change_event.resource_name,
          change_event.change_date_time,
          change_event.change_resource_name,
          change_event.user_email,
          change_event.client_type,
          change_event.change_resource_type,
          change_event.old_resource,
          change_event.new_resource,
          change_event.resource_change_operation,
          change_event.changed_fields
        FROM change_event
        WHERE change_event.change_date_time <= '{tomorrow}'
        AND change_event.change_date_time >= '{two_weeks_ago}'
        ORDER BY change_event.change_date_time DESC
        LIMIT 5"""

    search_request = client.get_type("SearchGoogleAdsRequest")
    search_request.customer_id = customer_id
    search_request.query = query
    search_request.page_size = _DEFAULT_PAGE_SIZE

    results = googleads_service.search(request=search_request)

    for row in results:
        event = row.change_event
        resource_type = event.change_resource_type.name
        if resource_type == "AD":
            old_resource = event.old_resource.ad
            new_resource = event.new_resource.ad
        elif resource_type == "AD_GROUP":
            old_resource = event.old_resource.ad_group
            new_resource = event.new_resource.ad_group
        elif resource_type == "AD_GROUP_AD":
            old_resource = event.old_resource.ad_group_ad
            new_resource = event.new_resource.ad_group_ad
        elif resource_type == "AD_GROUP_CRITERION":
            old_resource = event.old_resource.ad_group_criterion
            new_resource = event.new_resource.ad_group_criterion
        elif resource_type == "AD_GROUP_BID_MODIFIER":
            old_resource = event.old_resource.ad_group_bid_modifier
            new_resource = event.new_resource.ad_group_bid_modifier
        elif resource_type == "AD_GROUP_FEED":
            old_resource = event.old_resource.ad_group_feed
            new_resource = event.new_resource.ad_group_feed
        elif resource_type == "CAMPAIGN":
            old_resource = event.old_resource.campaign
            new_resource = event.new_resource.campaign
        elif resource_type == "CAMPAIGN_BUDGET":
            old_resource = event.old_resource.campaign_budget
            new_resource = event.new_resource.campaign_budget
        elif resource_type == "CAMPAIGN_CRITERION":
            old_resource = event.old_resource.campaign_criterion
            new_resource = event.new_resource.campaign_criterion
        elif resource_type == "CAMPAIGN_FEED":
            old_resource = event.old_resource.campaign_feed
            new_resource = event.new_resource.campaign_feed
        elif resource_type == "FEED":
            old_resource = event.old_resource.feed
            new_resource = event.new_resource.feed
        elif resource_type == "FEED_ITEM":
            old_resource = event.old_resource.feed_item
            new_resource = event.new_resource.feed_item
        else:
            print(
                "Unknown change_resource_type: '{event.change_resource_type}'"
            )
            # If the resource type is unrecognized then we continue to
            # the next row.
            continue

        print(
            f"On {event.change_date_time}, user {event.user_email} "
            f"used interface {event.client_type.name} to perform a(n) "
            f"{event.resource_change_operation.name} operation on a "
            f"{event.change_resource_type.name} with resource name "
            f"'{event.change_resource_name}'"
        )

        operation_type = event.resource_change_operation.name

        if operation_type in ("UPDATE", "CREATE"):
            for changed_field in event.changed_fields.paths:
                # Change field name from "type" to "type_" so that it doesn't
                # raise an exception when accessed on the protobuf object, see:
                # https://developers.google.com/google-ads/api/docs/client-libs/python/library-version-10#field_names_that_are_reserved_words
                if changed_field == "type":
                    changed_field = "type_"
                new_value = get_nested_attr(new_resource, changed_field)
                if operation_type == "CREATE":
                    print(f"\t{changed_field} set to {new_value}")
                else:
                    old_value = get_nested_attr(old_resource, changed_field)
                    print(
                        f"\t{changed_field} changed from {old_value} to {new_value}"
                    )
                    # [END get_change_details]


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v8")

    parser = argparse.ArgumentParser(
        description="This example gets specific details about the most recent "
        "changes in the given account."
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
    try:
        main(googleads_client, args.customer_id)
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
