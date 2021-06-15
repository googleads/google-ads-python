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
    package="google.ads.googleads.v8.errors",
    marshal="google.ads.googleads.v8",
    manifest={"AssetErrorEnum",},
)


class AssetErrorEnum(proto.Message):
    r"""Container for enum describing possible asset errors.    """

    class AssetError(proto.Enum):
        r"""Enum describing possible asset errors."""
        UNSPECIFIED = 0
        UNKNOWN = 1
        CUSTOMER_NOT_ON_ALLOWLIST_FOR_ASSET_TYPE = 13
        DUPLICATE_ASSET = 3
        DUPLICATE_ASSET_NAME = 4
        ASSET_DATA_IS_MISSING = 5
        CANNOT_MODIFY_ASSET_NAME = 6
        FIELD_INCOMPATIBLE_WITH_ASSET_TYPE = 7
        INVALID_CALL_TO_ACTION_TEXT = 8
        LEAD_FORM_INVALID_FIELDS_COMBINATION = 9
        LEAD_FORM_MISSING_AGREEMENT = 10
        INVALID_ASSET_STATUS = 11
        FIELD_CANNOT_BE_MODIFIED_FOR_ASSET_TYPE = 12
        SCHEDULES_CANNOT_OVERLAP = 14
        PROMOTION_CANNOT_SET_PERCENT_OFF_AND_MONEY_AMOUNT_OFF = 15
        PROMOTION_CANNOT_SET_PROMOTION_CODE_AND_ORDERS_OVER_AMOUNT = 16
        TOO_MANY_DECIMAL_PLACES_SPECIFIED = 17
        DUPLICATE_ASSETS_WITH_DIFFERENT_FIELD_VALUE = 18


__all__ = tuple(sorted(__protobuf__.manifest))
