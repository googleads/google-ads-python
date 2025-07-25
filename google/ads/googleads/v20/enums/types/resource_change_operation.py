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
        "ResourceChangeOperationEnum",
    },
)


class ResourceChangeOperationEnum(proto.Message):
    r"""Container for enum describing resource change operations
    in the ChangeEvent resource.

    """

    class ResourceChangeOperation(proto.Enum):
        r"""The operation on the changed resource in change_event resource.

        Values:
            UNSPECIFIED (0):
                No value has been specified.
            UNKNOWN (1):
                Used for return value only. Represents an
                unclassified operation unknown in this version.
            CREATE (2):
                The resource was created.
            UPDATE (3):
                The resource was modified.
            REMOVE (4):
                The resource was removed.
        """

        UNSPECIFIED = 0
        UNKNOWN = 1
        CREATE = 2
        UPDATE = 3
        REMOVE = 4


__all__ = tuple(sorted(__protobuf__.manifest))
