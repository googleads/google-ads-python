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


from google.ads.googleads.v4.enums.types import keyword_match_type
from google.protobuf import wrappers_pb2 as wrappers  # type: ignore


__protobuf__ = proto.module(
    package="google.ads.googleads.v4.resources",
    marshal="google.ads.googleads.v4",
    manifest={"KeywordPlanCampaignKeyword",},
)


class KeywordPlanCampaignKeyword(proto.Message):
    r"""A Keyword Plan Campaign keyword.
    Only negative keywords are supported for Campaign Keyword.

    Attributes:
        resource_name (str):
            Immutable. The resource name of the Keyword Plan Campaign
            keyword. KeywordPlanCampaignKeyword resource names have the
            form:

            ``customers/{customer_id}/keywordPlanCampaignKeywords/{kp_campaign_keyword_id}``
        keyword_plan_campaign (google.protobuf.wrappers_pb2.StringValue):
            The Keyword Plan campaign to which this
            negative keyword belongs.
        id (google.protobuf.wrappers_pb2.Int64Value):
            Output only. The ID of the Keyword Plan
            negative keyword.
        text (google.protobuf.wrappers_pb2.StringValue):
            The keyword text.
        match_type (google.ads.googleads.v4.enums.types.KeywordMatchTypeEnum.KeywordMatchType):
            The keyword match type.
        negative (google.protobuf.wrappers_pb2.BoolValue):
            Immutable. If true, the keyword is negative.
            Must be set to true. Only negative campaign
            keywords are supported.
    """

    resource_name = proto.Field(proto.STRING, number=1)
    keyword_plan_campaign = proto.Field(
        proto.MESSAGE, number=2, message=wrappers.StringValue,
    )
    id = proto.Field(proto.MESSAGE, number=3, message=wrappers.Int64Value,)
    text = proto.Field(proto.MESSAGE, number=4, message=wrappers.StringValue,)
    match_type = proto.Field(
        proto.ENUM,
        number=5,
        enum=keyword_match_type.KeywordMatchTypeEnum.KeywordMatchType,
    )
    negative = proto.Field(proto.MESSAGE, number=7, message=wrappers.BoolValue,)


__all__ = tuple(sorted(__protobuf__.manifest))
