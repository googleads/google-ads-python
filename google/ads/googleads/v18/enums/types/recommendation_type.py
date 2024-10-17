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
    manifest={"RecommendationTypeEnum",},
)


class RecommendationTypeEnum(proto.Message):
    r"""Container for enum describing types of recommendations.
    """

    class RecommendationType(proto.Enum):
        r"""Types of recommendations."""
        UNSPECIFIED = 0
        UNKNOWN = 1
        CAMPAIGN_BUDGET = 2
        KEYWORD = 3
        TEXT_AD = 4
        TARGET_CPA_OPT_IN = 5
        MAXIMIZE_CONVERSIONS_OPT_IN = 6
        ENHANCED_CPC_OPT_IN = 7
        SEARCH_PARTNERS_OPT_IN = 8
        MAXIMIZE_CLICKS_OPT_IN = 9
        OPTIMIZE_AD_ROTATION = 10
        KEYWORD_MATCH_TYPE = 14
        MOVE_UNUSED_BUDGET = 15
        FORECASTING_CAMPAIGN_BUDGET = 16
        TARGET_ROAS_OPT_IN = 17
        RESPONSIVE_SEARCH_AD = 18
        MARGINAL_ROI_CAMPAIGN_BUDGET = 19
        USE_BROAD_MATCH_KEYWORD = 20
        RESPONSIVE_SEARCH_AD_ASSET = 21
        UPGRADE_SMART_SHOPPING_CAMPAIGN_TO_PERFORMANCE_MAX = 22
        RESPONSIVE_SEARCH_AD_IMPROVE_AD_STRENGTH = 23
        DISPLAY_EXPANSION_OPT_IN = 24
        UPGRADE_LOCAL_CAMPAIGN_TO_PERFORMANCE_MAX = 25
        RAISE_TARGET_CPA_BID_TOO_LOW = 26
        FORECASTING_SET_TARGET_ROAS = 27
        CALLOUT_ASSET = 28
        SITELINK_ASSET = 29
        CALL_ASSET = 30
        SHOPPING_ADD_AGE_GROUP = 31
        SHOPPING_ADD_COLOR = 32
        SHOPPING_ADD_GENDER = 33
        SHOPPING_ADD_GTIN = 34
        SHOPPING_ADD_MORE_IDENTIFIERS = 35
        SHOPPING_ADD_SIZE = 36
        SHOPPING_ADD_PRODUCTS_TO_CAMPAIGN = 37
        SHOPPING_FIX_DISAPPROVED_PRODUCTS = 38
        SHOPPING_TARGET_ALL_OFFERS = 39
        SHOPPING_FIX_SUSPENDED_MERCHANT_CENTER_ACCOUNT = 40
        SHOPPING_FIX_MERCHANT_CENTER_ACCOUNT_SUSPENSION_WARNING = 41
        SHOPPING_MIGRATE_REGULAR_SHOPPING_CAMPAIGN_OFFERS_TO_PERFORMANCE_MAX = (
            42
        )
        DYNAMIC_IMAGE_EXTENSION_OPT_IN = 43
        RAISE_TARGET_CPA = 44
        LOWER_TARGET_ROAS = 45
        PERFORMANCE_MAX_OPT_IN = 46
        IMPROVE_PERFORMANCE_MAX_AD_STRENGTH = 47
        MIGRATE_DYNAMIC_SEARCH_ADS_CAMPAIGN_TO_PERFORMANCE_MAX = 48
        FORECASTING_SET_TARGET_CPA = 49
        SET_TARGET_CPA = 50
        SET_TARGET_ROAS = 51
        MAXIMIZE_CONVERSION_VALUE_OPT_IN = 52
        IMPROVE_GOOGLE_TAG_COVERAGE = 53
        PERFORMANCE_MAX_FINAL_URL_OPT_IN = 54
        REFRESH_CUSTOMER_MATCH_LIST = 55
        CUSTOM_AUDIENCE_OPT_IN = 56
        LEAD_FORM_ASSET = 57
        IMPROVE_DEMAND_GEN_AD_STRENGTH = 58


__all__ = tuple(sorted(__protobuf__.manifest))
