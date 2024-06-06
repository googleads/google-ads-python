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
    package="google.ads.googleads.v17.errors",
    marshal="google.ads.googleads.v17",
    manifest={
        "ConversionGoalCampaignConfigErrorEnum",
    },
)


class ConversionGoalCampaignConfigErrorEnum(proto.Message):
    r"""Container for enum describing possible conversion goal
    campaign config errors.

    """

    class ConversionGoalCampaignConfigError(proto.Enum):
        r"""Enum describing possible conversion goal campaign config
        errors.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        CANNOT_USE_CAMPAIGN_GOAL_FOR_SEARCH_ADS_360_MANAGED_CAMPAIGN = 2
        CUSTOM_GOAL_DOES_NOT_BELONG_TO_GOOGLE_ADS_CONVERSION_CUSTOMER = 3
        CAMPAIGN_CANNOT_USE_UNIFIED_GOALS = 4
        EMPTY_CONVERSION_GOALS = 5
        STORE_SALE_STORE_VISIT_CANNOT_BE_BOTH_INCLUDED = 6
        PERFORMANCE_MAX_CAMPAIGN_CANNOT_USE_CUSTOM_GOAL_WITH_STORE_SALES = 7


__all__ = tuple(sorted(__protobuf__.manifest))
