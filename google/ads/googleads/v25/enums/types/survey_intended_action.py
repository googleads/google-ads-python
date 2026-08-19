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
        "SurveyIntendedActionEnum",
    },
)


class SurveyIntendedActionEnum(proto.Message):
    r"""Container for enum"""

    class SurveyIntendedAction(proto.Enum):
        r"""The enum

        Values:
            UNSPECIFIED (0):
                Not specified.
            UNKNOWN (1):
                Unknown value.
            APPLY_FOR (2):
                Apply For
            APPLY_TO_WORK_FOR (3):
                Apply To Work For
            ATTEND (4):
                Attend
            BOOK (5):
                Book
            BOOK_WITH (6):
                Book With
            BUY (7):
                Buy
            BUY_CONTENT_FROM (8):
                Buy Content From
            BUY_TICKETS_FOR (9):
                Buy Tickets For
            CARE_ABOUT (10):
                Care About
            CHOOSE (11):
                Choose
            DONATE_TO (12):
                Donate To
            DOWNLOAD (13):
                Download
            DOWNLOAD_FROM (14):
                Download From
            EAT (15):
                Eat
            EAT_AT (16):
                Eat At
            HAVE_UNFAVORABLE_OPINION_OF (17):
                Have Unfavorable Opinion Of
            JOIN (18):
                Join
            LEARN (19):
                Learn
            LISTEN_TO (20):
                Listen To
            NONE (21):
                None
            ORDER_FROM (22):
                Order From
            PARTICIPATE_IN (23):
                Participate In
            PLAY (24):
                Play
            PLAY_AT (25):
                Play At
            PLAY_ON (26):
                Play On
            RENT (27):
                Rent
            SEE (28):
                See
            SEE_IN_THEATERS (29):
                See In Theaters
            SHOP (30):
                Shop
            SIGN_UP_FOR (31):
                Sign Up For
            SUBSCRIBE_TO (32):
                Subscribe To
            TAKE_ACTION_ON (33):
                Take Action On
            USE (34):
                Use
            VISIT (35):
                Visit
            VOTE_FOR (36):
                Vote For
            WATCH (37):
                Watch
            WATCH_IN_THEATERS (38):
                Watch In Theaters
        """

        UNSPECIFIED = 0
        UNKNOWN = 1
        APPLY_FOR = 2
        APPLY_TO_WORK_FOR = 3
        ATTEND = 4
        BOOK = 5
        BOOK_WITH = 6
        BUY = 7
        BUY_CONTENT_FROM = 8
        BUY_TICKETS_FOR = 9
        CARE_ABOUT = 10
        CHOOSE = 11
        DONATE_TO = 12
        DOWNLOAD = 13
        DOWNLOAD_FROM = 14
        EAT = 15
        EAT_AT = 16
        HAVE_UNFAVORABLE_OPINION_OF = 17
        JOIN = 18
        LEARN = 19
        LISTEN_TO = 20
        NONE = 21
        ORDER_FROM = 22
        PARTICIPATE_IN = 23
        PLAY = 24
        PLAY_AT = 25
        PLAY_ON = 26
        RENT = 27
        SEE = 28
        SEE_IN_THEATERS = 29
        SHOP = 30
        SIGN_UP_FOR = 31
        SUBSCRIBE_TO = 32
        TAKE_ACTION_ON = 33
        USE = 34
        VISIT = 35
        VOTE_FOR = 36
        WATCH = 37
        WATCH_IN_THEATERS = 38


__all__ = tuple(sorted(__protobuf__.manifest))
