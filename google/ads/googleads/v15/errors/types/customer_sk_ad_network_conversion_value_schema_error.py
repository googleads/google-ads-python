# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
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
    package="google.ads.googleads.v15.errors",
    marshal="google.ads.googleads.v15",
    manifest={
        "CustomerSkAdNetworkConversionValueSchemaErrorEnum",
    },
)


class CustomerSkAdNetworkConversionValueSchemaErrorEnum(proto.Message):
    r"""Container for enum describing possible
    CustomerSkAdNetworkConversionValueSchema errors.

    """

    class CustomerSkAdNetworkConversionValueSchemaError(proto.Enum):
        r"""Enum describing possible
        CustomerSkAdNetworkConversionValueSchema errors.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        INVALID_LINK_ID = 2
        INVALID_APP_ID = 3
        INVALID_SCHEMA = 4
        LINK_CODE_NOT_FOUND = 5


__all__ = tuple(sorted(__protobuf__.manifest))
