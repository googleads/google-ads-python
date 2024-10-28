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
        "AppPlaceholderFieldEnum",
    },
)


class AppPlaceholderFieldEnum(proto.Message):
    r"""Values for App placeholder fields."""

    class AppPlaceholderField(proto.Enum):
        r"""Possible values for App placeholder fields.

        Values:
            UNSPECIFIED (0):
                Not specified.
            UNKNOWN (1):
                Used for return value only. Represents value
                unknown in this version.
            STORE (2):
                Data Type: INT64. The application store that
                the target application belongs to. Valid values
                are: 1 = Apple iTunes Store; 2 = Google Play
                Store.
            ID (3):
                Data Type: STRING. The store-specific ID for
                the target application.
            LINK_TEXT (4):
                Data Type: STRING. The visible text displayed
                when the link is rendered in an ad.
            URL (5):
                Data Type: STRING. The destination URL of the
                in-app link.
            FINAL_URLS (6):
                Data Type: URL_LIST. Final URLs for the in-app link when
                using Upgraded URLs.
            FINAL_MOBILE_URLS (7):
                Data Type: URL_LIST. Final Mobile URLs for the in-app link
                when using Upgraded URLs.
            TRACKING_URL (8):
                Data Type: URL. Tracking template for the
                in-app link when using Upgraded URLs.
            FINAL_URL_SUFFIX (9):
                Data Type: STRING. Final URL suffix for the
                in-app link when using parallel tracking.
        """

        UNSPECIFIED = 0
        UNKNOWN = 1
        STORE = 2
        ID = 3
        LINK_TEXT = 4
        URL = 5
        FINAL_URLS = 6
        FINAL_MOBILE_URLS = 7
        TRACKING_URL = 8
        FINAL_URL_SUFFIX = 9


__all__ = tuple(sorted(__protobuf__.manifest))
