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
        "PlaceholderTypeEnum",
    },
)


class PlaceholderTypeEnum(proto.Message):
    r"""Container for enum describing possible placeholder types for
    a feed mapping.

    """

    class PlaceholderType(proto.Enum):
        r"""Possible placeholder types for a feed mapping.

        Values:
            UNSPECIFIED (0):
                Not specified.
            UNKNOWN (1):
                Used for return value only. Represents value
                unknown in this version.
            SITELINK (2):
                Lets you show links in your ad to pages from
                your website, including the main landing page.
            CALL (3):
                Lets you attach a phone number to an ad,
                allowing customers to call directly from the ad.
            APP (4):
                Lets you provide users with a link that
                points to a mobile app in addition to a website.
            LOCATION (5):
                Lets you show locations of businesses from
                your Business Profile in your ad. This helps
                people find your locations by showing your ads
                with your address, a map to your location, or
                the distance to your business. This extension
                type is useful to draw customers to your
                brick-and-mortar location.
            AFFILIATE_LOCATION (6):
                If you sell your product through retail
                chains, affiliate location extensions let you
                show nearby stores that carry your products.
            CALLOUT (7):
                Lets you include additional text with your
                search ads that provide detailed information
                about your business, including products and
                services you offer. Callouts appear in ads at
                the top and bottom of Google search results.
            STRUCTURED_SNIPPET (8):
                Lets you add more info to your ad, specific
                to some predefined categories such as types,
                brands, styles, etc. A minimum of 3 text
                (SNIPPETS) values are required.
            MESSAGE (9):
                Allows users to see your ad, click an icon,
                and contact you directly by text message. With
                one tap on your ad, people can contact you to
                book an appointment, get a quote, ask for
                information, or request a service.
            PRICE (10):
                Lets you display prices for a list of items
                along with your ads. A price feed is composed of
                three to eight price table rows.
            PROMOTION (11):
                Lets you highlight sales and other promotions
                that let users see how they can save by buying
                now.
            AD_CUSTOMIZER (12):
                Lets you dynamically inject custom data into
                the title and description of your ads.
            DYNAMIC_EDUCATION (13):
                Indicates that this feed is for education
                dynamic remarketing.
            DYNAMIC_FLIGHT (14):
                Indicates that this feed is for flight
                dynamic remarketing.
            DYNAMIC_CUSTOM (15):
                Indicates that this feed is for a custom
                dynamic remarketing type. Use this only if the
                other business types don't apply to your
                products or services.
            DYNAMIC_HOTEL (16):
                Indicates that this feed is for hotels and
                rentals dynamic remarketing.
            DYNAMIC_REAL_ESTATE (17):
                Indicates that this feed is for real estate
                dynamic remarketing.
            DYNAMIC_TRAVEL (18):
                Indicates that this feed is for travel
                dynamic remarketing.
            DYNAMIC_LOCAL (19):
                Indicates that this feed is for local deals
                dynamic remarketing.
            DYNAMIC_JOB (20):
                Indicates that this feed is for job dynamic
                remarketing.
            IMAGE (21):
                Lets you attach an image to an ad.
        """

        UNSPECIFIED = 0
        UNKNOWN = 1
        SITELINK = 2
        CALL = 3
        APP = 4
        LOCATION = 5
        AFFILIATE_LOCATION = 6
        CALLOUT = 7
        STRUCTURED_SNIPPET = 8
        MESSAGE = 9
        PRICE = 10
        PROMOTION = 11
        AD_CUSTOMIZER = 12
        DYNAMIC_EDUCATION = 13
        DYNAMIC_FLIGHT = 14
        DYNAMIC_CUSTOM = 15
        DYNAMIC_HOTEL = 16
        DYNAMIC_REAL_ESTATE = 17
        DYNAMIC_TRAVEL = 18
        DYNAMIC_LOCAL = 19
        DYNAMIC_JOB = 20
        IMAGE = 21


__all__ = tuple(sorted(__protobuf__.manifest))
