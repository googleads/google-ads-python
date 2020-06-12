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
    manifest={"ClickLocation",},
)


class ClickLocation(proto.Message):
    r"""Location criteria associated with a click.

    Attributes:
        city (google.protobuf.wrappers_pb2.StringValue):
            The city location criterion associated with
            the impression.
        country (google.protobuf.wrappers_pb2.StringValue):
            The country location criterion associated
            with the impression.
        metro (google.protobuf.wrappers_pb2.StringValue):
            The metro location criterion associated with
            the impression.
        most_specific (google.protobuf.wrappers_pb2.StringValue):
            The most specific location criterion
            associated with the impression.
        region (google.protobuf.wrappers_pb2.StringValue):
            The region location criterion associated with
            the impression.
    """

    city = proto.Field(proto.MESSAGE, number=1, message=wrappers.StringValue,)
    country = proto.Field(
        proto.MESSAGE, number=2, message=wrappers.StringValue,
    )
    metro = proto.Field(proto.MESSAGE, number=3, message=wrappers.StringValue,)
    most_specific = proto.Field(
        proto.MESSAGE, number=4, message=wrappers.StringValue,
    )
    region = proto.Field(proto.MESSAGE, number=5, message=wrappers.StringValue,)


__all__ = tuple(sorted(__protobuf__.manifest))
