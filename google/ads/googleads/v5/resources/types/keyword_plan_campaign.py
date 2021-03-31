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


from google.ads.googleads.v5.enums.types import (
    keyword_plan_network as gage_keyword_plan_network,
)
from google.protobuf import wrappers_pb2 as wrappers  # type: ignore


__protobuf__ = proto.module(
    package="google.ads.googleads.v5.resources",
    marshal="google.ads.googleads.v5",
    manifest={"KeywordPlanCampaign", "KeywordPlanGeoTarget",},
)


class KeywordPlanCampaign(proto.Message):
    r"""A Keyword Plan campaign.
    Max number of keyword plan campaigns per plan allowed: 1.

    Attributes:
        resource_name (str):
            Immutable. The resource name of the Keyword Plan campaign.
            KeywordPlanCampaign resource names have the form:

            ``customers/{customer_id}/keywordPlanCampaigns/{kp_campaign_id}``
        keyword_plan (google.protobuf.wrappers_pb2.StringValue):
            The keyword plan this campaign belongs to.
        id (google.protobuf.wrappers_pb2.Int64Value):
            Output only. The ID of the Keyword Plan
            campaign.
        name (google.protobuf.wrappers_pb2.StringValue):
            The name of the Keyword Plan campaign.
            This field is required and should not be empty
            when creating Keyword Plan campaigns.
        language_constants (Sequence[google.protobuf.wrappers_pb2.StringValue]):
            The languages targeted for the Keyword Plan
            campaign. Max allowed: 1.
        keyword_plan_network (google.ads.googleads.v5.enums.types.KeywordPlanNetworkEnum.KeywordPlanNetwork):
            Targeting network.
            This field is required and should not be empty
            when creating Keyword Plan campaigns.
        cpc_bid_micros (google.protobuf.wrappers_pb2.Int64Value):
            A default max cpc bid in micros, and in the
            account currency, for all ad groups under the
            campaign.
            This field is required and should not be empty
            when creating Keyword Plan campaigns.
        geo_targets (Sequence[google.ads.googleads.v5.resources.types.KeywordPlanGeoTarget]):
            The geo targets.
            Max number allowed: 20.
    """

    resource_name = proto.Field(proto.STRING, number=1)
    keyword_plan = proto.Field(
        proto.MESSAGE, number=2, message=wrappers.StringValue,
    )
    id = proto.Field(proto.MESSAGE, number=3, message=wrappers.Int64Value,)
    name = proto.Field(proto.MESSAGE, number=4, message=wrappers.StringValue,)
    language_constants = proto.RepeatedField(
        proto.MESSAGE, number=5, message=wrappers.StringValue,
    )
    keyword_plan_network = proto.Field(
        proto.ENUM,
        number=6,
        enum=gage_keyword_plan_network.KeywordPlanNetworkEnum.KeywordPlanNetwork,
    )
    cpc_bid_micros = proto.Field(
        proto.MESSAGE, number=7, message=wrappers.Int64Value,
    )
    geo_targets = proto.RepeatedField(
        proto.MESSAGE, number=8, message="KeywordPlanGeoTarget",
    )


class KeywordPlanGeoTarget(proto.Message):
    r"""A geo target.

    Attributes:
        geo_target_constant (google.protobuf.wrappers_pb2.StringValue):
            Required. The resource name of the geo
            target.
    """

    geo_target_constant = proto.Field(
        proto.MESSAGE, number=1, message=wrappers.StringValue,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
