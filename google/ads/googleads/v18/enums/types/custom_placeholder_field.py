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
        "CustomPlaceholderFieldEnum",
    },
)


class CustomPlaceholderFieldEnum(proto.Message):
    r"""Values for Custom placeholder fields.
    For more information about dynamic remarketing feeds, see
    https://support.google.com/google-ads/answer/6053288.

    """

    class CustomPlaceholderField(proto.Enum):
        r"""Possible values for Custom placeholder fields.

        Values:
            UNSPECIFIED (0):
                Not specified.
            UNKNOWN (1):
                Used for return value only. Represents value
                unknown in this version.
            ID (2):
                Data Type: STRING. Required. Combination ID
                and ID2 must be unique per offer.
            ID2 (3):
                Data Type: STRING. Combination ID and ID2
                must be unique per offer.
            ITEM_TITLE (4):
                Data Type: STRING. Required. Main headline
                with product name to be shown in dynamic ad.
            ITEM_SUBTITLE (5):
                Data Type: STRING. Optional text to be shown
                in the image ad.
            ITEM_DESCRIPTION (6):
                Data Type: STRING. Optional description of
                the product to be shown in the ad.
            ITEM_ADDRESS (7):
                Data Type: STRING. Full address of your offer
                or service, including postal code. This will be
                used to identify the closest product to the user
                when there are multiple offers in the feed that
                are relevant to the user.
            PRICE (8):
                Data Type: STRING. Price to be shown in the
                ad. Example: "100.00 USD".
            FORMATTED_PRICE (9):
                Data Type: STRING. Formatted price to be
                shown in the ad. Example: "Starting at $100.00
                USD", "$80 - $100".
            SALE_PRICE (10):
                Data Type: STRING. Sale price to be shown in
                the ad. Example: "80.00 USD".
            FORMATTED_SALE_PRICE (11):
                Data Type: STRING. Formatted sale price to be
                shown in the ad. Example: "On sale for $80.00",
                "$60 - $80".
            IMAGE_URL (12):
                Data Type: URL. Image to be displayed in the
                ad. Highly recommended for image ads.
            ITEM_CATEGORY (13):
                Data Type: STRING. Used as a recommendation
                engine signal to serve items in the same
                category.
            FINAL_URLS (14):
                Data Type: URL_LIST. Final URLs for the ad when using
                Upgraded URLs. User will be redirected to these URLs when
                they click on an ad, or when they click on a specific
                product for ads that have multiple products.
            FINAL_MOBILE_URLS (15):
                Data Type: URL_LIST. Final mobile URLs for the ad when using
                Upgraded URLs.
            TRACKING_URL (16):
                Data Type: URL. Tracking template for the ad
                when using Upgraded URLs.
            CONTEXTUAL_KEYWORDS (17):
                Data Type: STRING_LIST. Keywords used for product retrieval.
            ANDROID_APP_LINK (18):
                Data Type: STRING. Android app link. Must be formatted as:
                android-app://{package_id}/{scheme}/{host_path}. The
                components are defined as follows: package_id: app ID as
                specified in Google Play. scheme: the scheme to pass to the
                application. Can be HTTP, or a custom scheme. host_path:
                identifies the specific content within your application.
            SIMILAR_IDS (19):
                Data Type: STRING_LIST. List of recommended IDs to show
                together with this item.
            IOS_APP_LINK (20):
                Data Type: STRING. iOS app link.
            IOS_APP_STORE_ID (21):
                Data Type: INT64. iOS app store ID.
        """

        UNSPECIFIED = 0
        UNKNOWN = 1
        ID = 2
        ID2 = 3
        ITEM_TITLE = 4
        ITEM_SUBTITLE = 5
        ITEM_DESCRIPTION = 6
        ITEM_ADDRESS = 7
        PRICE = 8
        FORMATTED_PRICE = 9
        SALE_PRICE = 10
        FORMATTED_SALE_PRICE = 11
        IMAGE_URL = 12
        ITEM_CATEGORY = 13
        FINAL_URLS = 14
        FINAL_MOBILE_URLS = 15
        TRACKING_URL = 16
        CONTEXTUAL_KEYWORDS = 17
        ANDROID_APP_LINK = 18
        SIMILAR_IDS = 19
        IOS_APP_LINK = 20
        IOS_APP_STORE_ID = 21


__all__ = tuple(sorted(__protobuf__.manifest))
