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


__protobuf__ = proto.module(
    package="google.ads.googleads.v23.enums",
    marshal="google.ads.googleads.v23",
    manifest={
        "PreviewTypeEnum",
    },
)


class PreviewTypeEnum(proto.Message):
    r"""Preview type."""

    class PreviewType(proto.Enum):
        r"""Enum describing the preview type.
        Next Id: 4

        Values:
            UNSPECIFIED (0):
                Not specified.
            UNKNOWN (1):
                Used for return value only. Represents value
                unknown in this version.
            UI_PREVIEW (2):
                Request a URL to a preview in the Google Ads
                UI. The generated URLs are shareable.
            YOUTUBE_LIVE_PREVIEW (3):
                Request a URL to a preview of the ad in
                YouTube. The generated URLs are shareable.
        """

        UNSPECIFIED = 0
        UNKNOWN = 1
        UI_PREVIEW = 2
        YOUTUBE_LIVE_PREVIEW = 3


__all__ = tuple(sorted(__protobuf__.manifest))
