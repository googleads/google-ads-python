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
        "IncentiveErrorEnum",
    },
)


class IncentiveErrorEnum(proto.Message):
    r"""Container for enum describing possible incentive errors."""

    class IncentiveError(proto.Enum):
        r"""Enum describing possible incentive errors.

        Values:
            UNSPECIFIED (0):
                Enum unspecified.
            UNKNOWN (1):
                The received error code is not known in this
                version.
            INVALID_INCENTIVE_ID (2):
                The incentive ID is either invalid or not
                supported for the given country.
            MAX_INCENTIVES_REDEEMED (3):
                The maximum number of coupons has been
                redeemed.
            ACCOUNT_TOO_OLD (4):
                This incentive cannot be applied because too
                much time has passed since the account's first
                ad impression.
            BILLING_COUNTRY_NOT_ELIGIBLE (5):
                This incentive cannot be applied because the
                billing country is not eligible.
            USER_IS_MCC_MANAGER (6):
                This incentive cannot be applied because the
                user is a manager account.
            USER_SUSPENDED (7):
                This incentive cannot be applied because the
                account is suspended.
            MAX_PENDING_INCENTIVES (8):
                This incentive cannot be applied because you
                have reached the maximum number of pending
                incentives.
            ACCOUNT_HAD_RECENT_SPEND (9):
                This incentive cannot be applied because the
                account had recent spend.
            MAX_INCENTIVES_REDEEMED_FROM_OFFER (10):
                This incentive cannot be applied because you
                have already redeemed the maximum number of
                incentives from this offer.
            MISMATCHING_BILLING_COUNTRY_CODE (11):
                The billing country code provided in the
                request does not match the customer's country
                code.
        """

        UNSPECIFIED = 0
        UNKNOWN = 1
        INVALID_INCENTIVE_ID = 2
        MAX_INCENTIVES_REDEEMED = 3
        ACCOUNT_TOO_OLD = 4
        BILLING_COUNTRY_NOT_ELIGIBLE = 5
        USER_IS_MCC_MANAGER = 6
        USER_SUSPENDED = 7
        MAX_PENDING_INCENTIVES = 8
        ACCOUNT_HAD_RECENT_SPEND = 9
        MAX_INCENTIVES_REDEEMED_FROM_OFFER = 10
        MISMATCHING_BILLING_COUNTRY_CODE = 11


__all__ = tuple(sorted(__protobuf__.manifest))
