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
    package="google.ads.googleads.v4.common",
    marshal="google.ads.googleads.v4",
    manifest={"UrlCollection",},
)


class UrlCollection(proto.Message):
    r"""Collection of urls that is tagged with a unique identifier.

    Attributes:
        url_collection_id (google.protobuf.wrappers_pb2.StringValue):
            Unique identifier for this UrlCollection
            instance.
        final_urls (Sequence[google.protobuf.wrappers_pb2.StringValue]):
            A list of possible final URLs.
        final_mobile_urls (Sequence[google.protobuf.wrappers_pb2.StringValue]):
            A list of possible final mobile URLs.
        tracking_url_template (google.protobuf.wrappers_pb2.StringValue):
            URL template for constructing a tracking URL.
    """

    url_collection_id = proto.Field(
        proto.MESSAGE, number=1, message=wrappers.StringValue,
    )
    final_urls = proto.RepeatedField(
        proto.MESSAGE, number=2, message=wrappers.StringValue,
    )
    final_mobile_urls = proto.RepeatedField(
        proto.MESSAGE, number=3, message=wrappers.StringValue,
    )
    tracking_url_template = proto.Field(
        proto.MESSAGE, number=4, message=wrappers.StringValue,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
