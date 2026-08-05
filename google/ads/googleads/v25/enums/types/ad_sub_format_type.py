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
        "AdSubFormatTypeEnum",
    },
)


class AdSubFormatTypeEnum(proto.Message):
    r"""Container for enumeration of Google Ads sub format types."""

    class AdSubFormatType(proto.Enum):
        r"""Enumerates Google Ads sub format types.

        Values:
            UNSPECIFIED (0):
                Not specified.
            UNKNOWN (1):
                Unknown.
            UNSEGMENTED (2):
                Category for formats that are not further
                split into sub formats.
            INSTREAM_NON_SKIPPABLE_STANDARD (3):
                Standard length non-skippable instream
                YouTube ad.
            INSTREAM_NON_SKIPPABLE_MAX30_SEC (4):
                Non-skippable instream YouTube ad with a
                duration up to 30.99 seconds.
            INSTREAM_NON_SKIPPABLE_MAX60_SEC (5):
                Non-skippable instream YouTube ad with a
                duration between 31 and 60 seconds.
        """

        UNSPECIFIED = 0
        UNKNOWN = 1
        UNSEGMENTED = 2
        INSTREAM_NON_SKIPPABLE_STANDARD = 3
        INSTREAM_NON_SKIPPABLE_MAX30_SEC = 4
        INSTREAM_NON_SKIPPABLE_MAX60_SEC = 5


__all__ = tuple(sorted(__protobuf__.manifest))
