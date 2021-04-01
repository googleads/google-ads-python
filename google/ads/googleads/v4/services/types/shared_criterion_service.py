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


from google.ads.googleads.v4.resources.types import shared_criterion
from google.rpc import status_pb2 as status  # type: ignore


__protobuf__ = proto.module(
    package="google.ads.googleads.v4.services",
    marshal="google.ads.googleads.v4",
    manifest={
        "GetSharedCriterionRequest",
        "MutateSharedCriteriaRequest",
        "SharedCriterionOperation",
        "MutateSharedCriteriaResponse",
        "MutateSharedCriterionResult",
    },
)


class GetSharedCriterionRequest(proto.Message):
    r"""Request message for
    [SharedCriterionService.GetSharedCriterion][google.ads.googleads.v4.services.SharedCriterionService.GetSharedCriterion].

    Attributes:
        resource_name (str):
            Required. The resource name of the shared
            criterion to fetch.
    """

    resource_name = proto.Field(proto.STRING, number=1)


class MutateSharedCriteriaRequest(proto.Message):
    r"""Request message for
    [SharedCriterionService.MutateSharedCriteria][google.ads.googleads.v4.services.SharedCriterionService.MutateSharedCriteria].

    Attributes:
        customer_id (str):
            Required. The ID of the customer whose shared
            criteria are being modified.
        operations (Sequence[google.ads.googleads.v4.services.types.SharedCriterionOperation]):
            Required. The list of operations to perform
            on individual shared criteria.
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
        proto.MESSAGE, number=2, message="SharedCriterionOperation",
    )
    partial_failure = proto.Field(proto.BOOL, number=3)
    validate_only = proto.Field(proto.BOOL, number=4)


class SharedCriterionOperation(proto.Message):
    r"""A single operation (create, remove) on an shared criterion.

    Attributes:
        create (google.ads.googleads.v4.resources.types.SharedCriterion):
            Create operation: No resource name is
            expected for the new shared criterion.
        remove (str):
            Remove operation: A resource name for the removed shared
            criterion is expected, in this format:

            ``customers/{customer_id}/sharedCriteria/{shared_set_id}~{criterion_id}``
    """

    create = proto.Field(
        proto.MESSAGE,
        number=1,
        oneof="operation",
        message=shared_criterion.SharedCriterion,
    )
    remove = proto.Field(proto.STRING, number=3, oneof="operation")


class MutateSharedCriteriaResponse(proto.Message):
    r"""Response message for a shared criterion mutate.

    Attributes:
        partial_failure_error (google.rpc.status_pb2.Status):
            Errors that pertain to operation failures in the partial
            failure mode. Returned only when partial_failure = true and
            all errors occur inside the operations. If any errors occur
            outside the operations (e.g. auth errors), we return an RPC
            level error.
        results (Sequence[google.ads.googleads.v4.services.types.MutateSharedCriterionResult]):
            All results for the mutate.
    """

    partial_failure_error = proto.Field(
        proto.MESSAGE, number=3, message=status.Status,
    )
    results = proto.RepeatedField(
        proto.MESSAGE, number=2, message="MutateSharedCriterionResult",
    )


class MutateSharedCriterionResult(proto.Message):
    r"""The result for the shared criterion mutate.

    Attributes:
        resource_name (str):
            Returned for successful operations.
    """

    resource_name = proto.Field(proto.STRING, number=1)


__all__ = tuple(sorted(__protobuf__.manifest))
