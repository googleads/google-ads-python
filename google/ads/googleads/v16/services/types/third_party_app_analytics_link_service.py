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


import proto  # type: ignore


__protobuf__ = proto.module(
    package="google.ads.googleads.v16.services",
    marshal="google.ads.googleads.v16",
    manifest={
        "RegenerateShareableLinkIdRequest",
        "RegenerateShareableLinkIdResponse",
    },
)


class RegenerateShareableLinkIdRequest(proto.Message):
    r"""Request message for
    [ThirdPartyAppAnalyticsLinkService.RegenerateShareableLinkId][google.ads.googleads.v16.services.ThirdPartyAppAnalyticsLinkService.RegenerateShareableLinkId].

    Attributes:
        resource_name (str):
            Resource name of the third party app
            analytics link.
    """

    resource_name: str = proto.Field(
        proto.STRING,
        number=1,
    )


class RegenerateShareableLinkIdResponse(proto.Message):
    r"""Response message for
    [ThirdPartyAppAnalyticsLinkService.RegenerateShareableLinkId][google.ads.googleads.v16.services.ThirdPartyAppAnalyticsLinkService.RegenerateShareableLinkId].

    """


__all__ = tuple(sorted(__protobuf__.manifest))
