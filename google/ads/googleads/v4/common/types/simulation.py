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


from google.protobuf import wrappers_pb2 as wrappers  # type: ignore


__protobuf__ = proto.module(
    package="google.ads.googleads.v4.common",
    marshal="google.ads.googleads.v4",
    manifest={
        "BidModifierSimulationPointList",
        "CpcBidSimulationPointList",
        "CpvBidSimulationPointList",
        "TargetCpaSimulationPointList",
        "TargetRoasSimulationPointList",
        "BidModifierSimulationPoint",
        "CpcBidSimulationPoint",
        "CpvBidSimulationPoint",
        "TargetCpaSimulationPoint",
        "TargetRoasSimulationPoint",
    },
)


class BidModifierSimulationPointList(proto.Message):
    r"""A container for simulation points for simulations of type
    BID_MODIFIER.

    Attributes:
        points (Sequence[google.ads.googleads.v4.common.types.BidModifierSimulationPoint]):
            Projected metrics for a series of bid
            modifier amounts.
    """

    points = proto.RepeatedField(
        proto.MESSAGE, number=1, message="BidModifierSimulationPoint",
    )


class CpcBidSimulationPointList(proto.Message):
    r"""A container for simulation points for simulations of type CPC_BID.

    Attributes:
        points (Sequence[google.ads.googleads.v4.common.types.CpcBidSimulationPoint]):
            Projected metrics for a series of CPC bid
            amounts.
    """

    points = proto.RepeatedField(
        proto.MESSAGE, number=1, message="CpcBidSimulationPoint",
    )


class CpvBidSimulationPointList(proto.Message):
    r"""A container for simulation points for simulations of type CPV_BID.

    Attributes:
        points (Sequence[google.ads.googleads.v4.common.types.CpvBidSimulationPoint]):
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
        points (Sequence[google.ads.googleads.v4.common.types.TargetCpaSimulationPoint]):
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
        points (Sequence[google.ads.googleads.v4.common.types.TargetRoasSimulationPoint]):
            Projected metrics for a series of target ROAS
            amounts.
    """

    points = proto.RepeatedField(
        proto.MESSAGE, number=1, message="TargetRoasSimulationPoint",
    )


class BidModifierSimulationPoint(proto.Message):
    r"""Projected metrics for a specific bid modifier amount.

    Attributes:
        bid_modifier (google.protobuf.wrappers_pb2.DoubleValue):
            The simulated bid modifier upon which
            projected metrics are based.
        biddable_conversions (google.protobuf.wrappers_pb2.DoubleValue):
            Projected number of biddable conversions.
            Only search advertising channel type supports
            this field.
        biddable_conversions_value (google.protobuf.wrappers_pb2.DoubleValue):
            Projected total value of biddable
            conversions. Only search advertising channel
            type supports this field.
        clicks (google.protobuf.wrappers_pb2.Int64Value):
            Projected number of clicks.
        cost_micros (google.protobuf.wrappers_pb2.Int64Value):
            Projected cost in micros.
        impressions (google.protobuf.wrappers_pb2.Int64Value):
            Projected number of impressions.
        top_slot_impressions (google.protobuf.wrappers_pb2.Int64Value):
            Projected number of top slot impressions.
            Only search advertising channel type supports
            this field.
        parent_biddable_conversions (google.protobuf.wrappers_pb2.DoubleValue):
            Projected number of biddable conversions for
            the parent resource. Only search advertising
            channel type supports this field.
        parent_biddable_conversions_value (google.protobuf.wrappers_pb2.DoubleValue):
            Projected total value of biddable conversions
            for the parent resource. Only search advertising
            channel type supports this field.
        parent_clicks (google.protobuf.wrappers_pb2.Int64Value):
            Projected number of clicks for the parent
            resource.
        parent_cost_micros (google.protobuf.wrappers_pb2.Int64Value):
            Projected cost in micros for the parent
            resource.
        parent_impressions (google.protobuf.wrappers_pb2.Int64Value):
            Projected number of impressions for the
            parent resource.
        parent_top_slot_impressions (google.protobuf.wrappers_pb2.Int64Value):
            Projected number of top slot impressions for
            the parent resource. Only search advertising
            channel type supports this field.
        parent_required_budget_micros (google.protobuf.wrappers_pb2.Int64Value):
            Projected minimum daily budget that must be
            available to the parent resource to realize this
            simulation.
    """

    bid_modifier = proto.Field(
        proto.MESSAGE, number=1, message=wrappers.DoubleValue,
    )
    biddable_conversions = proto.Field(
        proto.MESSAGE, number=2, message=wrappers.DoubleValue,
    )
    biddable_conversions_value = proto.Field(
        proto.MESSAGE, number=3, message=wrappers.DoubleValue,
    )
    clicks = proto.Field(proto.MESSAGE, number=4, message=wrappers.Int64Value,)
    cost_micros = proto.Field(
        proto.MESSAGE, number=5, message=wrappers.Int64Value,
    )
    impressions = proto.Field(
        proto.MESSAGE, number=6, message=wrappers.Int64Value,
    )
    top_slot_impressions = proto.Field(
        proto.MESSAGE, number=7, message=wrappers.Int64Value,
    )
    parent_biddable_conversions = proto.Field(
        proto.MESSAGE, number=8, message=wrappers.DoubleValue,
    )
    parent_biddable_conversions_value = proto.Field(
        proto.MESSAGE, number=9, message=wrappers.DoubleValue,
    )
    parent_clicks = proto.Field(
        proto.MESSAGE, number=10, message=wrappers.Int64Value,
    )
    parent_cost_micros = proto.Field(
        proto.MESSAGE, number=11, message=wrappers.Int64Value,
    )
    parent_impressions = proto.Field(
        proto.MESSAGE, number=12, message=wrappers.Int64Value,
    )
    parent_top_slot_impressions = proto.Field(
        proto.MESSAGE, number=13, message=wrappers.Int64Value,
    )
    parent_required_budget_micros = proto.Field(
        proto.MESSAGE, number=14, message=wrappers.Int64Value,
    )


class CpcBidSimulationPoint(proto.Message):
    r"""Projected metrics for a specific CPC bid amount.

    Attributes:
        cpc_bid_micros (google.protobuf.wrappers_pb2.Int64Value):
            The simulated CPC bid upon which projected
            metrics are based.
        biddable_conversions (google.protobuf.wrappers_pb2.DoubleValue):
            Projected number of biddable conversions.
        biddable_conversions_value (google.protobuf.wrappers_pb2.DoubleValue):
            Projected total value of biddable
            conversions.
        clicks (google.protobuf.wrappers_pb2.Int64Value):
            Projected number of clicks.
        cost_micros (google.protobuf.wrappers_pb2.Int64Value):
            Projected cost in micros.
        impressions (google.protobuf.wrappers_pb2.Int64Value):
            Projected number of impressions.
        top_slot_impressions (google.protobuf.wrappers_pb2.Int64Value):
            Projected number of top slot impressions.
            Only search advertising channel type supports
            this field.
    """

    cpc_bid_micros = proto.Field(
        proto.MESSAGE, number=1, message=wrappers.Int64Value,
    )
    biddable_conversions = proto.Field(
        proto.MESSAGE, number=2, message=wrappers.DoubleValue,
    )
    biddable_conversions_value = proto.Field(
        proto.MESSAGE, number=3, message=wrappers.DoubleValue,
    )
    clicks = proto.Field(proto.MESSAGE, number=4, message=wrappers.Int64Value,)
    cost_micros = proto.Field(
        proto.MESSAGE, number=5, message=wrappers.Int64Value,
    )
    impressions = proto.Field(
        proto.MESSAGE, number=6, message=wrappers.Int64Value,
    )
    top_slot_impressions = proto.Field(
        proto.MESSAGE, number=7, message=wrappers.Int64Value,
    )


class CpvBidSimulationPoint(proto.Message):
    r"""Projected metrics for a specific CPV bid amount.

    Attributes:
        cpv_bid_micros (google.protobuf.wrappers_pb2.Int64Value):
            The simulated CPV bid upon which projected
            metrics are based.
        cost_micros (google.protobuf.wrappers_pb2.Int64Value):
            Projected cost in micros.
        impressions (google.protobuf.wrappers_pb2.Int64Value):
            Projected number of impressions.
        views (google.protobuf.wrappers_pb2.Int64Value):
            Projected number of views.
    """

    cpv_bid_micros = proto.Field(
        proto.MESSAGE, number=1, message=wrappers.Int64Value,
    )
    cost_micros = proto.Field(
        proto.MESSAGE, number=2, message=wrappers.Int64Value,
    )
    impressions = proto.Field(
        proto.MESSAGE, number=3, message=wrappers.Int64Value,
    )
    views = proto.Field(proto.MESSAGE, number=4, message=wrappers.Int64Value,)


class TargetCpaSimulationPoint(proto.Message):
    r"""Projected metrics for a specific target CPA amount.

    Attributes:
        target_cpa_micros (google.protobuf.wrappers_pb2.Int64Value):
            The simulated target CPA upon which projected
            metrics are based.
        biddable_conversions (google.protobuf.wrappers_pb2.DoubleValue):
            Projected number of biddable conversions.
        biddable_conversions_value (google.protobuf.wrappers_pb2.DoubleValue):
            Projected total value of biddable
            conversions.
        clicks (google.protobuf.wrappers_pb2.Int64Value):
            Projected number of clicks.
        cost_micros (google.protobuf.wrappers_pb2.Int64Value):
            Projected cost in micros.
        impressions (google.protobuf.wrappers_pb2.Int64Value):
            Projected number of impressions.
        top_slot_impressions (google.protobuf.wrappers_pb2.Int64Value):
            Projected number of top slot impressions.
            Only search advertising channel type supports
            this field.
    """

    target_cpa_micros = proto.Field(
        proto.MESSAGE, number=1, message=wrappers.Int64Value,
    )
    biddable_conversions = proto.Field(
        proto.MESSAGE, number=2, message=wrappers.DoubleValue,
    )
    biddable_conversions_value = proto.Field(
        proto.MESSAGE, number=3, message=wrappers.DoubleValue,
    )
    clicks = proto.Field(proto.MESSAGE, number=4, message=wrappers.Int64Value,)
    cost_micros = proto.Field(
        proto.MESSAGE, number=5, message=wrappers.Int64Value,
    )
    impressions = proto.Field(
        proto.MESSAGE, number=6, message=wrappers.Int64Value,
    )
    top_slot_impressions = proto.Field(
        proto.MESSAGE, number=7, message=wrappers.Int64Value,
    )


class TargetRoasSimulationPoint(proto.Message):
    r"""Projected metrics for a specific target ROAS amount.

    Attributes:
        target_roas (google.protobuf.wrappers_pb2.DoubleValue):
            The simulated target ROAS upon which
            projected metrics are based.
        biddable_conversions (google.protobuf.wrappers_pb2.DoubleValue):
            Projected number of biddable conversions.
        biddable_conversions_value (google.protobuf.wrappers_pb2.DoubleValue):
            Projected total value of biddable
            conversions.
        clicks (google.protobuf.wrappers_pb2.Int64Value):
            Projected number of clicks.
        cost_micros (google.protobuf.wrappers_pb2.Int64Value):
            Projected cost in micros.
        impressions (google.protobuf.wrappers_pb2.Int64Value):
            Projected number of impressions.
        top_slot_impressions (google.protobuf.wrappers_pb2.Int64Value):
            Projected number of top slot impressions.
            Only Search advertising channel type supports
            this field.
    """

    target_roas = proto.Field(
        proto.MESSAGE, number=1, message=wrappers.DoubleValue,
    )
    biddable_conversions = proto.Field(
        proto.MESSAGE, number=2, message=wrappers.DoubleValue,
    )
    biddable_conversions_value = proto.Field(
        proto.MESSAGE, number=3, message=wrappers.DoubleValue,
    )
    clicks = proto.Field(proto.MESSAGE, number=4, message=wrappers.Int64Value,)
    cost_micros = proto.Field(
        proto.MESSAGE, number=5, message=wrappers.Int64Value,
    )
    impressions = proto.Field(
        proto.MESSAGE, number=6, message=wrappers.Int64Value,
    )
    top_slot_impressions = proto.Field(
        proto.MESSAGE, number=7, message=wrappers.Int64Value,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
