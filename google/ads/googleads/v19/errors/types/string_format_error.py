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
    package="google.ads.googleads.v19.errors",
    marshal="google.ads.googleads.v19",
    manifest={
        "StringFormatErrorEnum",
    },
)


class StringFormatErrorEnum(proto.Message):
    r"""Container for enum describing possible string format errors."""

    class StringFormatError(proto.Enum):
        r"""Enum describing possible string format errors.

        Values:
            UNSPECIFIED (0):
                Enum unspecified.
            UNKNOWN (1):
                The received error code is not known in this
                version.
            ILLEGAL_CHARS (2):
                The input string value contains disallowed
                characters.
            INVALID_FORMAT (3):
                The input string value is invalid for the
                associated field.
        """

        UNSPECIFIED = 0
        UNKNOWN = 1
        ILLEGAL_CHARS = 2
        INVALID_FORMAT = 3


__all__ = tuple(sorted(__protobuf__.manifest))
