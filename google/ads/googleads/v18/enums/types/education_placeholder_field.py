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
        "EducationPlaceholderFieldEnum",
    },
)


class EducationPlaceholderFieldEnum(proto.Message):
    r"""Values for Education placeholder fields.
    For more information about dynamic remarketing feeds, see
    https://support.google.com/google-ads/answer/6053288.

    """

    class EducationPlaceholderField(proto.Enum):
        r"""Possible values for Education placeholder fields.

        Values:
            UNSPECIFIED (0):
                Not specified.
            UNKNOWN (1):
                Used for return value only. Represents value
                unknown in this version.
            PROGRAM_ID (2):
                Data Type: STRING. Required. Combination of
                PROGRAM ID and LOCATION ID must be unique per
                offer.
            LOCATION_ID (3):
                Data Type: STRING. Combination of PROGRAM ID
                and LOCATION ID must be unique per offer.
            PROGRAM_NAME (4):
                Data Type: STRING. Required. Main headline
                with program name to be shown in dynamic ad.
            AREA_OF_STUDY (5):
                Data Type: STRING. Area of study that can be
                shown in dynamic ad.
            PROGRAM_DESCRIPTION (6):
                Data Type: STRING. Description of program
                that can be shown in dynamic ad.
            SCHOOL_NAME (7):
                Data Type: STRING. Name of school that can be
                shown in dynamic ad.
            ADDRESS (8):
                Data Type: STRING. Complete school address,
                including postal code.
            THUMBNAIL_IMAGE_URL (9):
                Data Type: URL. Image to be displayed in ads.
            ALTERNATIVE_THUMBNAIL_IMAGE_URL (10):
                Data Type: URL. Alternative hosted file of
                image to be used in the ad.
            FINAL_URLS (11):
                Data Type: URL_LIST. Required. Final URLs to be used in ad
                when using Upgraded URLs; the more specific the better (for
                example, the individual URL of a specific program and its
                location).
            FINAL_MOBILE_URLS (12):
                Data Type: URL_LIST. Final mobile URLs for the ad when using
                Upgraded URLs.
            TRACKING_URL (13):
                Data Type: URL. Tracking template for the ad
                when using Upgraded URLs.
            CONTEXTUAL_KEYWORDS (14):
                Data Type: STRING_LIST. Keywords used for product retrieval.
            ANDROID_APP_LINK (15):
                Data Type: STRING. Android app link. Must be formatted as:
                android-app://{package_id}/{scheme}/{host_path}. The
                components are defined as follows: package_id: app ID as
                specified in Google Play. scheme: the scheme to pass to the
                application. Can be HTTP, or a custom scheme. host_path:
                identifies the specific content within your application.
            SIMILAR_PROGRAM_IDS (16):
                Data Type: STRING_LIST. List of recommended program IDs to
                show together with this item.
            IOS_APP_LINK (17):
                Data Type: STRING. iOS app link.
            IOS_APP_STORE_ID (18):
                Data Type: INT64. iOS app store ID.
        """

        UNSPECIFIED = 0
        UNKNOWN = 1
        PROGRAM_ID = 2
        LOCATION_ID = 3
        PROGRAM_NAME = 4
        AREA_OF_STUDY = 5
        PROGRAM_DESCRIPTION = 6
        SCHOOL_NAME = 7
        ADDRESS = 8
        THUMBNAIL_IMAGE_URL = 9
        ALTERNATIVE_THUMBNAIL_IMAGE_URL = 10
        FINAL_URLS = 11
        FINAL_MOBILE_URLS = 12
        TRACKING_URL = 13
        CONTEXTUAL_KEYWORDS = 14
        ANDROID_APP_LINK = 15
        SIMILAR_PROGRAM_IDS = 16
        IOS_APP_LINK = 17
        IOS_APP_STORE_ID = 18


__all__ = tuple(sorted(__protobuf__.manifest))
