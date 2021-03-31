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


from google.ads.googleads.v5.enums.types import (
    response_content_type as gage_response_content_type,
)
from google.ads.googleads.v5.resources.types import asset as gagr_asset


__protobuf__ = proto.module(
    package="google.ads.googleads.v5.services",
    marshal="google.ads.googleads.v5",
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
    [AssetService.GetAsset][google.ads.googleads.v5.services.AssetService.GetAsset]

    Attributes:
        resource_name (str):
            Required. The resource name of the asset to
            fetch.
    """

    resource_name = proto.Field(proto.STRING, number=1)


class MutateAssetsRequest(proto.Message):
    r"""Request message for
    [AssetService.MutateAssets][google.ads.googleads.v5.services.AssetService.MutateAssets]

    Attributes:
        customer_id (str):
            Required. The ID of the customer whose assets
            are being modified.
        operations (Sequence[google.ads.googleads.v5.services.types.AssetOperation]):
            Required. The list of operations to perform
            on individual assets.
        response_content_type (google.ads.googleads.v5.enums.types.ResponseContentTypeEnum.ResponseContentType):
            The response content type setting. Determines
            whether the mutable resource or just the
            resource name should be returned post mutation.
    """

    customer_id = proto.Field(proto.STRING, number=1)
    operations = proto.RepeatedField(
        proto.MESSAGE, number=2, message="AssetOperation",
    )
    response_content_type = proto.Field(
        proto.ENUM,
        number=3,
        enum=gage_response_content_type.ResponseContentTypeEnum.ResponseContentType,
    )


class AssetOperation(proto.Message):
    r"""A single operation to create an asset. Supported asset types
    are YoutubeVideoAsset, MediaBundleAsset, ImageAsset, and
    LeadFormAsset. TextAsset should be created with Ad inline.

    Attributes:
        create (google.ads.googleads.v5.resources.types.Asset):
            Create operation: No resource name is
            expected for the new asset.
    """

    create = proto.Field(
        proto.MESSAGE, number=1, oneof="operation", message=gagr_asset.Asset,
    )


class MutateAssetsResponse(proto.Message):
    r"""Response message for an asset mutate.

    Attributes:
        results (Sequence[google.ads.googleads.v5.services.types.MutateAssetResult]):
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
        asset (google.ads.googleads.v5.resources.types.Asset):
            The mutated asset with only mutable fields after mutate. The
            field will only be returned when response_content_type is
            set to "MUTABLE_RESOURCE".
    """

    resource_name = proto.Field(proto.STRING, number=1)
    asset = proto.Field(proto.MESSAGE, number=2, message=gagr_asset.Asset,)


__all__ = tuple(sorted(__protobuf__.manifest))
