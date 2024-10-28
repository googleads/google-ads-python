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
    package="google.ads.googleads.v19.enums",
    marshal="google.ads.googleads.v19",
    manifest={
        "ConversionLagBucketEnum",
    },
)


class ConversionLagBucketEnum(proto.Message):
    r"""Container for enum representing the number of days between
    impression and conversion.

    """

    class ConversionLagBucket(proto.Enum):
        r"""Enum representing the number of days between impression and
        conversion.

        Values:
            UNSPECIFIED (0):
                Not specified.
            UNKNOWN (1):
                Used for return value only. Represents value
                unknown in this version.
            LESS_THAN_ONE_DAY (2):
                Conversion lag bucket from 0 to 1 day. 0 day
                is included, 1 day is not.
            ONE_TO_TWO_DAYS (3):
                Conversion lag bucket from 1 to 2 days. 1 day
                is included, 2 days is not.
            TWO_TO_THREE_DAYS (4):
                Conversion lag bucket from 2 to 3 days. 2
                days is included, 3 days is not.
            THREE_TO_FOUR_DAYS (5):
                Conversion lag bucket from 3 to 4 days. 3
                days is included, 4 days is not.
            FOUR_TO_FIVE_DAYS (6):
                Conversion lag bucket from 4 to 5 days. 4
                days is included, 5 days is not.
            FIVE_TO_SIX_DAYS (7):
                Conversion lag bucket from 5 to 6 days. 5
                days is included, 6 days is not.
            SIX_TO_SEVEN_DAYS (8):
                Conversion lag bucket from 6 to 7 days. 6
                days is included, 7 days is not.
            SEVEN_TO_EIGHT_DAYS (9):
                Conversion lag bucket from 7 to 8 days. 7
                days is included, 8 days is not.
            EIGHT_TO_NINE_DAYS (10):
                Conversion lag bucket from 8 to 9 days. 8
                days is included, 9 days is not.
            NINE_TO_TEN_DAYS (11):
                Conversion lag bucket from 9 to 10 days. 9
                days is included, 10 days is not.
            TEN_TO_ELEVEN_DAYS (12):
                Conversion lag bucket from 10 to 11 days. 10
                days is included, 11 days is not.
            ELEVEN_TO_TWELVE_DAYS (13):
                Conversion lag bucket from 11 to 12 days. 11
                days is included, 12 days is not.
            TWELVE_TO_THIRTEEN_DAYS (14):
                Conversion lag bucket from 12 to 13 days. 12
                days is included, 13 days is not.
            THIRTEEN_TO_FOURTEEN_DAYS (15):
                Conversion lag bucket from 13 to 14 days. 13
                days is included, 14 days is not.
            FOURTEEN_TO_TWENTY_ONE_DAYS (16):
                Conversion lag bucket from 14 to 21 days. 14
                days is included, 21 days is not.
            TWENTY_ONE_TO_THIRTY_DAYS (17):
                Conversion lag bucket from 21 to 30 days. 21
                days is included, 30 days is not.
            THIRTY_TO_FORTY_FIVE_DAYS (18):
                Conversion lag bucket from 30 to 45 days. 30
                days is included, 45 days is not.
            FORTY_FIVE_TO_SIXTY_DAYS (19):
                Conversion lag bucket from 45 to 60 days. 45
                days is included, 60 days is not.
            SIXTY_TO_NINETY_DAYS (20):
                Conversion lag bucket from 60 to 90 days. 60
                days is included, 90 days is not.
        """

        UNSPECIFIED = 0
        UNKNOWN = 1
        LESS_THAN_ONE_DAY = 2
        ONE_TO_TWO_DAYS = 3
        TWO_TO_THREE_DAYS = 4
        THREE_TO_FOUR_DAYS = 5
        FOUR_TO_FIVE_DAYS = 6
        FIVE_TO_SIX_DAYS = 7
        SIX_TO_SEVEN_DAYS = 8
        SEVEN_TO_EIGHT_DAYS = 9
        EIGHT_TO_NINE_DAYS = 10
        NINE_TO_TEN_DAYS = 11
        TEN_TO_ELEVEN_DAYS = 12
        ELEVEN_TO_TWELVE_DAYS = 13
        TWELVE_TO_THIRTEEN_DAYS = 14
        THIRTEEN_TO_FOURTEEN_DAYS = 15
        FOURTEEN_TO_TWENTY_ONE_DAYS = 16
        TWENTY_ONE_TO_THIRTY_DAYS = 17
        THIRTY_TO_FORTY_FIVE_DAYS = 18
        FORTY_FIVE_TO_SIXTY_DAYS = 19
        SIXTY_TO_NINETY_DAYS = 20


__all__ = tuple(sorted(__protobuf__.manifest))
