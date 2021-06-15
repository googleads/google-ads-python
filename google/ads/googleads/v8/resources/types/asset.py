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

from google.ads.googleads.v8.common.types import asset_types
from google.ads.googleads.v8.common.types import custom_parameter
from google.ads.googleads.v8.common.types import policy
from google.ads.googleads.v8.enums.types import asset_type
from google.ads.googleads.v8.enums.types import policy_approval_status
from google.ads.googleads.v8.enums.types import policy_review_status


__protobuf__ = proto.module(
    package="google.ads.googleads.v8.resources",
    marshal="google.ads.googleads.v8",
    manifest={"Asset", "AssetPolicySummary",},
)


class Asset(proto.Message):
    r"""Asset is a part of an ad which can be shared across multiple
    ads. It can be an image (ImageAsset), a video
    (YoutubeVideoAsset), etc. Assets are immutable and cannot be
    removed. To stop an asset from serving, remove the asset from
    the entity that is using it.

    Attributes:
        resource_name (str):
            Immutable. The resource name of the asset. Asset resource
            names have the form:

            ``customers/{customer_id}/assets/{asset_id}``
        id (int):
            Output only. The ID of the asset.
        name (str):
            Optional name of the asset.
        type_ (google.ads.googleads.v8.enums.types.AssetTypeEnum.AssetType):
            Output only. Type of the asset.
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
            URL template for appending params to landing
            page URLs served with parallel tracking.
        policy_summary (google.ads.googleads.v8.resources.types.AssetPolicySummary):
            Output only. Policy information for the
            asset.
        youtube_video_asset (google.ads.googleads.v8.common.types.YoutubeVideoAsset):
            Immutable. A YouTube video asset.
        media_bundle_asset (google.ads.googleads.v8.common.types.MediaBundleAsset):
            Immutable. A media bundle asset.
        image_asset (google.ads.googleads.v8.common.types.ImageAsset):
            Output only. An image asset.
        text_asset (google.ads.googleads.v8.common.types.TextAsset):
            Output only. A text asset.
        lead_form_asset (google.ads.googleads.v8.common.types.LeadFormAsset):
            A lead form asset.
        book_on_google_asset (google.ads.googleads.v8.common.types.BookOnGoogleAsset):
            A book on google asset.
        promotion_asset (google.ads.googleads.v8.common.types.PromotionAsset):
            A promotion asset.
        callout_asset (google.ads.googleads.v8.common.types.CalloutAsset):
            A callout asset.
        structured_snippet_asset (google.ads.googleads.v8.common.types.StructuredSnippetAsset):
            A structured snippet asset.
        sitelink_asset (google.ads.googleads.v8.common.types.SitelinkAsset):
            A sitelink asset.
    """

    resource_name = proto.Field(proto.STRING, number=1,)
    id = proto.Field(proto.INT64, number=11, optional=True,)
    name = proto.Field(proto.STRING, number=12, optional=True,)
    type_ = proto.Field(
        proto.ENUM, number=4, enum=asset_type.AssetTypeEnum.AssetType,
    )
    final_urls = proto.RepeatedField(proto.STRING, number=14,)
    final_mobile_urls = proto.RepeatedField(proto.STRING, number=16,)
    tracking_url_template = proto.Field(proto.STRING, number=17, optional=True,)
    url_custom_parameters = proto.RepeatedField(
        proto.MESSAGE, number=18, message=custom_parameter.CustomParameter,
    )
    final_url_suffix = proto.Field(proto.STRING, number=19, optional=True,)
    policy_summary = proto.Field(
        proto.MESSAGE, number=13, message="AssetPolicySummary",
    )
    youtube_video_asset = proto.Field(
        proto.MESSAGE,
        number=5,
        oneof="asset_data",
        message=asset_types.YoutubeVideoAsset,
    )
    media_bundle_asset = proto.Field(
        proto.MESSAGE,
        number=6,
        oneof="asset_data",
        message=asset_types.MediaBundleAsset,
    )
    image_asset = proto.Field(
        proto.MESSAGE,
        number=7,
        oneof="asset_data",
        message=asset_types.ImageAsset,
    )
    text_asset = proto.Field(
        proto.MESSAGE,
        number=8,
        oneof="asset_data",
        message=asset_types.TextAsset,
    )
    lead_form_asset = proto.Field(
        proto.MESSAGE,
        number=9,
        oneof="asset_data",
        message=asset_types.LeadFormAsset,
    )
    book_on_google_asset = proto.Field(
        proto.MESSAGE,
        number=10,
        oneof="asset_data",
        message=asset_types.BookOnGoogleAsset,
    )
    promotion_asset = proto.Field(
        proto.MESSAGE,
        number=15,
        oneof="asset_data",
        message=asset_types.PromotionAsset,
    )
    callout_asset = proto.Field(
        proto.MESSAGE,
        number=20,
        oneof="asset_data",
        message=asset_types.CalloutAsset,
    )
    structured_snippet_asset = proto.Field(
        proto.MESSAGE,
        number=21,
        oneof="asset_data",
        message=asset_types.StructuredSnippetAsset,
    )
    sitelink_asset = proto.Field(
        proto.MESSAGE,
        number=22,
        oneof="asset_data",
        message=asset_types.SitelinkAsset,
    )


class AssetPolicySummary(proto.Message):
    r"""Contains policy information for an asset.
    Attributes:
        policy_topic_entries (Sequence[google.ads.googleads.v8.common.types.PolicyTopicEntry]):
            Output only. The list of policy findings for
            this asset.
        review_status (google.ads.googleads.v8.enums.types.PolicyReviewStatusEnum.PolicyReviewStatus):
            Output only. Where in the review process this
            asset is.
        approval_status (google.ads.googleads.v8.enums.types.PolicyApprovalStatusEnum.PolicyApprovalStatus):
            Output only. The overall approval status of
            this asset, calculated based on the status of
            its individual policy topic entries.
    """

    policy_topic_entries = proto.RepeatedField(
        proto.MESSAGE, number=1, message=policy.PolicyTopicEntry,
    )
    review_status = proto.Field(
        proto.ENUM,
        number=2,
        enum=policy_review_status.PolicyReviewStatusEnum.PolicyReviewStatus,
    )
    approval_status = proto.Field(
        proto.ENUM,
        number=3,
        enum=policy_approval_status.PolicyApprovalStatusEnum.PolicyApprovalStatus,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
