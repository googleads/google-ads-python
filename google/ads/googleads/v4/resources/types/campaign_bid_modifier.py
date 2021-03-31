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
from google.protobuf import wrappers_pb2 as wrappers  # type: ignore


__protobuf__ = proto.module(
    package="google.ads.googleads.v4.resources",
    marshal="google.ads.googleads.v4",
    manifest={"CampaignBidModifier",},
)


class CampaignBidModifier(proto.Message):
    r"""Represents a bid-modifiable only criterion at the campaign
    level.

    Attributes:
        resource_name (str):
            Immutable. The resource name of the campaign bid modifier.
            Campaign bid modifier resource names have the form:

            ``customers/{customer_id}/campaignBidModifiers/{campaign_id}~{criterion_id}``
        campaign (google.protobuf.wrappers_pb2.StringValue):
            Output only. The campaign to which this
            criterion belongs.
        criterion_id (google.protobuf.wrappers_pb2.Int64Value):
            Output only. The ID of the criterion to bid
            modify.
            This field is ignored for mutates.
        bid_modifier (google.protobuf.wrappers_pb2.DoubleValue):
            The modifier for the bid when the criterion
            matches.
        interaction_type (google.ads.googleads.v4.common.types.InteractionTypeInfo):
            Immutable. Criterion for interaction type.
            Only supported for search campaigns.
    """

    resource_name = proto.Field(proto.STRING, number=1)
    campaign = proto.Field(
        proto.MESSAGE, number=2, message=wrappers.StringValue,
    )
    criterion_id = proto.Field(
        proto.MESSAGE, number=3, message=wrappers.Int64Value,
    )
    bid_modifier = proto.Field(
        proto.MESSAGE, number=4, message=wrappers.DoubleValue,
    )
    interaction_type = proto.Field(
        proto.MESSAGE,
        number=5,
        oneof="criterion",
        message=criteria.InteractionTypeInfo,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
