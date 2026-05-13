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
    package="google.ads.googleads.v24.enums",
    marshal="google.ads.googleads.v24",
    manifest={
        "ExperimentAssetDetailOperationEnum",
    },
)


class ExperimentAssetDetailOperationEnum(proto.Message):
    r"""Container for enum describing the type of experiment asset
    detail operation.

    """

    class ExperimentAssetDetailOperation(proto.Enum):
        r"""The type of the experiment asset detail operation.

        Values:
            UNSPECIFIED (0):
                Not specified.
            UNKNOWN (1):
                The value is unknown in this version.
            ADD (2):
                Asset is attached to the ad.
            REMOVE (3):
                Asset is removed from the ad.
        """

        UNSPECIFIED = 0
        UNKNOWN = 1
        ADD = 2
        REMOVE = 3


__all__ = tuple(sorted(__protobuf__.manifest))
