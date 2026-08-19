# -*- coding: utf-8 -*-
# Copyright 2026 Google LLC
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

from google.ads.googleads.v25.enums.types import conversion_action_category
from google.ads.googleads.v25.enums.types import conversion_origin


__protobuf__ = proto.module(
    package="google.ads.googleads.v25.common",
    marshal="google.ads.googleads.v25",
    manifest={
        "EffectiveAutomaticGoal",
    },
)


class EffectiveAutomaticGoal(proto.Message):
    r"""Represents an effective automatic conversion goal.

    Attributes:
        category (google.ads.googleads.v25.enums.types.ConversionActionCategoryEnum.ConversionActionCategory):
            Conversion category.
        origin (google.ads.googleads.v25.enums.types.ConversionOriginEnum.ConversionOrigin):
            Conversion origin.
    """

    category: (
        conversion_action_category.ConversionActionCategoryEnum.ConversionActionCategory
    ) = proto.Field(
        proto.ENUM,
        number=1,
        enum=conversion_action_category.ConversionActionCategoryEnum.ConversionActionCategory,
    )
    origin: conversion_origin.ConversionOriginEnum.ConversionOrigin = (
        proto.Field(
            proto.ENUM,
            number=2,
            enum=conversion_origin.ConversionOriginEnum.ConversionOrigin,
        )
    )


__all__ = tuple(sorted(__protobuf__.manifest))
