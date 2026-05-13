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
        "VideoExperimentSubtypeEnum",
    },
)


class VideoExperimentSubtypeEnum(proto.Message):
    r"""Describes the video experiment subtype to enforce appropriate
    validation rules and reporting structures. While ad serving is
    governed by the experiment type, this field determines which
    mutations are permitted (for example, restricting asset removal
    in uplift experiments) and how the experiment is categorized in
    reports.

    """

    class VideoExperimentSubtype(proto.Enum):
        r"""The enum describing video experiment subtype.

        Values:
            UNSPECIFIED (0):
                Not specified.
            UNKNOWN (1):
                The value is unknown in this version.
            DEMAND_GEN_ASSET (2):
                The experiment is testing a Demand Gen asset
                experiment. User can add or delete assets from
                the control campaigns.
            ASSET (3):
                The experiment is testing ads with different
                video assets in the experimental campaign versus
                the control campaign. It applies to Video
                Campaigns where users can add or delete assets
                from control campaigns.
            ASSET_UPLIFT (4):
                The experiment is testing video asset uplift
                (the performance impact of different video
                assets in a campaign). It applies to Video
                Campaigns where users can only add assets to
                control campaigns.
        """

        UNSPECIFIED = 0
        UNKNOWN = 1
        DEMAND_GEN_ASSET = 2
        ASSET = 3
        ASSET_UPLIFT = 4


__all__ = tuple(sorted(__protobuf__.manifest))
