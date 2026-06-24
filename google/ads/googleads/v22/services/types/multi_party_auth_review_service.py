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

from google.ads.googleads.v22.enums.types import multi_party_auth_review_status
from google.rpc import status_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.ads.googleads.v22.services",
    marshal="google.ads.googleads.v22",
    manifest={
        "ResolveMultiPartyAuthReviewRequest",
        "ResolveMultiPartyAuthReviewResponse",
        "ResolveMultiPartyAuthReviewOperation",
        "ResolveMultiPartyAuthReviewResultOrError",
        "ResolveMultiPartyAuthReviewResult",
    },
)


class ResolveMultiPartyAuthReviewRequest(proto.Message):
    r"""Request message for
    [MultiPartyAuthReviewService.ResolveMultiPartyAuthReview][google.ads.googleads.v22.services.MultiPartyAuthReviewService.ResolveMultiPartyAuthReview].

    Attributes:
        customer_id (str):
            Required. The ID of the customer.
        operations (MutableSequence[google.ads.googleads.v22.services.types.ResolveMultiPartyAuthReviewOperation]):
            Required. The operations to perform.
            Currently only one operation is supported.
    """

    customer_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    operations: MutableSequence["ResolveMultiPartyAuthReviewOperation"] = (
        proto.RepeatedField(
            proto.MESSAGE,
            number=2,
            message="ResolveMultiPartyAuthReviewOperation",
        )
    )


class ResolveMultiPartyAuthReviewResponse(proto.Message):
    r"""Response message for
    [MultiPartyAuthReviewService.ResolveMultiPartyAuthReview][google.ads.googleads.v22.services.MultiPartyAuthReviewService.ResolveMultiPartyAuthReview].

    Attributes:
        result_or_error (MutableSequence[google.ads.googleads.v22.services.types.ResolveMultiPartyAuthReviewResultOrError]):
            The results of the operations.
    """

    result_or_error: MutableSequence[
        "ResolveMultiPartyAuthReviewResultOrError"
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="ResolveMultiPartyAuthReviewResultOrError",
    )


class ResolveMultiPartyAuthReviewOperation(proto.Message):
    r"""Operation to resolve a Multi-Party Authorization review.

    Attributes:
        multi_party_auth_review (str):
            Required. The resource name of the
            Multi-Party Authorization review.
        new_status (google.ads.googleads.v22.enums.types.MultiPartyAuthReviewStatusEnum.MultiPartyAuthReviewStatus):
            Required. The status to which the Multi-Party
            Authorization review should be resolved. Valid
            values for requests are limited to: APPROVED,
            REJECTED, REVOKED.
    """

    multi_party_auth_review: str = proto.Field(
        proto.STRING,
        number=1,
    )
    new_status: (
        multi_party_auth_review_status.MultiPartyAuthReviewStatusEnum.MultiPartyAuthReviewStatus
    ) = proto.Field(
        proto.ENUM,
        number=2,
        enum=multi_party_auth_review_status.MultiPartyAuthReviewStatusEnum.MultiPartyAuthReviewStatus,
    )


class ResolveMultiPartyAuthReviewResultOrError(proto.Message):
    r"""Result of the ResolveMultiPartyAuthReview action.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        result (google.ads.googleads.v22.services.types.ResolveMultiPartyAuthReviewResult):
            The result of the operation in case of
            success.

            This field is a member of `oneof`_ ``result_or_error``.
        partial_failure_error (google.rpc.status_pb2.Status):
            Failure status when the request could not be
            processed.

            This field is a member of `oneof`_ ``result_or_error``.
    """

    result: "ResolveMultiPartyAuthReviewResult" = proto.Field(
        proto.MESSAGE,
        number=1,
        oneof="result_or_error",
        message="ResolveMultiPartyAuthReviewResult",
    )
    partial_failure_error: status_pb2.Status = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="result_or_error",
        message=status_pb2.Status,
    )


class ResolveMultiPartyAuthReviewResult(proto.Message):
    r"""Result of the ResolveMultiPartyAuthReview action.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        multi_party_auth_review (str):
            Output only. The resource name of the
            Multi-Party Auth review itself.
        customer_user_access_invitation (str):
            Output only. The resource name of the
            CustomerUserAccessInvitation resource.

            This field is a member of `oneof`_ ``resolved_resource``.
        customer_user_access (str):
            Output only. The resource name of the
            CustomerUserAccess resource.

            This field is a member of `oneof`_ ``resolved_resource``.
    """

    multi_party_auth_review: str = proto.Field(
        proto.STRING,
        number=1,
    )
    customer_user_access_invitation: str = proto.Field(
        proto.STRING,
        number=2,
        oneof="resolved_resource",
    )
    customer_user_access: str = proto.Field(
        proto.STRING,
        number=3,
        oneof="resolved_resource",
    )


__all__ = tuple(sorted(__protobuf__.manifest))
