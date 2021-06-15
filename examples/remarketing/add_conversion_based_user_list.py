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
"""Creates a basic user list based on conversion actions.

The given conversion action IDs will be associated with the new user list.
A user will be added to the list upon triggering more than one of the actions,
e.g. by visiting a site and making a purchase.
"""

import argparse
import sys
from uuid import uuid4

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


# [START add_conversion_based_user_list]
def main(client, customer_id, conversion_action_ids):
    """Creates a combination user list.

    Args:
        client: The Google Ads client.
        customer_id: The customer ID for which to add the user list.
        conversion_action_ids: The IDs of the conversion actions for the basic
            user list.
    """
    # Get the UserListService and ConversionActionService clients.
    user_list_service = client.get_service("UserListService")
    conversion_action_service = client.get_service("ConversionActionService")

    # Create a list of UserListActionInfo objects for the given conversion
    # actions. These specify the conversion actions that, when triggered, will
    # cause a user to be added to a UserList.
    user_list_action_info_list = []
    for conversion_action_id in conversion_action_ids:
        user_list_action_info = client.get_type("UserListActionInfo")
        user_list_action_info.conversion_action = conversion_action_service.conversion_action_path(
            customer_id, conversion_action_id
        )
        user_list_action_info_list.append(user_list_action_info)

    # Create a UserListOperation and populate the UserList.
    user_list_operation = client.get_type("UserListOperation")
    user_list = user_list_operation.create
    user_list.name = f"Example BasicUserList #{uuid4()}"
    user_list.description = (
        "A list of people who have triggered one or more conversion actions"
    )
    user_list.membership_status = client.get_type(
        "UserListMembershipStatusEnum"
    ).UserListMembershipStatus.OPEN
    user_list.membership_life_span = 365
    # The basic user list info object contains the conversion action info.
    user_list.basic_user_list.actions.extend(user_list_action_info_list)

    # Issue a mutate request to add the user list, then print the results.
    response = user_list_service.mutate_user_lists(
        customer_id=customer_id, operations=[user_list_operation]
    )
    print(
        "Created basic user list with resource name "
        f"'{response.results[0].resource_name}.'"
    )
    # [END add_conversion_based_user_list]


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v8")

    parser = argparse.ArgumentParser(
        description="Creates a basic user list based on conversion actions."
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
        "--conversion_action_ids",
        nargs="+",
        type=str,
        required=True,
        help="The IDs of the conversion actions for the basic user list.",
    )
    args = parser.parse_args()

    try:
        main(googleads_client, args.customer_id, args.conversion_action_ids)
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
