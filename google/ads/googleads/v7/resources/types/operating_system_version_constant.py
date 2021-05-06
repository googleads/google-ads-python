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

from google.ads.googleads.v7.enums.types import (
    operating_system_version_operator_type,
)


__protobuf__ = proto.module(
    package="google.ads.googleads.v7.resources",
    marshal="google.ads.googleads.v7",
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
        id (int):
            Output only. The ID of the operating system
            version.
        name (str):
            Output only. Name of the operating system.
        os_major_version (int):
            Output only. The OS Major Version number.
        os_minor_version (int):
            Output only. The OS Minor Version number.
        operator_type (google.ads.googleads.v7.enums.types.OperatingSystemVersionOperatorTypeEnum.OperatingSystemVersionOperatorType):
            Output only. Determines whether this constant
            represents a single version or a range of
            versions.
    """

    resource_name = proto.Field(proto.STRING, number=1,)
    id = proto.Field(proto.INT64, number=7, optional=True,)
    name = proto.Field(proto.STRING, number=8, optional=True,)
    os_major_version = proto.Field(proto.INT32, number=9, optional=True,)
    os_minor_version = proto.Field(proto.INT32, number=10, optional=True,)
    operator_type = proto.Field(
        proto.ENUM,
        number=6,
        enum=operating_system_version_operator_type.OperatingSystemVersionOperatorTypeEnum.OperatingSystemVersionOperatorType,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
