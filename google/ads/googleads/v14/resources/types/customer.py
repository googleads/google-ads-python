# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
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

from google.ads.googleads.v14.enums.types import conversion_tracking_status_enum
from google.ads.googleads.v14.enums.types import (
    customer_pay_per_conversion_eligibility_failure_reason,
)
from google.ads.googleads.v14.enums.types import customer_status
from google.ads.googleads.v14.enums.types import (
    offline_conversion_diagnostic_status_enum,
)
from google.ads.googleads.v14.enums.types import (
    offline_event_upload_client_enum,
)
from google.ads.googleads.v14.errors.types import (
    collection_size_error as gage_collection_size_error,
)
from google.ads.googleads.v14.errors.types import (
    conversion_adjustment_upload_error as gage_conversion_adjustment_upload_error,
)
from google.ads.googleads.v14.errors.types import (
    conversion_upload_error as gage_conversion_upload_error,
)
from google.ads.googleads.v14.errors.types import date_error as gage_date_error
from google.ads.googleads.v14.errors.types import (
    distinct_error as gage_distinct_error,
)
from google.ads.googleads.v14.errors.types import (
    field_error as gage_field_error,
)
from google.ads.googleads.v14.errors.types import (
    mutate_error as gage_mutate_error,
)
from google.ads.googleads.v14.errors.types import (
    not_allowlisted_error as gage_not_allowlisted_error,
)
from google.ads.googleads.v14.errors.types import (
    string_format_error as gage_string_format_error,
)
from google.ads.googleads.v14.errors.types import (
    string_length_error as gage_string_length_error,
)


__protobuf__ = proto.module(
    package="google.ads.googleads.v14.resources",
    marshal="google.ads.googleads.v14",
    manifest={
        "Customer",
        "CallReportingSetting",
        "ConversionTrackingSetting",
        "RemarketingSetting",
        "OfflineConversionClientSummary",
        "OfflineConversionUploadSummary",
        "OfflineConversionUploadAlert",
        "OfflineConversionUploadError",
        "CustomerAgreementSetting",
    },
)


class Customer(proto.Message):
    r"""A customer.
    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        resource_name (str):
            Immutable. The resource name of the customer. Customer
            resource names have the form:

            ``customers/{customer_id}``
        id (int):
            Output only. The ID of the customer.

            This field is a member of `oneof`_ ``_id``.
        descriptive_name (str):
            Optional, non-unique descriptive name of the
            customer.

            This field is a member of `oneof`_ ``_descriptive_name``.
        currency_code (str):
            Immutable. The currency in which the account
            operates. A subset of the currency codes from
            the ISO 4217 standard is supported.

            This field is a member of `oneof`_ ``_currency_code``.
        time_zone (str):
            Immutable. The local timezone ID of the
            customer.

            This field is a member of `oneof`_ ``_time_zone``.
        tracking_url_template (str):
            The URL template for constructing a tracking URL out of
            parameters. Only mutable in an ``update`` operation.

            This field is a member of `oneof`_ ``_tracking_url_template``.
        final_url_suffix (str):
            The URL template for appending params to the final URL. Only
            mutable in an ``update`` operation.

            This field is a member of `oneof`_ ``_final_url_suffix``.
        auto_tagging_enabled (bool):
            Whether auto-tagging is enabled for the
            customer.

            This field is a member of `oneof`_ ``_auto_tagging_enabled``.
        has_partners_badge (bool):
            Output only. Whether the Customer has a
            Partners program badge. If the Customer is not
            associated with the Partners program, this will
            be false. For more information, see
            https://support.google.com/partners/answer/3125774.

            This field is a member of `oneof`_ ``_has_partners_badge``.
        manager (bool):
            Output only. Whether the customer is a
            manager.

            This field is a member of `oneof`_ ``_manager``.
        test_account (bool):
            Output only. Whether the customer is a test
            account.

            This field is a member of `oneof`_ ``_test_account``.
        call_reporting_setting (google.ads.googleads.v14.resources.types.CallReportingSetting):
            Call reporting setting for a customer. Only mutable in an
            ``update`` operation.
        conversion_tracking_setting (google.ads.googleads.v14.resources.types.ConversionTrackingSetting):
            Output only. Conversion tracking setting for
            a customer.
        remarketing_setting (google.ads.googleads.v14.resources.types.RemarketingSetting):
            Output only. Remarketing setting for a
            customer.
        pay_per_conversion_eligibility_failure_reasons (MutableSequence[google.ads.googleads.v14.enums.types.CustomerPayPerConversionEligibilityFailureReasonEnum.CustomerPayPerConversionEligibilityFailureReason]):
            Output only. Reasons why the customer is not
            eligible to use PaymentMode.CONVERSIONS. If the
            list is empty, the customer is eligible. This
            field is read-only.
        optimization_score (float):
            Output only. Optimization score of the
            customer.
            Optimization score is an estimate of how well a
            customer's campaigns are set to perform. It
            ranges from 0% (0.0) to 100% (1.0). This field
            is null for all manager customers, and for
            unscored non-manager customers.

            See "About optimization score" at
            https://support.google.com/google-ads/answer/9061546.

            This field is read-only.

            This field is a member of `oneof`_ ``_optimization_score``.
        optimization_score_weight (float):
            Output only. Optimization score weight of the customer.

            Optimization score weight can be used to compare/aggregate
            optimization scores across multiple non-manager customers.
            The aggregate optimization score of a manager is computed as
            the sum over all of their customers of
            ``Customer.optimization_score * Customer.optimization_score_weight``.
            This field is 0 for all manager customers, and for unscored
            non-manager customers.

            This field is read-only.
        status (google.ads.googleads.v14.enums.types.CustomerStatusEnum.CustomerStatus):
            Output only. The status of the customer.
        location_asset_auto_migration_done (bool):
            Output only. True if feed based location has
            been migrated to asset based location.

            This field is a member of `oneof`_ ``_location_asset_auto_migration_done``.
        image_asset_auto_migration_done (bool):
            Output only. True if feed based image has
            been migrated to asset based image.

            This field is a member of `oneof`_ ``_image_asset_auto_migration_done``.
        location_asset_auto_migration_done_date_time (str):
            Output only. Timestamp of migration from feed
            based location to asset base location in
            yyyy-MM-dd HH:mm:ss format.

            This field is a member of `oneof`_ ``_location_asset_auto_migration_done_date_time``.
        image_asset_auto_migration_done_date_time (str):
            Output only. Timestamp of migration from feed
            based image to asset base image in yyyy-MM-dd
            HH:mm:ss format.

            This field is a member of `oneof`_ ``_image_asset_auto_migration_done_date_time``.
        offline_conversion_client_summaries (MutableSequence[google.ads.googleads.v14.resources.types.OfflineConversionClientSummary]):
            Output only. Offline conversion upload
            diagnostics.
        customer_agreement_setting (google.ads.googleads.v14.resources.types.CustomerAgreementSetting):
            Output only. Customer Agreement Setting for a
            customer.
    """

    resource_name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    id: int = proto.Field(
        proto.INT64,
        number=19,
        optional=True,
    )
    descriptive_name: str = proto.Field(
        proto.STRING,
        number=20,
        optional=True,
    )
    currency_code: str = proto.Field(
        proto.STRING,
        number=21,
        optional=True,
    )
    time_zone: str = proto.Field(
        proto.STRING,
        number=22,
        optional=True,
    )
    tracking_url_template: str = proto.Field(
        proto.STRING,
        number=23,
        optional=True,
    )
    final_url_suffix: str = proto.Field(
        proto.STRING,
        number=24,
        optional=True,
    )
    auto_tagging_enabled: bool = proto.Field(
        proto.BOOL,
        number=25,
        optional=True,
    )
    has_partners_badge: bool = proto.Field(
        proto.BOOL,
        number=26,
        optional=True,
    )
    manager: bool = proto.Field(
        proto.BOOL,
        number=27,
        optional=True,
    )
    test_account: bool = proto.Field(
        proto.BOOL,
        number=28,
        optional=True,
    )
    call_reporting_setting: "CallReportingSetting" = proto.Field(
        proto.MESSAGE,
        number=10,
        message="CallReportingSetting",
    )
    conversion_tracking_setting: "ConversionTrackingSetting" = proto.Field(
        proto.MESSAGE,
        number=14,
        message="ConversionTrackingSetting",
    )
    remarketing_setting: "RemarketingSetting" = proto.Field(
        proto.MESSAGE,
        number=15,
        message="RemarketingSetting",
    )
    pay_per_conversion_eligibility_failure_reasons: MutableSequence[
        customer_pay_per_conversion_eligibility_failure_reason.CustomerPayPerConversionEligibilityFailureReasonEnum.CustomerPayPerConversionEligibilityFailureReason
    ] = proto.RepeatedField(
        proto.ENUM,
        number=16,
        enum=customer_pay_per_conversion_eligibility_failure_reason.CustomerPayPerConversionEligibilityFailureReasonEnum.CustomerPayPerConversionEligibilityFailureReason,
    )
    optimization_score: float = proto.Field(
        proto.DOUBLE,
        number=29,
        optional=True,
    )
    optimization_score_weight: float = proto.Field(
        proto.DOUBLE,
        number=30,
    )
    status: customer_status.CustomerStatusEnum.CustomerStatus = proto.Field(
        proto.ENUM,
        number=36,
        enum=customer_status.CustomerStatusEnum.CustomerStatus,
    )
    location_asset_auto_migration_done: bool = proto.Field(
        proto.BOOL,
        number=38,
        optional=True,
    )
    image_asset_auto_migration_done: bool = proto.Field(
        proto.BOOL,
        number=39,
        optional=True,
    )
    location_asset_auto_migration_done_date_time: str = proto.Field(
        proto.STRING,
        number=40,
        optional=True,
    )
    image_asset_auto_migration_done_date_time: str = proto.Field(
        proto.STRING,
        number=41,
        optional=True,
    )
    offline_conversion_client_summaries: MutableSequence[
        "OfflineConversionClientSummary"
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=43,
        message="OfflineConversionClientSummary",
    )
    customer_agreement_setting: "CustomerAgreementSetting" = proto.Field(
        proto.MESSAGE,
        number=44,
        message="CustomerAgreementSetting",
    )


class CallReportingSetting(proto.Message):
    r"""Call reporting setting for a customer. Only mutable in an ``update``
    operation.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        call_reporting_enabled (bool):
            Enable reporting of phone call events by
            redirecting them through Google System.

            This field is a member of `oneof`_ ``_call_reporting_enabled``.
        call_conversion_reporting_enabled (bool):
            Whether to enable call conversion reporting.

            This field is a member of `oneof`_ ``_call_conversion_reporting_enabled``.
        call_conversion_action (str):
            Customer-level call conversion action to attribute a call
            conversion to. If not set a default conversion action is
            used. Only in effect when call_conversion_reporting_enabled
            is set to true.

            This field is a member of `oneof`_ ``_call_conversion_action``.
    """

    call_reporting_enabled: bool = proto.Field(
        proto.BOOL,
        number=10,
        optional=True,
    )
    call_conversion_reporting_enabled: bool = proto.Field(
        proto.BOOL,
        number=11,
        optional=True,
    )
    call_conversion_action: str = proto.Field(
        proto.STRING,
        number=12,
        optional=True,
    )


class ConversionTrackingSetting(proto.Message):
    r"""A collection of customer-wide settings related to Google Ads
    Conversion Tracking.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        conversion_tracking_id (int):
            Output only. The conversion tracking id used for this
            account. This id doesn't indicate whether the customer uses
            conversion tracking (conversion_tracking_status does). This
            field is read-only.

            This field is a member of `oneof`_ ``_conversion_tracking_id``.
        cross_account_conversion_tracking_id (int):
            Output only. The conversion tracking id of the customer's
            manager. This is set when the customer is opted into cross
            account conversion tracking, and it overrides
            conversion_tracking_id. This field can only be managed
            through the Google Ads UI. This field is read-only.

            This field is a member of `oneof`_ ``_cross_account_conversion_tracking_id``.
        accepted_customer_data_terms (bool):
            Output only. Whether the customer has
            accepted customer data terms. If using
            cross-account conversion tracking, this value is
            inherited from the manager. This field is
            read-only. For more
            information, see
            https://support.google.com/adspolicy/answer/7475709.
        conversion_tracking_status (google.ads.googleads.v14.enums.types.ConversionTrackingStatusEnum.ConversionTrackingStatus):
            Output only. Conversion tracking status. It indicates
            whether the customer is using conversion tracking, and who
            is the conversion tracking owner of this customer. If this
            customer is using cross-account conversion tracking, the
            value returned will differ based on the
            ``login-customer-id`` of the request.
        enhanced_conversions_for_leads_enabled (bool):
            Output only. Whether the customer is opted-in
            for enhanced conversions for leads. If using
            cross-account conversion tracking, this value is
            inherited from the manager. This field is
            read-only.
        google_ads_conversion_customer (str):
            Output only. The resource name of the
            customer where conversions are created and
            managed. This field is read-only.
    """

    conversion_tracking_id: int = proto.Field(
        proto.INT64,
        number=3,
        optional=True,
    )
    cross_account_conversion_tracking_id: int = proto.Field(
        proto.INT64,
        number=4,
        optional=True,
    )
    accepted_customer_data_terms: bool = proto.Field(
        proto.BOOL,
        number=5,
    )
    conversion_tracking_status: conversion_tracking_status_enum.ConversionTrackingStatusEnum.ConversionTrackingStatus = proto.Field(
        proto.ENUM,
        number=6,
        enum=conversion_tracking_status_enum.ConversionTrackingStatusEnum.ConversionTrackingStatus,
    )
    enhanced_conversions_for_leads_enabled: bool = proto.Field(
        proto.BOOL,
        number=7,
    )
    google_ads_conversion_customer: str = proto.Field(
        proto.STRING,
        number=8,
    )


class RemarketingSetting(proto.Message):
    r"""Remarketing setting for a customer.
    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        google_global_site_tag (str):
            Output only. The Google tag.

            This field is a member of `oneof`_ ``_google_global_site_tag``.
    """

    google_global_site_tag: str = proto.Field(
        proto.STRING,
        number=2,
        optional=True,
    )


class OfflineConversionClientSummary(proto.Message):
    r"""Offline conversion upload diagnostic summarized by client.
    This proto contains general information, breakdown by date/job
    and alerts for offline conversion upload results.

    Attributes:
        client (google.ads.googleads.v14.enums.types.OfflineEventUploadClientEnum.OfflineEventUploadClient):
            Output only. Client type of the upload event.
        status (google.ads.googleads.v14.enums.types.OfflineConversionDiagnosticStatusEnum.OfflineConversionDiagnosticStatus):
            Output only. Overall status for offline
            conversion client summary. Status is generated
            from most recent calendar day with upload stats.
        total_event_count (int):
            Output only. Total count of uploaded events.
        successful_event_count (int):
            Output only. Total count of successful
            uploaded events.
        success_rate (float):
            Output only. Successful rate.
        last_upload_date_time (str):
            Output only. Date for the latest upload
            batch.
        daily_summaries (MutableSequence[google.ads.googleads.v14.resources.types.OfflineConversionUploadSummary]):
            Output only. Summary of history stats by last
            N days.
        job_summaries (MutableSequence[google.ads.googleads.v14.resources.types.OfflineConversionUploadSummary]):
            Output only. Summary of history stats by last
            N jobs.
        alerts (MutableSequence[google.ads.googleads.v14.resources.types.OfflineConversionUploadAlert]):
            Output only. Details for each error code.
            Alerts are generated from most recent calendar
            day with upload stats.
    """

    client: offline_event_upload_client_enum.OfflineEventUploadClientEnum.OfflineEventUploadClient = proto.Field(
        proto.ENUM,
        number=1,
        enum=offline_event_upload_client_enum.OfflineEventUploadClientEnum.OfflineEventUploadClient,
    )
    status: offline_conversion_diagnostic_status_enum.OfflineConversionDiagnosticStatusEnum.OfflineConversionDiagnosticStatus = proto.Field(
        proto.ENUM,
        number=2,
        enum=offline_conversion_diagnostic_status_enum.OfflineConversionDiagnosticStatusEnum.OfflineConversionDiagnosticStatus,
    )
    total_event_count: int = proto.Field(
        proto.INT64,
        number=3,
    )
    successful_event_count: int = proto.Field(
        proto.INT64,
        number=4,
    )
    success_rate: float = proto.Field(
        proto.DOUBLE,
        number=5,
    )
    last_upload_date_time: str = proto.Field(
        proto.STRING,
        number=6,
    )
    daily_summaries: MutableSequence[
        "OfflineConversionUploadSummary"
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=7,
        message="OfflineConversionUploadSummary",
    )
    job_summaries: MutableSequence[
        "OfflineConversionUploadSummary"
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=8,
        message="OfflineConversionUploadSummary",
    )
    alerts: MutableSequence[
        "OfflineConversionUploadAlert"
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=9,
        message="OfflineConversionUploadAlert",
    )


class OfflineConversionUploadSummary(proto.Message):
    r"""Historical upload summary, grouped by upload date or job.
    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        successful_count (int):
            Output only. Total count of successful event.
        failed_count (int):
            Output only. Total count of failed event.
        job_id (int):
            Output only. Dimension key for last N jobs.

            This field is a member of `oneof`_ ``dimension_key``.
        upload_date (str):
            Output only. Dimension key for last N days.

            This field is a member of `oneof`_ ``dimension_key``.
    """

    successful_count: int = proto.Field(
        proto.INT64,
        number=3,
    )
    failed_count: int = proto.Field(
        proto.INT64,
        number=4,
    )
    job_id: int = proto.Field(
        proto.INT64,
        number=1,
        oneof="dimension_key",
    )
    upload_date: str = proto.Field(
        proto.STRING,
        number=2,
        oneof="dimension_key",
    )


class OfflineConversionUploadAlert(proto.Message):
    r"""Alert for offline conversion client summary.
    Attributes:
        error (google.ads.googleads.v14.resources.types.OfflineConversionUploadError):
            Output only. Error for offline conversion
            client alert.
        error_percentage (float):
            Output only. Percentage of the error.
    """

    error: "OfflineConversionUploadError" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="OfflineConversionUploadError",
    )
    error_percentage: float = proto.Field(
        proto.DOUBLE,
        number=2,
    )


class OfflineConversionUploadError(proto.Message):
    r"""Possible errors for offline conversion client summary.
    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        collection_size_error (google.ads.googleads.v14.errors.types.CollectionSizeErrorEnum.CollectionSizeError):
            Output only. Collection size error.

            This field is a member of `oneof`_ ``error_code``.
        conversion_adjustment_upload_error (google.ads.googleads.v14.errors.types.ConversionAdjustmentUploadErrorEnum.ConversionAdjustmentUploadError):
            Output only. Conversion adjustment upload
            error.

            This field is a member of `oneof`_ ``error_code``.
        conversion_upload_error (google.ads.googleads.v14.errors.types.ConversionUploadErrorEnum.ConversionUploadError):
            Output only. Conversion upload error.

            This field is a member of `oneof`_ ``error_code``.
        date_error (google.ads.googleads.v14.errors.types.DateErrorEnum.DateError):
            Output only. Date error.

            This field is a member of `oneof`_ ``error_code``.
        distinct_error (google.ads.googleads.v14.errors.types.DistinctErrorEnum.DistinctError):
            Output only. Distinct error.

            This field is a member of `oneof`_ ``error_code``.
        field_error (google.ads.googleads.v14.errors.types.FieldErrorEnum.FieldError):
            Output only. Field error.

            This field is a member of `oneof`_ ``error_code``.
        mutate_error (google.ads.googleads.v14.errors.types.MutateErrorEnum.MutateError):
            Output only. Mutate error.

            This field is a member of `oneof`_ ``error_code``.
        not_allowlisted_error (google.ads.googleads.v14.errors.types.NotAllowlistedErrorEnum.NotAllowlistedError):
            Output only. Not allowlisted error.

            This field is a member of `oneof`_ ``error_code``.
        string_format_error (google.ads.googleads.v14.errors.types.StringFormatErrorEnum.StringFormatError):
            Output only. String format error.

            This field is a member of `oneof`_ ``error_code``.
        string_length_error (google.ads.googleads.v14.errors.types.StringLengthErrorEnum.StringLengthError):
            Output only. String length error.

            This field is a member of `oneof`_ ``error_code``.
    """

    collection_size_error: gage_collection_size_error.CollectionSizeErrorEnum.CollectionSizeError = proto.Field(
        proto.ENUM,
        number=1,
        oneof="error_code",
        enum=gage_collection_size_error.CollectionSizeErrorEnum.CollectionSizeError,
    )
    conversion_adjustment_upload_error: gage_conversion_adjustment_upload_error.ConversionAdjustmentUploadErrorEnum.ConversionAdjustmentUploadError = proto.Field(
        proto.ENUM,
        number=2,
        oneof="error_code",
        enum=gage_conversion_adjustment_upload_error.ConversionAdjustmentUploadErrorEnum.ConversionAdjustmentUploadError,
    )
    conversion_upload_error: gage_conversion_upload_error.ConversionUploadErrorEnum.ConversionUploadError = proto.Field(
        proto.ENUM,
        number=3,
        oneof="error_code",
        enum=gage_conversion_upload_error.ConversionUploadErrorEnum.ConversionUploadError,
    )
    date_error: gage_date_error.DateErrorEnum.DateError = proto.Field(
        proto.ENUM,
        number=4,
        oneof="error_code",
        enum=gage_date_error.DateErrorEnum.DateError,
    )
    distinct_error: gage_distinct_error.DistinctErrorEnum.DistinctError = (
        proto.Field(
            proto.ENUM,
            number=5,
            oneof="error_code",
            enum=gage_distinct_error.DistinctErrorEnum.DistinctError,
        )
    )
    field_error: gage_field_error.FieldErrorEnum.FieldError = proto.Field(
        proto.ENUM,
        number=6,
        oneof="error_code",
        enum=gage_field_error.FieldErrorEnum.FieldError,
    )
    mutate_error: gage_mutate_error.MutateErrorEnum.MutateError = proto.Field(
        proto.ENUM,
        number=7,
        oneof="error_code",
        enum=gage_mutate_error.MutateErrorEnum.MutateError,
    )
    not_allowlisted_error: gage_not_allowlisted_error.NotAllowlistedErrorEnum.NotAllowlistedError = proto.Field(
        proto.ENUM,
        number=8,
        oneof="error_code",
        enum=gage_not_allowlisted_error.NotAllowlistedErrorEnum.NotAllowlistedError,
    )
    string_format_error: gage_string_format_error.StringFormatErrorEnum.StringFormatError = proto.Field(
        proto.ENUM,
        number=9,
        oneof="error_code",
        enum=gage_string_format_error.StringFormatErrorEnum.StringFormatError,
    )
    string_length_error: gage_string_length_error.StringLengthErrorEnum.StringLengthError = proto.Field(
        proto.ENUM,
        number=10,
        oneof="error_code",
        enum=gage_string_length_error.StringLengthErrorEnum.StringLengthError,
    )


class CustomerAgreementSetting(proto.Message):
    r"""Customer Agreement Setting for a customer.
    Attributes:
        accepted_lead_form_terms (bool):
            Output only. Whether the customer has
            accepted lead form term of service.
    """

    accepted_lead_form_terms: bool = proto.Field(
        proto.BOOL,
        number=1,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
