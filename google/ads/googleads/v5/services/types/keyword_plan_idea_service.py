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


from google.ads.googleads.v5.common.types import keyword_plan_common
from google.ads.googleads.v5.enums.types import (
    keyword_plan_network as gage_keyword_plan_network,
)
from google.protobuf import wrappers_pb2 as wrappers  # type: ignore


__protobuf__ = proto.module(
    package="google.ads.googleads.v5.services",
    marshal="google.ads.googleads.v5",
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
    [KeywordPlanIdeaService.GenerateKeywordIdeas][google.ads.googleads.v5.services.KeywordPlanIdeaService.GenerateKeywordIdeas].

    Attributes:
        customer_id (str):
            The ID of the customer with the
            recommendation.
        language (google.protobuf.wrappers_pb2.StringValue):
            Required. The resource name of the language
            to target. Required
        geo_target_constants (Sequence[google.protobuf.wrappers_pb2.StringValue]):
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
        keyword_plan_network (google.ads.googleads.v5.enums.types.KeywordPlanNetworkEnum.KeywordPlanNetwork):
            Targeting network.
        keyword_and_url_seed (google.ads.googleads.v5.services.types.KeywordAndUrlSeed):
            A Keyword and a specific Url to generate
            ideas from e.g. cars, www.example.com/cars.
        keyword_seed (google.ads.googleads.v5.services.types.KeywordSeed):
            A Keyword or phrase to generate ideas from,
            e.g. cars.
        url_seed (google.ads.googleads.v5.services.types.UrlSeed):
            A specific url to generate ideas from, e.g.
            www.example.com/cars.
        site_seed (google.ads.googleads.v5.services.types.SiteSeed):
            The site to generate ideas from, e.g.
            www.example.com.
    """

    customer_id = proto.Field(proto.STRING, number=1)
    language = proto.Field(
        proto.MESSAGE, number=7, message=wrappers.StringValue,
    )
    geo_target_constants = proto.RepeatedField(
        proto.MESSAGE, number=8, message=wrappers.StringValue,
    )
    include_adult_keywords = proto.Field(proto.BOOL, number=10)
    page_token = proto.Field(proto.STRING, number=12)
    page_size = proto.Field(proto.INT32, number=13)
    keyword_plan_network = proto.Field(
        proto.ENUM,
        number=9,
        enum=gage_keyword_plan_network.KeywordPlanNetworkEnum.KeywordPlanNetwork,
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
        url (google.protobuf.wrappers_pb2.StringValue):
            The URL to crawl in order to generate keyword
            ideas.
        keywords (Sequence[google.protobuf.wrappers_pb2.StringValue]):
            Requires at least one keyword.
    """

    url = proto.Field(proto.MESSAGE, number=1, message=wrappers.StringValue,)
    keywords = proto.RepeatedField(
        proto.MESSAGE, number=2, message=wrappers.StringValue,
    )


class KeywordSeed(proto.Message):
    r"""Keyword Seed

    Attributes:
        keywords (Sequence[google.protobuf.wrappers_pb2.StringValue]):
            Requires at least one keyword.
    """

    keywords = proto.RepeatedField(
        proto.MESSAGE, number=1, message=wrappers.StringValue,
    )


class SiteSeed(proto.Message):
    r"""Site Seed

    Attributes:
        site (google.protobuf.wrappers_pb2.StringValue):
            The domain name of the site. If the customer
            requesting the ideas doesn't own the site
            provided only public information is returned.
    """

    site = proto.Field(proto.MESSAGE, number=1, message=wrappers.StringValue,)


class UrlSeed(proto.Message):
    r"""Url Seed

    Attributes:
        url (google.protobuf.wrappers_pb2.StringValue):
            The URL to crawl in order to generate keyword
            ideas.
    """

    url = proto.Field(proto.MESSAGE, number=1, message=wrappers.StringValue,)


class GenerateKeywordIdeaResponse(proto.Message):
    r"""Response message for
    [KeywordPlanIdeaService.GenerateKeywordIdeas][google.ads.googleads.v5.services.KeywordPlanIdeaService.GenerateKeywordIdeas].

    Attributes:
        results (Sequence[google.ads.googleads.v5.services.types.GenerateKeywordIdeaResult]):
            Results of generating keyword ideas.
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
    next_page_token = proto.Field(proto.STRING, number=2)
    total_size = proto.Field(proto.INT64, number=3)


class GenerateKeywordIdeaResult(proto.Message):
    r"""The result of generating keyword ideas.

    Attributes:
        text (google.protobuf.wrappers_pb2.StringValue):
            Text of the keyword idea.
            As in Keyword Plan historical metrics, this text
            may not be an actual keyword, but the canonical
            form of multiple keywords. See
            KeywordPlanKeywordHistoricalMetrics message in
            KeywordPlanService.
        keyword_idea_metrics (google.ads.googleads.v5.common.types.KeywordPlanHistoricalMetrics):
            The historical metrics for the keyword.
    """

    text = proto.Field(proto.MESSAGE, number=2, message=wrappers.StringValue,)
    keyword_idea_metrics = proto.Field(
        proto.MESSAGE,
        number=3,
        message=keyword_plan_common.KeywordPlanHistoricalMetrics,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
