# -*- coding: utf-8 -*-
# Copyright 2026 Google LLC
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
    package="google.ads.googleads.v25.enums",
    marshal="google.ads.googleads.v25",
    manifest={
        "GlsPhoneNumberTypeEnum",
    },
)


class GlsPhoneNumberTypeEnum(proto.Message):
    r"""Container for enum describing possible types of GLS phone
    numbers.

    """

    class GlsPhoneNumberType(proto.Enum):
        r"""Possible types of GLS phone numbers.

        Values:
            UNSPECIFIED (0):
                Not specified.
            UNKNOWN (1):
                Used for return value only. Represents value
                unknown in this version.
            DESTINATION_PHONE_NUMBER_FOR_ADS (2):
                Provider-provided destination number to use
                for calls originating from a GLS ad unit. This
                is the default.
            DESTINATION_PHONE_NUMBER_FOR_SMS_ONLY (3):
                Destination phone number that supports SMS.
            DESTINATION_PHONE_NUMBER_FOR_WHATSAPP_ONLY (4):
                Destination phone number for a provider's
                WhatsApp account.
        """

        UNSPECIFIED = 0
        UNKNOWN = 1
        DESTINATION_PHONE_NUMBER_FOR_ADS = 2
        DESTINATION_PHONE_NUMBER_FOR_SMS_ONLY = 3
        DESTINATION_PHONE_NUMBER_FOR_WHATSAPP_ONLY = 4


__all__ = tuple(sorted(__protobuf__.manifest))
