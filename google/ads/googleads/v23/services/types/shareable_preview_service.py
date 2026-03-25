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

from google.ads.googleads.v23.enums.types import (
    preview_type as gage_preview_type,
)
from google.rpc import status_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.ads.googleads.v23.services",
    marshal="google.ads.googleads.v23",
    manifest={
        "GenerateShareablePreviewsRequest",
        "ShareablePreview",
        "AssetGroupIdentifier",
        "GenerateShareablePreviewsResponse",
        "ShareablePreviewOrError",
        "ShareablePreviewResult",
        "YouTubeLivePreviewResult",
    },
)


class GenerateShareablePreviewsRequest(proto.Message):
    r"""Request message for
    [ShareablePreviewService.GenerateShareablePreviews][google.ads.googleads.v23.services.ShareablePreviewService.GenerateShareablePreviews].

    Attributes:
        customer_id (str):
            Required. The customer creating the shareable
            previews request.
        shareable_previews (MutableSequence[google.ads.googleads.v23.services.types.ShareablePreview]):
            Required. The list of shareable previews to
            generate.
    """

    customer_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    shareable_previews: MutableSequence["ShareablePreview"] = (
        proto.RepeatedField(
            proto.MESSAGE,
            number=2,
            message="ShareablePreview",
        )
    )


class ShareablePreview(proto.Message):
    r"""A shareable preview with its identifier.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        asset_group_identifier (google.ads.googleads.v23.services.types.AssetGroupIdentifier):
            Optional. Asset group of the shareable preview. Only
            supported for preview type UI_PREVIEW or unset.
        preview_type (google.ads.googleads.v23.enums.types.PreviewTypeEnum.PreviewType):
            Optional. The type of preview to generate.
        ad_group_ad (str):
            Ad group ad of the shareable preview. Only supported for
            preview type YOUTUBE_LIVE_PREVIEW. Format:
            customers/{customer_id}/adGroupAds/{ad_group_id}~{ad_id}

            This field is a member of `oneof`_ ``identifier``.
    """

    asset_group_identifier: "AssetGroupIdentifier" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="AssetGroupIdentifier",
    )
    preview_type: gage_preview_type.PreviewTypeEnum.PreviewType = proto.Field(
        proto.ENUM,
        number=3,
        enum=gage_preview_type.PreviewTypeEnum.PreviewType,
    )
    ad_group_ad: str = proto.Field(
        proto.STRING,
        number=2,
        oneof="identifier",
    )


class AssetGroupIdentifier(proto.Message):
    r"""Asset group of the shareable preview.

    Attributes:
        asset_group_id (int):
            Required. The asset group identifier.
    """

    asset_group_id: int = proto.Field(
        proto.INT64,
        number=1,
    )


class GenerateShareablePreviewsResponse(proto.Message):
    r"""Response message for
    [ShareablePreviewService.GenerateShareablePreviews][google.ads.googleads.v23.services.ShareablePreviewService.GenerateShareablePreviews].

    Attributes:
        responses (MutableSequence[google.ads.googleads.v23.services.types.ShareablePreviewOrError]):
            List of generate shareable preview results.
    """

    responses: MutableSequence["ShareablePreviewOrError"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="ShareablePreviewOrError",
    )


class ShareablePreviewOrError(proto.Message):
    r"""Result of the generate shareable preview.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        asset_group_identifier (google.ads.googleads.v23.services.types.AssetGroupIdentifier):
            The asset group of the shareable preview.
        shareable_preview_result (google.ads.googleads.v23.services.types.ShareablePreviewResult):
            The shareable preview result.

            This field is a member of `oneof`_ ``generate_shareable_preview_response``.
        partial_failure_error (google.rpc.status_pb2.Status):
            The shareable preview partial failure error.

            This field is a member of `oneof`_ ``generate_shareable_preview_response``.
        ad_group_ad (str):
            The ad group ad of the shareable preview. Format:
            customers/{customer_id}/adGroupAds/{ad_group_id}~{ad_id}

            This field is a member of `oneof`_ ``identifier``.
    """

    asset_group_identifier: "AssetGroupIdentifier" = proto.Field(
        proto.MESSAGE,
        number=3,
        message="AssetGroupIdentifier",
    )
    shareable_preview_result: "ShareablePreviewResult" = proto.Field(
        proto.MESSAGE,
        number=1,
        oneof="generate_shareable_preview_response",
        message="ShareablePreviewResult",
    )
    partial_failure_error: status_pb2.Status = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="generate_shareable_preview_response",
        message=status_pb2.Status,
    )
    ad_group_ad: str = proto.Field(
        proto.STRING,
        number=4,
        oneof="identifier",
    )


class ShareablePreviewResult(proto.Message):
    r"""Message to hold a shareable preview result.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        shareable_preview_url (str):
            The shareable preview URL. Only populated if preview type is
            UI_PREVIEW or unset.
        expiration_date_time (str):
            Expiration date time using the ISO-8601
            format.
        youtube_live_preview_result (google.ads.googleads.v23.services.types.YouTubeLivePreviewResult):
            The result of a YouTube live preview. Only populated for
            preview type YOUTUBE_LIVE_PREVIEW.

            This field is a member of `oneof`_ ``result``.
    """

    shareable_preview_url: str = proto.Field(
        proto.STRING,
        number=1,
    )
    expiration_date_time: str = proto.Field(
        proto.STRING,
        number=2,
    )
    youtube_live_preview_result: "YouTubeLivePreviewResult" = proto.Field(
        proto.MESSAGE,
        number=3,
        oneof="result",
        message="YouTubeLivePreviewResult",
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
