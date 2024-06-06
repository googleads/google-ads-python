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
    package="google.ads.googleads.v17.errors",
    marshal="google.ads.googleads.v17",
    manifest={
        "UserListCustomerTypeErrorEnum",
    },
)


class UserListCustomerTypeErrorEnum(proto.Message):
    r"""Container for enum describing possible user list customer
    type errors.

    """

    class UserListCustomerTypeError(proto.Enum):
        r"""Enum describing possible user list customer type errors."""
        UNSPECIFIED = 0
        UNKNOWN = 1
        CONFLICTING_CUSTOMER_TYPES = 2
        NO_ACCESS_TO_USER_LIST = 3
        USERLIST_NOT_ELIGIBLE = 4
        CONVERSION_TRACKING_NOT_ENABLED_OR_NOT_MCC_MANAGER_ACCOUNT = 5
        TOO_MANY_USER_LISTS_FOR_THE_CUSTOMER_TYPE = 6


__all__ = tuple(sorted(__protobuf__.manifest))
