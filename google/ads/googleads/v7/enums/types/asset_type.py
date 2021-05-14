# -*- coding: utf-8 -*-
# Copyright 2020 Google LLC
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
import proto  # type: ignore


__protobuf__ = proto.module(
    package="google.ads.googleads.v7.enums",
    marshal="google.ads.googleads.v7",
    manifest={"AssetTypeEnum",},
)


class AssetTypeEnum(proto.Message):
    r"""Container for enum describing the types of asset.    """

    class AssetType(proto.Enum):
        r"""Enum describing possible types of asset."""
        UNSPECIFIED = 0
        UNKNOWN = 1
        YOUTUBE_VIDEO = 2
        MEDIA_BUNDLE = 3
        IMAGE = 4
        TEXT = 5
        LEAD_FORM = 6
        BOOK_ON_GOOGLE = 7
        PROMOTION = 8
        CALLOUT = 9
        STRUCTURED_SNIPPET = 10
        SITELINK = 11


__all__ = tuple(sorted(__protobuf__.manifest))
