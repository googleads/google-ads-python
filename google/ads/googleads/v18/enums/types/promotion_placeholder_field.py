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
    manifest={
        "PromotionPlaceholderFieldEnum",
    },
)


class PromotionPlaceholderFieldEnum(proto.Message):
    r"""Values for Promotion placeholder fields."""

    class PromotionPlaceholderField(proto.Enum):
        r"""Possible values for Promotion placeholder fields.

        Values:
            UNSPECIFIED (0):
                Not specified.
            UNKNOWN (1):
                Used for return value only. Represents value
                unknown in this version.
            PROMOTION_TARGET (2):
                Data Type: STRING. The text that appears on
                the ad when the extension is shown.
            DISCOUNT_MODIFIER (3):
                Data Type: STRING. Lets you add "up to"
                phrase to the promotion, in case you have
                variable promotion rates.
            PERCENT_OFF (4):
                Data Type: INT64. Takes a value in micros,
                where 1 million micros represents 1%, and is
                shown as a percentage when rendered.
            MONEY_AMOUNT_OFF (5):
                Data Type: MONEY. Requires a currency and an
                amount of money.
            PROMOTION_CODE (6):
                Data Type: STRING. A string that the user
                enters to get the discount.
            ORDERS_OVER_AMOUNT (7):
                Data Type: MONEY. A minimum spend before the
                user qualifies for the promotion.
            PROMOTION_START (8):
                Data Type: DATE. The start date of the
                promotion.
            PROMOTION_END (9):
                Data Type: DATE. The end date of the
                promotion.
            OCCASION (10):
                Data Type: STRING. Describes the associated event for the
                promotion using one of the PromotionExtensionOccasion enum
                values, for example NEW_YEARS.
            FINAL_URLS (11):
                Data Type: URL_LIST. Final URLs to be used in the ad when
                using Upgraded URLs.
            FINAL_MOBILE_URLS (12):
                Data Type: URL_LIST. Final mobile URLs for the ad when using
                Upgraded URLs.
            TRACKING_URL (13):
                Data Type: URL. Tracking template for the ad
                when using Upgraded URLs.
            LANGUAGE (14):
                Data Type: STRING. A string represented by a
                language code for the promotion.
            FINAL_URL_SUFFIX (15):
                Data Type: STRING. Final URL suffix for the
                ad when using parallel tracking.
        """

        UNSPECIFIED = 0
        UNKNOWN = 1
        PROMOTION_TARGET = 2
        DISCOUNT_MODIFIER = 3
        PERCENT_OFF = 4
        MONEY_AMOUNT_OFF = 5
        PROMOTION_CODE = 6
        ORDERS_OVER_AMOUNT = 7
        PROMOTION_START = 8
        PROMOTION_END = 9
        OCCASION = 10
        FINAL_URLS = 11
        FINAL_MOBILE_URLS = 12
        TRACKING_URL = 13
        LANGUAGE = 14
        FINAL_URL_SUFFIX = 15


__all__ = tuple(sorted(__protobuf__.manifest))
