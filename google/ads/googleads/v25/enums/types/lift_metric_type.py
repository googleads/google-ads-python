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
        "LiftMetricTypeEnum",
    },
)


class LiftMetricTypeEnum(proto.Message):
    r"""Container for enum describing the type of lift being studied."""

    class LiftMetricType(proto.Enum):
        r"""Specifies the type of lift being studied.

        Values:
            UNSPECIFIED (0):
                Not specified.
            UNKNOWN (1):
                Used for return value only. Represents value
                unknown in this version.
            CONVERSION (2):
                Conversion lift is running on this set of
                campaigns.
            SEARCH (3):
                Search lift is running on this set of
                campaigns.
            SURVEY (4):
                Survey lift is running on this set of
                campaigns.
        """

        UNSPECIFIED = 0
        UNKNOWN = 1
        CONVERSION = 2
        SEARCH = 3
        SURVEY = 4


__all__ = tuple(sorted(__protobuf__.manifest))
