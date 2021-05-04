# -*- coding: utf-8 -*-
# Copyright 2020 Google LLC
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
import proto  # type: ignore

from google.ads.googleads.v7.enums.types import target_impression_share_location


__protobuf__ = proto.module(
    package="google.ads.googleads.v7.common",
    marshal="google.ads.googleads.v7",
    manifest={
        "Commission",
        "EnhancedCpc",
        "ManualCpc",
        "ManualCpm",
        "ManualCpv",
        "MaximizeConversions",
        "MaximizeConversionValue",
        "TargetCpa",
        "TargetCpm",
        "TargetImpressionShare",
        "TargetRoas",
        "TargetSpend",
        "PercentCpc",
    },
)


class Commission(proto.Message):
    r"""Commission is an automatic bidding strategy in which the
    advertiser pays a certain portion of the conversion value.

    Attributes:
        commission_rate_micros (int):
            Commission rate defines the portion of the conversion value
            that the advertiser will be billed. A commission rate of x
            should be passed into this field as (x \* 1,000,000). For
            example, 106,000 represents a commission rate of 0.106
            (10.6%).
    """

    commission_rate_micros = proto.Field(proto.INT64, number=2, optional=True,)


class EnhancedCpc(proto.Message):
    r"""An automated bidding strategy that raises bids for clicks
    that seem more likely to lead to a conversion and lowers them
    for clicks where they seem less likely.
        """


class ManualCpc(proto.Message):
    r"""Manual click-based bidding where user pays per click.
    Attributes:
        enhanced_cpc_enabled (bool):
            Whether bids are to be enhanced based on
            conversion optimizer data.
    """

    enhanced_cpc_enabled = proto.Field(proto.BOOL, number=2, optional=True,)


class ManualCpm(proto.Message):
    r"""Manual impression-based bidding where user pays per thousand
    impressions.
        """


class ManualCpv(proto.Message):
    r"""View based bidding where user pays per video view.    """


class MaximizeConversions(proto.Message):
    r"""An automated bidding strategy to help get the most
    conversions for your campaigns while spending your budget.

    Attributes:
        target_cpa (int):
            The target cost per acquisition (CPA) option.
            This is the average amount that you would like
            to spend per acquisition.
            This field is read-only.
    """

    target_cpa = proto.Field(proto.INT64, number=1,)


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
    """

    target_roas = proto.Field(proto.DOUBLE, number=2, optional=True,)


class TargetCpa(proto.Message):
    r"""An automated bid strategy that sets bids to help get as many
    conversions as possible at the target cost-per-acquisition (CPA)
    you set.

    Attributes:
        target_cpa_micros (int):
            Average CPA target.
            This target should be greater than or equal to
            minimum billable unit based on the currency for
            the account.
        cpc_bid_ceiling_micros (int):
            Maximum bid limit that can be set by the bid
            strategy. The limit applies to all keywords
            managed by the strategy.
        cpc_bid_floor_micros (int):
            Minimum bid limit that can be set by the bid
            strategy. The limit applies to all keywords
            managed by the strategy.
    """

    target_cpa_micros = proto.Field(proto.INT64, number=4, optional=True,)
    cpc_bid_ceiling_micros = proto.Field(proto.INT64, number=5, optional=True,)
    cpc_bid_floor_micros = proto.Field(proto.INT64, number=6, optional=True,)


class TargetCpm(proto.Message):
    r"""Target CPM (cost per thousand impressions) is an automated
    bidding strategy that sets bids to optimize performance given
    the target CPM you set.
        """


class TargetImpressionShare(proto.Message):
    r"""An automated bidding strategy that sets bids so that a
    certain percentage of search ads are shown at the top of the
    first page (or other targeted location).

    Attributes:
        location (google.ads.googleads.v7.enums.types.TargetImpressionShareLocationEnum.TargetImpressionShareLocation):
            The targeted location on the search results
            page.
        location_fraction_micros (int):
            The desired fraction of ads to be shown in
            the targeted location in micros. E.g. 1% equals
            10,000.
        cpc_bid_ceiling_micros (int):
            The highest CPC bid the automated bidding
            system is permitted to specify. This is a
            required field entered by the advertiser that
            sets the ceiling and specified in local micros.
    """

    location = proto.Field(
        proto.ENUM,
        number=1,
        enum=target_impression_share_location.TargetImpressionShareLocationEnum.TargetImpressionShareLocation,
    )
    location_fraction_micros = proto.Field(
        proto.INT64, number=4, optional=True,
    )
    cpc_bid_ceiling_micros = proto.Field(proto.INT64, number=5, optional=True,)


class TargetRoas(proto.Message):
    r"""An automated bidding strategy that helps you maximize revenue
    while averaging a specific target return on ad spend (ROAS).

    Attributes:
        target_roas (float):
            Required. The desired revenue (based on
            conversion data) per unit of spend. Value must
            be between 0.01 and 1000.0, inclusive.
        cpc_bid_ceiling_micros (int):
            Maximum bid limit that can be set by the bid
            strategy. The limit applies to all keywords
            managed by the strategy.
        cpc_bid_floor_micros (int):
            Minimum bid limit that can be set by the bid
            strategy. The limit applies to all keywords
            managed by the strategy.
    """

    target_roas = proto.Field(proto.DOUBLE, number=4, optional=True,)
    cpc_bid_ceiling_micros = proto.Field(proto.INT64, number=5, optional=True,)
    cpc_bid_floor_micros = proto.Field(proto.INT64, number=6, optional=True,)


class TargetSpend(proto.Message):
    r"""An automated bid strategy that sets your bids to help get as
    many clicks as possible within your budget.

    Attributes:
        target_spend_micros (int):
            The spend target under which to maximize
            clicks. A TargetSpend bidder will attempt to
            spend the smaller of this value or the natural
            throttling spend amount.
            If not specified, the budget is used as the
            spend target. This field is deprecated and
            should no longer be used. See https://ads-
            developers.googleblog.com/2020/05/reminder-
            about-sunset-creation-of.html for details.
        cpc_bid_ceiling_micros (int):
            Maximum bid limit that can be set by the bid
            strategy. The limit applies to all keywords
            managed by the strategy.
    """

    target_spend_micros = proto.Field(proto.INT64, number=3, optional=True,)
    cpc_bid_ceiling_micros = proto.Field(proto.INT64, number=4, optional=True,)


class PercentCpc(proto.Message):
    r"""A bidding strategy where bids are a fraction of the
    advertised price for some good or service.

    Attributes:
        cpc_bid_ceiling_micros (int):
            Maximum bid limit that can be set by the bid strategy. This
            is an optional field entered by the advertiser and specified
            in local micros. Note: A zero value is interpreted in the
            same way as having bid_ceiling undefined.
        enhanced_cpc_enabled (bool):
            Adjusts the bid for each auction upward or downward,
            depending on the likelihood of a conversion. Individual bids
            may exceed cpc_bid_ceiling_micros, but the average bid
            amount for a campaign should not.
    """

    cpc_bid_ceiling_micros = proto.Field(proto.INT64, number=3, optional=True,)
    enhanced_cpc_enabled = proto.Field(proto.BOOL, number=4, optional=True,)


__all__ = tuple(sorted(__protobuf__.manifest))
