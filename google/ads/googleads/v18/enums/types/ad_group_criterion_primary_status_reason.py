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
    package="google.ads.googleads.v18.enums",
    marshal="google.ads.googleads.v18",
    manifest={"AdGroupCriterionPrimaryStatusReasonEnum",},
)


class AdGroupCriterionPrimaryStatusReasonEnum(proto.Message):
    r"""Container for enum describing possible ad group criterion
    primary status reasons.

    """

    class AdGroupCriterionPrimaryStatusReason(proto.Enum):
        r"""Enum describing the possible Ad Group Criterion primary
        status reasons. Provides insight into why an Ad Group Criterion
        is not serving or not serving optimally. These reasons are
        aggregated to determine an overall Ad Group Criterion primary
        status.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        CAMPAIGN_PENDING = 2
        CAMPAIGN_CRITERION_NEGATIVE = 3
        CAMPAIGN_PAUSED = 4
        CAMPAIGN_REMOVED = 5
        CAMPAIGN_ENDED = 6
        AD_GROUP_PAUSED = 7
        AD_GROUP_REMOVED = 8
        AD_GROUP_CRITERION_DISAPPROVED = 9
        AD_GROUP_CRITERION_RARELY_SERVED = 10
        AD_GROUP_CRITERION_LOW_QUALITY = 11
        AD_GROUP_CRITERION_UNDER_REVIEW = 12
        AD_GROUP_CRITERION_PENDING_REVIEW = 13
        AD_GROUP_CRITERION_BELOW_FIRST_PAGE_BID = 14
        AD_GROUP_CRITERION_NEGATIVE = 15
        AD_GROUP_CRITERION_RESTRICTED = 16
        AD_GROUP_CRITERION_PAUSED = 17
        AD_GROUP_CRITERION_PAUSED_DUE_TO_LOW_ACTIVITY = 18
        AD_GROUP_CRITERION_REMOVED = 19


__all__ = tuple(sorted(__protobuf__.manifest))
