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
    package="google.ads.googleads.v19.enums",
    marshal="google.ads.googleads.v19",
    manifest={
        "BusinessMessageCallToActionTypeEnum",
    },
)


class BusinessMessageCallToActionTypeEnum(proto.Message):
    r"""Describes the type of call-to-action phrases in a business
    message.

    """

    class BusinessMessageCallToActionType(proto.Enum):
        r"""Enum describing the type of call-to-action phrases in a
        business message.
        """

        UNSPECIFIED = 0
        UNKNOWN = 1
        APPLY_NOW = 2
        BOOK_NOW = 3
        CONTACT_US = 4
        GET_INFO = 5
        GET_OFFER = 6
        GET_QUOTE = 7
        GET_STARTED = 8
        LEARN_MORE = 9


__all__ = tuple(sorted(__protobuf__.manifest))
