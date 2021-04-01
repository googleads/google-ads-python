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
    package="google.ads.googleads.v6.enums",
    marshal="google.ads.googleads.v6",
    manifest={"AssetFieldTypeEnum",},
)


class AssetFieldTypeEnum(proto.Message):
    r"""Container for enum describing the possible placements of an
    asset.
    """

    class AssetFieldType(proto.Enum):
        r"""Enum describing the possible placements of an asset."""
        UNSPECIFIED = 0
        UNKNOWN = 1
        HEADLINE = 2
        DESCRIPTION = 3
        MANDATORY_AD_TEXT = 4
        MARKETING_IMAGE = 5
        MEDIA_BUNDLE = 6
        YOUTUBE_VIDEO = 7
        BOOK_ON_GOOGLE = 8
        LEAD_FORM = 9


__all__ = tuple(sorted(__protobuf__.manifest))
