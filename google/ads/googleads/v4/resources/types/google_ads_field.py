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


from google.ads.googleads.v4.enums.types import google_ads_field_category
from google.ads.googleads.v4.enums.types import google_ads_field_data_type
from google.protobuf import wrappers_pb2 as wrappers  # type: ignore


__protobuf__ = proto.module(
    package="google.ads.googleads.v4.resources",
    marshal="google.ads.googleads.v4",
    manifest={"GoogleAdsField",},
)


class GoogleAdsField(proto.Message):
    r"""A field or resource (artifact) used by GoogleAdsService.

    Attributes:
        resource_name (str):
            Output only. The resource name of the artifact. Artifact
            resource names have the form:

            ``googleAdsFields/{name}``
        name (google.protobuf.wrappers_pb2.StringValue):
            Output only. The name of the artifact.
        category (google.ads.googleads.v4.enums.types.GoogleAdsFieldCategoryEnum.GoogleAdsFieldCategory):
            Output only. The category of the artifact.
        selectable (google.protobuf.wrappers_pb2.BoolValue):
            Output only. Whether the artifact can be used
            in a SELECT clause in search queries.
        filterable (google.protobuf.wrappers_pb2.BoolValue):
            Output only. Whether the artifact can be used
            in a WHERE clause in search queries.
        sortable (google.protobuf.wrappers_pb2.BoolValue):
            Output only. Whether the artifact can be used
            in a ORDER BY clause in search queries.
        selectable_with (Sequence[google.protobuf.wrappers_pb2.StringValue]):
            Output only. The names of all resources,
            segments, and metrics that are selectable with
            the described artifact.
        attribute_resources (Sequence[google.protobuf.wrappers_pb2.StringValue]):
            Output only. The names of all resources that
            are selectable with the described artifact.
            Fields from these resources do not segment
            metrics when included in search queries.

            This field is only set for artifacts whose
            category is RESOURCE.
        metrics (Sequence[google.protobuf.wrappers_pb2.StringValue]):
            Output only. At and beyond version V1 this
            field lists the names of all metrics that are
            selectable with the described artifact when it
            is used in the FROM clause. It is only set for
            artifacts whose category is RESOURCE.
            Before version V1 this field lists the names of
            all metrics that are selectable with the
            described artifact. It is only set for artifacts
            whose category is either RESOURCE or SEGMENT
        segments (Sequence[google.protobuf.wrappers_pb2.StringValue]):
            Output only. At and beyond version V1 this
            field lists the names of all artifacts, whether
            a segment or another resource, that segment
            metrics when included in search queries and when
            the described artifact is used in the FROM
            clause. It is only set for artifacts whose
            category is RESOURCE.
            Before version V1 this field lists the names of
            all artifacts, whether a segment or another
            resource, that segment metrics when included in
            search queries. It is only set for artifacts of
            category RESOURCE, SEGMENT or METRIC.
        enum_values (Sequence[google.protobuf.wrappers_pb2.StringValue]):
            Output only. Values the artifact can assume
            if it is a field of type ENUM.
            This field is only set for artifacts of category
            SEGMENT or ATTRIBUTE.
        data_type (google.ads.googleads.v4.enums.types.GoogleAdsFieldDataTypeEnum.GoogleAdsFieldDataType):
            Output only. This field determines the
            operators that can be used with the artifact in
            WHERE clauses.
        type_url (google.protobuf.wrappers_pb2.StringValue):
            Output only. The URL of proto describing the
            artifact's data type.
        is_repeated (google.protobuf.wrappers_pb2.BoolValue):
            Output only. Whether the field artifact is
            repeated.
    """

    resource_name = proto.Field(proto.STRING, number=1)
    name = proto.Field(proto.MESSAGE, number=2, message=wrappers.StringValue,)
    category = proto.Field(
        proto.ENUM,
        number=3,
        enum=google_ads_field_category.GoogleAdsFieldCategoryEnum.GoogleAdsFieldCategory,
    )
    selectable = proto.Field(
        proto.MESSAGE, number=4, message=wrappers.BoolValue,
    )
    filterable = proto.Field(
        proto.MESSAGE, number=5, message=wrappers.BoolValue,
    )
    sortable = proto.Field(proto.MESSAGE, number=6, message=wrappers.BoolValue,)
    selectable_with = proto.RepeatedField(
        proto.MESSAGE, number=7, message=wrappers.StringValue,
    )
    attribute_resources = proto.RepeatedField(
        proto.MESSAGE, number=8, message=wrappers.StringValue,
    )
    metrics = proto.RepeatedField(
        proto.MESSAGE, number=9, message=wrappers.StringValue,
    )
    segments = proto.RepeatedField(
        proto.MESSAGE, number=10, message=wrappers.StringValue,
    )
    enum_values = proto.RepeatedField(
        proto.MESSAGE, number=11, message=wrappers.StringValue,
    )
    data_type = proto.Field(
        proto.ENUM,
        number=12,
        enum=google_ads_field_data_type.GoogleAdsFieldDataTypeEnum.GoogleAdsFieldDataType,
    )
    type_url = proto.Field(
        proto.MESSAGE, number=13, message=wrappers.StringValue,
    )
    is_repeated = proto.Field(
        proto.MESSAGE, number=14, message=wrappers.BoolValue,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
