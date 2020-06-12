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


from google.ads.googleads.v4.enums.types import geo_target_constant_status
from google.protobuf import wrappers_pb2 as wrappers  # type: ignore


__protobuf__ = proto.module(
    package="google.ads.googleads.v4.resources",
    marshal="google.ads.googleads.v4",
    manifest={"GeoTargetConstant",},
)


class GeoTargetConstant(proto.Message):
    r"""A geo target constant.

    Attributes:
        resource_name (str):
            Output only. The resource name of the geo target constant.
            Geo target constant resource names have the form:

            ``geoTargetConstants/{geo_target_constant_id}``
        id (google.protobuf.wrappers_pb2.Int64Value):
            Output only. The ID of the geo target
            constant.
        name (google.protobuf.wrappers_pb2.StringValue):
            Output only. Geo target constant English
            name.
        country_code (google.protobuf.wrappers_pb2.StringValue):
            Output only. The ISO-3166-1 alpha-2 country
            code that is associated with the target.
        target_type (google.protobuf.wrappers_pb2.StringValue):
            Output only. Geo target constant target type.
        status (google.ads.googleads.v4.enums.types.GeoTargetConstantStatusEnum.GeoTargetConstantStatus):
            Output only. Geo target constant status.
        canonical_name (google.protobuf.wrappers_pb2.StringValue):
            Output only. The fully qualified English
            name, consisting of the target's name and that
            of its parent and country.
    """

    resource_name = proto.Field(proto.STRING, number=1)
    id = proto.Field(proto.MESSAGE, number=3, message=wrappers.Int64Value,)
    name = proto.Field(proto.MESSAGE, number=4, message=wrappers.StringValue,)
    country_code = proto.Field(
        proto.MESSAGE, number=5, message=wrappers.StringValue,
    )
    target_type = proto.Field(
        proto.MESSAGE, number=6, message=wrappers.StringValue,
    )
    status = proto.Field(
        proto.ENUM,
        number=7,
        enum=geo_target_constant_status.GeoTargetConstantStatusEnum.GeoTargetConstantStatus,
    )
    canonical_name = proto.Field(
        proto.MESSAGE, number=8, message=wrappers.StringValue,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
