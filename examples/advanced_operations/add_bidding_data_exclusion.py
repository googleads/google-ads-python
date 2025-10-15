#!/usr/bin/env python
# Copyright 2021 Google LLC
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
"""Adds a channel-level data exclusion for Smart Bidding.

The exclusion specifically excludes conversions from being used by Smart Bidding
for the time interval specified.

For more information on using data exclusions, see:
https://developers.google.com/google-ads/api/docs/campaigns/bidding/data-exclusions
"""


import argparse
import sys
from uuid import uuid4

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.ads.googleads.v22.resources.types.bidding_data_exclusion import (
    BiddingDataExclusion,
)
from google.ads.googleads.v22.services.services.bidding_data_exclusion_service import (
    BiddingDataExclusionServiceClient,
)
from google.ads.googleads.v22.services.types.bidding_data_exclusion_service import (
    BiddingDataExclusionOperation,
    MutateBiddingDataExclusionsResponse,
)


def main(
    client: GoogleAdsClient,
    customer_id: str,
    start_date_time: str,
    end_date_time: str,
) -> None:
    """The main method that creates all necessary entities for the example.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        start_date_time: a str of the start date for the exclusion period.
        end_date_time: a str of the end date for the exclusion period.
    """
    # [START add_bidding_data_exclusion]
    bidding_data_exclusion_service: BiddingDataExclusionServiceClient = (
        client.get_service("BiddingDataExclusionService")
    )
    operation: BiddingDataExclusionOperation = client.get_type(
        "BiddingDataExclusionOperation"
    )
    bidding_data_exclusion: BiddingDataExclusion = operation.create
    # A unique name is required for every data exclusion
    bidding_data_exclusion.name = f"Data exclusion #{uuid4()}"
    # The CHANNEL scope applies the data exclusion to all campaigns of specific
    # advertising channel types. In this example, the exclusion will only
    # apply to Search campaigns. Use the CAMPAIGN scope to instead limit the
    # scope to specific campaigns.
    bidding_data_exclusion.scope = (
        client.enums.SeasonalityEventScopeEnum.CHANNEL
    )
    bidding_data_exclusion.advertising_channel_types.append(
        client.enums.AdvertisingChannelTypeEnum.SEARCH
    )
    # If setting scope CAMPAIGN, add individual campaign resource name(s)
    # according to the commented out line below.
    #
    # bidding_data_exclusion.campaigns.append(
    #     "INSERT_CAMPAIGN_RESOURCE_NAME_HERE"
    # )

    bidding_data_exclusion.start_date_time = start_date_time
    bidding_data_exclusion.end_date_time = end_date_time

    response: MutateBiddingDataExclusionsResponse = (
        bidding_data_exclusion_service.mutate_bidding_data_exclusions(
            customer_id=customer_id, operations=[operation]
        )
    )

    resource_name: str = response.results[0].resource_name

    print(f"Added data exclusion with resource name: '{resource_name}'")
    # [END add_bidding_data_exclusion]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Adds a data exclusion for conversions in Smart Bidding "
        "for the given time interval."
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
        "-s",
        "--start_date_time",
        type=str,
        required=True,
        help="The start date for the exclusion period, must be in the format: "
        "'yyyy-MM-dd HH:mm:ss'.",
    )
    parser.add_argument(
        "-e",
        "--end_date_time",
        type=str,
        required=True,
        help="The end date for the exclusion period, must be in the format: "
        "'yyyy-MM-dd HH:mm:ss'.",
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
            args.start_date_time,
            args.end_date_time,
        )
    except GoogleAdsException as ex:
        print(
            f'Request with ID "{ex.request_id}" failed with status '
            f'"{ex.error.code().name}" and includes the following errors:'
        )
        for error in ex.failure.errors:
            print(f'Error with message "{error.message}".')
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print(f"\t\tOn field: {field_path_element.field_name}")
        sys.exit(1)
