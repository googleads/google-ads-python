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
        "ListingGroupFilterCustomAttributeIndexEnum",
    },
)


class ListingGroupFilterCustomAttributeIndexEnum(proto.Message):
    r"""Container for enum describing the indexes of custom attribute
    used in ListingGroupFilterDimension.

    """

    class ListingGroupFilterCustomAttributeIndex(proto.Enum):
        r"""The index of customer attributes.

        Values:
            UNSPECIFIED (0):
                Not specified.
            UNKNOWN (1):
                Used for return value only. Represents value
                unknown in this version.
            INDEX0 (2):
                First listing group filter custom attribute.
            INDEX1 (3):
                Second listing group filter custom attribute.
            INDEX2 (4):
                Third listing group filter custom attribute.
            INDEX3 (5):
                Fourth listing group filter custom attribute.
            INDEX4 (6):
                Fifth listing group filter custom attribute.
        """

        UNSPECIFIED = 0
        UNKNOWN = 1
        INDEX0 = 2
        INDEX1 = 3
        INDEX2 = 4
        INDEX3 = 5
        INDEX4 = 6


__all__ = tuple(sorted(__protobuf__.manifest))
