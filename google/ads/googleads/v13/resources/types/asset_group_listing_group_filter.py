# -*- coding: utf-8 -*-
# Copyright 2022 Google LLC
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

from google.ads.googleads.v13.enums.types import (
    listing_group_filter_bidding_category_level,
)
from google.ads.googleads.v13.enums.types import (
    listing_group_filter_custom_attribute_index,
)
from google.ads.googleads.v13.enums.types import (
    listing_group_filter_product_channel,
)
from google.ads.googleads.v13.enums.types import (
    listing_group_filter_product_condition,
)
from google.ads.googleads.v13.enums.types import (
    listing_group_filter_product_type_level,
)
from google.ads.googleads.v13.enums.types import listing_group_filter_type_enum
from google.ads.googleads.v13.enums.types import listing_group_filter_vertical


__protobuf__ = proto.module(
    package="google.ads.googleads.v13.resources",
    marshal="google.ads.googleads.v13",
    manifest={"AssetGroupListingGroupFilter", "ListingGroupFilterDimension",},
)


class AssetGroupListingGroupFilter(proto.Message):
    r"""AssetGroupListingGroupFilter represents a listing group
    filter tree node in an asset group.

    Attributes:
        resource_name (str):
            Immutable. The resource name of the asset group listing
            group filter. Asset group listing group filter resource name
            have the form:

            ``customers/{customer_id}/assetGroupListingGroupFilters/{asset_group_id}~{listing_group_filter_id}``
        asset_group (str):
            Immutable. The asset group which this asset
            group listing group filter is part of.
        id (int):
            Output only. The ID of the
            ListingGroupFilter.
        type_ (google.ads.googleads.v13.enums.types.ListingGroupFilterTypeEnum.ListingGroupFilterType):
            Immutable. Type of a listing group filter
            node.
        vertical (google.ads.googleads.v13.enums.types.ListingGroupFilterVerticalEnum.ListingGroupFilterVertical):
            Immutable. The vertical the current node tree
            represents. All nodes in the same tree must
            belong to the same vertical.
        case_value (google.ads.googleads.v13.resources.types.ListingGroupFilterDimension):
            Dimension value with which this listing group
            is refining its parent. Undefined for the root
            group.
        parent_listing_group_filter (str):
            Immutable. Resource name of the parent
            listing group subdivision. Null for the root
            listing group filter node.
    """

    resource_name: str = proto.Field(
        proto.STRING, number=1,
    )
    asset_group: str = proto.Field(
        proto.STRING, number=2,
    )
    id: int = proto.Field(
        proto.INT64, number=3,
    )
    type_: listing_group_filter_type_enum.ListingGroupFilterTypeEnum.ListingGroupFilterType = proto.Field(
        proto.ENUM,
        number=4,
        enum=listing_group_filter_type_enum.ListingGroupFilterTypeEnum.ListingGroupFilterType,
    )
    vertical: listing_group_filter_vertical.ListingGroupFilterVerticalEnum.ListingGroupFilterVertical = proto.Field(
        proto.ENUM,
        number=5,
        enum=listing_group_filter_vertical.ListingGroupFilterVerticalEnum.ListingGroupFilterVertical,
    )
    case_value: "ListingGroupFilterDimension" = proto.Field(
        proto.MESSAGE, number=6, message="ListingGroupFilterDimension",
    )
    parent_listing_group_filter: str = proto.Field(
        proto.STRING, number=7,
    )


class ListingGroupFilterDimension(proto.Message):
    r"""Listing dimensions for the asset group listing group filter.
    This message has `oneof`_ fields (mutually exclusive fields).
    For each oneof, at most one member field can be set at the same time.
    Setting any member of the oneof automatically clears all other
    members.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        product_bidding_category (google.ads.googleads.v13.resources.types.ListingGroupFilterDimension.ProductBiddingCategory):
            Bidding category of a product offer.

            This field is a member of `oneof`_ ``dimension``.
        product_brand (google.ads.googleads.v13.resources.types.ListingGroupFilterDimension.ProductBrand):
            Brand of a product offer.

            This field is a member of `oneof`_ ``dimension``.
        product_channel (google.ads.googleads.v13.resources.types.ListingGroupFilterDimension.ProductChannel):
            Locality of a product offer.

            This field is a member of `oneof`_ ``dimension``.
        product_condition (google.ads.googleads.v13.resources.types.ListingGroupFilterDimension.ProductCondition):
            Condition of a product offer.

            This field is a member of `oneof`_ ``dimension``.
        product_custom_attribute (google.ads.googleads.v13.resources.types.ListingGroupFilterDimension.ProductCustomAttribute):
            Custom attribute of a product offer.

            This field is a member of `oneof`_ ``dimension``.
        product_item_id (google.ads.googleads.v13.resources.types.ListingGroupFilterDimension.ProductItemId):
            Item id of a product offer.

            This field is a member of `oneof`_ ``dimension``.
        product_type (google.ads.googleads.v13.resources.types.ListingGroupFilterDimension.ProductType):
            Type of a product offer.

            This field is a member of `oneof`_ ``dimension``.
    """

    class ProductBiddingCategory(proto.Message):
        r"""One element of a bidding category at a certain level.
        Top-level categories are at level 1, their children at level 2,
        and so on. We currently support up to 5 levels. The user must
        specify a dimension type that indicates the level of the
        category. All cases of the same subdivision must have the same
        dimension type (category level).

        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            id (int):
                ID of the product bidding category.

                This ID is equivalent to the google_product_category ID as
                described in this article:
                https://support.google.com/merchants/answer/6324436

                This field is a member of `oneof`_ ``_id``.
            level (google.ads.googleads.v13.enums.types.ListingGroupFilterBiddingCategoryLevelEnum.ListingGroupFilterBiddingCategoryLevel):
                Indicates the level of the category in the
                taxonomy.
        """

        id: int = proto.Field(
            proto.INT64, number=1, optional=True,
        )
        level: listing_group_filter_bidding_category_level.ListingGroupFilterBiddingCategoryLevelEnum.ListingGroupFilterBiddingCategoryLevel = proto.Field(
            proto.ENUM,
            number=2,
            enum=listing_group_filter_bidding_category_level.ListingGroupFilterBiddingCategoryLevelEnum.ListingGroupFilterBiddingCategoryLevel,
        )

    class ProductBrand(proto.Message):
        r"""Brand of the product.
        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            value (str):
                String value of the product brand.

                This field is a member of `oneof`_ ``_value``.
        """

        value: str = proto.Field(
            proto.STRING, number=1, optional=True,
        )

    class ProductChannel(proto.Message):
        r"""Locality of a product offer.
        Attributes:
            channel (google.ads.googleads.v13.enums.types.ListingGroupFilterProductChannelEnum.ListingGroupFilterProductChannel):
                Value of the locality.
        """

        channel: listing_group_filter_product_channel.ListingGroupFilterProductChannelEnum.ListingGroupFilterProductChannel = proto.Field(
            proto.ENUM,
            number=1,
            enum=listing_group_filter_product_channel.ListingGroupFilterProductChannelEnum.ListingGroupFilterProductChannel,
        )

    class ProductCondition(proto.Message):
        r"""Condition of a product offer.
        Attributes:
            condition (google.ads.googleads.v13.enums.types.ListingGroupFilterProductConditionEnum.ListingGroupFilterProductCondition):
                Value of the condition.
        """

        condition: listing_group_filter_product_condition.ListingGroupFilterProductConditionEnum.ListingGroupFilterProductCondition = proto.Field(
            proto.ENUM,
            number=1,
            enum=listing_group_filter_product_condition.ListingGroupFilterProductConditionEnum.ListingGroupFilterProductCondition,
        )

    class ProductCustomAttribute(proto.Message):
        r"""Custom attribute of a product offer.
        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            value (str):
                String value of the product custom attribute.

                This field is a member of `oneof`_ ``_value``.
            index (google.ads.googleads.v13.enums.types.ListingGroupFilterCustomAttributeIndexEnum.ListingGroupFilterCustomAttributeIndex):
                Indicates the index of the custom attribute.
        """

        value: str = proto.Field(
            proto.STRING, number=1, optional=True,
        )
        index: listing_group_filter_custom_attribute_index.ListingGroupFilterCustomAttributeIndexEnum.ListingGroupFilterCustomAttributeIndex = proto.Field(
            proto.ENUM,
            number=2,
            enum=listing_group_filter_custom_attribute_index.ListingGroupFilterCustomAttributeIndexEnum.ListingGroupFilterCustomAttributeIndex,
        )

    class ProductItemId(proto.Message):
        r"""Item id of a product offer.
        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            value (str):
                Value of the id.

                This field is a member of `oneof`_ ``_value``.
        """

        value: str = proto.Field(
            proto.STRING, number=1, optional=True,
        )

    class ProductType(proto.Message):
        r"""Type of a product offer.
        .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

        Attributes:
            value (str):
                Value of the type.

                This field is a member of `oneof`_ ``_value``.
            level (google.ads.googleads.v13.enums.types.ListingGroupFilterProductTypeLevelEnum.ListingGroupFilterProductTypeLevel):
                Level of the type.
        """

        value: str = proto.Field(
            proto.STRING, number=1, optional=True,
        )
        level: listing_group_filter_product_type_level.ListingGroupFilterProductTypeLevelEnum.ListingGroupFilterProductTypeLevel = proto.Field(
            proto.ENUM,
            number=2,
            enum=listing_group_filter_product_type_level.ListingGroupFilterProductTypeLevelEnum.ListingGroupFilterProductTypeLevel,
        )

    product_bidding_category: ProductBiddingCategory = proto.Field(
        proto.MESSAGE,
        number=1,
        oneof="dimension",
        message=ProductBiddingCategory,
    )
    product_brand: ProductBrand = proto.Field(
        proto.MESSAGE, number=2, oneof="dimension", message=ProductBrand,
    )
    product_channel: ProductChannel = proto.Field(
        proto.MESSAGE, number=3, oneof="dimension", message=ProductChannel,
    )
    product_condition: ProductCondition = proto.Field(
        proto.MESSAGE, number=4, oneof="dimension", message=ProductCondition,
    )
    product_custom_attribute: ProductCustomAttribute = proto.Field(
        proto.MESSAGE,
        number=5,
        oneof="dimension",
        message=ProductCustomAttribute,
    )
    product_item_id: ProductItemId = proto.Field(
        proto.MESSAGE, number=6, oneof="dimension", message=ProductItemId,
    )
    product_type: ProductType = proto.Field(
        proto.MESSAGE, number=7, oneof="dimension", message=ProductType,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
