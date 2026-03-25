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

from typing import MutableSequence

import proto  # type: ignore

from google.ads.googleads.v23.common.types import asset_usage


__protobuf__ = proto.module(
    package="google.ads.googleads.v23.resources",
    marshal="google.ads.googleads.v23",
    manifest={
        "AppTopCombinationView",
        "AdGroupCreativeAssetCombinationData",
    },
)


class AppTopCombinationView(proto.Message):
    r"""A view resource in the App Top Combination Report.

    Attributes:
        resource_name (str):
            Output only. The resource name of the app top combination
            view. App Top Combination view resource names have the form:
            ``customers/{customer_id}/appTopCombinationViews/{ad_group_id}~{ad_id}~{asset_combination_category}``
        ad_group_top_combinations (MutableSequence[google.ads.googleads.v23.resources.types.AdGroupCreativeAssetCombinationData]):
            Output only. The top combinations of assets
            that served together.
    """

    resource_name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    ad_group_top_combinations: MutableSequence[
        "AdGroupCreativeAssetCombinationData"
    ] = proto.RepeatedField(
        proto.MESSAGE,
        number=2,
        message="AdGroupCreativeAssetCombinationData",
    )


class AdGroupCreativeAssetCombinationData(proto.Message):
    r"""Ad group asset combination data

    Attributes:
        asset_combination_served_assets (MutableSequence[google.ads.googleads.v23.common.types.AssetUsage]):
            Output only. Served assets.
    """

    asset_combination_served_assets: MutableSequence[asset_usage.AssetUsage] = (
        proto.RepeatedField(
            proto.MESSAGE,
            number=1,
            message=asset_usage.AssetUsage,
        )
    )


__all__ = tuple(sorted(__protobuf__.manifest))
