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
    package="google.ads.googleads.v5.common",
    marshal="google.ads.googleads.v5",
    manifest={"DateRange",},
)


class DateRange(proto.Message):
    r"""A date range.

    Attributes:
        start_date (google.protobuf.wrappers_pb2.StringValue):
            The start date, in yyyy-mm-dd format. This
            date is inclusive.
        end_date (google.protobuf.wrappers_pb2.StringValue):
            The end date, in yyyy-mm-dd format. This date
            is inclusive.
    """

    start_date = proto.Field(
        proto.MESSAGE, number=1, message=wrappers.StringValue,
    )
    end_date = proto.Field(
        proto.MESSAGE, number=2, message=wrappers.StringValue,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
