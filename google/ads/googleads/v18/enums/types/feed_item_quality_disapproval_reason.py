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
        "FeedItemQualityDisapprovalReasonEnum",
    },
)


class FeedItemQualityDisapprovalReasonEnum(proto.Message):
    r"""Container for enum describing possible quality evaluation
    disapproval reasons of a feed item.

    """

    class FeedItemQualityDisapprovalReason(proto.Enum):
        r"""The possible quality evaluation disapproval reasons of a feed
        item.

        Values:
            UNSPECIFIED (0):
                No value has been specified.
            UNKNOWN (1):
                Used for return value only. Represents value
                unknown in this version.
            PRICE_TABLE_REPETITIVE_HEADERS (2):
                Price contains repetitive headers.
            PRICE_TABLE_REPETITIVE_DESCRIPTION (3):
                Price contains repetitive description.
            PRICE_TABLE_INCONSISTENT_ROWS (4):
                Price contains inconsistent items.
            PRICE_DESCRIPTION_HAS_PRICE_QUALIFIERS (5):
                Price contains qualifiers in description.
            PRICE_UNSUPPORTED_LANGUAGE (6):
                Price contains an unsupported language.
            PRICE_TABLE_ROW_HEADER_TABLE_TYPE_MISMATCH (7):
                Price item header is not relevant to the
                price type.
            PRICE_TABLE_ROW_HEADER_HAS_PROMOTIONAL_TEXT (8):
                Price item header has promotional text.
            PRICE_TABLE_ROW_DESCRIPTION_NOT_RELEVANT (9):
                Price item description is not relevant to the
                item header.
            PRICE_TABLE_ROW_DESCRIPTION_HAS_PROMOTIONAL_TEXT (10):
                Price item description contains promotional
                text.
            PRICE_TABLE_ROW_HEADER_DESCRIPTION_REPETITIVE (11):
                Price item header and description are
                repetitive.
            PRICE_TABLE_ROW_UNRATEABLE (12):
                Price item is in a foreign language,
                nonsense, or can't be rated.
            PRICE_TABLE_ROW_PRICE_INVALID (13):
                Price item price is invalid or inaccurate.
            PRICE_TABLE_ROW_URL_INVALID (14):
                Price item URL is invalid or irrelevant.
            PRICE_HEADER_OR_DESCRIPTION_HAS_PRICE (15):
                Price item header or description has price.
            STRUCTURED_SNIPPETS_HEADER_POLICY_VIOLATED (16):
                Structured snippet values do not match the
                header.
            STRUCTURED_SNIPPETS_REPEATED_VALUES (17):
                Structured snippet values are repeated.
            STRUCTURED_SNIPPETS_EDITORIAL_GUIDELINES (18):
                Structured snippet values violate editorial
                guidelines like punctuation.
            STRUCTURED_SNIPPETS_HAS_PROMOTIONAL_TEXT (19):
                Structured snippet contain promotional text.
        """

        UNSPECIFIED = 0
        UNKNOWN = 1
        PRICE_TABLE_REPETITIVE_HEADERS = 2
        PRICE_TABLE_REPETITIVE_DESCRIPTION = 3
        PRICE_TABLE_INCONSISTENT_ROWS = 4
        PRICE_DESCRIPTION_HAS_PRICE_QUALIFIERS = 5
        PRICE_UNSUPPORTED_LANGUAGE = 6
        PRICE_TABLE_ROW_HEADER_TABLE_TYPE_MISMATCH = 7
        PRICE_TABLE_ROW_HEADER_HAS_PROMOTIONAL_TEXT = 8
        PRICE_TABLE_ROW_DESCRIPTION_NOT_RELEVANT = 9
        PRICE_TABLE_ROW_DESCRIPTION_HAS_PROMOTIONAL_TEXT = 10
        PRICE_TABLE_ROW_HEADER_DESCRIPTION_REPETITIVE = 11
        PRICE_TABLE_ROW_UNRATEABLE = 12
        PRICE_TABLE_ROW_PRICE_INVALID = 13
        PRICE_TABLE_ROW_URL_INVALID = 14
        PRICE_HEADER_OR_DESCRIPTION_HAS_PRICE = 15
        STRUCTURED_SNIPPETS_HEADER_POLICY_VIOLATED = 16
        STRUCTURED_SNIPPETS_REPEATED_VALUES = 17
        STRUCTURED_SNIPPETS_EDITORIAL_GUIDELINES = 18
        STRUCTURED_SNIPPETS_HAS_PROMOTIONAL_TEXT = 19


__all__ = tuple(sorted(__protobuf__.manifest))
