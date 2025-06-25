# -*- coding: utf-8 -*-
# Copyright 2024 Google LLC
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
    package="google.ads.googleads.v18.enums",
    marshal="google.ads.googleads.v18",
    manifest={
        "SitelinkPlaceholderFieldEnum",
    },
)


class SitelinkPlaceholderFieldEnum(proto.Message):
    r"""Values for Sitelink placeholder fields."""

    class SitelinkPlaceholderField(proto.Enum):
        r"""Possible values for Sitelink placeholder fields.

        Values:
            UNSPECIFIED (0):
                Not specified.
            UNKNOWN (1):
                Used for return value only. Represents value
                unknown in this version.
            TEXT (2):
                Data Type: STRING. The link text for your
                sitelink.
            LINE_1 (3):
                Data Type: STRING. First line of the sitelink
                description.
            LINE_2 (4):
                Data Type: STRING. Second line of the
                sitelink description.
            FINAL_URLS (5):
                Data Type: URL_LIST. Final URLs for the sitelink when using
                Upgraded URLs.
            FINAL_MOBILE_URLS (6):
                Data Type: URL_LIST. Final Mobile URLs for the sitelink when
                using Upgraded URLs.
            TRACKING_URL (7):
                Data Type: URL. Tracking template for the
                sitelink when using Upgraded URLs.
            FINAL_URL_SUFFIX (8):
                Data Type: STRING. Final URL suffix for
                sitelink when using parallel tracking.
        """

        UNSPECIFIED = 0
        UNKNOWN = 1
        TEXT = 2
        LINE_1 = 3
        LINE_2 = 4
        FINAL_URLS = 5
        FINAL_MOBILE_URLS = 6
        TRACKING_URL = 7
        FINAL_URL_SUFFIX = 8


__all__ = tuple(sorted(__protobuf__.manifest))
