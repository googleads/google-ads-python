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


from google.ads.googleads.v4.enums.types import merchant_center_link_status
from google.protobuf import wrappers_pb2 as wrappers  # type: ignore


__protobuf__ = proto.module(
    package="google.ads.googleads.v4.resources",
    marshal="google.ads.googleads.v4",
    manifest={"MerchantCenterLink",},
)


class MerchantCenterLink(proto.Message):
    r"""A data sharing connection, proposed or in use,
    between a Google Ads Customer and a Merchant Center account.

    Attributes:
        resource_name (str):
            Immutable. The resource name of the merchant center link.
            Merchant center link resource names have the form:

            ``customers/{customer_id}/merchantCenterLinks/{merchant_center_id}``
        id (google.protobuf.wrappers_pb2.Int64Value):
            Output only. The ID of the Merchant Center
            account. This field is readonly.
        merchant_center_account_name (google.protobuf.wrappers_pb2.StringValue):
            Output only. The name of the Merchant Center
            account. This field is readonly.
        status (google.ads.googleads.v4.enums.types.MerchantCenterLinkStatusEnum.MerchantCenterLinkStatus):
            The status of the link.
    """

    resource_name = proto.Field(proto.STRING, number=1)
    id = proto.Field(proto.MESSAGE, number=3, message=wrappers.Int64Value,)
    merchant_center_account_name = proto.Field(
        proto.MESSAGE, number=4, message=wrappers.StringValue,
    )
    status = proto.Field(
        proto.ENUM,
        number=5,
        enum=merchant_center_link_status.MerchantCenterLinkStatusEnum.MerchantCenterLinkStatus,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
