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

from typing import MutableSequence

import proto  # type: ignore

from google.ads.googleads.v20.enums.types import (
    advertising_channel_sub_type as gage_advertising_channel_sub_type,
)
from google.ads.googleads.v20.enums.types import (
    advertising_channel_type as gage_advertising_channel_type,
)
from google.ads.googleads.v20.enums.types import (
    criterion_category_channel_availability_mode,
)
from google.ads.googleads.v20.enums.types import (
    criterion_category_locale_availability_mode,
)


__protobuf__ = proto.module(
    package="google.ads.googleads.v20.common",
    marshal="google.ads.googleads.v20",
    manifest={
        "CriterionCategoryAvailability",
        "CriterionCategoryChannelAvailability",
        "CriterionCategoryLocaleAvailability",
    },
)


class CriterionCategoryAvailability(proto.Message):
    r"""Information of category availability, per advertising
    channel.

    Attributes:
        channel (google.ads.googleads.v20.common.types.CriterionCategoryChannelAvailability):
            Channel types and subtypes that are available
            to the category.
        locale (MutableSequence[google.ads.googleads.v20.common.types.CriterionCategoryLocaleAvailability]):
            Locales that are available to the category
            for the channel.
    """

    channel: "CriterionCategoryChannelAvailability" = proto.Field(
        proto.MESSAGE,
        number=1,
        message="CriterionCategoryChannelAvailability",
    )
    locale: MutableSequence["CriterionCategoryLocaleAvailability"] = (
        proto.RepeatedField(
            proto.MESSAGE,
            number=2,
            message="CriterionCategoryLocaleAvailability",
        )
    )


class CriterionCategoryChannelAvailability(proto.Message):
    r"""Information of advertising channel type and subtypes a
    category is available in.


    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        availability_mode (google.ads.googleads.v20.enums.types.CriterionCategoryChannelAvailabilityModeEnum.CriterionCategoryChannelAvailabilityMode):
            Format of the channel availability. Can be ALL_CHANNELS (the
            rest of the fields will not be set), CHANNEL_TYPE (only
            advertising_channel_type type will be set, the category is
            available to all sub types under it) or
            CHANNEL_TYPE_AND_SUBTYPES (advertising_channel_type,
            advertising_channel_sub_type, and
            include_default_channel_sub_type will all be set).
        advertising_channel_type (google.ads.googleads.v20.enums.types.AdvertisingChannelTypeEnum.AdvertisingChannelType):
            Channel type the category is available to.
        advertising_channel_sub_type (MutableSequence[google.ads.googleads.v20.enums.types.AdvertisingChannelSubTypeEnum.AdvertisingChannelSubType]):
            Channel subtypes under the channel type the
            category is available to.
        include_default_channel_sub_type (bool):
            Whether default channel sub type is included. For example,
            advertising_channel_type being DISPLAY and
            include_default_channel_sub_type being false means that the
            default display campaign where channel sub type is not set
            is not included in this availability configuration.

            This field is a member of `oneof`_ ``_include_default_channel_sub_type``.
    """

    availability_mode: (
        criterion_category_channel_availability_mode.CriterionCategoryChannelAvailabilityModeEnum.CriterionCategoryChannelAvailabilityMode
    ) = proto.Field(
        proto.ENUM,
        number=1,
        enum=criterion_category_channel_availability_mode.CriterionCategoryChannelAvailabilityModeEnum.CriterionCategoryChannelAvailabilityMode,
    )
    advertising_channel_type: (
        gage_advertising_channel_type.AdvertisingChannelTypeEnum.AdvertisingChannelType
    ) = proto.Field(
        proto.ENUM,
        number=2,
        enum=gage_advertising_channel_type.AdvertisingChannelTypeEnum.AdvertisingChannelType,
    )
    advertising_channel_sub_type: MutableSequence[
        gage_advertising_channel_sub_type.AdvertisingChannelSubTypeEnum.AdvertisingChannelSubType
    ] = proto.RepeatedField(
        proto.ENUM,
        number=3,
        enum=gage_advertising_channel_sub_type.AdvertisingChannelSubTypeEnum.AdvertisingChannelSubType,
    )
    include_default_channel_sub_type: bool = proto.Field(
        proto.BOOL,
        number=5,
        optional=True,
    )


class CriterionCategoryLocaleAvailability(proto.Message):
    r"""Information about which locales a category is available in.

    .. _oneof: https://proto-plus-python.readthedocs.io/en/stable/fields.html#oneofs-mutually-exclusive-fields

    Attributes:
        availability_mode (google.ads.googleads.v20.enums.types.CriterionCategoryLocaleAvailabilityModeEnum.CriterionCategoryLocaleAvailabilityMode):
            Format of the locale availability. Can be LAUNCHED_TO_ALL
            (both country and language will be empty), COUNTRY (only
            country will be set), LANGUAGE (only language wil be set),
            COUNTRY_AND_LANGUAGE (both country and language will be
            set).
        country_code (str):
            The ISO-3166-1 alpha-2 country code
            associated with the category.

            This field is a member of `oneof`_ ``_country_code``.
        language_code (str):
            ISO 639-1 code of the language associated
            with the category.

            This field is a member of `oneof`_ ``_language_code``.
    """

    availability_mode: (
        criterion_category_locale_availability_mode.CriterionCategoryLocaleAvailabilityModeEnum.CriterionCategoryLocaleAvailabilityMode
    ) = proto.Field(
        proto.ENUM,
        number=1,
        enum=criterion_category_locale_availability_mode.CriterionCategoryLocaleAvailabilityModeEnum.CriterionCategoryLocaleAvailabilityMode,
    )
    country_code: str = proto.Field(
        proto.STRING,
        number=4,
        optional=True,
    )
    language_code: str = proto.Field(
        proto.STRING,
        number=5,
        optional=True,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
