# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
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

from typing import MutableSequence

import proto  # type: ignore


__protobuf__ = proto.module(
    package="google.ads.googleads.v14.common",
    marshal="google.ads.googleads.v14",
    manifest={
        "CpcBidSimulationPointList",
        "CpvBidSimulationPointList",
        "TargetCpaSimulationPointList",
        "TargetRoasSimulationPointList",
        "PercentCpcBidSimulationPointList",
        "BudgetSimulationPointList",
        "TargetImpressionShareSimulationPointList",
        "CpcBidSimulationPoint",
        "CpvBidSimulationPoint",
        "TargetCpaSimulationPoint",
        "TargetRoasSimulationPoint",
        "PercentCpcBidSimulationPoint",
        "BudgetSimulationPoint",
        "TargetImpressionShareSimulationPoint",
    },
)


class CpcBidSimulationPointList(proto.Message):
    r"""A container for simulation points for simulations of type CPC_BID.
    Attributes:
        points (MutableSequence[google.ads.googleads.v14.common.types.CpcBidSimulationPoint]):
            Projected metrics for a series of CPC bid
            amounts.
    """

    points: MutableSequence["CpcBidSimulationPoint"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="CpcBidSimulationPoint",
    )


class CpvBidSimulationPointList(proto.Message):
    r"""A container for simulation points for simulations of type CPV_BID.
    Attributes:
        points (MutableSequence[google.ads.googleads.v14.common.types.CpvBidSimulationPoint]):
            Projected metrics for a series of CPV bid
            amounts.
    """

    points: MutableSequence["CpvBidSimulationPoint"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="CpvBidSimulationPoint",
    )


class TargetCpaSimulationPointList(proto.Message):
    r"""A container for simulation points for simulations of type
    TARGET_CPA.

    Attributes:
        points (MutableSequence[google.ads.googleads.v14.common.types.TargetCpaSimulationPoint]):
            Projected metrics for a series of target CPA
            amounts.
    """

    points: MutableSequence["TargetCpaSimulationPoint"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="TargetCpaSimulationPoint",
    )


class TargetRoasSimulationPointList(proto.Message):
    r"""A container for simulation points for simulations of type
    TARGET_ROAS.

    Attributes:
        points (MutableSequence[google.ads.googleads.v14.common.types.TargetRoasSimulationPoint]):
            Projected metrics for a series of target ROAS
            amounts.
    """

    points: MutableSequence["TargetRoasSimulationPoint"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="TargetRoasSimulationPoint",
    )


class PercentCpcBidSimulationPointList(proto.Message):
    r"""A container for simulation points for simulations of type
    PERCENT_CPC_BID.

    Attributes:
        points (MutableSequence[google.ads.googleads.v14.common.types.PercentCpcBidSimulationPoint]):
            Projected metrics for a series of percent CPC
            bid amounts.
    """

    points: MutableSequence[
        "PercentCpcBidSimulationPoint"
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="PercentCpcBidSimulationPoint",
    )


class BudgetSimulationPointList(proto.Message):
    r"""A container for simulation points for simulations of type
    BUDGET.

    Attributes:
        points (MutableSequence[google.ads.googleads.v14.common.types.BudgetSimulationPoint]):
            Projected metrics for a series of budget
            amounts.
    """

    points: MutableSequence["BudgetSimulationPoint"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="BudgetSimulationPoint",
    )


class TargetImpressionShareSimulationPointList(proto.Message):
    r"""A container for simulation points for simulations of type
    TARGET_IMPRESSION_SHARE.

    Attributes:
        points (MutableSequence[google.ads.googleads.v14.common.types.TargetImpressionShareSimulationPoint]):
            Projected metrics for a specific target
            impression share value.
    """

    points: MutableSequence[
        "TargetImpressionShareSimulationPoint"
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="TargetImpressionShareSimulationPoint",
    )


class CpcBidSimulationPoint(proto.Message):
    r"""Projected metrics for a specific CPC bid amount.
    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        required_budget_amount_micros (int):
            Projected required daily budget that the
            advertiser must set in order to receive the
            estimated traffic, in micros of advertiser
            currency.
        biddable_conversions (float):
            Projected number of biddable conversions.

            This field is a member of `oneof`_ ``_biddable_conversions``.
        biddable_conversions_value (float):
            Projected total value of biddable
            conversions.

            This field is a member of `oneof`_ ``_biddable_conversions_value``.
        clicks (int):
            Projected number of clicks.

            This field is a member of `oneof`_ ``_clicks``.
        cost_micros (int):
            Projected cost in micros.

            This field is a member of `oneof`_ ``_cost_micros``.
        impressions (int):
            Projected number of impressions.

            This field is a member of `oneof`_ ``_impressions``.
        top_slot_impressions (int):
            Projected number of top slot impressions.
            Only search advertising channel type supports
            this field.

            This field is a member of `oneof`_ ``_top_slot_impressions``.
        cpc_bid_micros (int):
            The simulated CPC bid upon which projected
            metrics are based.

            This field is a member of `oneof`_ ``cpc_simulation_key_value``.
        cpc_bid_scaling_modifier (float):
            The simulated scaling modifier upon which
            projected metrics are based. All CPC bids
            relevant to the simulated entity are scaled by
            this modifier.

            This field is a member of `oneof`_ ``cpc_simulation_key_value``.
    """

    required_budget_amount_micros: int = proto.Field(
        proto.INT64,
        number=17,
    )
    biddable_conversions: float = proto.Field(
        proto.DOUBLE,
        number=9,
        optional=True,
    )
    biddable_conversions_value: float = proto.Field(
        proto.DOUBLE,
        number=10,
        optional=True,
    )
    clicks: int = proto.Field(
        proto.INT64,
        number=11,
        optional=True,
    )
    cost_micros: int = proto.Field(
        proto.INT64,
        number=12,
        optional=True,
    )
    impressions: int = proto.Field(
        proto.INT64,
        number=13,
        optional=True,
    )
    top_slot_impressions: int = proto.Field(
        proto.INT64,
        number=14,
        optional=True,
    )
    cpc_bid_micros: int = proto.Field(
        proto.INT64,
        number=15,
        oneof="cpc_simulation_key_value",
    )
    cpc_bid_scaling_modifier: float = proto.Field(
        proto.DOUBLE,
        number=16,
        oneof="cpc_simulation_key_value",
    )


class CpvBidSimulationPoint(proto.Message):
    r"""Projected metrics for a specific CPV bid amount.
    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        cpv_bid_micros (int):
            The simulated CPV bid upon which projected
            metrics are based.

            This field is a member of `oneof`_ ``_cpv_bid_micros``.
        cost_micros (int):
            Projected cost in micros.

            This field is a member of `oneof`_ ``_cost_micros``.
        impressions (int):
            Projected number of impressions.

            This field is a member of `oneof`_ ``_impressions``.
        views (int):
            Projected number of views.

            This field is a member of `oneof`_ ``_views``.
    """

    cpv_bid_micros: int = proto.Field(
        proto.INT64,
        number=5,
        optional=True,
    )
    cost_micros: int = proto.Field(
        proto.INT64,
        number=6,
        optional=True,
    )
    impressions: int = proto.Field(
        proto.INT64,
        number=7,
        optional=True,
    )
    views: int = proto.Field(
        proto.INT64,
        number=8,
        optional=True,
    )


class TargetCpaSimulationPoint(proto.Message):
    r"""Projected metrics for a specific target CPA amount.
    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        required_budget_amount_micros (int):
            Projected required daily budget that the
            advertiser must set in order to receive the
            estimated traffic, in micros of advertiser
            currency.
        biddable_conversions (float):
            Projected number of biddable conversions.

            This field is a member of `oneof`_ ``_biddable_conversions``.
        biddable_conversions_value (float):
            Projected total value of biddable
            conversions.

            This field is a member of `oneof`_ ``_biddable_conversions_value``.
        app_installs (float):
            Projected number of app installs.
        in_app_actions (float):
            Projected number of in-app actions.
        clicks (int):
            Projected number of clicks.

            This field is a member of `oneof`_ ``_clicks``.
        cost_micros (int):
            Projected cost in micros.

            This field is a member of `oneof`_ ``_cost_micros``.
        impressions (int):
            Projected number of impressions.

            This field is a member of `oneof`_ ``_impressions``.
        top_slot_impressions (int):
            Projected number of top slot impressions.
            Only search advertising channel type supports
            this field.

            This field is a member of `oneof`_ ``_top_slot_impressions``.
        target_cpa_micros (int):
            The simulated target CPA upon which projected
            metrics are based.

            This field is a member of `oneof`_ ``target_cpa_simulation_key_value``.
        target_cpa_scaling_modifier (float):
            The simulated scaling modifier upon which
            projected metrics are based. All CPA targets
            relevant to the simulated entity are scaled by
            this modifier.

            This field is a member of `oneof`_ ``target_cpa_simulation_key_value``.
    """

    required_budget_amount_micros: int = proto.Field(
        proto.INT64,
        number=19,
    )
    biddable_conversions: float = proto.Field(
        proto.DOUBLE,
        number=9,
        optional=True,
    )
    biddable_conversions_value: float = proto.Field(
        proto.DOUBLE,
        number=10,
        optional=True,
    )
    app_installs: float = proto.Field(
        proto.DOUBLE,
        number=15,
    )
    in_app_actions: float = proto.Field(
        proto.DOUBLE,
        number=16,
    )
    clicks: int = proto.Field(
        proto.INT64,
        number=11,
        optional=True,
    )
    cost_micros: int = proto.Field(
        proto.INT64,
        number=12,
        optional=True,
    )
    impressions: int = proto.Field(
        proto.INT64,
        number=13,
        optional=True,
    )
    top_slot_impressions: int = proto.Field(
        proto.INT64,
        number=14,
        optional=True,
    )
    target_cpa_micros: int = proto.Field(
        proto.INT64,
        number=17,
        oneof="target_cpa_simulation_key_value",
    )
    target_cpa_scaling_modifier: float = proto.Field(
        proto.DOUBLE,
        number=18,
        oneof="target_cpa_simulation_key_value",
    )


class TargetRoasSimulationPoint(proto.Message):
    r"""Projected metrics for a specific target ROAS amount.
    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        target_roas (float):
            The simulated target ROAS upon which
            projected metrics are based.

            This field is a member of `oneof`_ ``_target_roas``.
        required_budget_amount_micros (int):
            Projected required daily budget that the
            advertiser must set in order to receive the
            estimated traffic, in micros of advertiser
            currency.
        biddable_conversions (float):
            Projected number of biddable conversions.

            This field is a member of `oneof`_ ``_biddable_conversions``.
        biddable_conversions_value (float):
            Projected total value of biddable
            conversions.

            This field is a member of `oneof`_ ``_biddable_conversions_value``.
        clicks (int):
            Projected number of clicks.

            This field is a member of `oneof`_ ``_clicks``.
        cost_micros (int):
            Projected cost in micros.

            This field is a member of `oneof`_ ``_cost_micros``.
        impressions (int):
            Projected number of impressions.

            This field is a member of `oneof`_ ``_impressions``.
        top_slot_impressions (int):
            Projected number of top slot impressions.
            Only Search advertising channel type supports
            this field.

            This field is a member of `oneof`_ ``_top_slot_impressions``.
    """

    target_roas: float = proto.Field(
        proto.DOUBLE,
        number=8,
        optional=True,
    )
    required_budget_amount_micros: int = proto.Field(
        proto.INT64,
        number=15,
    )
    biddable_conversions: float = proto.Field(
        proto.DOUBLE,
        number=9,
        optional=True,
    )
    biddable_conversions_value: float = proto.Field(
        proto.DOUBLE,
        number=10,
        optional=True,
    )
    clicks: int = proto.Field(
        proto.INT64,
        number=11,
        optional=True,
    )
    cost_micros: int = proto.Field(
        proto.INT64,
        number=12,
        optional=True,
    )
    impressions: int = proto.Field(
        proto.INT64,
        number=13,
        optional=True,
    )
    top_slot_impressions: int = proto.Field(
        proto.INT64,
        number=14,
        optional=True,
    )


class PercentCpcBidSimulationPoint(proto.Message):
    r"""Projected metrics for a specific percent CPC amount. Only
    Hotel advertising channel type supports this field.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        percent_cpc_bid_micros (int):
            The simulated percent CPC upon which projected metrics are
            based. Percent CPC expressed as fraction of the advertised
            price for some good or service. The value stored here is
            1,000,000 \* [fraction].

            This field is a member of `oneof`_ ``_percent_cpc_bid_micros``.
        biddable_conversions (float):
            Projected number of biddable conversions.

            This field is a member of `oneof`_ ``_biddable_conversions``.
        biddable_conversions_value (float):
            Projected total value of biddable conversions
            in local currency.

            This field is a member of `oneof`_ ``_biddable_conversions_value``.
        clicks (int):
            Projected number of clicks.

            This field is a member of `oneof`_ ``_clicks``.
        cost_micros (int):
            Projected cost in micros.

            This field is a member of `oneof`_ ``_cost_micros``.
        impressions (int):
            Projected number of impressions.

            This field is a member of `oneof`_ ``_impressions``.
        top_slot_impressions (int):
            Projected number of top slot impressions.

            This field is a member of `oneof`_ ``_top_slot_impressions``.
    """

    percent_cpc_bid_micros: int = proto.Field(
        proto.INT64,
        number=1,
        optional=True,
    )
    biddable_conversions: float = proto.Field(
        proto.DOUBLE,
        number=2,
        optional=True,
    )
    biddable_conversions_value: float = proto.Field(
        proto.DOUBLE,
        number=3,
        optional=True,
    )
    clicks: int = proto.Field(
        proto.INT64,
        number=4,
        optional=True,
    )
    cost_micros: int = proto.Field(
        proto.INT64,
        number=5,
        optional=True,
    )
    impressions: int = proto.Field(
        proto.INT64,
        number=6,
        optional=True,
    )
    top_slot_impressions: int = proto.Field(
        proto.INT64,
        number=7,
        optional=True,
    )


class BudgetSimulationPoint(proto.Message):
    r"""Projected metrics for a specific budget amount.
    Attributes:
        budget_amount_micros (int):
            The simulated budget upon which projected
            metrics are based.
        required_cpc_bid_ceiling_micros (int):
            Projected required daily cpc bid ceiling that
            the advertiser must set to realize this
            simulation, in micros of the advertiser
            currency. Only campaigns with the Target Spend
            bidding strategy support this field.
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

    budget_amount_micros: int = proto.Field(
        proto.INT64,
        number=1,
    )
    required_cpc_bid_ceiling_micros: int = proto.Field(
        proto.INT64,
        number=2,
    )
    biddable_conversions: float = proto.Field(
        proto.DOUBLE,
        number=3,
    )
    biddable_conversions_value: float = proto.Field(
        proto.DOUBLE,
        number=4,
    )
    clicks: int = proto.Field(
        proto.INT64,
        number=5,
    )
    cost_micros: int = proto.Field(
        proto.INT64,
        number=6,
    )
    impressions: int = proto.Field(
        proto.INT64,
        number=7,
    )
    top_slot_impressions: int = proto.Field(
        proto.INT64,
        number=8,
    )


class TargetImpressionShareSimulationPoint(proto.Message):
    r"""Projected metrics for a specific target impression share
    value.

    Attributes:
        target_impression_share_micros (int):
            The simulated target impression share value (in micros) upon
            which projected metrics are based. For example, 10%
            impression share, which is equal to 0.1, is stored as
            100_000. This value is validated and will not exceed 1M
            (100%).
        required_cpc_bid_ceiling_micros (int):
            Projected required daily cpc bid ceiling that
            the advertiser must set to realize this
            simulation, in micros of the advertiser
            currency.
        required_budget_amount_micros (int):
            Projected required daily budget that the
            advertiser must set in order to receive the
            estimated traffic, in micros of advertiser
            currency.
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
        absolute_top_impressions (int):
            Projected number of absolute top impressions.
            Only search advertising channel type supports
            this field.
    """

    target_impression_share_micros: int = proto.Field(
        proto.INT64,
        number=1,
    )
    required_cpc_bid_ceiling_micros: int = proto.Field(
        proto.INT64,
        number=2,
    )
    required_budget_amount_micros: int = proto.Field(
        proto.INT64,
        number=3,
    )
    biddable_conversions: float = proto.Field(
        proto.DOUBLE,
        number=4,
    )
    biddable_conversions_value: float = proto.Field(
        proto.DOUBLE,
        number=5,
    )
    clicks: int = proto.Field(
        proto.INT64,
        number=6,
    )
    cost_micros: int = proto.Field(
        proto.INT64,
        number=7,
    )
    impressions: int = proto.Field(
        proto.INT64,
        number=8,
    )
    top_slot_impressions: int = proto.Field(
        proto.INT64,
        number=9,
    )
    absolute_top_impressions: int = proto.Field(
        proto.INT64,
        number=10,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
