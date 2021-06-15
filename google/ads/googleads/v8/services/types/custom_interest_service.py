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

from google.ads.googleads.v8.resources.types import custom_interest
from google.protobuf import field_mask_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.ads.googleads.v8.services",
    marshal="google.ads.googleads.v8",
    manifest={
        "GetCustomInterestRequest",
        "MutateCustomInterestsRequest",
        "CustomInterestOperation",
        "MutateCustomInterestsResponse",
        "MutateCustomInterestResult",
    },
)


class GetCustomInterestRequest(proto.Message):
    r"""Request message for
    [CustomInterestService.GetCustomInterest][google.ads.googleads.v8.services.CustomInterestService.GetCustomInterest].

    Attributes:
        resource_name (str):
            Required. The resource name of the custom
            interest to fetch.
    """

    resource_name = proto.Field(proto.STRING, number=1,)


class MutateCustomInterestsRequest(proto.Message):
    r"""Request message for
    [CustomInterestService.MutateCustomInterests][google.ads.googleads.v8.services.CustomInterestService.MutateCustomInterests].

    Attributes:
        customer_id (str):
            Required. The ID of the customer whose custom
            interests are being modified.
        operations (Sequence[google.ads.googleads.v8.services.types.CustomInterestOperation]):
            Required. The list of operations to perform
            on individual custom interests.
        validate_only (bool):
            If true, the request is validated but not
            executed. Only errors are returned, not results.
    """

    customer_id = proto.Field(proto.STRING, number=1,)
    operations = proto.RepeatedField(
        proto.MESSAGE, number=2, message="CustomInterestOperation",
    )
    validate_only = proto.Field(proto.BOOL, number=4,)


class CustomInterestOperation(proto.Message):
    r"""A single operation (create, update) on a custom interest.
    Attributes:
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            FieldMask that determines which resource
            fields are modified in an update.
        create (google.ads.googleads.v8.resources.types.CustomInterest):
            Create operation: No resource name is
            expected for the new custom interest.
        update (google.ads.googleads.v8.resources.types.CustomInterest):
            Update operation: The custom interest is
            expected to have a valid resource name.
    """

    update_mask = proto.Field(
        proto.MESSAGE, number=4, message=field_mask_pb2.FieldMask,
    )
    create = proto.Field(
        proto.MESSAGE,
        number=1,
        oneof="operation",
        message=custom_interest.CustomInterest,
    )
    update = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="operation",
        message=custom_interest.CustomInterest,
    )


class MutateCustomInterestsResponse(proto.Message):
    r"""Response message for custom interest mutate.
    Attributes:
        results (Sequence[google.ads.googleads.v8.services.types.MutateCustomInterestResult]):
            All results for the mutate.
    """

    results = proto.RepeatedField(
        proto.MESSAGE, number=2, message="MutateCustomInterestResult",
    )


class MutateCustomInterestResult(proto.Message):
    r"""The result for the custom interest mutate.
    Attributes:
        resource_name (str):
            Returned for successful operations.
    """

    resource_name = proto.Field(proto.STRING, number=1,)


__all__ = tuple(sorted(__protobuf__.manifest))
