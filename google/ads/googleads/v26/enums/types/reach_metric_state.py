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
        "ReachMetricStateEnum",
    },
)


class ReachMetricStateEnum(proto.Message):
    r"""Container for enum with additional information about reach
    metrics.

    """

    class ReachMetricState(proto.Enum):
        r"""Enum listing all possible reach metric states.

        Values:
            UNSPECIFIED (0):
                Not specified.
            UNKNOWN (1):
                Represents unknown value.
            COMPLETE (2):
                The corresponding reach metric is complete.
                Meaning that there was no suppression due to
                privacy, quality or any other reason.
            PRIVACY_SUPPRESSION (3):
                The reach metrics were suppressed due to
                privacy reasons.
            QUALITY_SUPPRESSION (4):
                The reach metrics were suppressed due to
                quality reasons.
            LOW_QUALITY (5):
                The reach metric is low quality.
            DATE_RANGE_BEYOND_RETENTION (6):
                The reach metrics are unavailable because the
                selected date range is beyond the data retention
                period of 3 years.
        """

        UNSPECIFIED = 0
        UNKNOWN = 1
        COMPLETE = 2
        PRIVACY_SUPPRESSION = 3
        QUALITY_SUPPRESSION = 4
        LOW_QUALITY = 5
        DATE_RANGE_BEYOND_RETENTION = 6


__all__ = tuple(sorted(__protobuf__.manifest))
