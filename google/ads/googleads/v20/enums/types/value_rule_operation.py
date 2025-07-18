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
        "ValueRuleOperationEnum",
    },
)


class ValueRuleOperationEnum(proto.Message):
    r"""Container for enum describing possible operations for value
    rules which are executed when rules are triggered.

    """

    class ValueRuleOperation(proto.Enum):
        r"""Possible operations of the action of a conversion value rule.

        Values:
            UNSPECIFIED (0):
                Not specified.
            UNKNOWN (1):
                Used for return value only. Represents value
                unknown in this version.
            ADD (2):
                Add provided value to conversion value.
            MULTIPLY (3):
                Multiply conversion value by provided value.
            SET (4):
                Set conversion value to provided value.
        """

        UNSPECIFIED = 0
        UNKNOWN = 1
        ADD = 2
        MULTIPLY = 3
        SET = 4


__all__ = tuple(sorted(__protobuf__.manifest))
