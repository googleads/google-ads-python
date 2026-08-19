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
        "LiftMeasurementFlightStatusEnum",
    },
)


class LiftMeasurementFlightStatusEnum(proto.Message):
    r"""Container for enum describing the status of a
    LiftMeasurementFlight.

    """

    class LiftMeasurementFlightStatus(proto.Enum):
        r"""Status of a LiftMeasurementFlight.

        Values:
            UNSPECIFIED (0):
                Not specified.
            UNKNOWN (1):
                Used for return value only. Represents value
                unknown in this version.
            ENABLED (2):
                The flight is enabled.
            STOPPED (3):
                The flight has been stopped.
        """

        UNSPECIFIED = 0
        UNKNOWN = 1
        ENABLED = 2
        STOPPED = 3


__all__ = tuple(sorted(__protobuf__.manifest))
