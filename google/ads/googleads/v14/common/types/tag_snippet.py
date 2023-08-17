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

from google.ads.googleads.v14.enums.types import tracking_code_page_format
from google.ads.googleads.v14.enums.types import tracking_code_type


__protobuf__ = proto.module(
    package="google.ads.googleads.v14.common",
    marshal="google.ads.googleads.v14",
    manifest={
        "TagSnippet",
    },
)


class TagSnippet(proto.Message):
    r"""The site tag and event snippet pair for a TrackingCodeType.
    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        type_ (google.ads.googleads.v14.enums.types.TrackingCodeTypeEnum.TrackingCodeType):
            The type of the generated tag snippets for
            tracking conversions.
        page_format (google.ads.googleads.v14.enums.types.TrackingCodePageFormatEnum.TrackingCodePageFormat):
            The format of the web page where the tracking
            tag and snippet will be installed, for example,
            HTML.
        global_site_tag (str):
            The site tag that adds visitors to your basic
            remarketing lists and sets new cookies on your
            domain.

            This field is a member of `oneof`_ ``_global_site_tag``.
        event_snippet (str):
            The event snippet that works with the site
            tag to track actions that should be counted as
            conversions.

            This field is a member of `oneof`_ ``_event_snippet``.
    """

    type_: tracking_code_type.TrackingCodeTypeEnum.TrackingCodeType = (
        proto.Field(
            proto.ENUM,
            number=1,
            enum=tracking_code_type.TrackingCodeTypeEnum.TrackingCodeType,
        )
    )
    page_format: tracking_code_page_format.TrackingCodePageFormatEnum.TrackingCodePageFormat = proto.Field(
        proto.ENUM,
        number=2,
        enum=tracking_code_page_format.TrackingCodePageFormatEnum.TrackingCodePageFormat,
    )
    global_site_tag: str = proto.Field(
        proto.STRING,
        number=5,
        optional=True,
    )
    event_snippet: str = proto.Field(
        proto.STRING,
        number=6,
        optional=True,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
