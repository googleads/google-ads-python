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
"""Creates a rule-based user list.

The list will be defined by an expression rule for users who have visited two
different pages of a website.
"""

import argparse
import sys
from uuid import uuid4

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

URL_LIST = ["http://example.com/section1", "http://example.com/section2"]


def main(client, customer_id):
    """Creates a rule-based user list.

    The list will be defined by an expression rule for users who have visited
    two different pages of a website.

    Args:
        client: The Google Ads client.
        customer_id: The customer ID for which to add the user list.
    """
    # Get the UserListService client.
    user_list_service = client.get_service("UserListService")

    user_list_rule_info = client.get_type("UserListRuleInfo")

    # Combine the two rule items into a UserListRuleItemGroupInfo object so
    # Google Ads will AND their rules together. To instead OR the rules
    # together, each rule should be placed in its own rule item group.
    user_list_rule_item_group_info = client.get_type(
        "UserListRuleItemGroupInfo"
    )

    # Create rules targeting any user that visits the URLs in URL_LIST.
    for url in URL_LIST:
        user_list_rule_item_group_info.rule_items.append(
            _build_visited_site_rule_info(client, url)
        )
    user_list_rule_info.rule_item_groups.append(user_list_rule_item_group_info)

    # Creates an ExpressionRuleUserListInfo object, or a boolean rule that
    # defines this user list. The default rule_type for a UserListRuleInfo
    # object is OR of ANDs (disjunctive normal form). That is, rule items will
    # be ANDed together within rule item groups and the groups themselves will
    # be ORed together.
    expression_rule_user_list_info = client.get_type(
        "ExpressionRuleUserListInfo"
    )
    client.copy_from(expression_rule_user_list_info.rule, user_list_rule_info)

    # Define a representation of a user list that is generated by a rule.
    rule_based_user_list_info = client.get_type("RuleBasedUserListInfo")
    # Optional: To include past users in the user list, set the
    # prepopulation_status to REQUESTED.
    rule_based_user_list_info.prepopulation_status = client.get_type(
        "UserListPrepopulationStatusEnum"
    ).UserListPrepopulationStatus.REQUESTED
    client.copy_from(
        rule_based_user_list_info.expression_rule_user_list,
        expression_rule_user_list_info,
    )

    # Create a UserListOperation and populate the UserList.
    user_list_operation = client.get_type("UserListOperation")
    user_list = user_list_operation.create
    joined_urls = " AND ".join(URL_LIST)
    user_list.name = f"All visitors to {joined_urls} #{uuid4()}"
    user_list.description = f"Visitors of {joined_urls}"
    user_list.membership_status = client.get_type(
        "UserListMembershipStatusEnum"
    ).UserListMembershipStatus.OPEN
    user_list.membership_life_span = 365
    client.copy_from(user_list.rule_based_user_list, rule_based_user_list_info)

    # Issue a mutate request to add the user list, then print the results.
    response = user_list_service.mutate_user_lists(
        customer_id=customer_id, operations=[user_list_operation]
    )
    print(
        "Created expression rule user list with resource name "
        f"'{response.results[0].resource_name}.'"
    )


def _build_visited_site_rule_info(client, url):
    """Creates a UserListRuleItemInfo object targeting a visit to a given URL.

    Args:
        client: An initialized Google Ads client.
        url: The URL at which the rule will be targeted.
    Returns:
        A populated UserListRuleItemInfo object.
    """
    user_visited_site_rule = client.get_type("UserListRuleItemInfo")
    # Use a built-in parameter to create a domain URL rule.
    user_visited_site_rule.name = "url__"
    user_visited_site_rule.string_rule_item.operator = client.get_type(
        "UserListStringRuleItemOperatorEnum"
    ).UserListStringRuleItemOperator.CONTAINS
    user_visited_site_rule.string_rule_item.value = url

    return user_visited_site_rule


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v6")

    parser = argparse.ArgumentParser(
        description="Creates a rule-based user list defined by an expression "
        "rule for users who have visited two different sections of a website."
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
