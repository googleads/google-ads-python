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
        "RealEstatePlaceholderFieldEnum",
    },
)


class RealEstatePlaceholderFieldEnum(proto.Message):
    r"""Values for Real Estate placeholder fields.
    For more information about dynamic remarketing feeds, see
    https://support.google.com/google-ads/answer/6053288.

    """

    class RealEstatePlaceholderField(proto.Enum):
        r"""Possible values for Real Estate placeholder fields.

        Values:
            UNSPECIFIED (0):
                Not specified.
            UNKNOWN (1):
                Used for return value only. Represents value
                unknown in this version.
            LISTING_ID (2):
                Data Type: STRING. Unique ID.
            LISTING_NAME (3):
                Data Type: STRING. Main headline with listing
                name to be shown in dynamic ad.
            CITY_NAME (4):
                Data Type: STRING. City name to be shown in
                dynamic ad.
            DESCRIPTION (5):
                Data Type: STRING. Description of listing to
                be shown in dynamic ad.
            ADDRESS (6):
                Data Type: STRING. Complete listing address,
                including postal code.
            PRICE (7):
                Data Type: STRING. Price to be shown in the
                ad. Example: "100.00 USD".
            FORMATTED_PRICE (8):
                Data Type: STRING. Formatted price to be
                shown in the ad. Example: "Starting at $100.00
                USD", "$80 - $100".
            IMAGE_URL (9):
                Data Type: URL. Image to be displayed in the
                ad.
            PROPERTY_TYPE (10):
                Data Type: STRING. Type of property (house,
                condo, apartment, etc.) used to group like items
                together for recommendation engine.
            LISTING_TYPE (11):
                Data Type: STRING. Type of listing (resale,
                rental, foreclosure, etc.) used to group like
                items together for recommendation engine.
            CONTEXTUAL_KEYWORDS (12):
                Data Type: STRING_LIST. Keywords used for product retrieval.
            FINAL_URLS (13):
                Data Type: URL_LIST. Final URLs to be used in ad when using
                Upgraded URLs; the more specific the better (for example,
                the individual URL of a specific listing and its location).
            FINAL_MOBILE_URLS (14):
                Data Type: URL_LIST. Final mobile URLs for the ad when using
                Upgraded URLs.
            TRACKING_URL (15):
                Data Type: URL. Tracking template for the ad
                when using Upgraded URLs.
            ANDROID_APP_LINK (16):
                Data Type: STRING. Android app link. Must be formatted as:
                android-app://{package_id}/{scheme}/{host_path}. The
                components are defined as follows: package_id: app ID as
                specified in Google Play. scheme: the scheme to pass to the
                application. Can be HTTP, or a custom scheme. host_path:
                identifies the specific content within your application.
            SIMILAR_LISTING_IDS (17):
                Data Type: STRING_LIST. List of recommended listing IDs to
                show together with this item.
            IOS_APP_LINK (18):
                Data Type: STRING. iOS app link.
            IOS_APP_STORE_ID (19):
                Data Type: INT64. iOS app store ID.
        """

        UNSPECIFIED = 0
        UNKNOWN = 1
        LISTING_ID = 2
        LISTING_NAME = 3
        CITY_NAME = 4
        DESCRIPTION = 5
        ADDRESS = 6
        PRICE = 7
        FORMATTED_PRICE = 8
        IMAGE_URL = 9
        PROPERTY_TYPE = 10
        LISTING_TYPE = 11
        CONTEXTUAL_KEYWORDS = 12
        FINAL_URLS = 13
        FINAL_MOBILE_URLS = 14
        TRACKING_URL = 15
        ANDROID_APP_LINK = 16
        SIMILAR_LISTING_IDS = 17
        IOS_APP_LINK = 18
        IOS_APP_STORE_ID = 19


__all__ = tuple(sorted(__protobuf__.manifest))
