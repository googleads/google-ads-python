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
    package="google.ads.googleads.v19.enums",
    marshal="google.ads.googleads.v19",
    manifest={
        "SharedSetTypeEnum",
    },
)


class SharedSetTypeEnum(proto.Message):
    r"""Container for enum describing types of shared sets."""

    class SharedSetType(proto.Enum):
        r"""Enum listing the possible shared set types.

        Values:
            UNSPECIFIED (0):
                Not specified.
            UNKNOWN (1):
                Used for return value only. Represents value
                unknown in this version.
            NEGATIVE_KEYWORDS (2):
                A set of keywords that can be excluded from
                targeting.
            NEGATIVE_PLACEMENTS (3):
                A set of placements that can be excluded from
                targeting.
            ACCOUNT_LEVEL_NEGATIVE_KEYWORDS (4):
                An account-level set of keywords that can be
                excluded from targeting.
            BRANDS (5):
                A set of brands can be included or excluded
                from targeting.
        """

        UNSPECIFIED = 0
        UNKNOWN = 1
        NEGATIVE_KEYWORDS = 2
        NEGATIVE_PLACEMENTS = 3
        ACCOUNT_LEVEL_NEGATIVE_KEYWORDS = 4
        BRANDS = 5


__all__ = tuple(sorted(__protobuf__.manifest))
