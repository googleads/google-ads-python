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


from google.ads.googleads.v5.common.types import asset_types
from google.ads.googleads.v5.enums.types import asset_type


__protobuf__ = proto.module(
    package="google.ads.googleads.v5.resources",
    marshal="google.ads.googleads.v5",
    manifest={"Asset",},
)


class Asset(proto.Message):
    r"""Asset is a part of an ad which can be shared across multiple
    ads. It can be an image (ImageAsset), a video
    (YoutubeVideoAsset), etc. Assets are immutable and cannot be
    removed. To stop an asset from serving, remove the asset from
    the entity that is using it.

    Attributes:
        resource_name (str):
            Immutable. The resource name of the asset. Asset resource
            names have the form:

            ``customers/{customer_id}/assets/{asset_id}``
        id (int):
            Output only. The ID of the asset.
        name (str):
            Optional name of the asset.
        type_ (google.ads.googleads.v5.enums.types.AssetTypeEnum.AssetType):
            Output only. Type of the asset.
        youtube_video_asset (google.ads.googleads.v5.common.types.YoutubeVideoAsset):
            Immutable. A YouTube video asset.
        media_bundle_asset (google.ads.googleads.v5.common.types.MediaBundleAsset):
            Immutable. A media bundle asset.
        image_asset (google.ads.googleads.v5.common.types.ImageAsset):
            Output only. An image asset.
        text_asset (google.ads.googleads.v5.common.types.TextAsset):
            Output only. A text asset.
        book_on_google_asset (google.ads.googleads.v5.common.types.BookOnGoogleAsset):
            A book on google asset.
    """

    resource_name = proto.Field(proto.STRING, number=1)
    id = proto.Field(proto.INT64, number=11, optional=True)
    name = proto.Field(proto.STRING, number=12, optional=True)
    type_ = proto.Field(
        proto.ENUM, number=4, enum=asset_type.AssetTypeEnum.AssetType,
    )
    youtube_video_asset = proto.Field(
        proto.MESSAGE,
        number=5,
        oneof="asset_data",
        message=asset_types.YoutubeVideoAsset,
    )
    media_bundle_asset = proto.Field(
        proto.MESSAGE,
        number=6,
        oneof="asset_data",
        message=asset_types.MediaBundleAsset,
    )
    image_asset = proto.Field(
        proto.MESSAGE,
        number=7,
        oneof="asset_data",
        message=asset_types.ImageAsset,
    )
    text_asset = proto.Field(
        proto.MESSAGE,
        number=8,
        oneof="asset_data",
        message=asset_types.TextAsset,
    )
    book_on_google_asset = proto.Field(
        proto.MESSAGE,
        number=10,
        oneof="asset_data",
        message=asset_types.BookOnGoogleAsset,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
