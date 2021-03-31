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


__protobuf__ = proto.module(
    package="google.ads.googleads.v6.errors",
    marshal="google.ads.googleads.v6",
    manifest={"ConversionUploadErrorEnum",},
)


class ConversionUploadErrorEnum(proto.Message):
    r"""Container for enum describing possible conversion upload
    errors.
    """

    class ConversionUploadError(proto.Enum):
        r"""Enum describing possible conversion upload errors."""
        UNSPECIFIED = 0
        UNKNOWN = 1
        TOO_MANY_CONVERSIONS_IN_REQUEST = 2
        UNPARSEABLE_GCLID = 3
        CONVERSION_PRECEDES_GCLID = 4
        EXPIRED_GCLID = 5
        TOO_RECENT_GCLID = 6
        GCLID_NOT_FOUND = 7
        UNAUTHORIZED_CUSTOMER = 8
        INVALID_CONVERSION_ACTION = 9
        TOO_RECENT_CONVERSION_ACTION = 10
        CONVERSION_TRACKING_NOT_ENABLED_AT_IMPRESSION_TIME = 11
        EXTERNAL_ATTRIBUTION_DATA_SET_FOR_NON_EXTERNALLY_ATTRIBUTED_CONVERSION_ACTION = (
            12
        )
        EXTERNAL_ATTRIBUTION_DATA_NOT_SET_FOR_EXTERNALLY_ATTRIBUTED_CONVERSION_ACTION = (
            13
        )
        ORDER_ID_NOT_PERMITTED_FOR_EXTERNALLY_ATTRIBUTED_CONVERSION_ACTION = 14
        ORDER_ID_ALREADY_IN_USE = 15
        DUPLICATE_ORDER_ID = 16
        TOO_RECENT_CALL = 17
        EXPIRED_CALL = 18
        CALL_NOT_FOUND = 19
        CONVERSION_PRECEDES_CALL = 20
        CONVERSION_TRACKING_NOT_ENABLED_AT_CALL_TIME = 21
        UNPARSEABLE_CALLERS_PHONE_NUMBER = 22


__all__ = tuple(sorted(__protobuf__.manifest))
