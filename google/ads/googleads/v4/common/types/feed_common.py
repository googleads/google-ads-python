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
    manifest={"Money",},
)


class Money(proto.Message):
    r"""Represents a price in a particular currency.

    Attributes:
        currency_code (google.protobuf.wrappers_pb2.StringValue):
            Three-character ISO 4217 currency code.
        amount_micros (google.protobuf.wrappers_pb2.Int64Value):
            Amount in micros. One million is equivalent
            to one unit.
    """

    currency_code = proto.Field(
        proto.MESSAGE, number=1, message=wrappers.StringValue,
    )
    amount_micros = proto.Field(
        proto.MESSAGE, number=2, message=wrappers.Int64Value,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
