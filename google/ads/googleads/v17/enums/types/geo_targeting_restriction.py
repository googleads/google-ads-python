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
    package="google.ads.googleads.v17.enums",
    marshal="google.ads.googleads.v17",
    manifest={
        "GeoTargetingRestrictionEnum",
    },
)


class GeoTargetingRestrictionEnum(proto.Message):
    r"""Message describing feed item geo targeting restriction."""

    class GeoTargetingRestriction(proto.Enum):
        r"""A restriction used to determine if the request context's
        geo should be matched.

        Values:
            UNSPECIFIED (0):
                Not specified.
            UNKNOWN (1):
                Used for return value only. Represents value
                unknown in this version.
            LOCATION_OF_PRESENCE (2):
                Indicates that request context should match
                the physical location of the user.
        """

        UNSPECIFIED = 0
        UNKNOWN = 1
        LOCATION_OF_PRESENCE = 2


__all__ = tuple(sorted(__protobuf__.manifest))
