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
    package="google.ads.googleads.v18.enums",
    marshal="google.ads.googleads.v18",
    manifest={
        "CallPlaceholderFieldEnum",
    },
)


class CallPlaceholderFieldEnum(proto.Message):
    r"""Values for Call placeholder fields."""

    class CallPlaceholderField(proto.Enum):
        r"""Possible values for Call placeholder fields.

        Values:
            UNSPECIFIED (0):
                Not specified.
            UNKNOWN (1):
                Used for return value only. Represents value
                unknown in this version.
            PHONE_NUMBER (2):
                Data Type: STRING. The advertiser's phone
                number to append to the ad.
            COUNTRY_CODE (3):
                Data Type: STRING. Uppercase two-letter
                country code of the advertiser's phone number.
            TRACKED (4):
                Data Type: BOOLEAN. Indicates whether call
                tracking is enabled. Default: true.
            CONVERSION_TYPE_ID (5):
                Data Type: INT64. The ID of an
                AdCallMetricsConversion object. This object
                contains the phoneCallDurationfield which is the
                minimum duration (in seconds) of a call to be
                considered a conversion.
            CONVERSION_REPORTING_STATE (6):
                Data Type: STRING. Indicates whether this call extension
                uses its own call conversion setting or follows the account
                level setting. Valid values are:
                USE_ACCOUNT_LEVEL_CALL_CONVERSION_ACTION and
                USE_RESOURCE_LEVEL_CALL_CONVERSION_ACTION.
        """

        UNSPECIFIED = 0
        UNKNOWN = 1
        PHONE_NUMBER = 2
        COUNTRY_CODE = 3
        TRACKED = 4
        CONVERSION_TYPE_ID = 5
        CONVERSION_REPORTING_STATE = 6


__all__ = tuple(sorted(__protobuf__.manifest))
