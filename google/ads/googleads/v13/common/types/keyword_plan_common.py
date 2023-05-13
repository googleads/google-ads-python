# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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

from typing import MutableSequence

import proto  # type: ignore

from google.ads.googleads.v13.common.types import dates
from google.ads.googleads.v13.enums.types import device as gage_device
from google.ads.googleads.v13.enums.types import (
    keyword_plan_aggregate_metric_type,
)
from google.ads.googleads.v13.enums.types import keyword_plan_competition_level
from google.ads.googleads.v13.enums.types import keyword_plan_concept_group_type
from google.ads.googleads.v13.enums.types import month_of_year


__protobuf__ = proto.module(
    package="google.ads.googleads.v13.common",
    marshal="google.ads.googleads.v13",
    manifest={
        "KeywordPlanHistoricalMetrics",
        "HistoricalMetricsOptions",
        "MonthlySearchVolume",
        "KeywordPlanAggregateMetrics",
        "KeywordPlanAggregateMetricResults",
        "KeywordPlanDeviceSearches",
        "KeywordAnnotations",
        "KeywordConcept",
        "ConceptGroup",
    },
)


class KeywordPlanHistoricalMetrics(proto.Message):
    r"""Historical metrics specific to the targeting options
    selected. Targeting options include geographies, network, and so
    on. Refer to
    https://support.google.com/google-ads/answer/3022575 for more
    details.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        avg_monthly_searches (int):
            Approximate number of monthly searches on
            this query, averaged for the past 12 months.

            This field is a member of `oneof`_ ``_avg_monthly_searches``.
        monthly_search_volumes (MutableSequence[google.ads.googleads.v13.common.types.MonthlySearchVolume]):
            Approximate number of searches on this query
            for the past twelve months.
        competition (google.ads.googleads.v13.enums.types.KeywordPlanCompetitionLevelEnum.KeywordPlanCompetitionLevel):
            The competition level for the query.
        competition_index (int):
            The competition index for the query in the range [0, 100].
            Shows how competitive ad placement is for a keyword. The
            level of competition from 0-100 is determined by the number
            of ad slots filled divided by the total number of ad slots
            available. If not enough data is available, null is
            returned.

            This field is a member of `oneof`_ ``_competition_index``.
        low_top_of_page_bid_micros (int):
            Top of page bid low range (20th percentile)
            in micros for the keyword.

            This field is a member of `oneof`_ ``_low_top_of_page_bid_micros``.
        high_top_of_page_bid_micros (int):
            Top of page bid high range (80th percentile)
            in micros for the keyword.

            This field is a member of `oneof`_ ``_high_top_of_page_bid_micros``.
        average_cpc_micros (int):
            Average Cost Per Click in micros for the
            keyword.

            This field is a member of `oneof`_ ``_average_cpc_micros``.
    """

    avg_monthly_searches: int = proto.Field(
        proto.INT64, number=7, optional=True,
    )
    monthly_search_volumes: MutableSequence[
        "MonthlySearchVolume"
    ] = proto.RepeatedField(
        proto.MESSAGE, number=6, message="MonthlySearchVolume",
    )
    competition: keyword_plan_competition_level.KeywordPlanCompetitionLevelEnum.KeywordPlanCompetitionLevel = proto.Field(
        proto.ENUM,
        number=2,
        enum=keyword_plan_competition_level.KeywordPlanCompetitionLevelEnum.KeywordPlanCompetitionLevel,
    )
    competition_index: int = proto.Field(
        proto.INT64, number=8, optional=True,
    )
    low_top_of_page_bid_micros: int = proto.Field(
        proto.INT64, number=9, optional=True,
    )
    high_top_of_page_bid_micros: int = proto.Field(
        proto.INT64, number=10, optional=True,
    )
    average_cpc_micros: int = proto.Field(
        proto.INT64, number=11, optional=True,
    )


class HistoricalMetricsOptions(proto.Message):
    r"""Historical metrics options.
    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        year_month_range (google.ads.googleads.v13.common.types.YearMonthRange):
            The year month range for historical metrics. If not
            specified, metrics for the past 12 months are returned.
            Search metrics are available for the past 4 years. If the
            search volume is not available for the entire
            year_month_range provided, the subset of the year month
            range for which search volume is available are returned.

            This field is a member of `oneof`_ ``_year_month_range``.
        include_average_cpc (bool):
            Indicates whether to include average cost per
            click value. Average CPC is provided only for
            legacy support.
    """

    year_month_range: dates.YearMonthRange = proto.Field(
        proto.MESSAGE, number=1, optional=True, message=dates.YearMonthRange,
    )
    include_average_cpc: bool = proto.Field(
        proto.BOOL, number=2,
    )


class MonthlySearchVolume(proto.Message):
    r"""Monthly search volume.
    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        year (int):
            The year of the search volume (for example,
            2020).

            This field is a member of `oneof`_ ``_year``.
        month (google.ads.googleads.v13.enums.types.MonthOfYearEnum.MonthOfYear):
            The month of the search volume.
        monthly_searches (int):
            Approximate number of searches for the month.
            A null value indicates the search volume is
            unavailable for that month.

            This field is a member of `oneof`_ ``_monthly_searches``.
    """

    year: int = proto.Field(
        proto.INT64, number=4, optional=True,
    )
    month: month_of_year.MonthOfYearEnum.MonthOfYear = proto.Field(
        proto.ENUM, number=2, enum=month_of_year.MonthOfYearEnum.MonthOfYear,
    )
    monthly_searches: int = proto.Field(
        proto.INT64, number=5, optional=True,
    )


class KeywordPlanAggregateMetrics(proto.Message):
    r"""The aggregate metrics specification of the request.
    Attributes:
        aggregate_metric_types (MutableSequence[google.ads.googleads.v13.enums.types.KeywordPlanAggregateMetricTypeEnum.KeywordPlanAggregateMetricType]):
            The list of aggregate metrics to fetch data.
    """

    aggregate_metric_types: MutableSequence[
        keyword_plan_aggregate_metric_type.KeywordPlanAggregateMetricTypeEnum.KeywordPlanAggregateMetricType
    ] = proto.RepeatedField(
        proto.ENUM,
        number=1,
        enum=keyword_plan_aggregate_metric_type.KeywordPlanAggregateMetricTypeEnum.KeywordPlanAggregateMetricType,
    )


class KeywordPlanAggregateMetricResults(proto.Message):
    r"""The aggregated historical metrics for keyword plan keywords.
    Attributes:
        device_searches (MutableSequence[google.ads.googleads.v13.common.types.KeywordPlanDeviceSearches]):
            The aggregate searches for all the keywords
            segmented by device for the specified time.
            Supports the following device types: MOBILE,
            TABLET, DESKTOP.
            This is only set when
            KeywordPlanAggregateMetricTypeEnum.DEVICE is set
            in the KeywordPlanAggregateMetrics field in the
            request.
    """

    device_searches: MutableSequence[
        "KeywordPlanDeviceSearches"
    ] = proto.RepeatedField(
        proto.MESSAGE, number=1, message="KeywordPlanDeviceSearches",
    )


class KeywordPlanDeviceSearches(proto.Message):
    r"""The total searches for the device type during the specified
    time period.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        device (google.ads.googleads.v13.enums.types.DeviceEnum.Device):
            The device type.
        search_count (int):
            The total searches for the device.

            This field is a member of `oneof`_ ``_search_count``.
    """

    device: gage_device.DeviceEnum.Device = proto.Field(
        proto.ENUM, number=1, enum=gage_device.DeviceEnum.Device,
    )
    search_count: int = proto.Field(
        proto.INT64, number=2, optional=True,
    )


class KeywordAnnotations(proto.Message):
    r"""The annotations for the keyword plan keywords.
    Attributes:
        concepts (MutableSequence[google.ads.googleads.v13.common.types.KeywordConcept]):
            The list of concepts for the keyword.
    """

    concepts: MutableSequence["KeywordConcept"] = proto.RepeatedField(
        proto.MESSAGE, number=1, message="KeywordConcept",
    )


class KeywordConcept(proto.Message):
    r"""The concept for the keyword.
    Attributes:
        name (str):
            The concept name for the keyword in the concept_group.
        concept_group (google.ads.googleads.v13.common.types.ConceptGroup):
            The concept group of the concept details.
    """

    name: str = proto.Field(
        proto.STRING, number=1,
    )
    concept_group: "ConceptGroup" = proto.Field(
        proto.MESSAGE, number=2, message="ConceptGroup",
    )


class ConceptGroup(proto.Message):
    r"""The concept group for the keyword concept.
    Attributes:
        name (str):
            The concept group name.
        type_ (google.ads.googleads.v13.enums.types.KeywordPlanConceptGroupTypeEnum.KeywordPlanConceptGroupType):
            The concept group type.
    """

    name: str = proto.Field(
        proto.STRING, number=1,
    )
    type_: keyword_plan_concept_group_type.KeywordPlanConceptGroupTypeEnum.KeywordPlanConceptGroupType = proto.Field(
        proto.ENUM,
        number=2,
        enum=keyword_plan_concept_group_type.KeywordPlanConceptGroupTypeEnum.KeywordPlanConceptGroupType,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
