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


from google.ads.googleads.v4.enums.types import product_bidding_category_level
from google.ads.googleads.v4.enums.types import product_bidding_category_status
from google.protobuf import wrappers_pb2 as wrappers  # type: ignore


__protobuf__ = proto.module(
    package="google.ads.googleads.v4.resources",
    marshal="google.ads.googleads.v4",
    manifest={"ProductBiddingCategoryConstant",},
)


class ProductBiddingCategoryConstant(proto.Message):
    r"""A Product Bidding Category.

    Attributes:
        resource_name (str):
            Output only. The resource name of the product bidding
            category. Product bidding category resource names have the
            form:

            ``productBiddingCategoryConstants/{country_code}~{level}~{id}``
        id (google.protobuf.wrappers_pb2.Int64Value):
            Output only. ID of the product bidding category.

            This ID is equivalent to the google_product_category ID as
            described in this article:
            https://support.google.com/merchants/answer/6324436.
        country_code (google.protobuf.wrappers_pb2.StringValue):
            Output only. Two-letter upper-case country
            code of the product bidding category.
        product_bidding_category_constant_parent (google.protobuf.wrappers_pb2.StringValue):
            Output only. Resource name of the parent
            product bidding category.
        level (google.ads.googleads.v4.enums.types.ProductBiddingCategoryLevelEnum.ProductBiddingCategoryLevel):
            Output only. Level of the product bidding
            category.
        status (google.ads.googleads.v4.enums.types.ProductBiddingCategoryStatusEnum.ProductBiddingCategoryStatus):
            Output only. Status of the product bidding
            category.
        language_code (google.protobuf.wrappers_pb2.StringValue):
            Output only. Language code of the product
            bidding category.
        localized_name (google.protobuf.wrappers_pb2.StringValue):
            Output only. Display value of the product bidding category
            localized according to language_code.
    """

    resource_name = proto.Field(proto.STRING, number=1)
    id = proto.Field(proto.MESSAGE, number=2, message=wrappers.Int64Value,)
    country_code = proto.Field(
        proto.MESSAGE, number=3, message=wrappers.StringValue,
    )
    product_bidding_category_constant_parent = proto.Field(
        proto.MESSAGE, number=4, message=wrappers.StringValue,
    )
    level = proto.Field(
        proto.ENUM,
        number=5,
        enum=product_bidding_category_level.ProductBiddingCategoryLevelEnum.ProductBiddingCategoryLevel,
    )
    status = proto.Field(
        proto.ENUM,
        number=6,
        enum=product_bidding_category_status.ProductBiddingCategoryStatusEnum.ProductBiddingCategoryStatus,
    )
    language_code = proto.Field(
        proto.MESSAGE, number=7, message=wrappers.StringValue,
    )
    localized_name = proto.Field(
        proto.MESSAGE, number=8, message=wrappers.StringValue,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
