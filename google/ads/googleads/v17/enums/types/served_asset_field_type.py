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
    package="google.ads.googleads.v17.enums",
    marshal="google.ads.googleads.v17",
    manifest={
        "ServedAssetFieldTypeEnum",
    },
)


class ServedAssetFieldTypeEnum(proto.Message):
    r"""Container for enum describing possible asset field types."""

    class ServedAssetFieldType(proto.Enum):
        r"""The possible asset field types."""
        UNSPECIFIED = 0
        UNKNOWN = 1
        HEADLINE_1 = 2
        HEADLINE_2 = 3
        HEADLINE_3 = 4
        DESCRIPTION_1 = 5
        DESCRIPTION_2 = 6
        HEADLINE = 7
        HEADLINE_IN_PORTRAIT = 8
        LONG_HEADLINE = 9
        DESCRIPTION = 10
        DESCRIPTION_IN_PORTRAIT = 11
        BUSINESS_NAME_IN_PORTRAIT = 12
        BUSINESS_NAME = 13
        MARKETING_IMAGE = 14
        MARKETING_IMAGE_IN_PORTRAIT = 15
        SQUARE_MARKETING_IMAGE = 16
        PORTRAIT_MARKETING_IMAGE = 17
        LOGO = 18
        LANDSCAPE_LOGO = 19
        CALL_TO_ACTION = 20
        YOU_TUBE_VIDEO = 21
        SITELINK = 22
        CALL = 23
        MOBILE_APP = 24
        CALLOUT = 25
        STRUCTURED_SNIPPET = 26
        PRICE = 27
        PROMOTION = 28
        AD_IMAGE = 29
        LEAD_FORM = 30
        BUSINESS_LOGO = 31


__all__ = tuple(sorted(__protobuf__.manifest))
