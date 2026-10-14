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
    package="google.ads.googleads.v26.enums",
    marshal="google.ads.googleads.v26",
    manifest={
        "SearchLiftMatchingInfoSourceEnum",
    },
)


class SearchLiftMatchingInfoSourceEnum(proto.Message):
    r"""Container for enum describing matching info source for Search
    Lift.

    """

    class SearchLiftMatchingInfoSource(proto.Enum):
        r"""Enum describing matching info source for Search Lift.

        Values:
            UNSPECIFIED (0):
                Not specified.
            UNKNOWN (1):
                Used for return value only. Represents value
                unknown in this version.
            SURVEY_PREFERRED_OPTION (2):
                Matching info is based on the survey lift
                preferred option.
            SURVEY_COMPETITOR_OPTION (3):
                Matching info is based on the survey lift
                competitor option.
            USER (4):
                Matching info is based on user input.
            SINGLE_KEYWORD (5):
                Specifies a single keyword from a set of
                keywords.
            CONTROL (6):
                Random keywords used to evaluate measure, for
                which we expect no lift.
        """

        UNSPECIFIED = 0
        UNKNOWN = 1
        SURVEY_PREFERRED_OPTION = 2
        SURVEY_COMPETITOR_OPTION = 3
        USER = 4
        SINGLE_KEYWORD = 5
        CONTROL = 6


__all__ = tuple(sorted(__protobuf__.manifest))
