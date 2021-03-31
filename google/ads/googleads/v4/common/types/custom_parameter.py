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
    manifest={"CustomParameter",},
)


class CustomParameter(proto.Message):
    r"""A mapping that can be used by custom parameter tags in a
    ``tracking_url_template``, ``final_urls``, or ``mobile_final_urls``.

    Attributes:
        key (google.protobuf.wrappers_pb2.StringValue):
            The key matching the parameter tag name.
        value (google.protobuf.wrappers_pb2.StringValue):
            The value to be substituted.
    """

    key = proto.Field(proto.MESSAGE, number=1, message=wrappers.StringValue,)
    value = proto.Field(proto.MESSAGE, number=2, message=wrappers.StringValue,)


__all__ = tuple(sorted(__protobuf__.manifest))
