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
        "MatchingFunctionContextTypeEnum",
    },
)


class MatchingFunctionContextTypeEnum(proto.Message):
    r"""Container for context types for an operand in a matching
    function.

    """

    class MatchingFunctionContextType(proto.Enum):
        r"""Possible context types for an operand in a matching function.

        Values:
            UNSPECIFIED (0):
                Not specified.
            UNKNOWN (1):
                Used for return value only. Represents value
                unknown in this version.
            FEED_ITEM_ID (2):
                Feed item id in the request context.
            DEVICE_NAME (3):
                The device being used (possible values are
                'Desktop' or 'Mobile').
            FEED_ITEM_SET_ID (4):
                Feed item set id in the request context.
        """

        UNSPECIFIED = 0
        UNKNOWN = 1
        FEED_ITEM_ID = 2
        DEVICE_NAME = 3
        FEED_ITEM_SET_ID = 4


__all__ = tuple(sorted(__protobuf__.manifest))
