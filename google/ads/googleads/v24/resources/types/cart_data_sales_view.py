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


__protobuf__ = proto.module(
    package="google.ads.googleads.v24.resources",
    marshal="google.ads.googleads.v24",
    manifest={
        "CartDataSalesView",
    },
)


class CartDataSalesView(proto.Message):
    r"""Cart data sales view.

    Provides information about the products which were purchased if
    conversions with cart data is implemented. Performance metrics
    like revenue, gross profit, lead/cross-sell metrics etc. and
    Merchant Center attributes such as brand, category etc. are
    available for products defined in an inventory feed and sold as
    a result of Google ads. For purchases attributed to clicks on
    Shopping ads, dimensions of both clicked and sold products can
    be viewed together.

    Attributes:
        resource_name (str):
            Output only. The resource name of the Cart data sales view.
            Cart data sales view resource names have the form:
            ``customers/{customer_id}/cartDataSalesView``
    """

    resource_name: str = proto.Field(
        proto.STRING,
        number=1,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
