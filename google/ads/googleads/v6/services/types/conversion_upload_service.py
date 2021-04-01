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


from google.rpc import status_pb2 as status  # type: ignore


__protobuf__ = proto.module(
    package="google.ads.googleads.v6.services",
    marshal="google.ads.googleads.v6",
    manifest={
        "UploadClickConversionsRequest",
        "UploadClickConversionsResponse",
        "UploadCallConversionsRequest",
        "UploadCallConversionsResponse",
        "ClickConversion",
        "CallConversion",
        "ExternalAttributionData",
        "ClickConversionResult",
        "CallConversionResult",
    },
)


class UploadClickConversionsRequest(proto.Message):
    r"""Request message for
    [ConversionUploadService.UploadClickConversions][google.ads.googleads.v6.services.ConversionUploadService.UploadClickConversions].

    Attributes:
        customer_id (str):
            Required. The ID of the customer performing
            the upload.
        conversions (Sequence[google.ads.googleads.v6.services.types.ClickConversion]):
            Required. The conversions that are being
            uploaded.
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
    conversions = proto.RepeatedField(
        proto.MESSAGE, number=2, message="ClickConversion",
    )
    partial_failure = proto.Field(proto.BOOL, number=3)
    validate_only = proto.Field(proto.BOOL, number=4)


class UploadClickConversionsResponse(proto.Message):
    r"""Response message for
    [ConversionUploadService.UploadClickConversions][google.ads.googleads.v6.services.ConversionUploadService.UploadClickConversions].

    Attributes:
        partial_failure_error (google.rpc.status_pb2.Status):
            Errors that pertain to conversion failures in
            the partial failure mode. Returned when all
            errors occur inside the conversions. If any
            errors occur outside the conversions (e.g. auth
            errors), we return an RPC level error. See
            https://developers.google.com/google-
            ads/api/docs/best-practices/partial-failures for
            more information about partial failure.
        results (Sequence[google.ads.googleads.v6.services.types.ClickConversionResult]):
            Returned for successfully processed conversions. Proto will
            be empty for rows that received an error. Results are not
            returned when validate_only is true.
    """

    partial_failure_error = proto.Field(
        proto.MESSAGE, number=1, message=status.Status,
    )
    results = proto.RepeatedField(
        proto.MESSAGE, number=2, message="ClickConversionResult",
    )


class UploadCallConversionsRequest(proto.Message):
    r"""Request message for
    [ConversionUploadService.UploadCallConversions][google.ads.googleads.v6.services.ConversionUploadService.UploadCallConversions].

    Attributes:
        customer_id (str):
            Required. The ID of the customer performing
            the upload.
        conversions (Sequence[google.ads.googleads.v6.services.types.CallConversion]):
            Required. The conversions that are being
            uploaded.
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
    conversions = proto.RepeatedField(
        proto.MESSAGE, number=2, message="CallConversion",
    )
    partial_failure = proto.Field(proto.BOOL, number=3)
    validate_only = proto.Field(proto.BOOL, number=4)


class UploadCallConversionsResponse(proto.Message):
    r"""Response message for
    [ConversionUploadService.UploadCallConversions][google.ads.googleads.v6.services.ConversionUploadService.UploadCallConversions].

    Attributes:
        partial_failure_error (google.rpc.status_pb2.Status):
            Errors that pertain to conversion failures in
            the partial failure mode. Returned when all
            errors occur inside the conversions. If any
            errors occur outside the conversions (e.g. auth
            errors), we return an RPC level error. See
            https://developers.google.com/google-
            ads/api/docs/best-practices/partial-failures for
            more information about partial failure.
        results (Sequence[google.ads.googleads.v6.services.types.CallConversionResult]):
            Returned for successfully processed conversions. Proto will
            be empty for rows that received an error. Results are not
            returned when validate_only is true.
    """

    partial_failure_error = proto.Field(
        proto.MESSAGE, number=1, message=status.Status,
    )
    results = proto.RepeatedField(
        proto.MESSAGE, number=2, message="CallConversionResult",
    )


class ClickConversion(proto.Message):
    r"""A click conversion.

    Attributes:
        gclid (str):
            The Google click ID (gclid) associated with
            this conversion.
        conversion_action (str):
            Resource name of the conversion action
            associated with this conversion. Note: Although
            this resource name consists of a customer id and
            a conversion action id, validation will ignore
            the customer id and use the conversion action id
            as the sole identifier of the conversion action.
        conversion_date_time (str):
            The date time at which the conversion occurred. Must be
            after the click time. The timezone must be specified. The
            format is "yyyy-mm-dd hh:mm:ss+|-hh:mm", e.g. “2019-01-01
            12:32:45-08:00”.
        conversion_value (float):
            The value of the conversion for the
            advertiser.
        currency_code (str):
            Currency associated with the conversion
            value. This is the ISO 4217 3-character currency
            code. For example: USD, EUR.
        order_id (str):
            The order ID associated with the conversion.
            An order id can only be used for one conversion
            per conversion action.
        external_attribution_data (google.ads.googleads.v6.services.types.ExternalAttributionData):
            Additional data about externally attributed
            conversions. This field is required for
            conversions with an externally attributed
            conversion action, but should not be set
            otherwise.
    """

    gclid = proto.Field(proto.STRING, number=9, optional=True)
    conversion_action = proto.Field(proto.STRING, number=10, optional=True)
    conversion_date_time = proto.Field(proto.STRING, number=11, optional=True)
    conversion_value = proto.Field(proto.DOUBLE, number=12, optional=True)
    currency_code = proto.Field(proto.STRING, number=13, optional=True)
    order_id = proto.Field(proto.STRING, number=14, optional=True)
    external_attribution_data = proto.Field(
        proto.MESSAGE, number=7, message="ExternalAttributionData",
    )


class CallConversion(proto.Message):
    r"""A call conversion.

    Attributes:
        caller_id (str):
            The caller id from which this call was
            placed. Caller id is expected to be in E.164
            format with preceding '+' sign. e.g.
            "+16502531234".
        call_start_date_time (str):
            The date time at which the call occurred. The timezone must
            be specified. The format is "yyyy-mm-dd hh:mm:ss+|-hh:mm",
            e.g. "2019-01-01 12:32:45-08:00".
        conversion_action (str):
            Resource name of the conversion action
            associated with this conversion. Note: Although
            this resource name consists of a customer id and
            a conversion action id, validation will ignore
            the customer id and use the conversion action id
            as the sole identifier of the conversion action.
        conversion_date_time (str):
            The date time at which the conversion occurred. Must be
            after the call time. The timezone must be specified. The
            format is "yyyy-mm-dd hh:mm:ss+|-hh:mm", e.g. "2019-01-01
            12:32:45-08:00".
        conversion_value (float):
            The value of the conversion for the
            advertiser.
        currency_code (str):
            Currency associated with the conversion
            value. This is the ISO 4217 3-character currency
            code. For example: USD, EUR.
    """

    caller_id = proto.Field(proto.STRING, number=7, optional=True)
    call_start_date_time = proto.Field(proto.STRING, number=8, optional=True)
    conversion_action = proto.Field(proto.STRING, number=9, optional=True)
    conversion_date_time = proto.Field(proto.STRING, number=10, optional=True)
    conversion_value = proto.Field(proto.DOUBLE, number=11, optional=True)
    currency_code = proto.Field(proto.STRING, number=12, optional=True)


class ExternalAttributionData(proto.Message):
    r"""Contains additional information about externally attributed
    conversions.

    Attributes:
        external_attribution_credit (float):
            Represents the fraction of the conversion
            that is attributed to the Google Ads click.
        external_attribution_model (str):
            Specifies the attribution model name.
    """

    external_attribution_credit = proto.Field(
        proto.DOUBLE, number=3, optional=True
    )
    external_attribution_model = proto.Field(
        proto.STRING, number=4, optional=True
    )


class ClickConversionResult(proto.Message):
    r"""Identifying information for a successfully processed
    ClickConversion.

    Attributes:
        gclid (str):
            The Google Click ID (gclid) associated with
            this conversion.
        conversion_action (str):
            Resource name of the conversion action
            associated with this conversion.
        conversion_date_time (str):
            The date time at which the conversion occurred. The format
            is "yyyy-mm-dd hh:mm:ss+|-hh:mm", e.g. “2019-01-01
            12:32:45-08:00”.
    """

    gclid = proto.Field(proto.STRING, number=4, optional=True)
    conversion_action = proto.Field(proto.STRING, number=5, optional=True)
    conversion_date_time = proto.Field(proto.STRING, number=6, optional=True)


class CallConversionResult(proto.Message):
    r"""Identifying information for a successfully processed
    CallConversionUpload.

    Attributes:
        caller_id (str):
            The caller id from which this call was
            placed. Caller id is expected to be in E.164
            format with preceding '+' sign.
        call_start_date_time (str):
            The date time at which the call occurred. The format is
            "yyyy-mm-dd hh:mm:ss+|-hh:mm", e.g. "2019-01-01
            12:32:45-08:00".
        conversion_action (str):
            Resource name of the conversion action
            associated with this conversion.
        conversion_date_time (str):
            The date time at which the conversion occurred. The format
            is "yyyy-mm-dd hh:mm:ss+|-hh:mm", e.g. "2019-01-01
            12:32:45-08:00".
    """

    caller_id = proto.Field(proto.STRING, number=5, optional=True)
    call_start_date_time = proto.Field(proto.STRING, number=6, optional=True)
    conversion_action = proto.Field(proto.STRING, number=7, optional=True)
    conversion_date_time = proto.Field(proto.STRING, number=8, optional=True)


__all__ = tuple(sorted(__protobuf__.manifest))
