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


from google.ads.googleads.v5.enums.types import (
    placement_type as gage_placement_type,
)
from google.protobuf import wrappers_pb2 as wrappers  # type: ignore


__protobuf__ = proto.module(
    package="google.ads.googleads.v5.resources",
    marshal="google.ads.googleads.v5",
    manifest={"GroupPlacementView",},
)


class GroupPlacementView(proto.Message):
    r"""A group placement view.

    Attributes:
        resource_name (str):
            Output only. The resource name of the group placement view.
            Group placement view resource names have the form:

            ``customers/{customer_id}/groupPlacementViews/{ad_group_id}~{base64_placement}``
        placement (google.protobuf.wrappers_pb2.StringValue):
            Output only. The automatic placement string
            at group level, e. g. web domain, mobile app ID,
            or a YouTube channel ID.
        display_name (google.protobuf.wrappers_pb2.StringValue):
            Output only. Domain name for websites and
            YouTube channel name for YouTube channels.
        target_url (google.protobuf.wrappers_pb2.StringValue):
            Output only. URL of the group placement, e.g.
            domain, link to the mobile application in app
            store, or a YouTube channel URL.
        placement_type (google.ads.googleads.v5.enums.types.PlacementTypeEnum.PlacementType):
            Output only. Type of the placement, e.g.
            Website, YouTube Channel, Mobile Application.
    """

    resource_name = proto.Field(proto.STRING, number=1)
    placement = proto.Field(
        proto.MESSAGE, number=2, message=wrappers.StringValue,
    )
    display_name = proto.Field(
        proto.MESSAGE, number=3, message=wrappers.StringValue,
    )
    target_url = proto.Field(
        proto.MESSAGE, number=4, message=wrappers.StringValue,
    )
    placement_type = proto.Field(
        proto.ENUM,
        number=5,
        enum=gage_placement_type.PlacementTypeEnum.PlacementType,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
