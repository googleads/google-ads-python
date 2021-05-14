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

from google.ads.googleads.v7.common.types import keyword_plan_common
from google.ads.googleads.v7.enums.types import keyword_plan_keyword_annotation
from google.ads.googleads.v7.enums.types import (
    keyword_plan_network as gage_keyword_plan_network,
)


__protobuf__ = proto.module(
    package="google.ads.googleads.v7.services",
    marshal="google.ads.googleads.v7",
    manifest={
        "GenerateKeywordIdeasRequest",
        "KeywordAndUrlSeed",
        "KeywordSeed",
        "SiteSeed",
        "UrlSeed",
        "GenerateKeywordIdeaResponse",
        "GenerateKeywordIdeaResult",
    },
)


class GenerateKeywordIdeasRequest(proto.Message):
    r"""Request message for
    [KeywordPlanIdeaService.GenerateKeywordIdeas][google.ads.googleads.v7.services.KeywordPlanIdeaService.GenerateKeywordIdeas].

    Attributes:
        customer_id (str):
            The ID of the customer with the
            recommendation.
        language (str):
            The resource name of the language to target.
            Required
        geo_target_constants (Sequence[str]):
            The resource names of the location to target.
            Max 10
        include_adult_keywords (bool):
            If true, adult keywords will be included in
            response. The default value is false.
        page_token (str):
            Token of the page to retrieve. If not specified, the first
            page of results will be returned. To request next page of
            results use the value obtained from ``next_page_token`` in
            the previous response. The request fields must match across
            pages.
        page_size (int):
            Number of results to retrieve in a single page. A maximum of
            10,000 results may be returned, if the page_size exceeds
            this, it is ignored. If unspecified, at most 10,000 results
            will be returned. The server may decide to further limit the
            number of returned resources. If the response contains fewer
            than 10,000 results it may not be assumed as last page of
            results.
        keyword_plan_network (google.ads.googleads.v7.enums.types.KeywordPlanNetworkEnum.KeywordPlanNetwork):
            Targeting network.
        keyword_annotation (Sequence[google.ads.googleads.v7.enums.types.KeywordPlanKeywordAnnotationEnum.KeywordPlanKeywordAnnotation]):
            The keyword annotations to include in
            response.
        aggregate_metrics (google.ads.googleads.v7.common.types.KeywordPlanAggregateMetrics):
            The aggregate fields to include in response.
        historical_metrics_options (google.ads.googleads.v7.common.types.HistoricalMetricsOptions):
            The options for historical metrics data.
        keyword_and_url_seed (google.ads.googleads.v7.services.types.KeywordAndUrlSeed):
            A Keyword and a specific Url to generate
            ideas from e.g. cars, www.example.com/cars.
        keyword_seed (google.ads.googleads.v7.services.types.KeywordSeed):
            A Keyword or phrase to generate ideas from,
            e.g. cars.
        url_seed (google.ads.googleads.v7.services.types.UrlSeed):
            A specific url to generate ideas from, e.g.
            www.example.com/cars.
        site_seed (google.ads.googleads.v7.services.types.SiteSeed):
            The site to generate ideas from, e.g.
            www.example.com.
    """

    customer_id = proto.Field(proto.STRING, number=1,)
    language = proto.Field(proto.STRING, number=14, optional=True,)
    geo_target_constants = proto.RepeatedField(proto.STRING, number=15,)
    include_adult_keywords = proto.Field(proto.BOOL, number=10,)
    page_token = proto.Field(proto.STRING, number=12,)
    page_size = proto.Field(proto.INT32, number=13,)
    keyword_plan_network = proto.Field(
        proto.ENUM,
        number=9,
        enum=gage_keyword_plan_network.KeywordPlanNetworkEnum.KeywordPlanNetwork,
    )
    keyword_annotation = proto.RepeatedField(
        proto.ENUM,
        number=17,
        enum=keyword_plan_keyword_annotation.KeywordPlanKeywordAnnotationEnum.KeywordPlanKeywordAnnotation,
    )
    aggregate_metrics = proto.Field(
        proto.MESSAGE,
        number=16,
        message=keyword_plan_common.KeywordPlanAggregateMetrics,
    )
    historical_metrics_options = proto.Field(
        proto.MESSAGE,
        number=18,
        message=keyword_plan_common.HistoricalMetricsOptions,
    )
    keyword_and_url_seed = proto.Field(
        proto.MESSAGE, number=2, oneof="seed", message="KeywordAndUrlSeed",
    )
    keyword_seed = proto.Field(
        proto.MESSAGE, number=3, oneof="seed", message="KeywordSeed",
    )
    url_seed = proto.Field(
        proto.MESSAGE, number=5, oneof="seed", message="UrlSeed",
    )
    site_seed = proto.Field(
        proto.MESSAGE, number=11, oneof="seed", message="SiteSeed",
    )


class KeywordAndUrlSeed(proto.Message):
    r"""Keyword And Url Seed
    Attributes:
        url (str):
            The URL to crawl in order to generate keyword
            ideas.
        keywords (Sequence[str]):
            Requires at least one keyword.
    """

    url = proto.Field(proto.STRING, number=3, optional=True,)
    keywords = proto.RepeatedField(proto.STRING, number=4,)


class KeywordSeed(proto.Message):
    r"""Keyword Seed
    Attributes:
        keywords (Sequence[str]):
            Requires at least one keyword.
    """

    keywords = proto.RepeatedField(proto.STRING, number=2,)


class SiteSeed(proto.Message):
    r"""Site Seed
    Attributes:
        site (str):
            The domain name of the site. If the customer
            requesting the ideas doesn't own the site
            provided only public information is returned.
    """

    site = proto.Field(proto.STRING, number=2, optional=True,)


class UrlSeed(proto.Message):
    r"""Url Seed
    Attributes:
        url (str):
            The URL to crawl in order to generate keyword
            ideas.
    """

    url = proto.Field(proto.STRING, number=2, optional=True,)


class GenerateKeywordIdeaResponse(proto.Message):
    r"""Response message for
    [KeywordPlanIdeaService.GenerateKeywordIdeas][google.ads.googleads.v7.services.KeywordPlanIdeaService.GenerateKeywordIdeas].

    Attributes:
        results (Sequence[google.ads.googleads.v7.services.types.GenerateKeywordIdeaResult]):
            Results of generating keyword ideas.
        aggregate_metric_results (google.ads.googleads.v7.common.types.KeywordPlanAggregateMetricResults):
            The aggregate metrics for all keyword ideas.
        next_page_token (str):
            Pagination token used to retrieve the next page of results.
            Pass the content of this string as the ``page_token``
            attribute of the next request. ``next_page_token`` is not
            returned for the last page.
        total_size (int):
            Total number of results available.
    """

    @property
    def raw_page(self):
        return self

    results = proto.RepeatedField(
        proto.MESSAGE, number=1, message="GenerateKeywordIdeaResult",
    )
    aggregate_metric_results = proto.Field(
        proto.MESSAGE,
        number=4,
        message=keyword_plan_common.KeywordPlanAggregateMetricResults,
    )
    next_page_token = proto.Field(proto.STRING, number=2,)
    total_size = proto.Field(proto.INT64, number=3,)


class GenerateKeywordIdeaResult(proto.Message):
    r"""The result of generating keyword ideas.
    Attributes:
        text (str):
            Text of the keyword idea.
            As in Keyword Plan historical metrics, this text
            may not be an actual keyword, but the canonical
            form of multiple keywords. See
            KeywordPlanKeywordHistoricalMetrics message in
            KeywordPlanService.
        keyword_idea_metrics (google.ads.googleads.v7.common.types.KeywordPlanHistoricalMetrics):
            The historical metrics for the keyword.
        keyword_annotations (google.ads.googleads.v7.common.types.KeywordAnnotations):
            The annotations for the keyword.
            The annotation data is only provided if
            requested.
    """

    text = proto.Field(proto.STRING, number=5, optional=True,)
    keyword_idea_metrics = proto.Field(
        proto.MESSAGE,
        number=3,
        message=keyword_plan_common.KeywordPlanHistoricalMetrics,
    )
    keyword_annotations = proto.Field(
        proto.MESSAGE, number=6, message=keyword_plan_common.KeywordAnnotations,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
