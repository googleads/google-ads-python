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

from google.ads.googleads.v20.resources.types import customer_label
from google.rpc import status_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.ads.googleads.v20.services",
    marshal="google.ads.googleads.v20",
    manifest={
        "MutateCustomerLabelsRequest",
        "CustomerLabelOperation",
        "MutateCustomerLabelsResponse",
        "MutateCustomerLabelResult",
    },
)


class MutateCustomerLabelsRequest(proto.Message):
    r"""Request message for
    [CustomerLabelService.MutateCustomerLabels][google.ads.googleads.v20.services.CustomerLabelService.MutateCustomerLabels].

    Attributes:
        customer_id (str):
            Required. ID of the customer whose
            customer-label relationships are being modified.
        operations (MutableSequence[google.ads.googleads.v20.services.types.CustomerLabelOperation]):
            Required. The list of operations to perform
            on customer-label relationships.
        partial_failure (bool):
            If true, successful operations will be
            carried out and invalid operations will return
            errors. If false, all operations will be carried
            out in one transaction if and only if they are
            all valid. Default is false.
        validate_only (bool):
            If true, the request is validated but not
            executed. Only errors are returned, not results.
    """

    customer_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    operations: MutableSequence["CustomerLabelOperation"] = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message="CustomerLabelOperation",
    )
    partial_failure: bool = proto.Field(
        proto.BOOL,
        number=3,
    )
    validate_only: bool = proto.Field(
        proto.BOOL,
        number=4,
    )


class CustomerLabelOperation(proto.Message):
    r"""A single operation (create, remove) on a customer-label
    relationship.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        create (google.ads.googleads.v20.resources.types.CustomerLabel):
            Create operation: No resource name is
            expected for the new customer-label
            relationship.

            This field is a member of `oneof`_ ``operation``.
        remove (str):
            Remove operation: A resource name for the customer-label
            relationship being removed, in this format:

            ``customers/{customer_id}/customerLabels/{label_id}``

            This field is a member of `oneof`_ ``operation``.
    """

    create: customer_label.CustomerLabel = proto.Field(
        proto.MESSAGE,
        number=1,
        oneof="operation",
        message=customer_label.CustomerLabel,
    )
    remove: str = proto.Field(
        proto.STRING,
        number=2,
        oneof="operation",
    )


class MutateCustomerLabelsResponse(proto.Message):
    r"""Response message for a customer labels mutate.

    Attributes:
        partial_failure_error (google.rpc.status_pb2.Status):
            Errors that pertain to operation failures in the partial
            failure mode. Returned only when partial_failure = true and
            all errors occur inside the operations. If any errors occur
            outside the operations (for example, auth errors), we return
            an RPC level error.
        results (MutableSequence[google.ads.googleads.v20.services.types.MutateCustomerLabelResult]):
            All results for the mutate.
    """

    partial_failure_error: status_pb2.Status = proto.Field(
        proto.MESSAGE,
        number=3,
        message=status_pb2.Status,
    )
    results: MutableSequence["MutateCustomerLabelResult"] = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message="MutateCustomerLabelResult",
    )


class MutateCustomerLabelResult(proto.Message):
    r"""The result for a customer label mutate.

    Attributes:
        resource_name (str):
            Returned for successful operations.
    """

    resource_name: str = proto.Field(
        proto.STRING,
        number=1,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
