# -*- coding: utf-8 -*-
# Copyright 2024 Google LLC
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

from google.ads.googleads.v19.enums.types import (
    response_content_type as gage_response_content_type,
)
from google.ads.googleads.v19.resources.types import (
    customer_asset_set as gagr_customer_asset_set,
)
from google.rpc import status_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.ads.googleads.v19.services",
    marshal="google.ads.googleads.v19",
    manifest={
        "MutateCustomerAssetSetsRequest",
        "CustomerAssetSetOperation",
        "MutateCustomerAssetSetsResponse",
        "MutateCustomerAssetSetResult",
    },
)


class MutateCustomerAssetSetsRequest(proto.Message):
    r"""Request message for
    [CustomerAssetSetService.MutateCustomerAssetSets][google.ads.googleads.v19.services.CustomerAssetSetService.MutateCustomerAssetSets].

    Attributes:
        customer_id (str):
            Required. The ID of the customer whose
            customer asset sets are being modified.
        operations (MutableSequence[google.ads.googleads.v19.services.types.CustomerAssetSetOperation]):
            Required. The list of operations to perform
            on individual customer asset sets.
        partial_failure (bool):
            If true, successful operations will be
            carried out and invalid operations will return
            errors. If false, all operations will be carried
            out in one transaction if and only if they are
            all valid. Default is false.
        validate_only (bool):
            If true, the request is validated but not
            executed. Only errors are returned, not results.
        response_content_type (google.ads.googleads.v19.enums.types.ResponseContentTypeEnum.ResponseContentType):
            The response content type setting. Determines
            whether the mutable resource or just the
            resource name should be returned post mutation.
    """

    customer_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    operations: MutableSequence["CustomerAssetSetOperation"] = (
        proto.RepeatedField(
            proto.MESSAGE,
            number=2,
            message="CustomerAssetSetOperation",
        )
    )
    partial_failure: bool = proto.Field(
        proto.BOOL,
        number=3,
    )
    validate_only: bool = proto.Field(
        proto.BOOL,
        number=4,
    )
    response_content_type: (
        gage_response_content_type.ResponseContentTypeEnum.ResponseContentType
    ) = proto.Field(
        proto.ENUM,
        number=5,
        enum=gage_response_content_type.ResponseContentTypeEnum.ResponseContentType,
    )


class CustomerAssetSetOperation(proto.Message):
    r"""A single operation (create, remove) on a customer asset set.
    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        create (google.ads.googleads.v19.resources.types.CustomerAssetSet):
            Create operation: No resource name is
            expected for the new customer asset set.

            This field is a member of `oneof`_ ``operation``.
        remove (str):
            Remove operation: A resource name for the removed customer
            asset set is expected, in this format:
            ``customers/{customer_id}/customerAssetSets/{asset_set_id}``

            This field is a member of `oneof`_ ``operation``.
    """

    create: gagr_customer_asset_set.CustomerAssetSet = proto.Field(
        proto.MESSAGE,
        number=1,
        oneof="operation",
        message=gagr_customer_asset_set.CustomerAssetSet,
    )
    remove: str = proto.Field(
        proto.STRING,
        number=2,
        oneof="operation",
    )


class MutateCustomerAssetSetsResponse(proto.Message):
    r"""Response message for a customer asset set mutate.
    Attributes:
        results (MutableSequence[google.ads.googleads.v19.services.types.MutateCustomerAssetSetResult]):
            All results for the mutate.
        partial_failure_error (google.rpc.status_pb2.Status):
            Errors that pertain to operation failures in the partial
            failure mode. Returned only when partial_failure = true and
            all errors occur inside the operations. If any errors occur
            outside the operations (e.g. auth errors), we return an RPC
            level error.
    """

    results: MutableSequence["MutateCustomerAssetSetResult"] = (
        proto.RepeatedField(
            proto.MESSAGE,
            number=1,
            message="MutateCustomerAssetSetResult",
        )
    )
    partial_failure_error: status_pb2.Status = proto.Field(
        proto.MESSAGE,
        number=2,
        message=status_pb2.Status,
    )


class MutateCustomerAssetSetResult(proto.Message):
    r"""The result for the customer asset set mutate.
    Attributes:
        resource_name (str):
            Returned for successful operations.
        customer_asset_set (google.ads.googleads.v19.resources.types.CustomerAssetSet):
            The mutated customer asset set with only mutable fields
            after mutate. The field will only be returned when
            response_content_type is set to "MUTABLE_RESOURCE".
    """

    resource_name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    customer_asset_set: gagr_customer_asset_set.CustomerAssetSet = proto.Field(
        proto.MESSAGE,
        number=2,
        message=gagr_customer_asset_set.CustomerAssetSet,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
