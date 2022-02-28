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
    package="google.ads.googleads.v9.enums",
    marshal="google.ads.googleads.v9",
    manifest={"AssetSetTypeEnum",},
)


class AssetSetTypeEnum(proto.Message):
    r"""Container for enum describing possible types of an asset set.
    """

    class AssetSetType(proto.Enum):
        r"""Possible types of an asset set."""
        UNSPECIFIED = 0
        UNKNOWN = 1
        PAGE_FEED = 2
        DYNAMIC_EDUCATION = 3
        MERCHANT_CENTER_FEED = 4


__all__ = tuple(sorted(__protobuf__.manifest))
