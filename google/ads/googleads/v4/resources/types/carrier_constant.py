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
    manifest={"CarrierConstant",},
)


class CarrierConstant(proto.Message):
    r"""A carrier criterion that can be used in campaign targeting.

    Attributes:
        resource_name (str):
            Output only. The resource name of the carrier criterion.
            Carrier criterion resource names have the form:

            ``carrierConstants/{criterion_id}``
        id (google.protobuf.wrappers_pb2.Int64Value):
            Output only. The ID of the carrier criterion.
        name (google.protobuf.wrappers_pb2.StringValue):
            Output only. The full name of the carrier in
            English.
        country_code (google.protobuf.wrappers_pb2.StringValue):
            Output only. The country code of the country
            where the carrier is located, e.g., "AR", "FR",
            etc.
    """

    resource_name = proto.Field(proto.STRING, number=1)
    id = proto.Field(proto.MESSAGE, number=2, message=wrappers.Int64Value,)
    name = proto.Field(proto.MESSAGE, number=3, message=wrappers.StringValue,)
    country_code = proto.Field(
        proto.MESSAGE, number=4, message=wrappers.StringValue,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
