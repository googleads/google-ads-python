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

from google.ads.googleads.v15.enums.types import conversion_action_category
from google.ads.googleads.v15.enums.types import conversion_origin


__protobuf__ = proto.module(
    package="google.ads.googleads.v15.resources",
    marshal="google.ads.googleads.v15",
    manifest={
        "CampaignConversionGoal",
    },
)


class CampaignConversionGoal(proto.Message):
    r"""The biddability setting for the specified campaign only for
    all conversion actions with a matching category and origin.

    Attributes:
        resource_name (str):
            Immutable. The resource name of the campaign conversion
            goal. Campaign conversion goal resource names have the form:

            ``customers/{customer_id}/campaignConversionGoals/{campaign_id}~{category}~{origin}``
        campaign (str):
            Immutable. The campaign with which this
            campaign conversion goal is associated.
        category (google.ads.googleads.v15.enums.types.ConversionActionCategoryEnum.ConversionActionCategory):
            The conversion category of this campaign
            conversion goal.
        origin (google.ads.googleads.v15.enums.types.ConversionOriginEnum.ConversionOrigin):
            The conversion origin of this campaign
            conversion goal.
        biddable (bool):
            The biddability of the campaign conversion
            goal.
    """

    resource_name: str = proto.Field(
        proto.STRING,
        number=1,
    )
    campaign: str = proto.Field(
        proto.STRING,
        number=2,
    )
    category: conversion_action_category.ConversionActionCategoryEnum.ConversionActionCategory = proto.Field(
        proto.ENUM,
        number=3,
        enum=conversion_action_category.ConversionActionCategoryEnum.ConversionActionCategory,
    )
    origin: conversion_origin.ConversionOriginEnum.ConversionOrigin = (
        proto.Field(
            proto.ENUM,
            number=4,
            enum=conversion_origin.ConversionOriginEnum.ConversionOrigin,
        )
    )
    biddable: bool = proto.Field(
        proto.BOOL,
        number=5,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
