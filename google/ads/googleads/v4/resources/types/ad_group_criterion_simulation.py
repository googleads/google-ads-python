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


from google.ads.googleads.v4.common.types import simulation
from google.ads.googleads.v4.enums.types import simulation_modification_method
from google.ads.googleads.v4.enums.types import simulation_type
from google.protobuf import wrappers_pb2 as wrappers  # type: ignore


__protobuf__ = proto.module(
    package="google.ads.googleads.v4.resources",
    marshal="google.ads.googleads.v4",
    manifest={"AdGroupCriterionSimulation",},
)


class AdGroupCriterionSimulation(proto.Message):
    r"""An ad group criterion simulation. Supported combinations of
    advertising channel type, criterion type, simulation type, and
    simulation modification method are detailed below respectively.
    Hotel AdGroupCriterion simulation operations starting in V5.

    1. DISPLAY - KEYWORD - CPC_BID - UNIFORM
    2. SEARCH - KEYWORD - CPC_BID - UNIFORM
    3. SHOPPING - LISTING_GROUP - CPC_BID - UNIFORM
    4. HOTEL - LISTING_GROUP - CPC_BID - UNIFORM
    5. HOTEL - LISTING_GROUP - PERCENT_CPC_BID - UNIFORM

    Attributes:
        resource_name (str):
            Output only. The resource name of the ad group criterion
            simulation. Ad group criterion simulation resource names
            have the form:

            ``customers/{customer_id}/adGroupCriterionSimulations/{ad_group_id}~{criterion_id}~{type}~{modification_method}~{start_date}~{end_date}``
        ad_group_id (google.protobuf.wrappers_pb2.Int64Value):
            Output only. AdGroup ID of the simulation.
        criterion_id (google.protobuf.wrappers_pb2.Int64Value):
            Output only. Criterion ID of the simulation.
        type_ (google.ads.googleads.v4.enums.types.SimulationTypeEnum.SimulationType):
            Output only. The field that the simulation
            modifies.
        modification_method (google.ads.googleads.v4.enums.types.SimulationModificationMethodEnum.SimulationModificationMethod):
            Output only. How the simulation modifies the
            field.
        start_date (google.protobuf.wrappers_pb2.StringValue):
            Output only. First day on which the
            simulation is based, in YYYY-MM-DD format.
        end_date (google.protobuf.wrappers_pb2.StringValue):
            Output only. Last day on which the simulation
            is based, in YYYY-MM-DD format.
        cpc_bid_point_list (google.ads.googleads.v4.common.types.CpcBidSimulationPointList):
            Output only. Simulation points if the simulation type is
            CPC_BID.
    """

    resource_name = proto.Field(proto.STRING, number=1)
    ad_group_id = proto.Field(
        proto.MESSAGE, number=2, message=wrappers.Int64Value,
    )
    criterion_id = proto.Field(
        proto.MESSAGE, number=3, message=wrappers.Int64Value,
    )
    type_ = proto.Field(
        proto.ENUM,
        number=4,
        enum=simulation_type.SimulationTypeEnum.SimulationType,
    )
    modification_method = proto.Field(
        proto.ENUM,
        number=5,
        enum=simulation_modification_method.SimulationModificationMethodEnum.SimulationModificationMethod,
    )
    start_date = proto.Field(
        proto.MESSAGE, number=6, message=wrappers.StringValue,
    )
    end_date = proto.Field(
        proto.MESSAGE, number=7, message=wrappers.StringValue,
    )
    cpc_bid_point_list = proto.Field(
        proto.MESSAGE,
        number=8,
        oneof="point_list",
        message=simulation.CpcBidSimulationPointList,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
