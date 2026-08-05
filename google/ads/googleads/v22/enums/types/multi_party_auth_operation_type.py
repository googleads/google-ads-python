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
    package="google.ads.googleads.v22.enums",
    marshal="google.ads.googleads.v22",
    manifest={
        "MultiPartyAuthOperationTypeEnum",
    },
)


class MultiPartyAuthOperationTypeEnum(proto.Message):
    r"""The operation type of a Multi-Party Authorization review."""

    class MultiPartyAuthOperationType(proto.Enum):
        r"""The possible operation types of a Multi-Party Authorization
        review.

        Values:
            UNSPECIFIED (0):
                Not specified.
            UNKNOWN (1):
                Value unknown in this version.
            CREATE (2):
                The operation is for creating a new resource.
            UPDATE (3):
                The operation is for updating an existing
                resource.
            REMOVE (4):
                The operation is for removing a resource.
        """

        UNSPECIFIED = 0
        UNKNOWN = 1
        CREATE = 2
        UPDATE = 3
        REMOVE = 4


__all__ = tuple(sorted(__protobuf__.manifest))
