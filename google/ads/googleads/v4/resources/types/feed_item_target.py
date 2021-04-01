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


from google.ads.googleads.v4.common.types import criteria
from google.ads.googleads.v4.enums.types import feed_item_target_device
from google.ads.googleads.v4.enums.types import feed_item_target_status
from google.ads.googleads.v4.enums.types import (
    feed_item_target_type as gage_feed_item_target_type,
)
from google.protobuf import wrappers_pb2 as wrappers  # type: ignore


__protobuf__ = proto.module(
    package="google.ads.googleads.v4.resources",
    marshal="google.ads.googleads.v4",
    manifest={"FeedItemTarget",},
)


class FeedItemTarget(proto.Message):
    r"""A feed item target.

    Attributes:
        resource_name (str):
            Immutable. The resource name of the feed item target. Feed
            item target resource names have the form:
            ``customers/{customer_id}/feedItemTargets/{feed_id}~{feed_item_id}~{feed_item_target_type}~{feed_item_target_id}``
        feed_item (google.protobuf.wrappers_pb2.StringValue):
            Immutable. The feed item to which this feed
            item target belongs.
        feed_item_target_type (google.ads.googleads.v4.enums.types.FeedItemTargetTypeEnum.FeedItemTargetType):
            Output only. The target type of this feed
            item target. This field is read-only.
        feed_item_target_id (google.protobuf.wrappers_pb2.Int64Value):
            Output only. The ID of the targeted resource.
            This field is read-only.
        status (google.ads.googleads.v4.enums.types.FeedItemTargetStatusEnum.FeedItemTargetStatus):
            Output only. Status of the feed item target.
            This field is read-only.
        campaign (google.protobuf.wrappers_pb2.StringValue):
            Immutable. The targeted campaign.
        ad_group (google.protobuf.wrappers_pb2.StringValue):
            Immutable. The targeted ad group.
        keyword (google.ads.googleads.v4.common.types.KeywordInfo):
            Immutable. The targeted keyword.
        geo_target_constant (google.protobuf.wrappers_pb2.StringValue):
            Immutable. The targeted geo target constant
            resource name.
        device (google.ads.googleads.v4.enums.types.FeedItemTargetDeviceEnum.FeedItemTargetDevice):
            Immutable. The targeted device.
        ad_schedule (google.ads.googleads.v4.common.types.AdScheduleInfo):
            Immutable. The targeted schedule.
    """

    resource_name = proto.Field(proto.STRING, number=1)
    feed_item = proto.Field(
        proto.MESSAGE, number=2, message=wrappers.StringValue,
    )
    feed_item_target_type = proto.Field(
        proto.ENUM,
        number=3,
        enum=gage_feed_item_target_type.FeedItemTargetTypeEnum.FeedItemTargetType,
    )
    feed_item_target_id = proto.Field(
        proto.MESSAGE, number=6, message=wrappers.Int64Value,
    )
    status = proto.Field(
        proto.ENUM,
        number=11,
        enum=feed_item_target_status.FeedItemTargetStatusEnum.FeedItemTargetStatus,
    )
    campaign = proto.Field(
        proto.MESSAGE, number=4, oneof="target", message=wrappers.StringValue,
    )
    ad_group = proto.Field(
        proto.MESSAGE, number=5, oneof="target", message=wrappers.StringValue,
    )
    keyword = proto.Field(
        proto.MESSAGE, number=7, oneof="target", message=criteria.KeywordInfo,
    )
    geo_target_constant = proto.Field(
        proto.MESSAGE, number=8, oneof="target", message=wrappers.StringValue,
    )
    device = proto.Field(
        proto.ENUM,
        number=9,
        oneof="target",
        enum=feed_item_target_device.FeedItemTargetDeviceEnum.FeedItemTargetDevice,
    )
    ad_schedule = proto.Field(
        proto.MESSAGE,
        number=10,
        oneof="target",
        message=criteria.AdScheduleInfo,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
