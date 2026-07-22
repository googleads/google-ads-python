# -*- coding: utf-8 -*-
# Copyright 2026 Google LLC
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
    package="google.ads.googleads.v25.errors",
    marshal="google.ads.googleads.v25",
    manifest={
        "CampaignGoalConfigErrorEnum",
    },
)


class CampaignGoalConfigErrorEnum(proto.Message):
    r"""Container for enum describing possible campaign goal config
    errors.

    """

    class CampaignGoalConfigError(proto.Enum):
        r"""Enum describing possible campaign goal config errors.

        Values:
            UNSPECIFIED (0):
                Enum unspecified.
            UNKNOWN (1):
                The received error code is not known in this
                version.
            GOAL_NOT_FOUND (3):
                Goal is either removed or does not exist for
                this account.
            CAMPAIGN_NOT_FOUND (4):
                Campaign is either removed or does not exist.
            HIGH_LIFETIME_VALUE_PRESENT_BUT_VALUE_ABSENT (9):
                If high lifetime value is present then value
                should be present.
            HIGH_LIFETIME_VALUE_LESS_THAN_OR_EQUAL_TO_VALUE (10):
                High lifetime value should be greater than
                value.
            CUSTOMER_LIFECYCLE_OPTIMIZATION_CAMPAIGN_TYPE_NOT_SUPPORTED (11):
                When using customer lifecycle optimization
                goal, campaign type should be supported.
            CUSTOMER_NOT_ALLOWLISTED_FOR_RETENTION_ONLY (12):
                Customer must be allowlisted to use retention
                only goal.
            CAMPAIGN_OVERRIDE_VALUES_SET_FOR_NEW_CUSTOMER_ACQUISITION_TARGET_SPECIFIC_OPTION (13):
                New customer acquisition customer lifecycle
                optimization goal targeting only new customers
                should not have campaign override values set.
            CAMPAIGN_OVERRIDE_HIGH_LIFETIME_VALUE_NOT_SUPPORTED_FOR_CAMPAIGN_TYPE (14):
                New customer acquisition customer lifecycle
                optimization goal campaign override high
                lifetime values should only be set for supported
                campaign type.
            CANNOT_USE_INCOMPATIBLE_CLO_GOALS (15):
                Error when the campaign is attempting to
                combine incompatible CLO goals.
            LOYALTY_RETENTION_GOAL_INVALID_MODE (16):
                At least one mode (either enabling bid
                adjustments or showing benefits in PLA) must be
                enabled for loyalty retention goal.
        """

        UNSPECIFIED = 0
        UNKNOWN = 1
        GOAL_NOT_FOUND = 3
        CAMPAIGN_NOT_FOUND = 4
        HIGH_LIFETIME_VALUE_PRESENT_BUT_VALUE_ABSENT = 9
        HIGH_LIFETIME_VALUE_LESS_THAN_OR_EQUAL_TO_VALUE = 10
        CUSTOMER_LIFECYCLE_OPTIMIZATION_CAMPAIGN_TYPE_NOT_SUPPORTED = 11
        CUSTOMER_NOT_ALLOWLISTED_FOR_RETENTION_ONLY = 12
        CAMPAIGN_OVERRIDE_VALUES_SET_FOR_NEW_CUSTOMER_ACQUISITION_TARGET_SPECIFIC_OPTION = (
            13
        )
        CAMPAIGN_OVERRIDE_HIGH_LIFETIME_VALUE_NOT_SUPPORTED_FOR_CAMPAIGN_TYPE = (
            14
        )
        CANNOT_USE_INCOMPATIBLE_CLO_GOALS = 15
        LOYALTY_RETENTION_GOAL_INVALID_MODE = 16


__all__ = tuple(sorted(__protobuf__.manifest))
