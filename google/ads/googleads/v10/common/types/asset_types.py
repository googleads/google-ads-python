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

from google.ads.googleads.v10.common.types import criteria
from google.ads.googleads.v10.common.types import feed_common
from google.ads.googleads.v10.enums.types import (
    call_conversion_reporting_state as gage_call_conversion_reporting_state,
)
from google.ads.googleads.v10.enums.types import (
    call_to_action_type as gage_call_to_action_type,
)
from google.ads.googleads.v10.enums.types import lead_form_call_to_action_type
from google.ads.googleads.v10.enums.types import lead_form_desired_intent
from google.ads.googleads.v10.enums.types import lead_form_field_user_input_type
from google.ads.googleads.v10.enums.types import (
    lead_form_post_submit_call_to_action_type,
)
from google.ads.googleads.v10.enums.types import mime_type as gage_mime_type
from google.ads.googleads.v10.enums.types import mobile_app_vendor
from google.ads.googleads.v10.enums.types import price_extension_price_qualifier
from google.ads.googleads.v10.enums.types import price_extension_price_unit
from google.ads.googleads.v10.enums.types import price_extension_type
from google.ads.googleads.v10.enums.types import (
    promotion_extension_discount_modifier,
)
from google.ads.googleads.v10.enums.types import promotion_extension_occasion


__protobuf__ = proto.module(
    package="google.ads.googleads.v10.common",
    marshal="google.ads.googleads.v10",
    manifest={
        "YoutubeVideoAsset",
        "MediaBundleAsset",
        "ImageAsset",
        "ImageDimension",
        "TextAsset",
        "LeadFormAsset",
        "LeadFormField",
        "LeadFormSingleChoiceAnswers",
        "LeadFormDeliveryMethod",
        "WebhookDelivery",
        "BookOnGoogleAsset",
        "PromotionAsset",
        "CalloutAsset",
        "StructuredSnippetAsset",
        "SitelinkAsset",
        "PageFeedAsset",
        "DynamicEducationAsset",
        "MobileAppAsset",
        "HotelCalloutAsset",
        "CallAsset",
        "PriceAsset",
        "PriceOffering",
        "CallToActionAsset",
    },
)


class YoutubeVideoAsset(proto.Message):
    r"""A YouTube asset.

    Attributes:
        youtube_video_id (str):
            YouTube video id. This is the 11 character
            string value used in the YouTube video URL.

            This field is a member of `oneof`_ ``_youtube_video_id``.
        youtube_video_title (str):
            YouTube video title.
    """

    youtube_video_id = proto.Field(proto.STRING, number=2, optional=True,)
    youtube_video_title = proto.Field(proto.STRING, number=3,)


class MediaBundleAsset(proto.Message):
    r"""A MediaBundle asset.

    Attributes:
        data (bytes):
            Media bundle (ZIP file) asset data. The
            format of the uploaded ZIP file depends on the
            ad field where it will be used. For more
            information on the format, see the documentation
            of the ad field where you plan on using the
            MediaBundleAsset. This field is mutate only.

            This field is a member of `oneof`_ ``_data``.
    """

    data = proto.Field(proto.BYTES, number=2, optional=True,)


class ImageAsset(proto.Message):
    r"""An Image asset.

    Attributes:
        data (bytes):
            The raw bytes data of an image. This field is
            mutate only.

            This field is a member of `oneof`_ ``_data``.
        file_size (int):
            File size of the image asset in bytes.

            This field is a member of `oneof`_ ``_file_size``.
        mime_type (google.ads.googleads.v10.enums.types.MimeTypeEnum.MimeType):
            MIME type of the image asset.
        full_size (google.ads.googleads.v10.common.types.ImageDimension):
            Metadata for this image at its original size.
    """

    data = proto.Field(proto.BYTES, number=5, optional=True,)
    file_size = proto.Field(proto.INT64, number=6, optional=True,)
    mime_type = proto.Field(
        proto.ENUM, number=3, enum=gage_mime_type.MimeTypeEnum.MimeType,
    )
    full_size = proto.Field(proto.MESSAGE, number=4, message="ImageDimension",)


class ImageDimension(proto.Message):
    r"""Metadata for an image at a certain size, either original or
    resized.

    Attributes:
        height_pixels (int):
            Height of the image.

            This field is a member of `oneof`_ ``_height_pixels``.
        width_pixels (int):
            Width of the image.

            This field is a member of `oneof`_ ``_width_pixels``.
        url (str):
            A URL that returns the image with this height
            and width.

            This field is a member of `oneof`_ ``_url``.
    """

    height_pixels = proto.Field(proto.INT64, number=4, optional=True,)
    width_pixels = proto.Field(proto.INT64, number=5, optional=True,)
    url = proto.Field(proto.STRING, number=6, optional=True,)


class TextAsset(proto.Message):
    r"""A Text asset.

    Attributes:
        text (str):
            Text content of the text asset.

            This field is a member of `oneof`_ ``_text``.
    """

    text = proto.Field(proto.STRING, number=2, optional=True,)


class LeadFormAsset(proto.Message):
    r"""A Lead Form asset.

    Attributes:
        business_name (str):
            Required. The name of the business being
            advertised.
        call_to_action_type (google.ads.googleads.v10.enums.types.LeadFormCallToActionTypeEnum.LeadFormCallToActionType):
            Required. Pre-defined display text that
            encourages user to expand the form.
        call_to_action_description (str):
            Required. Text giving a clear value
            proposition of what users expect once they
            expand the form.
        headline (str):
            Required. Headline of the expanded form to
            describe what the form is asking for or
            facilitating.
        description (str):
            Required. Detailed description of the
            expanded form to describe what the form is
            asking for or facilitating.
        privacy_policy_url (str):
            Required. Link to a page describing the
            policy on how the collected data is handled by
            the advertiser/business.
        post_submit_headline (str):
            Headline of text shown after form submission
            that describes how the advertiser will follow up
            with the user.

            This field is a member of `oneof`_ ``_post_submit_headline``.
        post_submit_description (str):
            Detailed description shown after form
            submission that describes how the advertiser
            will follow up with the user.

            This field is a member of `oneof`_ ``_post_submit_description``.
        fields (Sequence[google.ads.googleads.v10.common.types.LeadFormField]):
            Ordered list of input fields.
        delivery_methods (Sequence[google.ads.googleads.v10.common.types.LeadFormDeliveryMethod]):
            Configured methods for collected lead data to
            be delivered to advertiser. Only one method
            typed as WebhookDelivery can be configured.
        post_submit_call_to_action_type (google.ads.googleads.v10.enums.types.LeadFormPostSubmitCallToActionTypeEnum.LeadFormPostSubmitCallToActionType):
            Pre-defined display text that encourages user
            action after the form is submitted.
        background_image_asset (str):
            Asset resource name of the background image.
            The minimum size is 600x314 and the aspect ratio
            must be 1.91:1 (+-1%).

            This field is a member of `oneof`_ ``_background_image_asset``.
        desired_intent (google.ads.googleads.v10.enums.types.LeadFormDesiredIntentEnum.LeadFormDesiredIntent):
            Desired intent for the lead form, e.g. more
            volume or more qualified.
        custom_disclosure (str):
            Custom disclosure shown along with Google
            disclaimer on the lead form. Accessible to
            allowed customers only.

            This field is a member of `oneof`_ ``_custom_disclosure``.
    """

    business_name = proto.Field(proto.STRING, number=10,)
    call_to_action_type = proto.Field(
        proto.ENUM,
        number=17,
        enum=lead_form_call_to_action_type.LeadFormCallToActionTypeEnum.LeadFormCallToActionType,
    )
    call_to_action_description = proto.Field(proto.STRING, number=18,)
    headline = proto.Field(proto.STRING, number=12,)
    description = proto.Field(proto.STRING, number=13,)
    privacy_policy_url = proto.Field(proto.STRING, number=14,)
    post_submit_headline = proto.Field(proto.STRING, number=15, optional=True,)
    post_submit_description = proto.Field(
        proto.STRING, number=16, optional=True,
    )
    fields = proto.RepeatedField(
        proto.MESSAGE, number=8, message="LeadFormField",
    )
    delivery_methods = proto.RepeatedField(
        proto.MESSAGE, number=9, message="LeadFormDeliveryMethod",
    )
    post_submit_call_to_action_type = proto.Field(
        proto.ENUM,
        number=19,
        enum=lead_form_post_submit_call_to_action_type.LeadFormPostSubmitCallToActionTypeEnum.LeadFormPostSubmitCallToActionType,
    )
    background_image_asset = proto.Field(
        proto.STRING, number=20, optional=True,
    )
    desired_intent = proto.Field(
        proto.ENUM,
        number=21,
        enum=lead_form_desired_intent.LeadFormDesiredIntentEnum.LeadFormDesiredIntent,
    )
    custom_disclosure = proto.Field(proto.STRING, number=22, optional=True,)


class LeadFormField(proto.Message):
    r"""One input field instance within a form.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        input_type (google.ads.googleads.v10.enums.types.LeadFormFieldUserInputTypeEnum.LeadFormFieldUserInputType):
            Describes the input type, which may be a
            predefined type such as "full name" or a
            pre-vetted question like "Do you own a car?".
        single_choice_answers (google.ads.googleads.v10.common.types.LeadFormSingleChoiceAnswers):
            Answer configuration for a single choice
            question. Can be set only for pre-vetted
            question fields. Minimum of 2 answers required
            and maximum of 12 allowed.

            This field is a member of `oneof`_ ``answers``.
    """

    input_type = proto.Field(
        proto.ENUM,
        number=1,
        enum=lead_form_field_user_input_type.LeadFormFieldUserInputTypeEnum.LeadFormFieldUserInputType,
    )
    single_choice_answers = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="answers",
        message="LeadFormSingleChoiceAnswers",
    )


class LeadFormSingleChoiceAnswers(proto.Message):
    r"""Defines possible answers for a single choice question,
    usually presented as a single-choice drop-down list.

    Attributes:
        answers (Sequence[str]):
            List of choices for a single question field.
            The order of entries defines UI order. Minimum
            of 2 answers required and maximum of 12 allowed.
    """

    answers = proto.RepeatedField(proto.STRING, number=1,)


class LeadFormDeliveryMethod(proto.Message):
    r"""A configuration of how leads are delivered to the advertiser.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        webhook (google.ads.googleads.v10.common.types.WebhookDelivery):
            Webhook method of delivery.

            This field is a member of `oneof`_ ``delivery_details``.
    """

    webhook = proto.Field(
        proto.MESSAGE,
        number=1,
        oneof="delivery_details",
        message="WebhookDelivery",
    )


class WebhookDelivery(proto.Message):
    r"""Google notifies the advertiser of leads by making HTTP calls
    to an endpoint they specify. The requests contain JSON matching
    a schema that Google publishes as part of form ads
    documentation.

    Attributes:
        advertiser_webhook_url (str):
            Webhook url specified by advertiser to send
            the lead.

            This field is a member of `oneof`_ ``_advertiser_webhook_url``.
        google_secret (str):
            Anti-spoofing secret set by the advertiser as
            part of the webhook payload.

            This field is a member of `oneof`_ ``_google_secret``.
        payload_schema_version (int):
            The schema version that this delivery
            instance will use.

            This field is a member of `oneof`_ ``_payload_schema_version``.
    """

    advertiser_webhook_url = proto.Field(proto.STRING, number=4, optional=True,)
    google_secret = proto.Field(proto.STRING, number=5, optional=True,)
    payload_schema_version = proto.Field(proto.INT64, number=6, optional=True,)


class BookOnGoogleAsset(proto.Message):
    r"""A Book on Google asset. Used to redirect user to book through
    Google. Book on Google will change the redirect url to book
    directly through Google.

    """


class PromotionAsset(proto.Message):
    r"""A Promotion asset.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        promotion_target (str):
            Required. A freeform description of what the
            promotion is targeting.
        discount_modifier (google.ads.googleads.v10.enums.types.PromotionExtensionDiscountModifierEnum.PromotionExtensionDiscountModifier):
            A modifier for qualification of the discount.
        redemption_start_date (str):
            Start date of when the promotion is eligible
            to be redeemed, in yyyy-MM-dd format.
        redemption_end_date (str):
            Last date of when the promotion is eligible
            to be redeemed, in yyyy-MM-dd format.
        occasion (google.ads.googleads.v10.enums.types.PromotionExtensionOccasionEnum.PromotionExtensionOccasion):
            The occasion the promotion was intended for.
            If an occasion is set, the redemption window
            will need to fall within the date range
            associated with the occasion.
        language_code (str):
            The language of the promotion.
            Represented as BCP 47 language tag.
        start_date (str):
            Start date of when this asset is effective
            and can begin serving, in yyyy-MM-dd format.
        end_date (str):
            Last date of when this asset is effective and
            still serving, in yyyy-MM-dd format.
        ad_schedule_targets (Sequence[google.ads.googleads.v10.common.types.AdScheduleInfo]):
            List of non-overlapping schedules specifying
            all time intervals for which the asset may
            serve. There can be a maximum of 6 schedules per
            day, 42 in total.
        percent_off (int):
            Percentage off discount in the promotion. 1,000,000 = 100%.
            Either this or money_amount_off is required.

            This field is a member of `oneof`_ ``discount_type``.
        money_amount_off (google.ads.googleads.v10.common.types.Money):
            Money amount off for discount in the promotion. Either this
            or percent_off is required.

            This field is a member of `oneof`_ ``discount_type``.
        promotion_code (str):
            A code the user should use in order to be
            eligible for the promotion.

            This field is a member of `oneof`_ ``promotion_trigger``.
        orders_over_amount (google.ads.googleads.v10.common.types.Money):
            The amount the total order needs to be for
            the user to be eligible for the promotion.

            This field is a member of `oneof`_ ``promotion_trigger``.
    """

    promotion_target = proto.Field(proto.STRING, number=1,)
    discount_modifier = proto.Field(
        proto.ENUM,
        number=2,
        enum=promotion_extension_discount_modifier.PromotionExtensionDiscountModifierEnum.PromotionExtensionDiscountModifier,
    )
    redemption_start_date = proto.Field(proto.STRING, number=7,)
    redemption_end_date = proto.Field(proto.STRING, number=8,)
    occasion = proto.Field(
        proto.ENUM,
        number=9,
        enum=promotion_extension_occasion.PromotionExtensionOccasionEnum.PromotionExtensionOccasion,
    )
    language_code = proto.Field(proto.STRING, number=10,)
    start_date = proto.Field(proto.STRING, number=11,)
    end_date = proto.Field(proto.STRING, number=12,)
    ad_schedule_targets = proto.RepeatedField(
        proto.MESSAGE, number=13, message=criteria.AdScheduleInfo,
    )
    percent_off = proto.Field(proto.INT64, number=3, oneof="discount_type",)
    money_amount_off = proto.Field(
        proto.MESSAGE,
        number=4,
        oneof="discount_type",
        message=feed_common.Money,
    )
    promotion_code = proto.Field(
        proto.STRING, number=5, oneof="promotion_trigger",
    )
    orders_over_amount = proto.Field(
        proto.MESSAGE,
        number=6,
        oneof="promotion_trigger",
        message=feed_common.Money,
    )


class CalloutAsset(proto.Message):
    r"""A Callout asset.

    Attributes:
        callout_text (str):
            Required. The callout text.
            The length of this string should be between 1
            and 25, inclusive.
        start_date (str):
            Start date of when this asset is effective
            and can begin serving, in yyyy-MM-dd format.
        end_date (str):
            Last date of when this asset is effective and
            still serving, in yyyy-MM-dd format.
        ad_schedule_targets (Sequence[google.ads.googleads.v10.common.types.AdScheduleInfo]):
            List of non-overlapping schedules specifying
            all time intervals for which the asset may
            serve. There can be a maximum of 6 schedules per
            day, 42 in total.
    """

    callout_text = proto.Field(proto.STRING, number=1,)
    start_date = proto.Field(proto.STRING, number=2,)
    end_date = proto.Field(proto.STRING, number=3,)
    ad_schedule_targets = proto.RepeatedField(
        proto.MESSAGE, number=4, message=criteria.AdScheduleInfo,
    )


class StructuredSnippetAsset(proto.Message):
    r"""A Structured Snippet asset.

    Attributes:
        header (str):
            Required. The header of the snippet.
            This string should be one of the predefined
            values at
            https://developers.google.com/google-ads/api/reference/data/structured-snippet-headers
        values (Sequence[str]):
            Required. The values in the snippet.
            The size of this collection should be between 3
            and 10, inclusive. The length of each value
            should be between 1 and 25 characters,
            inclusive.
    """

    header = proto.Field(proto.STRING, number=1,)
    values = proto.RepeatedField(proto.STRING, number=2,)


class SitelinkAsset(proto.Message):
    r"""A Sitelink asset.

    Attributes:
        link_text (str):
            Required. URL display text for the sitelink.
            The length of this string should be between 1
            and 25, inclusive.
        description1 (str):
            First line of the description for the
            sitelink. If set, the length should be between 1
            and 35, inclusive, and description2 must also be
            set.
        description2 (str):
            Second line of the description for the
            sitelink. If set, the length should be between 1
            and 35, inclusive, and description1 must also be
            set.
        start_date (str):
            Start date of when this asset is effective
            and can begin serving, in yyyy-MM-dd format.
        end_date (str):
            Last date of when this asset is effective and
            still serving, in yyyy-MM-dd format.
        ad_schedule_targets (Sequence[google.ads.googleads.v10.common.types.AdScheduleInfo]):
            List of non-overlapping schedules specifying
            all time intervals for which the asset may
            serve. There can be a maximum of 6 schedules per
            day, 42 in total.
    """

    link_text = proto.Field(proto.STRING, number=1,)
    description1 = proto.Field(proto.STRING, number=2,)
    description2 = proto.Field(proto.STRING, number=3,)
    start_date = proto.Field(proto.STRING, number=4,)
    end_date = proto.Field(proto.STRING, number=5,)
    ad_schedule_targets = proto.RepeatedField(
        proto.MESSAGE, number=6, message=criteria.AdScheduleInfo,
    )


class PageFeedAsset(proto.Message):
    r"""A Page Feed asset.

    Attributes:
        page_url (str):
            Required. The webpage that advertisers want
            to target.
        labels (Sequence[str]):
            Labels used to group the page urls.
    """

    page_url = proto.Field(proto.STRING, number=1,)
    labels = proto.RepeatedField(proto.STRING, number=2,)


class DynamicEducationAsset(proto.Message):
    r"""A Dynamic Education asset.

    Attributes:
        program_id (str):
            Required. Program ID which can be any
            sequence of letters and digits, and must be
            unique and match the values of remarketing tag.
            Required.
        location_id (str):
            Location ID which can be any sequence of
            letters and digits and must be unique.
        program_name (str):
            Required. Program name, e.g. Nursing.
            Required.
        subject (str):
            Subject of study, e.g. Health.
        program_description (str):
            Program description, e.g. Nursing
            Certification.
        school_name (str):
            School name, e.g. Mountain View School of
            Nursing.
        address (str):
            School address which can be specified in one
            of the following formats. (1) City, state, code,
            country, e.g. Mountain View, CA, USA. (2) Full
            address, e.g. 123 Boulevard St, Mountain View,
            CA 94043. (3) Latitude-longitude in the DDD
            format, e.g. 41.40338, 2.17403
        contextual_keywords (Sequence[str]):
            Contextual keywords, e.g. Nursing
            certification, Health, Mountain View.
        android_app_link (str):
            Android deep link, e.g.
            android-app://com.example.android/http/example.com/gizmos?1234.
        similar_program_ids (Sequence[str]):
            Similar program IDs.
        ios_app_link (str):
            iOS deep link, e.g.
            exampleApp://content/page.
        ios_app_store_id (int):
            iOS app store ID. This is used to check if the user has the
            app installed on their device before deep linking. If this
            field is set, then the ios_app_link field must also be
            present.
        thumbnail_image_url (str):
            Thumbnail image url, e.g.
            http://www.example.com/thumbnail.png. The
            thumbnail image will not be uploaded as image
            asset.
        image_url (str):
            Image url, e.g.
            http://www.example.com/image.png. The image will
            not be uploaded as image asset.
    """

    program_id = proto.Field(proto.STRING, number=1,)
    location_id = proto.Field(proto.STRING, number=2,)
    program_name = proto.Field(proto.STRING, number=3,)
    subject = proto.Field(proto.STRING, number=4,)
    program_description = proto.Field(proto.STRING, number=5,)
    school_name = proto.Field(proto.STRING, number=6,)
    address = proto.Field(proto.STRING, number=7,)
    contextual_keywords = proto.RepeatedField(proto.STRING, number=8,)
    android_app_link = proto.Field(proto.STRING, number=9,)
    similar_program_ids = proto.RepeatedField(proto.STRING, number=10,)
    ios_app_link = proto.Field(proto.STRING, number=11,)
    ios_app_store_id = proto.Field(proto.INT64, number=12,)
    thumbnail_image_url = proto.Field(proto.STRING, number=13,)
    image_url = proto.Field(proto.STRING, number=14,)


class MobileAppAsset(proto.Message):
    r"""An asset representing a mobile app.

    Attributes:
        app_id (str):
            Required. A string that uniquely identifies a
            mobile application. It should just contain the
            platform native id, like "com.android.ebay" for
            Android or "12345689" for iOS.
        app_store (google.ads.googleads.v10.enums.types.MobileAppVendorEnum.MobileAppVendor):
            Required. The application store that
            distributes this specific app.
        link_text (str):
            Required. The visible text displayed when the
            link is rendered in an ad. The length of this
            string should be between 1 and 25, inclusive.
        start_date (str):
            Start date of when this asset is effective
            and can begin serving, in yyyy-MM-dd format.
        end_date (str):
            Last date of when this asset is effective and
            still serving, in yyyy-MM-dd format.
    """

    app_id = proto.Field(proto.STRING, number=1,)
    app_store = proto.Field(
        proto.ENUM,
        number=2,
        enum=mobile_app_vendor.MobileAppVendorEnum.MobileAppVendor,
    )
    link_text = proto.Field(proto.STRING, number=3,)
    start_date = proto.Field(proto.STRING, number=4,)
    end_date = proto.Field(proto.STRING, number=5,)


class HotelCalloutAsset(proto.Message):
    r"""An asset representing a hotel callout.

    Attributes:
        text (str):
            Required. The text of the hotel callout
            asset. The length of this string should be
            between 1 and 25, inclusive.
        language_code (str):
            Required. The language of the hotel callout.
            Represented as BCP 47 language tag.
    """

    text = proto.Field(proto.STRING, number=1,)
    language_code = proto.Field(proto.STRING, number=2,)


class CallAsset(proto.Message):
    r"""A Call asset.

    Attributes:
        country_code (str):
            Required. Two-letter country code of the
            phone number. Examples: 'US', 'us'.
        phone_number (str):
            Required. The advertiser's raw phone number.
            Examples: '1234567890', '(123)456-7890'
        call_conversion_reporting_state (google.ads.googleads.v10.enums.types.CallConversionReportingStateEnum.CallConversionReportingState):
            Indicates whether this CallAsset should use
            its own call conversion setting, follow the
            account level setting, or disable call
            conversion.
        call_conversion_action (str):
            The conversion action to attribute a call conversion to. If
            not set, the default conversion action is used. This field
            only has effect if call_conversion_reporting_state is set to
            USE_RESOURCE_LEVEL_CALL_CONVERSION_ACTION.
        ad_schedule_targets (Sequence[google.ads.googleads.v10.common.types.AdScheduleInfo]):
            List of non-overlapping schedules specifying
            all time intervals for which the asset may
            serve. There can be a maximum of 6 schedules per
            day, 42 in total.
    """

    country_code = proto.Field(proto.STRING, number=1,)
    phone_number = proto.Field(proto.STRING, number=2,)
    call_conversion_reporting_state = proto.Field(
        proto.ENUM,
        number=3,
        enum=gage_call_conversion_reporting_state.CallConversionReportingStateEnum.CallConversionReportingState,
    )
    call_conversion_action = proto.Field(proto.STRING, number=4,)
    ad_schedule_targets = proto.RepeatedField(
        proto.MESSAGE, number=5, message=criteria.AdScheduleInfo,
    )


class PriceAsset(proto.Message):
    r"""An asset representing a list of price offers.

    Attributes:
        type_ (google.ads.googleads.v10.enums.types.PriceExtensionTypeEnum.PriceExtensionType):
            Required. The type of the price asset.
        price_qualifier (google.ads.googleads.v10.enums.types.PriceExtensionPriceQualifierEnum.PriceExtensionPriceQualifier):
            The price qualifier of the price asset.
        language_code (str):
            Required. The language of the price asset.
            Represented as BCP 47 language tag.
        price_offerings (Sequence[google.ads.googleads.v10.common.types.PriceOffering]):
            The price offerings of the price asset.
            The size of this collection should be between 3
            and 8, inclusive.
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
    language_code = proto.Field(proto.STRING, number=3,)
    price_offerings = proto.RepeatedField(
        proto.MESSAGE, number=4, message="PriceOffering",
    )


class PriceOffering(proto.Message):
    r"""A single price offering within a PriceAsset.

    Attributes:
        header (str):
            Required. The header of the price offering.
            The length of this string should be between 1
            and 25, inclusive.
        description (str):
            Required. The description of the price
            offering. The length of this string should be
            between 1 and 25, inclusive.
        price (google.ads.googleads.v10.common.types.Money):
            Required. The price value of the price
            offering.
        unit (google.ads.googleads.v10.enums.types.PriceExtensionPriceUnitEnum.PriceExtensionPriceUnit):
            The price unit of the price offering.
        final_url (str):
            Required. The final URL after all cross
            domain redirects.
        final_mobile_url (str):
            The final mobile URL after all cross domain
            redirects.
    """

    header = proto.Field(proto.STRING, number=1,)
    description = proto.Field(proto.STRING, number=2,)
    price = proto.Field(proto.MESSAGE, number=3, message=feed_common.Money,)
    unit = proto.Field(
        proto.ENUM,
        number=4,
        enum=price_extension_price_unit.PriceExtensionPriceUnitEnum.PriceExtensionPriceUnit,
    )
    final_url = proto.Field(proto.STRING, number=5,)
    final_mobile_url = proto.Field(proto.STRING, number=6,)


class CallToActionAsset(proto.Message):
    r"""A call to action asset.

    Attributes:
        call_to_action (google.ads.googleads.v10.enums.types.CallToActionTypeEnum.CallToActionType):
            Call to action.
    """

    call_to_action = proto.Field(
        proto.ENUM,
        number=1,
        enum=gage_call_to_action_type.CallToActionTypeEnum.CallToActionType,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
