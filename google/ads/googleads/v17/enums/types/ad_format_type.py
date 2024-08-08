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
        "AdFormatTypeEnum",
    },
)


class AdFormatTypeEnum(proto.Message):
    r"""Container for enumeration of Google Ads format types."""

    class AdFormatType(proto.Enum):
        r"""Enumerates Google Ads format types.

        Note that this segmentation is available only for Video and
        Discovery campaigns. For assets, only video assets are
        supported.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        OTHER = 2
        UNSEGMENTED = 3
        INSTREAM_SKIPPABLE = 4
        INSTREAM_NON_SKIPPABLE = 5
        INFEED = 6
        BUMPER = 7
        OUTSTREAM = 8
        MASTHEAD = 9
        AUDIO = 10
        SHORTS = 11


__all__ = tuple(sorted(__protobuf__.manifest))
