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
"""Creates a combination user list.

The list will contain users that are present on any one of the provided user
lists.
"""

import argparse
import sys
from uuid import uuid4

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


# [START add_logical_user_list]
def main(client, customer_id, user_list_ids):
    """Creates a combination user list.

    Args:
        client: The Google Ads client.
        customer_id: The customer ID for which to add the user list.
        user_list_ids: A list of user list IDs to logically combine.
    """
    # Get the UserListService client.
    user_list_service = client.get_service("UserListService")

    # Add each of the provided list IDs to a list of rule operands specifying
    # which lists the operator should target.
    logical_user_list_operand_info_list = []
    for user_list_id in user_list_ids:
        logical_user_list_operand_info = client.get_type(
            "LogicalUserListOperandInfo"
        )
        logical_user_list_operand_info.user_list = user_list_service.user_list_path(
            customer_id, user_list_id
        )
        logical_user_list_operand_info_list.append(
            logical_user_list_operand_info
        )

    # Create a UserListOperation and populate the UserList.
    user_list_operation = client.get_type("UserListOperation")
    user_list = user_list_operation.create
    user_list.name = f"My combination list of other user lists #{uuid4()}"
    # Create a UserListLogicalRuleInfo specifying that a user should be added to
    # the new list if they are present in any of the provided lists.
    user_list_logical_rule_info = client.get_type("UserListLogicalRuleInfo")
    # Using ANY means that a user should be added to the combined list if they
    # are present on any of the lists targeted in the
    # LogicalUserListOperandInfo. Use ALL to add users present on all of the
    # provided lists or NONE to add users that aren't present on any of the
    # targeted lists.
    user_list_logical_rule_info.operator = client.get_type(
        "UserListLogicalRuleOperatorEnum"
    ).UserListLogicalRuleOperator.ANY
    user_list_logical_rule_info.rule_operands.extend(
        logical_user_list_operand_info_list
    )
    user_list.logical_user_list.rules.append(user_list_logical_rule_info)

    # Issue a mutate request to add the user list, then print the results.
    response = user_list_service.mutate_user_lists(
        customer_id=customer_id, operations=[user_list_operation]
    )
    print(
        "Created logical user list with resource name "
        f"'{response.results[0].resource_name}.'"
    )
    # [END add_logical_user_list]


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v8")

    parser = argparse.ArgumentParser(
        description="Creates a combination user list containing users that are "
        "present on any one of the provided user lists."
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
        "-l",
        "--user_list_ids",
        nargs="+",
        type=str,
        required=True,
        help="The user list IDs logically combine.",
    )
    args = parser.parse_args()

    try:
        main(googleads_client, args.customer_id, args.user_list_ids)
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
