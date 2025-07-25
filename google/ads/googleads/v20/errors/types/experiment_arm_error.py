# -*- coding: utf-8 -*-
# Copyright 2025 Google LLC
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
    package="google.ads.googleads.v20.errors",
    marshal="google.ads.googleads.v20",
    manifest={
        "ExperimentArmErrorEnum",
    },
)


class ExperimentArmErrorEnum(proto.Message):
    r"""Container for enum describing possible experiment arm error."""

    class ExperimentArmError(proto.Enum):
        r"""Enum describing possible experiment arm errors.

        Values:
            UNSPECIFIED (0):
                Enum unspecified.
            UNKNOWN (1):
                The received error code is not known in this
                version.
            EXPERIMENT_ARM_COUNT_LIMIT_EXCEEDED (2):
                Number of experiment arms is above limit.
            INVALID_CAMPAIGN_STATUS (3):
                Cannot add campaign with invalid status to
                the experiment arm.
            DUPLICATE_EXPERIMENT_ARM_NAME (4):
                Cannot add duplicate experiment arm name in
                one experiment.
            CANNOT_SET_TREATMENT_ARM_CAMPAIGN (5):
                Cannot set campaigns of treatment experiment
                arm.
            CANNOT_MODIFY_CAMPAIGN_IDS (6):
                Cannot edit campaign ids in trial arms in non
                SETUP experiment.
            CANNOT_MODIFY_CAMPAIGN_WITHOUT_SUFFIX_SET (7):
                Cannot modify the campaigns in the control
                arm if there is not a suffix set in the trial.
            CANNOT_MUTATE_TRAFFIC_SPLIT_AFTER_START (8):
                Traffic split related settings (like traffic
                share bounds) can't be modified after the trial
                has started.
            CANNOT_ADD_CAMPAIGN_WITH_SHARED_BUDGET (9):
                Cannot use shared budget on experiment's
                control campaign.
            CANNOT_ADD_CAMPAIGN_WITH_CUSTOM_BUDGET (10):
                Cannot use custom budget on experiment's
                control campaigns.
            CANNOT_ADD_CAMPAIGNS_WITH_DYNAMIC_ASSETS_ENABLED (11):
                Cannot have enable_dynamic_assets turned on in experiment's
                campaigns.
            UNSUPPORTED_CAMPAIGN_ADVERTISING_CHANNEL_SUB_TYPE (12):
                Cannot use campaign's advertising channel sub
                type in experiment.
            CANNOT_ADD_BASE_CAMPAIGN_WITH_DATE_RANGE (13):
                Experiment date range must be within base
                campaign's date range.
            BIDDING_STRATEGY_NOT_SUPPORTED_IN_EXPERIMENTS (14):
                Bidding strategy is not supported in
                experiments.
            TRAFFIC_SPLIT_NOT_SUPPORTED_FOR_CHANNEL_TYPE (15):
                Traffic split is not supported for some
                channel types.
        """

        UNSPECIFIED = 0
        UNKNOWN = 1
        EXPERIMENT_ARM_COUNT_LIMIT_EXCEEDED = 2
        INVALID_CAMPAIGN_STATUS = 3
        DUPLICATE_EXPERIMENT_ARM_NAME = 4
        CANNOT_SET_TREATMENT_ARM_CAMPAIGN = 5
        CANNOT_MODIFY_CAMPAIGN_IDS = 6
        CANNOT_MODIFY_CAMPAIGN_WITHOUT_SUFFIX_SET = 7
        CANNOT_MUTATE_TRAFFIC_SPLIT_AFTER_START = 8
        CANNOT_ADD_CAMPAIGN_WITH_SHARED_BUDGET = 9
        CANNOT_ADD_CAMPAIGN_WITH_CUSTOM_BUDGET = 10
        CANNOT_ADD_CAMPAIGNS_WITH_DYNAMIC_ASSETS_ENABLED = 11
        UNSUPPORTED_CAMPAIGN_ADVERTISING_CHANNEL_SUB_TYPE = 12
        CANNOT_ADD_BASE_CAMPAIGN_WITH_DATE_RANGE = 13
        BIDDING_STRATEGY_NOT_SUPPORTED_IN_EXPERIMENTS = 14
        TRAFFIC_SPLIT_NOT_SUPPORTED_FOR_CHANNEL_TYPE = 15


__all__ = tuple(sorted(__protobuf__.manifest))
