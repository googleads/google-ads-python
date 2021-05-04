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
    package="google.ads.googleads.v7.errors",
    marshal="google.ads.googleads.v7",
    manifest={"ConversionAdjustmentUploadErrorEnum",},
)


class ConversionAdjustmentUploadErrorEnum(proto.Message):
    r"""Container for enum describing possible conversion adjustment
    upload errors.
        """

    class ConversionAdjustmentUploadError(proto.Enum):
        r"""Enum describing possible conversion adjustment upload errors."""
        UNSPECIFIED = 0
        UNKNOWN = 1
        TOO_RECENT_CONVERSION_ACTION = 2
        INVALID_CONVERSION_ACTION = 3
        CONVERSION_ALREADY_RETRACTED = 4
        CONVERSION_NOT_FOUND = 5
        CONVERSION_EXPIRED = 6
        ADJUSTMENT_PRECEDES_CONVERSION = 7
        MORE_RECENT_RESTATEMENT_FOUND = 8
        TOO_RECENT_CONVERSION = 9
        CANNOT_RESTATE_CONVERSION_ACTION_THAT_ALWAYS_USES_DEFAULT_CONVERSION_VALUE = (
            10
        )
        TOO_MANY_ADJUSTMENTS_IN_REQUEST = 11
        TOO_MANY_ADJUSTMENTS = 12


__all__ = tuple(sorted(__protobuf__.manifest))
