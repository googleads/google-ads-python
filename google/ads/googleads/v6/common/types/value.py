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


__protobuf__ = proto.module(
    package="google.ads.googleads.v6.common",
    marshal="google.ads.googleads.v6",
    manifest={"Value",},
)


class Value(proto.Message):
    r"""A generic data container.

    Attributes:
        boolean_value (bool):
            A boolean.
        int64_value (int):
            An int64.
        float_value (float):
            A float.
        double_value (float):
            A double.
        string_value (str):
            A string.
    """

    boolean_value = proto.Field(proto.BOOL, number=1, oneof="value")
    int64_value = proto.Field(proto.INT64, number=2, oneof="value")
    float_value = proto.Field(proto.FLOAT, number=3, oneof="value")
    double_value = proto.Field(proto.DOUBLE, number=4, oneof="value")
    string_value = proto.Field(proto.STRING, number=5, oneof="value")


__all__ = tuple(sorted(__protobuf__.manifest))
