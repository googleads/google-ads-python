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
    package="google.ads.googleads.v26.errors",
    marshal="google.ads.googleads.v26",
    manifest={
        "BudgetNetworkSettingErrorEnum",
    },
)


class BudgetNetworkSettingErrorEnum(proto.Message):
    r"""Container for enum describing possible budget network setting
    errors.

    """

    class BudgetNetworkSettingError(proto.Enum):
        r"""Enum describing possible budget network setting errors.

        Values:
            UNSPECIFIED (0):
                Enum unspecified.
            UNKNOWN (1):
                The received error code is not known in this
                version.
            DUPLICATE_CHANNEL_ACROSS_PRIORITY_TIERS (2):
                A network channel cannot appear in more than
                one priority tier.
            CAP_NOT_ALLOWED_FOR_PRIMARY_TIER (3):
                Budget caps are not allowed on channels in
                the primary priority tier (TIER1).
            MISSING_PRIMARY_PRIORITY_CHANNEL (4):
                A primary priority tier (TIER1) with at least
                one network channel is required.
            INVALID_PRIORITY_TIER (5):
                The specified priority tier is invalid or
                unsupported.
            UNSUPPORTED_NETWORK_CHANNEL (6):
                The specified network channel is not
                supported for the given advertising channel
                type.
            UNSUPPORTED_ADVERTISING_CHANNEL_TYPE (7):
                The specified advertising channel type is not
                supported for budget network settings.
            CANNOT_BE_SET_ON_FLIGHTED_BUDGET (8):
                Budget network settings cannot be set on
                custom-period (flighted) budgets.
            INCOMPLETE_NETWORK_CHANNELS (9):
                All supported network channels for the
                advertising channel type must be assigned to a
                priority tier.
            CUSTOMER_NOT_ALLOWLISTED (10):
                The customer is not allowlisted for budget
                network settings.
            BUDGET_CAPS_UNSUPPORTED_FOR_ADVERTISING_CHANNEL_TYPE (11):
                Budget caps are not supported for the
                specified advertising channel type.
        """

        UNSPECIFIED = 0
        UNKNOWN = 1
        DUPLICATE_CHANNEL_ACROSS_PRIORITY_TIERS = 2
        CAP_NOT_ALLOWED_FOR_PRIMARY_TIER = 3
        MISSING_PRIMARY_PRIORITY_CHANNEL = 4
        INVALID_PRIORITY_TIER = 5
        UNSUPPORTED_NETWORK_CHANNEL = 6
        UNSUPPORTED_ADVERTISING_CHANNEL_TYPE = 7
        CANNOT_BE_SET_ON_FLIGHTED_BUDGET = 8
        INCOMPLETE_NETWORK_CHANNELS = 9
        CUSTOMER_NOT_ALLOWLISTED = 10
        BUDGET_CAPS_UNSUPPORTED_FOR_ADVERTISING_CHANNEL_TYPE = 11


__all__ = tuple(sorted(__protobuf__.manifest))
