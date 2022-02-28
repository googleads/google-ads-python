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

from google.ads.googleads.v10.enums.types import asset_field_type
from google.ads.googleads.v10.enums.types import asset_link_status


__protobuf__ = proto.module(
    package="google.ads.googleads.v10.resources",
    marshal="google.ads.googleads.v10",
    manifest={"AdGroupAsset",},
)


class AdGroupAsset(proto.Message):
    r"""A link between an ad group and an asset.

    Attributes:
        resource_name (str):
            Immutable. The resource name of the ad group asset.
            AdGroupAsset resource names have the form:

            ``customers/{customer_id}/adGroupAssets/{ad_group_id}~{asset_id}~{field_type}``
        ad_group (str):
            Required. Immutable. The ad group to which
            the asset is linked.
        asset (str):
            Required. Immutable. The asset which is
            linked to the ad group.
        field_type (google.ads.googleads.v10.enums.types.AssetFieldTypeEnum.AssetFieldType):
            Required. Immutable. Role that the asset
            takes under the linked ad group.
        status (google.ads.googleads.v10.enums.types.AssetLinkStatusEnum.AssetLinkStatus):
            Status of the ad group asset.
    """

    resource_name = proto.Field(proto.STRING, number=1,)
    ad_group = proto.Field(proto.STRING, number=2,)
    asset = proto.Field(proto.STRING, number=3,)
    field_type = proto.Field(
        proto.ENUM,
        number=4,
        enum=asset_field_type.AssetFieldTypeEnum.AssetFieldType,
    )
    status = proto.Field(
        proto.ENUM,
        number=5,
        enum=asset_link_status.AssetLinkStatusEnum.AssetLinkStatus,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
