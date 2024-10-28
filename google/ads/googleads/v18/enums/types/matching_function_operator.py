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
        "MatchingFunctionOperatorEnum",
    },
)


class MatchingFunctionOperatorEnum(proto.Message):
    r"""Container for enum describing matching function operator."""

    class MatchingFunctionOperator(proto.Enum):
        r"""Possible operators in a matching function.

        Values:
            UNSPECIFIED (0):
                Not specified.
            UNKNOWN (1):
                Used for return value only. Represents value
                unknown in this version.
            IN (2):
                The IN operator.
            IDENTITY (3):
                The IDENTITY operator.
            EQUALS (4):
                The EQUALS operator
            AND (5):
                Operator that takes two or more operands that are of type
                FunctionOperand and checks that all the operands evaluate to
                true. For functions related to ad formats, all the operands
                must be in left_operands.
            CONTAINS_ANY (6):
                Operator that returns true if the elements in left_operands
                contain any of the elements in right_operands. Otherwise,
                return false. The right_operands must contain at least 1 and
                no more than 3 ConstantOperands.
        """

        UNSPECIFIED = 0
        UNKNOWN = 1
        IN = 2
        IDENTITY = 3
        EQUALS = 4
        AND = 5
        CONTAINS_ANY = 6


__all__ = tuple(sorted(__protobuf__.manifest))
