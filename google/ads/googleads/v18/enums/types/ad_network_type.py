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
        "AdNetworkTypeEnum",
    },
)


class AdNetworkTypeEnum(proto.Message):
    r"""Container for enumeration of Google Ads network types."""

    class AdNetworkType(proto.Enum):
        r"""Enumerates Google Ads network types.

        Values:
            UNSPECIFIED (0):
                Not specified.
            UNKNOWN (1):
                The value is unknown in this version.
            SEARCH (2):
                Google search.
            SEARCH_PARTNERS (3):
                Search partners.
            CONTENT (4):
                Display Network.
            MIXED (7):
                Cross-network.
            YOUTUBE (8):
                YouTube
            GOOGLE_TV (9):
                Google TV
            GOOGLE_OWNED_CHANNELS (10):
                Google Owned Channels such as Discover feed,
                Gmail, YouTube. This network is only used by
                Demand Gen campaigns.
        """

        UNSPECIFIED = 0
        UNKNOWN = 1
        SEARCH = 2
        SEARCH_PARTNERS = 3
        CONTENT = 4
        MIXED = 7
        YOUTUBE = 8
        GOOGLE_TV = 9
        GOOGLE_OWNED_CHANNELS = 10


__all__ = tuple(sorted(__protobuf__.manifest))
