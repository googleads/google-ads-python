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
"""Adds sitelinks to a campaign.

To create a campaign, run add_campaigns.py.
"""


import argparse
import datetime
import sys
from collections import namedtuple

from google.ads.google_ads.client import GoogleAdsClient
from google.ads.google_ads.errors import GoogleAdsException


_DateRange = namedtuple('_DateRange', ['start_datetime', 'end_datetime'])
_date_format = '%Y-%m-%d %H:%M:%S'


def main(client, customer_id, campaign_id):
    """The main method that creates all necessary entities for the example."""
    # Create an extension setting.
    campaign_service = client.get_service('CampaignService', version='v3')
    campaign_ext_setting_service = client.get_service(
        'CampaignExtensionSettingService', version='v3')

    campaign_resource_name = campaign_service.campaign_path(
        customer_id, campaign_id)

    feed_item_resource_names = _create_extension_feed_items(
        client, customer_id, campaign_resource_name)

    campaign_ext_setting_operation = client.get_type(
        'CampaignExtensionSettingOperation', version='v3')
    extension_type_enum = client.get_type(
        'ExtensionTypeEnum', version='v3')

    campaign_ext_setting = campaign_ext_setting_operation.create
    campaign_ext_setting.campaign.value = campaign_resource_name
    campaign_ext_setting.extension_type = (
        extension_type_enum.SITELINK)

    campaign_ext_setting.extension_feed_items.extend(feed_item_resource_names)

    # Add campaign extension setting with site link feed items.
    try:
        response = (
            campaign_ext_setting_service.mutate_campaign_extension_settings(
                customer_id, [campaign_ext_setting_operation]))
    except GoogleAdsException as ex:
        print(f'Request with ID "{ex.request_id}" failed with status '
              f'"{ex.error.code().name}" and includes the following errors:')
        for error in ex.failure.errors:
            print(f'\tError with message "{error.message}".')
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print('\t\tOn field: {field_path_element.field_name}')
        sys.exit(1)

    print('Created CampaignExtensionSetting: '
          f'"{response.results[0].resource_name}".')


def _create_extension_feed_items(client, customer_id, campaign_resource_name):
    """Helper method that creates extension feed items.

    Args:
        client: a GoogleAdsClient instance.
        customer_id: a str Google Ads customer ID, that the extension feed items
            will be created for.
        campaign_resource_name: a str resource name for the campaign that will
            be tracked by the created extension feed items.

    Returns:
        A list containing StringValue resource names for the created extension
        feed items.
    """
    extension_feed_item_service = client.get_service(
        'ExtensionFeedItemService', version='v3')
    geo_target_constant_service = client.get_service(
        'GeoTargetConstantService', version='v3')
    extension_type_enum = client.get_type('ExtensionTypeEnum')
    feed_item_target_device_enum = client.get_type('FeedItemTargetDeviceEnum')
    day_of_week_enum = client.get_type('DayOfWeekEnum')
    minute_of_hour_enum = client.get_type('MinuteOfHourEnum')

    extension_feed_item_operation1 = client.get_type(
        'ExtensionFeedItemOperation', version='v3')
    extension_feed_item1 = extension_feed_item_operation1.create
    extension_feed_item1.extension_type = extension_type_enum.SITELINK
    extension_feed_item1.sitelink_feed_item.link_text.value = 'Store Hours'
    extension_feed_item1.targeted_campaign.value = campaign_resource_name
    final_url1 = extension_feed_item1.sitelink_feed_item.final_urls.add()
    final_url1.value = 'http://www.example.com/storehours'

    extension_feed_item_operation2 = client.get_type(
        'ExtensionFeedItemOperation', version='v3')
    date_range = _get_thanksgiving_string_date_range()
    extension_feed_item2 = extension_feed_item_operation2.create
    extension_feed_item2.extension_type = extension_type_enum.SITELINK
    extension_feed_item2.sitelink_feed_item.link_text.value = (
        'Thanksgiving Specials')
    extension_feed_item2.targeted_campaign.value = campaign_resource_name
    extension_feed_item2.start_date_time.value = date_range.start_datetime
    extension_feed_item2.end_date_time.value = date_range.end_datetime
    # Targets this sitelink for the United States only.
    # A list of country codes can be referenced here:
    # https://developers.google.com/adwords/api/docs/appendix/geotargeting
    united_states = geo_target_constant_service.geo_target_constant_path(2048)
    extension_feed_item2.targeted_geo_target_constant.value = united_states
    final_url2 = extension_feed_item2.sitelink_feed_item.final_urls.add()
    final_url2.value = 'http://www.example.com/thanksgiving'

    extension_feed_item_operation3 = client.get_type(
        'ExtensionFeedItemOperation', version='v3')
    extension_feed_item3 = extension_feed_item_operation3.create
    extension_feed_item3.extension_type = extension_type_enum.SITELINK
    extension_feed_item3.sitelink_feed_item.link_text.value = 'Wifi available'
    extension_feed_item3.targeted_campaign.value = campaign_resource_name
    extension_feed_item3.device = feed_item_target_device_enum.MOBILE
    final_url3 = extension_feed_item3.sitelink_feed_item.final_urls.add()
    final_url3.value = 'http://www.example.com/mobile/wifi'

    extension_feed_item_operation4 = client.get_type(
        'ExtensionFeedItemOperation', version='v3')
    extension_feed_item4 = extension_feed_item_operation4.create
    extension_feed_item4.extension_type = extension_type_enum.SITELINK
    extension_feed_item4.sitelink_feed_item.link_text.value = 'Happy hours'
    extension_feed_item4.targeted_campaign.value = campaign_resource_name
    extension_feed_item4.device = feed_item_target_device_enum.MOBILE
    final_url4 = extension_feed_item4.sitelink_feed_item.final_urls.add()
    final_url4.value = 'http://www.example.com/happyhours'
    for day_of_week in [day_of_week_enum.MONDAY, day_of_week_enum.TUESDAY,
                        day_of_week_enum.WEDNESDAY, day_of_week_enum.THURSDAY,
                        day_of_week_enum.FRIDAY]:
        _populate_ad_schedule(
            extension_feed_item4.ad_schedules.add(), day_of_week, 18,
            minute_of_hour_enum.ZERO, 21, minute_of_hour_enum.ZERO)

    # Add extension feed items
    try:
        feed_response = (
            extension_feed_item_service.mutate_extension_feed_items(
                customer_id, [extension_feed_item_operation1,
                              extension_feed_item_operation2,
                              extension_feed_item_operation3,
                              extension_feed_item_operation4]))
    except GoogleAdsException as ex:
        print(f'Request with ID "{ex.request_id}" failed with status '
              f'"{ex.error.code().name}" and includes the following errors:')
        for error in ex.failure.errors:
            print(f'\tError with message "{error.message}"')
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print(f'\t\tOn field: {field_path_element.field_name}')
        sys.exit(1)

    print('Created ExtensionFeedItems:')
    for feed_item in feed_response.results:
        print(f'\tResource name: {feed_item.resource_name}')

    resource_names = [result.resource_name for result in feed_response.results]

    return [_to_string_value(client, resource_name) for resource_name in
            resource_names]


def _to_string_value(client, s):
    """Helper method that converts a given str to a StringValue instance."""
    str_val = client.get_type('StringValue')
    str_val.value = s
    return str_val


def _get_thanksgiving_string_date_range():
    """Retrieves a _DateRange with formatted datetime start/end strings."""
    now = datetime.datetime.now()
    start_dt = datetime.datetime(now.year, 11, 20, 0, 0, 0)

    if start_dt < now:
        # Move start_dt to next year if the current date is past November 20th.
        start_dt.year += 1

    end_dt = datetime.datetime(start_dt.year, 11, 27, 23, 59, 59)

    return _DateRange(start_dt.strftime(_date_format),
                      end_dt.strftime(_date_format))


def _populate_ad_schedule(ad_schedule, day_of_week, start_hour, start_minute,
                          end_hour, end_minute):
    """Helper method to populate a given AdScheduleInfo instance."""
    ad_schedule.day_of_week = day_of_week
    ad_schedule.start_hour.value = start_hour
    ad_schedule.start_minute = start_minute
    ad_schedule.end_hour.value = end_hour
    ad_schedule.end_minute = end_minute


if __name__ == '__main__':
    # GoogleAdsClient will read the google-ads.yaml configuration file in the
    # home directory if none is specified.
    google_ads_client = GoogleAdsClient.load_from_storage()

    parser = argparse.ArgumentParser(
        description='Adds sitelinks to the specified campaign.')
    # The following argument(s) should be provided to run the example.
    parser.add_argument('-c', '--customer_id', type=str, required=True,
                        help='The Google Ads customer ID')
    parser.add_argument('-i', '--campaign_id', type=str, required=True,
                        help='The campaign ID sitelinks will be added to.')
    args = parser.parse_args()

    main(google_ads_client, args.customer_id, args.campaign_id)
