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

from google.ads.googleads.v17.common.types import policy
from google.ads.googleads.v17.enums.types import ad_group_ad_primary_status
from google.ads.googleads.v17.enums.types import (
    ad_group_ad_primary_status_reason,
)
from google.ads.googleads.v17.enums.types import ad_group_ad_status
from google.ads.googleads.v17.enums.types import ad_strength as gage_ad_strength
from google.ads.googleads.v17.enums.types import policy_approval_status
from google.ads.googleads.v17.enums.types import policy_review_status
from google.ads.googleads.v17.resources.types import ad as gagr_ad


__protobuf__ = proto.module(
    package="google.ads.googleads.v17.resources",
    marshal="google.ads.googleads.v17",
    manifest={
        "AdGroupAd",
        "AdGroupAdPolicySummary",
    },
)


class AdGroupAd(proto.Message):
    r"""An ad group ad.
    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        resource_name (str):
            Immutable. The resource name of the ad. Ad group ad resource
            names have the form:

            ``customers/{customer_id}/adGroupAds/{ad_group_id}~{ad_id}``
        status (google.ads.googleads.v17.enums.types.AdGroupAdStatusEnum.AdGroupAdStatus):
            The status of the ad.
        ad_group (str):
            Immutable. The ad group to which the ad
            belongs.

            This field is a member of `oneof`_ ``_ad_group``.
        ad (google.ads.googleads.v17.resources.types.Ad):
            Immutable. The ad.
        policy_summary (google.ads.googleads.v17.resources.types.AdGroupAdPolicySummary):
            Output only. Policy information for the ad.
        ad_strength (google.ads.googleads.v17.enums.types.AdStrengthEnum.AdStrength):
            Output only. Overall ad strength for this ad
            group ad.
        action_items (MutableSequence[str]):
            Output only. A list of recommendations to
            improve the ad strength. For example, a
            recommendation could be "Try adding a few more
            unique headlines or unpinning some assets.".
        labels (MutableSequence[str]):
            Output only. The resource names of labels
            attached to this ad group ad.
        primary_status (google.ads.googleads.v17.enums.types.AdGroupAdPrimaryStatusEnum.AdGroupAdPrimaryStatus):
            Output only. Provides aggregated view into
            why an ad group ad is not serving or not serving
            optimally.
        primary_status_reasons (MutableSequence[google.ads.googleads.v17.enums.types.AdGroupAdPrimaryStatusReasonEnum.AdGroupAdPrimaryStatusReason]):
            Output only. Provides reasons for why an ad
            group ad is not serving or not serving
            optimally.
    """

    resource_name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    status: ad_group_ad_status.AdGroupAdStatusEnum.AdGroupAdStatus = (
        proto.Field(
            proto.ENUM,
            number=3,
            enum=ad_group_ad_status.AdGroupAdStatusEnum.AdGroupAdStatus,
        )
    )
    ad_group: str = proto.Field(
        proto.STRING,
        number=9,
        optional=True,
    )
    ad: gagr_ad.Ad = proto.Field(
        proto.MESSAGE,
        number=5,
        message=gagr_ad.Ad,
    )
    policy_summary: "AdGroupAdPolicySummary" = proto.Field(
        proto.MESSAGE,
        number=6,
        message="AdGroupAdPolicySummary",
    )
    ad_strength: gage_ad_strength.AdStrengthEnum.AdStrength = proto.Field(
        proto.ENUM,
        number=7,
        enum=gage_ad_strength.AdStrengthEnum.AdStrength,
    )
    action_items: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=13,
    )
    labels: MutableSequence[str] = proto.RepeatedField(
        proto.STRING,
        number=10,
    )
    primary_status: ad_group_ad_primary_status.AdGroupAdPrimaryStatusEnum.AdGroupAdPrimaryStatus = proto.Field(
        proto.ENUM,
        number=16,
        enum=ad_group_ad_primary_status.AdGroupAdPrimaryStatusEnum.AdGroupAdPrimaryStatus,
    )
    primary_status_reasons: MutableSequence[
        ad_group_ad_primary_status_reason.AdGroupAdPrimaryStatusReasonEnum.AdGroupAdPrimaryStatusReason
    ] = proto.RepeatedField(
        proto.ENUM,
        number=17,
        enum=ad_group_ad_primary_status_reason.AdGroupAdPrimaryStatusReasonEnum.AdGroupAdPrimaryStatusReason,
    )


class AdGroupAdPolicySummary(proto.Message):
    r"""Contains policy information for an ad.
    Attributes:
        policy_topic_entries (MutableSequence[google.ads.googleads.v17.common.types.PolicyTopicEntry]):
            Output only. The list of policy findings for
            this ad.
        review_status (google.ads.googleads.v17.enums.types.PolicyReviewStatusEnum.PolicyReviewStatus):
            Output only. Where in the review process this
            ad is.
        approval_status (google.ads.googleads.v17.enums.types.PolicyApprovalStatusEnum.PolicyApprovalStatus):
            Output only. The overall approval status of
            this ad, calculated based on the status of its
            individual policy topic entries.
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
