#!/usr/bin/env python
# Copyright 2018 Google LLC
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
"""Demonstrates how to add a campaign-level bid modifier for call interactions.
"""


import argparse
import sys

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


def main(client, customer_id, campaign_id, bid_modifier_value):
    campaign_service = client.get_service("CampaignService")
    campaign_bm_service = client.get_service("CampaignBidModifierService")

    # Create campaign bid modifier for call interactions with the specified
    # campaign ID and bid modifier value.
    campaign_bid_modifier_operation = client.get_type(
        "CampaignBidModifierOperation"
    )
    campaign_bid_modifier = campaign_bid_modifier_operation.create

    # Set the campaign.
    campaign_bid_modifier.campaign = campaign_service.campaign_path(
        customer_id, campaign_id
    )

    # Set the bid modifier.
    campaign_bid_modifier.bid_modifier = bid_modifier_value

    # Sets the interaction type.
    campaign_bid_modifier.interaction_type.type_ = client.get_type(
        "InteractionTypeEnum"
    ).InteractionType.CALLS

    # [START mutable_resource]
    # Add the campaign bid modifier. Here we pass the optional parameter
    # response_content_type=MUTABLE_RESOURCE so that the response contains
    # the mutated object and not just its resource name.
    request = client.get_type("MutateCampaignBidModifiersRequest")
    request.customer_id = customer_id
    request.operations = [campaign_bid_modifier_operation]
    request.response_content_type = client.get_type(
        "ResponseContentTypeEnum"
    ).ResponseContentType.MUTABLE_RESOURCE

    campaign_bm_response = campaign_bm_service.mutate_campaign_bid_modifiers(
        request=request
    )

    # The resource returned in the response can be accessed directly in the
    # results list. Its fields can be read directly, and it can also be mutated
    # further and used in subsequent requests, without needing to make
    # additional Get or Search requests.
    mutable_resource = campaign_bm_response.results[0].campaign_bid_modifier
    print(
        "Created campaign bid modifier with resource_name "
        f"'{mutable_resource.resource_name}', criterion ID "
        f"'{mutable_resource.criterion_id}', and bid modifier value "
        f"'{mutable_resource.bid_modifier}', under the campaign with "
        f"resource_name '{mutable_resource.campaign}', "
    )
    # [END mutable_resource]


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v8")

    parser = argparse.ArgumentParser(
        description=(
            "Adds a bid modifier to the specified campaign ID, for "
            "the given customer ID."
        )
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
        "-i", "--campaign_id", type=str, required=True, help="The campaign ID."
    )
    parser.add_argument(
        "-b",
        "--bid_modifier_value",
        type=float,
        required=False,
        default=1.5,
        help="The bid modifier value.",
    )
    args = parser.parse_args()

    try:
        main(
            googleads_client,
            args.customer_id,
            args.campaign_id,
            args.bid_modifier_value,
        )
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
