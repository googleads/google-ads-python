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
        "FeedItemValidationStatusEnum",
    },
)


class FeedItemValidationStatusEnum(proto.Message):
    r"""Container for enum describing possible validation statuses of
    a feed item.

    """

    class FeedItemValidationStatus(proto.Enum):
        r"""The possible validation statuses of a feed item.

        Values:
            UNSPECIFIED (0):
                No value has been specified.
            UNKNOWN (1):
                Used for return value only. Represents value
                unknown in this version.
            PENDING (2):
                Validation pending.
            INVALID (3):
                An error was found.
            VALID (4):
                Feed item is semantically well-formed.
        """

        UNSPECIFIED = 0
        UNKNOWN = 1
        PENDING = 2
        INVALID = 3
        VALID = 4


__all__ = tuple(sorted(__protobuf__.manifest))
