# -*- coding: utf-8 -*-
# Copyright 2025 Google LLC
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


__protobuf__ = proto.module(
    package="google.ads.googleads.v20.enums",
    marshal="google.ads.googleads.v20",
    manifest={
        "MonthOfYearEnum",
    },
)


class MonthOfYearEnum(proto.Message):
    r"""Container for enumeration of months of the year, for example,
    "January".

    """

    class MonthOfYear(proto.Enum):
        r"""Enumerates months of the year, for example, "January".

        Values:
            UNSPECIFIED (0):
                Not specified.
            UNKNOWN (1):
                The value is unknown in this version.
            JANUARY (2):
                January.
            FEBRUARY (3):
                February.
            MARCH (4):
                March.
            APRIL (5):
                April.
            MAY (6):
                May.
            JUNE (7):
                June.
            JULY (8):
                July.
            AUGUST (9):
                August.
            SEPTEMBER (10):
                September.
            OCTOBER (11):
                October.
            NOVEMBER (12):
                November.
            DECEMBER (13):
                December.
        """

        UNSPECIFIED = 0
        UNKNOWN = 1
        JANUARY = 2
        FEBRUARY = 3
        MARCH = 4
        APRIL = 5
        MAY = 6
        JUNE = 7
        JULY = 8
        AUGUST = 9
        SEPTEMBER = 10
        OCTOBER = 11
        NOVEMBER = 12
        DECEMBER = 13


__all__ = tuple(sorted(__protobuf__.manifest))
