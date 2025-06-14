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
        "ConversionAdjustmentTypeEnum",
    },
)


class ConversionAdjustmentTypeEnum(proto.Message):
    r"""Container for enum describing conversion adjustment types."""

    class ConversionAdjustmentType(proto.Enum):
        r"""The different actions advertisers can take to adjust the
        conversions that they already reported. Retractions negate a
        conversion. Restatements change the value of a conversion.

        Values:
            UNSPECIFIED (0):
                Not specified.
            UNKNOWN (1):
                Represents value unknown in this version.
            RETRACTION (2):
                Negates a conversion so that its total value
                and count are both zero.
            RESTATEMENT (3):
                Changes the value of a conversion.
            ENHANCEMENT (4):
                Supplements an existing conversion with
                provided user identifiers and user agent, which
                can be used by Google to enhance the conversion
                count.
        """

        UNSPECIFIED = 0
        UNKNOWN = 1
        RETRACTION = 2
        RESTATEMENT = 3
        ENHANCEMENT = 4


__all__ = tuple(sorted(__protobuf__.manifest))
