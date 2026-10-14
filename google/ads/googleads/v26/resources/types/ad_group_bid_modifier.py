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

from google.ads.googleads.v26.common.types import criteria
from google.ads.googleads.v26.enums.types import (
    bid_modifier_source as gage_bid_modifier_source,
)


__protobuf__ = proto.module(
    package="google.ads.googleads.v26.resources",
    marshal="google.ads.googleads.v26",
    manifest={
        "AdGroupBidModifier",
    },
)


class AdGroupBidModifier(proto.Message):
    r"""Represents an ad group bid modifier.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        resource_name (str):
            Immutable. The resource name of the ad group bid modifier.
            Ad group bid modifier resource names have the form:

            ``customers/{customer_id}/adGroupBidModifiers/{ad_group_id}~{criterion_id}``
        ad_group (str):
            Immutable. The ad group to which this
            criterion belongs.

            This field is a member of `oneof`_ ``_ad_group``.
        criterion_id (int):
            Output only. The ID of the criterion to bid
            modify.
            This field is ignored for mutates.

            This field is a member of `oneof`_ ``_criterion_id``.
        bid_modifier (float):
            The modifier for the bid when the criterion
            matches. The modifier must be in the range: 0.1
            - 10.0. Use 0 to opt out of a Device type.

            This field is a member of `oneof`_ ``_bid_modifier``.
        base_ad_group (str):
            Output only. The base ad group from which this draft/trial
            adgroup bid modifier was created. If ad_group is a base ad
            group then this field will be equal to ad_group. If the ad
            group was created in the draft or trial and has no
            corresponding base ad group, then this field will be null.
            This field is readonly.

            This field is a member of `oneof`_ ``_base_ad_group``.
        bid_modifier_source (google.ads.googleads.v26.enums.types.BidModifierSourceEnum.BidModifierSource):
            Output only. Bid modifier source.
        device (google.ads.googleads.v26.common.types.DeviceInfo):
            Immutable. A device criterion.

            This field is a member of `oneof`_ ``criterion``.
        user_set_dates (google.ads.googleads.v26.common.types.UserSetDatesInfo):
            Immutable. Criterion for the date selection
            (default dates versus user selected).

            This field is a member of `oneof`_ ``criterion``.
        advance_booking_window (google.ads.googleads.v26.common.types.AdvanceBookingWindowInfo):
            Immutable. Criterion for the number of days
            prior to the start date of the booking.

            This field is a member of `oneof`_ ``criterion``.
        length_of_booking (google.ads.googleads.v26.common.types.LengthOfBookingInfo):
            Immutable. Criterion for the length of the
            booking in days.

            This field is a member of `oneof`_ ``criterion``.
        start_day_of_week (google.ads.googleads.v26.common.types.StartDayOfWeekInfo):
            Immutable. Criterion for the day of the week
            of the booking start date.

            This field is a member of `oneof`_ ``criterion``.
        start_date_range (google.ads.googleads.v26.common.types.StartDateRangeInfo):
            Immutable. Criterion for the date range of
            the start of the booking.

            This field is a member of `oneof`_ ``criterion``.
    """

    resource_name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    ad_group: str = proto.Field(
        proto.STRING,
        number=13,
        optional=True,
    )
    criterion_id: int = proto.Field(
        proto.INT64,
        number=14,
        optional=True,
    )
    bid_modifier: float = proto.Field(
        proto.DOUBLE,
        number=15,
        optional=True,
    )
    base_ad_group: str = proto.Field(
        proto.STRING,
        number=16,
        optional=True,
    )
    bid_modifier_source: (
        gage_bid_modifier_source.BidModifierSourceEnum.BidModifierSource
    ) = proto.Field(
        proto.ENUM,
        number=10,
        enum=gage_bid_modifier_source.BidModifierSourceEnum.BidModifierSource,
    )
    device: criteria.DeviceInfo = proto.Field(
        proto.MESSAGE,
        number=11,
        oneof="criterion",
        message=criteria.DeviceInfo,
    )
    user_set_dates: criteria.UserSetDatesInfo = proto.Field(
        proto.MESSAGE,
        number=18,
        oneof="criterion",
        message=criteria.UserSetDatesInfo,
    )
    advance_booking_window: criteria.AdvanceBookingWindowInfo = proto.Field(
        proto.MESSAGE,
        number=19,
        oneof="criterion",
        message=criteria.AdvanceBookingWindowInfo,
    )
    length_of_booking: criteria.LengthOfBookingInfo = proto.Field(
        proto.MESSAGE,
        number=20,
        oneof="criterion",
        message=criteria.LengthOfBookingInfo,
    )
    start_day_of_week: criteria.StartDayOfWeekInfo = proto.Field(
        proto.MESSAGE,
        number=21,
        oneof="criterion",
        message=criteria.StartDayOfWeekInfo,
    )
    start_date_range: criteria.StartDateRangeInfo = proto.Field(
        proto.MESSAGE,
        number=22,
        oneof="criterion",
        message=criteria.StartDateRangeInfo,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
