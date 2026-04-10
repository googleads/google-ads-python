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
    package="google.ads.googleads.v23.enums",
    marshal="google.ads.googleads.v23",
    manifest={
        "PartnershipOpportunityEnum",
    },
)


class PartnershipOpportunityEnum(proto.Message):
    r"""Container for enum describing partnership opportunity."""

    class PartnershipOpportunity(proto.Enum):
        r"""Partnership opportunity between media buyers and creators for
        paid media on YouTube.

        Values:
            UNSPECIFIED (0):
                Default value. This value is equivalent to
                null.
            UNKNOWN (1):
                Output-only. Represents a format not yet
                defined in this enum.
            CREATOR_PARTNERSHIPS (2):
                A partnership opportunity that allows
                advertisers to partner with YouTube creators on
                sponsored content that mentions a brand or
                product. See
                https://support.google.com/google-ads/answer/15471603
                to learn more.
            CREATOR_TAKEOVER (3):
                A partnership opportunity that gives brands
                exclusive access to all ad slots on channels of
                top creators.
            PARTNERSHIP_ADS (4):
                A partnership opportunity that enables brands
                to use YouTube creator videos in their ad
                campaigns. See
                https://support.google.com/google-ads/answer/15223349
                to learn more.
            YOUTUBE_SELECT_LINEUPS (5):
                A partnership opportunity that allows
                advertisers to buy specific ad placements on a
                reservation basis to target among the top 1% of
                popular channels on YouTube. See
                https://support.google.com/google-ads/answer/6030919
                to learn more.
        """

        UNSPECIFIED = 0
        UNKNOWN = 1
        CREATOR_PARTNERSHIPS = 2
        CREATOR_TAKEOVER = 3
        PARTNERSHIP_ADS = 4
        YOUTUBE_SELECT_LINEUPS = 5


__all__ = tuple(sorted(__protobuf__.manifest))
