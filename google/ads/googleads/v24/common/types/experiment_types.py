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

from google.ads.googleads.v24.enums.types import (
    optimize_assets_experiment_subtype as gage_optimize_assets_experiment_subtype,
)
from google.ads.googleads.v24.enums.types import (
    video_experiment_subtype as gage_video_experiment_subtype,
)


__protobuf__ = proto.module(
    package="google.ads.googleads.v24.common",
    marshal="google.ads.googleads.v24",
    manifest={
        "VideoExperimentInfo",
        "OptimizeAssetsExperimentInfo",
    },
)


class VideoExperimentInfo(proto.Message):
    r"""Configuration for a Video experiment.

    Attributes:
        video_experiment_subtype (google.ads.googleads.v24.enums.types.VideoExperimentSubtypeEnum.VideoExperimentSubtype):
            The subtype of the Video experiment.
    """

    video_experiment_subtype: (
        gage_video_experiment_subtype.VideoExperimentSubtypeEnum.VideoExperimentSubtype
    ) = proto.Field(
        proto.ENUM,
        number=1,
        enum=gage_video_experiment_subtype.VideoExperimentSubtypeEnum.VideoExperimentSubtype,
    )


class OptimizeAssetsExperimentInfo(proto.Message):
    r"""Configuration for an Optimize Assets experiment.

    Attributes:
        optimize_assets_experiment_subtype (google.ads.googleads.v24.enums.types.OptimizeAssetsExperimentSubtypeEnum.OptimizeAssetsExperimentSubtype):
            The subtype of the Optimize Assets
            experiment.
    """

    optimize_assets_experiment_subtype: (
        gage_optimize_assets_experiment_subtype.OptimizeAssetsExperimentSubtypeEnum.OptimizeAssetsExperimentSubtype
    ) = proto.Field(
        proto.ENUM,
        number=1,
        enum=gage_optimize_assets_experiment_subtype.OptimizeAssetsExperimentSubtypeEnum.OptimizeAssetsExperimentSubtype,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
