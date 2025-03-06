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
        "StructuredSnippetPlaceholderFieldEnum",
    },
)


class StructuredSnippetPlaceholderFieldEnum(proto.Message):
    r"""Values for Structured Snippet placeholder fields."""

    class StructuredSnippetPlaceholderField(proto.Enum):
        r"""Possible values for Structured Snippet placeholder fields.

        Values:
            UNSPECIFIED (0):
                Not specified.
            UNKNOWN (1):
                Used for return value only. Represents value
                unknown in this version.
            HEADER (2):
                Data Type: STRING. The category of snippet of
                your products/services. Must match exactly one
                of the predefined structured snippets headers.
                For a list, visit
                https://developers.google.com/google-ads/api/reference/data/structured-snippet-headers
            SNIPPETS (3):
                Data Type: STRING_LIST. Text values that describe your
                products/services. All text must be family safe. Special or
                non-ASCII characters are not permitted. A snippet can be at
                most 25 characters.
        """

        UNSPECIFIED = 0
        UNKNOWN = 1
        HEADER = 2
        SNIPPETS = 3


__all__ = tuple(sorted(__protobuf__.manifest))
