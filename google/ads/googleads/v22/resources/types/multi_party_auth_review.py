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


import proto  # type: ignore

from google.ads.googleads.v22.enums.types import multi_party_auth_operation_type
from google.ads.googleads.v22.enums.types import multi_party_auth_review_status
from google.ads.googleads.v22.enums.types import (
    multi_party_auth_review_target_resource,
)
from google.ads.googleads.v22.resources.types import customer_user_access
from google.ads.googleads.v22.resources.types import (
    customer_user_access_invitation,
)


__protobuf__ = proto.module(
    package="google.ads.googleads.v22.resources",
    marshal="google.ads.googleads.v22",
    manifest={
        "MultiPartyAuthReview",
        "CustomerUserAccessReview",
        "CustomerUserAccessInvitationReview",
    },
)


class MultiPartyAuthReview(proto.Message):
    r"""Resource representing a Multi-Party Authentication review.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        resource_name (str):
            Immutable. The resource name of the Multi-Party
            Authentication review. Resource names have the form:
            ``customers/{customer_id}/multiPartyAuthReviews/{multi_party_auth_review_id}``
        multi_party_auth_review_id (int):
            Output only. The ID of the Multi-Party
            Authorization review.
        creation_date_time (str):
            Output only. The creation date and time of
            the Multi-Party Authorization review.
        review_status (google.ads.googleads.v22.enums.types.MultiPartyAuthReviewStatusEnum.MultiPartyAuthReviewStatus):
            Output only. The status of the Multi-Party
            Authorization review.
        approval_date_time (str):
            Output only. The approval date and time of
            the Multi-Party Authorization review.
        justification (str):
            Output only. The justification for the
            Multi-Party Authorization review request given
            by the requester.
        request_user_email (str):
            Output only. The email of the user who
            requested the Multi-Party Authorization review
        operation_type (google.ads.googleads.v22.enums.types.MultiPartyAuthOperationTypeEnum.MultiPartyAuthOperationType):
            Output only. The operation type of the
            Multi-Party Authorization review.
        target_resource (google.ads.googleads.v22.enums.types.MultiPartyAuthReviewTargetResourceEnum.MultiPartyAuthReviewTargetResource):
            Output only. The target resource for which
            Multi-Party Authorization is requested.
        customer_user_access_review (google.ads.googleads.v22.resources.types.CustomerUserAccessReview):
            Output only. The CustomerUserAccess details.

            This field is a member of `oneof`_ ``multi_party_review_detail``.
        customer_user_access_invitation_review (google.ads.googleads.v22.resources.types.CustomerUserAccessInvitationReview):
            Output only. The CustomerUserAccessInvitation
            details.

            This field is a member of `oneof`_ ``multi_party_review_detail``.
    """

    resource_name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    multi_party_auth_review_id: int = proto.Field(
        proto.INT64,
        number=4,
    )
    creation_date_time: str = proto.Field(
        proto.STRING,
        number=5,
    )
    review_status: (
        multi_party_auth_review_status.MultiPartyAuthReviewStatusEnum.MultiPartyAuthReviewStatus
    ) = proto.Field(
        proto.ENUM,
        number=6,
        enum=multi_party_auth_review_status.MultiPartyAuthReviewStatusEnum.MultiPartyAuthReviewStatus,
    )
    approval_date_time: str = proto.Field(
        proto.STRING,
        number=7,
    )
    justification: str = proto.Field(
        proto.STRING,
        number=9,
    )
    request_user_email: str = proto.Field(
        proto.STRING,
        number=10,
    )
    operation_type: (
        multi_party_auth_operation_type.MultiPartyAuthOperationTypeEnum.MultiPartyAuthOperationType
    ) = proto.Field(
        proto.ENUM,
        number=11,
        enum=multi_party_auth_operation_type.MultiPartyAuthOperationTypeEnum.MultiPartyAuthOperationType,
    )
    target_resource: (
        multi_party_auth_review_target_resource.MultiPartyAuthReviewTargetResourceEnum.MultiPartyAuthReviewTargetResource
    ) = proto.Field(
        proto.ENUM,
        number=12,
        enum=multi_party_auth_review_target_resource.MultiPartyAuthReviewTargetResourceEnum.MultiPartyAuthReviewTargetResource,
    )
    customer_user_access_review: "CustomerUserAccessReview" = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="multi_party_review_detail",
        message="CustomerUserAccessReview",
    )
    customer_user_access_invitation_review: (
        "CustomerUserAccessInvitationReview"
    ) = proto.Field(
        proto.MESSAGE,
        number=3,
        oneof="multi_party_review_detail",
        message="CustomerUserAccessInvitationReview",
    )


class CustomerUserAccessReview(proto.Message):
    r"""Details for CustomerUserAccess.

    Attributes:
        old_customer_user_access (str):
            Output only. The resource name of the
            CustomerUserAccess being changed.
        new_customer_user_access (google.ads.googleads.v22.resources.types.CustomerUserAccess):
            Output only. The new CustomerUserAccess
            details. Only fields that need to be reviewed
            are populated.
    """

    old_customer_user_access: str = proto.Field(
        proto.STRING,
        number=1,
    )
    new_customer_user_access: customer_user_access.CustomerUserAccess = (
        proto.Field(
            proto.MESSAGE,
            number=2,
            message=customer_user_access.CustomerUserAccess,
        )
    )


class CustomerUserAccessInvitationReview(proto.Message):
    r"""Details for CustomerUserAccessInvitation.

    Attributes:
        new_customer_user_access_invitation (google.ads.googleads.v22.resources.types.CustomerUserAccessInvitation):
            Output only. The new
            CustomerUserAccessInvitation details. Only
            fields that need to be reviewed are populated.
    """

    new_customer_user_access_invitation: (
        customer_user_access_invitation.CustomerUserAccessInvitation
    ) = proto.Field(
        proto.MESSAGE,
        number=2,
        message=customer_user_access_invitation.CustomerUserAccessInvitation,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
