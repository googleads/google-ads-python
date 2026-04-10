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
    package="google.ads.googleads.v23.errors",
    marshal="google.ads.googleads.v23",
    manifest={
        "VideoReservationErrorEnum",
    },
)


class VideoReservationErrorEnum(proto.Message):
    r"""Container for enum describing possible video reservation
    errors.

    """

    class VideoReservationError(proto.Enum):
        r"""Enum describing possible video reservation errors.

        Values:
            UNSPECIFIED (0):
                Enum unspecified.
            UNKNOWN (1):
                The received error code is not known in this
                version.
            NEW_QUOTE_REQUIRED (2):
                The quote has expired.
            CAMPAIGN_END_TIME_TOO_DISTANT (3):
                The campaign's end date has to be less than
                120 days from now.
            BUDGET_TOO_SMALL (4):
                The campaign budget is too small. To get a
                quote, increase the budget.
            CAMPAIGN_DURATION_TOO_SHORT (5):
                The campaign must run for more than 24 hours.
            CAMPAIGN_NOT_ENABLED (6):
                The campaign must be enabled before booking.
            NOT_ENOUGH_AVAILABLE_INVENTORY (7):
                There aren't enough impressions available for
                the campaigns settings and targeting. Broaden
                the targeting or lower the budget of the
                campaign to get a quote.
            TARGETING_TOO_NARROW (8):
                There aren't enough impressions available for
                the campaign settings and targeting.
            UNSUPPORTED_AD_GROUP_TYPE (9):
                The type of the enabled ad group of this
                campaign isn't supported.
            UNSUPPORTED_BID_MODIFIER (10):
                Bid modifiers other than 0% or -100% aren't
                supported.
            CANNOT_CHANGE_PRICING_MODEL (11):
                The type of placement was changed. YouTube
                Select lineups can only be paired with other
                YouTube Select lineups.
            INCOMPATIBLE_TARGETING (12):
                More than one lineup was selected. Only one
                lineup per campaign can be targeted.
            UNSUPPORTED_FEATURE (13):
                Some options in this campaign aren't
                supported.
            MISSING_ELECTION_CERTIFICATE (14):
                The customer must be verified by Google to
                run election ads in the targeted country.
            CAMPAIGN_ENDED (15):
                This campaign has ended. Select a campaign
                that hasn't reached its end date.
            UNSUPPORTED_BUDGET_PERIOD (16):
                Daily budget isn't available for fixed CPM
                campaigns. To use fixed CPM, enter a campaign
                total budget.
            EXACTLY_ONE_ENABLED_ADGROUP_REQUIRED (17):
                The campaign must have exactly one enabled ad
                group for reservation.
            FREQUENCY_CAP_TOO_NARROW (18):
                The frequency cap is lower than the minimum
                allowed for an enabled campaign. Update the
                frequency cap to either a daily cap or a weekly
                cap with at least 3 impressions per week.
            TARGETED_PACK_NEEDS_DEAL (19):
                The targeted country requires either a deal
                or a market rate.
            DEAL_CURRENCY_MISMATCH (20):
                The account is set to a currency that doesn't
                match the currency of the rate card for the
                targeted video lineups.
            CANNOT_HOLD_CONTRACT (21):
                Quote holds are unavailable for this campaign
                configuration.
            CUSTOMER_NOT_ENABLED (22):
                The account is suspended. Contact support for
                more info.
            CUSTOMER_NOT_ALLOWED (23):
                The customer doesn't have permission to
                request a quote. Contact the account owner for
                more info.
            INVALID_ACCOUNT_TYPE (24):
                This account type can't request quotes. Use a
                different account or contact support for more
                info.
            ACCOUNT_IS_MANAGER (25):
                Google Account Managers can't request quotes
                for reservation campaigns.
            SEASONAL_LINEUP_BOOKING_WINDOW_NOT_OPEN (26):
                The booking window for this lineup is not
                open yet.
            SEASONAL_LINEUP_END_DATE_OFF_SEASON (27):
                The campaign end date is later than the
                allowable end date for this lineup. To continue
                booking, choose an earlier end date.
            SEASONAL_LINEUP_GEO_TARGETING_TOO_NARROW (28):
                There aren't enough impressions available for
                the campaign settings and targeting. Broaden the
                location targeting to get a quote.
            NO_MARKET_RATE_CARD_OR_BASE_RATE (29):
                The market rate for the targeted product
                isn't available.
            STALE_QUOTE (30):
                The quote is stale, get a new quote and try
                again.
            LINEUP_NOT_ALLOWED (31):
                Some of the targeted video lineups aren't
                available for reservation campaigns.
            UNSUPPORTED_BIDDING_STRATEGY (32):
                This bidding strategy is not supported for
                reservation.
            UNSUPPORTED_POSITIVE_GEO_TARGET_TYPE (33):
                The campaign settings contain a positive geo
                target type which is not allowed, for example
                Audio ads support PRESENCE only.
            VALIDATE_ONLY_REQUIRED (34):
                Only validate_only requests are supported.
            TOO_MANY_CAMPAIGNS (35):
                Too many campaigns in request.
        """

        UNSPECIFIED = 0
        UNKNOWN = 1
        NEW_QUOTE_REQUIRED = 2
        CAMPAIGN_END_TIME_TOO_DISTANT = 3
        BUDGET_TOO_SMALL = 4
        CAMPAIGN_DURATION_TOO_SHORT = 5
        CAMPAIGN_NOT_ENABLED = 6
        NOT_ENOUGH_AVAILABLE_INVENTORY = 7
        TARGETING_TOO_NARROW = 8
        UNSUPPORTED_AD_GROUP_TYPE = 9
        UNSUPPORTED_BID_MODIFIER = 10
        CANNOT_CHANGE_PRICING_MODEL = 11
        INCOMPATIBLE_TARGETING = 12
        UNSUPPORTED_FEATURE = 13
        MISSING_ELECTION_CERTIFICATE = 14
        CAMPAIGN_ENDED = 15
        UNSUPPORTED_BUDGET_PERIOD = 16
        EXACTLY_ONE_ENABLED_ADGROUP_REQUIRED = 17
        FREQUENCY_CAP_TOO_NARROW = 18
        TARGETED_PACK_NEEDS_DEAL = 19
        DEAL_CURRENCY_MISMATCH = 20
        CANNOT_HOLD_CONTRACT = 21
        CUSTOMER_NOT_ENABLED = 22
        CUSTOMER_NOT_ALLOWED = 23
        INVALID_ACCOUNT_TYPE = 24
        ACCOUNT_IS_MANAGER = 25
        SEASONAL_LINEUP_BOOKING_WINDOW_NOT_OPEN = 26
        SEASONAL_LINEUP_END_DATE_OFF_SEASON = 27
        SEASONAL_LINEUP_GEO_TARGETING_TOO_NARROW = 28
        NO_MARKET_RATE_CARD_OR_BASE_RATE = 29
        STALE_QUOTE = 30
        LINEUP_NOT_ALLOWED = 31
        UNSUPPORTED_BIDDING_STRATEGY = 32
        UNSUPPORTED_POSITIVE_GEO_TARGET_TYPE = 33
        VALIDATE_ONLY_REQUIRED = 34
        TOO_MANY_CAMPAIGNS = 35


__all__ = tuple(sorted(__protobuf__.manifest))
