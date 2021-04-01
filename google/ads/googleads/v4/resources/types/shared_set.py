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


from google.ads.googleads.v4.enums.types import shared_set_status
from google.ads.googleads.v4.enums.types import shared_set_type
from google.protobuf import wrappers_pb2 as wrappers  # type: ignore


__protobuf__ = proto.module(
    package="google.ads.googleads.v4.resources",
    marshal="google.ads.googleads.v4",
    manifest={"SharedSet",},
)


class SharedSet(proto.Message):
    r"""SharedSets are used for sharing criterion exclusions across
    multiple campaigns.

    Attributes:
        resource_name (str):
            Immutable. The resource name of the shared set. Shared set
            resource names have the form:

            ``customers/{customer_id}/sharedSets/{shared_set_id}``
        id (google.protobuf.wrappers_pb2.Int64Value):
            Output only. The ID of this shared set. Read
            only.
        type_ (google.ads.googleads.v4.enums.types.SharedSetTypeEnum.SharedSetType):
            Immutable. The type of this shared set: each
            shared set holds only a single kind of resource.
            Required. Immutable.
        name (google.protobuf.wrappers_pb2.StringValue):
            The name of this shared set. Required.
            Shared Sets must have names that are unique
            among active shared sets of the same type.
            The length of this string should be between 1
            and 255 UTF-8 bytes, inclusive.
        status (google.ads.googleads.v4.enums.types.SharedSetStatusEnum.SharedSetStatus):
            Output only. The status of this shared set.
            Read only.
        member_count (google.protobuf.wrappers_pb2.Int64Value):
            Output only. The number of shared criteria
            within this shared set. Read only.
        reference_count (google.protobuf.wrappers_pb2.Int64Value):
            Output only. The number of campaigns
            associated with this shared set. Read only.
    """

    resource_name = proto.Field(proto.STRING, number=1)
    id = proto.Field(proto.MESSAGE, number=2, message=wrappers.Int64Value,)
    type_ = proto.Field(
        proto.ENUM,
        number=3,
        enum=shared_set_type.SharedSetTypeEnum.SharedSetType,
    )
    name = proto.Field(proto.MESSAGE, number=4, message=wrappers.StringValue,)
    status = proto.Field(
        proto.ENUM,
        number=5,
        enum=shared_set_status.SharedSetStatusEnum.SharedSetStatus,
    )
    member_count = proto.Field(
        proto.MESSAGE, number=6, message=wrappers.Int64Value,
    )
    reference_count = proto.Field(
        proto.MESSAGE, number=7, message=wrappers.Int64Value,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
