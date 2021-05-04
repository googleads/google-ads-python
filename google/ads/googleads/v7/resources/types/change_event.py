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

from google.ads.googleads.v7.enums.types import change_client_type
from google.ads.googleads.v7.enums.types import change_event_resource_type
from google.ads.googleads.v7.enums.types import (
    resource_change_operation as gage_resource_change_operation,
)
from google.ads.googleads.v7.resources.types import ad as gagr_ad
from google.ads.googleads.v7.resources.types import ad_group as gagr_ad_group
from google.ads.googleads.v7.resources.types import (
    ad_group_ad as gagr_ad_group_ad,
)
from google.ads.googleads.v7.resources.types import (
    ad_group_bid_modifier as gagr_ad_group_bid_modifier,
)
from google.ads.googleads.v7.resources.types import (
    ad_group_criterion as gagr_ad_group_criterion,
)
from google.ads.googleads.v7.resources.types import (
    ad_group_feed as gagr_ad_group_feed,
)
from google.ads.googleads.v7.resources.types import campaign as gagr_campaign
from google.ads.googleads.v7.resources.types import (
    campaign_budget as gagr_campaign_budget,
)
from google.ads.googleads.v7.resources.types import (
    campaign_criterion as gagr_campaign_criterion,
)
from google.ads.googleads.v7.resources.types import (
    campaign_feed as gagr_campaign_feed,
)
from google.ads.googleads.v7.resources.types import feed as gagr_feed
from google.ads.googleads.v7.resources.types import feed_item as gagr_feed_item
from google.protobuf import field_mask_pb2 as field_mask  # type: ignore


__protobuf__ = proto.module(
    package="google.ads.googleads.v7.resources",
    marshal="google.ads.googleads.v7",
    manifest={"ChangeEvent",},
)


class ChangeEvent(proto.Message):
    r"""Describes the granular change of returned resource of certain
    resource types. Changes made through UI, API and new versions of
    Editor by external users (including external users, and internal
    users that can be shown externally) in the past 30 days will be
    shown. The change shows the old values of the changed fields
    before the change and the new values right after the change.
    ChangeEvent could have up to 3 minutes delay to reflect a new
    change.

    Attributes:
        resource_name (str):
            Output only. The resource name of the change event. Change
            event resource names have the form:

            ``customers/{customer_id}/changeEvent/{timestamp_micros}~{command_index}~{mutate_index}``
        change_date_time (str):
            Output only. Time at which the change was
            committed on this resource.
        change_resource_type (google.ads.googleads.v7.enums.types.ChangeEventResourceTypeEnum.ChangeEventResourceType):
            Output only. The type of the changed resource. This dictates
            what resource will be set in old_resource and new_resource.
        change_resource_name (str):
            Output only. The Simply resource this change
            occurred on.
        client_type (google.ads.googleads.v7.enums.types.ChangeClientTypeEnum.ChangeClientType):
            Output only. Where the change was made
            through.
        user_email (str):
            Output only. The email of the user who made
            this change.
        old_resource (google.ads.googleads.v7.resources.types.ChangeEvent.ChangedResource):
            Output only. The old resource before the
            change. Only changed fields will be populated.
        new_resource (google.ads.googleads.v7.resources.types.ChangeEvent.ChangedResource):
            Output only. The new resource after the
            change. Only changed fields will be populated.
        resource_change_operation (google.ads.googleads.v7.enums.types.ResourceChangeOperationEnum.ResourceChangeOperation):
            Output only. The operation on the changed
            resource.
        changed_fields (google.protobuf.field_mask_pb2.FieldMask):
            Output only. A list of fields that are
            changed in the returned resource.
        campaign (str):
            Output only. The Campaign affected by this
            change.
        ad_group (str):
            Output only. The AdGroup affected by this
            change.
        feed (str):
            Output only. The Feed affected by this
            change.
        feed_item (str):
            Output only. The FeedItem affected by this
            change.
    """

    class ChangedResource(proto.Message):
        r"""A wrapper proto presenting all supported resources. Only the
        resource of the change_resource_type will be set.

        Attributes:
            ad (google.ads.googleads.v7.resources.types.Ad):
                Output only. Set if change_resource_type == AD.
            ad_group (google.ads.googleads.v7.resources.types.AdGroup):
                Output only. Set if change_resource_type == AD_GROUP.
            ad_group_criterion (google.ads.googleads.v7.resources.types.AdGroupCriterion):
                Output only. Set if change_resource_type ==
                AD_GROUP_CRITERION.
            campaign (google.ads.googleads.v7.resources.types.Campaign):
                Output only. Set if change_resource_type == CAMPAIGN.
            campaign_budget (google.ads.googleads.v7.resources.types.CampaignBudget):
                Output only. Set if change_resource_type == CAMPAIGN_BUDGET.
            ad_group_bid_modifier (google.ads.googleads.v7.resources.types.AdGroupBidModifier):
                Output only. Set if change_resource_type ==
                AD_GROUP_BID_MODIFIER.
            campaign_criterion (google.ads.googleads.v7.resources.types.CampaignCriterion):
                Output only. Set if change_resource_type ==
                CAMPAIGN_CRITERION.
            feed (google.ads.googleads.v7.resources.types.Feed):
                Output only. Set if change_resource_type == FEED.
            feed_item (google.ads.googleads.v7.resources.types.FeedItem):
                Output only. Set if change_resource_type == FEED_ITEM.
            campaign_feed (google.ads.googleads.v7.resources.types.CampaignFeed):
                Output only. Set if change_resource_type == CAMPAIGN_FEED.
            ad_group_feed (google.ads.googleads.v7.resources.types.AdGroupFeed):
                Output only. Set if change_resource_type == AD_GROUP_FEED.
            ad_group_ad (google.ads.googleads.v7.resources.types.AdGroupAd):
                Output only. Set if change_resource_type == AD_GROUP_AD.
        """

        ad = proto.Field(proto.MESSAGE, number=1, message=gagr_ad.Ad,)
        ad_group = proto.Field(
            proto.MESSAGE, number=2, message=gagr_ad_group.AdGroup,
        )
        ad_group_criterion = proto.Field(
            proto.MESSAGE,
            number=3,
            message=gagr_ad_group_criterion.AdGroupCriterion,
        )
        campaign = proto.Field(
            proto.MESSAGE, number=4, message=gagr_campaign.Campaign,
        )
        campaign_budget = proto.Field(
            proto.MESSAGE,
            number=5,
            message=gagr_campaign_budget.CampaignBudget,
        )
        ad_group_bid_modifier = proto.Field(
            proto.MESSAGE,
            number=6,
            message=gagr_ad_group_bid_modifier.AdGroupBidModifier,
        )
        campaign_criterion = proto.Field(
            proto.MESSAGE,
            number=7,
            message=gagr_campaign_criterion.CampaignCriterion,
        )
        feed = proto.Field(proto.MESSAGE, number=8, message=gagr_feed.Feed,)
        feed_item = proto.Field(
            proto.MESSAGE, number=9, message=gagr_feed_item.FeedItem,
        )
        campaign_feed = proto.Field(
            proto.MESSAGE, number=10, message=gagr_campaign_feed.CampaignFeed,
        )
        ad_group_feed = proto.Field(
            proto.MESSAGE, number=11, message=gagr_ad_group_feed.AdGroupFeed,
        )
        ad_group_ad = proto.Field(
            proto.MESSAGE, number=12, message=gagr_ad_group_ad.AdGroupAd,
        )

    resource_name = proto.Field(proto.STRING, number=1,)
    change_date_time = proto.Field(proto.STRING, number=2,)
    change_resource_type = proto.Field(
        proto.ENUM,
        number=3,
        enum=change_event_resource_type.ChangeEventResourceTypeEnum.ChangeEventResourceType,
    )
    change_resource_name = proto.Field(proto.STRING, number=4,)
    client_type = proto.Field(
        proto.ENUM,
        number=5,
        enum=change_client_type.ChangeClientTypeEnum.ChangeClientType,
    )
    user_email = proto.Field(proto.STRING, number=6,)
    old_resource = proto.Field(
        proto.MESSAGE, number=7, message=ChangedResource,
    )
    new_resource = proto.Field(
        proto.MESSAGE, number=8, message=ChangedResource,
    )
    resource_change_operation = proto.Field(
        proto.ENUM,
        number=9,
        enum=gage_resource_change_operation.ResourceChangeOperationEnum.ResourceChangeOperation,
    )
    changed_fields = proto.Field(
        proto.MESSAGE, number=10, message=field_mask.FieldMask,
    )
    campaign = proto.Field(proto.STRING, number=11,)
    ad_group = proto.Field(proto.STRING, number=12,)
    feed = proto.Field(proto.STRING, number=13,)
    feed_item = proto.Field(proto.STRING, number=14,)


__all__ = tuple(sorted(__protobuf__.manifest))
