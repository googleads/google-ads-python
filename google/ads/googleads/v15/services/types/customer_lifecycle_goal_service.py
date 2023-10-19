# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
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


import proto  # type: ignore

from google.ads.googleads.v15.resources.types import customer_lifecycle_goal
from google.protobuf import field_mask_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.ads.googleads.v15.services",
    marshal="google.ads.googleads.v15",
    manifest={
        "ConfigureCustomerLifecycleGoalsRequest",
        "CustomerLifecycleGoalOperation",
        "ConfigureCustomerLifecycleGoalsResponse",
        "ConfigureCustomerLifecycleGoalsResult",
    },
)


class ConfigureCustomerLifecycleGoalsRequest(proto.Message):
    r"""Request message for
    [CustomerLifecycleService.configureCustomerLifecycleGoals][].

    Attributes:
        customer_id (str):
            Required. The ID of the customer performing
            the upload.
        operation (google.ads.googleads.v15.services.types.CustomerLifecycleGoalOperation):
            Required. The operation to perform customer
            lifecycle goal update.
        validate_only (bool):
            Optional. If true, the request is validated
            but not executed. Only errors are returned, not
            results.
    """

    customer_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    operation: "CustomerLifecycleGoalOperation" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="CustomerLifecycleGoalOperation",
    )
    validate_only: bool = proto.Field(
        proto.BOOL,
        number=3,
    )


class CustomerLifecycleGoalOperation(proto.Message):
    r"""A single operation on a customer lifecycle goal.
    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            Optional. FieldMask that determines which
            resource fields are modified in an update.
        create (google.ads.googleads.v15.resources.types.CustomerLifecycleGoal):
            Create operation: to create a new customer
            lifecycle goal or update an existing customer
            lifecycle goal. When creating a new customer
            lifecycle goal, all required fields needs to be
            set. Resource name and field mask needs to be
            empty. When updating an existing customer
            lifecycle goal, resource name and field mask
            need to be set. Partial update based on field
            mask is supported when updating an existing
            customer lifecycle goal.

            This field is a member of `oneof`_ ``operation``.
    """

    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=2,
        message=field_mask_pb2.FieldMask,
    )
    create: customer_lifecycle_goal.CustomerLifecycleGoal = proto.Field(
        proto.MESSAGE,
        number=1,
        oneof="operation",
        message=customer_lifecycle_goal.CustomerLifecycleGoal,
    )


class ConfigureCustomerLifecycleGoalsResponse(proto.Message):
    r"""Response message for
    [CustomerLifecycleService.configureCustomerLifecycleGoals][].

    Attributes:
        result (google.ads.googleads.v15.services.types.ConfigureCustomerLifecycleGoalsResult):
            result for the customer lifecycle goal
            configuration.
    """

    result: "ConfigureCustomerLifecycleGoalsResult" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="ConfigureCustomerLifecycleGoalsResult",
    )


class ConfigureCustomerLifecycleGoalsResult(proto.Message):
    r"""The result for the customer lifecycle goal configuration.
    Attributes:
        resource_name (str):
            Returned for the successful operation.
    """

    resource_name: str = proto.Field(
        proto.STRING,
        number=1,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
