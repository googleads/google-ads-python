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


import proto  # type: ignore

from google.ads.googleads.v23.enums.types import video_enhancement_source


__protobuf__ = proto.module(
    package="google.ads.googleads.v23.resources",
    marshal="google.ads.googleads.v23",
    manifest={
        "VideoEnhancement",
    },
)


class VideoEnhancement(proto.Message):
    r"""Represents a video that can include both advertiser uploaded videos
    or enhancements generated from the advertiser uploaded videos. Only
    publicly available videos are returned.

    Each row in this resource represents either the video uploaded by
    the advertiser or each specific variation of it. In contrast, the
    ``Video`` resource represents only the advertiser-provided video and
    would aggregate metrics across all its variations (including
    enhancements). {-- next tag to use: 5 --}

    Attributes:
        resource_name (str):
            Output only. The resource name of the video enhancement.
            Video enhancement resource names have the form:

            ``customers/{customer_id}/videoEnhancements/{video_id}``
        duration_millis (int):
            Output only. Duration of this video, in
            milliseconds.
        source (google.ads.googleads.v23.enums.types.VideoEnhancementSourceEnum.VideoEnhancementSource):
            Output only. The source of the video (e.g.
            advertiser or enhanced by Google Ads).
        title (str):
            Output only. Title of this video.
    """

    resource_name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    duration_millis: int = proto.Field(
        proto.INT64,
        number=2,
    )
    source: (
        video_enhancement_source.VideoEnhancementSourceEnum.VideoEnhancementSource
    ) = proto.Field(
        proto.ENUM,
        number=3,
        enum=video_enhancement_source.VideoEnhancementSourceEnum.VideoEnhancementSource,
    )
    title: str = proto.Field(
        proto.STRING,
        number=4,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
