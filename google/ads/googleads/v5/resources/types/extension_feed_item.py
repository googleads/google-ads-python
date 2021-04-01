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


from google.ads.googleads.v5.common.types import criteria
from google.ads.googleads.v5.common.types import extensions
from google.ads.googleads.v5.enums.types import (
    extension_type as gage_extension_type,
)
from google.ads.googleads.v5.enums.types import feed_item_status
from google.ads.googleads.v5.enums.types import feed_item_target_device
from google.protobuf import wrappers_pb2 as wrappers  # type: ignore


__protobuf__ = proto.module(
    package="google.ads.googleads.v5.resources",
    marshal="google.ads.googleads.v5",
    manifest={"ExtensionFeedItem",},
)


class ExtensionFeedItem(proto.Message):
    r"""An extension feed item.

    Attributes:
        resource_name (str):
            Immutable. The resource name of the extension feed item.
            Extension feed item resource names have the form:

            ``customers/{customer_id}/extensionFeedItems/{feed_item_id}``
        id (google.protobuf.wrappers_pb2.Int64Value):
            Output only. The ID of this feed item. Read-
            nly.
        extension_type (google.ads.googleads.v5.enums.types.ExtensionTypeEnum.ExtensionType):
            Output only. The extension type of the
            extension feed item. This field is read-only.
        start_date_time (google.protobuf.wrappers_pb2.StringValue):
            Start time in which this feed item is
            effective and can begin serving. The time is in
            the customer's time zone. The format is "YYYY-
            MM-DD HH:MM:SS".
            Examples: "2018-03-05 09:15:00" or "2018-02-01
            14:34:30".
        end_date_time (google.protobuf.wrappers_pb2.StringValue):
            End time in which this feed item is no longer
            effective and will stop serving. The time is in
            the customer's time zone. The format is "YYYY-
            MM-DD HH:MM:SS".
            Examples: "2018-03-05 09:15:00" or "2018-02-01
            14:34:30".
        ad_schedules (Sequence[google.ads.googleads.v5.common.types.AdScheduleInfo]):
            List of non-overlapping schedules specifying
            all time intervals for which the feed item may
            serve. There can be a maximum of 6 schedules per
            day.
        device (google.ads.googleads.v5.enums.types.FeedItemTargetDeviceEnum.FeedItemTargetDevice):
            The targeted device.
        targeted_geo_target_constant (google.protobuf.wrappers_pb2.StringValue):
            The targeted geo target constant.
        targeted_keyword (google.ads.googleads.v5.common.types.KeywordInfo):
            The targeted keyword.
        status (google.ads.googleads.v5.enums.types.FeedItemStatusEnum.FeedItemStatus):
            Output only. Status of the feed item.
            This field is read-only.
        sitelink_feed_item (google.ads.googleads.v5.common.types.SitelinkFeedItem):
            Sitelink extension.
        structured_snippet_feed_item (google.ads.googleads.v5.common.types.StructuredSnippetFeedItem):
            Structured snippet extension.
        app_feed_item (google.ads.googleads.v5.common.types.AppFeedItem):
            App extension.
        call_feed_item (google.ads.googleads.v5.common.types.CallFeedItem):
            Call extension.
        callout_feed_item (google.ads.googleads.v5.common.types.CalloutFeedItem):
            Callout extension.
        text_message_feed_item (google.ads.googleads.v5.common.types.TextMessageFeedItem):
            Text message extension.
        price_feed_item (google.ads.googleads.v5.common.types.PriceFeedItem):
            Price extension.
        promotion_feed_item (google.ads.googleads.v5.common.types.PromotionFeedItem):
            Promotion extension.
        location_feed_item (google.ads.googleads.v5.common.types.LocationFeedItem):
            Output only. Location extension. Locations
            are synced from a GMB account into a feed. This
            field is read-only.
        affiliate_location_feed_item (google.ads.googleads.v5.common.types.AffiliateLocationFeedItem):
            Output only. Affiliate location extension.
            Feed locations are populated by Google Ads based
            on a chain ID. This field is read-only.
        hotel_callout_feed_item (google.ads.googleads.v5.common.types.HotelCalloutFeedItem):
            Hotel Callout extension.
        targeted_campaign (google.protobuf.wrappers_pb2.StringValue):
            The targeted campaign.
        targeted_ad_group (google.protobuf.wrappers_pb2.StringValue):
            The targeted ad group.
    """

    resource_name = proto.Field(proto.STRING, number=1)
    id = proto.Field(proto.MESSAGE, number=24, message=wrappers.Int64Value,)
    extension_type = proto.Field(
        proto.ENUM,
        number=13,
        enum=gage_extension_type.ExtensionTypeEnum.ExtensionType,
    )
    start_date_time = proto.Field(
        proto.MESSAGE, number=5, message=wrappers.StringValue,
    )
    end_date_time = proto.Field(
        proto.MESSAGE, number=6, message=wrappers.StringValue,
    )
    ad_schedules = proto.RepeatedField(
        proto.MESSAGE, number=16, message=criteria.AdScheduleInfo,
    )
    device = proto.Field(
        proto.ENUM,
        number=17,
        enum=feed_item_target_device.FeedItemTargetDeviceEnum.FeedItemTargetDevice,
    )
    targeted_geo_target_constant = proto.Field(
        proto.MESSAGE, number=20, message=wrappers.StringValue,
    )
    targeted_keyword = proto.Field(
        proto.MESSAGE, number=22, message=criteria.KeywordInfo,
    )
    status = proto.Field(
        proto.ENUM,
        number=4,
        enum=feed_item_status.FeedItemStatusEnum.FeedItemStatus,
    )
    sitelink_feed_item = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="extension",
        message=extensions.SitelinkFeedItem,
    )
    structured_snippet_feed_item = proto.Field(
        proto.MESSAGE,
        number=3,
        oneof="extension",
        message=extensions.StructuredSnippetFeedItem,
    )
    app_feed_item = proto.Field(
        proto.MESSAGE,
        number=7,
        oneof="extension",
        message=extensions.AppFeedItem,
    )
    call_feed_item = proto.Field(
        proto.MESSAGE,
        number=8,
        oneof="extension",
        message=extensions.CallFeedItem,
    )
    callout_feed_item = proto.Field(
        proto.MESSAGE,
        number=9,
        oneof="extension",
        message=extensions.CalloutFeedItem,
    )
    text_message_feed_item = proto.Field(
        proto.MESSAGE,
        number=10,
        oneof="extension",
        message=extensions.TextMessageFeedItem,
    )
    price_feed_item = proto.Field(
        proto.MESSAGE,
        number=11,
        oneof="extension",
        message=extensions.PriceFeedItem,
    )
    promotion_feed_item = proto.Field(
        proto.MESSAGE,
        number=12,
        oneof="extension",
        message=extensions.PromotionFeedItem,
    )
    location_feed_item = proto.Field(
        proto.MESSAGE,
        number=14,
        oneof="extension",
        message=extensions.LocationFeedItem,
    )
    affiliate_location_feed_item = proto.Field(
        proto.MESSAGE,
        number=15,
        oneof="extension",
        message=extensions.AffiliateLocationFeedItem,
    )
    hotel_callout_feed_item = proto.Field(
        proto.MESSAGE,
        number=23,
        oneof="extension",
        message=extensions.HotelCalloutFeedItem,
    )
    targeted_campaign = proto.Field(
        proto.MESSAGE,
        number=18,
        oneof="serving_resource_targeting",
        message=wrappers.StringValue,
    )
    targeted_ad_group = proto.Field(
        proto.MESSAGE,
        number=19,
        oneof="serving_resource_targeting",
        message=wrappers.StringValue,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
