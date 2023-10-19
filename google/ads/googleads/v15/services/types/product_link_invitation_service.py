# -*- coding: utf-8 -*-
# Copyright 2023 Google LLC
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

from google.ads.googleads.v15.enums.types import (
    product_link_invitation_status as gage_product_link_invitation_status,
)


__protobuf__ = proto.module(
    package="google.ads.googleads.v15.services",
    marshal="google.ads.googleads.v15",
    manifest={
        "UpdateProductLinkInvitationRequest",
        "UpdateProductLinkInvitationResponse",
    },
)


class UpdateProductLinkInvitationRequest(proto.Message):
    r"""Request message for
    [ProductLinkInvitationService.UpdateProductLinkInvitation][google.ads.googleads.v15.services.ProductLinkInvitationService.UpdateProductLinkInvitation].

    Attributes:
        customer_id (str):
            Required. The ID of the customer being
            modified.
        product_link_invitation_status (google.ads.googleads.v15.enums.types.ProductLinkInvitationStatusEnum.ProductLinkInvitationStatus):
            Required. The product link invitation to be
            created.
        resource_name (str):
            Required. Resource name of the product link
            invitation.
    """

    customer_id: str = proto.Field(
        proto.STRING,
        number=1,
    )
    product_link_invitation_status: gage_product_link_invitation_status.ProductLinkInvitationStatusEnum.ProductLinkInvitationStatus = proto.Field(
        proto.ENUM,
        number=2,
        enum=gage_product_link_invitation_status.ProductLinkInvitationStatusEnum.ProductLinkInvitationStatus,
    )
    resource_name: str = proto.Field(
        proto.STRING,
        number=3,
    )


class UpdateProductLinkInvitationResponse(proto.Message):
    r"""Response message for product link invitation update.
    Attributes:
        resource_name (str):
            Result of the update.
    """

    resource_name: str = proto.Field(
        proto.STRING,
        number=1,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
