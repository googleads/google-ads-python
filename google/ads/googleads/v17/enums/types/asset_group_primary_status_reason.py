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
        "AssetGroupPrimaryStatusReasonEnum",
    },
)


class AssetGroupPrimaryStatusReasonEnum(proto.Message):
    r"""Container for enum describing possible asset group primary
    status reasons.

    """

    class AssetGroupPrimaryStatusReason(proto.Enum):
        r"""Enum describing the possible asset group primary status
        reasons. Provides reasons into why an asset group is not serving
        or not serving optimally. It will be empty when the asset group
        is serving without issues.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        ASSET_GROUP_PAUSED = 2
        ASSET_GROUP_REMOVED = 3
        CAMPAIGN_REMOVED = 4
        CAMPAIGN_PAUSED = 5
        CAMPAIGN_PENDING = 6
        CAMPAIGN_ENDED = 7
        ASSET_GROUP_LIMITED = 8
        ASSET_GROUP_DISAPPROVED = 9
        ASSET_GROUP_UNDER_REVIEW = 10


__all__ = tuple(sorted(__protobuf__.manifest))
