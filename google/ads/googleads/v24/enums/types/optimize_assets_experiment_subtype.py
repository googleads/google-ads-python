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
        "OptimizeAssetsExperimentSubtypeEnum",
    },
)


class OptimizeAssetsExperimentSubtypeEnum(proto.Message):
    r"""Indicates the subtype of an optimize assets experiment."""

    class OptimizeAssetsExperimentSubtype(proto.Enum):
        r"""The enum describing optimize assets subtype.

        Values:
            UNSPECIFIED (0):
                Not specified.
            UNKNOWN (1):
                The value is unknown in this version.
            ADD_ASSETS_TO_ASSETLESS_RETAIL (2):
                The experiment is testing adding assets to
                assetless retail PMax experiment.
            ADD_VIDEO_ASSETS_TO_VIDEOLESS (3):
                The experiment is testing adding video assets
                to videoless PMax experiment.
            COMPARE_ASSETS (4):
                The experiment is testing comparing two
                different sets of assets in a PMax experiment.
        """

        UNSPECIFIED = 0
        UNKNOWN = 1
        ADD_ASSETS_TO_ASSETLESS_RETAIL = 2
        ADD_VIDEO_ASSETS_TO_VIDEOLESS = 3
        COMPARE_ASSETS = 4


__all__ = tuple(sorted(__protobuf__.manifest))
