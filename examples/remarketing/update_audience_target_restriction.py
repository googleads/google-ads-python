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
"""Updates the audience target restriction of a given ad group to bid only."""


import argparse
import sys

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.api_core import protobuf_helpers


def main(client, customer_id, ad_group_id):
    """Updates the audience target restriction of a given ad group to bid only.

    Args:
        client: An initialized GoogleAdsClient instance.
        customer_id: The client customer ID string.
        ad_group_id: The ad group ID for which to update the audience targeting
            restriction.
    """
    # Get the GoogleAdsService client.
    googleads_service = client.get_service("GoogleAdsService")

    # Create a search request that retrieves the targeting settings from a given
    # ad group.
    # [START update_audience_target_restriction]
    query = f"""
        SELECT
          ad_group.id,
          ad_group.name,
          ad_group.targeting_setting.target_restrictions
        FROM ad_group
        WHERE ad_group.id = {ad_group_id}"""
    # [END update_audience_target_restriction]

    # Issue the search request.
    search_response = googleads_service.search(
        customer_id=customer_id, query=query
    )

    targeting_dimension_enum = client.get_type(
        "TargetingDimensionEnum"
    ).TargetingDimension

    # Create an empty TargetingSetting instance.
    targeting_setting = client.get_type("TargetingSetting")

    # Create a flag that specifies whether or not we should update the
    # targeting setting. We should only do this if we find an audience
    # target restriction with bid_only set to false.
    should_update_targeting_setting = False

    ad_group = next(iter(search_response)).ad_group

    print(
        f"Ad group with ID {ad_group.id} and name '{ad_group.name}' "
        "was found with the following targeting restrictions:"
    )

    target_restrictions = ad_group.targeting_setting.target_restrictions

    # Loop through and print each of the target restrictions.
    # Reconstruct the TargetingSetting object with the updated audience
    # target restriction because Google Ads will overwrite the entire
    # targeting_setting field of the ad group when the field mask
    # includes targeting_setting in an update operation.
    # [START update_audience_target_restriction_1]
    for target_restriction in target_restrictions:
        targeting_dimension = target_restriction.targeting_dimension
        bid_only = target_restriction.bid_only

        print(
            "\tTargeting restriction with targeting dimension "
            f"'{targeting_dimension.name}' "
            f"and bid only set to '{bid_only}'."
        )

        # Add the target restriction to the TargetingSetting object as
        # is if the targeting dimension has a value other than audience
        # because those should not change.
        if targeting_dimension != targeting_dimension_enum.AUDIENCE:
            targeting_setting.target_restrictions.append(target_restriction)
        elif not bid_only:
            should_update_targeting_setting = True

            # Add an audience target restriction with bid_only set to
            # true to the targeting setting object. This has the effect
            # of setting the audience target restriction to
            # "Observation". For more details about the targeting
            # setting, visit
            # https://support.google.com/google-ads/answer/7365594.
            new_target_restriction = targeting_setting.target_restrictions.add()
            new_target_restriction.targeting_dimension = (
                targeting_dimension_enum.AUDIENCE
            )
            new_target_restriction.bid_only = True
            # [END update_audience_target_restriction_1]

    # Only update the TargetSetting on the ad group if there is an audience
    # TargetRestriction with bid_only set to false.
    if should_update_targeting_setting:
        _update_targeting_setting(
            client, customer_id, ad_group_id, targeting_setting
        )
    else:
        print("No target restrictions to update.")


# [START update_audience_target_restriction_2]
def _update_targeting_setting(
    client, customer_id, ad_group_id, targeting_setting
):
    """Updates the given TargetingSetting of an ad group.

    Args:
        client: The Google Ads client.
        customer_id: The Google Ads customer ID.
        ad_group_id: The ad group ID for which to update the audience targeting
            restriction.
        targeting_setting: The updated targeting setting.
    """
    # Get the AdGroupService client.
    ad_group_service = client.get_service("AdGroupService")

    # Construct an operation that will update the ad group.
    ad_group_operation = client.get_type("AdGroupOperation")

    # Populate the ad group object with the updated targeting setting.
    ad_group = ad_group_operation.update
    ad_group.resource_name = ad_group_service.ad_group_path(
        customer_id, ad_group_id
    )
    ad_group.targeting_setting.target_restrictions.extend(
        targeting_setting.target_restrictions
    )
    # Use the field_mask utility to derive the update mask. This mask tells the
    # Google Ads API which attributes of the ad group you want to change.
    client.copy_from(
        ad_group_operation.update_mask,
        protobuf_helpers.field_mask(None, ad_group._pb),
    )

    # Send the operation in a mutate request and print the resource name of the
    # updated object.
    mutate_ad_groups_response = ad_group_service.mutate_ad_groups(
        customer_id=customer_id, operations=[ad_group_operation]
    )
    print(
        "Updated targeting setting of ad group with resource name "
        f"'{mutate_ad_groups_response.results[0].resource_name}'; set the "
        "audience target restriction to 'Observation'."
    )
    # [END update_audience_target_restriction_2]


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v8")

    parser = argparse.ArgumentParser(
        description="Updates the audience target restriction of a given ad "
        "group to bid only."
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
        "--ad_group_id",
        type=str,
        required=True,
        help="The ad group ID for which to update the audience targeting "
        "restriction.",
    )
    args = parser.parse_args()

    try:
        main(googleads_client, args.customer_id, args.ad_group_id)
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
