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
        "LoyaltyMembershipEnum",
    },
)


class LoyaltyMembershipEnum(proto.Message):
    r"""Container for enumeration of loyalty membership."""

    class LoyaltyMembership(proto.Enum):
        r"""Enumerates loyalty membership.

        Values:
            UNSPECIFIED (0):
                Not specified.
            UNKNOWN (1):
                Unknown.
            NONMEMBER (2):
                The user is not a member of the loyalty
                program.
            TIER1 (3):
                The user is a tier 1 member of the loyalty
                program.
            TIER2 (4):
                The user is a tier 2 member of the loyalty
                program.
            TIER3 (5):
                The user is a tier 3 member of the loyalty
                program.
            TIER4 (6):
                The user is a tier 4 member of the loyalty
                program.
            TIER5 (7):
                The user is a tier 5 member of the loyalty
                program.
            TIER6 (8):
                The user is a tier 6 member of the loyalty
                program.
            TIER7 (9):
                The user is a tier 7 member of the loyalty
                program.
        """

        UNSPECIFIED = 0
        UNKNOWN = 1
        NONMEMBER = 2
        TIER1 = 3
        TIER2 = 4
        TIER3 = 5
        TIER4 = 6
        TIER5 = 7
        TIER6 = 8
        TIER7 = 9


__all__ = tuple(sorted(__protobuf__.manifest))
