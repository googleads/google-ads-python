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


from google.protobuf import wrappers_pb2 as wrappers  # type: ignore


__protobuf__ = proto.module(
    package="google.ads.googleads.v4.resources",
    marshal="google.ads.googleads.v4",
    manifest={"DynamicSearchAdsSearchTermView",},
)


class DynamicSearchAdsSearchTermView(proto.Message):
    r"""A dynamic search ads search term view.

    Attributes:
        resource_name (str):
            Output only. The resource name of the dynamic search ads
            search term view. Dynamic search ads search term view
            resource names have the form:

            ``customers/{customer_id}/dynamicSearchAdsSearchTermViews/{ad_group_id}~{search_term_fingerprint}~{headline_fingerprint}~{landing_page_fingerprint}~{page_url_fingerprint}``
        search_term (google.protobuf.wrappers_pb2.StringValue):
            Output only. Search term
            This field is read-only.
        headline (google.protobuf.wrappers_pb2.StringValue):
            Output only. The dynamically generated
            headline of the Dynamic Search Ad.
            This field is read-only.
        landing_page (google.protobuf.wrappers_pb2.StringValue):
            Output only. The dynamically selected landing
            page URL of the impression.
            This field is read-only.
        page_url (google.protobuf.wrappers_pb2.StringValue):
            Output only. The URL of page feed item served
            for the impression.
            This field is read-only.
        has_negative_keyword (google.protobuf.wrappers_pb2.BoolValue):
            Output only. True if query matches a negative
            keyword.
            This field is read-only.
        has_matching_keyword (google.protobuf.wrappers_pb2.BoolValue):
            Output only. True if query is added to
            targeted keywords.
            This field is read-only.
        has_negative_url (google.protobuf.wrappers_pb2.BoolValue):
            Output only. True if query matches a negative
            url.
            This field is read-only.
    """

    resource_name = proto.Field(proto.STRING, number=1)
    search_term = proto.Field(
        proto.MESSAGE, number=2, message=wrappers.StringValue,
    )
    headline = proto.Field(
        proto.MESSAGE, number=3, message=wrappers.StringValue,
    )
    landing_page = proto.Field(
        proto.MESSAGE, number=4, message=wrappers.StringValue,
    )
    page_url = proto.Field(
        proto.MESSAGE, number=5, message=wrappers.StringValue,
    )
    has_negative_keyword = proto.Field(
        proto.MESSAGE, number=6, message=wrappers.BoolValue,
    )
    has_matching_keyword = proto.Field(
        proto.MESSAGE, number=7, message=wrappers.BoolValue,
    )
    has_negative_url = proto.Field(
        proto.MESSAGE, number=8, message=wrappers.BoolValue,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
