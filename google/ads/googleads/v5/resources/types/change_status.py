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


from google.ads.googleads.v5.enums.types import change_status_operation
from google.ads.googleads.v5.enums.types import change_status_resource_type
from google.protobuf import wrappers_pb2 as wrappers  # type: ignore


__protobuf__ = proto.module(
    package="google.ads.googleads.v5.resources",
    marshal="google.ads.googleads.v5",
    manifest={"ChangeStatus",},
)


class ChangeStatus(proto.Message):
    r"""Describes the status of returned resource. ChangeStatus could
    have up to 3 minutes delay to reflect a new change.

    Attributes:
        resource_name (str):
            Output only. The resource name of the change status. Change
            status resource names have the form:

            ``customers/{customer_id}/changeStatus/{change_status_id}``
        last_change_date_time (google.protobuf.wrappers_pb2.StringValue):
            Output only. Time at which the most recent
            change has occurred on this resource.
        resource_type (google.ads.googleads.v5.enums.types.ChangeStatusResourceTypeEnum.ChangeStatusResourceType):
            Output only. Represents the type of the changed resource.
            This dictates what fields will be set. For example, for
            AD_GROUP, campaign and ad_group fields will be set.
        campaign (str):
            Output only. The Campaign affected by this
            change.
        ad_group (str):
            Output only. The AdGroup affected by this
            change.
        resource_status (google.ads.googleads.v5.enums.types.ChangeStatusOperationEnum.ChangeStatusOperation):
            Output only. Represents the status of the
            changed resource.
        ad_group_ad (google.protobuf.wrappers_pb2.StringValue):
            Output only. The AdGroupAd affected by this
            change.
        ad_group_criterion (google.protobuf.wrappers_pb2.StringValue):
            Output only. The AdGroupCriterion affected by
            this change.
        campaign_criterion (google.protobuf.wrappers_pb2.StringValue):
            Output only. The CampaignCriterion affected
            by this change.
        feed (google.protobuf.wrappers_pb2.StringValue):
            Output only. The Feed affected by this
            change.
        feed_item (google.protobuf.wrappers_pb2.StringValue):
            Output only. The FeedItem affected by this
            change.
        ad_group_feed (google.protobuf.wrappers_pb2.StringValue):
            Output only. The AdGroupFeed affected by this
            change.
        campaign_feed (google.protobuf.wrappers_pb2.StringValue):
            Output only. The CampaignFeed affected by
            this change.
        ad_group_bid_modifier (google.protobuf.wrappers_pb2.StringValue):
            Output only. The AdGroupBidModifier affected
            by this change.
    """

    resource_name = proto.Field(proto.STRING, number=1)
    last_change_date_time = proto.Field(
        proto.MESSAGE, number=3, message=wrappers.StringValue,
    )
    resource_type = proto.Field(
        proto.ENUM,
        number=4,
        enum=change_status_resource_type.ChangeStatusResourceTypeEnum.ChangeStatusResourceType,
    )
    campaign = proto.Field(proto.STRING, number=17, optional=True)
    ad_group = proto.Field(proto.STRING, number=18, optional=True)
    resource_status = proto.Field(
        proto.ENUM,
        number=8,
        enum=change_status_operation.ChangeStatusOperationEnum.ChangeStatusOperation,
    )
    ad_group_ad = proto.Field(
        proto.MESSAGE, number=9, message=wrappers.StringValue,
    )
    ad_group_criterion = proto.Field(
        proto.MESSAGE, number=10, message=wrappers.StringValue,
    )
    campaign_criterion = proto.Field(
        proto.MESSAGE, number=11, message=wrappers.StringValue,
    )
    feed = proto.Field(proto.MESSAGE, number=12, message=wrappers.StringValue,)
    feed_item = proto.Field(
        proto.MESSAGE, number=13, message=wrappers.StringValue,
    )
    ad_group_feed = proto.Field(
        proto.MESSAGE, number=14, message=wrappers.StringValue,
    )
    campaign_feed = proto.Field(
        proto.MESSAGE, number=15, message=wrappers.StringValue,
    )
    ad_group_bid_modifier = proto.Field(
        proto.MESSAGE, number=16, message=wrappers.StringValue,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
