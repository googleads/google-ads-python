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

from google.ads.googleads.v19.enums.types import (
    served_asset_field_type as gage_served_asset_field_type,
)


__protobuf__ = proto.module(
    package="google.ads.googleads.v19.common",
    marshal="google.ads.googleads.v19",
    manifest={
        "AssetUsage",
    },
)


class AssetUsage(proto.Message):
    r"""Contains the usage information of the asset.

    Attributes:
        asset (str):
            Resource name of the asset.
        served_asset_field_type (google.ads.googleads.v19.enums.types.ServedAssetFieldTypeEnum.ServedAssetFieldType):
            The served field type of the asset.
    """

    asset: str = proto.Field(
        proto.STRING,
        number=1,
    )
    served_asset_field_type: (
        gage_served_asset_field_type.ServedAssetFieldTypeEnum.ServedAssetFieldType
    ) = proto.Field(
        proto.ENUM,
        number=2,
        enum=gage_served_asset_field_type.ServedAssetFieldTypeEnum.ServedAssetFieldType,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
