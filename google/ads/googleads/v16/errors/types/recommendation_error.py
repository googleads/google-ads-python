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
    package="google.ads.googleads.v16.errors",
    marshal="google.ads.googleads.v16",
    manifest={
        "RecommendationErrorEnum",
    },
)


class RecommendationErrorEnum(proto.Message):
    r"""Container for enum describing possible errors from applying a
    recommendation.

    """

    class RecommendationError(proto.Enum):
        r"""Enum describing possible errors from applying a
        recommendation.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        BUDGET_AMOUNT_TOO_SMALL = 2
        BUDGET_AMOUNT_TOO_LARGE = 3
        INVALID_BUDGET_AMOUNT = 4
        POLICY_ERROR = 5
        INVALID_BID_AMOUNT = 6
        ADGROUP_KEYWORD_LIMIT = 7
        RECOMMENDATION_ALREADY_APPLIED = 8
        RECOMMENDATION_INVALIDATED = 9
        TOO_MANY_OPERATIONS = 10
        NO_OPERATIONS = 11
        DIFFERENT_TYPES_NOT_SUPPORTED = 12
        DUPLICATE_RESOURCE_NAME = 13
        RECOMMENDATION_ALREADY_DISMISSED = 14
        INVALID_APPLY_REQUEST = 15
        RECOMMENDATION_TYPE_APPLY_NOT_SUPPORTED = 17
        INVALID_MULTIPLIER = 18
        ADVERTISING_CHANNEL_TYPE_GENERATE_NOT_SUPPORTED = 19
        RECOMMENDATION_TYPE_GENERATE_NOT_SUPPORTED = 20
        RECOMMENDATION_TYPES_CANNOT_BE_EMPTY = 21


__all__ = tuple(sorted(__protobuf__.manifest))
