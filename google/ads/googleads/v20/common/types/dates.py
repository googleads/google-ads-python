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

from google.ads.googleads.v20.enums.types import month_of_year


__protobuf__ = proto.module(
    package="google.ads.googleads.v20.common",
    marshal="google.ads.googleads.v20",
    manifest={
        "DateRange",
        "YearMonthRange",
        "YearMonth",
    },
)


class DateRange(proto.Message):
    r"""A date range.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        start_date (str):
            The start date, in yyyy-mm-dd format. This
            date is inclusive.

            This field is a member of `oneof`_ ``_start_date``.
        end_date (str):
            The end date, in yyyy-mm-dd format. This date
            is inclusive.

            This field is a member of `oneof`_ ``_end_date``.
    """

    start_date: str = proto.Field(
        proto.STRING,
        number=3,
        optional=True,
    )
    end_date: str = proto.Field(
        proto.STRING,
        number=4,
        optional=True,
    )


class YearMonthRange(proto.Message):
    r"""The year month range inclusive of the start and end months.
    Eg: A year month range to represent Jan 2020 would be: (Jan
    2020, Jan 2020).

    Attributes:
        start (google.ads.googleads.v20.common.types.YearMonth):
            The inclusive start year month.
        end (google.ads.googleads.v20.common.types.YearMonth):
            The inclusive end year month.
    """

    start: "YearMonth" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="YearMonth",
    )
    end: "YearMonth" = proto.Field(
        proto.MESSAGE,
        number=2,
        message="YearMonth",
    )


class YearMonth(proto.Message):
    r"""Year month.

    Attributes:
        year (int):
            The year (for example, 2020).
        month (google.ads.googleads.v20.enums.types.MonthOfYearEnum.MonthOfYear):
            The month of the year. (for example,
            FEBRUARY).
    """

    year: int = proto.Field(
        proto.INT64,
        number=1,
    )
    month: month_of_year.MonthOfYearEnum.MonthOfYear = proto.Field(
        proto.ENUM,
        number=2,
        enum=month_of_year.MonthOfYearEnum.MonthOfYear,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
