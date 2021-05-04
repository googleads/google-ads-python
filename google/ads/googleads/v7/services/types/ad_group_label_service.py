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

from google.ads.googleads.v7.resources.types import ad_group_label
from google.rpc import status_pb2 as status  # type: ignore


__protobuf__ = proto.module(
    package="google.ads.googleads.v7.services",
    marshal="google.ads.googleads.v7",
    manifest={
        "GetAdGroupLabelRequest",
        "MutateAdGroupLabelsRequest",
        "AdGroupLabelOperation",
        "MutateAdGroupLabelsResponse",
        "MutateAdGroupLabelResult",
    },
)


class GetAdGroupLabelRequest(proto.Message):
    r"""Request message for
    [AdGroupLabelService.GetAdGroupLabel][google.ads.googleads.v7.services.AdGroupLabelService.GetAdGroupLabel].

    Attributes:
        resource_name (str):
            Required. The resource name of the ad group
            label to fetch.
    """

    resource_name = proto.Field(proto.STRING, number=1,)


class MutateAdGroupLabelsRequest(proto.Message):
    r"""Request message for
    [AdGroupLabelService.MutateAdGroupLabels][google.ads.googleads.v7.services.AdGroupLabelService.MutateAdGroupLabels].

    Attributes:
        customer_id (str):
            Required. ID of the customer whose ad group
            labels are being modified.
        operations (Sequence[google.ads.googleads.v7.services.types.AdGroupLabelOperation]):
            Required. The list of operations to perform
            on ad group labels.
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

    customer_id = proto.Field(proto.STRING, number=1,)
    operations = proto.RepeatedField(
        proto.MESSAGE, number=2, message="AdGroupLabelOperation",
    )
    partial_failure = proto.Field(proto.BOOL, number=3,)
    validate_only = proto.Field(proto.BOOL, number=4,)


class AdGroupLabelOperation(proto.Message):
    r"""A single operation (create, remove) on an ad group label.
    Attributes:
        create (google.ads.googleads.v7.resources.types.AdGroupLabel):
            Create operation: No resource name is
            expected for the new ad group label.
        remove (str):
            Remove operation: A resource name for the ad group label
            being removed, in this format:

            ``customers/{customer_id}/adGroupLabels/{ad_group_id}~{label_id}``
    """

    create = proto.Field(
        proto.MESSAGE,
        number=1,
        oneof="operation",
        message=ad_group_label.AdGroupLabel,
    )
    remove = proto.Field(proto.STRING, number=2, oneof="operation",)


class MutateAdGroupLabelsResponse(proto.Message):
    r"""Response message for an ad group labels mutate.
    Attributes:
        partial_failure_error (google.rpc.status_pb2.Status):
            Errors that pertain to operation failures in the partial
            failure mode. Returned only when partial_failure = true and
            all errors occur inside the operations. If any errors occur
            outside the operations (e.g. auth errors), we return an RPC
            level error.
        results (Sequence[google.ads.googleads.v7.services.types.MutateAdGroupLabelResult]):
            All results for the mutate.
    """

    partial_failure_error = proto.Field(
        proto.MESSAGE, number=3, message=status.Status,
    )
    results = proto.RepeatedField(
        proto.MESSAGE, number=2, message="MutateAdGroupLabelResult",
    )


class MutateAdGroupLabelResult(proto.Message):
    r"""The result for an ad group label mutate.
    Attributes:
        resource_name (str):
            Returned for successful operations.
    """

    resource_name = proto.Field(proto.STRING, number=1,)


__all__ = tuple(sorted(__protobuf__.manifest))
