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


from google.ads.googleads.v4.enums.types import (
    customer_pay_per_conversion_eligibility_failure_reason,
)
from google.protobuf import wrappers_pb2 as wrappers  # type: ignore


__protobuf__ = proto.module(
    package="google.ads.googleads.v4.resources",
    marshal="google.ads.googleads.v4",
    manifest={
        "Customer",
        "CallReportingSetting",
        "ConversionTrackingSetting",
        "RemarketingSetting",
    },
)


class Customer(proto.Message):
    r"""A customer.

    Attributes:
        resource_name (str):
            Immutable. The resource name of the customer. Customer
            resource names have the form:

            ``customers/{customer_id}``
        id (google.protobuf.wrappers_pb2.Int64Value):
            Output only. The ID of the customer.
        descriptive_name (google.protobuf.wrappers_pb2.StringValue):
            Optional, non-unique descriptive name of the
            customer.
        currency_code (google.protobuf.wrappers_pb2.StringValue):
            Immutable. The currency in which the account
            operates. A subset of the currency codes from
            the ISO 4217 standard is supported.
        time_zone (google.protobuf.wrappers_pb2.StringValue):
            Immutable. The local timezone ID of the
            customer.
        tracking_url_template (google.protobuf.wrappers_pb2.StringValue):
            The URL template for constructing a tracking
            URL out of parameters.
        final_url_suffix (google.protobuf.wrappers_pb2.StringValue):
            The URL template for appending params to the
            final URL
        auto_tagging_enabled (google.protobuf.wrappers_pb2.BoolValue):
            Whether auto-tagging is enabled for the
            customer.
        has_partners_badge (google.protobuf.wrappers_pb2.BoolValue):
            Output only. Whether the Customer has a
            Partners program badge. If the Customer is not
            associated with the Partners program, this will
            be false. For more information, see
            https://support.google.com/partners/answer/3125774.
        manager (google.protobuf.wrappers_pb2.BoolValue):
            Output only. Whether the customer is a
            manager.
        test_account (google.protobuf.wrappers_pb2.BoolValue):
            Output only. Whether the customer is a test
            account.
        call_reporting_setting (google.ads.googleads.v4.resources.types.CallReportingSetting):
            Call reporting setting for a customer.
        conversion_tracking_setting (google.ads.googleads.v4.resources.types.ConversionTrackingSetting):
            Output only. Conversion tracking setting for
            a customer.
        remarketing_setting (google.ads.googleads.v4.resources.types.RemarketingSetting):
            Output only. Remarketing setting for a
            customer.
        pay_per_conversion_eligibility_failure_reasons (Sequence[google.ads.googleads.v4.enums.types.CustomerPayPerConversionEligibilityFailureReasonEnum.CustomerPayPerConversionEligibilityFailureReason]):
            Output only. Reasons why the customer is not
            eligible to use PaymentMode.CONVERSIONS. If the
            list is empty, the customer is eligible. This
            field is read-only.
        optimization_score (google.protobuf.wrappers_pb2.DoubleValue):
            Output only. Optimization score of the
            customer.
            Optimization score is an estimate of how well a
            customer's campaigns are set to perform. It
            ranges from 0% (0.0) to 100% (1.0). This field
            is null for all manager customers, and for
            unscored non-manager customers.
            See "About optimization score" at
            https://support.google.com/google-
            ads/answer/9061546.
            This field is read-only.
    """

    resource_name = proto.Field(proto.STRING, number=1)
    id = proto.Field(proto.MESSAGE, number=3, message=wrappers.Int64Value,)
    descriptive_name = proto.Field(
        proto.MESSAGE, number=4, message=wrappers.StringValue,
    )
    currency_code = proto.Field(
        proto.MESSAGE, number=5, message=wrappers.StringValue,
    )
    time_zone = proto.Field(
        proto.MESSAGE, number=6, message=wrappers.StringValue,
    )
    tracking_url_template = proto.Field(
        proto.MESSAGE, number=7, message=wrappers.StringValue,
    )
    final_url_suffix = proto.Field(
        proto.MESSAGE, number=11, message=wrappers.StringValue,
    )
    auto_tagging_enabled = proto.Field(
        proto.MESSAGE, number=8, message=wrappers.BoolValue,
    )
    has_partners_badge = proto.Field(
        proto.MESSAGE, number=9, message=wrappers.BoolValue,
    )
    manager = proto.Field(proto.MESSAGE, number=12, message=wrappers.BoolValue,)
    test_account = proto.Field(
        proto.MESSAGE, number=13, message=wrappers.BoolValue,
    )
    call_reporting_setting = proto.Field(
        proto.MESSAGE, number=10, message="CallReportingSetting",
    )
    conversion_tracking_setting = proto.Field(
        proto.MESSAGE, number=14, message="ConversionTrackingSetting",
    )
    remarketing_setting = proto.Field(
        proto.MESSAGE, number=15, message="RemarketingSetting",
    )
    pay_per_conversion_eligibility_failure_reasons = proto.RepeatedField(
        proto.ENUM,
        number=16,
        enum=customer_pay_per_conversion_eligibility_failure_reason.CustomerPayPerConversionEligibilityFailureReasonEnum.CustomerPayPerConversionEligibilityFailureReason,
    )
    optimization_score = proto.Field(
        proto.MESSAGE, number=17, message=wrappers.DoubleValue,
    )


class CallReportingSetting(proto.Message):
    r"""Call reporting setting for a customer.

    Attributes:
        call_reporting_enabled (google.protobuf.wrappers_pb2.BoolValue):
            Enable reporting of phone call events by
            redirecting them via Google System.
        call_conversion_reporting_enabled (google.protobuf.wrappers_pb2.BoolValue):
            Whether to enable call conversion reporting.
        call_conversion_action (google.protobuf.wrappers_pb2.StringValue):
            Customer-level call conversion action to attribute a call
            conversion to. If not set a default conversion action is
            used. Only in effect when call_conversion_reporting_enabled
            is set to true.
    """

    call_reporting_enabled = proto.Field(
        proto.MESSAGE, number=1, message=wrappers.BoolValue,
    )
    call_conversion_reporting_enabled = proto.Field(
        proto.MESSAGE, number=2, message=wrappers.BoolValue,
    )
    call_conversion_action = proto.Field(
        proto.MESSAGE, number=9, message=wrappers.StringValue,
    )


class ConversionTrackingSetting(proto.Message):
    r"""A collection of customer-wide settings related to Google Ads
    Conversion Tracking.

    Attributes:
        conversion_tracking_id (google.protobuf.wrappers_pb2.Int64Value):
            Output only. The conversion tracking id used
            for this account. This id is automatically
            assigned after any conversion tracking feature
            is used. If the customer doesn't use conversion
            tracking, this is 0. This field is read-only.
        cross_account_conversion_tracking_id (google.protobuf.wrappers_pb2.Int64Value):
            Output only. The conversion tracking id of the customer's
            manager. This is set when the customer is opted into cross
            account conversion tracking, and it overrides
            conversion_tracking_id. This field can only be managed
            through the Google Ads UI. This field is read-only.
    """

    conversion_tracking_id = proto.Field(
        proto.MESSAGE, number=1, message=wrappers.Int64Value,
    )
    cross_account_conversion_tracking_id = proto.Field(
        proto.MESSAGE, number=2, message=wrappers.Int64Value,
    )


class RemarketingSetting(proto.Message):
    r"""Remarketing setting for a customer.

    Attributes:
        google_global_site_tag (google.protobuf.wrappers_pb2.StringValue):
            Output only. The Google global site tag.
    """

    google_global_site_tag = proto.Field(
        proto.MESSAGE, number=1, message=wrappers.StringValue,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
