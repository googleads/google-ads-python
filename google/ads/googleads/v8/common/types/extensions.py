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

from google.ads.googleads.v8.common.types import custom_parameter
from google.ads.googleads.v8.common.types import feed_common
from google.ads.googleads.v8.enums.types import app_store as gage_app_store
from google.ads.googleads.v8.enums.types import (
    call_conversion_reporting_state as gage_call_conversion_reporting_state,
)
from google.ads.googleads.v8.enums.types import price_extension_price_qualifier
from google.ads.googleads.v8.enums.types import price_extension_price_unit
from google.ads.googleads.v8.enums.types import price_extension_type
from google.ads.googleads.v8.enums.types import (
    promotion_extension_discount_modifier,
)
from google.ads.googleads.v8.enums.types import promotion_extension_occasion


__protobuf__ = proto.module(
    package="google.ads.googleads.v8.common",
    marshal="google.ads.googleads.v8",
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
        "ImageFeedItem",
    },
)


class AppFeedItem(proto.Message):
    r"""Represents an App extension.
    Attributes:
        link_text (str):
            The visible text displayed when the link is
            rendered in an ad. This string must not be
            empty, and the length of this string should be
            between 1 and 25, inclusive.
        app_id (str):
            The store-specific ID for the target
            application. This string must not be empty.
        app_store (google.ads.googleads.v8.enums.types.AppStoreEnum.AppStore):
            The application store that the target
            application belongs to. This field is required.
        final_urls (Sequence[str]):
            A list of possible final URLs after all cross
            domain redirects. This list must not be empty.
        final_mobile_urls (Sequence[str]):
            A list of possible final mobile URLs after
            all cross domain redirects.
        tracking_url_template (str):
            URL template for constructing a tracking URL.
            Default value is "{lpurl}".
        url_custom_parameters (Sequence[google.ads.googleads.v8.common.types.CustomParameter]):
            A list of mappings to be used for substituting URL custom
            parameter tags in the tracking_url_template, final_urls,
            and/or final_mobile_urls.
        final_url_suffix (str):
            URL template for appending params to landing
            page URLs served with parallel tracking.
    """

    link_text = proto.Field(proto.STRING, number=9, optional=True,)
    app_id = proto.Field(proto.STRING, number=10, optional=True,)
    app_store = proto.Field(
        proto.ENUM, number=3, enum=gage_app_store.AppStoreEnum.AppStore,
    )
    final_urls = proto.RepeatedField(proto.STRING, number=11,)
    final_mobile_urls = proto.RepeatedField(proto.STRING, number=12,)
    tracking_url_template = proto.Field(proto.STRING, number=13, optional=True,)
    url_custom_parameters = proto.RepeatedField(
        proto.MESSAGE, number=7, message=custom_parameter.CustomParameter,
    )
    final_url_suffix = proto.Field(proto.STRING, number=14, optional=True,)


class CallFeedItem(proto.Message):
    r"""Represents a Call extension.
    Attributes:
        phone_number (str):
            The advertiser's phone number to append to
            the ad. This string must not be empty.
        country_code (str):
            Uppercase two-letter country code of the
            advertiser's phone number. This string must not
            be empty.
        call_tracking_enabled (bool):
            Indicates whether call tracking is enabled.
            By default, call tracking is not enabled.
        call_conversion_action (str):
            The conversion action to attribute a call conversion to. If
            not set a default conversion action is used. This field only
            has effect if call_tracking_enabled is set to true.
            Otherwise this field is ignored.
        call_conversion_tracking_disabled (bool):
            If true, disable call conversion tracking.
            call_conversion_action should not be set if this is true.
            Optional.
        call_conversion_reporting_state (google.ads.googleads.v8.enums.types.CallConversionReportingStateEnum.CallConversionReportingState):
            Enum value that indicates whether this call
            extension uses its own call conversion setting
            (or just have call conversion disabled), or
            following the account level setting.
    """

    phone_number = proto.Field(proto.STRING, number=7, optional=True,)
    country_code = proto.Field(proto.STRING, number=8, optional=True,)
    call_tracking_enabled = proto.Field(proto.BOOL, number=9, optional=True,)
    call_conversion_action = proto.Field(
        proto.STRING, number=10, optional=True,
    )
    call_conversion_tracking_disabled = proto.Field(
        proto.BOOL, number=11, optional=True,
    )
    call_conversion_reporting_state = proto.Field(
        proto.ENUM,
        number=6,
        enum=gage_call_conversion_reporting_state.CallConversionReportingStateEnum.CallConversionReportingState,
    )


class CalloutFeedItem(proto.Message):
    r"""Represents a callout extension.
    Attributes:
        callout_text (str):
            The callout text.
            The length of this string should be between 1
            and 25, inclusive.
    """

    callout_text = proto.Field(proto.STRING, number=2, optional=True,)


class LocationFeedItem(proto.Message):
    r"""Represents a location extension.
    Attributes:
        business_name (str):
            The name of the business.
        address_line_1 (str):
            Line 1 of the business address.
        address_line_2 (str):
            Line 2 of the business address.
        city (str):
            City of the business address.
        province (str):
            Province of the business address.
        postal_code (str):
            Postal code of the business address.
        country_code (str):
            Country code of the business address.
        phone_number (str):
            Phone number of the business.
    """

    business_name = proto.Field(proto.STRING, number=9, optional=True,)
    address_line_1 = proto.Field(proto.STRING, number=10, optional=True,)
    address_line_2 = proto.Field(proto.STRING, number=11, optional=True,)
    city = proto.Field(proto.STRING, number=12, optional=True,)
    province = proto.Field(proto.STRING, number=13, optional=True,)
    postal_code = proto.Field(proto.STRING, number=14, optional=True,)
    country_code = proto.Field(proto.STRING, number=15, optional=True,)
    phone_number = proto.Field(proto.STRING, number=16, optional=True,)


class AffiliateLocationFeedItem(proto.Message):
    r"""Represents an affiliate location extension.
    Attributes:
        business_name (str):
            The name of the business.
        address_line_1 (str):
            Line 1 of the business address.
        address_line_2 (str):
            Line 2 of the business address.
        city (str):
            City of the business address.
        province (str):
            Province of the business address.
        postal_code (str):
            Postal code of the business address.
        country_code (str):
            Country code of the business address.
        phone_number (str):
            Phone number of the business.
        chain_id (int):
            Id of the retail chain that is advertised as
            a seller of your product.
        chain_name (str):
            Name of chain.
    """

    business_name = proto.Field(proto.STRING, number=11, optional=True,)
    address_line_1 = proto.Field(proto.STRING, number=12, optional=True,)
    address_line_2 = proto.Field(proto.STRING, number=13, optional=True,)
    city = proto.Field(proto.STRING, number=14, optional=True,)
    province = proto.Field(proto.STRING, number=15, optional=True,)
    postal_code = proto.Field(proto.STRING, number=16, optional=True,)
    country_code = proto.Field(proto.STRING, number=17, optional=True,)
    phone_number = proto.Field(proto.STRING, number=18, optional=True,)
    chain_id = proto.Field(proto.INT64, number=19, optional=True,)
    chain_name = proto.Field(proto.STRING, number=20, optional=True,)


class TextMessageFeedItem(proto.Message):
    r"""An extension that users can click on to send a text message
    to the advertiser.

    Attributes:
        business_name (str):
            The business name to prepend to the message
            text. This field is required.
        country_code (str):
            Uppercase two-letter country code of the
            advertiser's phone number. This field is
            required.
        phone_number (str):
            The advertiser's phone number the message
            will be sent to. Required.
        text (str):
            The text to show in the ad.
            This field is required.
        extension_text (str):
            The message extension_text populated in the messaging app.
    """

    business_name = proto.Field(proto.STRING, number=6, optional=True,)
    country_code = proto.Field(proto.STRING, number=7, optional=True,)
    phone_number = proto.Field(proto.STRING, number=8, optional=True,)
    text = proto.Field(proto.STRING, number=9, optional=True,)
    extension_text = proto.Field(proto.STRING, number=10, optional=True,)


class PriceFeedItem(proto.Message):
    r"""Represents a Price extension.
    Attributes:
        type_ (google.ads.googleads.v8.enums.types.PriceExtensionTypeEnum.PriceExtensionType):
            Price extension type of this extension.
        price_qualifier (google.ads.googleads.v8.enums.types.PriceExtensionPriceQualifierEnum.PriceExtensionPriceQualifier):
            Price qualifier for all offers of this price
            extension.
        tracking_url_template (str):
            Tracking URL template for all offers of this
            price extension.
        language_code (str):
            The code of the language used for this price
            extension.
        price_offerings (Sequence[google.ads.googleads.v8.common.types.PriceOffer]):
            The price offerings in this price extension.
        final_url_suffix (str):
            Tracking URL template for all offers of this
            price extension.
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
    tracking_url_template = proto.Field(proto.STRING, number=7, optional=True,)
    language_code = proto.Field(proto.STRING, number=8, optional=True,)
    price_offerings = proto.RepeatedField(
        proto.MESSAGE, number=5, message="PriceOffer",
    )
    final_url_suffix = proto.Field(proto.STRING, number=9, optional=True,)


class PriceOffer(proto.Message):
    r"""Represents one price offer in a price extension.
    Attributes:
        header (str):
            Header text of this offer.
        description (str):
            Description text of this offer.
        price (google.ads.googleads.v8.common.types.Money):
            Price value of this offer.
        unit (google.ads.googleads.v8.enums.types.PriceExtensionPriceUnitEnum.PriceExtensionPriceUnit):
            Price unit for this offer.
        final_urls (Sequence[str]):
            A list of possible final URLs after all cross
            domain redirects.
        final_mobile_urls (Sequence[str]):
            A list of possible final mobile URLs after
            all cross domain redirects.
    """

    header = proto.Field(proto.STRING, number=7, optional=True,)
    description = proto.Field(proto.STRING, number=8, optional=True,)
    price = proto.Field(proto.MESSAGE, number=3, message=feed_common.Money,)
    unit = proto.Field(
        proto.ENUM,
        number=4,
        enum=price_extension_price_unit.PriceExtensionPriceUnitEnum.PriceExtensionPriceUnit,
    )
    final_urls = proto.RepeatedField(proto.STRING, number=9,)
    final_mobile_urls = proto.RepeatedField(proto.STRING, number=10,)


class PromotionFeedItem(proto.Message):
    r"""Represents a Promotion extension.
    Attributes:
        promotion_target (str):
            A freeform description of what the promotion
            is targeting. This field is required.
        discount_modifier (google.ads.googleads.v8.enums.types.PromotionExtensionDiscountModifierEnum.PromotionExtensionDiscountModifier):
            Enum that modifies the qualification of the
            discount.
        promotion_start_date (str):
            Start date of when the promotion is eligible
            to be redeemed.
        promotion_end_date (str):
            Last date when the promotion is eligible to
            be redeemed.
        occasion (google.ads.googleads.v8.enums.types.PromotionExtensionOccasionEnum.PromotionExtensionOccasion):
            The occasion the promotion was intended for.
            If an occasion is set, the redemption window
            will need to fall within the date range
            associated with the occasion.
        final_urls (Sequence[str]):
            A list of possible final URLs after all cross
            domain redirects. This field is required.
        final_mobile_urls (Sequence[str]):
            A list of possible final mobile URLs after
            all cross domain redirects.
        tracking_url_template (str):
            URL template for constructing a tracking URL.
        url_custom_parameters (Sequence[google.ads.googleads.v8.common.types.CustomParameter]):
            A list of mappings to be used for substituting URL custom
            parameter tags in the tracking_url_template, final_urls,
            and/or final_mobile_urls.
        final_url_suffix (str):
            URL template for appending params to landing
            page URLs served with parallel tracking.
        language_code (str):
            The language of the promotion.
            Represented as BCP 47 language tag.
        percent_off (int):
            Percentage off discount in the promotion in micros. One
            million is equivalent to one percent. Either this or
            money_off_amount is required.
        money_amount_off (google.ads.googleads.v8.common.types.Money):
            Money amount off for discount in the promotion. Either this
            or percent_off is required.
        promotion_code (str):
            A code the user should use in order to be
            eligible for the promotion.
        orders_over_amount (google.ads.googleads.v8.common.types.Money):
            The amount the total order needs to be for
            the user to be eligible for the promotion.
    """

    promotion_target = proto.Field(proto.STRING, number=16, optional=True,)
    discount_modifier = proto.Field(
        proto.ENUM,
        number=2,
        enum=promotion_extension_discount_modifier.PromotionExtensionDiscountModifierEnum.PromotionExtensionDiscountModifier,
    )
    promotion_start_date = proto.Field(proto.STRING, number=19, optional=True,)
    promotion_end_date = proto.Field(proto.STRING, number=20, optional=True,)
    occasion = proto.Field(
        proto.ENUM,
        number=9,
        enum=promotion_extension_occasion.PromotionExtensionOccasionEnum.PromotionExtensionOccasion,
    )
    final_urls = proto.RepeatedField(proto.STRING, number=21,)
    final_mobile_urls = proto.RepeatedField(proto.STRING, number=22,)
    tracking_url_template = proto.Field(proto.STRING, number=23, optional=True,)
    url_custom_parameters = proto.RepeatedField(
        proto.MESSAGE, number=13, message=custom_parameter.CustomParameter,
    )
    final_url_suffix = proto.Field(proto.STRING, number=24, optional=True,)
    language_code = proto.Field(proto.STRING, number=25, optional=True,)
    percent_off = proto.Field(proto.INT64, number=17, oneof="discount_type",)
    money_amount_off = proto.Field(
        proto.MESSAGE,
        number=4,
        oneof="discount_type",
        message=feed_common.Money,
    )
    promotion_code = proto.Field(
        proto.STRING, number=18, oneof="promotion_trigger",
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
        header (str):
            The header of the snippet.
            This string must not be empty.
        values (Sequence[str]):
            The values in the snippet.
            The maximum size of this collection is 10.
    """

    header = proto.Field(proto.STRING, number=3, optional=True,)
    values = proto.RepeatedField(proto.STRING, number=4,)


class SitelinkFeedItem(proto.Message):
    r"""Represents a sitelink extension.
    Attributes:
        link_text (str):
            URL display text for the sitelink.
            The length of this string should be between 1
            and 25, inclusive.
        line1 (str):
            First line of the description for the
            sitelink. If this value is set, line2 must also
            be set. The length of this string should be
            between 0 and 35, inclusive.
        line2 (str):
            Second line of the description for the
            sitelink. If this value is set, line1 must also
            be set. The length of this string should be
            between 0 and 35, inclusive.
        final_urls (Sequence[str]):
            A list of possible final URLs after all cross
            domain redirects.
        final_mobile_urls (Sequence[str]):
            A list of possible final mobile URLs after
            all cross domain redirects.
        tracking_url_template (str):
            URL template for constructing a tracking URL.
        url_custom_parameters (Sequence[google.ads.googleads.v8.common.types.CustomParameter]):
            A list of mappings to be used for substituting URL custom
            parameter tags in the tracking_url_template, final_urls,
            and/or final_mobile_urls.
        final_url_suffix (str):
            Final URL suffix to be appended to landing
            page URLs served with parallel tracking.
    """

    link_text = proto.Field(proto.STRING, number=9, optional=True,)
    line1 = proto.Field(proto.STRING, number=10, optional=True,)
    line2 = proto.Field(proto.STRING, number=11, optional=True,)
    final_urls = proto.RepeatedField(proto.STRING, number=12,)
    final_mobile_urls = proto.RepeatedField(proto.STRING, number=13,)
    tracking_url_template = proto.Field(proto.STRING, number=14, optional=True,)
    url_custom_parameters = proto.RepeatedField(
        proto.MESSAGE, number=7, message=custom_parameter.CustomParameter,
    )
    final_url_suffix = proto.Field(proto.STRING, number=15, optional=True,)


class HotelCalloutFeedItem(proto.Message):
    r"""Represents a hotel callout extension.
    Attributes:
        text (str):
            The callout text.
            The length of this string should be between 1
            and 25, inclusive.
        language_code (str):
            The language of the hotel callout text.
            IETF BCP 47 compliant language code.
    """

    text = proto.Field(proto.STRING, number=3, optional=True,)
    language_code = proto.Field(proto.STRING, number=4, optional=True,)


class ImageFeedItem(proto.Message):
    r"""Represents an advertiser provided image extension.
    Attributes:
        image_asset (str):
            Required. Resource name of the image asset.
    """

    image_asset = proto.Field(proto.STRING, number=1,)


__all__ = tuple(sorted(__protobuf__.manifest))
