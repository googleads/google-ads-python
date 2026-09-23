# -*- coding: utf-8 -*-
# Copyright 2026 Google LLC
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
    package="google.ads.googleads.v25.enums",
    marshal="google.ads.googleads.v25",
    manifest={
        "VideoCrawlSourcePlatformEnum",
    },
)


class VideoCrawlSourcePlatformEnum(proto.Message):
    r"""Container for enum describing the source platform of the
    crawled video.

    """

    class VideoCrawlSourcePlatform(proto.Enum):
        r"""The source platform of the crawled video.

        Values:
            UNSPECIFIED (0):
                Not specified.
            UNKNOWN (1):
                Used as a return value only. Represents value
                unknown in this version.
            LANDING_PAGE (2):
                Landing page: Videos on advertiser's landing
                page.
            SOCIAL (3):
                Organic Social Video: Videos found from
                social URLs linked in advertiser landing page
                (Facebook, Instagram, X, LinkedIn, TikTok).
            YOUTUBE (4):
                YouTube Channel Organic Videos: Videos from
                the advertiser's channel.
        """

        UNSPECIFIED = 0
        UNKNOWN = 1
        LANDING_PAGE = 2
        SOCIAL = 3
        YOUTUBE = 4


__all__ = tuple(sorted(__protobuf__.manifest))
