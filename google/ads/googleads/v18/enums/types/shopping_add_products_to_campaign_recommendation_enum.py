# -*- coding: utf-8 -*-
# Copyright 2024 Google LLC
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
    package="google.ads.googleads.v18.enums",
    marshal="google.ads.googleads.v18",
    manifest={"ShoppingAddProductsToCampaignRecommendationEnum",},
)


class ShoppingAddProductsToCampaignRecommendationEnum(proto.Message):
    r"""Indicates the key issue that results in a shopping campaign
    targeting zero products.

    """

    class Reason(proto.Enum):
        r"""Issues that results in a shopping campaign targeting zero
        products.
        """
        UNSPECIFIED = 0
        UNKNOWN = 1
        MERCHANT_CENTER_ACCOUNT_HAS_NO_SUBMITTED_PRODUCTS = 2
        MERCHANT_CENTER_ACCOUNT_HAS_NO_SUBMITTED_PRODUCTS_IN_FEED = 3
        ADS_ACCOUNT_EXCLUDES_OFFERS_FROM_CAMPAIGN = 4
        ALL_PRODUCTS_ARE_EXCLUDED_FROM_CAMPAIGN = 5


__all__ = tuple(sorted(__protobuf__.manifest))
