# -*- coding: utf-8 -*-
# Copyright 2026 Google LLC
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
    package="google.ads.googleads.v25.enums",
    marshal="google.ads.googleads.v25",
    manifest={
        "BenchmarksCustomerPercentileTierEnum",
    },
)


class BenchmarksCustomerPercentileTierEnum(proto.Message):
    r"""Container for enum describing customer percentile tiers for
    the Benchmarks Service.

    """

    class BenchmarksCustomerPercentileTier(proto.Enum):
        r"""Customer percentile tiers for the Benchmarks Service.

        Values:
            UNSPECIFIED (0):
                Not specified.
            UNKNOWN (1):
                The value is unknown in this version.
            DEVELOPING (2):
                Developing: The customer ranks below the 10th percentile
                among advertisers scoped by the analysis. Range: [0%, 10%).
            ENTRY_LEVEL (3):
                Entry level: The customer ranks in the 10th to 25th
                percentile among advertisers scoped by the analysis. Range:
                [10%, 25%).
            EMERGING_PLAYER (4):
                Emerging Player: The customer ranks in the 25th to 50th
                percentile among advertisers scoped by the analysis. Range:
                [25%, 50%).
            COMPETITOR (5):
                Competitor: The customer ranks in the 50th to 75th
                percentile among advertisers scoped by the analysis. Range:
                [50%, 75%).
            STRONG_COMPETITOR (6):
                Strong competitor: The customer ranks in the 75th to 90th
                percentile among advertisers scoped by the analysis. Range:
                [75%, 90%).
            MARKET_LEADER (7):
                Market leader: The customer ranks at or above the 90th
                percentile among advertisers scoped by the analysis. Range:
                [90%, 100%].
        """

        UNSPECIFIED = 0
        UNKNOWN = 1
        DEVELOPING = 2
        ENTRY_LEVEL = 3
        EMERGING_PLAYER = 4
        COMPETITOR = 5
        STRONG_COMPETITOR = 6
        MARKET_LEADER = 7


__all__ = tuple(sorted(__protobuf__.manifest))
