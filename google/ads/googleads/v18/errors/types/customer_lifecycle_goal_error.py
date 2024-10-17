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
    package="google.ads.googleads.v18.errors",
    marshal="google.ads.googleads.v18",
    manifest={"CustomerLifecycleGoalErrorEnum",},
)


class CustomerLifecycleGoalErrorEnum(proto.Message):
    r"""Container for enum describing possible customer lifecycle
    goal errors.

    """

    class CustomerLifecycleGoalError(proto.Enum):
        r"""Enum describing possible customer lifecycle goal errors."""
        UNSPECIFIED = 0
        UNKNOWN = 1
        CUSTOMER_ACQUISITION_VALUE_MISSING = 2
        CUSTOMER_ACQUISITION_INVALID_VALUE = 3
        CUSTOMER_ACQUISITION_INVALID_HIGH_LIFETIME_VALUE = 4
        CUSTOMER_ACQUISITION_VALUE_CANNOT_BE_CLEARED = 5
        CUSTOMER_ACQUISITION_HIGH_LIFETIME_VALUE_CANNOT_BE_CLEARED = 6
        INVALID_EXISTING_USER_LIST = 7
        INVALID_HIGH_LIFETIME_VALUE_USER_LIST = 8


__all__ = tuple(sorted(__protobuf__.manifest))
