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


from google.ads.googleads.v4.common.types import custom_parameter
from google.ads.googleads.v4.common.types import feed_common
from google.ads.googleads.v4.enums.types import app_store as gage_app_store
from google.ads.googleads.v4.enums.types import (
    call_conversion_reporting_state as gage_call_conversion_reporting_state,
)
from google.ads.googleads.v4.enums.types import price_extension_price_qualifier
from google.ads.googleads.v4.enums.types import price_extension_price_unit
from google.ads.googleads.v4.enums.types import price_extension_type
from google.ads.googleads.v4.enums.types import (
    promotion_extension_discount_modifier,
)
from google.ads.googleads.v4.enums.types import promotion_extension_occasion
from google.protobuf import wrappers_pb2 as wrappers  # type: ignore


__protobuf__ = proto.module(
    package="google.ads.googleads.v4.common",
    marshal="google.ads.googleads.v4",
    manifest={
        "AppFeedItem",
        "CallFeedItem",
        "CalloutFeedItem",
        "LocationFeedItem",
        "AffiliateLocationFeedItem",
        "TextMessageFeedItem",
        "PriceFeedItem",
        "PriceOffer",
        "PromotionFeedItem",
        "StructuredSnippetFeedItem",
        "SitelinkFeedItem",
        "HotelCalloutFeedItem",
    },
)


class AppFeedItem(proto.Message):
    r"""Represents an App extension.

    Attributes:
        link_text (google.protobuf.wrappers_pb2.StringValue):
            The visible text displayed when the link is
            rendered in an ad. This string must not be
            empty, and the length of this string should be
            between 1 and 25, inclusive.
        app_id (google.protobuf.wrappers_pb2.StringValue):
            The store-specific ID for the target
            application. This string must not be empty.
        app_store (google.ads.googleads.v4.enums.types.AppStoreEnum.AppStore):
            The application store that the target
            application belongs to. This field is required.
        final_urls (Sequence[google.protobuf.wrappers_pb2.StringValue]):
            A list of possible final URLs after all cross
            domain redirects. This list must not be empty.
        final_mobile_urls (Sequence[google.protobuf.wrappers_pb2.StringValue]):
            A list of possible final mobile URLs after
            all cross domain redirects.
        tracking_url_template (google.protobuf.wrappers_pb2.StringValue):
            URL template for constructing a tracking URL.
            Default value is "{lpurl}".
        url_custom_parameters (Sequence[google.ads.googleads.v4.common.types.CustomParameter]):
            A list of mappings to be used for substituting URL custom
            parameter tags in the tracking_url_template, final_urls,
            and/or final_mobile_urls.
        final_url_suffix (google.protobuf.wrappers_pb2.StringValue):
            URL template for appending params to landing
            page URLs served with parallel tracking.
    """

    link_text = proto.Field(
        proto.MESSAGE, number=1, message=wrappers.StringValue,
    )
    app_id = proto.Field(proto.MESSAGE, number=2, message=wrappers.StringValue,)
    app_store = proto.Field(
        proto.ENUM, number=3, enum=gage_app_store.AppStoreEnum.AppStore,
    )
    final_urls = proto.RepeatedField(
        proto.MESSAGE, number=4, message=wrappers.StringValue,
    )
    final_mobile_urls = proto.RepeatedField(
        proto.MESSAGE, number=5, message=wrappers.StringValue,
    )
    tracking_url_template = proto.Field(
        proto.MESSAGE, number=6, message=wrappers.StringValue,
    )
    url_custom_parameters = proto.RepeatedField(
        proto.MESSAGE, number=7, message=custom_parameter.CustomParameter,
    )
    final_url_suffix = proto.Field(
        proto.MESSAGE, number=8, message=wrappers.StringValue,
    )


class CallFeedItem(proto.Message):
    r"""Represents a Call extension.

    Attributes:
        phone_number (google.protobuf.wrappers_pb2.StringValue):
            The advertiser's phone number to append to
            the ad. This string must not be empty.
        country_code (google.protobuf.wrappers_pb2.StringValue):
            Uppercase two-letter country code of the
            advertiser's phone number. This string must not
            be empty.
        call_tracking_enabled (google.protobuf.wrappers_pb2.BoolValue):
            Indicates whether call tracking is enabled.
            By default, call tracking is not enabled.
        call_conversion_action (google.protobuf.wrappers_pb2.StringValue):
            The conversion action to attribute a call conversion to. If
            not set a default conversion action is used. This field only
            has effect if call_tracking_enabled is set to true.
            Otherwise this field is ignored.
        call_conversion_tracking_disabled (google.protobuf.wrappers_pb2.BoolValue):
            If true, disable call conversion tracking.
            call_conversion_action should not be set if this is true.
            Optional.
        call_conversion_reporting_state (google.ads.googleads.v4.enums.types.CallConversionReportingStateEnum.CallConversionReportingState):
            Enum value that indicates whether this call
            extension uses its own call conversion setting
            (or just have call conversion disabled), or
            following the account level setting.
    """

    phone_number = proto.Field(
        proto.MESSAGE, number=1, message=wrappers.StringValue,
    )
    country_code = proto.Field(
        proto.MESSAGE, number=2, message=wrappers.StringValue,
    )
    call_tracking_enabled = proto.Field(
        proto.MESSAGE, number=3, message=wrappers.BoolValue,
    )
    call_conversion_action = proto.Field(
        proto.MESSAGE, number=4, message=wrappers.StringValue,
    )
    call_conversion_tracking_disabled = proto.Field(
        proto.MESSAGE, number=5, message=wrappers.BoolValue,
    )
    call_conversion_reporting_state = proto.Field(
        proto.ENUM,
        number=6,
        enum=gage_call_conversion_reporting_state.CallConversionReportingStateEnum.CallConversionReportingState,
    )


class CalloutFeedItem(proto.Message):
    r"""Represents a callout extension.

    Attributes:
        callout_text (google.protobuf.wrappers_pb2.StringValue):
            The callout text.
            The length of this string should be between 1
            and 25, inclusive.
    """

    callout_text = proto.Field(
        proto.MESSAGE, number=1, message=wrappers.StringValue,
    )


class LocationFeedItem(proto.Message):
    r"""Represents a location extension.

    Attributes:
        business_name (google.protobuf.wrappers_pb2.StringValue):
            The name of the business.
        address_line_1 (google.protobuf.wrappers_pb2.StringValue):
            Line 1 of the business address.
        address_line_2 (google.protobuf.wrappers_pb2.StringValue):
            Line 2 of the business address.
        city (google.protobuf.wrappers_pb2.StringValue):
            City of the business address.
        province (google.protobuf.wrappers_pb2.StringValue):
            Province of the business address.
        postal_code (google.protobuf.wrappers_pb2.StringValue):
            Postal code of the business address.
        country_code (google.protobuf.wrappers_pb2.StringValue):
            Country code of the business address.
        phone_number (google.protobuf.wrappers_pb2.StringValue):
            Phone number of the business.
    """

    business_name = proto.Field(
        proto.MESSAGE, number=1, message=wrappers.StringValue,
    )
    address_line_1 = proto.Field(
        proto.MESSAGE, number=2, message=wrappers.StringValue,
    )
    address_line_2 = proto.Field(
        proto.MESSAGE, number=3, message=wrappers.StringValue,
    )
    city = proto.Field(proto.MESSAGE, number=4, message=wrappers.StringValue,)
    province = proto.Field(
        proto.MESSAGE, number=5, message=wrappers.StringValue,
    )
    postal_code = proto.Field(
        proto.MESSAGE, number=6, message=wrappers.StringValue,
    )
    country_code = proto.Field(
        proto.MESSAGE, number=7, message=wrappers.StringValue,
    )
    phone_number = proto.Field(
        proto.MESSAGE, number=8, message=wrappers.StringValue,
    )


class AffiliateLocationFeedItem(proto.Message):
    r"""Represents an affiliate location extension.

    Attributes:
        business_name (google.protobuf.wrappers_pb2.StringValue):
            The name of the business.
        address_line_1 (google.protobuf.wrappers_pb2.StringValue):
            Line 1 of the business address.
        address_line_2 (google.protobuf.wrappers_pb2.StringValue):
            Line 2 of the business address.
        city (google.protobuf.wrappers_pb2.StringValue):
            City of the business address.
        province (google.protobuf.wrappers_pb2.StringValue):
            Province of the business address.
        postal_code (google.protobuf.wrappers_pb2.StringValue):
            Postal code of the business address.
        country_code (google.protobuf.wrappers_pb2.StringValue):
            Country code of the business address.
        phone_number (google.protobuf.wrappers_pb2.StringValue):
            Phone number of the business.
        chain_id (google.protobuf.wrappers_pb2.Int64Value):
            Id of the retail chain that is advertised as
            a seller of your product.
        chain_name (google.protobuf.wrappers_pb2.StringValue):
            Name of chain.
    """

    business_name = proto.Field(
        proto.MESSAGE, number=1, message=wrappers.StringValue,
    )
    address_line_1 = proto.Field(
        proto.MESSAGE, number=2, message=wrappers.StringValue,
    )
    address_line_2 = proto.Field(
        proto.MESSAGE, number=3, message=wrappers.StringValue,
    )
    city = proto.Field(proto.MESSAGE, number=4, message=wrappers.StringValue,)
    province = proto.Field(
        proto.MESSAGE, number=5, message=wrappers.StringValue,
    )
    postal_code = proto.Field(
        proto.MESSAGE, number=6, message=wrappers.StringValue,
    )
    country_code = proto.Field(
        proto.MESSAGE, number=7, message=wrappers.StringValue,
    )
    phone_number = proto.Field(
        proto.MESSAGE, number=8, message=wrappers.StringValue,
    )
    chain_id = proto.Field(
        proto.MESSAGE, number=9, message=wrappers.Int64Value,
    )
    chain_name = proto.Field(
        proto.MESSAGE, number=10, message=wrappers.StringValue,
    )


class TextMessageFeedItem(proto.Message):
    r"""An extension that users can click on to send a text message
    to the advertiser.

    Attributes:
        business_name (google.protobuf.wrappers_pb2.StringValue):
            The business name to prepend to the message
            text. This field is required.
        country_code (google.protobuf.wrappers_pb2.StringValue):
            Uppercase two-letter country code of the
            advertiser's phone number. This field is
            required.
        phone_number (google.protobuf.wrappers_pb2.StringValue):
            The advertiser's phone number the message
            will be sent to. Required.
        text (google.protobuf.wrappers_pb2.StringValue):
            The text to show in the ad.
            This field is required.
        extension_text (google.protobuf.wrappers_pb2.StringValue):
            The message text populated in the messaging
            app.
    """

    business_name = proto.Field(
        proto.MESSAGE, number=1, message=wrappers.StringValue,
    )
    country_code = proto.Field(
        proto.MESSAGE, number=2, message=wrappers.StringValue,
    )
    phone_number = proto.Field(
        proto.MESSAGE, number=3, message=wrappers.StringValue,
    )
    text = proto.Field(proto.MESSAGE, number=4, message=wrappers.StringValue,)
    extension_text = proto.Field(
        proto.MESSAGE, number=5, message=wrappers.StringValue,
    )


class PriceFeedItem(proto.Message):
    r"""Represents a Price extension.

    Attributes:
        type_ (google.ads.googleads.v4.enums.types.PriceExtensionTypeEnum.PriceExtensionType):
            Price extension type of this extension.
        price_qualifier (google.ads.googleads.v4.enums.types.PriceExtensionPriceQualifierEnum.PriceExtensionPriceQualifier):
            Price qualifier for all offers of this price
            extension.
        tracking_url_template (google.protobuf.wrappers_pb2.StringValue):
            Tracking URL template for all offers of this
            price extension.
        language_code (google.protobuf.wrappers_pb2.StringValue):
            The code of the language used for this price
            extension.
        price_offerings (Sequence[google.ads.googleads.v4.common.types.PriceOffer]):
            The price offerings in this price extension.
        final_url_suffix (google.protobuf.wrappers_pb2.StringValue):
            URL template for appending params to landing
            page URLs served with parallel tracking.
    """

    type_ = proto.Field(
        proto.ENUM,
        number=1,
        enum=price_extension_type.PriceExtensionTypeEnum.PriceExtensionType,
    )
    price_qualifier = proto.Field(
        proto.ENUM,
        number=2,
        enum=price_extension_price_qualifier.PriceExtensionPriceQualifierEnum.PriceExtensionPriceQualifier,
    )
    tracking_url_template = proto.Field(
        proto.MESSAGE, number=3, message=wrappers.StringValue,
    )
    language_code = proto.Field(
        proto.MESSAGE, number=4, message=wrappers.StringValue,
    )
    price_offerings = proto.RepeatedField(
        proto.MESSAGE, number=5, message="PriceOffer",
    )
    final_url_suffix = proto.Field(
        proto.MESSAGE, number=6, message=wrappers.StringValue,
    )


class PriceOffer(proto.Message):
    r"""Represents one price offer in a price extension.

    Attributes:
        header (google.protobuf.wrappers_pb2.StringValue):
            Header text of this offer.
        description (google.protobuf.wrappers_pb2.StringValue):
            Description text of this offer.
        price (google.ads.googleads.v4.common.types.Money):
            Price value of this offer.
        unit (google.ads.googleads.v4.enums.types.PriceExtensionPriceUnitEnum.PriceExtensionPriceUnit):
            Price unit for this offer.
        final_urls (Sequence[google.protobuf.wrappers_pb2.StringValue]):
            A list of possible final URLs after all cross
            domain redirects.
        final_mobile_urls (Sequence[google.protobuf.wrappers_pb2.StringValue]):
            A list of possible final mobile URLs after
            all cross domain redirects.
    """

    header = proto.Field(proto.MESSAGE, number=1, message=wrappers.StringValue,)
    description = proto.Field(
        proto.MESSAGE, number=2, message=wrappers.StringValue,
    )
    price = proto.Field(proto.MESSAGE, number=3, message=feed_common.Money,)
    unit = proto.Field(
        proto.ENUM,
        number=4,
        enum=price_extension_price_unit.PriceExtensionPriceUnitEnum.PriceExtensionPriceUnit,
    )
    final_urls = proto.RepeatedField(
        proto.MESSAGE, number=5, message=wrappers.StringValue,
    )
    final_mobile_urls = proto.RepeatedField(
        proto.MESSAGE, number=6, message=wrappers.StringValue,
    )


class PromotionFeedItem(proto.Message):
    r"""Represents a Promotion extension.

    Attributes:
        promotion_target (google.protobuf.wrappers_pb2.StringValue):
            A freeform description of what the promotion
            is targeting. This field is required.
        discount_modifier (google.ads.googleads.v4.enums.types.PromotionExtensionDiscountModifierEnum.PromotionExtensionDiscountModifier):
            Enum that modifies the qualification of the
            discount.
        promotion_start_date (google.protobuf.wrappers_pb2.StringValue):
            Start date of when the promotion is eligible
            to be redeemed.
        promotion_end_date (google.protobuf.wrappers_pb2.StringValue):
            End date of when the promotion is eligible to
            be redeemed.
        occasion (google.ads.googleads.v4.enums.types.PromotionExtensionOccasionEnum.PromotionExtensionOccasion):
            The occasion the promotion was intended for.
            If an occasion is set, the redemption window
            will need to fall within the date range
            associated with the occasion.
        final_urls (Sequence[google.protobuf.wrappers_pb2.StringValue]):
            A list of possible final URLs after all cross
            domain redirects. This field is required.
        final_mobile_urls (Sequence[google.protobuf.wrappers_pb2.StringValue]):
            A list of possible final mobile URLs after
            all cross domain redirects.
        tracking_url_template (google.protobuf.wrappers_pb2.StringValue):
            URL template for constructing a tracking URL.
        url_custom_parameters (Sequence[google.ads.googleads.v4.common.types.CustomParameter]):
            A list of mappings to be used for substituting URL custom
            parameter tags in the tracking_url_template, final_urls,
            and/or final_mobile_urls.
        final_url_suffix (google.protobuf.wrappers_pb2.StringValue):
            URL template for appending params to landing
            page URLs served with parallel tracking.
        language_code (google.protobuf.wrappers_pb2.StringValue):
            The language of the promotion.
            Represented as BCP 47 language tag.
        percent_off (google.protobuf.wrappers_pb2.Int64Value):
            Percentage off discount in the promotion in micros. One
            million is equivalent to one percent. Either this or
            money_off_amount is required.
        money_amount_off (google.ads.googleads.v4.common.types.Money):
            Money amount off for discount in the promotion. Either this
            or percent_off is required.
        promotion_code (google.protobuf.wrappers_pb2.StringValue):
            A code the user should use in order to be
            eligible for the promotion.
        orders_over_amount (google.ads.googleads.v4.common.types.Money):
            The amount the total order needs to be for
            the user to be eligible for the promotion.
    """

    promotion_target = proto.Field(
        proto.MESSAGE, number=1, message=wrappers.StringValue,
    )
    discount_modifier = proto.Field(
        proto.ENUM,
        number=2,
        enum=promotion_extension_discount_modifier.PromotionExtensionDiscountModifierEnum.PromotionExtensionDiscountModifier,
    )
    promotion_start_date = proto.Field(
        proto.MESSAGE, number=7, message=wrappers.StringValue,
    )
    promotion_end_date = proto.Field(
        proto.MESSAGE, number=8, message=wrappers.StringValue,
    )
    occasion = proto.Field(
        proto.ENUM,
        number=9,
        enum=promotion_extension_occasion.PromotionExtensionOccasionEnum.PromotionExtensionOccasion,
    )
    final_urls = proto.RepeatedField(
        proto.MESSAGE, number=10, message=wrappers.StringValue,
    )
    final_mobile_urls = proto.RepeatedField(
        proto.MESSAGE, number=11, message=wrappers.StringValue,
    )
    tracking_url_template = proto.Field(
        proto.MESSAGE, number=12, message=wrappers.StringValue,
    )
    url_custom_parameters = proto.RepeatedField(
        proto.MESSAGE, number=13, message=custom_parameter.CustomParameter,
    )
    final_url_suffix = proto.Field(
        proto.MESSAGE, number=14, message=wrappers.StringValue,
    )
    language_code = proto.Field(
        proto.MESSAGE, number=15, message=wrappers.StringValue,
    )
    percent_off = proto.Field(
        proto.MESSAGE,
        number=3,
        oneof="discount_type",
        message=wrappers.Int64Value,
    )
    money_amount_off = proto.Field(
        proto.MESSAGE,
        number=4,
        oneof="discount_type",
        message=feed_common.Money,
    )
    promotion_code = proto.Field(
        proto.MESSAGE,
        number=5,
        oneof="promotion_trigger",
        message=wrappers.StringValue,
    )
    orders_over_amount = proto.Field(
        proto.MESSAGE,
        number=6,
        oneof="promotion_trigger",
        message=feed_common.Money,
    )


class StructuredSnippetFeedItem(proto.Message):
    r"""Represents a structured snippet extension.

    Attributes:
        header (google.protobuf.wrappers_pb2.StringValue):
            The header of the snippet.
            This string must not be empty.
        values (Sequence[google.protobuf.wrappers_pb2.StringValue]):
            The values in the snippet.
            The maximum size of this collection is 10.
    """

    header = proto.Field(proto.MESSAGE, number=1, message=wrappers.StringValue,)
    values = proto.RepeatedField(
        proto.MESSAGE, number=2, message=wrappers.StringValue,
    )


class SitelinkFeedItem(proto.Message):
    r"""Represents a sitelink extension.

    Attributes:
        link_text (google.protobuf.wrappers_pb2.StringValue):
            URL display text for the sitelink.
            The length of this string should be between 1
            and 25, inclusive.
        line1 (google.protobuf.wrappers_pb2.StringValue):
            First line of the description for the
            sitelink. If this value is set, line2 must also
            be set. The length of this string should be
            between 0 and 35, inclusive.
        line2 (google.protobuf.wrappers_pb2.StringValue):
            Second line of the description for the
            sitelink. If this value is set, line1 must also
            be set. The length of this string should be
            between 0 and 35, inclusive.
        final_urls (Sequence[google.protobuf.wrappers_pb2.StringValue]):
            A list of possible final URLs after all cross
            domain redirects.
        final_mobile_urls (Sequence[google.protobuf.wrappers_pb2.StringValue]):
            A list of possible final mobile URLs after
            all cross domain redirects.
        tracking_url_template (google.protobuf.wrappers_pb2.StringValue):
            URL template for constructing a tracking URL.
        url_custom_parameters (Sequence[google.ads.googleads.v4.common.types.CustomParameter]):
            A list of mappings to be used for substituting URL custom
            parameter tags in the tracking_url_template, final_urls,
            and/or final_mobile_urls.
        final_url_suffix (google.protobuf.wrappers_pb2.StringValue):
            Final URL suffix to be appended to landing
            page URLs served with parallel tracking.
    """

    link_text = proto.Field(
        proto.MESSAGE, number=1, message=wrappers.StringValue,
    )
    line1 = proto.Field(proto.MESSAGE, number=2, message=wrappers.StringValue,)
    line2 = proto.Field(proto.MESSAGE, number=3, message=wrappers.StringValue,)
    final_urls = proto.RepeatedField(
        proto.MESSAGE, number=4, message=wrappers.StringValue,
    )
    final_mobile_urls = proto.RepeatedField(
        proto.MESSAGE, number=5, message=wrappers.StringValue,
    )
    tracking_url_template = proto.Field(
        proto.MESSAGE, number=6, message=wrappers.StringValue,
    )
    url_custom_parameters = proto.RepeatedField(
        proto.MESSAGE, number=7, message=custom_parameter.CustomParameter,
    )
    final_url_suffix = proto.Field(
        proto.MESSAGE, number=8, message=wrappers.StringValue,
    )


class HotelCalloutFeedItem(proto.Message):
    r"""Represents a hotel callout extension.

    Attributes:
        text (google.protobuf.wrappers_pb2.StringValue):
            The callout text.
            The length of this string should be between 1
            and 25, inclusive.
        language_code (google.protobuf.wrappers_pb2.StringValue):
            The language of the hotel callout text.
            IETF BCP 47 compliant language code.
    """

    text = proto.Field(proto.MESSAGE, number=1, message=wrappers.StringValue,)
    language_code = proto.Field(
        proto.MESSAGE, number=2, message=wrappers.StringValue,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
