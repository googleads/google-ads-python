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

from google.ads.googleads.v14.enums.types import conversion_action_category
from google.ads.googleads.v14.enums.types import conversion_origin


__protobuf__ = proto.module(
    package="google.ads.googleads.v14.resources",
    marshal="google.ads.googleads.v14",
    manifest={
        "CustomerConversionGoal",
    },
)


class CustomerConversionGoal(proto.Message):
    r"""Biddability control for conversion actions with a matching
    category and origin.

    Attributes:
        resource_name (str):
            Immutable. The resource name of the customer conversion
            goal. Customer conversion goal resource names have the form:

            ``customers/{customer_id}/customerConversionGoals/{category}~{origin}``
        category (google.ads.googleads.v14.enums.types.ConversionActionCategoryEnum.ConversionActionCategory):
            The conversion category of this customer
            conversion goal. Only conversion actions that
            have this category will be included in this
            goal.
        origin (google.ads.googleads.v14.enums.types.ConversionOriginEnum.ConversionOrigin):
            The conversion origin of this customer
            conversion goal. Only conversion actions that
            have this conversion origin will be included in
            this goal.
        biddable (bool):
            The biddability of the customer conversion
            goal.
    """

    resource_name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    category: conversion_action_category.ConversionActionCategoryEnum.ConversionActionCategory = proto.Field(
        proto.ENUM,
        number=2,
        enum=conversion_action_category.ConversionActionCategoryEnum.ConversionActionCategory,
    )
    origin: conversion_origin.ConversionOriginEnum.ConversionOrigin = (
        proto.Field(
            proto.ENUM,
            number=3,
            enum=conversion_origin.ConversionOriginEnum.ConversionOrigin,
        )
    )
    biddable: bool = proto.Field(
        proto.BOOL,
        number=4,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
