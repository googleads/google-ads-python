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
    package="google.ads.googleads.v5.resources",
    marshal="google.ads.googleads.v5",
    manifest={"KeywordPlanAdGroup",},
)


class KeywordPlanAdGroup(proto.Message):
    r"""A Keyword Planner ad group.
    Max number of keyword plan ad groups per plan: 200.

    Attributes:
        resource_name (str):
            Immutable. The resource name of the Keyword Planner ad
            group. KeywordPlanAdGroup resource names have the form:

            ``customers/{customer_id}/keywordPlanAdGroups/{kp_ad_group_id}``
        keyword_plan_campaign (google.protobuf.wrappers_pb2.StringValue):
            The keyword plan campaign to which this ad
            group belongs.
        id (google.protobuf.wrappers_pb2.Int64Value):
            Output only. The ID of the keyword plan ad
            group.
        name (google.protobuf.wrappers_pb2.StringValue):
            The name of the keyword plan ad group.
            This field is required and should not be empty
            when creating keyword plan ad group.
        cpc_bid_micros (google.protobuf.wrappers_pb2.Int64Value):
            A default ad group max cpc bid in micros in
            account currency for all biddable keywords under
            the keyword plan ad group. If not set, will
            inherit from parent campaign.
    """

    resource_name = proto.Field(proto.STRING, number=1)
    keyword_plan_campaign = proto.Field(
        proto.MESSAGE, number=2, message=wrappers.StringValue,
    )
    id = proto.Field(proto.MESSAGE, number=3, message=wrappers.Int64Value,)
    name = proto.Field(proto.MESSAGE, number=4, message=wrappers.StringValue,)
    cpc_bid_micros = proto.Field(
        proto.MESSAGE, number=5, message=wrappers.Int64Value,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
