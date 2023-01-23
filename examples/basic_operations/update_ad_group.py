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
"""This example updates an ad group.

To get ad groups, run get_ad_groups.py.
"""


import argparse
import sys

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.api_core import protobuf_helpers


# [START update_ad_group]
def main(client, customer_id, ad_group_id, cpc_bid_micro_amount):
    ad_group_service = client.get_service("AdGroupService")

    # Create ad group operation.
    ad_group_operation = client.get_type("AdGroupOperation")
    ad_group = ad_group_operation.update
    ad_group.resource_name = ad_group_service.ad_group_path(
        customer_id, ad_group_id
    )
    ad_group.status = client.enums.AdGroupStatusEnum.PAUSED
    ad_group.cpc_bid_micros = cpc_bid_micro_amount
    client.copy_from(
        ad_group_operation.update_mask,
        protobuf_helpers.field_mask(None, ad_group._pb),
    )

    # Update the ad group.
    ad_group_response = ad_group_service.mutate_ad_groups(
        customer_id=customer_id, operations=[ad_group_operation]
    )

    print(f"Updated ad group {ad_group_response.results[0].resource_name}.")
    # [END update_ad_group]


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v12")

    parser = argparse.ArgumentParser(
        description=(
            "Updates an ad group for specified customer and campaign "
            "id with the given bid micro amount."
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
        "-a", "--ad_group_id", type=str, required=True, help="The ad group ID."
    )
    parser.add_argument(
        "-b",
        "--cpc_bid_micro_amount",
        type=int,
        required=True,
        help="The cpc bid micro amount.",
    )
    args = parser.parse_args()

    try:
        main(
            googleads_client,
            args.customer_id,
            args.ad_group_id,
            args.cpc_bid_micro_amount,
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
