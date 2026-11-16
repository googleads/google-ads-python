# -*- coding: utf-8 -*-
# Copyright 2026 Google LLC
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

from google.ads.googleads.v26.enums.types import (
    response_content_type as gage_response_content_type,
)
from google.ads.googleads.v26.resources.types import (
    customer_budget_network_setting as gagr_customer_budget_network_setting,
)
import google.protobuf.field_mask_pb2 as field_mask_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.ads.googleads.v26.services",
    marshal="google.ads.googleads.v26",
    manifest={
        "MutateCustomerBudgetNetworkSettingRequest",
        "CustomerBudgetNetworkSettingOperation",
        "MutateCustomerBudgetNetworkSettingResponse",
        "MutateCustomerBudgetNetworkSettingResult",
    },
)


class MutateCustomerBudgetNetworkSettingRequest(proto.Message):
    r"""Request message for
    [CustomerBudgetNetworkSettingService.MutateCustomerBudgetNetworkSetting][google.ads.googleads.v26.services.CustomerBudgetNetworkSettingService.MutateCustomerBudgetNetworkSetting].

    Attributes:
        customer_id (str):
            Required. The ID of the customer whose
            customer budget network setting is being
            modified.
        operation (google.ads.googleads.v26.services.types.CustomerBudgetNetworkSettingOperation):
            Required. The operation to perform on the
            customer budget network setting.
        validate_only (bool):
            If true, the request is validated but not
            executed. Only errors are returned, not results.
        response_content_type (google.ads.googleads.v26.enums.types.ResponseContentTypeEnum.ResponseContentType):
            The response content type setting. Determines
            whether the mutable resource or just the
            resource name should be returned post mutation.
    """

    customer_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    operation: "CustomerBudgetNetworkSettingOperation" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="CustomerBudgetNetworkSettingOperation",
    )
    validate_only: bool = proto.Field(
        proto.BOOL,
        number=3,
    )
    response_content_type: (
        gage_response_content_type.ResponseContentTypeEnum.ResponseContentType
    ) = proto.Field(
        proto.ENUM,
        number=4,
        enum=gage_response_content_type.ResponseContentTypeEnum.ResponseContentType,
    )


class CustomerBudgetNetworkSettingOperation(proto.Message):
    r"""A single operation (create, update) on a customer budget
    network setting.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            FieldMask that determines which resource
            fields are modified in an update.
        create (google.ads.googleads.v26.resources.types.CustomerBudgetNetworkSetting):
            Create operation: No resource name is
            expected for the new setting.

            This field is a member of `oneof`_ ``operation``.
        update (google.ads.googleads.v26.resources.types.CustomerBudgetNetworkSetting):
            Update operation: The customer budget network
            setting is expected to have a valid resource
            name.

            This field is a member of `oneof`_ ``operation``.
    """

    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=4,
        message=field_mask_pb2.FieldMask,
    )
    create: (
        gagr_customer_budget_network_setting.CustomerBudgetNetworkSetting
    ) = proto.Field(
        proto.MESSAGE,
        number=1,
        oneof="operation",
        message=gagr_customer_budget_network_setting.CustomerBudgetNetworkSetting,
    )
    update: (
        gagr_customer_budget_network_setting.CustomerBudgetNetworkSetting
    ) = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="operation",
        message=gagr_customer_budget_network_setting.CustomerBudgetNetworkSetting,
    )


class MutateCustomerBudgetNetworkSettingResponse(proto.Message):
    r"""Response message for customer budget network setting mutate.

    Attributes:
        result (google.ads.googleads.v26.services.types.MutateCustomerBudgetNetworkSettingResult):
            All results for the mutate.
    """

    result: "MutateCustomerBudgetNetworkSettingResult" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="MutateCustomerBudgetNetworkSettingResult",
    )


class MutateCustomerBudgetNetworkSettingResult(proto.Message):
    r"""The result for the customer budget network setting mutate.

    Attributes:
        resource_name (str):
            Returned for successful operations.
        customer_budget_network_setting (google.ads.googleads.v26.resources.types.CustomerBudgetNetworkSetting):
            The mutated customer budget network setting with only
            mutable fields after mutate. The field will only be returned
            when response_content_type is set to "MUTABLE_RESOURCE".
    """

    resource_name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    customer_budget_network_setting: (
        gagr_customer_budget_network_setting.CustomerBudgetNetworkSetting
    ) = proto.Field(
        proto.MESSAGE,
        number=2,
        message=gagr_customer_budget_network_setting.CustomerBudgetNetworkSetting,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
