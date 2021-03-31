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


from google.ads.googleads.v4.common.types import keyword_plan_common
from google.ads.googleads.v4.resources.types import (
    keyword_plan as gagr_keyword_plan,
)
from google.protobuf import field_mask_pb2 as field_mask  # type: ignore
from google.protobuf import wrappers_pb2 as wrappers  # type: ignore
from google.rpc import status_pb2 as status  # type: ignore


__protobuf__ = proto.module(
    package="google.ads.googleads.v4.services",
    marshal="google.ads.googleads.v4",
    manifest={
        "GetKeywordPlanRequest",
        "MutateKeywordPlansRequest",
        "KeywordPlanOperation",
        "MutateKeywordPlansResponse",
        "MutateKeywordPlansResult",
        "GenerateForecastCurveRequest",
        "GenerateForecastCurveResponse",
        "GenerateForecastMetricsRequest",
        "GenerateForecastMetricsResponse",
        "KeywordPlanCampaignForecast",
        "KeywordPlanAdGroupForecast",
        "KeywordPlanKeywordForecast",
        "KeywordPlanCampaignForecastCurve",
        "KeywordPlanMaxCpcBidForecastCurve",
        "KeywordPlanMaxCpcBidForecast",
        "ForecastMetrics",
        "GenerateHistoricalMetricsRequest",
        "GenerateHistoricalMetricsResponse",
        "KeywordPlanKeywordHistoricalMetrics",
    },
)


class GetKeywordPlanRequest(proto.Message):
    r"""Request message for
    [KeywordPlanService.GetKeywordPlan][google.ads.googleads.v4.services.KeywordPlanService.GetKeywordPlan].

    Attributes:
        resource_name (str):
            Required. The resource name of the plan to
            fetch.
    """

    resource_name = proto.Field(proto.STRING, number=1)


class MutateKeywordPlansRequest(proto.Message):
    r"""Request message for
    [KeywordPlanService.MutateKeywordPlans][google.ads.googleads.v4.services.KeywordPlanService.MutateKeywordPlans].

    Attributes:
        customer_id (str):
            Required. The ID of the customer whose
            keyword plans are being modified.
        operations (Sequence[google.ads.googleads.v4.services.types.KeywordPlanOperation]):
            Required. The list of operations to perform
            on individual keyword plans.
        partial_failure (bool):
            If true, successful operations will be
            carried out and invalid operations will return
            errors. If false, all operations will be carried
            out in one transaction if and only if they are
            all valid. Default is false.
        validate_only (bool):
            If true, the request is validated but not
            executed. Only errors are returned, not results.
    """

    customer_id = proto.Field(proto.STRING, number=1)
    operations = proto.RepeatedField(
        proto.MESSAGE, number=2, message="KeywordPlanOperation",
    )
    partial_failure = proto.Field(proto.BOOL, number=3)
    validate_only = proto.Field(proto.BOOL, number=4)


class KeywordPlanOperation(proto.Message):
    r"""A single operation (create, update, remove) on a keyword
    plan.

    Attributes:
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            The FieldMask that determines which resource
            fields are modified in an update.
        create (google.ads.googleads.v4.resources.types.KeywordPlan):
            Create operation: No resource name is
            expected for the new keyword plan.
        update (google.ads.googleads.v4.resources.types.KeywordPlan):
            Update operation: The keyword plan is
            expected to have a valid resource name.
        remove (str):
            Remove operation: A resource name for the removed keyword
            plan is expected in this format:

            ``customers/{customer_id}/keywordPlans/{keyword_plan_id}``
    """

    update_mask = proto.Field(
        proto.MESSAGE, number=4, message=field_mask.FieldMask,
    )
    create = proto.Field(
        proto.MESSAGE,
        number=1,
        oneof="operation",
        message=gagr_keyword_plan.KeywordPlan,
    )
    update = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="operation",
        message=gagr_keyword_plan.KeywordPlan,
    )
    remove = proto.Field(proto.STRING, number=3, oneof="operation")


class MutateKeywordPlansResponse(proto.Message):
    r"""Response message for a keyword plan mutate.

    Attributes:
        partial_failure_error (google.rpc.status_pb2.Status):
            Errors that pertain to operation failures in the partial
            failure mode. Returned only when partial_failure = true and
            all errors occur inside the operations. If any errors occur
            outside the operations (e.g. auth errors), we return an RPC
            level error.
        results (Sequence[google.ads.googleads.v4.services.types.MutateKeywordPlansResult]):
            All results for the mutate.
    """

    partial_failure_error = proto.Field(
        proto.MESSAGE, number=3, message=status.Status,
    )
    results = proto.RepeatedField(
        proto.MESSAGE, number=2, message="MutateKeywordPlansResult",
    )


class MutateKeywordPlansResult(proto.Message):
    r"""The result for the keyword plan mutate.

    Attributes:
        resource_name (str):
            Returned for successful operations.
    """

    resource_name = proto.Field(proto.STRING, number=1)


class GenerateForecastCurveRequest(proto.Message):
    r"""Request message for
    [KeywordPlanService.GenerateForecastCurve][google.ads.googleads.v4.services.KeywordPlanService.GenerateForecastCurve].

    Attributes:
        keyword_plan (str):
            Required. The resource name of the keyword
            plan to be forecasted.
    """

    keyword_plan = proto.Field(proto.STRING, number=1)


class GenerateForecastCurveResponse(proto.Message):
    r"""Response message for
    [KeywordPlanService.GenerateForecastCurve][google.ads.googleads.v4.services.KeywordPlanService.GenerateForecastCurve].

    Attributes:
        campaign_forecast_curves (Sequence[google.ads.googleads.v4.services.types.KeywordPlanCampaignForecastCurve]):
            List of forecast curves for the keyword plan
            campaign. One maximum.
    """

    campaign_forecast_curves = proto.RepeatedField(
        proto.MESSAGE, number=1, message="KeywordPlanCampaignForecastCurve",
    )


class GenerateForecastMetricsRequest(proto.Message):
    r"""Request message for
    [KeywordPlanService.GenerateForecastMetrics][google.ads.googleads.v4.services.KeywordPlanService.GenerateForecastMetrics].

    Attributes:
        keyword_plan (str):
            Required. The resource name of the keyword
            plan to be forecasted.
    """

    keyword_plan = proto.Field(proto.STRING, number=1)


class GenerateForecastMetricsResponse(proto.Message):
    r"""Response message for
    [KeywordPlanService.GenerateForecastMetrics][google.ads.googleads.v4.services.KeywordPlanService.GenerateForecastMetrics].

    Attributes:
        campaign_forecasts (Sequence[google.ads.googleads.v4.services.types.KeywordPlanCampaignForecast]):
            List of campaign forecasts.
            One maximum.
        ad_group_forecasts (Sequence[google.ads.googleads.v4.services.types.KeywordPlanAdGroupForecast]):
            List of ad group forecasts.
        keyword_forecasts (Sequence[google.ads.googleads.v4.services.types.KeywordPlanKeywordForecast]):
            List of keyword forecasts.
    """

    campaign_forecasts = proto.RepeatedField(
        proto.MESSAGE, number=1, message="KeywordPlanCampaignForecast",
    )
    ad_group_forecasts = proto.RepeatedField(
        proto.MESSAGE, number=2, message="KeywordPlanAdGroupForecast",
    )
    keyword_forecasts = proto.RepeatedField(
        proto.MESSAGE, number=3, message="KeywordPlanKeywordForecast",
    )


class KeywordPlanCampaignForecast(proto.Message):
    r"""A campaign forecast.

    Attributes:
        keyword_plan_campaign (google.protobuf.wrappers_pb2.StringValue):
            The resource name of the Keyword Plan campaign related to
            the forecast.

            ``customers/{customer_id}/keywordPlanCampaigns/{keyword_plan_campaign_id}``
        campaign_forecast (google.ads.googleads.v4.services.types.ForecastMetrics):
            The forecast for the Keyword Plan campaign.
    """

    keyword_plan_campaign = proto.Field(
        proto.MESSAGE, number=1, message=wrappers.StringValue,
    )
    campaign_forecast = proto.Field(
        proto.MESSAGE, number=2, message="ForecastMetrics",
    )


class KeywordPlanAdGroupForecast(proto.Message):
    r"""An ad group forecast.

    Attributes:
        keyword_plan_ad_group (google.protobuf.wrappers_pb2.StringValue):
            The resource name of the Keyword Plan ad group related to
            the forecast.

            ``customers/{customer_id}/keywordPlanAdGroups/{keyword_plan_ad_group_id}``
        ad_group_forecast (google.ads.googleads.v4.services.types.ForecastMetrics):
            The forecast for the Keyword Plan ad group.
    """

    keyword_plan_ad_group = proto.Field(
        proto.MESSAGE, number=1, message=wrappers.StringValue,
    )
    ad_group_forecast = proto.Field(
        proto.MESSAGE, number=2, message="ForecastMetrics",
    )


class KeywordPlanKeywordForecast(proto.Message):
    r"""A keyword forecast.

    Attributes:
        keyword_plan_ad_group_keyword (google.protobuf.wrappers_pb2.StringValue):
            The resource name of the Keyword Plan keyword related to the
            forecast.

            ``customers/{customer_id}/keywordPlanAdGroupKeywords/{keyword_plan_ad_group_keyword_id}``
        keyword_forecast (google.ads.googleads.v4.services.types.ForecastMetrics):
            The forecast for the Keyword Plan keyword.
    """

    keyword_plan_ad_group_keyword = proto.Field(
        proto.MESSAGE, number=1, message=wrappers.StringValue,
    )
    keyword_forecast = proto.Field(
        proto.MESSAGE, number=2, message="ForecastMetrics",
    )


class KeywordPlanCampaignForecastCurve(proto.Message):
    r"""The forecast curve for the campaign.

    Attributes:
        keyword_plan_campaign (google.protobuf.wrappers_pb2.StringValue):
            The resource name of the Keyword Plan campaign related to
            the forecast.

            ``customers/{customer_id}/keywordPlanCampaigns/{keyword_plan_campaign_id}``
        max_cpc_bid_forecast_curve (google.ads.googleads.v4.services.types.KeywordPlanMaxCpcBidForecastCurve):
            The max cpc bid forecast curve for the
            campaign.
    """

    keyword_plan_campaign = proto.Field(
        proto.MESSAGE, number=1, message=wrappers.StringValue,
    )
    max_cpc_bid_forecast_curve = proto.Field(
        proto.MESSAGE, number=2, message="KeywordPlanMaxCpcBidForecastCurve",
    )


class KeywordPlanMaxCpcBidForecastCurve(proto.Message):
    r"""The max cpc bid forecast curve.

    Attributes:
        max_cpc_bid_forecasts (Sequence[google.ads.googleads.v4.services.types.KeywordPlanMaxCpcBidForecast]):
            The forecasts for the Keyword Plan campaign
            at different max CPC bids.
    """

    max_cpc_bid_forecasts = proto.RepeatedField(
        proto.MESSAGE, number=1, message="KeywordPlanMaxCpcBidForecast",
    )


class KeywordPlanMaxCpcBidForecast(proto.Message):
    r"""The forecast of the campaign at a specific bid.

    Attributes:
        max_cpc_bid_micros (google.protobuf.wrappers_pb2.Int64Value):
            The max cpc bid in micros.
        max_cpc_bid_forecast (google.ads.googleads.v4.services.types.ForecastMetrics):
            The forecast for the Keyword Plan campaign at
            the specific bid.
    """

    max_cpc_bid_micros = proto.Field(
        proto.MESSAGE, number=1, message=wrappers.Int64Value,
    )
    max_cpc_bid_forecast = proto.Field(
        proto.MESSAGE, number=2, message="ForecastMetrics",
    )


class ForecastMetrics(proto.Message):
    r"""Forecast metrics.

    Attributes:
        impressions (google.protobuf.wrappers_pb2.DoubleValue):
            Impressions
        ctr (google.protobuf.wrappers_pb2.DoubleValue):
            Ctr
        average_cpc (google.protobuf.wrappers_pb2.Int64Value):
            AVG cpc
        clicks (google.protobuf.wrappers_pb2.DoubleValue):
            Clicks
        cost_micros (google.protobuf.wrappers_pb2.Int64Value):
            Cost
    """

    impressions = proto.Field(
        proto.MESSAGE, number=1, message=wrappers.DoubleValue,
    )
    ctr = proto.Field(proto.MESSAGE, number=2, message=wrappers.DoubleValue,)
    average_cpc = proto.Field(
        proto.MESSAGE, number=3, message=wrappers.Int64Value,
    )
    clicks = proto.Field(proto.MESSAGE, number=5, message=wrappers.DoubleValue,)
    cost_micros = proto.Field(
        proto.MESSAGE, number=6, message=wrappers.Int64Value,
    )


class GenerateHistoricalMetricsRequest(proto.Message):
    r"""Request message for
    [KeywordPlanService.GenerateHistoricalMetrics][google.ads.googleads.v4.services.KeywordPlanService.GenerateHistoricalMetrics].

    Attributes:
        keyword_plan (str):
            Required. The resource name of the keyword
            plan of which historical metrics are requested.
    """

    keyword_plan = proto.Field(proto.STRING, number=1)


class GenerateHistoricalMetricsResponse(proto.Message):
    r"""Response message for
    [KeywordPlanService.GenerateHistoricalMetrics][google.ads.googleads.v4.services.KeywordPlanService.GenerateHistoricalMetrics].

    Attributes:
        metrics (Sequence[google.ads.googleads.v4.services.types.KeywordPlanKeywordHistoricalMetrics]):
            List of keyword historical metrics.
    """

    metrics = proto.RepeatedField(
        proto.MESSAGE, number=1, message="KeywordPlanKeywordHistoricalMetrics",
    )


class KeywordPlanKeywordHistoricalMetrics(proto.Message):
    r"""A keyword historical metrics.

    Attributes:
        search_query (google.protobuf.wrappers_pb2.StringValue):
            The text of the query associated with one or more
            ad_group_keywords in the plan.

            Note that we de-dupe your keywords list, eliminating close
            variants before returning the plan's keywords as text. For
            example, if your plan originally contained the keywords
            'car' and 'cars', the returned search query will only
            contain 'cars'. Starting V5, the list of de-duped queries
            will be included in close_variants field.
        keyword_metrics (google.ads.googleads.v4.common.types.KeywordPlanHistoricalMetrics):
            The historical metrics for the query associated with one or
            more ad_group_keywords in the plan.
    """

    search_query = proto.Field(
        proto.MESSAGE, number=1, message=wrappers.StringValue,
    )
    keyword_metrics = proto.Field(
        proto.MESSAGE,
        number=2,
        message=keyword_plan_common.KeywordPlanHistoricalMetrics,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
