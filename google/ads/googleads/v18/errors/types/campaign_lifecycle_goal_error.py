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
    package="google.ads.googleads.v18.errors",
    marshal="google.ads.googleads.v18",
    manifest={"CampaignLifecycleGoalErrorEnum",},
)


class CampaignLifecycleGoalErrorEnum(proto.Message):
    r"""Container for enum describing possible campaign lifecycle
    goal errors.

    """

    class CampaignLifecycleGoalError(proto.Enum):
        r"""Enum describing possible campaign lifecycle goal errors."""
        UNSPECIFIED = 0
        UNKNOWN = 1
        CAMPAIGN_MISSING = 2
        INVALID_CAMPAIGN = 3
        CUSTOMER_ACQUISITION_INVALID_OPTIMIZATION_MODE = 4
        INCOMPATIBLE_BIDDING_STRATEGY = 5
        MISSING_PURCHASE_GOAL = 6
        CUSTOMER_ACQUISITION_INVALID_HIGH_LIFETIME_VALUE = 7
        CUSTOMER_ACQUISITION_UNSUPPORTED_CAMPAIGN_TYPE = 8
        CUSTOMER_ACQUISITION_INVALID_VALUE = 9
        CUSTOMER_ACQUISITION_VALUE_MISSING = 10
        CUSTOMER_ACQUISITION_MISSING_EXISTING_CUSTOMER_DEFINITION = 11
        CUSTOMER_ACQUISITION_MISSING_HIGH_VALUE_CUSTOMER_DEFINITION = 12


__all__ = tuple(sorted(__protobuf__.manifest))
