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
"""Adds a channel-level seasonality adjustment for Smart Bidding.

The adjustment changes Smart Bidding behavior by the expected change in
conversion rate for the given future time interval.

For more information on using seasonality adjustments, see:
https://developers.google.com/google-ads/api/docs/campaigns/bidding/seasonality-adjustments
"""


import argparse
import sys
from uuid import uuid4

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.ads.googleads.v22.resources.types.bidding_seasonality_adjustment import (
    BiddingSeasonalityAdjustment,
)
from google.ads.googleads.v22.services.services.bidding_seasonality_adjustment_service import (
    BiddingSeasonalityAdjustmentServiceClient,
)
from google.ads.googleads.v22.services.types.bidding_seasonality_adjustment_service import (
    BiddingSeasonalityAdjustmentOperation,
    MutateBiddingSeasonalityAdjustmentsResponse,
)


def main(
    client: GoogleAdsClient,
    customer_id: str,
    start_date_time: str,
    end_date_time: str,
    conversion_rate_modifier: float,
) -> None:
    """The main method that creates all necessary entities for the example.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        start_date_time: a str of the start date for the exclusion period.
        end_date_time: a str of the end date for the exclusion period.
        conversion_rate_modifier: the modifier to apply to conversions during
            the given time period.
    """
    # [START add_bidding_seasonality_adjustment]
    bidding_seasonality_adjustment_service: (
        BiddingSeasonalityAdjustmentServiceClient
    ) = client.get_service("BiddingSeasonalityAdjustmentService")
    operation: BiddingSeasonalityAdjustmentOperation = client.get_type(
        "BiddingSeasonalityAdjustmentOperation"
    )
    bidding_seasonality_adjustment: BiddingSeasonalityAdjustment = (
        operation.create
    )
    # A unique name is required for every seasonality adjustment.
    bidding_seasonality_adjustment.name = f"Seasonality adjustment #{uuid4()}"
    # The CHANNEL scope applies the conversion_rate_modifier to all campaigns of
    # specific advertising channel types. In this example, the
    # conversion_rate_modifier will only apply to Search campaigns. Use the
    # CAMPAIGN scope to instead limit the scope to specific campaigns.
    bidding_seasonality_adjustment.scope = (
        client.enums.SeasonalityEventScopeEnum.CHANNEL
    )
    bidding_seasonality_adjustment.advertising_channel_types.append(
        client.enums.AdvertisingChannelTypeEnum.SEARCH
    )
    # If setting scope CAMPAIGN, add individual campaign resource name(s)
    # according to the commented out line below.
    #
    # bidding_seasonality_adjustment.campaigns.append(
    #     "INSERT_CAMPAIGN_RESOURCE_NAME_HERE"
    # )

    bidding_seasonality_adjustment.start_date_time = start_date_time
    bidding_seasonality_adjustment.end_date_time = end_date_time
    # The conversion_rate_modifier is the expected future conversion rate
    # change. When this field is unset or set to 1.0, no adjustment will be
    # applied to traffic. The allowed range is 0.1 to 10.0.
    bidding_seasonality_adjustment.conversion_rate_modifier = (
        conversion_rate_modifier
    )

    response: MutateBiddingSeasonalityAdjustmentsResponse = (
        bidding_seasonality_adjustment_service.mutate_bidding_seasonality_adjustments(
            customer_id=customer_id, operations=[operation]
        )
    )

    resource_name: str = response.results[0].resource_name

    print(f"Added seasonality adjustment with resource name: '{resource_name}'")
    # [END add_bidding_seasonality_adjustment]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Adds a seasonality adjustment for conversions in Smart "
        "Bidding for the given time interval."
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
        help="The start date for the adjustment period, must be in the format: "
        "'yyyy-MM-dd HH:mm:ss'.",
    )
    parser.add_argument(
        "-e",
        "--end_date_time",
        type=str,
        required=True,
        help="The end date for the adjustment period, must be in the format: "
        "'yyyy-MM-dd HH:mm:ss'.",
    )
    parser.add_argument(
        "-m",
        "--conversion_rate_modifier",
        type=float,
        required=True,
        help="The conversion rate modifier that will be applied during the "
        "adjustment period. This value must be in the range 0.1 to 10.0.",
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
            args.conversion_rate_modifier,
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
