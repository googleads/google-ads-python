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
    manifest={"CurrencyConstant",},
)


class CurrencyConstant(proto.Message):
    r"""A currency constant.

    Attributes:
        resource_name (str):
            Output only. The resource name of the currency constant.
            Currency constant resource names have the form:

            ``currencyConstants/{code}``
        code (google.protobuf.wrappers_pb2.StringValue):
            Output only. ISO 4217 three-letter currency
            code, e.g. "USD".
        name (google.protobuf.wrappers_pb2.StringValue):
            Output only. Full English name of the
            currency.
        symbol (google.protobuf.wrappers_pb2.StringValue):
            Output only. Standard symbol for describing
            this currency, e.g. '$' for US Dollars.
        billable_unit_micros (google.protobuf.wrappers_pb2.Int64Value):
            Output only. The billable unit for this
            currency. Billed amounts should be multiples of
            this value.
    """

    resource_name = proto.Field(proto.STRING, number=1)
    code = proto.Field(proto.MESSAGE, number=2, message=wrappers.StringValue,)
    name = proto.Field(proto.MESSAGE, number=3, message=wrappers.StringValue,)
    symbol = proto.Field(proto.MESSAGE, number=4, message=wrappers.StringValue,)
    billable_unit_micros = proto.Field(
        proto.MESSAGE, number=5, message=wrappers.Int64Value,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
