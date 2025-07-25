# -*- coding: utf-8 -*-
# Copyright 2025 Google LLC
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
from __future__ import annotations

from typing import MutableSequence

import proto  # type: ignore

from google.ads.googleads.v20.enums.types import custom_interest_member_type
from google.ads.googleads.v20.enums.types import custom_interest_status
from google.ads.googleads.v20.enums.types import custom_interest_type


__protobuf__ = proto.module(
    package="google.ads.googleads.v20.resources",
    marshal="google.ads.googleads.v20",
    manifest={
        "CustomInterest",
        "CustomInterestMember",
    },
)


class CustomInterest(proto.Message):
    r"""A custom interest. This is a list of users by interest.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        resource_name (str):
            Immutable. The resource name of the custom interest. Custom
            interest resource names have the form:

            ``customers/{customer_id}/customInterests/{custom_interest_id}``
        id (int):
            Output only. Id of the custom interest.

            This field is a member of `oneof`_ ``_id``.
        status (google.ads.googleads.v20.enums.types.CustomInterestStatusEnum.CustomInterestStatus):
            Status of this custom interest. Indicates
            whether the custom interest is enabled or
            removed.
        name (str):
            Name of the custom interest. It should be
            unique across the same custom affinity audience.
            This field is required for create operations.

            This field is a member of `oneof`_ ``_name``.
        type_ (google.ads.googleads.v20.enums.types.CustomInterestTypeEnum.CustomInterestType):
            Type of the custom interest, CUSTOM_AFFINITY or
            CUSTOM_INTENT. By default the type is set to
            CUSTOM_AFFINITY.
        description (str):
            Description of this custom interest audience.

            This field is a member of `oneof`_ ``_description``.
        members (MutableSequence[google.ads.googleads.v20.resources.types.CustomInterestMember]):
            List of custom interest members that this
            custom interest is composed of. Members can be
            added during CustomInterest creation. If members
            are presented in UPDATE operation, existing
            members will be overridden.
    """

    resource_name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    id: int = proto.Field(
        proto.INT64,
        number=8,
        optional=True,
    )
    status: (
        custom_interest_status.CustomInterestStatusEnum.CustomInterestStatus
    ) = proto.Field(
        proto.ENUM,
        number=3,
        enum=custom_interest_status.CustomInterestStatusEnum.CustomInterestStatus,
    )
    name: str = proto.Field(
        proto.STRING,
        number=9,
        optional=True,
    )
    type_: custom_interest_type.CustomInterestTypeEnum.CustomInterestType = (
        proto.Field(
            proto.ENUM,
            number=5,
            enum=custom_interest_type.CustomInterestTypeEnum.CustomInterestType,
        )
    )
    description: str = proto.Field(
        proto.STRING,
        number=10,
        optional=True,
    )
    members: MutableSequence["CustomInterestMember"] = proto.RepeatedField(
        proto.MESSAGE,
        number=7,
        message="CustomInterestMember",
    )


class CustomInterestMember(proto.Message):
    r"""A member of custom interest audience. A member can be a
    keyword or url. It is immutable, that is, it can only be created
    or removed but not changed.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        member_type (google.ads.googleads.v20.enums.types.CustomInterestMemberTypeEnum.CustomInterestMemberType):
            The type of custom interest member, KEYWORD
            or URL.
        parameter (str):
            Keyword text when member_type is KEYWORD or URL string when
            member_type is URL.

            This field is a member of `oneof`_ ``_parameter``.
    """

    member_type: (
        custom_interest_member_type.CustomInterestMemberTypeEnum.CustomInterestMemberType
    ) = proto.Field(
        proto.ENUM,
        number=1,
        enum=custom_interest_member_type.CustomInterestMemberTypeEnum.CustomInterestMemberType,
    )
    parameter: str = proto.Field(
        proto.STRING,
        number=3,
        optional=True,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
