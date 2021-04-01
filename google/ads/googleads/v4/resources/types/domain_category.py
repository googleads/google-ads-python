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
    package="google.ads.googleads.v4.resources",
    marshal="google.ads.googleads.v4",
    manifest={"DomainCategory",},
)


class DomainCategory(proto.Message):
    r"""A category generated automatically by crawling a domain. If a
    campaign uses the DynamicSearchAdsSetting, then domain
    categories will be generated for the domain. The categories can
    be targeted using WebpageConditionInfo. See:
    https://support.google.com/google-ads/answer/2471185

    Attributes:
        resource_name (str):
            Output only. The resource name of the domain category.
            Domain category resource names have the form:

            ``customers/{customer_id}/domainCategories/{campaign_id}~{category_base64}~{language_code}``
        campaign (google.protobuf.wrappers_pb2.StringValue):
            Output only. The campaign this category is
            recommended for.
        category (google.protobuf.wrappers_pb2.StringValue):
            Output only. Recommended category for the
            website domain. e.g. if you have a website about
            electronics, the categories could be "cameras",
            "televisions", etc.
        language_code (google.protobuf.wrappers_pb2.StringValue):
            Output only. The language code specifying the
            language of the website. e.g. "en" for English.
            The language can be specified in the
            DynamicSearchAdsSetting required for dynamic
            search ads. This is the language of the pages
            from your website that you want Google Ads to
            find, create ads for, and match searches with.
        domain (google.protobuf.wrappers_pb2.StringValue):
            Output only. The domain for the website. The
            domain can be specified in the
            DynamicSearchAdsSetting required for dynamic
            search ads.
        coverage_fraction (google.protobuf.wrappers_pb2.DoubleValue):
            Output only. Fraction of pages on your site
            that this category matches.
        category_rank (google.protobuf.wrappers_pb2.Int64Value):
            Output only. The position of this category in
            the set of categories. Lower numbers indicate a
            better match for the domain. null indicates not
            recommended.
        has_children (google.protobuf.wrappers_pb2.BoolValue):
            Output only. Indicates whether this category
            has sub-categories.
        recommended_cpc_bid_micros (google.protobuf.wrappers_pb2.Int64Value):
            Output only. The recommended cost per click
            for the category.
    """

    resource_name = proto.Field(proto.STRING, number=1)
    campaign = proto.Field(
        proto.MESSAGE, number=2, message=wrappers.StringValue,
    )
    category = proto.Field(
        proto.MESSAGE, number=3, message=wrappers.StringValue,
    )
    language_code = proto.Field(
        proto.MESSAGE, number=4, message=wrappers.StringValue,
    )
    domain = proto.Field(proto.MESSAGE, number=5, message=wrappers.StringValue,)
    coverage_fraction = proto.Field(
        proto.MESSAGE, number=6, message=wrappers.DoubleValue,
    )
    category_rank = proto.Field(
        proto.MESSAGE, number=7, message=wrappers.Int64Value,
    )
    has_children = proto.Field(
        proto.MESSAGE, number=8, message=wrappers.BoolValue,
    )
    recommended_cpc_bid_micros = proto.Field(
        proto.MESSAGE, number=9, message=wrappers.Int64Value,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
