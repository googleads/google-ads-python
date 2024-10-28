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
        "PricePlaceholderFieldEnum",
    },
)


class PricePlaceholderFieldEnum(proto.Message):
    r"""Values for Price placeholder fields."""

    class PricePlaceholderField(proto.Enum):
        r"""Possible values for Price placeholder fields.

        Values:
            UNSPECIFIED (0):
                Not specified.
            UNKNOWN (1):
                Used for return value only. Represents value
                unknown in this version.
            TYPE (2):
                Data Type: STRING. The type of your price
                feed. Must match one of the predefined price
                feed type exactly.
            PRICE_QUALIFIER (3):
                Data Type: STRING. The qualifier of each
                price. Must match one of the predefined price
                qualifiers exactly.
            TRACKING_TEMPLATE (4):
                Data Type: URL. Tracking template for the
                price feed when using Upgraded URLs.
            LANGUAGE (5):
                Data Type: STRING. Language of the price
                feed. Must match one of the available available
                locale codes exactly.
            FINAL_URL_SUFFIX (6):
                Data Type: STRING. Final URL suffix for the
                price feed when using parallel tracking.
            ITEM_1_HEADER (100):
                Data Type: STRING. The header of item 1 of
                the table.
            ITEM_1_DESCRIPTION (101):
                Data Type: STRING. The description of item 1
                of the table.
            ITEM_1_PRICE (102):
                Data Type: MONEY. The price (money with
                currency) of item 1 of the table, for example,
                30 USD. The currency must match one of the
                available currencies.
            ITEM_1_UNIT (103):
                Data Type: STRING. The price unit of item 1
                of the table. Must match one of the predefined
                price units.
            ITEM_1_FINAL_URLS (104):
                Data Type: URL_LIST. The final URLs of item 1 of the table
                when using Upgraded URLs.
            ITEM_1_FINAL_MOBILE_URLS (105):
                Data Type: URL_LIST. The final mobile URLs of item 1 of the
                table when using Upgraded URLs.
            ITEM_2_HEADER (200):
                Data Type: STRING. The header of item 2 of
                the table.
            ITEM_2_DESCRIPTION (201):
                Data Type: STRING. The description of item 2
                of the table.
            ITEM_2_PRICE (202):
                Data Type: MONEY. The price (money with
                currency) of item 2 of the table, for example,
                30 USD. The currency must match one of the
                available currencies.
            ITEM_2_UNIT (203):
                Data Type: STRING. The price unit of item 2
                of the table. Must match one of the predefined
                price units.
            ITEM_2_FINAL_URLS (204):
                Data Type: URL_LIST. The final URLs of item 2 of the table
                when using Upgraded URLs.
            ITEM_2_FINAL_MOBILE_URLS (205):
                Data Type: URL_LIST. The final mobile URLs of item 2 of the
                table when using Upgraded URLs.
            ITEM_3_HEADER (300):
                Data Type: STRING. The header of item 3 of
                the table.
            ITEM_3_DESCRIPTION (301):
                Data Type: STRING. The description of item 3
                of the table.
            ITEM_3_PRICE (302):
                Data Type: MONEY. The price (money with
                currency) of item 3 of the table, for example,
                30 USD. The currency must match one of the
                available currencies.
            ITEM_3_UNIT (303):
                Data Type: STRING. The price unit of item 3
                of the table. Must match one of the predefined
                price units.
            ITEM_3_FINAL_URLS (304):
                Data Type: URL_LIST. The final URLs of item 3 of the table
                when using Upgraded URLs.
            ITEM_3_FINAL_MOBILE_URLS (305):
                Data Type: URL_LIST. The final mobile URLs of item 3 of the
                table when using Upgraded URLs.
            ITEM_4_HEADER (400):
                Data Type: STRING. The header of item 4 of
                the table.
            ITEM_4_DESCRIPTION (401):
                Data Type: STRING. The description of item 4
                of the table.
            ITEM_4_PRICE (402):
                Data Type: MONEY. The price (money with
                currency) of item 4 of the table, for example,
                30 USD. The currency must match one of the
                available currencies.
            ITEM_4_UNIT (403):
                Data Type: STRING. The price unit of item 4
                of the table. Must match one of the predefined
                price units.
            ITEM_4_FINAL_URLS (404):
                Data Type: URL_LIST. The final URLs of item 4 of the table
                when using Upgraded URLs.
            ITEM_4_FINAL_MOBILE_URLS (405):
                Data Type: URL_LIST. The final mobile URLs of item 4 of the
                table when using Upgraded URLs.
            ITEM_5_HEADER (500):
                Data Type: STRING. The header of item 5 of
                the table.
            ITEM_5_DESCRIPTION (501):
                Data Type: STRING. The description of item 5
                of the table.
            ITEM_5_PRICE (502):
                Data Type: MONEY. The price (money with
                currency) of item 5 of the table, for example,
                30 USD. The currency must match one of the
                available currencies.
            ITEM_5_UNIT (503):
                Data Type: STRING. The price unit of item 5
                of the table. Must match one of the predefined
                price units.
            ITEM_5_FINAL_URLS (504):
                Data Type: URL_LIST. The final URLs of item 5 of the table
                when using Upgraded URLs.
            ITEM_5_FINAL_MOBILE_URLS (505):
                Data Type: URL_LIST. The final mobile URLs of item 5 of the
                table when using Upgraded URLs.
            ITEM_6_HEADER (600):
                Data Type: STRING. The header of item 6 of
                the table.
            ITEM_6_DESCRIPTION (601):
                Data Type: STRING. The description of item 6
                of the table.
            ITEM_6_PRICE (602):
                Data Type: MONEY. The price (money with
                currency) of item 6 of the table, for example,
                30 USD. The currency must match one of the
                available currencies.
            ITEM_6_UNIT (603):
                Data Type: STRING. The price unit of item 6
                of the table. Must match one of the predefined
                price units.
            ITEM_6_FINAL_URLS (604):
                Data Type: URL_LIST. The final URLs of item 6 of the table
                when using Upgraded URLs.
            ITEM_6_FINAL_MOBILE_URLS (605):
                Data Type: URL_LIST. The final mobile URLs of item 6 of the
                table when using Upgraded URLs.
            ITEM_7_HEADER (700):
                Data Type: STRING. The header of item 7 of
                the table.
            ITEM_7_DESCRIPTION (701):
                Data Type: STRING. The description of item 7
                of the table.
            ITEM_7_PRICE (702):
                Data Type: MONEY. The price (money with
                currency) of item 7 of the table, for example,
                30 USD. The currency must match one of the
                available currencies.
            ITEM_7_UNIT (703):
                Data Type: STRING. The price unit of item 7
                of the table. Must match one of the predefined
                price units.
            ITEM_7_FINAL_URLS (704):
                Data Type: URL_LIST. The final URLs of item 7 of the table
                when using Upgraded URLs.
            ITEM_7_FINAL_MOBILE_URLS (705):
                Data Type: URL_LIST. The final mobile URLs of item 7 of the
                table when using Upgraded URLs.
            ITEM_8_HEADER (800):
                Data Type: STRING. The header of item 8 of
                the table.
            ITEM_8_DESCRIPTION (801):
                Data Type: STRING. The description of item 8
                of the table.
            ITEM_8_PRICE (802):
                Data Type: MONEY. The price (money with
                currency) of item 8 of the table, for example,
                30 USD. The currency must match one of the
                available currencies.
            ITEM_8_UNIT (803):
                Data Type: STRING. The price unit of item 8
                of the table. Must match one of the predefined
                price units.
            ITEM_8_FINAL_URLS (804):
                Data Type: URL_LIST. The final URLs of item 8 of the table
                when using Upgraded URLs.
            ITEM_8_FINAL_MOBILE_URLS (805):
                Data Type: URL_LIST. The final mobile URLs of item 8 of the
                table when using Upgraded URLs.
        """

        UNSPECIFIED = 0
        UNKNOWN = 1
        TYPE = 2
        PRICE_QUALIFIER = 3
        TRACKING_TEMPLATE = 4
        LANGUAGE = 5
        FINAL_URL_SUFFIX = 6
        ITEM_1_HEADER = 100
        ITEM_1_DESCRIPTION = 101
        ITEM_1_PRICE = 102
        ITEM_1_UNIT = 103
        ITEM_1_FINAL_URLS = 104
        ITEM_1_FINAL_MOBILE_URLS = 105
        ITEM_2_HEADER = 200
        ITEM_2_DESCRIPTION = 201
        ITEM_2_PRICE = 202
        ITEM_2_UNIT = 203
        ITEM_2_FINAL_URLS = 204
        ITEM_2_FINAL_MOBILE_URLS = 205
        ITEM_3_HEADER = 300
        ITEM_3_DESCRIPTION = 301
        ITEM_3_PRICE = 302
        ITEM_3_UNIT = 303
        ITEM_3_FINAL_URLS = 304
        ITEM_3_FINAL_MOBILE_URLS = 305
        ITEM_4_HEADER = 400
        ITEM_4_DESCRIPTION = 401
        ITEM_4_PRICE = 402
        ITEM_4_UNIT = 403
        ITEM_4_FINAL_URLS = 404
        ITEM_4_FINAL_MOBILE_URLS = 405
        ITEM_5_HEADER = 500
        ITEM_5_DESCRIPTION = 501
        ITEM_5_PRICE = 502
        ITEM_5_UNIT = 503
        ITEM_5_FINAL_URLS = 504
        ITEM_5_FINAL_MOBILE_URLS = 505
        ITEM_6_HEADER = 600
        ITEM_6_DESCRIPTION = 601
        ITEM_6_PRICE = 602
        ITEM_6_UNIT = 603
        ITEM_6_FINAL_URLS = 604
        ITEM_6_FINAL_MOBILE_URLS = 605
        ITEM_7_HEADER = 700
        ITEM_7_DESCRIPTION = 701
        ITEM_7_PRICE = 702
        ITEM_7_UNIT = 703
        ITEM_7_FINAL_URLS = 704
        ITEM_7_FINAL_MOBILE_URLS = 705
        ITEM_8_HEADER = 800
        ITEM_8_DESCRIPTION = 801
        ITEM_8_PRICE = 802
        ITEM_8_UNIT = 803
        ITEM_8_FINAL_URLS = 804
        ITEM_8_FINAL_MOBILE_URLS = 805


__all__ = tuple(sorted(__protobuf__.manifest))
