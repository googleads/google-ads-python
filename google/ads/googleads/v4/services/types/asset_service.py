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


from google.ads.googleads.v4.resources.types import asset


__protobuf__ = proto.module(
    package="google.ads.googleads.v4.services",
    marshal="google.ads.googleads.v4",
    manifest={
        "GetAssetRequest",
        "MutateAssetsRequest",
        "AssetOperation",
        "MutateAssetsResponse",
        "MutateAssetResult",
    },
)


class GetAssetRequest(proto.Message):
    r"""Request message for
    [AssetService.GetAsset][google.ads.googleads.v4.services.AssetService.GetAsset]

    Attributes:
        resource_name (str):
            Required. The resource name of the asset to
            fetch.
    """

    resource_name = proto.Field(proto.STRING, number=1)


class MutateAssetsRequest(proto.Message):
    r"""Request message for
    [AssetService.MutateAssets][google.ads.googleads.v4.services.AssetService.MutateAssets]

    Attributes:
        customer_id (str):
            Required. The ID of the customer whose assets
            are being modified.
        operations (Sequence[google.ads.googleads.v4.services.types.AssetOperation]):
            Required. The list of operations to perform
            on individual assets.
    """

    customer_id = proto.Field(proto.STRING, number=1)
    operations = proto.RepeatedField(
        proto.MESSAGE, number=2, message="AssetOperation",
    )


class AssetOperation(proto.Message):
    r"""A single operation to create an asset. Supported asset types
    are YoutubeVideoAsset, MediaBundleAsset, ImageAsset, and
    LeadFormAsset. TextAsset should be created with Ad inline.

    Attributes:
        create (google.ads.googleads.v4.resources.types.Asset):
            Create operation: No resource name is
            expected for the new asset.
    """

    create = proto.Field(
        proto.MESSAGE, number=1, oneof="operation", message=asset.Asset,
    )


class MutateAssetsResponse(proto.Message):
    r"""Response message for an asset mutate.

    Attributes:
        results (Sequence[google.ads.googleads.v4.services.types.MutateAssetResult]):
            All results for the mutate.
    """

    results = proto.RepeatedField(
        proto.MESSAGE, number=2, message="MutateAssetResult",
    )


class MutateAssetResult(proto.Message):
    r"""The result for the asset mutate.

    Attributes:
        resource_name (str):
            The resource name returned for successful
            operations.
    """

    resource_name = proto.Field(proto.STRING, number=1)


__all__ = tuple(sorted(__protobuf__.manifest))
