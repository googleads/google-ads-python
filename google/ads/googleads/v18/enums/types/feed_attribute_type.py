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
        "FeedAttributeTypeEnum",
    },
)


class FeedAttributeTypeEnum(proto.Message):
    r"""Container for enum describing possible data types for a feed
    attribute.

    """

    class FeedAttributeType(proto.Enum):
        r"""Possible data types for a feed attribute.

        Values:
            UNSPECIFIED (0):
                Not specified.
            UNKNOWN (1):
                Used for return value only. Represents value
                unknown in this version.
            INT64 (2):
                Int64.
            DOUBLE (3):
                Double.
            STRING (4):
                String.
            BOOLEAN (5):
                Boolean.
            URL (6):
                Url.
            DATE_TIME (7):
                Datetime.
            INT64_LIST (8):
                Int64 list.
            DOUBLE_LIST (9):
                Double (8 bytes) list.
            STRING_LIST (10):
                String list.
            BOOLEAN_LIST (11):
                Boolean list.
            URL_LIST (12):
                Url list.
            DATE_TIME_LIST (13):
                Datetime list.
            PRICE (14):
                Price.
        """

        UNSPECIFIED = 0
        UNKNOWN = 1
        INT64 = 2
        DOUBLE = 3
        STRING = 4
        BOOLEAN = 5
        URL = 6
        DATE_TIME = 7
        INT64_LIST = 8
        DOUBLE_LIST = 9
        STRING_LIST = 10
        BOOLEAN_LIST = 11
        URL_LIST = 12
        DATE_TIME_LIST = 13
        PRICE = 14


__all__ = tuple(sorted(__protobuf__.manifest))
