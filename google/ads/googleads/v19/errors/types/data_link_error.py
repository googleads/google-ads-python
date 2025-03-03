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
    package="google.ads.googleads.v19.errors",
    marshal="google.ads.googleads.v19",
    manifest={
        "DataLinkErrorEnum",
    },
)


class DataLinkErrorEnum(proto.Message):
    r"""Container for enum describing possible DataLink errors."""

    class DataLinkError(proto.Enum):
        r"""Enum describing possible DataLink errors."""

        UNSPECIFIED = 0
        UNKNOWN = 1
        YOUTUBE_CHANNEL_ID_INVALID = 2
        YOUTUBE_VIDEO_ID_INVALID = 3
        YOUTUBE_VIDEO_FROM_DIFFERENT_CHANNEL = 4
        PERMISSION_DENIED = 5
        INVALID_STATUS = 6
        INVALID_UPDATE_STATUS = 7
        INVALID_RESOURCE_NAME = 8


__all__ = tuple(sorted(__protobuf__.manifest))
