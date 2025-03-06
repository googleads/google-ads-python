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
        "JobPlaceholderFieldEnum",
    },
)


class JobPlaceholderFieldEnum(proto.Message):
    r"""Values for Job placeholder fields.
    For more information about dynamic remarketing feeds, see
    https://support.google.com/google-ads/answer/6053288.

    """

    class JobPlaceholderField(proto.Enum):
        r"""Possible values for Job placeholder fields.

        Values:
            UNSPECIFIED (0):
                Not specified.
            UNKNOWN (1):
                Used for return value only. Represents value
                unknown in this version.
            JOB_ID (2):
                Data Type: STRING. Required. If only JOB_ID is specified,
                then it must be unique. If both JOB_ID and LOCATION_ID are
                specified, then the pair must be unique. ID) pair must be
                unique.
            LOCATION_ID (3):
                Data Type: STRING. Combination of JOB_ID and LOCATION_ID
                must be unique per offer.
            TITLE (4):
                Data Type: STRING. Required. Main headline
                with job title to be shown in dynamic ad.
            SUBTITLE (5):
                Data Type: STRING. Job subtitle to be shown
                in dynamic ad.
            DESCRIPTION (6):
                Data Type: STRING. Description of job to be
                shown in dynamic ad.
            IMAGE_URL (7):
                Data Type: URL. Image to be displayed in the
                ad. Highly recommended for image ads.
            CATEGORY (8):
                Data Type: STRING. Category of property used
                to group like items together for recommendation
                engine.
            CONTEXTUAL_KEYWORDS (9):
                Data Type: STRING_LIST. Keywords used for product retrieval.
            ADDRESS (10):
                Data Type: STRING. Complete property address,
                including postal code.
            SALARY (11):
                Data Type: STRING. Salary or salary range of
                job to be shown in dynamic ad.
            FINAL_URLS (12):
                Data Type: URL_LIST. Required. Final URLs to be used in ad
                when using Upgraded URLs; the more specific the better (for
                example, the individual URL of a specific job and its
                location).
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
            SIMILAR_JOB_IDS (17):
                Data Type: STRING_LIST. List of recommended job IDs to show
                together with this item.
            IOS_APP_LINK (18):
                Data Type: STRING. iOS app link.
            IOS_APP_STORE_ID (19):
                Data Type: INT64. iOS app store ID.
        """

        UNSPECIFIED = 0
        UNKNOWN = 1
        JOB_ID = 2
        LOCATION_ID = 3
        TITLE = 4
        SUBTITLE = 5
        DESCRIPTION = 6
        IMAGE_URL = 7
        CATEGORY = 8
        CONTEXTUAL_KEYWORDS = 9
        ADDRESS = 10
        SALARY = 11
        FINAL_URLS = 12
        FINAL_MOBILE_URLS = 14
        TRACKING_URL = 15
        ANDROID_APP_LINK = 16
        SIMILAR_JOB_IDS = 17
        IOS_APP_LINK = 18
        IOS_APP_STORE_ID = 19


__all__ = tuple(sorted(__protobuf__.manifest))
