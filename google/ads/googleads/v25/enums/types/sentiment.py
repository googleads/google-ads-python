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
        "SentimentEnum",
    },
)


class SentimentEnum(proto.Message):
    r"""Container for the enum describing sentiment."""

    class Sentiment(proto.Enum):
        r"""Sentiment for a brand - how a brand is viewed according to
        content related to the brand.

        Values:
            UNSPECIFIED (0):
                Not specified.
            UNKNOWN (1):
                The value is unknown in this version.
            SENTIMENT_NEUTRAL (2):
                The sentiment is neutral; often this label is
                attributed to content that is instructional
                (how-to videos).
            SENTIMENT_POSITIVE (3):
                The sentiment is positive.
            SENTIMENT_NEGATIVE (4):
                The sentiment is negative.
        """

        UNSPECIFIED = 0
        UNKNOWN = 1
        SENTIMENT_NEUTRAL = 2
        SENTIMENT_POSITIVE = 3
        SENTIMENT_NEGATIVE = 4


__all__ = tuple(sorted(__protobuf__.manifest))
