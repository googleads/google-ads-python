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


from google.ads.googleads.v4.enums.types import keyword_plan_competition_level
from google.ads.googleads.v4.enums.types import month_of_year
from google.protobuf import wrappers_pb2 as wrappers  # type: ignore


__protobuf__ = proto.module(
    package="google.ads.googleads.v4.common",
    marshal="google.ads.googleads.v4",
    manifest={"KeywordPlanHistoricalMetrics", "MonthlySearchVolume",},
)


class KeywordPlanHistoricalMetrics(proto.Message):
    r"""Historical metrics specific to the targeting options
    selected. Targeting options include geographies, network, etc.
    Refer to https://support.google.com/google-ads/answer/3022575
    for more details.

    Attributes:
        avg_monthly_searches (google.protobuf.wrappers_pb2.Int64Value):
            Approximate number of monthly searches on
            this query averaged for the past 12 months.
        monthly_search_volumes (Sequence[google.ads.googleads.v4.common.types.MonthlySearchVolume]):
            Approximate number of searches on this query
            for the past twelve months.
        competition (google.ads.googleads.v4.enums.types.KeywordPlanCompetitionLevelEnum.KeywordPlanCompetitionLevel):
            The competition level for the query.
        competition_index (google.protobuf.wrappers_pb2.Int64Value):
            The competition index for the query in the range [0, 100].
            Shows how competitive ad placement is for a keyword. The
            level of competition from 0-100 is determined by the number
            of ad slots filled divided by the total number of ad slots
            available. If not enough data is available, null is
            returned.
        low_top_of_page_bid_micros (google.protobuf.wrappers_pb2.Int64Value):
            Top of page bid low range (20th percentile)
            in micros for the keyword.
        high_top_of_page_bid_micros (google.protobuf.wrappers_pb2.Int64Value):
            Top of page bid high range (80th percentile)
            in micros for the keyword.
    """

    avg_monthly_searches = proto.Field(
        proto.MESSAGE, number=1, message=wrappers.Int64Value,
    )
    monthly_search_volumes = proto.RepeatedField(
        proto.MESSAGE, number=6, message="MonthlySearchVolume",
    )
    competition = proto.Field(
        proto.ENUM,
        number=2,
        enum=keyword_plan_competition_level.KeywordPlanCompetitionLevelEnum.KeywordPlanCompetitionLevel,
    )
    competition_index = proto.Field(
        proto.MESSAGE, number=3, message=wrappers.Int64Value,
    )
    low_top_of_page_bid_micros = proto.Field(
        proto.MESSAGE, number=4, message=wrappers.Int64Value,
    )
    high_top_of_page_bid_micros = proto.Field(
        proto.MESSAGE, number=5, message=wrappers.Int64Value,
    )


class MonthlySearchVolume(proto.Message):
    r"""Monthly search volume.

    Attributes:
        year (google.protobuf.wrappers_pb2.Int64Value):
            The year of the search volume (e.g. 2020).
        month (google.ads.googleads.v4.enums.types.MonthOfYearEnum.MonthOfYear):
            The month of the search volume.
        monthly_searches (google.protobuf.wrappers_pb2.Int64Value):
            Approximate number of searches for the month.
            A null value indicates the search volume is
            unavailable for that month.
    """

    year = proto.Field(proto.MESSAGE, number=1, message=wrappers.Int64Value,)
    month = proto.Field(
        proto.ENUM, number=2, enum=month_of_year.MonthOfYearEnum.MonthOfYear,
    )
    monthly_searches = proto.Field(
        proto.MESSAGE, number=3, message=wrappers.Int64Value,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
