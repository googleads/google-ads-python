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


from google.ads.googleads.v4.common.types import policy
from google.ads.googleads.v4.enums.types import ad_group_ad_status
from google.ads.googleads.v4.enums.types import ad_strength as gage_ad_strength
from google.ads.googleads.v4.enums.types import policy_approval_status
from google.ads.googleads.v4.enums.types import policy_review_status
from google.ads.googleads.v4.resources.types import ad as gagr_ad
from google.protobuf import wrappers_pb2 as wrappers  # type: ignore


__protobuf__ = proto.module(
    package="google.ads.googleads.v4.resources",
    marshal="google.ads.googleads.v4",
    manifest={"AdGroupAd", "AdGroupAdPolicySummary",},
)


class AdGroupAd(proto.Message):
    r"""An ad group ad.

    Attributes:
        resource_name (str):
            Immutable. The resource name of the ad. Ad group ad resource
            names have the form:

            ``customers/{customer_id}/adGroupAds/{ad_group_id}~{ad_id}``
        status (google.ads.googleads.v4.enums.types.AdGroupAdStatusEnum.AdGroupAdStatus):
            The status of the ad.
        ad_group (google.protobuf.wrappers_pb2.StringValue):
            Immutable. The ad group to which the ad
            belongs.
        ad (google.ads.googleads.v4.resources.types.Ad):
            Immutable. The ad.
        policy_summary (google.ads.googleads.v4.resources.types.AdGroupAdPolicySummary):
            Output only. Policy information for the ad.
        ad_strength (google.ads.googleads.v4.enums.types.AdStrengthEnum.AdStrength):
            Output only. Overall ad strength for this ad
            group ad.
    """

    resource_name = proto.Field(proto.STRING, number=1)
    status = proto.Field(
        proto.ENUM,
        number=3,
        enum=ad_group_ad_status.AdGroupAdStatusEnum.AdGroupAdStatus,
    )
    ad_group = proto.Field(
        proto.MESSAGE, number=4, message=wrappers.StringValue,
    )
    ad = proto.Field(proto.MESSAGE, number=5, message=gagr_ad.Ad,)
    policy_summary = proto.Field(
        proto.MESSAGE, number=6, message="AdGroupAdPolicySummary",
    )
    ad_strength = proto.Field(
        proto.ENUM, number=7, enum=gage_ad_strength.AdStrengthEnum.AdStrength,
    )


class AdGroupAdPolicySummary(proto.Message):
    r"""Contains policy information for an ad.

    Attributes:
        policy_topic_entries (Sequence[google.ads.googleads.v4.common.types.PolicyTopicEntry]):
            Output only. The list of policy findings for
            this ad.
        review_status (google.ads.googleads.v4.enums.types.PolicyReviewStatusEnum.PolicyReviewStatus):
            Output only. Where in the review process this
            ad is.
        approval_status (google.ads.googleads.v4.enums.types.PolicyApprovalStatusEnum.PolicyApprovalStatus):
            Output only. The overall approval status of
            this ad, calculated based on the status of its
            individual policy topic entries.
    """

    policy_topic_entries = proto.RepeatedField(
        proto.MESSAGE, number=1, message=policy.PolicyTopicEntry,
    )
    review_status = proto.Field(
        proto.ENUM,
        number=2,
        enum=policy_review_status.PolicyReviewStatusEnum.PolicyReviewStatus,
    )
    approval_status = proto.Field(
        proto.ENUM,
        number=3,
        enum=policy_approval_status.PolicyApprovalStatusEnum.PolicyApprovalStatus,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
