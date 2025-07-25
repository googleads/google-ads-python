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
    package="google.ads.googleads.v20.enums",
    marshal="google.ads.googleads.v20",
    manifest={
        "ListingGroupFilterProductConditionEnum",
    },
)


class ListingGroupFilterProductConditionEnum(proto.Message):
    r"""Condition of a product offer."""

    class ListingGroupFilterProductCondition(proto.Enum):
        r"""Enum describing the condition of a product offer.

        Values:
            UNSPECIFIED (0):
                Not specified.
            UNKNOWN (1):
                Used for return value only. Represents value
                unknown in this version.
            NEW (2):
                The product condition is new.
            REFURBISHED (3):
                The product condition is refurbished.
            USED (4):
                The product condition is used.
        """

        UNSPECIFIED = 0
        UNKNOWN = 1
        NEW = 2
        REFURBISHED = 3
        USED = 4


__all__ = tuple(sorted(__protobuf__.manifest))
