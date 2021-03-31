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


from google.ads.googleads.v6.common.types import bidding
from google.ads.googleads.v6.enums.types import bidding_strategy_status
from google.ads.googleads.v6.enums.types import bidding_strategy_type


__protobuf__ = proto.module(
    package="google.ads.googleads.v6.resources",
    marshal="google.ads.googleads.v6",
    manifest={"BiddingStrategy",},
)


class BiddingStrategy(proto.Message):
    r"""A bidding strategy.

    Attributes:
        resource_name (str):
            Immutable. The resource name of the bidding strategy.
            Bidding strategy resource names have the form:

            ``customers/{customer_id}/biddingStrategies/{bidding_strategy_id}``
        id (int):
            Output only. The ID of the bidding strategy.
        name (str):
            The name of the bidding strategy.
            All bidding strategies within an account must be
            named distinctly.
            The length of this string should be between 1
            and 255, inclusive, in UTF-8 bytes, (trimmed).
        status (google.ads.googleads.v6.enums.types.BiddingStrategyStatusEnum.BiddingStrategyStatus):
            Output only. The status of the bidding
            strategy.
            This field is read-only.
        type_ (google.ads.googleads.v6.enums.types.BiddingStrategyTypeEnum.BiddingStrategyType):
            Output only. The type of the bidding
            strategy. Create a bidding strategy by setting
            the bidding scheme.
            This field is read-only.
        effective_currency_code (str):
            Output only. The currency used by the bidding strategy (ISO
            4217 three-letter code).

            For bidding strategies in manager customers, this is the
            currency set by the advertiser when creating the strategy.
            For serving customers, this is the customer's currency_code.

            Bidding strategy metrics are reported in this currency.

            This field is read-only.
        campaign_count (int):
            Output only. The number of campaigns attached
            to this bidding strategy.
            This field is read-only.
        non_removed_campaign_count (int):
            Output only. The number of non-removed
            campaigns attached to this bidding strategy.
            This field is read-only.
        enhanced_cpc (google.ads.googleads.v6.common.types.EnhancedCpc):
            A bidding strategy that raises bids for
            clicks that seem more likely to lead to a
            conversion and lowers them for clicks where they
            seem less likely.
        maximize_conversion_value (google.ads.googleads.v6.common.types.MaximizeConversionValue):
            An automated bidding strategy to help get the
            most conversion value for your campaigns while
            spending your budget.
        maximize_conversions (google.ads.googleads.v6.common.types.MaximizeConversions):
            An automated bidding strategy to help get the
            most conversions for your campaigns while
            spending your budget.
        target_cpa (google.ads.googleads.v6.common.types.TargetCpa):
            A bidding strategy that sets bids to help get
            as many conversions as possible at the target
            cost-per-acquisition (CPA) you set.
        target_impression_share (google.ads.googleads.v6.common.types.TargetImpressionShare):
            A bidding strategy that automatically
            optimizes towards a desired percentage of
            impressions.
        target_roas (google.ads.googleads.v6.common.types.TargetRoas):
            A bidding strategy that helps you maximize
            revenue while averaging a specific target Return
            On Ad Spend (ROAS).
        target_spend (google.ads.googleads.v6.common.types.TargetSpend):
            A bid strategy that sets your bids to help
            get as many clicks as possible within your
            budget.
    """

    resource_name = proto.Field(proto.STRING, number=1)
    id = proto.Field(proto.INT64, number=16, optional=True)
    name = proto.Field(proto.STRING, number=17, optional=True)
    status = proto.Field(
        proto.ENUM,
        number=15,
        enum=bidding_strategy_status.BiddingStrategyStatusEnum.BiddingStrategyStatus,
    )
    type_ = proto.Field(
        proto.ENUM,
        number=5,
        enum=bidding_strategy_type.BiddingStrategyTypeEnum.BiddingStrategyType,
    )
    effective_currency_code = proto.Field(
        proto.STRING, number=20, optional=True
    )
    campaign_count = proto.Field(proto.INT64, number=18, optional=True)
    non_removed_campaign_count = proto.Field(
        proto.INT64, number=19, optional=True
    )
    enhanced_cpc = proto.Field(
        proto.MESSAGE, number=7, oneof="scheme", message=bidding.EnhancedCpc,
    )
    maximize_conversion_value = proto.Field(
        proto.MESSAGE,
        number=21,
        oneof="scheme",
        message=bidding.MaximizeConversionValue,
    )
    maximize_conversions = proto.Field(
        proto.MESSAGE,
        number=22,
        oneof="scheme",
        message=bidding.MaximizeConversions,
    )
    target_cpa = proto.Field(
        proto.MESSAGE, number=9, oneof="scheme", message=bidding.TargetCpa,
    )
    target_impression_share = proto.Field(
        proto.MESSAGE,
        number=48,
        oneof="scheme",
        message=bidding.TargetImpressionShare,
    )
    target_roas = proto.Field(
        proto.MESSAGE, number=11, oneof="scheme", message=bidding.TargetRoas,
    )
    target_spend = proto.Field(
        proto.MESSAGE, number=12, oneof="scheme", message=bidding.TargetSpend,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
