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
    package="google.ads.googleads.v19.errors",
    marshal="google.ads.googleads.v19",
    manifest={
        "NewResourceCreationErrorEnum",
    },
)


class NewResourceCreationErrorEnum(proto.Message):
    r"""Container for enum describing possible new resource creation
    errors.

    """

    class NewResourceCreationError(proto.Enum):
        r"""Enum describing possible new resource creation errors."""

        UNSPECIFIED = 0
        UNKNOWN = 1
        CANNOT_SET_ID_FOR_CREATE = 2
        DUPLICATE_TEMP_IDS = 3
        TEMP_ID_RESOURCE_HAD_ERRORS = 4


__all__ = tuple(sorted(__protobuf__.manifest))
