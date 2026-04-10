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
        "ReservationRequestTypeEnum",
    },
)


class ReservationRequestTypeEnum(proto.Message):
    r"""Container for enum describing the request type of a
    reservation booking.

    """

    class ReservationRequestType(proto.Enum):
        r"""Enum describing the request type of a reservation booking.

        Values:
            UNSPECIFIED (0):
                Not specified.
            UNKNOWN (1):
                Used for return value only. Represents value
                unknown in this version.
            BOOK (2):
                Book the campaign. The campaign must have
                ENABLED status. If the campaign has a hold, it
                will remove the hold and confirm the contract.
            HOLD (3):
                Hold the inventory for the campaign. The
                campaign must have PAUSED status to request a
                hold.
        """

        UNSPECIFIED = 0
        UNKNOWN = 1
        BOOK = 2
        HOLD = 3


__all__ = tuple(sorted(__protobuf__.manifest))
