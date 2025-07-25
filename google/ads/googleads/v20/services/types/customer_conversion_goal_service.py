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

from google.ads.googleads.v20.resources.types import customer_conversion_goal
from google.protobuf import field_mask_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.ads.googleads.v20.services",
    marshal="google.ads.googleads.v20",
    manifest={
        "MutateCustomerConversionGoalsRequest",
        "CustomerConversionGoalOperation",
        "MutateCustomerConversionGoalsResponse",
        "MutateCustomerConversionGoalResult",
    },
)


class MutateCustomerConversionGoalsRequest(proto.Message):
    r"""Request message for
    [CustomerConversionGoalService.MutateCustomerConversionGoals][google.ads.googleads.v20.services.CustomerConversionGoalService.MutateCustomerConversionGoals].

    Attributes:
        customer_id (str):
            Required. The ID of the customer whose
            customer conversion goals are being modified.
        operations (MutableSequence[google.ads.googleads.v20.services.types.CustomerConversionGoalOperation]):
            Required. The list of operations to perform
            on individual customer conversion goal.
        validate_only (bool):
            If true, the request is validated but not
            executed. Only errors are returned, not results.
    """

    customer_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    operations: MutableSequence["CustomerConversionGoalOperation"] = (
        proto.RepeatedField(
            proto.MESSAGE,
            number=2,
            message="CustomerConversionGoalOperation",
        )
    )
    validate_only: bool = proto.Field(
        proto.BOOL,
        number=3,
    )


class CustomerConversionGoalOperation(proto.Message):
    r"""A single operation (update) on a customer conversion goal.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            FieldMask that determines which resource
            fields are modified in an update.
        update (google.ads.googleads.v20.resources.types.CustomerConversionGoal):
            Update operation: The customer conversion
            goal is expected to have a valid resource name.

            This field is a member of `oneof`_ ``operation``.
    """

    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )
    update: customer_conversion_goal.CustomerConversionGoal = proto.Field(
        proto.MESSAGE,
        number=1,
        oneof="operation",
        message=customer_conversion_goal.CustomerConversionGoal,
    )


class MutateCustomerConversionGoalsResponse(proto.Message):
    r"""Response message for a customer conversion goal mutate.

    Attributes:
        results (MutableSequence[google.ads.googleads.v20.services.types.MutateCustomerConversionGoalResult]):
            All results for the mutate.
    """

    results: MutableSequence["MutateCustomerConversionGoalResult"] = (
        proto.RepeatedField(
            proto.MESSAGE,
            number=1,
            message="MutateCustomerConversionGoalResult",
        )
    )


class MutateCustomerConversionGoalResult(proto.Message):
    r"""The result for the customer conversion goal mutate.

    Attributes:
        resource_name (str):
            Returned for successful operations.
    """

    resource_name: str = proto.Field(
        proto.STRING,
        number=1,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
