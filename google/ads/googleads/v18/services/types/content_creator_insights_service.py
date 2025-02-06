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

from google.ads.googleads.v18.common.types import audience_insights_attribute
from google.ads.googleads.v18.common.types import criteria


__protobuf__ = proto.module(
    package="google.ads.googleads.v18.services",
    marshal="google.ads.googleads.v18",
    manifest={
        "GenerateCreatorInsightsRequest",
        "GenerateCreatorInsightsResponse",
        "YouTubeCreatorInsights",
        "YouTubeMetrics",
        "YouTubeChannelInsights",
    },
)


class GenerateCreatorInsightsRequest(proto.Message):
    r"""Request message for
    [ContentCreatorInsightsService.GenerateCreatorInsights]

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        customer_id (str):
            Required. The ID of the customer.
        customer_insights_group (str):
            Required. The name of the customer being
            planned for.  This is a user-defined value.
        search_attributes (google.ads.googleads.v18.services.types.GenerateCreatorInsightsRequest.SearchAttributes):
            The list of attributes to search for top
            creators in.

            This field is a member of `oneof`_ ``criteria``.
        search_channels (google.ads.googleads.v18.services.types.GenerateCreatorInsightsRequest.YouTubeChannels):
            The list of YouTube Channel IDs to fetch
            creator insights for.

            This field is a member of `oneof`_ ``criteria``.
    """

    class SearchAttributes(proto.Message):
        r"""The audience attributes (such as Age, Gender, Affinity, and
        In-Market) and creator attributes (such as creator location and
        creator's content topics) used to search for top creators.

        Attributes:
            audience_attributes (MutableSequence[google.ads.googleads.v18.common.types.AudienceInsightsAttribute]):
                Optional. Audience attributes that describe
                an audience of viewers. This is used to search
                for creators whose own viewers match the input
                audience.
            creator_attributes (MutableSequence[google.ads.googleads.v18.common.types.AudienceInsightsAttribute]):
                Optional. Creator attributes that describe a
                collection of types of content. This is used to
                search for creators whose content matches the
                input creator attributes.
        """

        audience_attributes: MutableSequence[
            audience_insights_attribute.AudienceInsightsAttribute
        ] = proto.RepeatedField(
            proto.MESSAGE,
            number=1,
            message=audience_insights_attribute.AudienceInsightsAttribute,
        )
        creator_attributes: MutableSequence[
            audience_insights_attribute.AudienceInsightsAttribute
        ] = proto.RepeatedField(
            proto.MESSAGE,
            number=2,
            message=audience_insights_attribute.AudienceInsightsAttribute,
        )

    class YouTubeChannels(proto.Message):
        r"""A collection of YouTube Channels.
        Attributes:
            youtube_channels (MutableSequence[google.ads.googleads.v18.common.types.YouTubeChannelInfo]):
                Optional. The YouTube Channel IDs to fetch
                creator insights for.
        """

        youtube_channels: MutableSequence[
            criteria.YouTubeChannelInfo
        ] = proto.RepeatedField(
            proto.MESSAGE, number=1, message=criteria.YouTubeChannelInfo,
        )

    customer_id: str = proto.Field(
        proto.STRING, number=1,
    )
    customer_insights_group: str = proto.Field(
        proto.STRING, number=2,
    )
    search_attributes: SearchAttributes = proto.Field(
        proto.MESSAGE, number=3, oneof="criteria", message=SearchAttributes,
    )
    search_channels: YouTubeChannels = proto.Field(
        proto.MESSAGE, number=4, oneof="criteria", message=YouTubeChannels,
    )


class GenerateCreatorInsightsResponse(proto.Message):
    r"""Response message for
    [ContentCreatorInsightsService.GenerateCreatorInsights]

    Attributes:
        creator_insights (MutableSequence[google.ads.googleads.v18.services.types.YouTubeCreatorInsights]):
            A collection of YouTube Creators, each
            containing a collection of YouTube Channels
            maintained by the YouTube Creator.
    """

    creator_insights: MutableSequence[
        "YouTubeCreatorInsights"
    ] = proto.RepeatedField(
        proto.MESSAGE, number=1, message="YouTubeCreatorInsights",
    )


class YouTubeCreatorInsights(proto.Message):
    r"""A YouTube creator and the insights for this creator.
    Attributes:
        creator_name (str):
            The name of the creator.
        creator_channels (MutableSequence[google.ads.googleads.v18.services.types.YouTubeChannelInsights]):
            The list of YouTube Channels
    """

    creator_name: str = proto.Field(
        proto.STRING, number=1,
    )
    creator_channels: MutableSequence[
        "YouTubeChannelInsights"
    ] = proto.RepeatedField(
        proto.MESSAGE, number=2, message="YouTubeChannelInsights",
    )


class YouTubeMetrics(proto.Message):
    r"""YouTube Channel metrics.
    Attributes:
        subscriber_count (int):
            The number of subscribers.
        views_count (int):
            The total number of views.
    """

    subscriber_count: int = proto.Field(
        proto.INT64, number=1,
    )
    views_count: int = proto.Field(
        proto.INT64, number=2,
    )


class YouTubeChannelInsights(proto.Message):
    r"""YouTube Channel insights, and its metadata (such as channel
    name and channel ID), returned for a creator insights response.

    Attributes:
        display_name (str):
            The name of the YouTube Channel.
        youtube_channel (google.ads.googleads.v18.common.types.YouTubeChannelInfo):
            The YouTube Channel ID.
        channel_metrics (google.ads.googleads.v18.services.types.YouTubeMetrics):
            The metrics for a YouTube Channel.
        channel_audience_demographics (MutableSequence[google.ads.googleads.v18.common.types.AudienceInsightsAttributeMetadata]):
            The types of audiences and demographics
            associated with a channel's main audience.
            Audiences and demographics will have a breakdown
            of subscriber share across dimensions of the
            same value.
        channel_attributes (MutableSequence[google.ads.googleads.v18.common.types.AudienceInsightsAttributeMetadata]):
            The attributes associated with the content
            made by a channel.
        channel_type (str):
            Metadata string associated with the type of
            channel.
    """

    display_name: str = proto.Field(
        proto.STRING, number=1,
    )
    youtube_channel: criteria.YouTubeChannelInfo = proto.Field(
        proto.MESSAGE, number=2, message=criteria.YouTubeChannelInfo,
    )
    channel_metrics: "YouTubeMetrics" = proto.Field(
        proto.MESSAGE, number=3, message="YouTubeMetrics",
    )
    channel_audience_demographics: MutableSequence[
        audience_insights_attribute.AudienceInsightsAttributeMetadata
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=4,
        message=audience_insights_attribute.AudienceInsightsAttributeMetadata,
    )
    channel_attributes: MutableSequence[
        audience_insights_attribute.AudienceInsightsAttributeMetadata
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=5,
        message=audience_insights_attribute.AudienceInsightsAttributeMetadata,
    )
    channel_type: str = proto.Field(
        proto.STRING, number=6,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
