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


from google.ads.googleads.v4.enums.types import served_asset_field_type
from google.protobuf import wrappers_pb2 as wrappers  # type: ignore


__protobuf__ = proto.module(
    package="google.ads.googleads.v4.common",
    marshal="google.ads.googleads.v4",
    manifest={
        "AdTextAsset",
        "AdImageAsset",
        "AdVideoAsset",
        "AdMediaBundleAsset",
    },
)


class AdTextAsset(proto.Message):
    r"""A text asset used inside an ad.

    Attributes:
        text (google.protobuf.wrappers_pb2.StringValue):
            Asset text.
        pinned_field (google.ads.googleads.v4.enums.types.ServedAssetFieldTypeEnum.ServedAssetFieldType):
            The pinned field of the asset. This restricts
            the asset to only serve within this field.
            Multiple assets can be pinned to the same field.
            An asset that is unpinned or pinned to a
            different field will not serve in a field where
            some other asset has been pinned.
    """

    text = proto.Field(proto.MESSAGE, number=1, message=wrappers.StringValue,)
    pinned_field = proto.Field(
        proto.ENUM,
        number=2,
        enum=served_asset_field_type.ServedAssetFieldTypeEnum.ServedAssetFieldType,
    )


class AdImageAsset(proto.Message):
    r"""An image asset used inside an ad.

    Attributes:
        asset (google.protobuf.wrappers_pb2.StringValue):
            The Asset resource name of this image.
    """

    asset = proto.Field(proto.MESSAGE, number=1, message=wrappers.StringValue,)


class AdVideoAsset(proto.Message):
    r"""A video asset used inside an ad.

    Attributes:
        asset (google.protobuf.wrappers_pb2.StringValue):
            The Asset resource name of this video.
    """

    asset = proto.Field(proto.MESSAGE, number=1, message=wrappers.StringValue,)


class AdMediaBundleAsset(proto.Message):
    r"""A media bundle asset used inside an ad.

    Attributes:
        asset (google.protobuf.wrappers_pb2.StringValue):
            The Asset resource name of this media bundle.
    """

    asset = proto.Field(proto.MESSAGE, number=1, message=wrappers.StringValue,)


__all__ = tuple(sorted(__protobuf__.manifest))
