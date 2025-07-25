# -*- coding: utf-8 -*-
# Copyright 2025 Google LLC
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
    package="google.ads.googleads.v20.enums",
    marshal="google.ads.googleads.v20",
    manifest={
        "AssetOfflineEvaluationErrorReasonsEnum",
    },
)


class AssetOfflineEvaluationErrorReasonsEnum(proto.Message):
    r"""Provides the quality evaluation disapproval reason of an
    asset.

    """

    class AssetOfflineEvaluationErrorReasons(proto.Enum):
        r"""Enum describing the quality evaluation disapproval reason of
        an asset.

        Values:
            UNSPECIFIED (0):
                Not specified.
            UNKNOWN (1):
                Used for return value only. Represents value
                unknown in this version.
            PRICE_ASSET_DESCRIPTION_REPEATS_ROW_HEADER (2):
                One or more descriptions repeats its
                corresponding row header.
            PRICE_ASSET_REPETITIVE_HEADERS (3):
                Price asset contains repetitive headers.
            PRICE_ASSET_HEADER_INCOMPATIBLE_WITH_PRICE_TYPE (4):
                Price item header is not relevant to the
                price type.
            PRICE_ASSET_DESCRIPTION_INCOMPATIBLE_WITH_ITEM_HEADER (5):
                Price item description is not relevant to the
                item header.
            PRICE_ASSET_DESCRIPTION_HAS_PRICE_QUALIFIER (6):
                Price asset has a price qualifier in a
                description.
            PRICE_ASSET_UNSUPPORTED_LANGUAGE (7):
                Unsupported language for price assets
            PRICE_ASSET_OTHER_ERROR (8):
                Human raters identified an issue with the
                price asset that isn't captured by other error
                reasons. The primary purpose of this value is to
                represent legacy FeedItem disapprovals that are
                no longer produced.
        """

        UNSPECIFIED = 0
        UNKNOWN = 1
        PRICE_ASSET_DESCRIPTION_REPEATS_ROW_HEADER = 2
        PRICE_ASSET_REPETITIVE_HEADERS = 3
        PRICE_ASSET_HEADER_INCOMPATIBLE_WITH_PRICE_TYPE = 4
        PRICE_ASSET_DESCRIPTION_INCOMPATIBLE_WITH_ITEM_HEADER = 5
        PRICE_ASSET_DESCRIPTION_HAS_PRICE_QUALIFIER = 6
        PRICE_ASSET_UNSUPPORTED_LANGUAGE = 7
        PRICE_ASSET_OTHER_ERROR = 8


__all__ = tuple(sorted(__protobuf__.manifest))
