# -*- coding: utf-8 -*-
# Copyright 2024 Google LLC
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

from google.ads.googleads.v18.common.types import criteria
from google.ads.googleads.v18.common.types import dates
from google.ads.googleads.v18.enums.types import audience_insights_dimension
from google.ads.googleads.v18.enums.types import (
    audience_insights_marketing_objective,
)


__protobuf__ = proto.module(
    package="google.ads.googleads.v18.services",
    marshal="google.ads.googleads.v18",
    manifest={
        "GenerateInsightsFinderReportRequest",
        "GenerateInsightsFinderReportResponse",
        "GenerateAudienceCompositionInsightsRequest",
        "GenerateAudienceCompositionInsightsResponse",
        "GenerateSuggestedTargetingInsightsRequest",
        "GenerateSuggestedTargetingInsightsResponse",
        "TargetingSuggestionMetrics",
        "ListAudienceInsightsAttributesRequest",
        "ListAudienceInsightsAttributesResponse",
        "ListInsightsEligibleDatesRequest",
        "ListInsightsEligibleDatesResponse",
        "GenerateAudienceOverlapInsightsRequest",
        "GenerateAudienceOverlapInsightsResponse",
        "DimensionOverlapResult",
        "AudienceOverlapItem",
        "GenerateTargetingSuggestionMetricsRequest",
        "GenerateTargetingSuggestionMetricsResponse",
        "AudienceInsightsAttribute",
        "AudienceInsightsTopic",
        "AudienceInsightsEntity",
        "AudienceInsightsCategory",
        "AudienceInsightsDynamicLineup",
        "BasicInsightsAudience",
        "AudienceInsightsAttributeMetadata",
        "YouTubeChannelAttributeMetadata",
        "DynamicLineupAttributeMetadata",
        "LocationAttributeMetadata",
        "UserInterestAttributeMetadata",
        "InsightsAudienceDefinition",
        "InsightsAudienceDescription",
        "InsightsAudience",
        "InsightsAudienceAttributeGroup",
        "AudienceCompositionSection",
        "AudienceCompositionAttributeCluster",
        "AudienceCompositionMetrics",
        "AudienceCompositionAttribute",
    },
)


class GenerateInsightsFinderReportRequest(proto.Message):
    r"""Request message for
    [AudienceInsightsService.GenerateInsightsFinderReport][google.ads.googleads.v18.services.AudienceInsightsService.GenerateInsightsFinderReport].

    Attributes:
        customer_id (str):
            Required. The ID of the customer.
        baseline_audience (google.ads.googleads.v18.services.types.BasicInsightsAudience):
            Required. A baseline audience for this
            report, typically all people in a region.
        specific_audience (google.ads.googleads.v18.services.types.BasicInsightsAudience):
            Required. The specific audience of interest
            for this report.  The insights in the report
            will be based on attributes more prevalent in
            this audience than in the report's baseline
            audience.
        customer_insights_group (str):
            The name of the customer being planned for.
            This is a user-defined value.
    """

    customer_id: str = proto.Field(
        proto.STRING, number=1,
    )
    baseline_audience: "BasicInsightsAudience" = proto.Field(
        proto.MESSAGE, number=2, message="BasicInsightsAudience",
    )
    specific_audience: "BasicInsightsAudience" = proto.Field(
        proto.MESSAGE, number=3, message="BasicInsightsAudience",
    )
    customer_insights_group: str = proto.Field(
        proto.STRING, number=4,
    )


class GenerateInsightsFinderReportResponse(proto.Message):
    r"""The response message for
    [AudienceInsightsService.GenerateInsightsFinderReport][google.ads.googleads.v18.services.AudienceInsightsService.GenerateInsightsFinderReport],
    containing the shareable URL for the report.

    Attributes:
        saved_report_url (str):
            An HTTPS URL providing a deep link into the
            Insights Finder UI with the report inputs filled
            in according to the request.
    """

    saved_report_url: str = proto.Field(
        proto.STRING, number=1,
    )


class GenerateAudienceCompositionInsightsRequest(proto.Message):
    r"""Request message for
    [AudienceInsightsService.GenerateAudienceCompositionInsights][google.ads.googleads.v18.services.AudienceInsightsService.GenerateAudienceCompositionInsights].

    Attributes:
        customer_id (str):
            Required. The ID of the customer.
        audience (google.ads.googleads.v18.services.types.InsightsAudience):
            Required. The audience of interest for which
            insights are being requested.
        baseline_audience (google.ads.googleads.v18.services.types.InsightsAudience):
            The baseline audience to which the audience
            of interest is being compared.
        data_month (str):
            The one-month range of historical data to use
            for insights, in the format "yyyy-mm". If unset,
            insights will be returned for the last thirty
            days of data.
        dimensions (MutableSequence[google.ads.googleads.v18.enums.types.AudienceInsightsDimensionEnum.AudienceInsightsDimension]):
            Required. The audience dimensions for which
            composition insights should be returned.
        customer_insights_group (str):
            The name of the customer being planned for.
            This is a user-defined value.
    """

    customer_id: str = proto.Field(
        proto.STRING, number=1,
    )
    audience: "InsightsAudience" = proto.Field(
        proto.MESSAGE, number=2, message="InsightsAudience",
    )
    baseline_audience: "InsightsAudience" = proto.Field(
        proto.MESSAGE, number=6, message="InsightsAudience",
    )
    data_month: str = proto.Field(
        proto.STRING, number=3,
    )
    dimensions: MutableSequence[
        audience_insights_dimension.AudienceInsightsDimensionEnum.AudienceInsightsDimension
    ] = proto.RepeatedField(
        proto.ENUM,
        number=4,
        enum=audience_insights_dimension.AudienceInsightsDimensionEnum.AudienceInsightsDimension,
    )
    customer_insights_group: str = proto.Field(
        proto.STRING, number=5,
    )


class GenerateAudienceCompositionInsightsResponse(proto.Message):
    r"""Response message for
    [AudienceInsightsService.GenerateAudienceCompositionInsights][google.ads.googleads.v18.services.AudienceInsightsService.GenerateAudienceCompositionInsights].

    Attributes:
        sections (MutableSequence[google.ads.googleads.v18.services.types.AudienceCompositionSection]):
            The contents of the insights report,
            organized into sections. Each section is
            associated with one of the
            AudienceInsightsDimension values in the request.
            There may be more than one section per
            dimension.
    """

    sections: MutableSequence[
        "AudienceCompositionSection"
    ] = proto.RepeatedField(
        proto.MESSAGE, number=1, message="AudienceCompositionSection",
    )


class GenerateSuggestedTargetingInsightsRequest(proto.Message):
    r"""Request message for
    [AudienceInsightsService.GenerateSuggestedTargetingInsights][google.ads.googleads.v18.services.AudienceInsightsService.GenerateSuggestedTargetingInsights].

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        customer_id (str):
            Required. The ID of the customer.
        customer_insights_group (str):
            Optional. The name of the customer being
            planned for.  This is a user-defined value.
        audience_definition (google.ads.googleads.v18.services.types.InsightsAudienceDefinition):
            Provide a seed audience to get suggestions
            for.

            This field is a member of `oneof`_ ``audience_input``.
        audience_description (google.ads.googleads.v18.services.types.InsightsAudienceDescription):
            Provide a text description of an audience to
            get AI-generated targeting suggestions. This can
            take around 5 or more seconds to complete.

            This field is a member of `oneof`_ ``audience_input``.
    """

    customer_id: str = proto.Field(
        proto.STRING, number=1,
    )
    customer_insights_group: str = proto.Field(
        proto.STRING, number=5,
    )
    audience_definition: "InsightsAudienceDefinition" = proto.Field(
        proto.MESSAGE,
        number=6,
        oneof="audience_input",
        message="InsightsAudienceDefinition",
    )
    audience_description: "InsightsAudienceDescription" = proto.Field(
        proto.MESSAGE,
        number=7,
        oneof="audience_input",
        message="InsightsAudienceDescription",
    )


class GenerateSuggestedTargetingInsightsResponse(proto.Message):
    r"""Response message for
    [AudienceInsightsService.GenerateSuggestedTargetingInsights][google.ads.googleads.v18.services.AudienceInsightsService.GenerateSuggestedTargetingInsights].

    Attributes:
        suggestions (MutableSequence[google.ads.googleads.v18.services.types.TargetingSuggestionMetrics]):
            Suggested insights for targetable audiences.
    """

    suggestions: MutableSequence[
        "TargetingSuggestionMetrics"
    ] = proto.RepeatedField(
        proto.MESSAGE, number=1, message="TargetingSuggestionMetrics",
    )


class TargetingSuggestionMetrics(proto.Message):
    r"""A suggested targetable audience relevant to the requested
    audience.

    Attributes:
        locations (MutableSequence[google.ads.googleads.v18.services.types.AudienceInsightsAttributeMetadata]):
            Suggested location targeting. These attributes all have
            dimension GEO_TARGET_COUNTRY or SUB_COUNTRY_LOCATION
        age_ranges (MutableSequence[google.ads.googleads.v18.common.types.AgeRangeInfo]):
            Suggested age targeting; may be empty
            indicating no age targeting.
        gender (google.ads.googleads.v18.common.types.GenderInfo):
            Suggested gender targeting.  If present, this
            attribute has dimension GENDER.
        parental_status (google.ads.googleads.v18.common.types.ParentalStatusInfo):
            A Parental Status value (parent, or not a
            parent).
        user_interests (MutableSequence[google.ads.googleads.v18.services.types.AudienceInsightsAttributeMetadata]):
            Suggested audience segments to target. These attributes all
            have dimension AFFINITY_USER_INTEREST or
            IN_MARKET_USER_INTEREST
        coverage (float):
            The fraction (from 0 to 1 inclusive) of the
            requested audience that can be reached using the
            suggested targeting.
        index (float):
            The ratio of coverage to the coverage of the
            baseline audience or zero if this ratio is
            undefined or is not meaningful.
        potential_youtube_reach (int):
            The approximate estimated number of people
            that can be reached on YouTube using this
            targeting.
    """

    locations: MutableSequence[
        "AudienceInsightsAttributeMetadata"
    ] = proto.RepeatedField(
        proto.MESSAGE, number=1, message="AudienceInsightsAttributeMetadata",
    )
    age_ranges: MutableSequence[criteria.AgeRangeInfo] = proto.RepeatedField(
        proto.MESSAGE, number=2, message=criteria.AgeRangeInfo,
    )
    gender: criteria.GenderInfo = proto.Field(
        proto.MESSAGE, number=3, message=criteria.GenderInfo,
    )
    parental_status: criteria.ParentalStatusInfo = proto.Field(
        proto.MESSAGE, number=8, message=criteria.ParentalStatusInfo,
    )
    user_interests: MutableSequence[
        "AudienceInsightsAttributeMetadata"
    ] = proto.RepeatedField(
        proto.MESSAGE, number=4, message="AudienceInsightsAttributeMetadata",
    )
    coverage: float = proto.Field(
        proto.DOUBLE, number=5,
    )
    index: float = proto.Field(
        proto.DOUBLE, number=6,
    )
    potential_youtube_reach: int = proto.Field(
        proto.INT64, number=7,
    )


class ListAudienceInsightsAttributesRequest(proto.Message):
    r"""Request message for
    [AudienceInsightsService.ListAudienceInsightsAttributes][google.ads.googleads.v18.services.AudienceInsightsService.ListAudienceInsightsAttributes].

    Attributes:
        customer_id (str):
            Required. The ID of the customer.
        dimensions (MutableSequence[google.ads.googleads.v18.enums.types.AudienceInsightsDimensionEnum.AudienceInsightsDimension]):
            Required. The types of attributes to be
            returned.
        query_text (str):
            Required. A free text query. If the requested dimensions
            include Attributes CATEGORY or KNOWLEDGE_GRAPH, then the
            attributes returned for those dimensions will match or be
            related to this string. For other dimensions, this field is
            ignored and all available attributes are returned.
        customer_insights_group (str):
            The name of the customer being planned for.
            This is a user-defined value.
        location_country_filters (MutableSequence[google.ads.googleads.v18.common.types.LocationInfo]):
            If SUB_COUNTRY_LOCATION attributes are one of the requested
            dimensions and this field is present, then the
            SUB_COUNTRY_LOCATION attributes returned will be located in
            these countries. If this field is absent, then location
            attributes are not filtered by country. Setting this field
            when SUB_COUNTRY_LOCATION attributes are not requested will
            return an error.
        youtube_reach_location (google.ads.googleads.v18.common.types.LocationInfo):
            If present, potential YouTube reach estimates within the
            specified market will be returned for attributes for which
            they are available. Reach is only available for the
            AGE_RANGE, GENDER, AFFINITY_USER_INTEREST and
            IN_MARKET_USER_INTEREST dimensions, and may not be available
            for every attribute of those dimensions in every market.
    """

    customer_id: str = proto.Field(
        proto.STRING, number=1,
    )
    dimensions: MutableSequence[
        audience_insights_dimension.AudienceInsightsDimensionEnum.AudienceInsightsDimension
    ] = proto.RepeatedField(
        proto.ENUM,
        number=2,
        enum=audience_insights_dimension.AudienceInsightsDimensionEnum.AudienceInsightsDimension,
    )
    query_text: str = proto.Field(
        proto.STRING, number=3,
    )
    customer_insights_group: str = proto.Field(
        proto.STRING, number=4,
    )
    location_country_filters: MutableSequence[
        criteria.LocationInfo
    ] = proto.RepeatedField(
        proto.MESSAGE, number=5, message=criteria.LocationInfo,
    )
    youtube_reach_location: criteria.LocationInfo = proto.Field(
        proto.MESSAGE, number=6, message=criteria.LocationInfo,
    )


class ListAudienceInsightsAttributesResponse(proto.Message):
    r"""Response message for
    [AudienceInsightsService.ListAudienceInsightsAttributes][google.ads.googleads.v18.services.AudienceInsightsService.ListAudienceInsightsAttributes].

    Attributes:
        attributes (MutableSequence[google.ads.googleads.v18.services.types.AudienceInsightsAttributeMetadata]):
            The attributes matching the search query.
    """

    attributes: MutableSequence[
        "AudienceInsightsAttributeMetadata"
    ] = proto.RepeatedField(
        proto.MESSAGE, number=1, message="AudienceInsightsAttributeMetadata",
    )


class ListInsightsEligibleDatesRequest(proto.Message):
    r"""Request message for
    [AudienceInsightsService.ListInsightsEligibleDates][google.ads.googleads.v18.services.AudienceInsightsService.ListInsightsEligibleDates].

    """


class ListInsightsEligibleDatesResponse(proto.Message):
    r"""Response message for
    [AudienceInsightsService.ListInsightsEligibleDates][google.ads.googleads.v18.services.AudienceInsightsService.ListInsightsEligibleDates].

    Attributes:
        data_months (MutableSequence[str]):
            The months for which AudienceInsights data is
            currently available, each represented as a
            string in the form "YYYY-MM".
        last_thirty_days (google.ads.googleads.v18.common.types.DateRange):
            The actual dates covered by the "last 30 days" date range
            that will be used implicitly for
            [AudienceInsightsService.GenerateAudienceCompositionInsights][google.ads.googleads.v18.services.AudienceInsightsService.GenerateAudienceCompositionInsights]
            requests that have no data_month set.
    """

    data_months: MutableSequence[str] = proto.RepeatedField(
        proto.STRING, number=1,
    )
    last_thirty_days: dates.DateRange = proto.Field(
        proto.MESSAGE, number=2, message=dates.DateRange,
    )


class GenerateAudienceOverlapInsightsRequest(proto.Message):
    r"""Request message for
    [AudienceInsightsService.GenerateAudienceOverlapInsights][google.ads.googleads.v18.services.AudienceInsightsService.GenerateAudienceOverlapInsights].

    Attributes:
        customer_id (str):
            Required. The ID of the customer.
        country_location (google.ads.googleads.v18.common.types.LocationInfo):
            Required. The country in which to calculate
            the sizes and overlaps of audiences.
        primary_attribute (google.ads.googleads.v18.services.types.AudienceInsightsAttribute):
            Required. The audience attribute that should
            be intersected with all other eligible
            audiences.  This must be an Affinity or
            In-Market UserInterest, an AgeRange or a Gender.
        dimensions (MutableSequence[google.ads.googleads.v18.enums.types.AudienceInsightsDimensionEnum.AudienceInsightsDimension]):
            Required. The types of attributes of which to calculate the
            overlap with the primary_attribute. The values must be a
            subset of AFFINITY_USER_INTEREST, IN_MARKET_USER_INTEREST,
            AGE_RANGE and GENDER.
        customer_insights_group (str):
            The name of the customer being planned for.
            This is a user-defined value.
    """

    customer_id: str = proto.Field(
        proto.STRING, number=1,
    )
    country_location: criteria.LocationInfo = proto.Field(
        proto.MESSAGE, number=2, message=criteria.LocationInfo,
    )
    primary_attribute: "AudienceInsightsAttribute" = proto.Field(
        proto.MESSAGE, number=3, message="AudienceInsightsAttribute",
    )
    dimensions: MutableSequence[
        audience_insights_dimension.AudienceInsightsDimensionEnum.AudienceInsightsDimension
    ] = proto.RepeatedField(
        proto.ENUM,
        number=4,
        enum=audience_insights_dimension.AudienceInsightsDimensionEnum.AudienceInsightsDimension,
    )
    customer_insights_group: str = proto.Field(
        proto.STRING, number=5,
    )


class GenerateAudienceOverlapInsightsResponse(proto.Message):
    r"""Response message for
    [AudienceInsightsService.GenerateAudienceOverlapInsights][google.ads.googleads.v18.services.AudienceInsightsService.GenerateAudienceOverlapInsights].

    Attributes:
        primary_attribute_metadata (google.ads.googleads.v18.services.types.AudienceInsightsAttributeMetadata):
            Metadata for the primary attribute, including
            potential YouTube reach.
        dimension_results (MutableSequence[google.ads.googleads.v18.services.types.DimensionOverlapResult]):
            Lists of attributes and their overlap with
            the primary attribute, one list per requested
            dimension.
    """

    primary_attribute_metadata: "AudienceInsightsAttributeMetadata" = proto.Field(
        proto.MESSAGE, number=1, message="AudienceInsightsAttributeMetadata",
    )
    dimension_results: MutableSequence[
        "DimensionOverlapResult"
    ] = proto.RepeatedField(
        proto.MESSAGE, number=2, message="DimensionOverlapResult",
    )


class DimensionOverlapResult(proto.Message):
    r"""A list of audience attributes of a single dimension, including their
    overlap with a primary attribute, returned as part of a
    [GenerateAudienceOverlapInsightsResponse][google.ads.googleads.v18.services.GenerateAudienceOverlapInsightsResponse].

    Attributes:
        dimension (google.ads.googleads.v18.enums.types.AudienceInsightsDimensionEnum.AudienceInsightsDimension):
            The dimension of all the attributes in this
            section.
        items (MutableSequence[google.ads.googleads.v18.services.types.AudienceOverlapItem]):
            The attributes and their overlap with the
            primary attribute.
    """

    dimension: audience_insights_dimension.AudienceInsightsDimensionEnum.AudienceInsightsDimension = proto.Field(
        proto.ENUM,
        number=1,
        enum=audience_insights_dimension.AudienceInsightsDimensionEnum.AudienceInsightsDimension,
    )
    items: MutableSequence["AudienceOverlapItem"] = proto.RepeatedField(
        proto.MESSAGE, number=2, message="AudienceOverlapItem",
    )


class AudienceOverlapItem(proto.Message):
    r"""An audience attribute, with metadata including the overlap
    between this attribute's potential YouTube reach and that of a
    primary attribute.

    Attributes:
        attribute_metadata (google.ads.googleads.v18.services.types.AudienceInsightsAttributeMetadata):
            The attribute and its metadata, including
            potential YouTube reach.
        potential_youtube_reach_intersection (int):
            The estimated size of the intersection of
            this audience attribute with the primary
            attribute, that is, the number of reachable
            YouTube users who match BOTH the primary
            attribute and this one.
    """

    attribute_metadata: "AudienceInsightsAttributeMetadata" = proto.Field(
        proto.MESSAGE, number=1, message="AudienceInsightsAttributeMetadata",
    )
    potential_youtube_reach_intersection: int = proto.Field(
        proto.INT64, number=2,
    )


class GenerateTargetingSuggestionMetricsRequest(proto.Message):
    r"""Request message for
    [AudienceInsightsService.GenerateTargetingSuggestionMetrics].

    Attributes:
        customer_id (str):
            Required. The ID of the customer.
        audiences (MutableSequence[google.ads.googleads.v18.services.types.BasicInsightsAudience]):
            Required. Audiences to request metrics for.
        customer_insights_group (str):
            Optional. The name of the customer being
            planned for.  This is a user-defined value.
    """

    customer_id: str = proto.Field(
        proto.STRING, number=1,
    )
    audiences: MutableSequence["BasicInsightsAudience"] = proto.RepeatedField(
        proto.MESSAGE, number=2, message="BasicInsightsAudience",
    )
    customer_insights_group: str = proto.Field(
        proto.STRING, number=3,
    )


class GenerateTargetingSuggestionMetricsResponse(proto.Message):
    r"""Response message for
    [AudienceInsightsService.GenerateTargetingSuggestionMetrics][google.ads.googleads.v18.services.AudienceInsightsService.GenerateTargetingSuggestionMetrics].

    Attributes:
        suggestions (MutableSequence[google.ads.googleads.v18.services.types.TargetingSuggestionMetrics]):
            Suggested targetable audiences. There will be one suggestion
            for each
            [GenerateTargetingSuggestionMetricsRequest.audiences]
            requested, matching the order requested.
    """

    suggestions: MutableSequence[
        "TargetingSuggestionMetrics"
    ] = proto.RepeatedField(
        proto.MESSAGE, number=1, message="TargetingSuggestionMetrics",
    )


class AudienceInsightsAttribute(proto.Message):
    r"""An audience attribute that can be used to request insights
    about the audience.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        age_range (google.ads.googleads.v18.common.types.AgeRangeInfo):
            An audience attribute defined by an age
            range.

            This field is a member of `oneof`_ ``attribute``.
        gender (google.ads.googleads.v18.common.types.GenderInfo):
            An audience attribute defined by a gender.

            This field is a member of `oneof`_ ``attribute``.
        location (google.ads.googleads.v18.common.types.LocationInfo):
            An audience attribute defined by a geographic
            location.

            This field is a member of `oneof`_ ``attribute``.
        user_interest (google.ads.googleads.v18.common.types.UserInterestInfo):
            An Affinity or In-Market audience.

            This field is a member of `oneof`_ ``attribute``.
        entity (google.ads.googleads.v18.services.types.AudienceInsightsEntity):
            An audience attribute defined by interest in
            a topic represented by a Knowledge Graph entity.

            This field is a member of `oneof`_ ``attribute``.
        category (google.ads.googleads.v18.services.types.AudienceInsightsCategory):
            An audience attribute defined by interest in
            a Product & Service category.

            This field is a member of `oneof`_ ``attribute``.
        dynamic_lineup (google.ads.googleads.v18.services.types.AudienceInsightsDynamicLineup):
            A YouTube Dynamic Lineup

            This field is a member of `oneof`_ ``attribute``.
        parental_status (google.ads.googleads.v18.common.types.ParentalStatusInfo):
            A Parental Status value (parent, or not a
            parent).

            This field is a member of `oneof`_ ``attribute``.
        income_range (google.ads.googleads.v18.common.types.IncomeRangeInfo):
            A household income percentile range.

            This field is a member of `oneof`_ ``attribute``.
        youtube_channel (google.ads.googleads.v18.common.types.YouTubeChannelInfo):
            A YouTube channel.

            This field is a member of `oneof`_ ``attribute``.
    """

    age_range: criteria.AgeRangeInfo = proto.Field(
        proto.MESSAGE,
        number=1,
        oneof="attribute",
        message=criteria.AgeRangeInfo,
    )
    gender: criteria.GenderInfo = proto.Field(
        proto.MESSAGE, number=2, oneof="attribute", message=criteria.GenderInfo,
    )
    location: criteria.LocationInfo = proto.Field(
        proto.MESSAGE,
        number=3,
        oneof="attribute",
        message=criteria.LocationInfo,
    )
    user_interest: criteria.UserInterestInfo = proto.Field(
        proto.MESSAGE,
        number=4,
        oneof="attribute",
        message=criteria.UserInterestInfo,
    )
    entity: "AudienceInsightsEntity" = proto.Field(
        proto.MESSAGE,
        number=5,
        oneof="attribute",
        message="AudienceInsightsEntity",
    )
    category: "AudienceInsightsCategory" = proto.Field(
        proto.MESSAGE,
        number=6,
        oneof="attribute",
        message="AudienceInsightsCategory",
    )
    dynamic_lineup: "AudienceInsightsDynamicLineup" = proto.Field(
        proto.MESSAGE,
        number=7,
        oneof="attribute",
        message="AudienceInsightsDynamicLineup",
    )
    parental_status: criteria.ParentalStatusInfo = proto.Field(
        proto.MESSAGE,
        number=8,
        oneof="attribute",
        message=criteria.ParentalStatusInfo,
    )
    income_range: criteria.IncomeRangeInfo = proto.Field(
        proto.MESSAGE,
        number=9,
        oneof="attribute",
        message=criteria.IncomeRangeInfo,
    )
    youtube_channel: criteria.YouTubeChannelInfo = proto.Field(
        proto.MESSAGE,
        number=10,
        oneof="attribute",
        message=criteria.YouTubeChannelInfo,
    )


class AudienceInsightsTopic(proto.Message):
    r"""An entity or category representing a topic that defines an
    audience.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        entity (google.ads.googleads.v18.services.types.AudienceInsightsEntity):
            A Knowledge Graph entity

            This field is a member of `oneof`_ ``topic``.
        category (google.ads.googleads.v18.services.types.AudienceInsightsCategory):
            A Product & Service category

            This field is a member of `oneof`_ ``topic``.
    """

    entity: "AudienceInsightsEntity" = proto.Field(
        proto.MESSAGE,
        number=1,
        oneof="topic",
        message="AudienceInsightsEntity",
    )
    category: "AudienceInsightsCategory" = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="topic",
        message="AudienceInsightsCategory",
    )


class AudienceInsightsEntity(proto.Message):
    r"""A Knowledge Graph entity, represented by its machine id.
    Attributes:
        knowledge_graph_machine_id (str):
            Required. The machine id (mid) of the
            Knowledge Graph entity.
    """

    knowledge_graph_machine_id: str = proto.Field(
        proto.STRING, number=1,
    )


class AudienceInsightsCategory(proto.Message):
    r"""A Product and Service category.
    Attributes:
        category_id (str):
            Required. The criterion id of the category.
    """

    category_id: str = proto.Field(
        proto.STRING, number=1,
    )


class AudienceInsightsDynamicLineup(proto.Message):
    r"""A YouTube Dynamic Lineup.
    Attributes:
        dynamic_lineup_id (str):
            Required. The numeric ID of the dynamic
            lineup.
    """

    dynamic_lineup_id: str = proto.Field(
        proto.STRING, number=1,
    )


class BasicInsightsAudience(proto.Message):
    r"""A description of an audience used for requesting insights.
    Attributes:
        country_location (MutableSequence[google.ads.googleads.v18.common.types.LocationInfo]):
            Required. The countries for this audience.
        sub_country_locations (MutableSequence[google.ads.googleads.v18.common.types.LocationInfo]):
            Sub-country geographic location attributes.
            If present, each of these must be contained in
            one of the countries in this audience.
        gender (google.ads.googleads.v18.common.types.GenderInfo):
            Gender for the audience.  If absent, the
            audience does not restrict by gender.
        age_ranges (MutableSequence[google.ads.googleads.v18.common.types.AgeRangeInfo]):
            Age ranges for the audience.  If absent, the
            audience represents all people over 18 that
            match the other attributes.
        user_interests (MutableSequence[google.ads.googleads.v18.common.types.UserInterestInfo]):
            User interests defining this audience.
            Affinity and In-Market audiences are supported.
        topics (MutableSequence[google.ads.googleads.v18.services.types.AudienceInsightsTopic]):
            Topics, represented by Knowledge Graph
            entities and/or Product & Service categories,
            that this audience is interested in.
    """

    country_location: MutableSequence[
        criteria.LocationInfo
    ] = proto.RepeatedField(
        proto.MESSAGE, number=1, message=criteria.LocationInfo,
    )
    sub_country_locations: MutableSequence[
        criteria.LocationInfo
    ] = proto.RepeatedField(
        proto.MESSAGE, number=2, message=criteria.LocationInfo,
    )
    gender: criteria.GenderInfo = proto.Field(
        proto.MESSAGE, number=3, message=criteria.GenderInfo,
    )
    age_ranges: MutableSequence[criteria.AgeRangeInfo] = proto.RepeatedField(
        proto.MESSAGE, number=4, message=criteria.AgeRangeInfo,
    )
    user_interests: MutableSequence[
        criteria.UserInterestInfo
    ] = proto.RepeatedField(
        proto.MESSAGE, number=5, message=criteria.UserInterestInfo,
    )
    topics: MutableSequence["AudienceInsightsTopic"] = proto.RepeatedField(
        proto.MESSAGE, number=6, message="AudienceInsightsTopic",
    )


class AudienceInsightsAttributeMetadata(proto.Message):
    r"""An audience attribute, with metadata about it, returned in
    response to a search.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        dimension (google.ads.googleads.v18.enums.types.AudienceInsightsDimensionEnum.AudienceInsightsDimension):
            The type of the attribute.
        attribute (google.ads.googleads.v18.services.types.AudienceInsightsAttribute):
            The attribute itself.
        display_name (str):
            The human-readable name of the attribute.
        display_info (str):
            A string that supplements the display_name to identify the
            attribute. If the dimension is TOPIC, this is a brief
            description of the Knowledge Graph entity, such as "American
            singer-songwriter". If the dimension is CATEGORY, this is
            the complete path to the category in The Product & Service
            taxonomy, for example "/Apparel/Clothing/Outerwear".
        potential_youtube_reach (int):
            An estimate of the number of reachable YouTube users
            matching this attribute in the requested location, or zero
            if that information is not available for this attribute.
            Only populated in GenerateAudienceOverlapInsightsResponses
            and in ListAudienceInsightsAttributesResponses when
            youtube_reach_location is present in the request.
        youtube_channel_metadata (google.ads.googleads.v18.services.types.YouTubeChannelAttributeMetadata):
            Special metadata for a YouTube channel.

            This field is a member of `oneof`_ ``dimension_metadata``.
        dynamic_attribute_metadata (google.ads.googleads.v18.services.types.DynamicLineupAttributeMetadata):
            Special metadata for a YouTube Dynamic
            Lineup.

            This field is a member of `oneof`_ ``dimension_metadata``.
        location_attribute_metadata (google.ads.googleads.v18.services.types.LocationAttributeMetadata):
            Special metadata for a Location.

            This field is a member of `oneof`_ ``dimension_metadata``.
        user_interest_attribute_metadata (google.ads.googleads.v18.services.types.UserInterestAttributeMetadata):
            Special metadata for a User Interest.

            This field is a member of `oneof`_ ``dimension_metadata``.
    """

    dimension: audience_insights_dimension.AudienceInsightsDimensionEnum.AudienceInsightsDimension = proto.Field(
        proto.ENUM,
        number=1,
        enum=audience_insights_dimension.AudienceInsightsDimensionEnum.AudienceInsightsDimension,
    )
    attribute: "AudienceInsightsAttribute" = proto.Field(
        proto.MESSAGE, number=2, message="AudienceInsightsAttribute",
    )
    display_name: str = proto.Field(
        proto.STRING, number=3,
    )
    display_info: str = proto.Field(
        proto.STRING, number=5,
    )
    potential_youtube_reach: int = proto.Field(
        proto.INT64, number=9,
    )
    youtube_channel_metadata: "YouTubeChannelAttributeMetadata" = proto.Field(
        proto.MESSAGE,
        number=6,
        oneof="dimension_metadata",
        message="YouTubeChannelAttributeMetadata",
    )
    dynamic_attribute_metadata: "DynamicLineupAttributeMetadata" = proto.Field(
        proto.MESSAGE,
        number=7,
        oneof="dimension_metadata",
        message="DynamicLineupAttributeMetadata",
    )
    location_attribute_metadata: "LocationAttributeMetadata" = proto.Field(
        proto.MESSAGE,
        number=8,
        oneof="dimension_metadata",
        message="LocationAttributeMetadata",
    )
    user_interest_attribute_metadata: "UserInterestAttributeMetadata" = proto.Field(
        proto.MESSAGE,
        number=10,
        oneof="dimension_metadata",
        message="UserInterestAttributeMetadata",
    )


class YouTubeChannelAttributeMetadata(proto.Message):
    r"""Metadata associated with a YouTube channel attribute.
    Attributes:
        subscriber_count (int):
            The approximate number of subscribers to the
            YouTube channel.
    """

    subscriber_count: int = proto.Field(
        proto.INT64, number=1,
    )


class DynamicLineupAttributeMetadata(proto.Message):
    r"""Metadata associated with a Dynamic Lineup attribute.
    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        inventory_country (google.ads.googleads.v18.common.types.LocationInfo):
            The national market associated with the
            lineup.
        median_monthly_inventory (int):
            The median number of impressions per month on
            this lineup.

            This field is a member of `oneof`_ ``_median_monthly_inventory``.
        channel_count_lower_bound (int):
            The lower end of a range containing the
            number of channels in the lineup.

            This field is a member of `oneof`_ ``_channel_count_lower_bound``.
        channel_count_upper_bound (int):
            The upper end of a range containing the
            number of channels in the lineup.

            This field is a member of `oneof`_ ``_channel_count_upper_bound``.
        sample_channels (MutableSequence[google.ads.googleads.v18.services.types.DynamicLineupAttributeMetadata.SampleChannel]):
            Examples of channels that are included in the
            lineup.
    """

    class SampleChannel(proto.Message):
        r"""A YouTube channel returned as an example of the content in a
        lineup.

        Attributes:
            youtube_channel (google.ads.googleads.v18.common.types.YouTubeChannelInfo):
                A YouTube channel.
            display_name (str):
                The name of the sample channel.
            youtube_channel_metadata (google.ads.googleads.v18.services.types.YouTubeChannelAttributeMetadata):
                Metadata for the sample channel.
        """

        youtube_channel: criteria.YouTubeChannelInfo = proto.Field(
            proto.MESSAGE, number=1, message=criteria.YouTubeChannelInfo,
        )
        display_name: str = proto.Field(
            proto.STRING, number=2,
        )
        youtube_channel_metadata: "YouTubeChannelAttributeMetadata" = proto.Field(
            proto.MESSAGE, number=3, message="YouTubeChannelAttributeMetadata",
        )

    inventory_country: criteria.LocationInfo = proto.Field(
        proto.MESSAGE, number=1, message=criteria.LocationInfo,
    )
    median_monthly_inventory: int = proto.Field(
        proto.INT64, number=2, optional=True,
    )
    channel_count_lower_bound: int = proto.Field(
        proto.INT64, number=3, optional=True,
    )
    channel_count_upper_bound: int = proto.Field(
        proto.INT64, number=4, optional=True,
    )
    sample_channels: MutableSequence[SampleChannel] = proto.RepeatedField(
        proto.MESSAGE, number=5, message=SampleChannel,
    )


class LocationAttributeMetadata(proto.Message):
    r"""Metadata associated with a Location attribute.
    Attributes:
        country_location (google.ads.googleads.v18.common.types.LocationInfo):
            The country location of the sub country
            location.
    """

    country_location: criteria.LocationInfo = proto.Field(
        proto.MESSAGE, number=1, message=criteria.LocationInfo,
    )


class UserInterestAttributeMetadata(proto.Message):
    r"""Metadata associated with a User Interest attribute.
    Attributes:
        user_interest_description (str):
            English language text description of the user
            interest category (200 characters max).
    """

    user_interest_description: str = proto.Field(
        proto.STRING, number=1,
    )


class InsightsAudienceDefinition(proto.Message):
    r"""A structured definition of the audience of interest for which
    insights are being requested in AudienceInsightsService.

    Attributes:
        audience (google.ads.googleads.v18.services.types.InsightsAudience):
            Required. The audience of interest for which
            insights are being requested.
        baseline_audience (google.ads.googleads.v18.services.types.InsightsAudience):
            Optional. The baseline audience. The default,
            if unspecified, is all people in the same
            country as the audience of interest.
        data_month (str):
            Optional. The one-month range of historical
            data to use for insights, in the format
            "yyyy-mm". If unset, insights will be returned
            for the last thirty days of data.
    """

    audience: "InsightsAudience" = proto.Field(
        proto.MESSAGE, number=1, message="InsightsAudience",
    )
    baseline_audience: "InsightsAudience" = proto.Field(
        proto.MESSAGE, number=2, message="InsightsAudience",
    )
    data_month: str = proto.Field(
        proto.STRING, number=3,
    )


class InsightsAudienceDescription(proto.Message):
    r"""A text description of the audience of interest for which
    insights are being requested in AudienceInsightsService.

    Attributes:
        country_locations (MutableSequence[google.ads.googleads.v18.common.types.LocationInfo]):
            Required. The countries for the audience.
        audience_description (str):
            Required. An English language text
            description of an audience to get suggestions
            for. Maximum length is 2000 characters. For
            example, "Women in their 30s who love to
            travel".
        marketing_objective (google.ads.googleads.v18.enums.types.AudienceInsightsMarketingObjectiveEnum.AudienceInsightsMarketingObjective):
            Optional. An optional marketing objective
            which will influence the type of suggestions
            produced. AWARENESS will provide affinity
            audience segments, while CONSIDERATION will
            provide in-market audience segments. Leaving it
            unset will provide both.
    """

    country_locations: MutableSequence[
        criteria.LocationInfo
    ] = proto.RepeatedField(
        proto.MESSAGE, number=1, message=criteria.LocationInfo,
    )
    audience_description: str = proto.Field(
        proto.STRING, number=2,
    )
    marketing_objective: audience_insights_marketing_objective.AudienceInsightsMarketingObjectiveEnum.AudienceInsightsMarketingObjective = proto.Field(
        proto.ENUM,
        number=3,
        enum=audience_insights_marketing_objective.AudienceInsightsMarketingObjectiveEnum.AudienceInsightsMarketingObjective,
    )


class InsightsAudience(proto.Message):
    r"""A set of users, defined by various characteristics, for which
    insights can be requested in AudienceInsightsService.

    Attributes:
        country_locations (MutableSequence[google.ads.googleads.v18.common.types.LocationInfo]):
            Required. The countries for the audience.
        sub_country_locations (MutableSequence[google.ads.googleads.v18.common.types.LocationInfo]):
            Sub-country geographic location attributes. If present, each
            of these must be contained in one of the countries in this
            audience. If absent, the audience is geographically to the
            country_locations and no further.
        gender (google.ads.googleads.v18.common.types.GenderInfo):
            Gender for the audience.  If absent, the
            audience does not restrict by gender.
        age_ranges (MutableSequence[google.ads.googleads.v18.common.types.AgeRangeInfo]):
            Age ranges for the audience.  If absent, the
            audience represents all people over 18 that
            match the other attributes.
        parental_status (google.ads.googleads.v18.common.types.ParentalStatusInfo):
            Parental status for the audience.  If absent,
            the audience does not restrict by parental
            status.
        income_ranges (MutableSequence[google.ads.googleads.v18.common.types.IncomeRangeInfo]):
            Household income percentile ranges for the
            audience.  If absent, the audience does not
            restrict by household income range.
        dynamic_lineups (MutableSequence[google.ads.googleads.v18.services.types.AudienceInsightsDynamicLineup]):
            Dynamic lineups representing the YouTube
            content viewed by the audience.
        topic_audience_combinations (MutableSequence[google.ads.googleads.v18.services.types.InsightsAudienceAttributeGroup]):
            A combination of entity, category and user
            interest attributes defining the audience. The
            combination has a logical AND-of-ORs structure:
            Attributes within each
            InsightsAudienceAttributeGroup are combined with
            OR, and the combinations themselves are combined
            together with AND.  For example, the expression
            (Entity OR Affinity) AND (In-Market OR Category)
            can be formed using two
            InsightsAudienceAttributeGroups with two
            Attributes each.
    """

    country_locations: MutableSequence[
        criteria.LocationInfo
    ] = proto.RepeatedField(
        proto.MESSAGE, number=1, message=criteria.LocationInfo,
    )
    sub_country_locations: MutableSequence[
        criteria.LocationInfo
    ] = proto.RepeatedField(
        proto.MESSAGE, number=2, message=criteria.LocationInfo,
    )
    gender: criteria.GenderInfo = proto.Field(
        proto.MESSAGE, number=3, message=criteria.GenderInfo,
    )
    age_ranges: MutableSequence[criteria.AgeRangeInfo] = proto.RepeatedField(
        proto.MESSAGE, number=4, message=criteria.AgeRangeInfo,
    )
    parental_status: criteria.ParentalStatusInfo = proto.Field(
        proto.MESSAGE, number=5, message=criteria.ParentalStatusInfo,
    )
    income_ranges: MutableSequence[
        criteria.IncomeRangeInfo
    ] = proto.RepeatedField(
        proto.MESSAGE, number=6, message=criteria.IncomeRangeInfo,
    )
    dynamic_lineups: MutableSequence[
        "AudienceInsightsDynamicLineup"
    ] = proto.RepeatedField(
        proto.MESSAGE, number=7, message="AudienceInsightsDynamicLineup",
    )
    topic_audience_combinations: MutableSequence[
        "InsightsAudienceAttributeGroup"
    ] = proto.RepeatedField(
        proto.MESSAGE, number=8, message="InsightsAudienceAttributeGroup",
    )


class InsightsAudienceAttributeGroup(proto.Message):
    r"""A list of AudienceInsightsAttributes.
    Attributes:
        attributes (MutableSequence[google.ads.googleads.v18.services.types.AudienceInsightsAttribute]):
            Required. A collection of audience attributes
            to be combined with logical OR. Attributes need
            not all be the same dimension.  Only Knowledge
            Graph entities, Product & Service Categories,
            and Affinity and In-Market audiences are
            supported in this context.
    """

    attributes: MutableSequence[
        "AudienceInsightsAttribute"
    ] = proto.RepeatedField(
        proto.MESSAGE, number=1, message="AudienceInsightsAttribute",
    )


class AudienceCompositionSection(proto.Message):
    r"""A collection of related attributes of the same type in an
    audience composition insights report.

    Attributes:
        dimension (google.ads.googleads.v18.enums.types.AudienceInsightsDimensionEnum.AudienceInsightsDimension):
            The type of the attributes in this section.
        top_attributes (MutableSequence[google.ads.googleads.v18.services.types.AudienceCompositionAttribute]):
            The most relevant segments for this audience. If dimension
            is GENDER, AGE_RANGE or PARENTAL_STATUS, then this list of
            attributes is exhaustive.
        clustered_attributes (MutableSequence[google.ads.googleads.v18.services.types.AudienceCompositionAttributeCluster]):
            Additional attributes for this audience, grouped into
            clusters. Only populated if dimension is YOUTUBE_CHANNEL.
    """

    dimension: audience_insights_dimension.AudienceInsightsDimensionEnum.AudienceInsightsDimension = proto.Field(
        proto.ENUM,
        number=1,
        enum=audience_insights_dimension.AudienceInsightsDimensionEnum.AudienceInsightsDimension,
    )
    top_attributes: MutableSequence[
        "AudienceCompositionAttribute"
    ] = proto.RepeatedField(
        proto.MESSAGE, number=3, message="AudienceCompositionAttribute",
    )
    clustered_attributes: MutableSequence[
        "AudienceCompositionAttributeCluster"
    ] = proto.RepeatedField(
        proto.MESSAGE, number=4, message="AudienceCompositionAttributeCluster",
    )


class AudienceCompositionAttributeCluster(proto.Message):
    r"""A collection of related attributes, with metadata and
    metrics, in an audience composition insights report.

    Attributes:
        cluster_display_name (str):
            The name of this cluster of attributes
        cluster_metrics (google.ads.googleads.v18.services.types.AudienceCompositionMetrics):
            If the dimension associated with this cluster is
            YOUTUBE_CHANNEL, then cluster_metrics are metrics associated
            with the cluster as a whole. For other dimensions, this
            field is unset.
        attributes (MutableSequence[google.ads.googleads.v18.services.types.AudienceCompositionAttribute]):
            The individual attributes that make up this
            cluster, with metadata and metrics.
    """

    cluster_display_name: str = proto.Field(
        proto.STRING, number=1,
    )
    cluster_metrics: "AudienceCompositionMetrics" = proto.Field(
        proto.MESSAGE, number=3, message="AudienceCompositionMetrics",
    )
    attributes: MutableSequence[
        "AudienceCompositionAttribute"
    ] = proto.RepeatedField(
        proto.MESSAGE, number=4, message="AudienceCompositionAttribute",
    )


class AudienceCompositionMetrics(proto.Message):
    r"""The share and index metrics associated with an attribute in
    an audience composition insights report.

    Attributes:
        baseline_audience_share (float):
            The fraction (from 0 to 1 inclusive) of the
            baseline audience that match the attribute.
        audience_share (float):
            The fraction (from 0 to 1 inclusive) of the
            specific audience that match the attribute.
        index (float):
            The ratio of audience_share to baseline_audience_share, or
            zero if this ratio is undefined or is not meaningful.
        score (float):
            A relevance score from 0 to 1 inclusive.
    """

    baseline_audience_share: float = proto.Field(
        proto.DOUBLE, number=1,
    )
    audience_share: float = proto.Field(
        proto.DOUBLE, number=2,
    )
    index: float = proto.Field(
        proto.DOUBLE, number=3,
    )
    score: float = proto.Field(
        proto.DOUBLE, number=4,
    )


class AudienceCompositionAttribute(proto.Message):
    r"""An audience attribute with metadata and metrics.
    Attributes:
        attribute_metadata (google.ads.googleads.v18.services.types.AudienceInsightsAttributeMetadata):
            The attribute with its metadata.
        metrics (google.ads.googleads.v18.services.types.AudienceCompositionMetrics):
            Share and index metrics for the attribute.
    """

    attribute_metadata: "AudienceInsightsAttributeMetadata" = proto.Field(
        proto.MESSAGE, number=1, message="AudienceInsightsAttributeMetadata",
    )
    metrics: "AudienceCompositionMetrics" = proto.Field(
        proto.MESSAGE, number=2, message="AudienceCompositionMetrics",
    )


__all__ = tuple(sorted(__protobuf__.manifest))
