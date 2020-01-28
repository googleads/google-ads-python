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

from google.ads.google_ads.client import GoogleAdsClient
from google.ads.google_ads.errors import GoogleAdsException
from google.ads.google_ads.v2.services.campaign_service_client import (
    CampaignServiceClient
)


def main(client, customer_id, campaign_id):
    """The main method that creates all necessary entities for the example.

    Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID str.
        campaign_id: a campaign ID str.
    """
    # Create the price extension feed item
    price_feed_item = client.get_type('PriceFeedItem', version='v2')
    price_feed_item.type = (
        client.get_type('PriceExtensionTypeEnum', version='v2').SERVICES)
    # Optional: set price qualifier
    price_feed_item.price_qualifier = (
        client.get_type('PriceExtensionPriceQualifierEnum').FROM)
    price_feed_item.tracking_url_template.value = (
        'http://tracker.example.com/?u={lpurl}')
    price_feed_item.language_code.value = 'en'

    # To create a price extension, at least three price offerings are needed.
    price_feed_item.price_offerings.extend([
        create_price_offer(client,
                    'Scrubs',
                    'Body Scrub, Salt Scrub',
                    60000000,  # 60 USD
                    'USD',
                    client.get_type('PriceExtensionPriceUnitEnum').PER_HOUR,
                    'http://www.example.com/scrubs',
                    'http://m.example.com/scrubs'),
        create_price_offer(client,
                    'Hair Cuts',
                    'Once a month',
                    75000000,  # 75 USD
                    'USD',
                    client.get_type('PriceExtensionPriceUnitEnum').PER_MONTH,
                    'http://www.example.com/haircuts',
                    'http://m.example.com/haircuts'),
        create_price_offer(client, 'Skin Care Package',
                    'Four times a month',
                    250000000,  # 250 USD
                    'USD',
                    client.get_type('PriceExtensionPriceUnitEnum').PER_MONTH,
                    'http://www.example.com/skincarepackage')
    ])

    # Create a customer extension setting using the previously created
    # extension feed item. This associates the price extension to your
    # account.
    extension_feed_item_operation = (
        client.get_type('ExtensionFeedItemOperation', version='v2'))
    extension_feed_item = extension_feed_item_operation.create
    extension_feed_item.extension_type = (
        client.get_type('ExtensionTypeEnum').PRICE)
    extension_feed_item.price_feed_item.CopyFrom(price_feed_item)
    extension_feed_item.targeted_campaign.value = (
        CampaignServiceClient.campaign_path(customer_id, campaign_id))
    extension_feed_item.ad_schedules.extend([
        create_ad_schedule_info(client,
            client.get_type('DayOfWeekEnum', version='v2').SUNDAY,
            10,
            client.get_type('MinuteOfHourEnum', version='v2').ZERO,
            18,
            client.get_type('MinuteOfHourEnum', version='v2').ZERO),
        create_ad_schedule_info(client, 
            client.get_type('DayOfWeekEnum', version='v2').SATURDAY,
            10,
            client.get_type('MinuteOfHourEnum', version='v2').ZERO,
            22,
            client.get_type('MinuteOfHourEnum', version='v2').ZERO)
    ])

    # Add the extension
    try:
        feed_service = client.get_service('ExtensionFeedItemService', version='v2')
        # Issues a mutate request to add the customer extension setting and
        # print its information.
        feed_response = (
            feed_service.mutate_extension_feed_items(customer_id, 
                [extension_feed_item_operation])
        )
    except GoogleAdsException as ex:
        print('Request with ID "%s" failed with status "%s" and includes the '
              'following errors:' % (ex.request_id, ex.error.code().name))
        for error in ex.failure.errors:
            print('\tError with message "%s".' % error.message)
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print('\t\tOn field: %s' % field_path_element.field_name)
        sys.exit(1)

    print('Created extension feed with resource name {}.'
          .format(feed_response.results[0].resource_name))


def create_price_offer(client, header, description, price_in_micros,
                       currency_code, unit, in_final_url,
                       in_final_mobile_url=None):
    """Create a price offer."""
    price_offer = client.get_type('PriceOffer', version='v2')
    price_offer.header.value = header
    price_offer.description.value = description
    final_url = price_offer.final_urls.add()
    final_url.value = in_final_url
    price_offer.price.amount_micros.value = price_in_micros
    price_offer.price.currency_code.value = currency_code
    price_offer.unit = unit
    # Optional: set the final mobile URLs
    if in_final_mobile_url:
        final_mobile_url = price_offer.final_mobile_urls.add()
        final_mobile_url.value = in_final_mobile_url
    return price_offer


def create_ad_schedule_info(client, day_of_week, start_hour, start_minute,
                            end_hour, end_minute):
    """Create a new ad schedule info with the specified parameters."""
    ad_schedule_info = client.get_type('AdScheduleInfo', version='v2')
    ad_schedule_info.day_of_week = day_of_week
    ad_schedule_info.start_hour.value = start_hour
    ad_schedule_info.start_minute = start_minute
    ad_schedule_info.end_hour.value = end_hour
    ad_schedule_info.end_minute = end_minute
    return ad_schedule_info


if __name__ == '__main__':
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    google_ads_client = GoogleAdsClient.load_from_storage()

    parser = argparse.ArgumentParser(
        description='Add price extension for the specified customer id')
    # The following argument(s) should be provided to run the example.
    parser.add_argument('-c', '--customer_id', type=str,
                        required=True, help='The Google Ads customer ID')
    parser.add_argument('-i', '--campaign_id', type=str,
                        required=True, help='The campaign ID.')
    args = parser.parse_args()

    main(google_ads_client, args.customer_id, args.campaign_id)
