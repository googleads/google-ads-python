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
    package="google.ads.googleads.v26.enums",
    marshal="google.ads.googleads.v26",
    manifest={
        "BudgetNetworkIneligibleReasonEnum",
    },
)


class BudgetNetworkIneligibleReasonEnum(proto.Message):
    r"""Container for enum describing reasons why a campaign budget
    is ineligible for budget network settings.

    """

    class BudgetNetworkIneligibleReason(proto.Enum):
        r"""Reasons why a budget is ineligible for waterfall or budget
        cap allocation.

        Values:
            UNSPECIFIED (0):
                Not specified.
            UNKNOWN (1):
                Used for return value only. Represents value
                unknown in this version.
            UNSUPPORTED_BIDDING_STRATEGY (2):
                Associated campaign(s) use an unsupported
                bidding strategy.
            MIXED_CAMPAIGN_TYPES (3):
                Shared budget is associated with campaigns of
                mixed advertising channel types.
            HAS_ENABLED_TRIALS (4):
                Associated campaign(s) have active
                experiments/trials.
            UNSUPPORTED_BUDGET_PERIOD (5):
                Budget uses a custom period.
            MIXED_BIDDING_STRATEGIES (6):
                Shared budget is associated with campaigns of
                mixed bidding strategy types.
            INSUFFICIENT_ELIGIBLE_CHANNELS (7):
                Budget does not have all required network
                channels enabled.
        """

        UNSPECIFIED = 0
        UNKNOWN = 1
        UNSUPPORTED_BIDDING_STRATEGY = 2
        MIXED_CAMPAIGN_TYPES = 3
        HAS_ENABLED_TRIALS = 4
        UNSUPPORTED_BUDGET_PERIOD = 5
        MIXED_BIDDING_STRATEGIES = 6
        INSUFFICIENT_ELIGIBLE_CHANNELS = 7


__all__ = tuple(sorted(__protobuf__.manifest))
