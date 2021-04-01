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


from google.ads.googleads.v6.enums.types import lead_form_call_to_action_type
from google.ads.googleads.v6.enums.types import lead_form_desired_intent
from google.ads.googleads.v6.enums.types import lead_form_field_user_input_type
from google.ads.googleads.v6.enums.types import (
    lead_form_post_submit_call_to_action_type,
)
from google.ads.googleads.v6.enums.types import mime_type as gage_mime_type


__protobuf__ = proto.module(
    package="google.ads.googleads.v6.common",
    marshal="google.ads.googleads.v6",
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
    },
)


class YoutubeVideoAsset(proto.Message):
    r"""A YouTube asset.

    Attributes:
        youtube_video_id (str):
            YouTube video id. This is the 11 character
            string value used in the YouTube video URL.
        youtube_video_title (str):
            YouTube video title.
    """

    youtube_video_id = proto.Field(proto.STRING, number=2, optional=True)
    youtube_video_title = proto.Field(proto.STRING, number=3)


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
    """

    data = proto.Field(proto.BYTES, number=2, optional=True)


class ImageAsset(proto.Message):
    r"""An Image asset.

    Attributes:
        data (bytes):
            The raw bytes data of an image. This field is
            mutate only.
        file_size (int):
            File size of the image asset in bytes.
        mime_type (google.ads.googleads.v6.enums.types.MimeTypeEnum.MimeType):
            MIME type of the image asset.
        full_size (google.ads.googleads.v6.common.types.ImageDimension):
            Metadata for this image at its original size.
    """

    data = proto.Field(proto.BYTES, number=5, optional=True)
    file_size = proto.Field(proto.INT64, number=6, optional=True)
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
        width_pixels (int):
            Width of the image.
        url (str):
            A URL that returns the image with this height
            and width.
    """

    height_pixels = proto.Field(proto.INT64, number=4, optional=True)
    width_pixels = proto.Field(proto.INT64, number=5, optional=True)
    url = proto.Field(proto.STRING, number=6, optional=True)


class TextAsset(proto.Message):
    r"""A Text asset.

    Attributes:
        text (str):
            Text content of the text asset.
    """

    text = proto.Field(proto.STRING, number=2, optional=True)


class LeadFormAsset(proto.Message):
    r"""A Lead Form asset.

    Attributes:
        business_name (str):
            Required. The name of the business being
            advertised.
        call_to_action_type (google.ads.googleads.v6.enums.types.LeadFormCallToActionTypeEnum.LeadFormCallToActionType):
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
        post_submit_description (str):
            Detailed description shown after form
            submission that describes how the advertiser
            will follow up with the user.
        fields (Sequence[google.ads.googleads.v6.common.types.LeadFormField]):
            Ordered list of input fields.
        delivery_methods (Sequence[google.ads.googleads.v6.common.types.LeadFormDeliveryMethod]):
            Configured methods for collected lead data to
            be delivered to advertiser.
        post_submit_call_to_action_type (google.ads.googleads.v6.enums.types.LeadFormPostSubmitCallToActionTypeEnum.LeadFormPostSubmitCallToActionType):
            Pre-defined display text that encourages user
            action after the form is submitted.
        background_image_asset (str):
            Asset resource name of the background image.
            The minimum size is 600x314 and the aspect ratio
            must be 1.91:1 (+-1%).
        desired_intent (google.ads.googleads.v6.enums.types.LeadFormDesiredIntentEnum.LeadFormDesiredIntent):
            Desired intent for the lead form, e.g. more
            volume or higher intent.
        custom_disclosure (str):
            Custom disclosure shown along with Google
            disclaimer on the lead form. Accessible to
            allowed customers only.
    """

    business_name = proto.Field(proto.STRING, number=10)
    call_to_action_type = proto.Field(
        proto.ENUM,
        number=17,
        enum=lead_form_call_to_action_type.LeadFormCallToActionTypeEnum.LeadFormCallToActionType,
    )
    call_to_action_description = proto.Field(proto.STRING, number=18)
    headline = proto.Field(proto.STRING, number=12)
    description = proto.Field(proto.STRING, number=13)
    privacy_policy_url = proto.Field(proto.STRING, number=14)
    post_submit_headline = proto.Field(proto.STRING, number=15, optional=True)
    post_submit_description = proto.Field(
        proto.STRING, number=16, optional=True
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
    background_image_asset = proto.Field(proto.STRING, number=20, optional=True)
    desired_intent = proto.Field(
        proto.ENUM,
        number=21,
        enum=lead_form_desired_intent.LeadFormDesiredIntentEnum.LeadFormDesiredIntent,
    )
    custom_disclosure = proto.Field(proto.STRING, number=22, optional=True)


class LeadFormField(proto.Message):
    r"""One input field instance within a form.

    Attributes:
        input_type (google.ads.googleads.v6.enums.types.LeadFormFieldUserInputTypeEnum.LeadFormFieldUserInputType):
            Describes the input type, which may be a
            predefined type such as "full name" or a pre-
            vetted question like "Do you own a car?".
        single_choice_answers (google.ads.googleads.v6.common.types.LeadFormSingleChoiceAnswers):
            Answer configuration for a single choice
            question. Can be set only for pre-vetted
            question fields. Minimum of 2 answers required
            and maximum of 12 allowed.
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

    answers = proto.RepeatedField(proto.STRING, number=1)


class LeadFormDeliveryMethod(proto.Message):
    r"""A configuration of how leads are delivered to the advertiser.

    Attributes:
        webhook (google.ads.googleads.v6.common.types.WebhookDelivery):
            Webhook method of delivery.
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
        google_secret (str):
            Anti-spoofing secret set by the advertiser as
            part of the webhook payload.
        payload_schema_version (int):
            The schema version that this delivery
            instance will use.
    """

    advertiser_webhook_url = proto.Field(proto.STRING, number=4, optional=True)
    google_secret = proto.Field(proto.STRING, number=5, optional=True)
    payload_schema_version = proto.Field(proto.INT64, number=6, optional=True)


class BookOnGoogleAsset(proto.Message):
    r"""A Book on Google asset. Used to redirect user to book through
    Google. Book on Google will change the redirect url to book
    directly through Google.
    """


__all__ = tuple(sorted(__protobuf__.manifest))
