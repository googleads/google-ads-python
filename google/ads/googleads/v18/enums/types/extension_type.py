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
        "ExtensionTypeEnum",
    },
)


class ExtensionTypeEnum(proto.Message):
    r"""Container for enum describing possible data types for an
    extension in an extension setting.

    """

    class ExtensionType(proto.Enum):
        r"""Possible data types for an extension in an extension setting.

        Values:
            UNSPECIFIED (0):
                Not specified.
            UNKNOWN (1):
                Used for return value only. Represents value
                unknown in this version.
            NONE (2):
                None.
            APP (3):
                App.
            CALL (4):
                Call.
            CALLOUT (5):
                Callout.
            MESSAGE (6):
                Message.
            PRICE (7):
                Price.
            PROMOTION (8):
                Promotion.
            SITELINK (10):
                Sitelink.
            STRUCTURED_SNIPPET (11):
                Structured snippet.
            LOCATION (12):
                Location.
            AFFILIATE_LOCATION (13):
                Affiliate location.
            HOTEL_CALLOUT (15):
                Hotel callout
            IMAGE (16):
                Image.
        """

        UNSPECIFIED = 0
        UNKNOWN = 1
        NONE = 2
        APP = 3
        CALL = 4
        CALLOUT = 5
        MESSAGE = 6
        PRICE = 7
        PROMOTION = 8
        SITELINK = 10
        STRUCTURED_SNIPPET = 11
        LOCATION = 12
        AFFILIATE_LOCATION = 13
        HOTEL_CALLOUT = 15
        IMAGE = 16


__all__ = tuple(sorted(__protobuf__.manifest))
