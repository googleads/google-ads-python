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


from google.ads.googleads.v6.enums.types import conversion_adjustment_type
from google.rpc import status_pb2 as status  # type: ignore


__protobuf__ = proto.module(
    package="google.ads.googleads.v6.services",
    marshal="google.ads.googleads.v6",
    manifest={
        "UploadConversionAdjustmentsRequest",
        "UploadConversionAdjustmentsResponse",
        "ConversionAdjustment",
        "RestatementValue",
        "GclidDateTimePair",
        "ConversionAdjustmentResult",
    },
)


class UploadConversionAdjustmentsRequest(proto.Message):
    r"""Request message for
    [ConversionAdjustmentUploadService.UploadConversionAdjustments][google.ads.googleads.v6.services.ConversionAdjustmentUploadService.UploadConversionAdjustments].

    Attributes:
        customer_id (str):
            Required. The ID of the customer performing
            the upload.
        conversion_adjustments (Sequence[google.ads.googleads.v6.services.types.ConversionAdjustment]):
            Required. The conversion adjustments that are
            being uploaded.
        partial_failure (bool):
            Required. If true, successful operations will
            be carried out and invalid operations will
            return errors. If false, all operations will be
            carried out in one transaction if and only if
            they are all valid. This should always be set to
            true.
            See
            https://developers.google.com/google-
            ads/api/docs/best-practices/partial-failures for
            more information about partial failure.
        validate_only (bool):
            If true, the request is validated but not
            executed. Only errors are returned, not results.
    """

    customer_id = proto.Field(proto.STRING, number=1)
    conversion_adjustments = proto.RepeatedField(
        proto.MESSAGE, number=2, message="ConversionAdjustment",
    )
    partial_failure = proto.Field(proto.BOOL, number=3)
    validate_only = proto.Field(proto.BOOL, number=4)


class UploadConversionAdjustmentsResponse(proto.Message):
    r"""Response message for
    [ConversionAdjustmentUploadService.UploadConversionAdjustments][google.ads.googleads.v6.services.ConversionAdjustmentUploadService.UploadConversionAdjustments].

    Attributes:
        partial_failure_error (google.rpc.status_pb2.Status):
            Errors that pertain to conversion adjustment
            failures in the partial failure mode. Returned
            when all errors occur inside the adjustments. If
            any errors occur outside the adjustments (e.g.
            auth errors), we return an RPC level error.
            See
            https://developers.google.com/google-
            ads/api/docs/best-practices/partial-failures for
            more information about partial failure.
        results (Sequence[google.ads.googleads.v6.services.types.ConversionAdjustmentResult]):
            Returned for successfully processed conversion adjustments.
            Proto will be empty for rows that received an error. Results
            are not returned when validate_only is true.
    """

    partial_failure_error = proto.Field(
        proto.MESSAGE, number=1, message=status.Status,
    )
    results = proto.RepeatedField(
        proto.MESSAGE, number=2, message="ConversionAdjustmentResult",
    )


class ConversionAdjustment(proto.Message):
    r"""A conversion adjustment.

    Attributes:
        conversion_action (str):
            Resource name of the conversion action
            associated with this conversion adjustment.
            Note: Although this resource name consists of a
            customer id and a conversion action id,
            validation will ignore the customer id and use
            the conversion action id as the sole identifier
            of the conversion action.
        adjustment_date_time (str):
            The date time at which the adjustment occurred. Must be
            after the conversion_date_time. The timezone must be
            specified. The format is "yyyy-mm-dd hh:mm:ss+|-hh:mm", e.g.
            "2019-01-01 12:32:45-08:00".
        adjustment_type (google.ads.googleads.v6.enums.types.ConversionAdjustmentTypeEnum.ConversionAdjustmentType):
            The adjustment type.
        restatement_value (google.ads.googleads.v6.services.types.RestatementValue):
            Information needed to restate the
            conversion's value. Required for restatements.
            Should not be supplied for retractions. An error
            will be returned if provided for a retraction.
            NOTE: If you want to upload a second restatement
            with a different adjusted value, it must have a
            new, more recent, adjustment occurrence time.
            Otherwise, it will be treated as a duplicate of
            the previous restatement and ignored.
        gclid_date_time_pair (google.ads.googleads.v6.services.types.GclidDateTimePair):
            Uniquely identifies a conversion that was
            reported without an order ID specified.
        order_id (str):
            The order ID of the conversion to be
            adjusted. If the conversion was reported with an
            order ID specified, that order ID must be used
            as the identifier here.
    """

    conversion_action = proto.Field(proto.STRING, number=8, optional=True)
    adjustment_date_time = proto.Field(proto.STRING, number=9, optional=True)
    adjustment_type = proto.Field(
        proto.ENUM,
        number=5,
        enum=conversion_adjustment_type.ConversionAdjustmentTypeEnum.ConversionAdjustmentType,
    )
    restatement_value = proto.Field(
        proto.MESSAGE, number=6, message="RestatementValue",
    )
    gclid_date_time_pair = proto.Field(
        proto.MESSAGE,
        number=1,
        oneof="conversion_identifier",
        message="GclidDateTimePair",
    )
    order_id = proto.Field(
        proto.STRING, number=7, oneof="conversion_identifier"
    )


class RestatementValue(proto.Message):
    r"""Contains information needed to restate a conversion's value.

    Attributes:
        adjusted_value (float):
            The restated conversion value. This is the
            value of the conversion after restatement. For
            example, to change the value of a conversion
            from 100 to 70, an adjusted value of 70 should
            be reported. NOTE: If you want to upload a
            second restatement with a different adjusted
            value, it must have a new, more recent,
            adjustment occurrence time. Otherwise, it will
            be treated as a duplicate of the previous
            restatement and ignored.
        currency_code (str):
            The currency of the restated value. If not
            provided, then the default currency from the
            conversion action is used, and if that is not
            set then the account currency is used. This is
            the ISO 4217 3-character currency code e.g. USD
            or EUR.
    """

    adjusted_value = proto.Field(proto.DOUBLE, number=3, optional=True)
    currency_code = proto.Field(proto.STRING, number=4, optional=True)


class GclidDateTimePair(proto.Message):
    r"""Uniquely identifies a conversion that was reported without an
    order ID specified.

    Attributes:
        gclid (str):
            Google click ID (gclid) associated with the
            original conversion for this adjustment.
        conversion_date_time (str):
            The date time at which the original conversion for this
            adjustment occurred. The timezone must be specified. The
            format is "yyyy-mm-dd hh:mm:ss+|-hh:mm", e.g. "2019-01-01
            12:32:45-08:00".
    """

    gclid = proto.Field(proto.STRING, number=3, optional=True)
    conversion_date_time = proto.Field(proto.STRING, number=4, optional=True)


class ConversionAdjustmentResult(proto.Message):
    r"""Information identifying a successfully processed
    ConversionAdjustment.

    Attributes:
        conversion_action (str):
            Resource name of the conversion action
            associated with this conversion adjustment.
        adjustment_date_time (str):
            The date time at which the adjustment occurred. The format
            is "yyyy-mm-dd hh:mm:ss+|-hh:mm", e.g. "2019-01-01
            12:32:45-08:00".
        adjustment_type (google.ads.googleads.v6.enums.types.ConversionAdjustmentTypeEnum.ConversionAdjustmentType):
            The adjustment type.
        gclid_date_time_pair (google.ads.googleads.v6.services.types.GclidDateTimePair):
            Uniquely identifies a conversion that was
            reported without an order ID specified.
        order_id (str):
            The order ID of the conversion that was
            adjusted.
    """

    conversion_action = proto.Field(proto.STRING, number=7, optional=True)
    adjustment_date_time = proto.Field(proto.STRING, number=8, optional=True)
    adjustment_type = proto.Field(
        proto.ENUM,
        number=5,
        enum=conversion_adjustment_type.ConversionAdjustmentTypeEnum.ConversionAdjustmentType,
    )
    gclid_date_time_pair = proto.Field(
        proto.MESSAGE,
        number=1,
        oneof="conversion_identifier",
        message="GclidDateTimePair",
    )
    order_id = proto.Field(
        proto.STRING, number=6, oneof="conversion_identifier"
    )


__all__ = tuple(sorted(__protobuf__.manifest))
