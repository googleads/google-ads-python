# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
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
    package="google.ads.googleads.v15.enums",
    marshal="google.ads.googleads.v15",
    manifest={
        "ReachPlanSurfaceEnum",
    },
)


class ReachPlanSurfaceEnum(proto.Message):
    r"""Container for enum describing surfaces available for
    targeting in forecasts. Surfaces refer to the available types of
    ad inventories such as In-Feed, In-Stream, and Shorts.

    """

    class ReachPlanSurface(proto.Enum):
        r"""Surfaces available to target in reach forecasts."""
        UNSPECIFIED = 0
        UNKNOWN = 1
        IN_FEED = 2
        IN_STREAM_BUMPER = 3
        IN_STREAM_NON_SKIPPABLE = 4
        IN_STREAM_SKIPPABLE = 5
        SHORTS = 6


__all__ = tuple(sorted(__protobuf__.manifest))
