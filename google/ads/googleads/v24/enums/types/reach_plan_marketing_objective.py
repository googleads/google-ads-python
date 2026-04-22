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
        "ReachPlanMarketingObjectiveEnum",
    },
)


class ReachPlanMarketingObjectiveEnum(proto.Message):
    r"""Container for enum describing marketing objectives available
    for reach planning.

    """

    class ReachPlanMarketingObjective(proto.Enum):
        r"""Marketing objectives available for reach planning.

        Values:
            UNSPECIFIED (0):
                Not specified.
            UNKNOWN (1):
                The value is unknown in this version.
            AWARENESS (2):
                The objective is to maximize brand visibility
                and reach as many relevant people as possible,
                making potential customers aware of the brand or
                product.
            CONSIDERATION (3):
                The objective is to encourage potential
                customers to learn more about the brand or
                products and consider them for a future
                purchase.
            ACTION (4):
                The objective is to persuade potential
                customers to take a specific, valuable action,
                such as making a purchase, signing up for a
                newsletter, or generating a lead.
        """

        UNSPECIFIED = 0
        UNKNOWN = 1
        AWARENESS = 2
        CONSIDERATION = 3
        ACTION = 4


__all__ = tuple(sorted(__protobuf__.manifest))
