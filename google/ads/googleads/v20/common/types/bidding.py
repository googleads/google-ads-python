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

from google.ads.googleads.v20.enums.types import fixed_cpm_goal
from google.ads.googleads.v20.enums.types import (
    fixed_cpm_target_frequency_time_unit,
)
from google.ads.googleads.v20.enums.types import target_frequency_time_unit
from google.ads.googleads.v20.enums.types import (
    target_impression_share_location,
)


__protobuf__ = proto.module(
    package="google.ads.googleads.v20.common",
    marshal="google.ads.googleads.v20",
    manifest={
        "Commission",
        "EnhancedCpc",
        "ManualCpa",
        "ManualCpc",
        "ManualCpm",
        "ManualCpv",
        "MaximizeConversions",
        "MaximizeConversionValue",
        "TargetCpa",
        "TargetCpm",
        "TargetCpmTargetFrequencyGoal",
        "TargetImpressionShare",
        "TargetRoas",
        "TargetSpend",
        "PercentCpc",
        "FixedCpm",
        "FixedCpmTargetFrequencyGoalInfo",
        "TargetCpv",
    },
)


class Commission(proto.Message):
    r"""Commission is an automatic bidding strategy in which the
    advertiser pays a certain portion of the conversion value.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        commission_rate_micros (int):
            Commission rate defines the portion of the conversion value
            that the advertiser will be billed. A commission rate of x
            should be passed into this field as (x \* 1,000,000). For
            example, 106,000 represents a commission rate of 0.106
            (10.6%).

            This field is a member of `oneof`_ ``_commission_rate_micros``.
    """

    commission_rate_micros: int = proto.Field(
        proto.INT64,
        number=2,
        optional=True,
    )


class EnhancedCpc(proto.Message):
    r"""An automated bidding strategy that raises bids for clicks that seem
    more likely to lead to a conversion and lowers them for clicks where
    they seem less likely.

    This bidding strategy is deprecated and cannot be created anymore.
    Use ManualCpc with enhanced_cpc_enabled set to true for equivalent
    functionality.

    """


class ManualCpa(proto.Message):
    r"""Manual bidding strategy that allows advertiser to set the bid
    per advertiser-specified action.

    """


class ManualCpc(proto.Message):
    r"""Manual click-based bidding where user pays per click.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        enhanced_cpc_enabled (bool):
            Whether bids are to be enhanced based on
            conversion optimizer data.

            This field is a member of `oneof`_ ``_enhanced_cpc_enabled``.
    """

    enhanced_cpc_enabled: bool = proto.Field(
        proto.BOOL,
        number=2,
        optional=True,
    )


class ManualCpm(proto.Message):
    r"""Manual impression-based bidding where user pays per thousand
    impressions.

    """


class ManualCpv(proto.Message):
    r"""View based bidding where user pays per video view."""


class MaximizeConversions(proto.Message):
    r"""An automated bidding strategy to help get the most
    conversions for your campaigns while spending your budget.

    Attributes:
        cpc_bid_ceiling_micros (int):
            Maximum bid limit that can be set by the bid
            strategy. The limit applies to all keywords
            managed by the strategy. Mutable for portfolio
            bidding strategies only.
        cpc_bid_floor_micros (int):
            Minimum bid limit that can be set by the bid
            strategy. The limit applies to all keywords
            managed by the strategy. Mutable for portfolio
            bidding strategies only.
        target_cpa_micros (int):
            The target cost-per-action (CPA) option. This
            is the average amount that you would like to
            spend per conversion action specified in micro
            units of the bidding strategy's currency. If
            set, the bid strategy will get as many
            conversions as possible at or below the target
            cost-per-action. If the target CPA is not set,
            the bid strategy will aim to achieve the lowest
            possible CPA given the budget.
    """

    cpc_bid_ceiling_micros: int = proto.Field(
        proto.INT64,
        number=2,
    )
    cpc_bid_floor_micros: int = proto.Field(
        proto.INT64,
        number=3,
    )
    target_cpa_micros: int = proto.Field(
        proto.INT64,
        number=4,
    )


class MaximizeConversionValue(proto.Message):
    r"""An automated bidding strategy to help get the most conversion
    value for your campaigns while spending your budget.

    Attributes:
        target_roas (float):
            The target return on ad spend (ROAS) option.
            If set, the bid strategy will maximize revenue
            while averaging the target return on ad spend.
            If the target ROAS is high, the bid strategy may
            not be able to spend the full budget. If the
            target ROAS is not set, the bid strategy will
            aim to achieve the highest possible ROAS for the
            budget.
        cpc_bid_ceiling_micros (int):
            Maximum bid limit that can be set by the bid
            strategy. The limit applies to all keywords
            managed by the strategy. Mutable for portfolio
            bidding strategies only.
        cpc_bid_floor_micros (int):
            Minimum bid limit that can be set by the bid
            strategy. The limit applies to all keywords
            managed by the strategy. Mutable for portfolio
            bidding strategies only.
    """

    target_roas: float = proto.Field(
        proto.DOUBLE,
        number=2,
    )
    cpc_bid_ceiling_micros: int = proto.Field(
        proto.INT64,
        number=3,
    )
    cpc_bid_floor_micros: int = proto.Field(
        proto.INT64,
        number=4,
    )


class TargetCpa(proto.Message):
    r"""An automated bid strategy that sets bids to help get as many
    conversions as possible at the target cost-per-acquisition (CPA)
    you set.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        target_cpa_micros (int):
            Average CPA target.
            This target should be greater than or equal to
            minimum billable unit based on the currency for
            the account.

            This field is a member of `oneof`_ ``_target_cpa_micros``.
        cpc_bid_ceiling_micros (int):
            Maximum bid limit that can be set by the bid
            strategy. The limit applies to all keywords
            managed by the strategy. This should only be set
            for portfolio bid strategies.

            This field is a member of `oneof`_ ``_cpc_bid_ceiling_micros``.
        cpc_bid_floor_micros (int):
            Minimum bid limit that can be set by the bid
            strategy. The limit applies to all keywords
            managed by the strategy. This should only be set
            for portfolio bid strategies.

            This field is a member of `oneof`_ ``_cpc_bid_floor_micros``.
    """

    target_cpa_micros: int = proto.Field(
        proto.INT64,
        number=4,
        optional=True,
    )
    cpc_bid_ceiling_micros: int = proto.Field(
        proto.INT64,
        number=5,
        optional=True,
    )
    cpc_bid_floor_micros: int = proto.Field(
        proto.INT64,
        number=6,
        optional=True,
    )


class TargetCpm(proto.Message):
    r"""Target CPM (cost per thousand impressions) is an automated
    bidding strategy that sets bids to optimize performance given
    the target CPM you set.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        target_frequency_goal (google.ads.googleads.v20.common.types.TargetCpmTargetFrequencyGoal):
            Target Frequency bidding goal details.

            This field is a member of `oneof`_ ``goal``.
    """

    target_frequency_goal: "TargetCpmTargetFrequencyGoal" = proto.Field(
        proto.MESSAGE,
        number=1,
        oneof="goal",
        message="TargetCpmTargetFrequencyGoal",
    )


class TargetCpmTargetFrequencyGoal(proto.Message):
    r"""Target Frequency bidding goal details.

    Attributes:
        target_count (int):
            Target Frequency count representing how many
            times you want to reach a single user.
        time_unit (google.ads.googleads.v20.enums.types.TargetFrequencyTimeUnitEnum.TargetFrequencyTimeUnit):
            Time window expressing the period over which you want to
            reach the specified target_count.
    """

    target_count: int = proto.Field(
        proto.INT64,
        number=1,
    )
    time_unit: (
        target_frequency_time_unit.TargetFrequencyTimeUnitEnum.TargetFrequencyTimeUnit
    ) = proto.Field(
        proto.ENUM,
        number=2,
        enum=target_frequency_time_unit.TargetFrequencyTimeUnitEnum.TargetFrequencyTimeUnit,
    )


class TargetImpressionShare(proto.Message):
    r"""An automated bidding strategy that sets bids so that a
    certain percentage of search ads are shown at the top of the
    first page (or other targeted location).


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        location (google.ads.googleads.v20.enums.types.TargetImpressionShareLocationEnum.TargetImpressionShareLocation):
            The targeted location on the search results
            page.
        location_fraction_micros (int):
            The chosen fraction of ads to be shown in the
            targeted location in micros. For example, 1%
            equals 10,000.

            This field is a member of `oneof`_ ``_location_fraction_micros``.
        cpc_bid_ceiling_micros (int):
            The highest CPC bid the automated bidding
            system is permitted to specify. This is a
            required field entered by the advertiser that
            sets the ceiling and specified in local micros.

            This field is a member of `oneof`_ ``_cpc_bid_ceiling_micros``.
    """

    location: (
        target_impression_share_location.TargetImpressionShareLocationEnum.TargetImpressionShareLocation
    ) = proto.Field(
        proto.ENUM,
        number=1,
        enum=target_impression_share_location.TargetImpressionShareLocationEnum.TargetImpressionShareLocation,
    )
    location_fraction_micros: int = proto.Field(
        proto.INT64,
        number=4,
        optional=True,
    )
    cpc_bid_ceiling_micros: int = proto.Field(
        proto.INT64,
        number=5,
        optional=True,
    )


class TargetRoas(proto.Message):
    r"""An automated bidding strategy that helps you maximize revenue
    while averaging a specific target return on ad spend (ROAS).


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        target_roas (float):
            Required. The chosen revenue (based on
            conversion data) per unit of spend. Value must
            be between 0.01 and 1000.0, inclusive.

            This field is a member of `oneof`_ ``_target_roas``.
        cpc_bid_ceiling_micros (int):
            Maximum bid limit that can be set by the bid
            strategy. The limit applies to all keywords
            managed by the strategy. This should only be set
            for portfolio bid strategies.

            This field is a member of `oneof`_ ``_cpc_bid_ceiling_micros``.
        cpc_bid_floor_micros (int):
            Minimum bid limit that can be set by the bid
            strategy. The limit applies to all keywords
            managed by the strategy. This should only be set
            for portfolio bid strategies.

            This field is a member of `oneof`_ ``_cpc_bid_floor_micros``.
    """

    target_roas: float = proto.Field(
        proto.DOUBLE,
        number=4,
        optional=True,
    )
    cpc_bid_ceiling_micros: int = proto.Field(
        proto.INT64,
        number=5,
        optional=True,
    )
    cpc_bid_floor_micros: int = proto.Field(
        proto.INT64,
        number=6,
        optional=True,
    )


class TargetSpend(proto.Message):
    r"""An automated bid strategy that sets your bids to help get as
    many clicks as possible within your budget.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        target_spend_micros (int):
            Deprecated: The spend target under which to
            maximize clicks. A TargetSpend bidder will
            attempt to spend the smaller of this value or
            the natural throttling spend amount.
            If not specified, the budget is used as the
            spend target. This field is deprecated and
            should no longer be used. See
            https://ads-developers.googleblog.com/2020/05/reminder-about-sunset-creation-of.html
            for details.

            This field is a member of `oneof`_ ``_target_spend_micros``.
        cpc_bid_ceiling_micros (int):
            Maximum bid limit that can be set by the bid
            strategy. The limit applies to all keywords
            managed by the strategy.

            This field is a member of `oneof`_ ``_cpc_bid_ceiling_micros``.
    """

    target_spend_micros: int = proto.Field(
        proto.INT64,
        number=3,
        optional=True,
    )
    cpc_bid_ceiling_micros: int = proto.Field(
        proto.INT64,
        number=4,
        optional=True,
    )


class PercentCpc(proto.Message):
    r"""A bidding strategy where bids are a fraction of the
    advertised price for some good or service.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        cpc_bid_ceiling_micros (int):
            Maximum bid limit that can be set by the bid strategy. This
            is an optional field entered by the advertiser and specified
            in local micros. Note: A zero value is interpreted in the
            same way as having bid_ceiling undefined.

            This field is a member of `oneof`_ ``_cpc_bid_ceiling_micros``.
        enhanced_cpc_enabled (bool):
            Adjusts the bid for each auction upward or downward,
            depending on the likelihood of a conversion. Individual bids
            may exceed cpc_bid_ceiling_micros, but the average bid
            amount for a campaign should not.

            This field is a member of `oneof`_ ``_enhanced_cpc_enabled``.
    """

    cpc_bid_ceiling_micros: int = proto.Field(
        proto.INT64,
        number=3,
        optional=True,
    )
    enhanced_cpc_enabled: bool = proto.Field(
        proto.BOOL,
        number=4,
        optional=True,
    )


class FixedCpm(proto.Message):
    r"""Fixed CPM (cost per thousand impression) bidding strategy. A
    manual bidding strategy with a fixed CPM.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        goal (google.ads.googleads.v20.enums.types.FixedCpmGoalEnum.FixedCpmGoal):
            Fixed CPM bidding goal. Determines the exact
            bidding optimization parameters.
        target_frequency_info (google.ads.googleads.v20.common.types.FixedCpmTargetFrequencyGoalInfo):
            Target frequency bidding goal details.

            This field is a member of `oneof`_ ``goal_info``.
    """

    goal: fixed_cpm_goal.FixedCpmGoalEnum.FixedCpmGoal = proto.Field(
        proto.ENUM,
        number=1,
        enum=fixed_cpm_goal.FixedCpmGoalEnum.FixedCpmGoal,
    )
    target_frequency_info: "FixedCpmTargetFrequencyGoalInfo" = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="goal_info",
        message="FixedCpmTargetFrequencyGoalInfo",
    )


class FixedCpmTargetFrequencyGoalInfo(proto.Message):
    r"""Target frequency bidding goal details for Fixed CPM bidding
    strategy. Only relevant if the goal of the bidding strategy is
    ``TARGET_FREQUENCY``.

    Attributes:
        target_count (int):
            Target frequency count represents the number
            of times an advertiser wants to show the ad to
            target a single user.
        time_unit (google.ads.googleads.v20.enums.types.FixedCpmTargetFrequencyTimeUnitEnum.FixedCpmTargetFrequencyTimeUnit):
            Time window expressing the period over which you want to
            reach the specified target_count.
    """

    target_count: int = proto.Field(
        proto.INT64,
        number=1,
    )
    time_unit: (
        fixed_cpm_target_frequency_time_unit.FixedCpmTargetFrequencyTimeUnitEnum.FixedCpmTargetFrequencyTimeUnit
    ) = proto.Field(
        proto.ENUM,
        number=2,
        enum=fixed_cpm_target_frequency_time_unit.FixedCpmTargetFrequencyTimeUnitEnum.FixedCpmTargetFrequencyTimeUnit,
    )


class TargetCpv(proto.Message):
    r"""Target CPV (cost per view) bidding strategy. An automated
    bidding strategy that sets bids to optimize performance given
    the target CPV you set.

    """


__all__ = tuple(sorted(__protobuf__.manifest))
