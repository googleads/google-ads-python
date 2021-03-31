# -*- coding: utf-8 -*-

# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import proto  # type: ignore


from google.ads.googleads.v4.common.types import criteria
from google.ads.googleads.v4.enums.types import (
    ad_network_type as gage_ad_network_type,
)
from google.ads.googleads.v4.enums.types import click_type as gage_click_type
from google.ads.googleads.v4.enums.types import (
    conversion_action_category as gage_conversion_action_category,
)
from google.ads.googleads.v4.enums.types import (
    conversion_attribution_event_type as gage_conversion_attribution_event_type,
)
from google.ads.googleads.v4.enums.types import (
    conversion_lag_bucket as gage_conversion_lag_bucket,
)
from google.ads.googleads.v4.enums.types import (
    conversion_or_adjustment_lag_bucket as gage_conversion_or_adjustment_lag_bucket,
)
from google.ads.googleads.v4.enums.types import day_of_week as gage_day_of_week
from google.ads.googleads.v4.enums.types import device as gage_device
from google.ads.googleads.v4.enums.types import (
    external_conversion_source as gage_external_conversion_source,
)
from google.ads.googleads.v4.enums.types import (
    hotel_date_selection_type as gage_hotel_date_selection_type,
)
from google.ads.googleads.v4.enums.types import (
    hotel_price_bucket as gage_hotel_price_bucket,
)
from google.ads.googleads.v4.enums.types import (
    hotel_rate_type as gage_hotel_rate_type,
)
from google.ads.googleads.v4.enums.types import (
    month_of_year as gage_month_of_year,
)
from google.ads.googleads.v4.enums.types import (
    placeholder_type as gage_placeholder_type,
)
from google.ads.googleads.v4.enums.types import (
    product_channel as gage_product_channel,
)
from google.ads.googleads.v4.enums.types import (
    product_channel_exclusivity as gage_product_channel_exclusivity,
)
from google.ads.googleads.v4.enums.types import (
    product_condition as gage_product_condition,
)
from google.ads.googleads.v4.enums.types import (
    search_engine_results_page_type as gage_search_engine_results_page_type,
)
from google.ads.googleads.v4.enums.types import (
    search_term_match_type as gage_search_term_match_type,
)
from google.ads.googleads.v4.enums.types import slot as gage_slot
from google.protobuf import wrappers_pb2 as wrappers  # type: ignore


__protobuf__ = proto.module(
    package="google.ads.googleads.v4.common",
    marshal="google.ads.googleads.v4",
    manifest={"Segments", "Keyword",},
)


class Segments(proto.Message):
    r"""Segment only fields.

    Attributes:
        ad_network_type (google.ads.googleads.v4.enums.types.AdNetworkTypeEnum.AdNetworkType):
            Ad network type.
        click_type (google.ads.googleads.v4.enums.types.ClickTypeEnum.ClickType):
            Click type.
        conversion_action (google.protobuf.wrappers_pb2.StringValue):
            Resource name of the conversion action.
        conversion_action_category (google.ads.googleads.v4.enums.types.ConversionActionCategoryEnum.ConversionActionCategory):
            Conversion action category.
        conversion_action_name (google.protobuf.wrappers_pb2.StringValue):
            Conversion action name.
        conversion_adjustment (google.protobuf.wrappers_pb2.BoolValue):
            This segments your conversion columns by the
            original conversion and conversion value vs. the
            delta if conversions were adjusted. False row
            has the data as originally stated; While true
            row has the delta between data now and the data
            as originally stated. Summing the two together
            results post-adjustment data.
        conversion_attribution_event_type (google.ads.googleads.v4.enums.types.ConversionAttributionEventTypeEnum.ConversionAttributionEventType):
            Conversion attribution event type.
        conversion_lag_bucket (google.ads.googleads.v4.enums.types.ConversionLagBucketEnum.ConversionLagBucket):
            An enum value representing the number of days
            between the impression and the conversion.
        conversion_or_adjustment_lag_bucket (google.ads.googleads.v4.enums.types.ConversionOrAdjustmentLagBucketEnum.ConversionOrAdjustmentLagBucket):
            An enum value representing the number of days
            between the impression and the conversion or
            between the impression and adjustments to the
            conversion.
        date (google.protobuf.wrappers_pb2.StringValue):
            Date to which metrics apply.
            yyyy-MM-dd format, e.g., 2018-04-17.
        day_of_week (google.ads.googleads.v4.enums.types.DayOfWeekEnum.DayOfWeek):
            Day of the week, e.g., MONDAY.
        device (google.ads.googleads.v4.enums.types.DeviceEnum.Device):
            Device to which metrics apply.
        external_conversion_source (google.ads.googleads.v4.enums.types.ExternalConversionSourceEnum.ExternalConversionSource):
            External conversion source.
        geo_target_airport (google.protobuf.wrappers_pb2.StringValue):
            Resource name of the geo target constant that
            represents an airport.
        geo_target_canton (google.protobuf.wrappers_pb2.StringValue):
            Resource name of the geo target constant that
            represents a canton.
        geo_target_city (google.protobuf.wrappers_pb2.StringValue):
            Resource name of the geo target constant that
            represents a city.
        geo_target_country (google.protobuf.wrappers_pb2.StringValue):
            Resource name of the geo target constant that
            represents a country.
        geo_target_county (google.protobuf.wrappers_pb2.StringValue):
            Resource name of the geo target constant that
            represents a county.
        geo_target_district (google.protobuf.wrappers_pb2.StringValue):
            Resource name of the geo target constant that
            represents a district.
        geo_target_metro (google.protobuf.wrappers_pb2.StringValue):
            Resource name of the geo target constant that
            represents a metro.
        geo_target_most_specific_location (google.protobuf.wrappers_pb2.StringValue):
            Resource name of the geo target constant that
            represents the most specific location.
        geo_target_postal_code (google.protobuf.wrappers_pb2.StringValue):
            Resource name of the geo target constant that
            represents a postal code.
        geo_target_province (google.protobuf.wrappers_pb2.StringValue):
            Resource name of the geo target constant that
            represents a province.
        geo_target_region (google.protobuf.wrappers_pb2.StringValue):
            Resource name of the geo target constant that
            represents a region.
        geo_target_state (google.protobuf.wrappers_pb2.StringValue):
            Resource name of the geo target constant that
            represents a state.
        hotel_booking_window_days (google.protobuf.wrappers_pb2.Int64Value):
            Hotel booking window in days.
        hotel_center_id (google.protobuf.wrappers_pb2.Int64Value):
            Hotel center ID.
        hotel_check_in_date (google.protobuf.wrappers_pb2.StringValue):
            Hotel check-in date. Formatted as yyyy-MM-dd.
        hotel_check_in_day_of_week (google.ads.googleads.v4.enums.types.DayOfWeekEnum.DayOfWeek):
            Hotel check-in day of week.
        hotel_city (google.protobuf.wrappers_pb2.StringValue):
            Hotel city.
        hotel_class (google.protobuf.wrappers_pb2.Int32Value):
            Hotel class.
        hotel_country (google.protobuf.wrappers_pb2.StringValue):
            Hotel country.
        hotel_date_selection_type (google.ads.googleads.v4.enums.types.HotelDateSelectionTypeEnum.HotelDateSelectionType):
            Hotel date selection type.
        hotel_length_of_stay (google.protobuf.wrappers_pb2.Int32Value):
            Hotel length of stay.
        hotel_rate_rule_id (google.protobuf.wrappers_pb2.StringValue):
            Hotel rate rule ID.
        hotel_rate_type (google.ads.googleads.v4.enums.types.HotelRateTypeEnum.HotelRateType):
            Hotel rate type.
        hotel_price_bucket (google.ads.googleads.v4.enums.types.HotelPriceBucketEnum.HotelPriceBucket):
            Hotel price bucket.
        hotel_state (google.protobuf.wrappers_pb2.StringValue):
            Hotel state.
        hour (google.protobuf.wrappers_pb2.Int32Value):
            Hour of day as a number between 0 and 23,
            inclusive.
        interaction_on_this_extension (google.protobuf.wrappers_pb2.BoolValue):
            Only used with feed item metrics.
            Indicates whether the interaction metrics
            occurred on the feed item itself or a different
            extension or ad unit.
        keyword (google.ads.googleads.v4.common.types.Keyword):
            Keyword criterion.
        month (google.protobuf.wrappers_pb2.StringValue):
            Month as represented by the date of the first
            day of a month. Formatted as yyyy-MM-dd.
        month_of_year (google.ads.googleads.v4.enums.types.MonthOfYearEnum.MonthOfYear):
            Month of the year, e.g., January.
        partner_hotel_id (google.protobuf.wrappers_pb2.StringValue):
            Partner hotel ID.
        placeholder_type (google.ads.googleads.v4.enums.types.PlaceholderTypeEnum.PlaceholderType):
            Placeholder type. This is only used with feed
            item metrics.
        product_aggregator_id (google.protobuf.wrappers_pb2.UInt64Value):
            Aggregator ID of the product.
        product_bidding_category_level1 (google.protobuf.wrappers_pb2.StringValue):
            Bidding category (level 1) of the product.
        product_bidding_category_level2 (google.protobuf.wrappers_pb2.StringValue):
            Bidding category (level 2) of the product.
        product_bidding_category_level3 (google.protobuf.wrappers_pb2.StringValue):
            Bidding category (level 3) of the product.
        product_bidding_category_level4 (google.protobuf.wrappers_pb2.StringValue):
            Bidding category (level 4) of the product.
        product_bidding_category_level5 (google.protobuf.wrappers_pb2.StringValue):
            Bidding category (level 5) of the product.
        product_brand (google.protobuf.wrappers_pb2.StringValue):
            Brand of the product.
        product_channel (google.ads.googleads.v4.enums.types.ProductChannelEnum.ProductChannel):
            Channel of the product.
        product_channel_exclusivity (google.ads.googleads.v4.enums.types.ProductChannelExclusivityEnum.ProductChannelExclusivity):
            Channel exclusivity of the product.
        product_condition (google.ads.googleads.v4.enums.types.ProductConditionEnum.ProductCondition):
            Condition of the product.
        product_country (google.protobuf.wrappers_pb2.StringValue):
            Resource name of the geo target constant for
            the country of sale of the product.
        product_custom_attribute0 (google.protobuf.wrappers_pb2.StringValue):
            Custom attribute 0 of the product.
        product_custom_attribute1 (google.protobuf.wrappers_pb2.StringValue):
            Custom attribute 1 of the product.
        product_custom_attribute2 (google.protobuf.wrappers_pb2.StringValue):
            Custom attribute 2 of the product.
        product_custom_attribute3 (google.protobuf.wrappers_pb2.StringValue):
            Custom attribute 3 of the product.
        product_custom_attribute4 (google.protobuf.wrappers_pb2.StringValue):
            Custom attribute 4 of the product.
        product_item_id (google.protobuf.wrappers_pb2.StringValue):
            Item ID of the product.
        product_language (google.protobuf.wrappers_pb2.StringValue):
            Resource name of the language constant for
            the language of the product.
        product_merchant_id (google.protobuf.wrappers_pb2.UInt64Value):
            Merchant ID of the product.
        product_store_id (google.protobuf.wrappers_pb2.StringValue):
            Store ID of the product.
        product_title (google.protobuf.wrappers_pb2.StringValue):
            Title of the product.
        product_type_l1 (google.protobuf.wrappers_pb2.StringValue):
            Type (level 1) of the product.
        product_type_l2 (google.protobuf.wrappers_pb2.StringValue):
            Type (level 2) of the product.
        product_type_l3 (google.protobuf.wrappers_pb2.StringValue):
            Type (level 3) of the product.
        product_type_l4 (google.protobuf.wrappers_pb2.StringValue):
            Type (level 4) of the product.
        product_type_l5 (google.protobuf.wrappers_pb2.StringValue):
            Type (level 5) of the product.
        quarter (google.protobuf.wrappers_pb2.StringValue):
            Quarter as represented by the date of the
            first day of a quarter. Uses the calendar year
            for quarters, e.g., the second quarter of 2018
            starts on 2018-04-01. Formatted as yyyy-MM-dd.
        search_engine_results_page_type (google.ads.googleads.v4.enums.types.SearchEngineResultsPageTypeEnum.SearchEngineResultsPageType):
            Type of the search engine results page.
        search_term_match_type (google.ads.googleads.v4.enums.types.SearchTermMatchTypeEnum.SearchTermMatchType):
            Match type of the keyword that triggered the
            ad, including variants.
        slot (google.ads.googleads.v4.enums.types.SlotEnum.Slot):
            Position of the ad.
        webpage (google.protobuf.wrappers_pb2.StringValue):
            Resource name of the ad group criterion that
            represents webpage criterion.
        week (google.protobuf.wrappers_pb2.StringValue):
            Week as defined as Monday through Sunday, and
            represented by the date of Monday. Formatted as
            yyyy-MM-dd.
        year (google.protobuf.wrappers_pb2.Int32Value):
            Year, formatted as yyyy.
    """

    ad_network_type = proto.Field(
        proto.ENUM,
        number=3,
        enum=gage_ad_network_type.AdNetworkTypeEnum.AdNetworkType,
    )
    click_type = proto.Field(
        proto.ENUM, number=26, enum=gage_click_type.ClickTypeEnum.ClickType,
    )
    conversion_action = proto.Field(
        proto.MESSAGE, number=52, message=wrappers.StringValue,
    )
    conversion_action_category = proto.Field(
        proto.ENUM,
        number=53,
        enum=gage_conversion_action_category.ConversionActionCategoryEnum.ConversionActionCategory,
    )
    conversion_action_name = proto.Field(
        proto.MESSAGE, number=54, message=wrappers.StringValue,
    )
    conversion_adjustment = proto.Field(
        proto.MESSAGE, number=27, message=wrappers.BoolValue,
    )
    conversion_attribution_event_type = proto.Field(
        proto.ENUM,
        number=2,
        enum=gage_conversion_attribution_event_type.ConversionAttributionEventTypeEnum.ConversionAttributionEventType,
    )
    conversion_lag_bucket = proto.Field(
        proto.ENUM,
        number=50,
        enum=gage_conversion_lag_bucket.ConversionLagBucketEnum.ConversionLagBucket,
    )
    conversion_or_adjustment_lag_bucket = proto.Field(
        proto.ENUM,
        number=51,
        enum=gage_conversion_or_adjustment_lag_bucket.ConversionOrAdjustmentLagBucketEnum.ConversionOrAdjustmentLagBucket,
    )
    date = proto.Field(proto.MESSAGE, number=4, message=wrappers.StringValue,)
    day_of_week = proto.Field(
        proto.ENUM, number=5, enum=gage_day_of_week.DayOfWeekEnum.DayOfWeek,
    )
    device = proto.Field(
        proto.ENUM, number=1, enum=gage_device.DeviceEnum.Device,
    )
    external_conversion_source = proto.Field(
        proto.ENUM,
        number=55,
        enum=gage_external_conversion_source.ExternalConversionSourceEnum.ExternalConversionSource,
    )
    geo_target_airport = proto.Field(
        proto.MESSAGE, number=65, message=wrappers.StringValue,
    )
    geo_target_canton = proto.Field(
        proto.MESSAGE, number=76, message=wrappers.StringValue,
    )
    geo_target_city = proto.Field(
        proto.MESSAGE, number=62, message=wrappers.StringValue,
    )
    geo_target_country = proto.Field(
        proto.MESSAGE, number=77, message=wrappers.StringValue,
    )
    geo_target_county = proto.Field(
        proto.MESSAGE, number=68, message=wrappers.StringValue,
    )
    geo_target_district = proto.Field(
        proto.MESSAGE, number=69, message=wrappers.StringValue,
    )
    geo_target_metro = proto.Field(
        proto.MESSAGE, number=63, message=wrappers.StringValue,
    )
    geo_target_most_specific_location = proto.Field(
        proto.MESSAGE, number=72, message=wrappers.StringValue,
    )
    geo_target_postal_code = proto.Field(
        proto.MESSAGE, number=71, message=wrappers.StringValue,
    )
    geo_target_province = proto.Field(
        proto.MESSAGE, number=75, message=wrappers.StringValue,
    )
    geo_target_region = proto.Field(
        proto.MESSAGE, number=64, message=wrappers.StringValue,
    )
    geo_target_state = proto.Field(
        proto.MESSAGE, number=67, message=wrappers.StringValue,
    )
    hotel_booking_window_days = proto.Field(
        proto.MESSAGE, number=6, message=wrappers.Int64Value,
    )
    hotel_center_id = proto.Field(
        proto.MESSAGE, number=7, message=wrappers.Int64Value,
    )
    hotel_check_in_date = proto.Field(
        proto.MESSAGE, number=8, message=wrappers.StringValue,
    )
    hotel_check_in_day_of_week = proto.Field(
        proto.ENUM, number=9, enum=gage_day_of_week.DayOfWeekEnum.DayOfWeek,
    )
    hotel_city = proto.Field(
        proto.MESSAGE, number=10, message=wrappers.StringValue,
    )
    hotel_class = proto.Field(
        proto.MESSAGE, number=11, message=wrappers.Int32Value,
    )
    hotel_country = proto.Field(
        proto.MESSAGE, number=12, message=wrappers.StringValue,
    )
    hotel_date_selection_type = proto.Field(
        proto.ENUM,
        number=13,
        enum=gage_hotel_date_selection_type.HotelDateSelectionTypeEnum.HotelDateSelectionType,
    )
    hotel_length_of_stay = proto.Field(
        proto.MESSAGE, number=14, message=wrappers.Int32Value,
    )
    hotel_rate_rule_id = proto.Field(
        proto.MESSAGE, number=73, message=wrappers.StringValue,
    )
    hotel_rate_type = proto.Field(
        proto.ENUM,
        number=74,
        enum=gage_hotel_rate_type.HotelRateTypeEnum.HotelRateType,
    )
    hotel_price_bucket = proto.Field(
        proto.ENUM,
        number=78,
        enum=gage_hotel_price_bucket.HotelPriceBucketEnum.HotelPriceBucket,
    )
    hotel_state = proto.Field(
        proto.MESSAGE, number=15, message=wrappers.StringValue,
    )
    hour = proto.Field(proto.MESSAGE, number=16, message=wrappers.Int32Value,)
    interaction_on_this_extension = proto.Field(
        proto.MESSAGE, number=49, message=wrappers.BoolValue,
    )
    keyword = proto.Field(proto.MESSAGE, number=61, message="Keyword",)
    month = proto.Field(proto.MESSAGE, number=17, message=wrappers.StringValue,)
    month_of_year = proto.Field(
        proto.ENUM,
        number=18,
        enum=gage_month_of_year.MonthOfYearEnum.MonthOfYear,
    )
    partner_hotel_id = proto.Field(
        proto.MESSAGE, number=19, message=wrappers.StringValue,
    )
    placeholder_type = proto.Field(
        proto.ENUM,
        number=20,
        enum=gage_placeholder_type.PlaceholderTypeEnum.PlaceholderType,
    )
    product_aggregator_id = proto.Field(
        proto.MESSAGE, number=28, message=wrappers.UInt64Value,
    )
    product_bidding_category_level1 = proto.Field(
        proto.MESSAGE, number=56, message=wrappers.StringValue,
    )
    product_bidding_category_level2 = proto.Field(
        proto.MESSAGE, number=57, message=wrappers.StringValue,
    )
    product_bidding_category_level3 = proto.Field(
        proto.MESSAGE, number=58, message=wrappers.StringValue,
    )
    product_bidding_category_level4 = proto.Field(
        proto.MESSAGE, number=59, message=wrappers.StringValue,
    )
    product_bidding_category_level5 = proto.Field(
        proto.MESSAGE, number=60, message=wrappers.StringValue,
    )
    product_brand = proto.Field(
        proto.MESSAGE, number=29, message=wrappers.StringValue,
    )
    product_channel = proto.Field(
        proto.ENUM,
        number=30,
        enum=gage_product_channel.ProductChannelEnum.ProductChannel,
    )
    product_channel_exclusivity = proto.Field(
        proto.ENUM,
        number=31,
        enum=gage_product_channel_exclusivity.ProductChannelExclusivityEnum.ProductChannelExclusivity,
    )
    product_condition = proto.Field(
        proto.ENUM,
        number=32,
        enum=gage_product_condition.ProductConditionEnum.ProductCondition,
    )
    product_country = proto.Field(
        proto.MESSAGE, number=33, message=wrappers.StringValue,
    )
    product_custom_attribute0 = proto.Field(
        proto.MESSAGE, number=34, message=wrappers.StringValue,
    )
    product_custom_attribute1 = proto.Field(
        proto.MESSAGE, number=35, message=wrappers.StringValue,
    )
    product_custom_attribute2 = proto.Field(
        proto.MESSAGE, number=36, message=wrappers.StringValue,
    )
    product_custom_attribute3 = proto.Field(
        proto.MESSAGE, number=37, message=wrappers.StringValue,
    )
    product_custom_attribute4 = proto.Field(
        proto.MESSAGE, number=38, message=wrappers.StringValue,
    )
    product_item_id = proto.Field(
        proto.MESSAGE, number=39, message=wrappers.StringValue,
    )
    product_language = proto.Field(
        proto.MESSAGE, number=40, message=wrappers.StringValue,
    )
    product_merchant_id = proto.Field(
        proto.MESSAGE, number=41, message=wrappers.UInt64Value,
    )
    product_store_id = proto.Field(
        proto.MESSAGE, number=42, message=wrappers.StringValue,
    )
    product_title = proto.Field(
        proto.MESSAGE, number=43, message=wrappers.StringValue,
    )
    product_type_l1 = proto.Field(
        proto.MESSAGE, number=44, message=wrappers.StringValue,
    )
    product_type_l2 = proto.Field(
        proto.MESSAGE, number=45, message=wrappers.StringValue,
    )
    product_type_l3 = proto.Field(
        proto.MESSAGE, number=46, message=wrappers.StringValue,
    )
    product_type_l4 = proto.Field(
        proto.MESSAGE, number=47, message=wrappers.StringValue,
    )
    product_type_l5 = proto.Field(
        proto.MESSAGE, number=48, message=wrappers.StringValue,
    )
    quarter = proto.Field(
        proto.MESSAGE, number=21, message=wrappers.StringValue,
    )
    search_engine_results_page_type = proto.Field(
        proto.ENUM,
        number=70,
        enum=gage_search_engine_results_page_type.SearchEngineResultsPageTypeEnum.SearchEngineResultsPageType,
    )
    search_term_match_type = proto.Field(
        proto.ENUM,
        number=22,
        enum=gage_search_term_match_type.SearchTermMatchTypeEnum.SearchTermMatchType,
    )
    slot = proto.Field(proto.ENUM, number=23, enum=gage_slot.SlotEnum.Slot,)
    webpage = proto.Field(
        proto.MESSAGE, number=66, message=wrappers.StringValue,
    )
    week = proto.Field(proto.MESSAGE, number=24, message=wrappers.StringValue,)
    year = proto.Field(proto.MESSAGE, number=25, message=wrappers.Int32Value,)


class Keyword(proto.Message):
    r"""A Keyword criterion segment.

    Attributes:
        ad_group_criterion (google.protobuf.wrappers_pb2.StringValue):
            The AdGroupCriterion resource name.
        info (google.ads.googleads.v4.common.types.KeywordInfo):
            Keyword info.
    """

    ad_group_criterion = proto.Field(
        proto.MESSAGE, number=1, message=wrappers.StringValue,
    )
    info = proto.Field(proto.MESSAGE, number=2, message=criteria.KeywordInfo,)


__all__ = tuple(sorted(__protobuf__.manifest))
