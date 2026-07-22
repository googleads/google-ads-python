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
        "IncentiveTypeEnum",
    },
)


class IncentiveTypeEnum(proto.Message):
    r"""Container for enum describing types of incentives."""

    class IncentiveType(proto.Enum):
        r"""Types of incentives offered

        Values:
            UNSPECIFIED (0):
                Not specified.
            UNKNOWN (1):
                Unknown incentive type. Should not be used as
                a value explicitly.
            ACQUISITION (2):
                An acquisition incentive.
        """

        UNSPECIFIED = 0
        UNKNOWN = 1
        ACQUISITION = 2


__all__ = tuple(sorted(__protobuf__.manifest))
