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


from google.ads.googleads.v4.resources.types import customer_negative_criterion
from google.rpc import status_pb2 as status  # type: ignore


__protobuf__ = proto.module(
    package="google.ads.googleads.v4.services",
    marshal="google.ads.googleads.v4",
    manifest={
        "GetCustomerNegativeCriterionRequest",
        "MutateCustomerNegativeCriteriaRequest",
        "CustomerNegativeCriterionOperation",
        "MutateCustomerNegativeCriteriaResponse",
        "MutateCustomerNegativeCriteriaResult",
    },
)


class GetCustomerNegativeCriterionRequest(proto.Message):
    r"""Request message for
    [CustomerNegativeCriterionService.GetCustomerNegativeCriterion][google.ads.googleads.v4.services.CustomerNegativeCriterionService.GetCustomerNegativeCriterion].

    Attributes:
        resource_name (str):
            Required. The resource name of the criterion
            to fetch.
    """

    resource_name = proto.Field(proto.STRING, number=1)


class MutateCustomerNegativeCriteriaRequest(proto.Message):
    r"""Request message for
    [CustomerNegativeCriterionService.MutateCustomerNegativeCriteria][google.ads.googleads.v4.services.CustomerNegativeCriterionService.MutateCustomerNegativeCriteria].

    Attributes:
        customer_id (str):
            Required. The ID of the customer whose
            criteria are being modified.
        operations (Sequence[google.ads.googleads.v4.services.types.CustomerNegativeCriterionOperation]):
            Required. The list of operations to perform
            on individual criteria.
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

    customer_id = proto.Field(proto.STRING, number=1)
    operations = proto.RepeatedField(
        proto.MESSAGE, number=2, message="CustomerNegativeCriterionOperation",
    )
    partial_failure = proto.Field(proto.BOOL, number=3)
    validate_only = proto.Field(proto.BOOL, number=4)


class CustomerNegativeCriterionOperation(proto.Message):
    r"""A single operation (create or remove) on a customer level
    negative criterion.

    Attributes:
        create (google.ads.googleads.v4.resources.types.CustomerNegativeCriterion):
            Create operation: No resource name is
            expected for the new criterion.
        remove (str):
            Remove operation: A resource name for the removed criterion
            is expected, in this format:

            ``customers/{customer_id}/customerNegativeCriteria/{criterion_id}``
    """

    create = proto.Field(
        proto.MESSAGE,
        number=1,
        oneof="operation",
        message=customer_negative_criterion.CustomerNegativeCriterion,
    )
    remove = proto.Field(proto.STRING, number=2, oneof="operation")


class MutateCustomerNegativeCriteriaResponse(proto.Message):
    r"""Response message for customer negative criterion mutate.

    Attributes:
        partial_failure_error (google.rpc.status_pb2.Status):
            Errors that pertain to operation failures in the partial
            failure mode. Returned only when partial_failure = true and
            all errors occur inside the operations. If any errors occur
            outside the operations (e.g. auth errors), we return an RPC
            level error.
        results (Sequence[google.ads.googleads.v4.services.types.MutateCustomerNegativeCriteriaResult]):
            All results for the mutate.
    """

    partial_failure_error = proto.Field(
        proto.MESSAGE, number=3, message=status.Status,
    )
    results = proto.RepeatedField(
        proto.MESSAGE, number=2, message="MutateCustomerNegativeCriteriaResult",
    )


class MutateCustomerNegativeCriteriaResult(proto.Message):
    r"""The result for the criterion mutate.

    Attributes:
        resource_name (str):
            Returned for successful operations.
    """

    resource_name = proto.Field(proto.STRING, number=1)


__all__ = tuple(sorted(__protobuf__.manifest))
