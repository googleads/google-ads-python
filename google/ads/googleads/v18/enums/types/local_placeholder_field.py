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
        "LocalPlaceholderFieldEnum",
    },
)


class LocalPlaceholderFieldEnum(proto.Message):
    r"""Values for Local placeholder fields.
    For more information about dynamic remarketing feeds, see
    https://support.google.com/google-ads/answer/6053288.

    """

    class LocalPlaceholderField(proto.Enum):
        r"""Possible values for Local placeholder fields.

        Values:
            UNSPECIFIED (0):
                Not specified.
            UNKNOWN (1):
                Used for return value only. Represents value
                unknown in this version.
            DEAL_ID (2):
                Data Type: STRING. Required. Unique ID.
            DEAL_NAME (3):
                Data Type: STRING. Required. Main headline
                with local deal title to be shown in dynamic ad.
            SUBTITLE (4):
                Data Type: STRING. Local deal subtitle to be
                shown in dynamic ad.
            DESCRIPTION (5):
                Data Type: STRING. Description of local deal
                to be shown in dynamic ad.
            PRICE (6):
                Data Type: STRING. Price to be shown in the
                ad. Highly recommended for dynamic ads. Example:
                "100.00 USD".
            FORMATTED_PRICE (7):
                Data Type: STRING. Formatted price to be
                shown in the ad. Example: "Starting at $100.00
                USD", "$80 - $100".
            SALE_PRICE (8):
                Data Type: STRING. Sale price to be shown in
                the ad. Example: "80.00 USD".
            FORMATTED_SALE_PRICE (9):
                Data Type: STRING. Formatted sale price to be
                shown in the ad. Example: "On sale for $80.00",
                "$60 - $80".
            IMAGE_URL (10):
                Data Type: URL. Image to be displayed in the
                ad.
            ADDRESS (11):
                Data Type: STRING. Complete property address,
                including postal code.
            CATEGORY (12):
                Data Type: STRING. Category of local deal
                used to group like items together for
                recommendation engine.
            CONTEXTUAL_KEYWORDS (13):
                Data Type: STRING_LIST. Keywords used for product retrieval.
            FINAL_URLS (14):
                Data Type: URL_LIST. Required. Final URLs to be used in ad
                when using Upgraded URLs; the more specific the better (for
                example, the individual URL of a specific local deal and its
                location).
            FINAL_MOBILE_URLS (15):
                Data Type: URL_LIST. Final mobile URLs for the ad when using
                Upgraded URLs.
            TRACKING_URL (16):
                Data Type: URL. Tracking template for the ad
                when using Upgraded URLs.
            ANDROID_APP_LINK (17):
                Data Type: STRING. Android app link. Must be formatted as:
                android-app://{package_id}/{scheme}/{host_path}. The
                components are defined as follows: package_id: app ID as
                specified in Google Play. scheme: the scheme to pass to the
                application. Can be HTTP, or a custom scheme. host_path:
                identifies the specific content within your application.
            SIMILAR_DEAL_IDS (18):
                Data Type: STRING_LIST. List of recommended local deal IDs
                to show together with this item.
            IOS_APP_LINK (19):
                Data Type: STRING. iOS app link.
            IOS_APP_STORE_ID (20):
                Data Type: INT64. iOS app store ID.
        """

        UNSPECIFIED = 0
        UNKNOWN = 1
        DEAL_ID = 2
        DEAL_NAME = 3
        SUBTITLE = 4
        DESCRIPTION = 5
        PRICE = 6
        FORMATTED_PRICE = 7
        SALE_PRICE = 8
        FORMATTED_SALE_PRICE = 9
        IMAGE_URL = 10
        ADDRESS = 11
        CATEGORY = 12
        CONTEXTUAL_KEYWORDS = 13
        FINAL_URLS = 14
        FINAL_MOBILE_URLS = 15
        TRACKING_URL = 16
        ANDROID_APP_LINK = 17
        SIMILAR_DEAL_IDS = 18
        IOS_APP_LINK = 19
        IOS_APP_STORE_ID = 20


__all__ = tuple(sorted(__protobuf__.manifest))
