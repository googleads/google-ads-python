# -*- coding: utf-8 -*-
# Copyright 2020 Google LLC
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
import proto  # type: ignore


__protobuf__ = proto.module(
    package="google.ads.googleads.v7.enums",
    marshal="google.ads.googleads.v7",
    manifest={"CampaignExperimentStatusEnum",},
)


class CampaignExperimentStatusEnum(proto.Message):
    r"""Container for enum describing possible statuses of a campaign
    experiment.
        """

    class CampaignExperimentStatus(proto.Enum):
        r"""Possible statuses of a campaign experiment."""
        UNSPECIFIED = 0
        UNKNOWN = 1
        INITIALIZING = 2
        INITIALIZATION_FAILED = 8
        ENABLED = 3
        GRADUATED = 4
        REMOVED = 5
        PROMOTING = 6
        PROMOTION_FAILED = 9
        PROMOTED = 7
        ENDED_MANUALLY = 10


__all__ = tuple(sorted(__protobuf__.manifest))
