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


from google.ads.googleads.v4.enums.types import (
    operating_system_version_operator_type,
)
from google.protobuf import wrappers_pb2 as wrappers  # type: ignore


__protobuf__ = proto.module(
    package="google.ads.googleads.v4.resources",
    marshal="google.ads.googleads.v4",
    manifest={"OperatingSystemVersionConstant",},
)


class OperatingSystemVersionConstant(proto.Message):
    r"""A mobile operating system version or a range of versions, depending
    on ``operator_type``. List of available mobile platforms at
    https://developers.google.com/adwords/api/docs/appendix/codes-formats#mobile-platforms

    Attributes:
        resource_name (str):
            Output only. The resource name of the operating system
            version constant. Operating system version constant resource
            names have the form:

            ``operatingSystemVersionConstants/{criterion_id}``
        id (google.protobuf.wrappers_pb2.Int64Value):
            Output only. The ID of the operating system
            version.
        name (google.protobuf.wrappers_pb2.StringValue):
            Output only. Name of the operating system.
        os_major_version (google.protobuf.wrappers_pb2.Int32Value):
            Output only. The OS Major Version number.
        os_minor_version (google.protobuf.wrappers_pb2.Int32Value):
            Output only. The OS Minor Version number.
        operator_type (google.ads.googleads.v4.enums.types.OperatingSystemVersionOperatorTypeEnum.OperatingSystemVersionOperatorType):
            Output only. Determines whether this constant
            represents a single version or a range of
            versions.
    """

    resource_name = proto.Field(proto.STRING, number=1)
    id = proto.Field(proto.MESSAGE, number=2, message=wrappers.Int64Value,)
    name = proto.Field(proto.MESSAGE, number=3, message=wrappers.StringValue,)
    os_major_version = proto.Field(
        proto.MESSAGE, number=4, message=wrappers.Int32Value,
    )
    os_minor_version = proto.Field(
        proto.MESSAGE, number=5, message=wrappers.Int32Value,
    )
    operator_type = proto.Field(
        proto.ENUM,
        number=6,
        enum=operating_system_version_operator_type.OperatingSystemVersionOperatorTypeEnum.OperatingSystemVersionOperatorType,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
