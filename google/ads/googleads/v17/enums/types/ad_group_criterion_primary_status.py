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
    package="google.ads.googleads.v17.enums",
    marshal="google.ads.googleads.v17",
    manifest={
        "AdGroupCriterionPrimaryStatusEnum",
    },
)


class AdGroupCriterionPrimaryStatusEnum(proto.Message):
    r"""Container for enum describing possible ad group criterion
    primary status.

    """

    class AdGroupCriterionPrimaryStatus(proto.Enum):
        r"""Enum describing the possible ad group criterion primary
        status. Provides insight into why an ad group criterion is not
        serving or not serving optimally.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        ELIGIBLE = 2
        PAUSED = 3
        REMOVED = 4
        PENDING = 5
        NOT_ELIGIBLE = 6


__all__ = tuple(sorted(__protobuf__.manifest))
