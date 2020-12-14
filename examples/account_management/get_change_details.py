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

from google.ads.google_ads.client import GoogleAdsClient
from google.ads.google_ads.errors import GoogleAdsException
from google.ads.google_ads.util import get_nested_attr


_DEFAULT_PAGE_SIZE = 1000


def main(client, customer_id):
    """Gets specific details about the most recent changes in the given account.

    Args:
      client: The Google Ads client.
      customer_id: The Google Ads customer ID.
    """
    google_ads_service = client.get_service("GoogleAdsService", version="v6")

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

    resource_type_enum = client.get_type(
        "ChangeEventResourceTypeEnum", version="v6"
    ).ChangeEventResourceType
    operation_type_enum = client.get_type(
        "ResourceChangeOperationEnum", version="v6"
    ).ResourceChangeOperation

    try:
        results = google_ads_service.search(
            customer_id, query=query, page_size=_DEFAULT_PAGE_SIZE
        )

        for row in results:
            event = row.change_event
            resource_type = resource_type_enum.Name(event.change_resource_type)
            if resource_type == "AD":
                old_resource = event.old_resource.ad
                new_resource = event.new_resource.ad
            elif resource_type == "AD_GROUP":
                old_resource = event.old_resource.ad_group
                new_resource = event.new_resource.ad_group
            elif resource_type == "AD_GROUP_CRITERION":
                old_resource = event.old_resource.ad_group_criterion
                new_resource = event.new_resource.ad_group_criterion
            elif resource_type == "AD_GROUP_BID_MODIFIER":
                old_resource = event.old_resource.ad_group_bid_modifier
                new_resource = event.new_resource.ad_group_bid_modifier
            elif resource_type == "CAMPAIGN":
                old_resource = event.old_resource.campaign
                new_resource = event.new_resource.campaign
            elif resource_type == "CAMPAIGN_BUDGET":
                old_resource = event.old_resource.campaign_budget
                new_resource = event.new_resource.campaign_budget
            elif resource_type == "CAMPAIGN_CRITERION":
                old_resource = event.old_resource.campaign_criterion
                new_resource = event.new_resource.campaign_criterion
            else:
                print(
                    "Unknown change_resource_type: '{event.change_resource_type}'"
                )
                # If the resource type is unrecognized then we continue to
                # the next row.
                continue

            print(
                f"On {event.change_date_time}, user {event.user_email} "
                f"used interface {event.client_type} to perform a(n) "
                f"{event.resource_change_operation} operation on a "
                f"{event.change_resource_type} with resource name "
                f"'{event.change_resource_name}'"
            )

            operation_type = operation_type_enum.Name(
                event.resource_change_operation
            )

            if operation_type in ("UPDATE", "CREATE"):
                for changed_field in event.changed_fields.paths:
                    new_value = get_nested_attr(new_resource, changed_field)
                    if operation_type == "CREATE":
                        print(f"\t{changed_field} set to {new_value}")
                    else:
                        old_value = get_nested_attr(old_resource, changed_field)
                        print(
                            f"\t{changed_field} changed from {old_value} to {new_value}"
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


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    google_ads_client = GoogleAdsClient.load_from_storage()

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
    main(google_ads_client, args.customer_id)
