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
        "ReachPlanNetworkEnum",
    },
)


class ReachPlanNetworkEnum(proto.Message):
    r"""Container for enum describing plannable networks."""

    class ReachPlanNetwork(proto.Enum):
        r"""Possible plannable network values.

        Values:
            UNSPECIFIED (0):
                Not specified.
            UNKNOWN (1):
                Used as a return value only. Represents value
                unknown in this version.
            YOUTUBE (2):
                YouTube network.
            GOOGLE_VIDEO_PARTNERS (3):
                Google Video Partners (GVP) network.
            YOUTUBE_AND_GOOGLE_VIDEO_PARTNERS (4):
                A combination of the YouTube network and the
                Google Video Partners network.
        """

        UNSPECIFIED = 0
        UNKNOWN = 1
        YOUTUBE = 2
        GOOGLE_VIDEO_PARTNERS = 3
        YOUTUBE_AND_GOOGLE_VIDEO_PARTNERS = 4


__all__ = tuple(sorted(__protobuf__.manifest))
