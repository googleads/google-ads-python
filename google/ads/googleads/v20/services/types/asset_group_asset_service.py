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

from google.ads.googleads.v20.resources.types import asset_group_asset
from google.protobuf import field_mask_pb2  # type: ignore
from google.rpc import status_pb2  # type: ignore


__protobuf__ = proto.module(
    package="google.ads.googleads.v20.services",
    marshal="google.ads.googleads.v20",
    manifest={
        "MutateAssetGroupAssetsRequest",
        "AssetGroupAssetOperation",
        "MutateAssetGroupAssetsResponse",
        "MutateAssetGroupAssetResult",
    },
)


class MutateAssetGroupAssetsRequest(proto.Message):
    r"""Request message for
    [AssetGroupAssetService.MutateAssetGroupAssets][google.ads.googleads.v20.services.AssetGroupAssetService.MutateAssetGroupAssets].

    Attributes:
        customer_id (str):
            Required. The ID of the customer whose asset
            group assets are being modified.
        operations (MutableSequence[google.ads.googleads.v20.services.types.AssetGroupAssetOperation]):
            Required. The list of operations to perform
            on individual asset group assets.
        partial_failure (bool):
            If true, successful operations will be
            carried out and invalid operations will return
            errors. If false, all operations will be carried
            out in one transaction if and only if they are
            all valid. Default is false.
        validate_only (bool):
            If true, the request is validated but not
            executed. Only errors are returned, not results.
    """

    customer_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    operations: MutableSequence["AssetGroupAssetOperation"] = (
        proto.RepeatedField(
            proto.MESSAGE,
            number=2,
            message="AssetGroupAssetOperation",
        )
    )
    partial_failure: bool = proto.Field(
        proto.BOOL,
        number=3,
    )
    validate_only: bool = proto.Field(
        proto.BOOL,
        number=4,
    )


class AssetGroupAssetOperation(proto.Message):
    r"""A single operation (create, remove) on an asset group asset.

    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        update_mask (google.protobuf.field_mask_pb2.FieldMask):
            FieldMask that determines which resource
            fields are modified in an update.
        create (google.ads.googleads.v20.resources.types.AssetGroupAsset):
            Create operation: No resource name is
            expected for the new asset group asset.

            This field is a member of `oneof`_ ``operation``.
        update (google.ads.googleads.v20.resources.types.AssetGroupAsset):
            Update operation: The asset group asset is
            expected to have a valid resource name.

            This field is a member of `oneof`_ ``operation``.
        remove (str):
            Remove operation: A resource name for the removed asset
            group asset is expected, in this format:
            ``customers/{customer_id}/assetGroupAssets/{asset_group_id}~{asset_id}~{field_type}``

            This field is a member of `oneof`_ ``operation``.
    """

    update_mask: field_mask_pb2.FieldMask = proto.Field(
        proto.MESSAGE,
        number=4,
        message=field_mask_pb2.FieldMask,
    )
    create: asset_group_asset.AssetGroupAsset = proto.Field(
        proto.MESSAGE,
        number=1,
        oneof="operation",
        message=asset_group_asset.AssetGroupAsset,
    )
    update: asset_group_asset.AssetGroupAsset = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="operation",
        message=asset_group_asset.AssetGroupAsset,
    )
    remove: str = proto.Field(
        proto.STRING,
        number=3,
        oneof="operation",
    )


class MutateAssetGroupAssetsResponse(proto.Message):
    r"""Response message for an asset group asset mutate.

    Attributes:
        results (MutableSequence[google.ads.googleads.v20.services.types.MutateAssetGroupAssetResult]):
            All results for the mutate.
        partial_failure_error (google.rpc.status_pb2.Status):
            Errors that pertain to operation failures in the partial
            failure mode. Returned only when partial_failure = true and
            all errors occur inside the operations. If any errors occur
            outside the operations (for example, auth errors), we return
            an RPC level error.
    """

    results: MutableSequence["MutateAssetGroupAssetResult"] = (
        proto.RepeatedField(
            proto.MESSAGE,
            number=1,
            message="MutateAssetGroupAssetResult",
        )
    )
    partial_failure_error: status_pb2.Status = proto.Field(
        proto.MESSAGE,
        number=2,
        message=status_pb2.Status,
    )


class MutateAssetGroupAssetResult(proto.Message):
    r"""The result for the asset group asset mutate.

    Attributes:
        resource_name (str):
            Returned for successful operations.
    """

    resource_name: str = proto.Field(
        proto.STRING,
        number=1,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
