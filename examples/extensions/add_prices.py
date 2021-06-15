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
"""This example adds a price extension and associates it with an account.

Campaign targeting is also set using the specified campaign ID. To get
campaigns, run basic_operations/get_campaigns.py
"""


import argparse
import sys

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


def main(client, customer_id, campaign_id):
    """The main method that creates all necessary entities for the example."""
    # Create the price extension feed item
    price_feed_item = client.get_type("PriceFeedItem")
    price_feed_item.type_ = client.get_type(
        "PriceExtensionTypeEnum"
    ).PriceExtensionType.SERVICES
    # Optional: set price qualifier
    price_feed_item.price_qualifier = client.get_type(
        "PriceExtensionPriceQualifierEnum"
    ).PriceExtensionPriceQualifier.FROM
    price_feed_item.tracking_url_template = (
        "http://tracker.example.com/?u={lpurl}"
    )
    price_feed_item.language_code = "en"

    # To create a price extension, at least three price offerings are needed.
    price_extension_price_unit_enum = client.get_type(
        "PriceExtensionPriceUnitEnum"
    ).PriceExtensionPriceUnit
    price_feed_item.price_offerings.extend(
        [
            _create_price_offer(
                client,
                "Scrubs",
                "Body Scrub, Salt Scrub",
                60000000,  # 60 USD
                "USD",
                price_extension_price_unit_enum.PER_HOUR,
                "http://www.example.com/scrubs",
                "http://m.example.com/scrubs",
            ),
            _create_price_offer(
                client,
                "Hair Cuts",
                "Once a month",
                75000000,  # 75 USD
                "USD",
                price_extension_price_unit_enum.PER_MONTH,
                "http://www.example.com/haircuts",
                "http://m.example.com/haircuts",
            ),
            _create_price_offer(
                client,
                "Skin Care Package",
                "Four times a month",
                250000000,  # 250 USD
                "USD",
                price_extension_price_unit_enum.PER_MONTH,
                "http://www.example.com/skincarepackage",
            ),
        ]
    )

    # Create a customer extension setting using the previously created
    # extension feed item. This associates the price extension to your
    # account.
    campaign_service = client.get_service("CampaignService")
    extension_feed_item_operation = client.get_type(
        "ExtensionFeedItemOperation"
    )
    extension_feed_item = extension_feed_item_operation.create
    extension_feed_item.extension_type = client.get_type(
        "ExtensionTypeEnum"
    ).ExtensionType.PRICE
    client.copy_from(extension_feed_item.price_feed_item, price_feed_item)
    extension_feed_item.targeted_campaign = campaign_service.campaign_path(
        customer_id, campaign_id
    )
    day_of_week_enum = client.get_type("DayOfWeekEnum").DayOfWeek
    minute_of_hour_enum = client.get_type("MinuteOfHourEnum").MinuteOfHour
    extension_feed_item.ad_schedules.extend(
        [
            _create_ad_schedule_info(
                client,
                day_of_week_enum.SUNDAY,
                10,
                minute_of_hour_enum.ZERO,
                18,
                minute_of_hour_enum.ZERO,
            ),
            _create_ad_schedule_info(
                client,
                day_of_week_enum.SATURDAY,
                10,
                minute_of_hour_enum.ZERO,
                22,
                minute_of_hour_enum.ZERO,
            ),
        ]
    )

    # Add the extension
    feed_service = client.get_service("ExtensionFeedItemService")
    # Issues a mutate request to add the customer extension setting and
    # print its information.
    feed_response = feed_service.mutate_extension_feed_items(
        customer_id=customer_id, operations=[extension_feed_item_operation]
    )

    print(
        "Created extension feed with resource name "
        f"{feed_response.results[0].resource_name}."
    )


def _create_price_offer(
    client,
    header,
    description,
    price_in_micros,
    currency_code,
    unit,
    in_final_url,
    in_final_mobile_url=None,
):
    """Create a price offer."""
    price_offer = client.get_type("PriceOffer")
    price_offer.header = header
    price_offer.description = description
    price_offer.final_urls.append(in_final_url)
    price_offer.price.amount_micros = price_in_micros
    price_offer.price.currency_code = currency_code
    price_offer.unit = unit
    # Optional: set the final mobile URLs
    if in_final_mobile_url:
        price_offer.final_mobile_urls.append(in_final_mobile_url)
    return price_offer


def _create_ad_schedule_info(
    client, day_of_week, start_hour, start_minute, end_hour, end_minute
):
    """Create a new ad schedule info with the specified parameters."""
    ad_schedule_info = client.get_type("AdScheduleInfo")
    ad_schedule_info.day_of_week = day_of_week
    ad_schedule_info.start_hour = start_hour
    ad_schedule_info.start_minute = start_minute
    ad_schedule_info.end_hour = end_hour
    ad_schedule_info.end_minute = end_minute
    return ad_schedule_info


if __name__ == "__main__":
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    googleads_client = GoogleAdsClient.load_from_storage(version="v8")

    parser = argparse.ArgumentParser(
        description="Add price extension for the specified customer id"
    )
    # The following argument(s) should be provided to run the example.
    parser.add_argument(
        "-c",
        "--customer_id",
        type=str,
        required=True,
        help="The Google Ads customer ID",
    )
    parser.add_argument(
        "-i", "--campaign_id", type=str, required=True, help="The campaign ID."
    )
    args = parser.parse_args()

    try:
        main(googleads_client, args.customer_id, args.campaign_id)
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
