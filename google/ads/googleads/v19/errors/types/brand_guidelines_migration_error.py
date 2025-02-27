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
    package="google.ads.googleads.v19.errors",
    marshal="google.ads.googleads.v19",
    manifest={
        "BrandGuidelinesMigrationErrorEnum",
    },
)


class BrandGuidelinesMigrationErrorEnum(proto.Message):
    r"""Container for enum describing brand guidelines migration
    errors.

    """

    class BrandGuidelinesMigrationError(proto.Enum):
        r"""Enum describing brand guidelines migration errors."""

        UNSPECIFIED = 0
        UNKNOWN = 1
        BRAND_GUIDELINES_ALREADY_ENABLED = 2
        CANNOT_ENABLE_BRAND_GUIDELINES_FOR_REMOVED_CAMPAIGN = 3
        BRAND_GUIDELINES_LOGO_LIMIT_EXCEEDED = 4
        CANNOT_AUTO_POPULATE_BRAND_ASSETS_WHEN_BRAND_ASSETS_PROVIDED = 5
        AUTO_POPULATE_BRAND_ASSETS_REQUIRED_WHEN_BRAND_ASSETS_OMITTED = 6
        TOO_MANY_ENABLE_OPERATIONS = 7


__all__ = tuple(sorted(__protobuf__.manifest))
