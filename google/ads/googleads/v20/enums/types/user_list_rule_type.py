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
        "UserListRuleTypeEnum",
    },
)


class UserListRuleTypeEnum(proto.Message):
    r"""Rule based user list rule type."""

    class UserListRuleType(proto.Enum):
        r"""Enum describing possible user list rule types.

        Values:
            UNSPECIFIED (0):
                Not specified.
            UNKNOWN (1):
                Used for return value only. Represents value
                unknown in this version.
            AND_OF_ORS (2):
                Conjunctive normal form.
            OR_OF_ANDS (3):
                Disjunctive normal form.
        """

        UNSPECIFIED = 0
        UNKNOWN = 1
        AND_OF_ORS = 2
        OR_OF_ANDS = 3


__all__ = tuple(sorted(__protobuf__.manifest))
