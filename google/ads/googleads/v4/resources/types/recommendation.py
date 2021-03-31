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


from google.ads.googleads.v4.common.types import criteria
from google.ads.googleads.v4.common.types import extensions
from google.ads.googleads.v4.enums.types import keyword_match_type
from google.ads.googleads.v4.enums.types import recommendation_type
from google.ads.googleads.v4.enums.types import (
    target_cpa_opt_in_recommendation_goal,
)
from google.ads.googleads.v4.resources.types import ad as gagr_ad
from google.protobuf import wrappers_pb2 as wrappers  # type: ignore


__protobuf__ = proto.module(
    package="google.ads.googleads.v4.resources",
    marshal="google.ads.googleads.v4",
    manifest={"Recommendation",},
)


class Recommendation(proto.Message):
    r"""A recommendation.

    Attributes:
        resource_name (str):
            Immutable. The resource name of the recommendation.

            ``customers/{customer_id}/recommendations/{recommendation_id}``
        type_ (google.ads.googleads.v4.enums.types.RecommendationTypeEnum.RecommendationType):
            Output only. The type of recommendation.
        impact (google.ads.googleads.v4.resources.types.Recommendation.RecommendationImpact):
            Output only. The impact on account
            performance as a result of applying the
            recommendation.
        campaign_budget (google.protobuf.wrappers_pb2.StringValue):
            Output only. The budget targeted by this recommendation.
            This will be set only when the recommendation affects a
            single campaign budget.

            This field will be set for the following recommendation
            types: CAMPAIGN_BUDGET, FORECASTING_CAMPAIGN_BUDGET,
            MOVE_UNUSED_BUDGET
        campaign (google.protobuf.wrappers_pb2.StringValue):
            Output only. The campaign targeted by this recommendation.
            This will be set only when the recommendation affects a
            single campaign.

            This field will be set for the following recommendation
            types: CALL_EXTENSION, CALLOUT_EXTENSION,
            ENHANCED_CPC_OPT_IN, KEYWORD, KEYWORD_MATCH_TYPE,
            MAXIMIZE_CLICKS_OPT_IN, MAXIMIZE_CONVERSIONS_OPT_IN,
            OPTIMIZE_AD_ROTATION, SEARCH_PARTNERS_OPT_IN,
            SITELINK_EXTENSION, TARGET_CPA_OPT_IN, TARGET_ROAS_OPT_IN,
            TEXT_AD
        ad_group (google.protobuf.wrappers_pb2.StringValue):
            Output only. The ad group targeted by this recommendation.
            This will be set only when the recommendation affects a
            single ad group.

            This field will be set for the following recommendation
            types: KEYWORD, OPTIMIZE_AD_ROTATION, TEXT_AD
        dismissed (google.protobuf.wrappers_pb2.BoolValue):
            Output only. Whether the recommendation is
            dismissed or not.
        campaign_budget_recommendation (google.ads.googleads.v4.resources.types.Recommendation.CampaignBudgetRecommendation):
            Output only. The campaign budget
            recommendation.
        keyword_recommendation (google.ads.googleads.v4.resources.types.Recommendation.KeywordRecommendation):
            Output only. The keyword recommendation.
        text_ad_recommendation (google.ads.googleads.v4.resources.types.Recommendation.TextAdRecommendation):
            Output only. Add expanded text ad
            recommendation.
        target_cpa_opt_in_recommendation (google.ads.googleads.v4.resources.types.Recommendation.TargetCpaOptInRecommendation):
            Output only. The TargetCPA opt-in
            recommendation.
        maximize_conversions_opt_in_recommendation (google.ads.googleads.v4.resources.types.Recommendation.MaximizeConversionsOptInRecommendation):
            Output only. The MaximizeConversions Opt-In
            recommendation.
        enhanced_cpc_opt_in_recommendation (google.ads.googleads.v4.resources.types.Recommendation.EnhancedCpcOptInRecommendation):
            Output only. The Enhanced Cost-Per-Click Opt-
            n recommendation.
        search_partners_opt_in_recommendation (google.ads.googleads.v4.resources.types.Recommendation.SearchPartnersOptInRecommendation):
            Output only. The Search Partners Opt-In
            recommendation.
        maximize_clicks_opt_in_recommendation (google.ads.googleads.v4.resources.types.Recommendation.MaximizeClicksOptInRecommendation):
            Output only. The MaximizeClicks Opt-In
            recommendation.
        optimize_ad_rotation_recommendation (google.ads.googleads.v4.resources.types.Recommendation.OptimizeAdRotationRecommendation):
            Output only. The Optimize Ad Rotation
            recommendation.
        callout_extension_recommendation (google.ads.googleads.v4.resources.types.Recommendation.CalloutExtensionRecommendation):
            Output only. The Callout extension
            recommendation.
        sitelink_extension_recommendation (google.ads.googleads.v4.resources.types.Recommendation.SitelinkExtensionRecommendation):
            Output only. The Sitelink extension
            recommendation.
        call_extension_recommendation (google.ads.googleads.v4.resources.types.Recommendation.CallExtensionRecommendation):
            Output only. The Call extension
            recommendation.
        keyword_match_type_recommendation (google.ads.googleads.v4.resources.types.Recommendation.KeywordMatchTypeRecommendation):
            Output only. The keyword match type
            recommendation.
        move_unused_budget_recommendation (google.ads.googleads.v4.resources.types.Recommendation.MoveUnusedBudgetRecommendation):
            Output only. The move unused budget
            recommendation.
    """

    class RecommendationImpact(proto.Message):
        r"""The impact of making the change as described in the
        recommendation. Some types of recommendations may not have
        impact information.

        Attributes:
            base_metrics (google.ads.googleads.v4.resources.types.Recommendation.RecommendationMetrics):
                Output only. Base metrics at the time the
                recommendation was generated.
            potential_metrics (google.ads.googleads.v4.resources.types.Recommendation.RecommendationMetrics):
                Output only. Estimated metrics if the
                recommendation is applied.
        """

        base_metrics = proto.Field(
            proto.MESSAGE,
            number=1,
            message="Recommendation.RecommendationMetrics",
        )
        potential_metrics = proto.Field(
            proto.MESSAGE,
            number=2,
            message="Recommendation.RecommendationMetrics",
        )

    class RecommendationMetrics(proto.Message):
        r"""Weekly account performance metrics. For some recommendation
        types, these are averaged over the past 90-day period and hence
        can be fractional.

        Attributes:
            impressions (google.protobuf.wrappers_pb2.DoubleValue):
                Output only. Number of ad impressions.
            clicks (google.protobuf.wrappers_pb2.DoubleValue):
                Output only. Number of ad clicks.
            cost_micros (google.protobuf.wrappers_pb2.Int64Value):
                Output only. Cost (in micros) for
                advertising, in the local currency for the
                account.
            conversions (google.protobuf.wrappers_pb2.DoubleValue):
                Output only. Number of conversions.
            video_views (google.protobuf.wrappers_pb2.DoubleValue):
                Output only. Number of video views for a
                video ad campaign.
        """

        impressions = proto.Field(
            proto.MESSAGE, number=1, message=wrappers.DoubleValue,
        )
        clicks = proto.Field(
            proto.MESSAGE, number=2, message=wrappers.DoubleValue,
        )
        cost_micros = proto.Field(
            proto.MESSAGE, number=3, message=wrappers.Int64Value,
        )
        conversions = proto.Field(
            proto.MESSAGE, number=4, message=wrappers.DoubleValue,
        )
        video_views = proto.Field(
            proto.MESSAGE, number=5, message=wrappers.DoubleValue,
        )

    class CampaignBudgetRecommendation(proto.Message):
        r"""The budget recommendation for budget constrained campaigns.

        Attributes:
            current_budget_amount_micros (google.protobuf.wrappers_pb2.Int64Value):
                Output only. The current budget amount in
                micros.
            recommended_budget_amount_micros (google.protobuf.wrappers_pb2.Int64Value):
                Output only. The recommended budget amount in
                micros.
            budget_options (Sequence[google.ads.googleads.v4.resources.types.Recommendation.CampaignBudgetRecommendation.CampaignBudgetRecommendationOption]):
                Output only. The budget amounts and
                associated impact estimates for some values of
                possible budget amounts.
        """

        class CampaignBudgetRecommendationOption(proto.Message):
            r"""The impact estimates for a given budget amount.

            Attributes:
                budget_amount_micros (google.protobuf.wrappers_pb2.Int64Value):
                    Output only. The budget amount for this
                    option.
                impact (google.ads.googleads.v4.resources.types.Recommendation.RecommendationImpact):
                    Output only. The impact estimate if budget is
                    changed to amount specified in this option.
            """

            budget_amount_micros = proto.Field(
                proto.MESSAGE, number=1, message=wrappers.Int64Value,
            )
            impact = proto.Field(
                proto.MESSAGE,
                number=2,
                message="Recommendation.RecommendationImpact",
            )

        current_budget_amount_micros = proto.Field(
            proto.MESSAGE, number=1, message=wrappers.Int64Value,
        )
        recommended_budget_amount_micros = proto.Field(
            proto.MESSAGE, number=2, message=wrappers.Int64Value,
        )
        budget_options = proto.RepeatedField(
            proto.MESSAGE,
            number=3,
            message="Recommendation.CampaignBudgetRecommendation.CampaignBudgetRecommendationOption",
        )

    class KeywordRecommendation(proto.Message):
        r"""The keyword recommendation.

        Attributes:
            keyword (google.ads.googleads.v4.common.types.KeywordInfo):
                Output only. The recommended keyword.
            recommended_cpc_bid_micros (google.protobuf.wrappers_pb2.Int64Value):
                Output only. The recommended CPC (cost-per-
                lick) bid.
        """

        keyword = proto.Field(
            proto.MESSAGE, number=1, message=criteria.KeywordInfo,
        )
        recommended_cpc_bid_micros = proto.Field(
            proto.MESSAGE, number=2, message=wrappers.Int64Value,
        )

    class TextAdRecommendation(proto.Message):
        r"""The text ad recommendation.

        Attributes:
            ad (google.ads.googleads.v4.resources.types.Ad):
                Output only. Recommended ad.
            creation_date (google.protobuf.wrappers_pb2.StringValue):
                Output only. Creation date of the recommended
                ad. YYYY-MM-DD format, e.g., 2018-04-17.
            auto_apply_date (google.protobuf.wrappers_pb2.StringValue):
                Output only. Date, if present, is the
                earliest when the recommendation will be auto
                applied. YYYY-MM-DD format, e.g., 2018-04-17.
        """

        ad = proto.Field(proto.MESSAGE, number=1, message=gagr_ad.Ad,)
        creation_date = proto.Field(
            proto.MESSAGE, number=2, message=wrappers.StringValue,
        )
        auto_apply_date = proto.Field(
            proto.MESSAGE, number=3, message=wrappers.StringValue,
        )

    class MaximizeConversionsOptInRecommendation(proto.Message):
        r"""The Maximize Conversions Opt-In recommendation.

        Attributes:
            recommended_budget_amount_micros (google.protobuf.wrappers_pb2.Int64Value):
                Output only. The recommended new budget
                amount.
        """

        recommended_budget_amount_micros = proto.Field(
            proto.MESSAGE, number=1, message=wrappers.Int64Value,
        )

    class MoveUnusedBudgetRecommendation(proto.Message):
        r"""The move unused budget recommendation.

        Attributes:
            excess_campaign_budget (google.protobuf.wrappers_pb2.StringValue):
                Output only. The excess budget's resource_name.
            budget_recommendation (google.ads.googleads.v4.resources.types.Recommendation.CampaignBudgetRecommendation):
                Output only. The recommendation for the
                constrained budget to increase.
        """

        excess_campaign_budget = proto.Field(
            proto.MESSAGE, number=1, message=wrappers.StringValue,
        )
        budget_recommendation = proto.Field(
            proto.MESSAGE,
            number=2,
            message="Recommendation.CampaignBudgetRecommendation",
        )

    class TargetCpaOptInRecommendation(proto.Message):
        r"""The Target CPA opt-in recommendation.

        Attributes:
            options (Sequence[google.ads.googleads.v4.resources.types.Recommendation.TargetCpaOptInRecommendation.TargetCpaOptInRecommendationOption]):
                Output only. The available goals and
                corresponding options for Target CPA strategy.
            recommended_target_cpa_micros (google.protobuf.wrappers_pb2.Int64Value):
                Output only. The recommended average CPA
                target. See required budget amount and impact of
                using this recommendation in options list.
        """

        class TargetCpaOptInRecommendationOption(proto.Message):
            r"""The Target CPA opt-in option with impact estimate.

            Attributes:
                goal (google.ads.googleads.v4.enums.types.TargetCpaOptInRecommendationGoalEnum.TargetCpaOptInRecommendationGoal):
                    Output only. The goal achieved by this
                    option.
                target_cpa_micros (google.protobuf.wrappers_pb2.Int64Value):
                    Output only. Average CPA target.
                required_campaign_budget_amount_micros (google.protobuf.wrappers_pb2.Int64Value):
                    Output only. The minimum campaign budget, in
                    local currency for the account, required to
                    achieve the target CPA. Amount is specified in
                    micros, where one million is equivalent to one
                    currency unit.
                impact (google.ads.googleads.v4.resources.types.Recommendation.RecommendationImpact):
                    Output only. The impact estimate if this
                    option is selected.
            """

            goal = proto.Field(
                proto.ENUM,
                number=1,
                enum=target_cpa_opt_in_recommendation_goal.TargetCpaOptInRecommendationGoalEnum.TargetCpaOptInRecommendationGoal,
            )
            target_cpa_micros = proto.Field(
                proto.MESSAGE, number=2, message=wrappers.Int64Value,
            )
            required_campaign_budget_amount_micros = proto.Field(
                proto.MESSAGE, number=3, message=wrappers.Int64Value,
            )
            impact = proto.Field(
                proto.MESSAGE,
                number=4,
                message="Recommendation.RecommendationImpact",
            )

        options = proto.RepeatedField(
            proto.MESSAGE,
            number=1,
            message="Recommendation.TargetCpaOptInRecommendation.TargetCpaOptInRecommendationOption",
        )
        recommended_target_cpa_micros = proto.Field(
            proto.MESSAGE, number=2, message=wrappers.Int64Value,
        )

    class EnhancedCpcOptInRecommendation(proto.Message):
        r"""The Enhanced Cost-Per-Click Opt-In recommendation."""

    class SearchPartnersOptInRecommendation(proto.Message):
        r"""The Search Partners Opt-In recommendation."""

    class MaximizeClicksOptInRecommendation(proto.Message):
        r"""The Maximize Clicks opt-in recommendation.

        Attributes:
            recommended_budget_amount_micros (google.protobuf.wrappers_pb2.Int64Value):
                Output only. The recommended new budget
                amount. Only set if the current budget is too
                high.
        """

        recommended_budget_amount_micros = proto.Field(
            proto.MESSAGE, number=1, message=wrappers.Int64Value,
        )

    class OptimizeAdRotationRecommendation(proto.Message):
        r"""The Optimize Ad Rotation recommendation."""

    class SitelinkExtensionRecommendation(proto.Message):
        r"""The Sitelink extension recommendation.

        Attributes:
            recommended_extensions (Sequence[google.ads.googleads.v4.common.types.SitelinkFeedItem]):
                Output only. Sitelink extensions recommended
                to be added.
        """

        recommended_extensions = proto.RepeatedField(
            proto.MESSAGE, number=1, message=extensions.SitelinkFeedItem,
        )

    class CalloutExtensionRecommendation(proto.Message):
        r"""The Callout extension recommendation.

        Attributes:
            recommended_extensions (Sequence[google.ads.googleads.v4.common.types.CalloutFeedItem]):
                Output only. Callout extensions recommended
                to be added.
        """

        recommended_extensions = proto.RepeatedField(
            proto.MESSAGE, number=1, message=extensions.CalloutFeedItem,
        )

    class CallExtensionRecommendation(proto.Message):
        r"""The Call extension recommendation.

        Attributes:
            recommended_extensions (Sequence[google.ads.googleads.v4.common.types.CallFeedItem]):
                Output only. Call extensions recommended to
                be added.
        """

        recommended_extensions = proto.RepeatedField(
            proto.MESSAGE, number=1, message=extensions.CallFeedItem,
        )

    class KeywordMatchTypeRecommendation(proto.Message):
        r"""The keyword match type recommendation.

        Attributes:
            keyword (google.ads.googleads.v4.common.types.KeywordInfo):
                Output only. The existing keyword where the
                match type should be more broad.
            recommended_match_type (google.ads.googleads.v4.enums.types.KeywordMatchTypeEnum.KeywordMatchType):
                Output only. The recommended new match type.
        """

        keyword = proto.Field(
            proto.MESSAGE, number=1, message=criteria.KeywordInfo,
        )
        recommended_match_type = proto.Field(
            proto.ENUM,
            number=2,
            enum=keyword_match_type.KeywordMatchTypeEnum.KeywordMatchType,
        )

    resource_name = proto.Field(proto.STRING, number=1)
    type_ = proto.Field(
        proto.ENUM,
        number=2,
        enum=recommendation_type.RecommendationTypeEnum.RecommendationType,
    )
    impact = proto.Field(proto.MESSAGE, number=3, message=RecommendationImpact,)
    campaign_budget = proto.Field(
        proto.MESSAGE, number=5, message=wrappers.StringValue,
    )
    campaign = proto.Field(
        proto.MESSAGE, number=6, message=wrappers.StringValue,
    )
    ad_group = proto.Field(
        proto.MESSAGE, number=7, message=wrappers.StringValue,
    )
    dismissed = proto.Field(
        proto.MESSAGE, number=13, message=wrappers.BoolValue,
    )
    campaign_budget_recommendation = proto.Field(
        proto.MESSAGE,
        number=4,
        oneof="recommendation",
        message=CampaignBudgetRecommendation,
    )
    keyword_recommendation = proto.Field(
        proto.MESSAGE,
        number=8,
        oneof="recommendation",
        message=KeywordRecommendation,
    )
    text_ad_recommendation = proto.Field(
        proto.MESSAGE,
        number=9,
        oneof="recommendation",
        message=TextAdRecommendation,
    )
    target_cpa_opt_in_recommendation = proto.Field(
        proto.MESSAGE,
        number=10,
        oneof="recommendation",
        message=TargetCpaOptInRecommendation,
    )
    maximize_conversions_opt_in_recommendation = proto.Field(
        proto.MESSAGE,
        number=11,
        oneof="recommendation",
        message=MaximizeConversionsOptInRecommendation,
    )
    enhanced_cpc_opt_in_recommendation = proto.Field(
        proto.MESSAGE,
        number=12,
        oneof="recommendation",
        message=EnhancedCpcOptInRecommendation,
    )
    search_partners_opt_in_recommendation = proto.Field(
        proto.MESSAGE,
        number=14,
        oneof="recommendation",
        message=SearchPartnersOptInRecommendation,
    )
    maximize_clicks_opt_in_recommendation = proto.Field(
        proto.MESSAGE,
        number=15,
        oneof="recommendation",
        message=MaximizeClicksOptInRecommendation,
    )
    optimize_ad_rotation_recommendation = proto.Field(
        proto.MESSAGE,
        number=16,
        oneof="recommendation",
        message=OptimizeAdRotationRecommendation,
    )
    callout_extension_recommendation = proto.Field(
        proto.MESSAGE,
        number=17,
        oneof="recommendation",
        message=CalloutExtensionRecommendation,
    )
    sitelink_extension_recommendation = proto.Field(
        proto.MESSAGE,
        number=18,
        oneof="recommendation",
        message=SitelinkExtensionRecommendation,
    )
    call_extension_recommendation = proto.Field(
        proto.MESSAGE,
        number=19,
        oneof="recommendation",
        message=CallExtensionRecommendation,
    )
    keyword_match_type_recommendation = proto.Field(
        proto.MESSAGE,
        number=20,
        oneof="recommendation",
        message=KeywordMatchTypeRecommendation,
    )
    move_unused_budget_recommendation = proto.Field(
        proto.MESSAGE,
        number=21,
        oneof="recommendation",
        message=MoveUnusedBudgetRecommendation,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
