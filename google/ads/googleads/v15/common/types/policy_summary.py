# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
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

from google.ads.googleads.v15.common.types import policy
from google.ads.googleads.v15.enums.types import policy_approval_status
from google.ads.googleads.v15.enums.types import policy_review_status


__protobuf__ = proto.module(
    package="google.ads.googleads.v15.common",
    marshal="google.ads.googleads.v15",
    manifest={
        "PolicySummary",
    },
)


class PolicySummary(proto.Message):
    r"""Contains policy summary information.
    Attributes:
        policy_topic_entries (MutableSequence[google.ads.googleads.v15.common.types.PolicyTopicEntry]):
            The list of policy findings.
        review_status (google.ads.googleads.v15.enums.types.PolicyReviewStatusEnum.PolicyReviewStatus):
            Where in the review process the resource is.
        approval_status (google.ads.googleads.v15.enums.types.PolicyApprovalStatusEnum.PolicyApprovalStatus):
            The overall approval status, which is
            calculated based on the status of its individual
            policy topic entries.
    """

    policy_topic_entries: MutableSequence[
        policy.PolicyTopicEntry
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=policy.PolicyTopicEntry,
    )
    review_status: policy_review_status.PolicyReviewStatusEnum.PolicyReviewStatus = proto.Field(
        proto.ENUM,
        number=2,
        enum=policy_review_status.PolicyReviewStatusEnum.PolicyReviewStatus,
    )
    approval_status: policy_approval_status.PolicyApprovalStatusEnum.PolicyApprovalStatus = proto.Field(
        proto.ENUM,
        number=3,
        enum=policy_approval_status.PolicyApprovalStatusEnum.PolicyApprovalStatus,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
