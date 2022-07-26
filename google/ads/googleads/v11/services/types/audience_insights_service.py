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
import proto  # type: ignore

from google.ads.googleads.v11.common.types import criteria
from google.ads.googleads.v11.enums.types import audience_insights_dimension


__protobuf__ = proto.module(
    package="google.ads.googleads.v11.services",
    marshal="google.ads.googleads.v11",
    manifest={
        "GenerateInsightsFinderReportRequest",
        "GenerateInsightsFinderReportResponse",
        "ListAudienceInsightsAttributesRequest",
        "ListAudienceInsightsAttributesResponse",
        "AudienceInsightsAttribute",
        "AudienceInsightsTopic",
        "AudienceInsightsEntity",
        "AudienceInsightsCategory",
        "BasicInsightsAudience",
        "AudienceInsightsAttributeMetadata",
    },
)


class GenerateInsightsFinderReportRequest(proto.Message):
    r"""Request message for
    [AudienceInsightsService.GenerateInsightsFinderReport][google.ads.googleads.v11.services.AudienceInsightsService.GenerateInsightsFinderReport].

    Attributes:
        customer_id (str):
            Required. The ID of the customer.
        baseline_audience (google.ads.googleads.v11.services.types.BasicInsightsAudience):
            Required. A baseline audience for this
            report, typically all people in a region.
        specific_audience (google.ads.googleads.v11.services.types.BasicInsightsAudience):
            Required. The specific audience of interest
            for this report.  The insights in the report
            will be based on attributes more prevalent in
            this audience than in the report's baseline
            audience.
        customer_insights_group (str):
            The name of the customer being planned for.
            This is a user-defined value.
    """

    customer_id = proto.Field(
        proto.STRING,
        number=1,
    )
    baseline_audience = proto.Field(
        proto.MESSAGE,
        number=2,
        message="BasicInsightsAudience",
    )
    specific_audience = proto.Field(
        proto.MESSAGE,
        number=3,
        message="BasicInsightsAudience",
    )
    customer_insights_group = proto.Field(
        proto.STRING,
        number=4,
    )


class GenerateInsightsFinderReportResponse(proto.Message):
    r"""The response message for
    [AudienceInsightsService.GenerateInsightsFinderReport][google.ads.googleads.v11.services.AudienceInsightsService.GenerateInsightsFinderReport],
    containing the shareable URL for the report.

    Attributes:
        saved_report_url (str):
            An HTTPS URL providing a deep link into the
            Insights Finder UI with the report inputs filled
            in according to the request.
    """

    saved_report_url = proto.Field(
        proto.STRING,
        number=1,
    )


class ListAudienceInsightsAttributesRequest(proto.Message):
    r"""Request message for
    [AudienceInsightsService.ListAudienceInsightsAttributes][google.ads.googleads.v11.services.AudienceInsightsService.ListAudienceInsightsAttributes].

    Attributes:
        customer_id (str):
            Required. The ID of the customer.
        dimensions (Sequence[google.ads.googleads.v11.enums.types.AudienceInsightsDimensionEnum.AudienceInsightsDimension]):
            Required. The types of attributes to be
            returned.
        query_text (str):
            Required. A free text query.  Attributes
            matching or related to this string will be
            returned.
        customer_insights_group (str):
            The name of the customer being planned for.
            This is a user-defined value.
    """

    customer_id = proto.Field(
        proto.STRING,
        number=1,
    )
    dimensions = proto.RepeatedField(
        proto.ENUM,
        number=2,
        enum=audience_insights_dimension.AudienceInsightsDimensionEnum.AudienceInsightsDimension,
    )
    query_text = proto.Field(
        proto.STRING,
        number=3,
    )
    customer_insights_group = proto.Field(
        proto.STRING,
        number=4,
    )


class ListAudienceInsightsAttributesResponse(proto.Message):
    r"""Response message for
    [AudienceInsightsService.ListAudienceInsightsAttributes][google.ads.googleads.v11.services.AudienceInsightsService.ListAudienceInsightsAttributes].

    Attributes:
        attributes (Sequence[google.ads.googleads.v11.services.types.AudienceInsightsAttributeMetadata]):
            The attributes matching the search query.
    """

    attributes = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message="AudienceInsightsAttributeMetadata",
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
        age_range (google.ads.googleads.v11.common.types.AgeRangeInfo):
            An audience attribute defined by an age
            range.

            This field is a member of `oneof`_ ``attribute``.
        gender (google.ads.googleads.v11.common.types.GenderInfo):
            An audience attribute defined by a gender.

            This field is a member of `oneof`_ ``attribute``.
        location (google.ads.googleads.v11.common.types.LocationInfo):
            An audience attribute defiend by a geographic
            location.

            This field is a member of `oneof`_ ``attribute``.
        user_interest (google.ads.googleads.v11.common.types.UserInterestInfo):
            An Affinity or In-Market audience.

            This field is a member of `oneof`_ ``attribute``.
        entity (google.ads.googleads.v11.services.types.AudienceInsightsEntity):
            An audience attribute defined by interest in
            a topic represented by a Knowledge Graph entity.

            This field is a member of `oneof`_ ``attribute``.
        category (google.ads.googleads.v11.services.types.AudienceInsightsCategory):
            An audience attribute defined by interest in
            a Product & Service category.

            This field is a member of `oneof`_ ``attribute``.
    """

    age_range = proto.Field(
        proto.MESSAGE,
        number=1,
        oneof="attribute",
        message=criteria.AgeRangeInfo,
    )
    gender = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="attribute",
        message=criteria.GenderInfo,
    )
    location = proto.Field(
        proto.MESSAGE,
        number=3,
        oneof="attribute",
        message=criteria.LocationInfo,
    )
    user_interest = proto.Field(
        proto.MESSAGE,
        number=4,
        oneof="attribute",
        message=criteria.UserInterestInfo,
    )
    entity = proto.Field(
        proto.MESSAGE,
        number=5,
        oneof="attribute",
        message="AudienceInsightsEntity",
    )
    category = proto.Field(
        proto.MESSAGE,
        number=6,
        oneof="attribute",
        message="AudienceInsightsCategory",
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
        entity (google.ads.googleads.v11.services.types.AudienceInsightsEntity):
            A Knowledge Graph entity

            This field is a member of `oneof`_ ``topic``.
        category (google.ads.googleads.v11.services.types.AudienceInsightsCategory):
            A Product & Service category

            This field is a member of `oneof`_ ``topic``.
    """

    entity = proto.Field(
        proto.MESSAGE,
        number=1,
        oneof="topic",
        message="AudienceInsightsEntity",
    )
    category = proto.Field(
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

    knowledge_graph_machine_id = proto.Field(
        proto.STRING,
        number=1,
    )


class AudienceInsightsCategory(proto.Message):
    r"""A Product and Service category.

    Attributes:
        category_id (str):
            Required. The criterion id of the category.
    """

    category_id = proto.Field(
        proto.STRING,
        number=1,
    )


class BasicInsightsAudience(proto.Message):
    r"""A description of an audience used for requesting insights.

    Attributes:
        country_location (Sequence[google.ads.googleads.v11.common.types.LocationInfo]):
            Required. The countries for this audience.
        sub_country_locations (Sequence[google.ads.googleads.v11.common.types.LocationInfo]):
            Sub-country geographic location attributes.
            If present, each of these must be contained in
            one of the countries in this audience.
        gender (google.ads.googleads.v11.common.types.GenderInfo):
            Gender for the audience.  If absent, the
            audience does not restrict by gender.
        age_ranges (Sequence[google.ads.googleads.v11.common.types.AgeRangeInfo]):
            Age ranges for the audience.  If absent, the
            audience represents all people over 18 that
            match the other attributes.
        user_interests (Sequence[google.ads.googleads.v11.common.types.UserInterestInfo]):
            User interests defining this audience.
            Affinity and In-Market audiences are supported.
        topics (Sequence[google.ads.googleads.v11.services.types.AudienceInsightsTopic]):
            Topics, represented by Knowledge Graph
            entities and/or Product & Service categories,
            that this audience is interested in.
    """

    country_location = proto.RepeatedField(
        proto.MESSAGE,
        number=1,
        message=criteria.LocationInfo,
    )
    sub_country_locations = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message=criteria.LocationInfo,
    )
    gender = proto.Field(
        proto.MESSAGE,
        number=3,
        message=criteria.GenderInfo,
    )
    age_ranges = proto.RepeatedField(
        proto.MESSAGE,
        number=4,
        message=criteria.AgeRangeInfo,
    )
    user_interests = proto.RepeatedField(
        proto.MESSAGE,
        number=5,
        message=criteria.UserInterestInfo,
    )
    topics = proto.RepeatedField(
        proto.MESSAGE,
        number=6,
        message="AudienceInsightsTopic",
    )


class AudienceInsightsAttributeMetadata(proto.Message):
    r"""An audience attribute, with metadata about it, returned in
    response to a search.

    Attributes:
        dimension (google.ads.googleads.v11.enums.types.AudienceInsightsDimensionEnum.AudienceInsightsDimension):
            The type of the attribute.
        attribute (google.ads.googleads.v11.services.types.AudienceInsightsAttribute):
            The attribute itself.
        display_name (str):
            The human-readable name of the attribute.
        score (float):
            A relevance score for this attribute, between
            0 and 1.
        display_info (str):
            A string that supplements the display_name to identify the
            attribute. If the dimension is TOPIC, this is a brief
            description of the Knowledge Graph entity, such as "American
            singer-songwriter". If the dimension is CATEGORY, this is
            the complete path to the category in The Product & Service
            taxonomy, for example "/Apparel/Clothing/Outerwear".
    """

    dimension = proto.Field(
        proto.ENUM,
        number=1,
        enum=audience_insights_dimension.AudienceInsightsDimensionEnum.AudienceInsightsDimension,
    )
    attribute = proto.Field(
        proto.MESSAGE,
        number=2,
        message="AudienceInsightsAttribute",
    )
    display_name = proto.Field(
        proto.STRING,
        number=3,
    )
    score = proto.Field(
        proto.DOUBLE,
        number=4,
    )
    display_info = proto.Field(
        proto.STRING,
        number=5,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
