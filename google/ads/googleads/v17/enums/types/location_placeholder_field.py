# -*- coding: utf-8 -*-
# Copyright 2024 Google LLC
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


import proto  # type: ignore


__protobuf__ = proto.module(
    package="google.ads.googleads.v17.enums",
    marshal="google.ads.googleads.v17",
    manifest={
        "LocationPlaceholderFieldEnum",
    },
)


class LocationPlaceholderFieldEnum(proto.Message):
    r"""Values for Location placeholder fields."""

    class LocationPlaceholderField(proto.Enum):
        r"""Possible values for Location placeholder fields.

        Values:
            UNSPECIFIED (0):
                Not specified.
            UNKNOWN (1):
                Used for return value only. Represents value
                unknown in this version.
            BUSINESS_NAME (2):
                Data Type: STRING. The name of the business.
            ADDRESS_LINE_1 (3):
                Data Type: STRING. Line 1 of the business
                address.
            ADDRESS_LINE_2 (4):
                Data Type: STRING. Line 2 of the business
                address.
            CITY (5):
                Data Type: STRING. City of the business
                address.
            PROVINCE (6):
                Data Type: STRING. Province of the business
                address.
            POSTAL_CODE (7):
                Data Type: STRING. Postal code of the
                business address.
            COUNTRY_CODE (8):
                Data Type: STRING. Country code of the
                business address.
            PHONE_NUMBER (9):
                Data Type: STRING. Phone number of the
                business.
        """

        UNSPECIFIED = 0
        UNKNOWN = 1
        BUSINESS_NAME = 2
        ADDRESS_LINE_1 = 3
        ADDRESS_LINE_2 = 4
        CITY = 5
        PROVINCE = 6
        POSTAL_CODE = 7
        COUNTRY_CODE = 8
        PHONE_NUMBER = 9


__all__ = tuple(sorted(__protobuf__.manifest))
