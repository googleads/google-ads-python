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
    package="google.ads.googleads.v26.enums",
    marshal="google.ads.googleads.v26",
    manifest={
        "ChannelPriorityTierEnum",
    },
)


class ChannelPriorityTierEnum(proto.Message):
    r"""Container for enum describing the priority tier of a network
    channel in waterfall prioritization.

    """

    class ChannelPriorityTier(proto.Enum):
        r"""Priority tiers for channel prioritization.

        Values:
            UNSPECIFIED (0):
                Not specified.
            UNKNOWN (1):
                Used for return value only. Represents value
                unknown in this version.
            TIER1 (2):
                Primary priority tier (allocated first before
                lower tiers).
            TIER2 (3):
                Secondary priority tier (allocated remaining
                budget after Tier 1).
        """

        UNSPECIFIED = 0
        UNKNOWN = 1
        TIER1 = 2
        TIER2 = 3


__all__ = tuple(sorted(__protobuf__.manifest))
