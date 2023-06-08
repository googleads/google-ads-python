# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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
    package="google.ads.googleads.v14.enums",
    marshal="google.ads.googleads.v14",
    manifest={
        "OfflineEventUploadClientEnum",
    },
)


class OfflineEventUploadClientEnum(proto.Message):
    r"""All possible clients for an offline upload event."""

    class OfflineEventUploadClient(proto.Enum):
        r"""Next id: 5"""
        UNSPECIFIED = 0
        UNKNOWN = 1
        GOOGLE_ADS_API = 2
        GOOGLE_ADS_WEB_CLIENT = 3
        ADS_DATA_CONNECTOR = 4


__all__ = tuple(sorted(__protobuf__.manifest))
