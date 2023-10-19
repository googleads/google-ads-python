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


import proto  # type: ignore

from google.ads.googleads.v15.common.types import criteria
from google.ads.googleads.v15.enums.types import criterion_type


__protobuf__ = proto.module(
    package="google.ads.googleads.v15.resources",
    marshal="google.ads.googleads.v15",
    manifest={
        "SharedCriterion",
    },
)


class SharedCriterion(proto.Message):
    r"""A criterion belonging to a shared set.
    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        resource_name (str):
            Immutable. The resource name of the shared criterion. Shared
            set resource names have the form:

            ``customers/{customer_id}/sharedCriteria/{shared_set_id}~{criterion_id}``
        shared_set (str):
            Immutable. The shared set to which the shared
            criterion belongs.

            This field is a member of `oneof`_ ``_shared_set``.
        criterion_id (int):
            Output only. The ID of the criterion.

            This field is ignored for mutates.

            This field is a member of `oneof`_ ``_criterion_id``.
        type_ (google.ads.googleads.v15.enums.types.CriterionTypeEnum.CriterionType):
            Output only. The type of the criterion.
        keyword (google.ads.googleads.v15.common.types.KeywordInfo):
            Immutable. Keyword.

            This field is a member of `oneof`_ ``criterion``.
        youtube_video (google.ads.googleads.v15.common.types.YouTubeVideoInfo):
            Immutable. YouTube Video.

            This field is a member of `oneof`_ ``criterion``.
        youtube_channel (google.ads.googleads.v15.common.types.YouTubeChannelInfo):
            Immutable. YouTube Channel.

            This field is a member of `oneof`_ ``criterion``.
        placement (google.ads.googleads.v15.common.types.PlacementInfo):
            Immutable. Placement.

            This field is a member of `oneof`_ ``criterion``.
        mobile_app_category (google.ads.googleads.v15.common.types.MobileAppCategoryInfo):
            Immutable. Mobile App Category.

            This field is a member of `oneof`_ ``criterion``.
        mobile_application (google.ads.googleads.v15.common.types.MobileApplicationInfo):
            Immutable. Mobile application.

            This field is a member of `oneof`_ ``criterion``.
        brand (google.ads.googleads.v15.common.types.BrandInfo):
            Immutable. Brand.

            This field is a member of `oneof`_ ``criterion``.
    """

    resource_name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    shared_set: str = proto.Field(
        proto.STRING,
        number=10,
        optional=True,
    )
    criterion_id: int = proto.Field(
        proto.INT64,
        number=11,
        optional=True,
    )
    type_: criterion_type.CriterionTypeEnum.CriterionType = proto.Field(
        proto.ENUM,
        number=4,
        enum=criterion_type.CriterionTypeEnum.CriterionType,
    )
    keyword: criteria.KeywordInfo = proto.Field(
        proto.MESSAGE,
        number=3,
        oneof="criterion",
        message=criteria.KeywordInfo,
    )
    youtube_video: criteria.YouTubeVideoInfo = proto.Field(
        proto.MESSAGE,
        number=5,
        oneof="criterion",
        message=criteria.YouTubeVideoInfo,
    )
    youtube_channel: criteria.YouTubeChannelInfo = proto.Field(
        proto.MESSAGE,
        number=6,
        oneof="criterion",
        message=criteria.YouTubeChannelInfo,
    )
    placement: criteria.PlacementInfo = proto.Field(
        proto.MESSAGE,
        number=7,
        oneof="criterion",
        message=criteria.PlacementInfo,
    )
    mobile_app_category: criteria.MobileAppCategoryInfo = proto.Field(
        proto.MESSAGE,
        number=8,
        oneof="criterion",
        message=criteria.MobileAppCategoryInfo,
    )
    mobile_application: criteria.MobileApplicationInfo = proto.Field(
        proto.MESSAGE,
        number=9,
        oneof="criterion",
        message=criteria.MobileApplicationInfo,
    )
    brand: criteria.BrandInfo = proto.Field(
        proto.MESSAGE,
        number=12,
        oneof="criterion",
        message=criteria.BrandInfo,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
