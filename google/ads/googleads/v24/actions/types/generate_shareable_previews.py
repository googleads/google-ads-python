# -*- coding: utf-8 -*-
# Copyright 2025 Google LLC
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
from __future__ import annotations

from typing import MutableSequence

import proto  # type: ignore

from google.ads.googleads.v24.enums.types import (
    preview_type as gage_preview_type,
)


__protobuf__ = proto.module(
    package="google.ads.googleads.v24.actions",
    marshal="google.ads.googleads.v24",
    manifest={
        "GenerateShareablePreviewsOperation",
        "ShareablePreview",
        "GenerateShareablePreviewsResult",
        "ShareablePreviewResult",
        "UiPreviewResult",
        "YouTubeLivePreviewResult",
    },
)


class GenerateShareablePreviewsOperation(proto.Message):
    r"""Operation to generate shareable previews.

    Attributes:
        shareable_previews (MutableSequence[google.ads.googleads.v24.actions.types.ShareablePreview]):
            Required. The list of shareable previews to
            generate.
    """

    shareable_previews: MutableSequence["ShareablePreview"] = (
        proto.RepeatedField(
            proto.MESSAGE,
            number=1,
            message="ShareablePreview",
        )
    )


class ShareablePreview(proto.Message):
    r"""A shareable preview with its identifier.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        preview_type (google.ads.googleads.v24.enums.types.PreviewTypeEnum.PreviewType):
            Required. The type of preview to generate.
        ad_group_ad (str):
            Ad group ad of the shareable preview. Only supported for
            preview type YOUTUBE_LIVE_PREVIEW. Format:
            customers/{customer_id}/adGroupAds/{ad_group_id}~{ad_id}

            This field is a member of `oneof`_ ``identifier``.
        asset_group (str):
            Asset group of the shareable preview. Format:
            customers/{customer_id}/assetGroups/{asset_group_id}

            This field is a member of `oneof`_ ``identifier``.
    """

    preview_type: gage_preview_type.PreviewTypeEnum.PreviewType = proto.Field(
        proto.ENUM,
        number=1,
        enum=gage_preview_type.PreviewTypeEnum.PreviewType,
    )
    ad_group_ad: str = proto.Field(
        proto.STRING,
        number=2,
        oneof="identifier",
    )
    asset_group: str = proto.Field(
        proto.STRING,
        number=3,
        oneof="identifier",
    )


class GenerateShareablePreviewsResult(proto.Message):
    r"""Result of the GenerateShareablePreviews action.

    Attributes:
        previews (MutableSequence[google.ads.googleads.v24.actions.types.ShareablePreviewResult]):
            List of previews.
    """

    previews: MutableSequence["ShareablePreviewResult"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="ShareablePreviewResult",
    )


class ShareablePreviewResult(proto.Message):
    r"""Message to hold a shareable preview result.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        expiration_date_time (str):
            Expiration date time using the ISO-8601
            format.
        ui_preview_result (google.ads.googleads.v24.actions.types.UiPreviewResult):
            The result of a UI preview. Only populated for preview type
            UI_PREVIEW.

            This field is a member of `oneof`_ ``result``.
        youtube_live_preview_result (google.ads.googleads.v24.actions.types.YouTubeLivePreviewResult):
            The result of a YouTube live preview. Only populated for
            preview type YOUTUBE_LIVE_PREVIEW.

            This field is a member of `oneof`_ ``result``.
        ad_group_ad (str):
            Ad group ad of the shareable preview. Format:
            customers/{customer_id}/adGroupAds/{ad_group_id}~{ad_id}

            This field is a member of `oneof`_ ``identifier``.
        asset_group (str):
            Asset group of the shareable preview. Format:
            customers/{customer_id}/assetGroups/{asset_group_id}

            This field is a member of `oneof`_ ``identifier``.
    """

    expiration_date_time: str = proto.Field(
        proto.STRING,
        number=3,
    )
    ui_preview_result: "UiPreviewResult" = proto.Field(
        proto.MESSAGE,
        number=1,
        oneof="result",
        message="UiPreviewResult",
    )
    youtube_live_preview_result: "YouTubeLivePreviewResult" = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="result",
        message="YouTubeLivePreviewResult",
    )
    ad_group_ad: str = proto.Field(
        proto.STRING,
        number=4,
        oneof="identifier",
    )
    asset_group: str = proto.Field(
        proto.STRING,
        number=5,
        oneof="identifier",
    )


class UiPreviewResult(proto.Message):
    r"""Message to hold a UI preview result.

    Attributes:
        shareable_preview_url (str):
            The shareable preview URL.
    """

    shareable_preview_url: str = proto.Field(
        proto.STRING,
        number=1,
    )


class YouTubeLivePreviewResult(proto.Message):
    r"""Message to hold a YouTube live preview result.

    Attributes:
        youtube_preview_url (str):
            The shareable preview URL for YouTube videos.
        youtube_tv_preview_url (str):
            The shareable preview URL for YouTube TV.
    """

    youtube_preview_url: str = proto.Field(
        proto.STRING,
        number=1,
    )
    youtube_tv_preview_url: str = proto.Field(
        proto.STRING,
        number=2,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
