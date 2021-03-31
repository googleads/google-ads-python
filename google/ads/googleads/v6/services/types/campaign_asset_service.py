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


from google.ads.googleads.v6.resources.types import campaign_asset
from google.rpc import status_pb2 as status  # type: ignore


__protobuf__ = proto.module(
    package="google.ads.googleads.v6.services",
    marshal="google.ads.googleads.v6",
    manifest={
        "GetCampaignAssetRequest",
        "MutateCampaignAssetsRequest",
        "CampaignAssetOperation",
        "MutateCampaignAssetsResponse",
        "MutateCampaignAssetResult",
    },
)


class GetCampaignAssetRequest(proto.Message):
    r"""Request message for
    [CampaignAssetService.GetCampaignAsset][google.ads.googleads.v6.services.CampaignAssetService.GetCampaignAsset].

    Attributes:
        resource_name (str):
            Required. The resource name of the campaign
            asset to fetch.
    """

    resource_name = proto.Field(proto.STRING, number=1)


class MutateCampaignAssetsRequest(proto.Message):
    r"""Request message for
    [CampaignAssetService.MutateCampaignAssets][google.ads.googleads.v6.services.CampaignAssetService.MutateCampaignAssets].

    Attributes:
        customer_id (str):
            Required. The ID of the customer whose
            campaign assets are being modified.
        operations (Sequence[google.ads.googleads.v6.services.types.CampaignAssetOperation]):
            Required. The list of operations to perform
            on individual campaign assets.
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

    customer_id = proto.Field(proto.STRING, number=1)
    operations = proto.RepeatedField(
        proto.MESSAGE, number=2, message="CampaignAssetOperation",
    )
    partial_failure = proto.Field(proto.BOOL, number=3)
    validate_only = proto.Field(proto.BOOL, number=4)


class CampaignAssetOperation(proto.Message):
    r"""A single operation (create, remove) on a campaign asset.

    Attributes:
        create (google.ads.googleads.v6.resources.types.CampaignAsset):
            Create operation: No resource name is
            expected for the new campaign asset.
        remove (str):
            Remove operation: A resource name for the removed campaign
            asset is expected, in this format:

            ``customers/{customer_id}/campaignAssets/{campaign_id}~{asset_id}~{field_type}``
    """

    create = proto.Field(
        proto.MESSAGE,
        number=1,
        oneof="operation",
        message=campaign_asset.CampaignAsset,
    )
    remove = proto.Field(proto.STRING, number=2, oneof="operation")


class MutateCampaignAssetsResponse(proto.Message):
    r"""Response message for a campaign asset mutate.

    Attributes:
        partial_failure_error (google.rpc.status_pb2.Status):
            Errors that pertain to operation failures in the partial
            failure mode. Returned only when partial_failure = true and
            all errors occur inside the operations. If any errors occur
            outside the operations (e.g. auth errors), we return an RPC
            level error.
        results (Sequence[google.ads.googleads.v6.services.types.MutateCampaignAssetResult]):
            All results for the mutate.
    """

    partial_failure_error = proto.Field(
        proto.MESSAGE, number=1, message=status.Status,
    )
    results = proto.RepeatedField(
        proto.MESSAGE, number=2, message="MutateCampaignAssetResult",
    )


class MutateCampaignAssetResult(proto.Message):
    r"""The result for the campaign asset mutate.

    Attributes:
        resource_name (str):
            Returned for successful operations.
    """

    resource_name = proto.Field(proto.STRING, number=1)


__all__ = tuple(sorted(__protobuf__.manifest))
