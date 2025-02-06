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
    package="google.ads.googleads.v16.enums",
    marshal="google.ads.googleads.v16",
    manifest={
        "AdGroupPrimaryStatusReasonEnum",
    },
)


class AdGroupPrimaryStatusReasonEnum(proto.Message):
    r"""Ad Group Primary Status Reason. Provides insight into why an
    ad group is not serving or not serving optimally. These reasons
    are aggregated to determine an overall AdGroupPrimaryStatus.

    """

    class AdGroupPrimaryStatusReason(proto.Enum):
        r"""Possible ad group status reasons."""
        UNSPECIFIED = 0
        UNKNOWN = 1
        CAMPAIGN_REMOVED = 2
        CAMPAIGN_PAUSED = 3
        CAMPAIGN_PENDING = 4
        CAMPAIGN_ENDED = 5
        AD_GROUP_PAUSED = 6
        AD_GROUP_REMOVED = 7
        AD_GROUP_INCOMPLETE = 8
        KEYWORDS_PAUSED = 9
        NO_KEYWORDS = 10
        AD_GROUP_ADS_PAUSED = 11
        NO_AD_GROUP_ADS = 12
        HAS_ADS_DISAPPROVED = 13
        HAS_ADS_LIMITED_BY_POLICY = 14
        MOST_ADS_UNDER_REVIEW = 15
        CAMPAIGN_DRAFT = 16
        AD_GROUP_PAUSED_DUE_TO_LOW_ACTIVITY = 19


__all__ = tuple(sorted(__protobuf__.manifest))
