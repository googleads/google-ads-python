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


from google.ads.googleads.v6.resources.types import custom_audience
from google.protobuf import field_mask_pb2 as field_mask  # type: ignore


__protobuf__ = proto.module(
    package="google.ads.googleads.v6.services",
    marshal="google.ads.googleads.v6",
    manifest={
        "GetCustomAudienceRequest",
        "MutateCustomAudiencesRequest",
        "CustomAudienceOperation",
        "MutateCustomAudiencesResponse",
        "MutateCustomAudienceResult",
    },
)


class GetCustomAudienceRequest(proto.Message):
    r"""Request message for
    [CustomAudienceService.GetCustomAudience][google.ads.googleads.v6.services.CustomAudienceService.GetCustomAudience].

    Attributes:
        resource_name (str):
            Required. The resource name of the custom
            audience to fetch.
    """

    resource_name = proto.Field(proto.STRING, number=1)


class MutateCustomAudiencesRequest(proto.Message):
    r"""Request message for
    [CustomAudienceService.MutateCustomAudiences][google.ads.googleads.v6.services.CustomAudienceService.MutateCustomAudiences].

    Attributes:
        customer_id (str):
            Required. The ID of the customer whose custom
            audiences are being modified.
        operations (Sequence[google.ads.googleads.v6.services.types.CustomAudienceOperation]):
            Required. The list of operations to perform
            on individual custom audiences.
        validate_only (bool):
            If true, the request is validated but not
            executed. Only errors are returned, not results.
    """

    customer_id = proto.Field(proto.STRING, number=1)
    operations = proto.RepeatedField(
        proto.MESSAGE, number=2, message="CustomAudienceOperation",
    )
    validate_only = proto.Field(proto.BOOL, number=3)


class CustomAudienceOperation(proto.Message):
    r"""A single operation (create, update) on a custom audience.

    Attributes:
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            FieldMask that determines which resource
            fields are modified in an update.
        create (google.ads.googleads.v6.resources.types.CustomAudience):
            Create operation: No resource name is
            expected for the new custom audience.
        update (google.ads.googleads.v6.resources.types.CustomAudience):
            Update operation: The custom audience is
            expected to have a valid resource name.
        remove (str):
            Remove operation: A resource name for the removed custom
            audience is expected, in this format:

            ``customers/{customer_id}/customAudiences/{custom_audience_id}``
    """

    update_mask = proto.Field(
        proto.MESSAGE, number=4, message=field_mask.FieldMask,
    )
    create = proto.Field(
        proto.MESSAGE,
        number=1,
        oneof="operation",
        message=custom_audience.CustomAudience,
    )
    update = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="operation",
        message=custom_audience.CustomAudience,
    )
    remove = proto.Field(proto.STRING, number=3, oneof="operation")


class MutateCustomAudiencesResponse(proto.Message):
    r"""Response message for custom audience mutate.

    Attributes:
        results (Sequence[google.ads.googleads.v6.services.types.MutateCustomAudienceResult]):
            All results for the mutate.
    """

    results = proto.RepeatedField(
        proto.MESSAGE, number=1, message="MutateCustomAudienceResult",
    )


class MutateCustomAudienceResult(proto.Message):
    r"""The result for the custom audience mutate.

    Attributes:
        resource_name (str):
            Returned for successful operations.
    """

    resource_name = proto.Field(proto.STRING, number=1)


__all__ = tuple(sorted(__protobuf__.manifest))
