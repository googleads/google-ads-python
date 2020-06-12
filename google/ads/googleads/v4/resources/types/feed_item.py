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


from google.ads.googleads.v4.common.types import custom_parameter
from google.ads.googleads.v4.common.types import feed_common
from google.ads.googleads.v4.common.types import policy
from google.ads.googleads.v4.enums.types import (
    feed_item_quality_approval_status,
)
from google.ads.googleads.v4.enums.types import (
    feed_item_quality_disapproval_reason,
)
from google.ads.googleads.v4.enums.types import feed_item_status
from google.ads.googleads.v4.enums.types import feed_item_validation_status
from google.ads.googleads.v4.enums.types import (
    geo_targeting_restriction as gage_geo_targeting_restriction,
)
from google.ads.googleads.v4.enums.types import placeholder_type
from google.ads.googleads.v4.enums.types import policy_approval_status
from google.ads.googleads.v4.enums.types import policy_review_status
from google.ads.googleads.v4.errors.types import feed_item_validation_error
from google.protobuf import wrappers_pb2 as wrappers  # type: ignore


__protobuf__ = proto.module(
    package="google.ads.googleads.v4.resources",
    marshal="google.ads.googleads.v4",
    manifest={
        "FeedItem",
        "FeedItemAttributeValue",
        "FeedItemPlaceholderPolicyInfo",
        "FeedItemValidationError",
    },
)


class FeedItem(proto.Message):
    r"""A feed item.

    Attributes:
        resource_name (str):
            Immutable. The resource name of the feed item. Feed item
            resource names have the form:

            ``customers/{customer_id}/feedItems/{feed_id}~{feed_item_id}``
        feed (google.protobuf.wrappers_pb2.StringValue):
            Immutable. The feed to which this feed item
            belongs.
        id (google.protobuf.wrappers_pb2.Int64Value):
            Output only. The ID of this feed item.
        start_date_time (google.protobuf.wrappers_pb2.StringValue):
            Start time in which this feed item is
            effective and can begin serving. The time is in
            the customer's time zone. The format is "YYYY-
            MM-DD HH:MM:SS".
            Examples: "2018-03-05 09:15:00" or "2018-02-01
            14:34:30".
        end_date_time (google.protobuf.wrappers_pb2.StringValue):
            End time in which this feed item is no longer
            effective and will stop serving. The time is in
            the customer's time zone. The format is "YYYY-
            MM-DD HH:MM:SS".
            Examples: "2018-03-05 09:15:00" or "2018-02-01
            14:34:30".
        attribute_values (Sequence[google.ads.googleads.v4.resources.types.FeedItemAttributeValue]):
            The feed item's attribute values.
        geo_targeting_restriction (google.ads.googleads.v4.enums.types.GeoTargetingRestrictionEnum.GeoTargetingRestriction):
            Geo targeting restriction specifies the type
            of location that can be used for targeting.
        url_custom_parameters (Sequence[google.ads.googleads.v4.common.types.CustomParameter]):
            The list of mappings used to substitute custom parameter
            tags in a ``tracking_url_template``, ``final_urls``, or
            ``mobile_final_urls``.
        status (google.ads.googleads.v4.enums.types.FeedItemStatusEnum.FeedItemStatus):
            Output only. Status of the feed item.
            This field is read-only.
        policy_infos (Sequence[google.ads.googleads.v4.resources.types.FeedItemPlaceholderPolicyInfo]):
            Output only. List of info about a feed item's
            validation and approval state for active feed
            mappings. There will be an entry in the list for
            each type of feed mapping associated with the
            feed, e.g. a feed with a sitelink and a call
            feed mapping would cause every feed item
            associated with that feed to have an entry in
            this list for both sitelink and call. This field
            is read-only.
    """

    resource_name = proto.Field(proto.STRING, number=1)
    feed = proto.Field(proto.MESSAGE, number=2, message=wrappers.StringValue,)
    id = proto.Field(proto.MESSAGE, number=3, message=wrappers.Int64Value,)
    start_date_time = proto.Field(
        proto.MESSAGE, number=4, message=wrappers.StringValue,
    )
    end_date_time = proto.Field(
        proto.MESSAGE, number=5, message=wrappers.StringValue,
    )
    attribute_values = proto.RepeatedField(
        proto.MESSAGE, number=6, message="FeedItemAttributeValue",
    )
    geo_targeting_restriction = proto.Field(
        proto.ENUM,
        number=7,
        enum=gage_geo_targeting_restriction.GeoTargetingRestrictionEnum.GeoTargetingRestriction,
    )
    url_custom_parameters = proto.RepeatedField(
        proto.MESSAGE, number=8, message=custom_parameter.CustomParameter,
    )
    status = proto.Field(
        proto.ENUM,
        number=9,
        enum=feed_item_status.FeedItemStatusEnum.FeedItemStatus,
    )
    policy_infos = proto.RepeatedField(
        proto.MESSAGE, number=10, message="FeedItemPlaceholderPolicyInfo",
    )


class FeedItemAttributeValue(proto.Message):
    r"""A feed item attribute value.

    Attributes:
        feed_attribute_id (google.protobuf.wrappers_pb2.Int64Value):
            Id of the feed attribute for which the value
            is associated with.
        integer_value (google.protobuf.wrappers_pb2.Int64Value):
            Int64 value. Should be set if feed_attribute_id refers to a
            feed attribute of type INT64.
        boolean_value (google.protobuf.wrappers_pb2.BoolValue):
            Bool value. Should be set if feed_attribute_id refers to a
            feed attribute of type BOOLEAN.
        string_value (google.protobuf.wrappers_pb2.StringValue):
            String value. Should be set if feed_attribute_id refers to a
            feed attribute of type STRING, URL or DATE_TIME. For STRING
            the maximum length is 1500 characters. For URL the maximum
            length is 2076 characters. For DATE_TIME the string must be
            in the format "YYYYMMDD HHMMSS".
        double_value (google.protobuf.wrappers_pb2.DoubleValue):
            Double value. Should be set if feed_attribute_id refers to a
            feed attribute of type DOUBLE.
        price_value (google.ads.googleads.v4.common.types.Money):
            Price value. Should be set if feed_attribute_id refers to a
            feed attribute of type PRICE.
        integer_values (Sequence[google.protobuf.wrappers_pb2.Int64Value]):
            Repeated int64 value. Should be set if feed_attribute_id
            refers to a feed attribute of type INT64_LIST.
        boolean_values (Sequence[google.protobuf.wrappers_pb2.BoolValue]):
            Repeated bool value. Should be set if feed_attribute_id
            refers to a feed attribute of type BOOLEAN_LIST.
        string_values (Sequence[google.protobuf.wrappers_pb2.StringValue]):
            Repeated string value. Should be set if feed_attribute_id
            refers to a feed attribute of type STRING_LIST, URL_LIST or
            DATE_TIME_LIST. For STRING_LIST and URL_LIST the total size
            of the list in bytes may not exceed 3000. For DATE_TIME_LIST
            the number of elements may not exceed 200.

            For STRING_LIST the maximum length of each string element is
            1500 characters. For URL_LIST the maximum length is 2076
            characters. For DATE_TIME the format of the string must be
            the same as start and end time for the feed item.
        double_values (Sequence[google.protobuf.wrappers_pb2.DoubleValue]):
            Repeated double value. Should be set if feed_attribute_id
            refers to a feed attribute of type DOUBLE_LIST.
    """

    feed_attribute_id = proto.Field(
        proto.MESSAGE, number=1, message=wrappers.Int64Value,
    )
    integer_value = proto.Field(
        proto.MESSAGE, number=2, message=wrappers.Int64Value,
    )
    boolean_value = proto.Field(
        proto.MESSAGE, number=3, message=wrappers.BoolValue,
    )
    string_value = proto.Field(
        proto.MESSAGE, number=4, message=wrappers.StringValue,
    )
    double_value = proto.Field(
        proto.MESSAGE, number=5, message=wrappers.DoubleValue,
    )
    price_value = proto.Field(
        proto.MESSAGE, number=6, message=feed_common.Money,
    )
    integer_values = proto.RepeatedField(
        proto.MESSAGE, number=7, message=wrappers.Int64Value,
    )
    boolean_values = proto.RepeatedField(
        proto.MESSAGE, number=8, message=wrappers.BoolValue,
    )
    string_values = proto.RepeatedField(
        proto.MESSAGE, number=9, message=wrappers.StringValue,
    )
    double_values = proto.RepeatedField(
        proto.MESSAGE, number=10, message=wrappers.DoubleValue,
    )


class FeedItemPlaceholderPolicyInfo(proto.Message):
    r"""Policy, validation, and quality approval info for a feed item
    for the specified placeholder type.

    Attributes:
        placeholder_type_enum (google.ads.googleads.v4.enums.types.PlaceholderTypeEnum.PlaceholderType):
            Output only. The placeholder type.
        feed_mapping_resource_name (google.protobuf.wrappers_pb2.StringValue):
            Output only. The FeedMapping that contains
            the placeholder type.
        review_status (google.ads.googleads.v4.enums.types.PolicyReviewStatusEnum.PolicyReviewStatus):
            Output only. Where the placeholder type is in
            the review process.
        approval_status (google.ads.googleads.v4.enums.types.PolicyApprovalStatusEnum.PolicyApprovalStatus):
            Output only. The overall approval status of
            the placeholder type, calculated based on the
            status of its individual policy topic entries.
        policy_topic_entries (Sequence[google.ads.googleads.v4.common.types.PolicyTopicEntry]):
            Output only. The list of policy findings for
            the placeholder type.
        validation_status (google.ads.googleads.v4.enums.types.FeedItemValidationStatusEnum.FeedItemValidationStatus):
            Output only. The validation status of the
            palceholder type.
        validation_errors (Sequence[google.ads.googleads.v4.resources.types.FeedItemValidationError]):
            Output only. List of placeholder type
            validation errors.
        quality_approval_status (google.ads.googleads.v4.enums.types.FeedItemQualityApprovalStatusEnum.FeedItemQualityApprovalStatus):
            Output only. Placeholder type quality
            evaluation approval status.
        quality_disapproval_reasons (Sequence[google.ads.googleads.v4.enums.types.FeedItemQualityDisapprovalReasonEnum.FeedItemQualityDisapprovalReason]):
            Output only. List of placeholder type quality
            evaluation disapproval reasons.
    """

    placeholder_type_enum = proto.Field(
        proto.ENUM,
        number=10,
        enum=placeholder_type.PlaceholderTypeEnum.PlaceholderType,
    )
    feed_mapping_resource_name = proto.Field(
        proto.MESSAGE, number=2, message=wrappers.StringValue,
    )
    review_status = proto.Field(
        proto.ENUM,
        number=3,
        enum=policy_review_status.PolicyReviewStatusEnum.PolicyReviewStatus,
    )
    approval_status = proto.Field(
        proto.ENUM,
        number=4,
        enum=policy_approval_status.PolicyApprovalStatusEnum.PolicyApprovalStatus,
    )
    policy_topic_entries = proto.RepeatedField(
        proto.MESSAGE, number=5, message=policy.PolicyTopicEntry,
    )
    validation_status = proto.Field(
        proto.ENUM,
        number=6,
        enum=feed_item_validation_status.FeedItemValidationStatusEnum.FeedItemValidationStatus,
    )
    validation_errors = proto.RepeatedField(
        proto.MESSAGE, number=7, message="FeedItemValidationError",
    )
    quality_approval_status = proto.Field(
        proto.ENUM,
        number=8,
        enum=feed_item_quality_approval_status.FeedItemQualityApprovalStatusEnum.FeedItemQualityApprovalStatus,
    )
    quality_disapproval_reasons = proto.RepeatedField(
        proto.ENUM,
        number=9,
        enum=feed_item_quality_disapproval_reason.FeedItemQualityDisapprovalReasonEnum.FeedItemQualityDisapprovalReason,
    )


class FeedItemValidationError(proto.Message):
    r"""Stores a validation error and the set of offending feed
    attributes which together are responsible for causing a feed
    item validation error.

    Attributes:
        validation_error (google.ads.googleads.v4.errors.types.FeedItemValidationErrorEnum.FeedItemValidationError):
            Output only. Error code indicating what
            validation error was triggered. The description
            of the error can be found in the 'description'
            field.
        description (google.protobuf.wrappers_pb2.StringValue):
            Output only. The description of the
            validation error.
        feed_attribute_ids (Sequence[google.protobuf.wrappers_pb2.Int64Value]):
            Output only. Set of feed attributes in the
            feed item flagged during validation. If empty,
            no specific feed attributes can be associated
            with the error (e.g. error across the entire
            feed item).
        extra_info (google.protobuf.wrappers_pb2.StringValue):
            Output only. Any extra information related to this error
            which is not captured by validation_error and
            feed_attribute_id (e.g. placeholder field IDs when
            feed_attribute_id is not mapped). Note that extra_info is
            not localized.
    """

    validation_error = proto.Field(
        proto.ENUM,
        number=1,
        enum=feed_item_validation_error.FeedItemValidationErrorEnum.FeedItemValidationError,
    )
    description = proto.Field(
        proto.MESSAGE, number=2, message=wrappers.StringValue,
    )
    feed_attribute_ids = proto.RepeatedField(
        proto.MESSAGE, number=3, message=wrappers.Int64Value,
    )
    extra_info = proto.Field(
        proto.MESSAGE, number=5, message=wrappers.StringValue,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
