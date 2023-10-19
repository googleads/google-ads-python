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
    package="google.ads.googleads.v15.enums",
    marshal="google.ads.googleads.v15",
    manifest={
        "AssetGroupSignalApprovalStatusEnum",
    },
)


class AssetGroupSignalApprovalStatusEnum(proto.Message):
    r"""Container for enum describing possible AssetGroupSignal
    approval statuses. Details see
    https://support.google.com/google-ads/answer/2453978.

    """

    class AssetGroupSignalApprovalStatus(proto.Enum):
        r"""Enumerates AssetGroupSignal approval statuses, which are only
        used for Search Theme Signal.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        APPROVED = 2
        LIMITED = 3
        DISAPPROVED = 4
        UNDER_REVIEW = 5


__all__ = tuple(sorted(__protobuf__.manifest))
