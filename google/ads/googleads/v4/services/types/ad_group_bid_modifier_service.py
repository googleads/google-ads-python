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


from google.ads.googleads.v4.resources.types import ad_group_bid_modifier
from google.protobuf import field_mask_pb2 as field_mask  # type: ignore
from google.rpc import status_pb2 as status  # type: ignore


__protobuf__ = proto.module(
    package="google.ads.googleads.v4.services",
    marshal="google.ads.googleads.v4",
    manifest={
        "GetAdGroupBidModifierRequest",
        "MutateAdGroupBidModifiersRequest",
        "AdGroupBidModifierOperation",
        "MutateAdGroupBidModifiersResponse",
        "MutateAdGroupBidModifierResult",
    },
)


class GetAdGroupBidModifierRequest(proto.Message):
    r"""Request message for
    [AdGroupBidModifierService.GetAdGroupBidModifier][google.ads.googleads.v4.services.AdGroupBidModifierService.GetAdGroupBidModifier].

    Attributes:
        resource_name (str):
            Required. The resource name of the ad group
            bid modifier to fetch.
    """

    resource_name = proto.Field(proto.STRING, number=1)


class MutateAdGroupBidModifiersRequest(proto.Message):
    r"""Request message for
    [AdGroupBidModifierService.MutateAdGroupBidModifiers][google.ads.googleads.v4.services.AdGroupBidModifierService.MutateAdGroupBidModifiers].

    Attributes:
        customer_id (str):
            Required. ID of the customer whose ad group
            bid modifiers are being modified.
        operations (Sequence[google.ads.googleads.v4.services.types.AdGroupBidModifierOperation]):
            Required. The list of operations to perform
            on individual ad group bid modifiers.
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
        proto.MESSAGE, number=2, message="AdGroupBidModifierOperation",
    )
    partial_failure = proto.Field(proto.BOOL, number=3)
    validate_only = proto.Field(proto.BOOL, number=4)


class AdGroupBidModifierOperation(proto.Message):
    r"""A single operation (create, remove, update) on an ad group
    bid modifier.

    Attributes:
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            FieldMask that determines which resource
            fields are modified in an update.
        create (google.ads.googleads.v4.resources.types.AdGroupBidModifier):
            Create operation: No resource name is
            expected for the new ad group bid modifier.
        update (google.ads.googleads.v4.resources.types.AdGroupBidModifier):
            Update operation: The ad group bid modifier
            is expected to have a valid resource name.
        remove (str):
            Remove operation: A resource name for the removed ad group
            bid modifier is expected, in this format:

            ``customers/{customer_id}/adGroupBidModifiers/{ad_group_id}~{criterion_id}``
    """

    update_mask = proto.Field(
        proto.MESSAGE, number=4, message=field_mask.FieldMask,
    )
    create = proto.Field(
        proto.MESSAGE,
        number=1,
        oneof="operation",
        message=ad_group_bid_modifier.AdGroupBidModifier,
    )
    update = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="operation",
        message=ad_group_bid_modifier.AdGroupBidModifier,
    )
    remove = proto.Field(proto.STRING, number=3, oneof="operation")


class MutateAdGroupBidModifiersResponse(proto.Message):
    r"""Response message for ad group bid modifiers mutate.

    Attributes:
        partial_failure_error (google.rpc.status_pb2.Status):
            Errors that pertain to operation failures in the partial
            failure mode. Returned only when partial_failure = true and
            all errors occur inside the operations. If any errors occur
            outside the operations (e.g. auth errors), we return an RPC
            level error.
        results (Sequence[google.ads.googleads.v4.services.types.MutateAdGroupBidModifierResult]):
            All results for the mutate.
    """

    partial_failure_error = proto.Field(
        proto.MESSAGE, number=3, message=status.Status,
    )
    results = proto.RepeatedField(
        proto.MESSAGE, number=2, message="MutateAdGroupBidModifierResult",
    )


class MutateAdGroupBidModifierResult(proto.Message):
    r"""The result for the criterion mutate.

    Attributes:
        resource_name (str):
            Returned for successful operations.
    """

    resource_name = proto.Field(proto.STRING, number=1)


__all__ = tuple(sorted(__protobuf__.manifest))
