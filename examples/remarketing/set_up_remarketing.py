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
"""Demonstrates various operations involved in remarketing.

Operations include (a) creating a user list based on visitors to a website,
(b) targeting a user list with an ad group criterion, (c) updating the bid
modifier on an ad group criterion, (d) finding and removing all ad group
criteria under a given campaign, (e) targeting a user list with a campaign
criterion, and (f) updating the bid modifier on a campaign criterion. It is
unlikely that users will need to perform all of these operations consecutively,
and all of the operations contained herein are meant of for illustrative
purposes.
"""


import argparse
import sys
from typing import List
from uuid import uuid4

from google.api_core import protobuf_helpers

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.ads.googleads.v22.common.types.user_lists import (
    FlexibleRuleOperandInfo,
    FlexibleRuleUserListInfo,
    UserListRuleItemGroupInfo,
    UserListRuleItemInfo,
)
from google.ads.googleads.v22.resources.types.ad_group_criterion import (
    AdGroupCriterion,
)
from google.ads.googleads.v22.resources.types.campaign_criterion import (
    CampaignCriterion,
)
from google.ads.googleads.v22.resources.types.user_list import UserList
from google.ads.googleads.v22.services.services.ad_group_criterion_service import (
    AdGroupCriterionServiceClient,
)
from google.ads.googleads.v22.services.services.campaign_criterion_service import (
    CampaignCriterionServiceClient,
)
from google.ads.googleads.v22.services.services.google_ads_service import (
    GoogleAdsServiceClient,
)
from google.ads.googleads.v22.services.services.user_list_service import (
    UserListServiceClient,
)
from google.ads.googleads.v22.services.types.ad_group_criterion_service import (
    AdGroupCriterionOperation,
    MutateAdGroupCriteriaResponse,
)
from google.ads.googleads.v22.services.types.campaign_criterion_service import (
    CampaignCriterionOperation,
    MutateCampaignCriteriaResponse,
)
from google.ads.googleads.v22.services.types.google_ads_service import (
    GoogleAdsRow,
    SearchGoogleAdsRequest,
    SearchGoogleAdsResponse,
)
from google.ads.googleads.v22.services.types.user_list_service import (
    MutateUserListsResponse,
    UserListOperation,
)


def main(
    client: GoogleAdsClient,
    customer_id: str,
    campaign_id: str,
    ad_group_id: str,
    bid_modifier_value: float,
) -> None:
    """The main method that creates all necessary entities for the example.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a str client customer ID used to create a user list and
            other various entities required for the example.
        campaign_id: a str ID for a campaign used to create an ad group
            criterion that targets members of a user list.
        ad_group_id: a str ID for an ad group used to create an ad group
            criterion that targets members of a user list.
        bid_modifier_value: a float that specifies a modifier on the bid amount
            for newly created ad group criterion.
    """
    user_list_resource_name: str = create_user_list(client, customer_id)
    ad_group_criterion_resource_name: str = target_ads_in_ad_group_to_user_list(
        client, customer_id, ad_group_id, user_list_resource_name
    )
    modify_ad_group_bids(
        client,
        customer_id,
        ad_group_criterion_resource_name,
        bid_modifier_value,
    )
    remove_existing_criteria_from_ad_group(client, customer_id, campaign_id)
    campaign_criterion_resource_name: str = target_ads_in_campaign_to_user_list(
        client, customer_id, campaign_id, user_list_resource_name
    )
    modify_campaign_bids(
        client,
        customer_id,
        campaign_criterion_resource_name,
        bid_modifier_value,
    )


# [START setup_remarketing]
def create_user_list(client: GoogleAdsClient, customer_id: str) -> str:
    """Creates a user list targeting users that have visited a given URL.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a str client customer ID used to create a user list.

    Returns:
        a str resource name for the newly created user list.
    """
    # Creates a UserListOperation.
    user_list_operation: UserListOperation = client.get_type(
        "UserListOperation"
    )
    # Creates a UserList.
    user_list: UserList = user_list_operation.create
    user_list.name = f"All visitors to example.com #{uuid4()}"
    user_list.description = "Any visitor to any page of example.com"
    user_list.membership_status = client.enums.UserListMembershipStatusEnum.OPEN
    user_list.membership_life_span = 365
    # Optional: To include past users in the user list, set the
    # prepopulation_status to REQUESTED.
    user_list.rule_based_user_list.prepopulation_status = (
        client.enums.UserListPrepopulationStatusEnum.REQUESTED
    )
    # Specifies that the user list targets visitors of a page with a URL that
    # contains 'example.com'.
    user_list_rule_item_group_info: UserListRuleItemGroupInfo = client.get_type(
        "UserListRuleItemGroupInfo"
    )
    user_list_rule_item_info: UserListRuleItemInfo = client.get_type(
        "UserListRuleItemInfo"
    )
    # Uses a built-in parameter to create a domain URL rule.
    user_list_rule_item_info.name = "url__"
    user_list_rule_item_info.string_rule_item.operator = (
        client.enums.UserListStringRuleItemOperatorEnum.CONTAINS
    )
    user_list_rule_item_info.string_rule_item.value = "example.com"
    user_list_rule_item_group_info.rule_items.append(user_list_rule_item_info)

    # Specify that the user list targets visitors of a page based on the
    # provided rule.
    flexible_rule_user_list_info: FlexibleRuleUserListInfo = (
        user_list.rule_based_user_list.flexible_rule_user_list
    )
    flexible_rule_user_list_info.inclusive_rule_operator = (
        client.enums.UserListFlexibleRuleOperatorEnum.AND
    )
    # Inclusive operands are joined together with the specified
    # inclusive rule operator.
    rule_operand: FlexibleRuleOperandInfo = client.get_type(
        "FlexibleRuleOperandInfo"
    )
    rule_operand.rule.rule_item_groups.extend([user_list_rule_item_group_info])
    rule_operand.lookback_window_days = 7
    flexible_rule_user_list_info.inclusive_operands.append(rule_operand)

    user_list_service: UserListServiceClient = client.get_service(
        "UserListService"
    )
    response: MutateUserListsResponse = user_list_service.mutate_user_lists(
        customer_id=customer_id, operations=[user_list_operation]
    )
    resource_name: str = response.results[0].resource_name
    print(f"Created user list with resource name: '{resource_name}'")
    return resource_name
    # [END setup_remarketing]


# [START setup_remarketing_1]
def target_ads_in_ad_group_to_user_list(
    client: GoogleAdsClient,
    customer_id: str,
    ad_group_id: str,
    user_list_resource_name: str,
) -> str:
    """Creates an ad group criterion that targets a user list with an ad group.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a str client customer ID used to create an ad group
            criterion.
        ad_group_id: a str ID for an ad group used to create an ad group
            criterion that targets members of a user list.
        user_list_resource_name: a str resource name for a user list.

    Returns:
        a str resource name for an ad group criterion.
    """
    ad_group_criterion_operation: AdGroupCriterionOperation = client.get_type(
        "AdGroupCriterionOperation"
    )
    # Creates the ad group criterion targeting members of the user list.
    ad_group_criterion: AdGroupCriterion = ad_group_criterion_operation.create
    ad_group_criterion.ad_group = client.get_service(
        "AdGroupService"
    ).ad_group_path(customer_id, ad_group_id)
    ad_group_criterion.user_list.user_list = user_list_resource_name

    ad_group_criterion_service: AdGroupCriterionServiceClient = (
        client.get_service("AdGroupCriterionService")
    )
    response: MutateAdGroupCriteriaResponse = (
        ad_group_criterion_service.mutate_ad_group_criteria(
            customer_id=customer_id, operations=[ad_group_criterion_operation]
        )
    )
    resource_name: str = response.results[0].resource_name
    print(
        "Successfully created ad group criterion with resource name: "
        f"'{resource_name}' targeting user list with resource name: "
        f"'{user_list_resource_name}' and with ad group with ID "
        f"{ad_group_id}."
    )
    return resource_name
    # [END setup_remarketing_1]


def modify_ad_group_bids(
    client: GoogleAdsClient,
    customer_id: str,
    ad_group_criterion_resource_name: str,
    bid_modifier_value: float,
) -> None:
    """Updates the bid modifier on an ad group criterion.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a str client customer ID.
        ad_group_criterion.resource_name: a str resource name for an ad group
            criterion.
        bid_modifier_value: a float value specifying an ad group criterion
            bid modifier.
    """
    # Constructs an operation that will update the ad group criterion with the
    # specified resource name.
    ad_group_criterion_operation: AdGroupCriterionOperation = client.get_type(
        "AdGroupCriterionOperation"
    )
    ad_group_criterion: AdGroupCriterion = ad_group_criterion_operation.update
    # Creates the ad group criterion with a bid modifier. You may alternatively
    # set the bid for the ad group criterion directly.
    ad_group_criterion.resource_name = ad_group_criterion_resource_name
    ad_group_criterion.bid_modifier = bid_modifier_value
    # Using the FieldMasks utility to derive the update mask tells the Google
    # Ads API which attributes of the ad group criterion you want to change.
    client.copy_from(
        ad_group_criterion_operation.update_mask,
        protobuf_helpers.field_mask(None, ad_group_criterion._pb),
    )
    ad_group_criterion_service: AdGroupCriterionServiceClient = (
        client.get_service("AdGroupCriterionService")
    )
    response: MutateAdGroupCriteriaResponse = (
        ad_group_criterion_service.mutate_ad_group_criteria(
            customer_id=customer_id, operations=[ad_group_criterion_operation]
        )
    )
    print(
        "Updated bid for ad group criterion with resource name: "
        f"'{response.results[0].resource_name}'"
    )


# [START setup_remarketing_3]
def remove_existing_criteria_from_ad_group(
    client: GoogleAdsClient, customer_id: str, campaign_id: str
) -> None:
    """Removes all ad group criteria targeting a user list under a campaign.

    This is a necessary step before targeting a user list at the campaign level.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a str client customer ID.
        campaign_id: a str ID for a campaign that will have all ad group
            criteria that targets user lists removed.
    """
    # Retrieves all of the ad group criteria under a campaign.
    all_ad_group_criteria: List[str] = get_user_list_ad_group_criteria(
        client, customer_id, campaign_id
    )

    # Creates a list of remove operations.
    remove_operations: List[AdGroupCriterionOperation] = []
    for ad_group_criterion_resource_name in all_ad_group_criteria:
        remove_operation: AdGroupCriterionOperation = client.get_type(
            "AdGroupCriterionOperation"
        )
        remove_operation.remove = ad_group_criterion_resource_name
        remove_operations.append(remove_operation)

    ad_group_criterion_service: AdGroupCriterionServiceClient = (
        client.get_service("AdGroupCriterionService")
    )
    response: MutateAdGroupCriteriaResponse = (
        ad_group_criterion_service.mutate_ad_group_criteria(
            customer_id=customer_id, operations=remove_operations
        )
    )
    print(
        "Successfully removed ad group criterion with resource name: "
        f"'{response.results[0].resource_name}'"
    )
    # [END setup_remarketing_3]


# [START setup_remarketing_2]
def get_user_list_ad_group_criteria(
    client: GoogleAdsClient, customer_id: str, campaign_id: str
) -> List[str]:
    """Finds all of user list ad group criteria under a campaign.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a str client customer ID.
        campaign_id: a str campaign ID.

    Returns:
        a list of ad group criterion resource names.
    """
    # Creates a query that retrieves all of the ad group criteria under a
    # campaign.
    query: str = f"""
        SELECT
          ad_group_criterion.criterion_id
        FROM ad_group_criterion
        WHERE campaign.id = {campaign_id}
        AND ad_group_criterion.type = USER_LIST"""

    googleads_service: GoogleAdsServiceClient = client.get_service(
        "GoogleAdsService"
    )
    search_request: SearchGoogleAdsRequest = client.get_type(
        "SearchGoogleAdsRequest"
    )
    search_request.customer_id = customer_id
    search_request.query = query
    response: SearchGoogleAdsResponse = googleads_service.search(
        request=search_request
    )

    # Iterates over all rows in all pages. Prints the user list criteria and
    # adds the ad group criteria resource names to the list.
    user_list_criteria: List[str] = []
    row: GoogleAdsRow
    for row in response:
        resource_name: str = row.ad_group_criterion.resource_name
        print(
            "Ad group criterion with resource name '{resource_name}' was "
            "found."
        )
        user_list_criteria.append(resource_name)

    return user_list_criteria
    # [END setup_remarketing_2]


# [START setup_remarketing_4]
def target_ads_in_campaign_to_user_list(
    client: GoogleAdsClient,
    customer_id: str,
    campaign_id: str,
    user_list_resource_name: str,
) -> str:
    """Creates a campaign criterion that targets a user list with a campaign.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a str client customer ID used to create an campaign
            criterion.
        campaign_id: a str ID for a campaign used to create a campaign
            criterion that targets members of a user list.
        user_list_resource_name: a str resource name for a user list.

    Returns:
        a str resource name for a campaign criterion.
    """
    campaign_criterion_operation: CampaignCriterionOperation = client.get_type(
        "CampaignCriterionOperation"
    )
    campaign_criterion: CampaignCriterion = campaign_criterion_operation.create
    campaign_criterion.campaign = client.get_service(
        "CampaignService"
    ).campaign_path(customer_id, campaign_id)
    campaign_criterion.user_list.user_list = user_list_resource_name

    campaign_criterion_service: CampaignCriterionServiceClient = (
        client.get_service("CampaignCriterionService")
    )
    response: MutateCampaignCriteriaResponse = (
        campaign_criterion_service.mutate_campaign_criteria(
            customer_id=customer_id, operations=[campaign_criterion_operation]
        )
    )
    resource_name: str = response.results[0].resource_name
    print(
        "Successfully created campaign criterion with resource name "
        f"'{resource_name}' targeting user list with resource name "
        f"'{user_list_resource_name}' with campaign with ID {campaign_id}"
    )
    return resource_name
    # [END setup_remarketing_4]


def modify_campaign_bids(
    client: GoogleAdsClient,
    customer_id: str,
    campaign_criterion_resource_name: str,
    bid_modifier_value: float,
) -> None:
    """Updates the bid modifier on a campaign criterion.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a str client customer ID.
        campaign_criterion_resource_name: a str resource name for a campaign
            criterion.
        bid_modifier_value: a float value specifying a campaign criterion
            bid modifier.
    """
    # Constructs an operation that will update the campaign criterion with the
    # specified resource name.
    campaign_criterion_operation: CampaignCriterionOperation = client.get_type(
        "CampaignCriterionOperation"
    )
    campaign_criterion: CampaignCriterion = campaign_criterion_operation.update
    campaign_criterion.resource_name = campaign_criterion_resource_name
    campaign_criterion.bid_modifier = bid_modifier_value

    # Using the FieldMasks utility to derive the update mask tells the Google
    # Ads API which attributes of the campaign criterion you want to change.
    client.copy_from(
        campaign_criterion_operation.update_mask,
        protobuf_helpers.field_mask(None, campaign_criterion._pb),
    )

    campaign_criterion_service: CampaignCriterionServiceClient = (
        client.get_service("CampaignCriterionService")
    )
    response: MutateCampaignCriteriaResponse = (
        campaign_criterion_service.mutate_campaign_criteria(
            customer_id=customer_id, operations=[campaign_criterion_operation]
        )
    )
    print(
        "Successfully updated the bid for campaign criterion with resource "
        f"name: '{response.results[0].resource_name}'"
    )


if __name__ == "__main__":
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Demonstrates various operations involved in remarketing."
    )
    # The following arguments are required to run the example.
    parser.add_argument(
        "-c",
        "--customer_id",
        type=str,
        required=True,
        help=(
            "A Google Ads customer ID used to create a user list and other "
            "various entities required for the example."
        ),
    )
    parser.add_argument(
        "-i",
        "--campaign_id",
        type=str,
        required=True,
        help=(
            "The ID for a campaign that will have its ad group criteria "
            "modified to target user lists members."
        ),
    )
    parser.add_argument(
        "-a",
        "--ad_group_id",
        type=str,
        required=True,
        help=(
            "The ID for an ad group used to create an ad group criterion "
            "that targets members of a user list."
        ),
    )
    # The following argument is optional.
    parser.add_argument(
        "-b",
        "--bid_modifier_value",
        type=float,
        default=1.5,
        help=(
            "A float that specifies a modifier on the bid amount "
            "for newly created ad group criterion."
        ),
    )
    args: argparse.Namespace = parser.parse_args()

    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client: GoogleAdsClient = GoogleAdsClient.load_from_storage(
        version="v22"
    )

    try:
        main(
            googleads_client,
            args.customer_id,
            args.campaign_id,
            args.ad_group_id,
            args.bid_modifier_value,
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
