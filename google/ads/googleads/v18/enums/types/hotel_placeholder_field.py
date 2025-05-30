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
        "HotelPlaceholderFieldEnum",
    },
)


class HotelPlaceholderFieldEnum(proto.Message):
    r"""Values for Hotel placeholder fields.
    For more information about dynamic remarketing feeds, see
    https://support.google.com/google-ads/answer/6053288.

    """

    class HotelPlaceholderField(proto.Enum):
        r"""Possible values for Hotel placeholder fields.

        Values:
            UNSPECIFIED (0):
                Not specified.
            UNKNOWN (1):
                Used for return value only. Represents value
                unknown in this version.
            PROPERTY_ID (2):
                Data Type: STRING. Required. Unique ID.
            PROPERTY_NAME (3):
                Data Type: STRING. Required. Main headline
                with property name to be shown in dynamic ad.
            DESTINATION_NAME (4):
                Data Type: STRING. Name of destination to be
                shown in dynamic ad.
            DESCRIPTION (5):
                Data Type: STRING. Description of destination
                to be shown in dynamic ad.
            ADDRESS (6):
                Data Type: STRING. Complete property address,
                including postal code.
            PRICE (7):
                Data Type: STRING. Price to be shown in the
                ad. Example: "100.00 USD".
            FORMATTED_PRICE (8):
                Data Type: STRING. Formatted price to be
                shown in the ad. Example: "Starting at $100.00
                USD", "$80 - $100".
            SALE_PRICE (9):
                Data Type: STRING. Sale price to be shown in
                the ad. Example: "80.00 USD".
            FORMATTED_SALE_PRICE (10):
                Data Type: STRING. Formatted sale price to be
                shown in the ad. Example: "On sale for $80.00",
                "$60 - $80".
            IMAGE_URL (11):
                Data Type: URL. Image to be displayed in the
                ad.
            CATEGORY (12):
                Data Type: STRING. Category of property used
                to group like items together for recommendation
                engine.
            STAR_RATING (13):
                Data Type: INT64. Star rating (1 to 5) used
                to group like items together for recommendation
                engine.
            CONTEXTUAL_KEYWORDS (14):
                Data Type: STRING_LIST. Keywords used for product retrieval.
            FINAL_URLS (15):
                Data Type: URL_LIST. Required. Final URLs for the ad when
                using Upgraded URLs. User will be redirected to these URLs
                when they click on an ad, or when they click on a specific
                flight for ads that show multiple flights.
            FINAL_MOBILE_URLS (16):
                Data Type: URL_LIST. Final mobile URLs for the ad when using
                Upgraded URLs.
            TRACKING_URL (17):
                Data Type: URL. Tracking template for the ad
                when using Upgraded URLs.
            ANDROID_APP_LINK (18):
                Data Type: STRING. Android app link. Must be formatted as:
                android-app://{package_id}/{scheme}/{host_path}. The
                components are defined as follows: package_id: app ID as
                specified in Google Play. scheme: the scheme to pass to the
                application. Can be HTTP, or a custom scheme. host_path:
                identifies the specific content within your application.
            SIMILAR_PROPERTY_IDS (19):
                Data Type: STRING_LIST. List of recommended property IDs to
                show together with this item.
            IOS_APP_LINK (20):
                Data Type: STRING. iOS app link.
            IOS_APP_STORE_ID (21):
                Data Type: INT64. iOS app store ID.
        """

        UNSPECIFIED = 0
        UNKNOWN = 1
        PROPERTY_ID = 2
        PROPERTY_NAME = 3
        DESTINATION_NAME = 4
        DESCRIPTION = 5
        ADDRESS = 6
        PRICE = 7
        FORMATTED_PRICE = 8
        SALE_PRICE = 9
        FORMATTED_SALE_PRICE = 10
        IMAGE_URL = 11
        CATEGORY = 12
        STAR_RATING = 13
        CONTEXTUAL_KEYWORDS = 14
        FINAL_URLS = 15
        FINAL_MOBILE_URLS = 16
        TRACKING_URL = 17
        ANDROID_APP_LINK = 18
        SIMILAR_PROPERTY_IDS = 19
        IOS_APP_LINK = 20
        IOS_APP_STORE_ID = 21


__all__ = tuple(sorted(__protobuf__.manifest))
