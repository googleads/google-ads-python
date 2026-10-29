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

from typing import MutableSequence

import proto  # type: ignore

from google.ads.googleads.v26.enums.types import (
    advertising_channel_type as gage_advertising_channel_type,
)
from google.ads.googleads.v26.enums.types import (
    budget_network_ineligible_reason,
)
from google.ads.googleads.v26.enums.types import channel_priority_tier
from google.ads.googleads.v26.enums.types import network_channel_type


__protobuf__ = proto.module(
    package="google.ads.googleads.v26.common",
    marshal="google.ads.googleads.v26",
    manifest={
        "BudgetNetworkSettings",
        "BudgetNetworkSetting",
        "BudgetCapConfig",
        "ChannelPriorityConfig",
        "BudgetNetworkEligibility",
    },
)


class BudgetNetworkSettings(proto.Message):
    r"""Container for budget network settings (waterfall channel
    prioritization and budget allocation).

    Attributes:
        settings (MutableSequence[google.ads.googleads.v26.common.types.BudgetNetworkSetting]):
            List of network allocation settings per
            advertising channel type. Each advertising
            channel type can appear at most once in this
            list.
    """

    settings: MutableSequence["BudgetNetworkSetting"] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="BudgetNetworkSetting",
    )


class BudgetNetworkSetting(proto.Message):
    r"""Budget allocation setting for a specific advertising channel type
    (e.g., SEARCH, SHOPPING, PERFORMANCE_MAX).

    Attributes:
        advertising_channel_type (google.ads.googleads.v26.enums.types.AdvertisingChannelTypeEnum.AdvertisingChannelType):
            The advertising channel type this setting applies to (e.g.,
            SEARCH, SHOPPING, or PERFORMANCE_MAX).
        budget_caps (MutableSequence[google.ads.googleads.v26.common.types.BudgetCapConfig]):
            Budget caps restricting spend per secondary
            network channel. Caps can only be applied to
            channels assigned to secondary priority tiers,
            and each network channel can appear at most once
            in this list.
        channel_priorities (MutableSequence[google.ads.googleads.v26.common.types.ChannelPriorityConfig]):
            Waterfall priority tiers per network channel.
    """

    advertising_channel_type: (
        gage_advertising_channel_type.AdvertisingChannelTypeEnum.AdvertisingChannelType
    ) = proto.Field(
        proto.ENUM,
        number=1,
        enum=gage_advertising_channel_type.AdvertisingChannelTypeEnum.AdvertisingChannelType,
    )
    budget_caps: MutableSequence["BudgetCapConfig"] = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message="BudgetCapConfig",
    )
    channel_priorities: MutableSequence["ChannelPriorityConfig"] = (
        proto.RepeatedField(
            proto.MESSAGE,
            number=3,
            message="ChannelPriorityConfig",
        )
    )


class BudgetCapConfig(proto.Message):
    r"""Configures a maximum percentage of the total budget that a
    network channel can spend.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        network_channel (google.ads.googleads.v26.enums.types.NetworkChannelTypeEnum.NetworkChannelType):
            The network channel being capped.
        cap_percent_millis (int):
            The maximum percentage of the total budget
            that this network channel can spend, specified
            in milli-percent units (for example, 100,000 =
            100%, 50,000 = 50%, and 1,000 = 1%). Valid range
            is 0 to 100,000, where 0 represents a complete
            0% opt-out.

            This field is a member of `oneof`_ ``_cap_percent_millis``.
    """

    network_channel: (
        network_channel_type.NetworkChannelTypeEnum.NetworkChannelType
    ) = proto.Field(
        proto.ENUM,
        number=1,
        enum=network_channel_type.NetworkChannelTypeEnum.NetworkChannelType,
    )
    cap_percent_millis: int = proto.Field(
        proto.INT64,
        number=2,
        optional=True,
    )


class ChannelPriorityConfig(proto.Message):
    r"""Configures which network channels belong to a priority tier.

    Attributes:
        priority_tier (google.ads.googleads.v26.enums.types.ChannelPriorityTierEnum.ChannelPriorityTier):
            The priority tier (e.g., TIER1, TIER2).
        network_channels (MutableSequence[google.ads.googleads.v26.enums.types.NetworkChannelTypeEnum.NetworkChannelType]):
            The network channels assigned to this
            priority tier.
    """

    priority_tier: (
        channel_priority_tier.ChannelPriorityTierEnum.ChannelPriorityTier
    ) = proto.Field(
        proto.ENUM,
        number=1,
        enum=channel_priority_tier.ChannelPriorityTierEnum.ChannelPriorityTier,
    )
    network_channels: MutableSequence[
        network_channel_type.NetworkChannelTypeEnum.NetworkChannelType
    ] = proto.RepeatedField(
        proto.ENUM,
        number=2,
        enum=network_channel_type.NetworkChannelTypeEnum.NetworkChannelType,
    )


class BudgetNetworkEligibility(proto.Message):
    r"""Read-only eligibility status and reasons for budget network
    allocation on a CampaignBudget.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        eligible (bool):
            Output only. True if the budget is eligible
            for waterfall and budget cap allocation.

            This field is a member of `oneof`_ ``_eligible``.
        ineligible_reasons (MutableSequence[google.ads.googleads.v26.enums.types.BudgetNetworkIneligibleReasonEnum.BudgetNetworkIneligibleReason]):
            Output only. Reasons why the budget is
            ineligible, if eligible is false.
    """

    eligible: bool = proto.Field(
        proto.BOOL,
        number=1,
        optional=True,
    )
    ineligible_reasons: MutableSequence[
        budget_network_ineligible_reason.BudgetNetworkIneligibleReasonEnum.BudgetNetworkIneligibleReason
    ] = proto.RepeatedField(
        proto.ENUM,
        number=2,
        enum=budget_network_ineligible_reason.BudgetNetworkIneligibleReasonEnum.BudgetNetworkIneligibleReason,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
