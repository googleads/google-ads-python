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
"""This demonstrates how to add an ad group bid modifier for mobile devices.

To get ad group bid modifiers, run get_ad_group_bid_modifiers.py
"""


import argparse
import sys

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.ads.googleads.v22.enums.types.device import DeviceEnum
from google.ads.googleads.v22.resources.types.ad_group_bid_modifier import (
    AdGroupBidModifier,
)
from google.ads.googleads.v22.services.services.ad_group_bid_modifier_service import (
    AdGroupBidModifierServiceClient,
)
from google.ads.googleads.v22.services.services.ad_group_service import (
    AdGroupServiceClient,
)
from google.ads.googleads.v22.services.types.ad_group_bid_modifier_service import (
    AdGroupBidModifierOperation,
    MutateAdGroupBidModifiersResponse,
)


# [START add_ad_group_bid_modifier]
def main(
    client: GoogleAdsClient,
    customer_id: str,
    ad_group_id: str,
    bid_modifier_value: float,
) -> None:
    ad_group_service: AdGroupServiceClient = client.get_service(
        "AdGroupService"
    )
    ad_group_bm_service: AdGroupBidModifierServiceClient = client.get_service(
        "AdGroupBidModifierService"
    )

    # Create ad group bid modifier for mobile devices with the specified ad
    # group ID and bid modifier value.
    ad_group_bid_modifier_operation: AdGroupBidModifierOperation = (
        client.get_type("AdGroupBidModifierOperation")
    )
    ad_group_bid_modifier: AdGroupBidModifier = (
        ad_group_bid_modifier_operation.create
    )

    # Set the ad group.
    ad_group_bid_modifier.ad_group = ad_group_service.ad_group_path(
        customer_id, ad_group_id
    )

    # Set the bid modifier.
    ad_group_bid_modifier.bid_modifier = bid_modifier_value

    # Sets the device.
    device_enum: DeviceEnum = client.enums.DeviceEnum
    ad_group_bid_modifier.device.type_ = device_enum.MOBILE

    # Add the ad group bid modifier.
    ad_group_bm_response: MutateAdGroupBidModifiersResponse = (
        ad_group_bm_service.mutate_ad_group_bid_modifiers(
            customer_id=customer_id,
            operations=[ad_group_bid_modifier_operation],
        )
    )
    # [END add_ad_group_bid_modifier]

    print(
        "Created ad group bid modifier: "
        f"{ad_group_bm_response.results[0].resource_name}."
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=(
            "Adds an ad group bid modifier to the specified ad group "
            "ID, for the given customer ID."
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
        "--bid_modifier_value",
        type=float,
        required=False,
        default=1.5,
        help="The bid modifier value.",
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
