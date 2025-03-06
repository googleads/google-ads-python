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
        "AppBiddingGoalEnum",
    },
)


class AppBiddingGoalEnum(proto.Message):
    r"""Container for enum describing an app bidding goal for raise
    Target CPA recommendation.

    """

    class AppBiddingGoal(proto.Enum):
        r"""Represents the goal towards which the bidding strategy, of an
        app campaign, should optimize for.

        Values:
            UNSPECIFIED (0):
                Not specified.
            UNKNOWN (1):
                Represents value unknown in this version of
                the API.
            OPTIMIZE_FOR_INSTALL_CONVERSION_VOLUME (2):
                The bidding strategy of the app campaign
                should aim to maximize installation of the app.
            OPTIMIZE_FOR_IN_APP_CONVERSION_VOLUME (3):
                The bidding strategy of the app campaign
                should aim to maximize the selected in-app
                conversions' volume.
            OPTIMIZE_FOR_TOTAL_CONVERSION_VALUE (4):
                The bidding strategy of the app campaign
                should aim to maximize all conversions' value,
                that is, install and selected in-app
                conversions.
            OPTIMIZE_FOR_TARGET_IN_APP_CONVERSION (5):
                The bidding strategy of the app campaign
                should aim to maximize just the selected in-app
                conversion's volume, while achieving or
                exceeding target cost per in-app conversion.
            OPTIMIZE_FOR_RETURN_ON_ADVERTISING_SPEND (6):
                The bidding strategy of the app campaign
                should aim to maximize all conversions' value,
                that is, install and selected in-app conversions
                while achieving or exceeding target return on
                advertising spend.
            OPTIMIZE_FOR_INSTALL_CONVERSION_VOLUME_WITHOUT_TARGET_CPI (7):
                This bidding strategy of the app campaign
                should aim to maximize installation of the app
                without advertiser-provided target
                cost-per-install.
            OPTIMIZE_FOR_PRE_REGISTRATION_CONVERSION_VOLUME (8):
                This bidding strategy of the app campaign
                should aim to maximize pre-registration of the
                app.
        """

        UNSPECIFIED = 0
        UNKNOWN = 1
        OPTIMIZE_FOR_INSTALL_CONVERSION_VOLUME = 2
        OPTIMIZE_FOR_IN_APP_CONVERSION_VOLUME = 3
        OPTIMIZE_FOR_TOTAL_CONVERSION_VALUE = 4
        OPTIMIZE_FOR_TARGET_IN_APP_CONVERSION = 5
        OPTIMIZE_FOR_RETURN_ON_ADVERTISING_SPEND = 6
        OPTIMIZE_FOR_INSTALL_CONVERSION_VOLUME_WITHOUT_TARGET_CPI = 7
        OPTIMIZE_FOR_PRE_REGISTRATION_CONVERSION_VOLUME = 8


__all__ = tuple(sorted(__protobuf__.manifest))
