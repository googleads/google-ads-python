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


from google.ads.googleads.v4.enums.types import age_range_type
from google.ads.googleads.v4.enums.types import app_payment_model_type
from google.ads.googleads.v4.enums.types import content_label_type
from google.ads.googleads.v4.enums.types import day_of_week as gage_day_of_week
from google.ads.googleads.v4.enums.types import device
from google.ads.googleads.v4.enums.types import gender_type
from google.ads.googleads.v4.enums.types import hotel_date_selection_type
from google.ads.googleads.v4.enums.types import income_range_type
from google.ads.googleads.v4.enums.types import interaction_type
from google.ads.googleads.v4.enums.types import keyword_match_type
from google.ads.googleads.v4.enums.types import listing_group_type
from google.ads.googleads.v4.enums.types import location_group_radius_units
from google.ads.googleads.v4.enums.types import minute_of_hour
from google.ads.googleads.v4.enums.types import parental_status_type
from google.ads.googleads.v4.enums.types import preferred_content_type
from google.ads.googleads.v4.enums.types import product_bidding_category_level
from google.ads.googleads.v4.enums.types import (
    product_channel as gage_product_channel,
)
from google.ads.googleads.v4.enums.types import (
    product_channel_exclusivity as gage_product_channel_exclusivity,
)
from google.ads.googleads.v4.enums.types import (
    product_condition as gage_product_condition,
)
from google.ads.googleads.v4.enums.types import product_custom_attribute_index
from google.ads.googleads.v4.enums.types import product_type_level
from google.ads.googleads.v4.enums.types import proximity_radius_units
from google.ads.googleads.v4.enums.types import webpage_condition_operand
from google.ads.googleads.v4.enums.types import webpage_condition_operator
from google.protobuf import wrappers_pb2 as wrappers  # type: ignore


__protobuf__ = proto.module(
    package="google.ads.googleads.v4.common",
    marshal="google.ads.googleads.v4",
    manifest={
        "KeywordInfo",
        "PlacementInfo",
        "MobileAppCategoryInfo",
        "MobileApplicationInfo",
        "LocationInfo",
        "DeviceInfo",
        "PreferredContentInfo",
        "ListingGroupInfo",
        "ListingScopeInfo",
        "ListingDimensionInfo",
        "HotelIdInfo",
        "HotelClassInfo",
        "HotelCountryRegionInfo",
        "HotelStateInfo",
        "HotelCityInfo",
        "ProductBiddingCategoryInfo",
        "ProductBrandInfo",
        "ProductChannelInfo",
        "ProductChannelExclusivityInfo",
        "ProductConditionInfo",
        "ProductCustomAttributeInfo",
        "ProductItemIdInfo",
        "ProductTypeInfo",
        "UnknownListingDimensionInfo",
        "HotelDateSelectionTypeInfo",
        "HotelAdvanceBookingWindowInfo",
        "HotelLengthOfStayInfo",
        "HotelCheckInDayInfo",
        "InteractionTypeInfo",
        "AdScheduleInfo",
        "AgeRangeInfo",
        "GenderInfo",
        "IncomeRangeInfo",
        "ParentalStatusInfo",
        "YouTubeVideoInfo",
        "YouTubeChannelInfo",
        "UserListInfo",
        "ProximityInfo",
        "GeoPointInfo",
        "AddressInfo",
        "TopicInfo",
        "LanguageInfo",
        "IpBlockInfo",
        "ContentLabelInfo",
        "CarrierInfo",
        "UserInterestInfo",
        "WebpageInfo",
        "WebpageConditionInfo",
        "OperatingSystemVersionInfo",
        "AppPaymentModelInfo",
        "MobileDeviceInfo",
        "CustomAffinityInfo",
        "CustomIntentInfo",
        "LocationGroupInfo",
    },
)


class KeywordInfo(proto.Message):
    r"""A keyword criterion.

    Attributes:
        text (google.protobuf.wrappers_pb2.StringValue):
            The text of the keyword (at most 80
            characters and 10 words).
        match_type (google.ads.googleads.v4.enums.types.KeywordMatchTypeEnum.KeywordMatchType):
            The match type of the keyword.
    """

    text = proto.Field(proto.MESSAGE, number=1, message=wrappers.StringValue,)
    match_type = proto.Field(
        proto.ENUM,
        number=2,
        enum=keyword_match_type.KeywordMatchTypeEnum.KeywordMatchType,
    )


class PlacementInfo(proto.Message):
    r"""A placement criterion. This can be used to modify bids for
    sites when targeting the content network.

    Attributes:
        url (google.protobuf.wrappers_pb2.StringValue):
            URL of the placement.
            For example, "http://www.domain.com".
    """

    url = proto.Field(proto.MESSAGE, number=1, message=wrappers.StringValue,)


class MobileAppCategoryInfo(proto.Message):
    r"""A mobile app category criterion.

    Attributes:
        mobile_app_category_constant (google.protobuf.wrappers_pb2.StringValue):
            The mobile app category constant resource
            name.
    """

    mobile_app_category_constant = proto.Field(
        proto.MESSAGE, number=1, message=wrappers.StringValue,
    )


class MobileApplicationInfo(proto.Message):
    r"""A mobile application criterion.

    Attributes:
        app_id (google.protobuf.wrappers_pb2.StringValue):
            A string that uniquely identifies a mobile application to
            Google Ads API. The format of this string is
            "{platform}-{platform_native_id}", where platform is "1" for
            iOS apps and "2" for Android apps, and where
            platform_native_id is the mobile application identifier
            native to the corresponding platform. For iOS, this native
            identifier is the 9 digit string that appears at the end of
            an App Store URL (e.g., "476943146" for "Flood-It! 2" whose
            App Store link is
            "http://itunes.apple.com/us/app/flood-it!-2/id476943146").
            For Android, this native identifier is the application's
            package name (e.g., "com.labpixies.colordrips" for "Color
            Drips" given Google Play link
            "https://play.google.com/store/apps/details?id=com.labpixies.colordrips").
            A well formed app id for Google Ads API would thus be
            "1-476943146" for iOS and "2-com.labpixies.colordrips" for
            Android. This field is required and must be set in CREATE
            operations.
        name (google.protobuf.wrappers_pb2.StringValue):
            Name of this mobile application.
    """

    app_id = proto.Field(proto.MESSAGE, number=2, message=wrappers.StringValue,)
    name = proto.Field(proto.MESSAGE, number=3, message=wrappers.StringValue,)


class LocationInfo(proto.Message):
    r"""A location criterion.

    Attributes:
        geo_target_constant (google.protobuf.wrappers_pb2.StringValue):
            The geo target constant resource name.
    """

    geo_target_constant = proto.Field(
        proto.MESSAGE, number=1, message=wrappers.StringValue,
    )


class DeviceInfo(proto.Message):
    r"""A device criterion.

    Attributes:
        type_ (google.ads.googleads.v4.enums.types.DeviceEnum.Device):
            Type of the device.
    """

    type_ = proto.Field(proto.ENUM, number=1, enum=device.DeviceEnum.Device,)


class PreferredContentInfo(proto.Message):
    r"""A preferred content criterion.

    Attributes:
        type_ (google.ads.googleads.v4.enums.types.PreferredContentTypeEnum.PreferredContentType):
            Type of the preferred content.
    """

    type_ = proto.Field(
        proto.ENUM,
        number=2,
        enum=preferred_content_type.PreferredContentTypeEnum.PreferredContentType,
    )


class ListingGroupInfo(proto.Message):
    r"""A listing group criterion.

    Attributes:
        type_ (google.ads.googleads.v4.enums.types.ListingGroupTypeEnum.ListingGroupType):
            Type of the listing group.
        case_value (google.ads.googleads.v4.common.types.ListingDimensionInfo):
            Dimension value with which this listing group
            is refining its parent. Undefined for the root
            group.
        parent_ad_group_criterion (google.protobuf.wrappers_pb2.StringValue):
            Resource name of ad group criterion which is
            the parent listing group subdivision. Null for
            the root group.
    """

    type_ = proto.Field(
        proto.ENUM,
        number=1,
        enum=listing_group_type.ListingGroupTypeEnum.ListingGroupType,
    )
    case_value = proto.Field(
        proto.MESSAGE, number=2, message="ListingDimensionInfo",
    )
    parent_ad_group_criterion = proto.Field(
        proto.MESSAGE, number=3, message=wrappers.StringValue,
    )


class ListingScopeInfo(proto.Message):
    r"""A listing scope criterion.

    Attributes:
        dimensions (Sequence[google.ads.googleads.v4.common.types.ListingDimensionInfo]):
            Scope of the campaign criterion.
    """

    dimensions = proto.RepeatedField(
        proto.MESSAGE, number=2, message="ListingDimensionInfo",
    )


class ListingDimensionInfo(proto.Message):
    r"""Listing dimensions for listing group criterion.

    Attributes:
        hotel_id (google.ads.googleads.v4.common.types.HotelIdInfo):
            Advertiser-specific hotel ID.
        hotel_class (google.ads.googleads.v4.common.types.HotelClassInfo):
            Class of the hotel as a number of stars 1 to
            5.
        hotel_country_region (google.ads.googleads.v4.common.types.HotelCountryRegionInfo):
            Country or Region the hotel is located in.
        hotel_state (google.ads.googleads.v4.common.types.HotelStateInfo):
            State the hotel is located in.
        hotel_city (google.ads.googleads.v4.common.types.HotelCityInfo):
            City the hotel is located in.
        product_bidding_category (google.ads.googleads.v4.common.types.ProductBiddingCategoryInfo):
            Bidding category of a product offer.
        product_brand (google.ads.googleads.v4.common.types.ProductBrandInfo):
            Brand of a product offer.
        product_channel (google.ads.googleads.v4.common.types.ProductChannelInfo):
            Locality of a product offer.
        product_channel_exclusivity (google.ads.googleads.v4.common.types.ProductChannelExclusivityInfo):
            Availability of a product offer.
        product_condition (google.ads.googleads.v4.common.types.ProductConditionInfo):
            Condition of a product offer.
        product_custom_attribute (google.ads.googleads.v4.common.types.ProductCustomAttributeInfo):
            Custom attribute of a product offer.
        product_item_id (google.ads.googleads.v4.common.types.ProductItemIdInfo):
            Item id of a product offer.
        product_type (google.ads.googleads.v4.common.types.ProductTypeInfo):
            Type of a product offer.
        unknown_listing_dimension (google.ads.googleads.v4.common.types.UnknownListingDimensionInfo):
            Unknown dimension. Set when no other listing
            dimension is set.
    """

    hotel_id = proto.Field(
        proto.MESSAGE, number=2, oneof="dimension", message="HotelIdInfo",
    )
    hotel_class = proto.Field(
        proto.MESSAGE, number=3, oneof="dimension", message="HotelClassInfo",
    )
    hotel_country_region = proto.Field(
        proto.MESSAGE,
        number=4,
        oneof="dimension",
        message="HotelCountryRegionInfo",
    )
    hotel_state = proto.Field(
        proto.MESSAGE, number=5, oneof="dimension", message="HotelStateInfo",
    )
    hotel_city = proto.Field(
        proto.MESSAGE, number=6, oneof="dimension", message="HotelCityInfo",
    )
    product_bidding_category = proto.Field(
        proto.MESSAGE,
        number=13,
        oneof="dimension",
        message="ProductBiddingCategoryInfo",
    )
    product_brand = proto.Field(
        proto.MESSAGE, number=15, oneof="dimension", message="ProductBrandInfo",
    )
    product_channel = proto.Field(
        proto.MESSAGE,
        number=8,
        oneof="dimension",
        message="ProductChannelInfo",
    )
    product_channel_exclusivity = proto.Field(
        proto.MESSAGE,
        number=9,
        oneof="dimension",
        message="ProductChannelExclusivityInfo",
    )
    product_condition = proto.Field(
        proto.MESSAGE,
        number=10,
        oneof="dimension",
        message="ProductConditionInfo",
    )
    product_custom_attribute = proto.Field(
        proto.MESSAGE,
        number=16,
        oneof="dimension",
        message="ProductCustomAttributeInfo",
    )
    product_item_id = proto.Field(
        proto.MESSAGE,
        number=11,
        oneof="dimension",
        message="ProductItemIdInfo",
    )
    product_type = proto.Field(
        proto.MESSAGE, number=12, oneof="dimension", message="ProductTypeInfo",
    )
    unknown_listing_dimension = proto.Field(
        proto.MESSAGE,
        number=14,
        oneof="dimension",
        message="UnknownListingDimensionInfo",
    )


class HotelIdInfo(proto.Message):
    r"""Advertiser-specific hotel ID.

    Attributes:
        value (google.protobuf.wrappers_pb2.StringValue):
            String value of the hotel ID.
    """

    value = proto.Field(proto.MESSAGE, number=1, message=wrappers.StringValue,)


class HotelClassInfo(proto.Message):
    r"""Class of the hotel as a number of stars 1 to 5.

    Attributes:
        value (google.protobuf.wrappers_pb2.Int64Value):
            Long value of the hotel class.
    """

    value = proto.Field(proto.MESSAGE, number=1, message=wrappers.Int64Value,)


class HotelCountryRegionInfo(proto.Message):
    r"""Country or Region the hotel is located in.

    Attributes:
        country_region_criterion (google.protobuf.wrappers_pb2.StringValue):
            The Geo Target Constant resource name.
    """

    country_region_criterion = proto.Field(
        proto.MESSAGE, number=1, message=wrappers.StringValue,
    )


class HotelStateInfo(proto.Message):
    r"""State the hotel is located in.

    Attributes:
        state_criterion (google.protobuf.wrappers_pb2.StringValue):
            The Geo Target Constant resource name.
    """

    state_criterion = proto.Field(
        proto.MESSAGE, number=1, message=wrappers.StringValue,
    )


class HotelCityInfo(proto.Message):
    r"""City the hotel is located in.

    Attributes:
        city_criterion (google.protobuf.wrappers_pb2.StringValue):
            The Geo Target Constant resource name.
    """

    city_criterion = proto.Field(
        proto.MESSAGE, number=1, message=wrappers.StringValue,
    )


class ProductBiddingCategoryInfo(proto.Message):
    r"""Bidding category of a product offer.

    Attributes:
        id (google.protobuf.wrappers_pb2.Int64Value):
            ID of the product bidding category.

            This ID is equivalent to the google_product_category ID as
            described in this article:
            https://support.google.com/merchants/answer/6324436
        country_code (google.protobuf.wrappers_pb2.StringValue):
            Two-letter upper-case country code of the product bidding
            category. It must match the
            campaign.shopping_setting.sales_country field.
        level (google.ads.googleads.v4.enums.types.ProductBiddingCategoryLevelEnum.ProductBiddingCategoryLevel):
            Level of the product bidding category.
    """

    id = proto.Field(proto.MESSAGE, number=1, message=wrappers.Int64Value,)
    country_code = proto.Field(
        proto.MESSAGE, number=2, message=wrappers.StringValue,
    )
    level = proto.Field(
        proto.ENUM,
        number=3,
        enum=product_bidding_category_level.ProductBiddingCategoryLevelEnum.ProductBiddingCategoryLevel,
    )


class ProductBrandInfo(proto.Message):
    r"""Brand of the product.

    Attributes:
        value (google.protobuf.wrappers_pb2.StringValue):
            String value of the product brand.
    """

    value = proto.Field(proto.MESSAGE, number=1, message=wrappers.StringValue,)


class ProductChannelInfo(proto.Message):
    r"""Locality of a product offer.

    Attributes:
        channel (google.ads.googleads.v4.enums.types.ProductChannelEnum.ProductChannel):
            Value of the locality.
    """

    channel = proto.Field(
        proto.ENUM,
        number=1,
        enum=gage_product_channel.ProductChannelEnum.ProductChannel,
    )


class ProductChannelExclusivityInfo(proto.Message):
    r"""Availability of a product offer.

    Attributes:
        channel_exclusivity (google.ads.googleads.v4.enums.types.ProductChannelExclusivityEnum.ProductChannelExclusivity):
            Value of the availability.
    """

    channel_exclusivity = proto.Field(
        proto.ENUM,
        number=1,
        enum=gage_product_channel_exclusivity.ProductChannelExclusivityEnum.ProductChannelExclusivity,
    )


class ProductConditionInfo(proto.Message):
    r"""Condition of a product offer.

    Attributes:
        condition (google.ads.googleads.v4.enums.types.ProductConditionEnum.ProductCondition):
            Value of the condition.
    """

    condition = proto.Field(
        proto.ENUM,
        number=1,
        enum=gage_product_condition.ProductConditionEnum.ProductCondition,
    )


class ProductCustomAttributeInfo(proto.Message):
    r"""Custom attribute of a product offer.

    Attributes:
        value (google.protobuf.wrappers_pb2.StringValue):
            String value of the product custom attribute.
        index (google.ads.googleads.v4.enums.types.ProductCustomAttributeIndexEnum.ProductCustomAttributeIndex):
            Indicates the index of the custom attribute.
    """

    value = proto.Field(proto.MESSAGE, number=1, message=wrappers.StringValue,)
    index = proto.Field(
        proto.ENUM,
        number=2,
        enum=product_custom_attribute_index.ProductCustomAttributeIndexEnum.ProductCustomAttributeIndex,
    )


class ProductItemIdInfo(proto.Message):
    r"""Item id of a product offer.

    Attributes:
        value (google.protobuf.wrappers_pb2.StringValue):
            Value of the id.
    """

    value = proto.Field(proto.MESSAGE, number=1, message=wrappers.StringValue,)


class ProductTypeInfo(proto.Message):
    r"""Type of a product offer.

    Attributes:
        value (google.protobuf.wrappers_pb2.StringValue):
            Value of the type.
        level (google.ads.googleads.v4.enums.types.ProductTypeLevelEnum.ProductTypeLevel):
            Level of the type.
    """

    value = proto.Field(proto.MESSAGE, number=1, message=wrappers.StringValue,)
    level = proto.Field(
        proto.ENUM,
        number=2,
        enum=product_type_level.ProductTypeLevelEnum.ProductTypeLevel,
    )


class UnknownListingDimensionInfo(proto.Message):
    r"""Unknown listing dimension."""


class HotelDateSelectionTypeInfo(proto.Message):
    r"""Criterion for hotel date selection (default dates vs. user
    selected).

    Attributes:
        type_ (google.ads.googleads.v4.enums.types.HotelDateSelectionTypeEnum.HotelDateSelectionType):
            Type of the hotel date selection
    """

    type_ = proto.Field(
        proto.ENUM,
        number=1,
        enum=hotel_date_selection_type.HotelDateSelectionTypeEnum.HotelDateSelectionType,
    )


class HotelAdvanceBookingWindowInfo(proto.Message):
    r"""Criterion for number of days prior to the stay the booking is
    being made.

    Attributes:
        min_days (google.protobuf.wrappers_pb2.Int64Value):
            Low end of the number of days prior to the
            stay.
        max_days (google.protobuf.wrappers_pb2.Int64Value):
            High end of the number of days prior to the
            stay.
    """

    min_days = proto.Field(
        proto.MESSAGE, number=1, message=wrappers.Int64Value,
    )
    max_days = proto.Field(
        proto.MESSAGE, number=2, message=wrappers.Int64Value,
    )


class HotelLengthOfStayInfo(proto.Message):
    r"""Criterion for length of hotel stay in nights.

    Attributes:
        min_nights (google.protobuf.wrappers_pb2.Int64Value):
            Low end of the number of nights in the stay.
        max_nights (google.protobuf.wrappers_pb2.Int64Value):
            High end of the number of nights in the stay.
    """

    min_nights = proto.Field(
        proto.MESSAGE, number=1, message=wrappers.Int64Value,
    )
    max_nights = proto.Field(
        proto.MESSAGE, number=2, message=wrappers.Int64Value,
    )


class HotelCheckInDayInfo(proto.Message):
    r"""Criterion for day of the week the booking is for.

    Attributes:
        day_of_week (google.ads.googleads.v4.enums.types.DayOfWeekEnum.DayOfWeek):
            The day of the week.
    """

    day_of_week = proto.Field(
        proto.ENUM, number=1, enum=gage_day_of_week.DayOfWeekEnum.DayOfWeek,
    )


class InteractionTypeInfo(proto.Message):
    r"""Criterion for Interaction Type.

    Attributes:
        type_ (google.ads.googleads.v4.enums.types.InteractionTypeEnum.InteractionType):
            The interaction type.
    """

    type_ = proto.Field(
        proto.ENUM,
        number=1,
        enum=interaction_type.InteractionTypeEnum.InteractionType,
    )


class AdScheduleInfo(proto.Message):
    r"""Represents an AdSchedule criterion.
    AdSchedule is specified as the day of the week and a time
    interval within which ads will be shown.

    No more than six AdSchedules can be added for the same day.

    Attributes:
        start_minute (google.ads.googleads.v4.enums.types.MinuteOfHourEnum.MinuteOfHour):
            Minutes after the start hour at which this
            schedule starts.
            This field is required for CREATE operations and
            is prohibited on UPDATE operations.
        end_minute (google.ads.googleads.v4.enums.types.MinuteOfHourEnum.MinuteOfHour):
            Minutes after the end hour at which this
            schedule ends. The schedule is exclusive of the
            end minute.
            This field is required for CREATE operations and
            is prohibited on UPDATE operations.
        start_hour (google.protobuf.wrappers_pb2.Int32Value):
            Starting hour in 24 hour time.
            This field must be between 0 and 23, inclusive.
            This field is required for CREATE operations and
            is prohibited on UPDATE operations.
        end_hour (google.protobuf.wrappers_pb2.Int32Value):
            Ending hour in 24 hour time; 24 signifies end
            of the day. This field must be between 0 and 24,
            inclusive.
            This field is required for CREATE operations and
            is prohibited on UPDATE operations.
        day_of_week (google.ads.googleads.v4.enums.types.DayOfWeekEnum.DayOfWeek):
            Day of the week the schedule applies to.
            This field is required for CREATE operations and
            is prohibited on UPDATE operations.
    """

    start_minute = proto.Field(
        proto.ENUM, number=1, enum=minute_of_hour.MinuteOfHourEnum.MinuteOfHour,
    )
    end_minute = proto.Field(
        proto.ENUM, number=2, enum=minute_of_hour.MinuteOfHourEnum.MinuteOfHour,
    )
    start_hour = proto.Field(
        proto.MESSAGE, number=3, message=wrappers.Int32Value,
    )
    end_hour = proto.Field(
        proto.MESSAGE, number=4, message=wrappers.Int32Value,
    )
    day_of_week = proto.Field(
        proto.ENUM, number=5, enum=gage_day_of_week.DayOfWeekEnum.DayOfWeek,
    )


class AgeRangeInfo(proto.Message):
    r"""An age range criterion.

    Attributes:
        type_ (google.ads.googleads.v4.enums.types.AgeRangeTypeEnum.AgeRangeType):
            Type of the age range.
    """

    type_ = proto.Field(
        proto.ENUM, number=1, enum=age_range_type.AgeRangeTypeEnum.AgeRangeType,
    )


class GenderInfo(proto.Message):
    r"""A gender criterion.

    Attributes:
        type_ (google.ads.googleads.v4.enums.types.GenderTypeEnum.GenderType):
            Type of the gender.
    """

    type_ = proto.Field(
        proto.ENUM, number=1, enum=gender_type.GenderTypeEnum.GenderType,
    )


class IncomeRangeInfo(proto.Message):
    r"""An income range criterion.

    Attributes:
        type_ (google.ads.googleads.v4.enums.types.IncomeRangeTypeEnum.IncomeRangeType):
            Type of the income range.
    """

    type_ = proto.Field(
        proto.ENUM,
        number=1,
        enum=income_range_type.IncomeRangeTypeEnum.IncomeRangeType,
    )


class ParentalStatusInfo(proto.Message):
    r"""A parental status criterion.

    Attributes:
        type_ (google.ads.googleads.v4.enums.types.ParentalStatusTypeEnum.ParentalStatusType):
            Type of the parental status.
    """

    type_ = proto.Field(
        proto.ENUM,
        number=1,
        enum=parental_status_type.ParentalStatusTypeEnum.ParentalStatusType,
    )


class YouTubeVideoInfo(proto.Message):
    r"""A YouTube Video criterion.

    Attributes:
        video_id (google.protobuf.wrappers_pb2.StringValue):
            YouTube video id as it appears on the YouTube
            watch page.
    """

    video_id = proto.Field(
        proto.MESSAGE, number=1, message=wrappers.StringValue,
    )


class YouTubeChannelInfo(proto.Message):
    r"""A YouTube Channel criterion.

    Attributes:
        channel_id (google.protobuf.wrappers_pb2.StringValue):
            The YouTube uploader channel id or the
            channel code of a YouTube channel.
    """

    channel_id = proto.Field(
        proto.MESSAGE, number=1, message=wrappers.StringValue,
    )


class UserListInfo(proto.Message):
    r"""A User List criterion. Represents a user list that is defined
    by the advertiser to be targeted.

    Attributes:
        user_list (google.protobuf.wrappers_pb2.StringValue):
            The User List resource name.
    """

    user_list = proto.Field(
        proto.MESSAGE, number=1, message=wrappers.StringValue,
    )


class ProximityInfo(proto.Message):
    r"""A Proximity criterion. The geo point and radius determine
    what geographical area is included. The address is a description
    of the geo point that does not affect ad serving.

    There are two ways to create a proximity. First, by setting an
    address and radius. The geo point will be automatically
    computed. Second, by setting a geo point and radius. The address
    is an optional label that won't be validated.

    Attributes:
        geo_point (google.ads.googleads.v4.common.types.GeoPointInfo):
            Latitude and longitude.
        radius (google.protobuf.wrappers_pb2.DoubleValue):
            The radius of the proximity.
        radius_units (google.ads.googleads.v4.enums.types.ProximityRadiusUnitsEnum.ProximityRadiusUnits):
            The unit of measurement of the radius.
            Default is KILOMETERS.
        address (google.ads.googleads.v4.common.types.AddressInfo):
            Full address.
    """

    geo_point = proto.Field(proto.MESSAGE, number=1, message="GeoPointInfo",)
    radius = proto.Field(proto.MESSAGE, number=2, message=wrappers.DoubleValue,)
    radius_units = proto.Field(
        proto.ENUM,
        number=3,
        enum=proximity_radius_units.ProximityRadiusUnitsEnum.ProximityRadiusUnits,
    )
    address = proto.Field(proto.MESSAGE, number=4, message="AddressInfo",)


class GeoPointInfo(proto.Message):
    r"""Geo point for proximity criterion.

    Attributes:
        longitude_in_micro_degrees (google.protobuf.wrappers_pb2.Int32Value):
            Micro degrees for the longitude.
        latitude_in_micro_degrees (google.protobuf.wrappers_pb2.Int32Value):
            Micro degrees for the latitude.
    """

    longitude_in_micro_degrees = proto.Field(
        proto.MESSAGE, number=1, message=wrappers.Int32Value,
    )
    latitude_in_micro_degrees = proto.Field(
        proto.MESSAGE, number=2, message=wrappers.Int32Value,
    )


class AddressInfo(proto.Message):
    r"""Address for proximity criterion.

    Attributes:
        postal_code (google.protobuf.wrappers_pb2.StringValue):
            Postal code.
        province_code (google.protobuf.wrappers_pb2.StringValue):
            Province or state code.
        country_code (google.protobuf.wrappers_pb2.StringValue):
            Country code.
        province_name (google.protobuf.wrappers_pb2.StringValue):
            Province or state name.
        street_address (google.protobuf.wrappers_pb2.StringValue):
            Street address line 1.
        street_address2 (google.protobuf.wrappers_pb2.StringValue):
            Street address line 2. This field is write-only. It is only
            used for calculating the longitude and latitude of an
            address when geo_point is empty.
        city_name (google.protobuf.wrappers_pb2.StringValue):
            Name of the city.
    """

    postal_code = proto.Field(
        proto.MESSAGE, number=1, message=wrappers.StringValue,
    )
    province_code = proto.Field(
        proto.MESSAGE, number=2, message=wrappers.StringValue,
    )
    country_code = proto.Field(
        proto.MESSAGE, number=3, message=wrappers.StringValue,
    )
    province_name = proto.Field(
        proto.MESSAGE, number=4, message=wrappers.StringValue,
    )
    street_address = proto.Field(
        proto.MESSAGE, number=5, message=wrappers.StringValue,
    )
    street_address2 = proto.Field(
        proto.MESSAGE, number=6, message=wrappers.StringValue,
    )
    city_name = proto.Field(
        proto.MESSAGE, number=7, message=wrappers.StringValue,
    )


class TopicInfo(proto.Message):
    r"""A topic criterion. Use topics to target or exclude placements
    in the Google Display Network based on the category into which
    the placement falls (for example, "Pets & Animals/Pets/Dogs").

    Attributes:
        topic_constant (google.protobuf.wrappers_pb2.StringValue):
            The Topic Constant resource name.
        path (Sequence[google.protobuf.wrappers_pb2.StringValue]):
            The category to target or exclude. Each
            subsequent element in the array describes a more
            specific sub-category. For example, "Pets &
            Animals", "Pets", "Dogs" represents the "Pets &
            Animals/Pets/Dogs" category.
    """

    topic_constant = proto.Field(
        proto.MESSAGE, number=1, message=wrappers.StringValue,
    )
    path = proto.RepeatedField(
        proto.MESSAGE, number=2, message=wrappers.StringValue,
    )


class LanguageInfo(proto.Message):
    r"""A language criterion.

    Attributes:
        language_constant (google.protobuf.wrappers_pb2.StringValue):
            The language constant resource name.
    """

    language_constant = proto.Field(
        proto.MESSAGE, number=1, message=wrappers.StringValue,
    )


class IpBlockInfo(proto.Message):
    r"""An IpBlock criterion used for IP exclusions. We allow:
    - IPv4 and IPv6 addresses
     - individual addresses (192.168.0.1)
     - masks for individual addresses (192.168.0.1/32)
     - masks for Class C networks (192.168.0.1/24)

    Attributes:
        ip_address (google.protobuf.wrappers_pb2.StringValue):
            The IP address of this IP block.
    """

    ip_address = proto.Field(
        proto.MESSAGE, number=1, message=wrappers.StringValue,
    )


class ContentLabelInfo(proto.Message):
    r"""Content Label for category exclusion.

    Attributes:
        type_ (google.ads.googleads.v4.enums.types.ContentLabelTypeEnum.ContentLabelType):
            Content label type, required for CREATE
            operations.
    """

    type_ = proto.Field(
        proto.ENUM,
        number=1,
        enum=content_label_type.ContentLabelTypeEnum.ContentLabelType,
    )


class CarrierInfo(proto.Message):
    r"""Represents a Carrier Criterion.

    Attributes:
        carrier_constant (google.protobuf.wrappers_pb2.StringValue):
            The Carrier constant resource name.
    """

    carrier_constant = proto.Field(
        proto.MESSAGE, number=1, message=wrappers.StringValue,
    )


class UserInterestInfo(proto.Message):
    r"""Represents a particular interest-based topic to be targeted.

    Attributes:
        user_interest_category (google.protobuf.wrappers_pb2.StringValue):
            The UserInterest resource name.
    """

    user_interest_category = proto.Field(
        proto.MESSAGE, number=1, message=wrappers.StringValue,
    )


class WebpageInfo(proto.Message):
    r"""Represents a criterion for targeting webpages of an
    advertiser's website.

    Attributes:
        criterion_name (google.protobuf.wrappers_pb2.StringValue):
            The name of the criterion that is defined by
            this parameter. The name value will be used for
            identifying, sorting and filtering criteria with
            this type of parameters.

            This field is required for CREATE operations and
            is prohibited on UPDATE operations.
        conditions (Sequence[google.ads.googleads.v4.common.types.WebpageConditionInfo]):
            Conditions, or logical expressions, for
            webpage targeting. The list of webpage targeting
            conditions are and-ed together when evaluated
            for targeting.

            This field is required for CREATE operations and
            is prohibited on UPDATE operations.
    """

    criterion_name = proto.Field(
        proto.MESSAGE, number=1, message=wrappers.StringValue,
    )
    conditions = proto.RepeatedField(
        proto.MESSAGE, number=2, message="WebpageConditionInfo",
    )


class WebpageConditionInfo(proto.Message):
    r"""Logical expression for targeting webpages of an advertiser's
    website.

    Attributes:
        operand (google.ads.googleads.v4.enums.types.WebpageConditionOperandEnum.WebpageConditionOperand):
            Operand of webpage targeting condition.
        operator (google.ads.googleads.v4.enums.types.WebpageConditionOperatorEnum.WebpageConditionOperator):
            Operator of webpage targeting condition.
        argument (google.protobuf.wrappers_pb2.StringValue):
            Argument of webpage targeting condition.
    """

    operand = proto.Field(
        proto.ENUM,
        number=1,
        enum=webpage_condition_operand.WebpageConditionOperandEnum.WebpageConditionOperand,
    )
    operator = proto.Field(
        proto.ENUM,
        number=2,
        enum=webpage_condition_operator.WebpageConditionOperatorEnum.WebpageConditionOperator,
    )
    argument = proto.Field(
        proto.MESSAGE, number=3, message=wrappers.StringValue,
    )


class OperatingSystemVersionInfo(proto.Message):
    r"""Represents an operating system version to be targeted.

    Attributes:
        operating_system_version_constant (google.protobuf.wrappers_pb2.StringValue):
            The operating system version constant
            resource name.
    """

    operating_system_version_constant = proto.Field(
        proto.MESSAGE, number=1, message=wrappers.StringValue,
    )


class AppPaymentModelInfo(proto.Message):
    r"""An app payment model criterion.

    Attributes:
        type_ (google.ads.googleads.v4.enums.types.AppPaymentModelTypeEnum.AppPaymentModelType):
            Type of the app payment model.
    """

    type_ = proto.Field(
        proto.ENUM,
        number=1,
        enum=app_payment_model_type.AppPaymentModelTypeEnum.AppPaymentModelType,
    )


class MobileDeviceInfo(proto.Message):
    r"""A mobile device criterion.

    Attributes:
        mobile_device_constant (google.protobuf.wrappers_pb2.StringValue):
            The mobile device constant resource name.
    """

    mobile_device_constant = proto.Field(
        proto.MESSAGE, number=1, message=wrappers.StringValue,
    )


class CustomAffinityInfo(proto.Message):
    r"""A custom affinity criterion.
    A criterion of this type is only targetable.

    Attributes:
        custom_affinity (google.protobuf.wrappers_pb2.StringValue):
            The CustomInterest resource name.
    """

    custom_affinity = proto.Field(
        proto.MESSAGE, number=1, message=wrappers.StringValue,
    )


class CustomIntentInfo(proto.Message):
    r"""A custom intent criterion.
    A criterion of this type is only targetable.

    Attributes:
        custom_intent (google.protobuf.wrappers_pb2.StringValue):
            The CustomInterest resource name.
    """

    custom_intent = proto.Field(
        proto.MESSAGE, number=1, message=wrappers.StringValue,
    )


class LocationGroupInfo(proto.Message):
    r"""A radius around a list of locations specified via a feed.

    Attributes:
        feed (google.protobuf.wrappers_pb2.StringValue):
            Feed specifying locations for targeting.
            This is required and must be set in CREATE
            operations.
        geo_target_constants (Sequence[google.protobuf.wrappers_pb2.StringValue]):
            Geo target constant(s) restricting the scope
            of the geographic area within the feed.
            Currently only one geo target constant is
            allowed.
        radius (google.protobuf.wrappers_pb2.Int64Value):
            Distance in units specifying the radius
            around targeted locations. This is required and
            must be set in CREATE operations.
        radius_units (google.ads.googleads.v4.enums.types.LocationGroupRadiusUnitsEnum.LocationGroupRadiusUnits):
            Unit of the radius. Miles and meters are
            supported for geo target constants. Milli miles
            and meters are supported for feed item sets.
            This is required and must be set in CREATE
            operations.
    """

    feed = proto.Field(proto.MESSAGE, number=1, message=wrappers.StringValue,)
    geo_target_constants = proto.RepeatedField(
        proto.MESSAGE, number=2, message=wrappers.StringValue,
    )
    radius = proto.Field(proto.MESSAGE, number=3, message=wrappers.Int64Value,)
    radius_units = proto.Field(
        proto.ENUM,
        number=4,
        enum=location_group_radius_units.LocationGroupRadiusUnitsEnum.LocationGroupRadiusUnits,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
