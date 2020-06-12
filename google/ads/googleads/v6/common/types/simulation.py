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


__protobuf__ = proto.module(
    package="google.ads.googleads.v6.common",
    marshal="google.ads.googleads.v6",
    manifest={
        "BidModifierSimulationPointList",
        "CpcBidSimulationPointList",
        "CpvBidSimulationPointList",
        "TargetCpaSimulationPointList",
        "TargetRoasSimulationPointList",
        "PercentCpcBidSimulationPointList",
        "BidModifierSimulationPoint",
        "CpcBidSimulationPoint",
        "CpvBidSimulationPoint",
        "TargetCpaSimulationPoint",
        "TargetRoasSimulationPoint",
        "PercentCpcBidSimulationPoint",
    },
)


class BidModifierSimulationPointList(proto.Message):
    r"""A container for simulation points for simulations of type
    BID_MODIFIER.

    Attributes:
        points (Sequence[google.ads.googleads.v6.common.types.BidModifierSimulationPoint]):
            Projected metrics for a series of bid
            modifier amounts.
    """

    points = proto.RepeatedField(
        proto.MESSAGE, number=1, message="BidModifierSimulationPoint",
    )


class CpcBidSimulationPointList(proto.Message):
    r"""A container for simulation points for simulations of type CPC_BID.

    Attributes:
        points (Sequence[google.ads.googleads.v6.common.types.CpcBidSimulationPoint]):
            Projected metrics for a series of CPC bid
            amounts.
    """

    points = proto.RepeatedField(
        proto.MESSAGE, number=1, message="CpcBidSimulationPoint",
    )


class CpvBidSimulationPointList(proto.Message):
    r"""A container for simulation points for simulations of type CPV_BID.

    Attributes:
        points (Sequence[google.ads.googleads.v6.common.types.CpvBidSimulationPoint]):
            Projected metrics for a series of CPV bid
            amounts.
    """

    points = proto.RepeatedField(
        proto.MESSAGE, number=1, message="CpvBidSimulationPoint",
    )


class TargetCpaSimulationPointList(proto.Message):
    r"""A container for simulation points for simulations of type
    TARGET_CPA.

    Attributes:
        points (Sequence[google.ads.googleads.v6.common.types.TargetCpaSimulationPoint]):
            Projected metrics for a series of target CPA
            amounts.
    """

    points = proto.RepeatedField(
        proto.MESSAGE, number=1, message="TargetCpaSimulationPoint",
    )


class TargetRoasSimulationPointList(proto.Message):
    r"""A container for simulation points for simulations of type
    TARGET_ROAS.

    Attributes:
        points (Sequence[google.ads.googleads.v6.common.types.TargetRoasSimulationPoint]):
            Projected metrics for a series of target ROAS
            amounts.
    """

    points = proto.RepeatedField(
        proto.MESSAGE, number=1, message="TargetRoasSimulationPoint",
    )


class PercentCpcBidSimulationPointList(proto.Message):
    r"""A container for simulation points for simulations of type
    PERCENT_CPC_BID.

    Attributes:
        points (Sequence[google.ads.googleads.v6.common.types.PercentCpcBidSimulationPoint]):
            Projected metrics for a series of percent CPC
            bid amounts.
    """

    points = proto.RepeatedField(
        proto.MESSAGE, number=1, message="PercentCpcBidSimulationPoint",
    )


class BidModifierSimulationPoint(proto.Message):
    r"""Projected metrics for a specific bid modifier amount.

    Attributes:
        bid_modifier (float):
            The simulated bid modifier upon which
            projected metrics are based.
        biddable_conversions (float):
            Projected number of biddable conversions.
            Only search advertising channel type supports
            this field.
        biddable_conversions_value (float):
            Projected total value of biddable
            conversions. Only search advertising channel
            type supports this field.
        clicks (int):
            Projected number of clicks.
        cost_micros (int):
            Projected cost in micros.
        impressions (int):
            Projected number of impressions.
        top_slot_impressions (int):
            Projected number of top slot impressions.
            Only search advertising channel type supports
            this field.
        parent_biddable_conversions (float):
            Projected number of biddable conversions for
            the parent resource. Only search advertising
            channel type supports this field.
        parent_biddable_conversions_value (float):
            Projected total value of biddable conversions
            for the parent resource. Only search advertising
            channel type supports this field.
        parent_clicks (int):
            Projected number of clicks for the parent
            resource.
        parent_cost_micros (int):
            Projected cost in micros for the parent
            resource.
        parent_impressions (int):
            Projected number of impressions for the
            parent resource.
        parent_top_slot_impressions (int):
            Projected number of top slot impressions for
            the parent resource. Only search advertising
            channel type supports this field.
        parent_required_budget_micros (int):
            Projected minimum daily budget that must be
            available to the parent resource to realize this
            simulation.
    """

    bid_modifier = proto.Field(proto.DOUBLE, number=15, optional=True)
    biddable_conversions = proto.Field(proto.DOUBLE, number=16, optional=True)
    biddable_conversions_value = proto.Field(
        proto.DOUBLE, number=17, optional=True
    )
    clicks = proto.Field(proto.INT64, number=18, optional=True)
    cost_micros = proto.Field(proto.INT64, number=19, optional=True)
    impressions = proto.Field(proto.INT64, number=20, optional=True)
    top_slot_impressions = proto.Field(proto.INT64, number=21, optional=True)
    parent_biddable_conversions = proto.Field(
        proto.DOUBLE, number=22, optional=True
    )
    parent_biddable_conversions_value = proto.Field(
        proto.DOUBLE, number=23, optional=True
    )
    parent_clicks = proto.Field(proto.INT64, number=24, optional=True)
    parent_cost_micros = proto.Field(proto.INT64, number=25, optional=True)
    parent_impressions = proto.Field(proto.INT64, number=26, optional=True)
    parent_top_slot_impressions = proto.Field(
        proto.INT64, number=27, optional=True
    )
    parent_required_budget_micros = proto.Field(
        proto.INT64, number=28, optional=True
    )


class CpcBidSimulationPoint(proto.Message):
    r"""Projected metrics for a specific CPC bid amount.

    Attributes:
        cpc_bid_micros (int):
            The simulated CPC bid upon which projected
            metrics are based.
        biddable_conversions (float):
            Projected number of biddable conversions.
        biddable_conversions_value (float):
            Projected total value of biddable
            conversions.
        clicks (int):
            Projected number of clicks.
        cost_micros (int):
            Projected cost in micros.
        impressions (int):
            Projected number of impressions.
        top_slot_impressions (int):
            Projected number of top slot impressions.
            Only search advertising channel type supports
            this field.
    """

    cpc_bid_micros = proto.Field(proto.INT64, number=8, optional=True)
    biddable_conversions = proto.Field(proto.DOUBLE, number=9, optional=True)
    biddable_conversions_value = proto.Field(
        proto.DOUBLE, number=10, optional=True
    )
    clicks = proto.Field(proto.INT64, number=11, optional=True)
    cost_micros = proto.Field(proto.INT64, number=12, optional=True)
    impressions = proto.Field(proto.INT64, number=13, optional=True)
    top_slot_impressions = proto.Field(proto.INT64, number=14, optional=True)


class CpvBidSimulationPoint(proto.Message):
    r"""Projected metrics for a specific CPV bid amount.

    Attributes:
        cpv_bid_micros (int):
            The simulated CPV bid upon which projected
            metrics are based.
        cost_micros (int):
            Projected cost in micros.
        impressions (int):
            Projected number of impressions.
        views (int):
            Projected number of views.
    """

    cpv_bid_micros = proto.Field(proto.INT64, number=5, optional=True)
    cost_micros = proto.Field(proto.INT64, number=6, optional=True)
    impressions = proto.Field(proto.INT64, number=7, optional=True)
    views = proto.Field(proto.INT64, number=8, optional=True)


class TargetCpaSimulationPoint(proto.Message):
    r"""Projected metrics for a specific target CPA amount.

    Attributes:
        target_cpa_micros (int):
            The simulated target CPA upon which projected
            metrics are based.
        biddable_conversions (float):
            Projected number of biddable conversions.
        biddable_conversions_value (float):
            Projected total value of biddable
            conversions.
        clicks (int):
            Projected number of clicks.
        cost_micros (int):
            Projected cost in micros.
        impressions (int):
            Projected number of impressions.
        top_slot_impressions (int):
            Projected number of top slot impressions.
            Only search advertising channel type supports
            this field.
    """

    target_cpa_micros = proto.Field(proto.INT64, number=8, optional=True)
    biddable_conversions = proto.Field(proto.DOUBLE, number=9, optional=True)
    biddable_conversions_value = proto.Field(
        proto.DOUBLE, number=10, optional=True
    )
    clicks = proto.Field(proto.INT64, number=11, optional=True)
    cost_micros = proto.Field(proto.INT64, number=12, optional=True)
    impressions = proto.Field(proto.INT64, number=13, optional=True)
    top_slot_impressions = proto.Field(proto.INT64, number=14, optional=True)


class TargetRoasSimulationPoint(proto.Message):
    r"""Projected metrics for a specific target ROAS amount.

    Attributes:
        target_roas (float):
            The simulated target ROAS upon which
            projected metrics are based.
        biddable_conversions (float):
            Projected number of biddable conversions.
        biddable_conversions_value (float):
            Projected total value of biddable
            conversions.
        clicks (int):
            Projected number of clicks.
        cost_micros (int):
            Projected cost in micros.
        impressions (int):
            Projected number of impressions.
        top_slot_impressions (int):
            Projected number of top slot impressions.
            Only Search advertising channel type supports
            this field.
    """

    target_roas = proto.Field(proto.DOUBLE, number=8, optional=True)
    biddable_conversions = proto.Field(proto.DOUBLE, number=9, optional=True)
    biddable_conversions_value = proto.Field(
        proto.DOUBLE, number=10, optional=True
    )
    clicks = proto.Field(proto.INT64, number=11, optional=True)
    cost_micros = proto.Field(proto.INT64, number=12, optional=True)
    impressions = proto.Field(proto.INT64, number=13, optional=True)
    top_slot_impressions = proto.Field(proto.INT64, number=14, optional=True)


class PercentCpcBidSimulationPoint(proto.Message):
    r"""Projected metrics for a specific percent CPC amount. Only
    Hotel advertising channel type supports this field.

    Attributes:
        percent_cpc_bid_micros (int):
            The simulated percent CPC upon which projected metrics are
            based. Percent CPC expressed as fraction of the advertised
            price for some good or service. The value stored here is
            1,000,000 \* [fraction].
        biddable_conversions (float):
            Projected number of biddable conversions.
        biddable_conversions_value (float):
            Projected total value of biddable conversions
            in local currency.
        clicks (int):
            Projected number of clicks.
        cost_micros (int):
            Projected cost in micros.
        impressions (int):
            Projected number of impressions.
        top_slot_impressions (int):
            Projected number of top slot impressions.
    """

    percent_cpc_bid_micros = proto.Field(proto.INT64, number=1, optional=True)
    biddable_conversions = proto.Field(proto.DOUBLE, number=2, optional=True)
    biddable_conversions_value = proto.Field(
        proto.DOUBLE, number=3, optional=True
    )
    clicks = proto.Field(proto.INT64, number=4, optional=True)
    cost_micros = proto.Field(proto.INT64, number=5, optional=True)
    impressions = proto.Field(proto.INT64, number=6, optional=True)
    top_slot_impressions = proto.Field(proto.INT64, number=7, optional=True)


__all__ = tuple(sorted(__protobuf__.manifest))
