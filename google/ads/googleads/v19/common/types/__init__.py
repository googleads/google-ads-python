# -*- coding: utf-8 -*-
# Copyright 2025 Google LLC
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
from .ad_asset import (
    AdAppDeepLinkAsset,
    AdCallToActionAsset,
    AdDemandGenCarouselCardAsset,
    AdImageAsset,
    AdMediaBundleAsset,
    AdTextAsset,
    AdVideoAsset,
    AdVideoAssetInfo,
    AdVideoAssetInventoryPreferences,
)
from .ad_type_infos import (
    AppAdInfo,
    AppEngagementAdInfo,
    AppPreRegistrationAdInfo,
    CallAdInfo,
    DemandGenCarouselAdInfo,
    DemandGenMultiAssetAdInfo,
    DemandGenProductAdInfo,
    DemandGenVideoResponsiveAdInfo,
    DisplayUploadAdInfo,
    ExpandedDynamicSearchAdInfo,
    ExpandedTextAdInfo,
    HotelAdInfo,
    ImageAdInfo,
    InFeedVideoAdInfo,
    LegacyAppInstallAdInfo,
    LegacyResponsiveDisplayAdInfo,
    LocalAdInfo,
    ResponsiveDisplayAdControlSpec,
    ResponsiveDisplayAdInfo,
    ResponsiveSearchAdInfo,
    ShoppingComparisonListingAdInfo,
    ShoppingProductAdInfo,
    ShoppingSmartAdInfo,
    SmartCampaignAdInfo,
    TextAdInfo,
    TravelAdInfo,
    VideoAdInfo,
    VideoBumperInStreamAdInfo,
    VideoNonSkippableInStreamAdInfo,
    VideoOutstreamAdInfo,
    VideoResponsiveAdInfo,
    VideoTrueViewInStreamAdInfo,
    YouTubeAudioAdInfo,
)
from .asset_policy import (
    AdAssetPolicySummary,
    AssetDisapproved,
    AssetLinkPrimaryStatusDetails,
)
from .asset_set_types import (
    BusinessProfileBusinessNameFilter,
    BusinessProfileLocationGroup,
    BusinessProfileLocationSet,
    ChainFilter,
    ChainLocationGroup,
    ChainSet,
    DynamicBusinessProfileLocationGroupFilter,
    LocationSet,
    MapsLocationInfo,
    MapsLocationSet,
)
from .asset_types import (
    AppDeepLinkAsset,
    BookOnGoogleAsset,
    BusinessMessageAsset,
    BusinessMessageCallToActionInfo,
    BusinessProfileLocation,
    CallAsset,
    CalloutAsset,
    CallToActionAsset,
    DemandGenCarouselCardAsset,
    DynamicCustomAsset,
    DynamicEducationAsset,
    DynamicFlightsAsset,
    DynamicHotelsAndRentalsAsset,
    DynamicJobsAsset,
    DynamicLocalAsset,
    DynamicRealEstateAsset,
    DynamicTravelAsset,
    HotelCalloutAsset,
    HotelPropertyAsset,
    ImageAsset,
    ImageDimension,
    LeadFormAsset,
    LeadFormCustomQuestionField,
    LeadFormDeliveryMethod,
    LeadFormField,
    LeadFormSingleChoiceAnswers,
    LocationAsset,
    MediaBundleAsset,
    MobileAppAsset,
    PageFeedAsset,
    PriceAsset,
    PriceOffering,
    PromotionAsset,
    SitelinkAsset,
    StructuredSnippetAsset,
    TextAsset,
    WebhookDelivery,
    WhatsappBusinessMessageInfo,
    YoutubeVideoAsset,
)
from .asset_usage import (
    AssetUsage,
)
from .audience_insights_attribute import (
    AudienceInsightsAttribute,
    AudienceInsightsAttributeMetadata,
    AudienceInsightsCategory,
    AudienceInsightsDynamicLineup,
    AudienceInsightsEntity,
    AudienceInsightsTopic,
    DynamicLineupAttributeMetadata,
    KnowledgeGraphAttributeMetadata,
    LocationAttributeMetadata,
    UserInterestAttributeMetadata,
    YouTubeChannelAttributeMetadata,
    YouTubeVideoAttributeMetadata,
)
from .audiences import (
    AgeDimension,
    AgeSegment,
    AudienceDimension,
    AudienceExclusionDimension,
    AudienceSegment,
    AudienceSegmentDimension,
    CustomAudienceSegment,
    DetailedDemographicSegment,
    ExclusionSegment,
    GenderDimension,
    HouseholdIncomeDimension,
    LifeEventSegment,
    ParentalStatusDimension,
    UserInterestSegment,
    UserListSegment,
)
from .bidding import (
    Commission,
    EnhancedCpc,
    FixedCpm,
    FixedCpmTargetFrequencyGoalInfo,
    ManualCpa,
    ManualCpc,
    ManualCpm,
    ManualCpv,
    MaximizeConversions,
    MaximizeConversionValue,
    PercentCpc,
    TargetCpa,
    TargetCpm,
    TargetCpmTargetFrequencyGoal,
    TargetCpv,
    TargetImpressionShare,
    TargetRoas,
    TargetSpend,
)
from .click_location import (
    ClickLocation,
)
from .consent import (
    Consent,
)
from .criteria import (
    ActivityCityInfo,
    ActivityCountryInfo,
    ActivityIdInfo,
    ActivityRatingInfo,
    ActivityStateInfo,
    AddressInfo,
    AdScheduleInfo,
    AgeRangeInfo,
    AppPaymentModelInfo,
    AudienceInfo,
    BrandInfo,
    BrandListInfo,
    CarrierInfo,
    CombinedAudienceInfo,
    ContentLabelInfo,
    CustomAffinityInfo,
    CustomAudienceInfo,
    CustomIntentInfo,
    DeviceInfo,
    GenderInfo,
    GeoPointInfo,
    HotelAdvanceBookingWindowInfo,
    HotelCheckInDateRangeInfo,
    HotelCheckInDayInfo,
    HotelCityInfo,
    HotelClassInfo,
    HotelCountryRegionInfo,
    HotelDateSelectionTypeInfo,
    HotelIdInfo,
    HotelLengthOfStayInfo,
    HotelStateInfo,
    IncomeRangeInfo,
    InteractionTypeInfo,
    IpBlockInfo,
    KeywordInfo,
    KeywordThemeInfo,
    LanguageInfo,
    ListingDimensionInfo,
    ListingDimensionPath,
    ListingGroupInfo,
    ListingScopeInfo,
    LocalServiceIdInfo,
    LocationGroupInfo,
    LocationInfo,
    MobileAppCategoryInfo,
    MobileApplicationInfo,
    MobileDeviceInfo,
    NegativeKeywordListInfo,
    OperatingSystemVersionInfo,
    ParentalStatusInfo,
    PlacementInfo,
    ProductBrandInfo,
    ProductCategoryInfo,
    ProductChannelExclusivityInfo,
    ProductChannelInfo,
    ProductConditionInfo,
    ProductCustomAttributeInfo,
    ProductGroupingInfo,
    ProductItemIdInfo,
    ProductLabelsInfo,
    ProductLegacyConditionInfo,
    ProductTypeFullInfo,
    ProductTypeInfo,
    ProximityInfo,
    SearchThemeInfo,
    TopicInfo,
    UnknownListingDimensionInfo,
    UserInterestInfo,
    UserListInfo,
    WebpageConditionInfo,
    WebpageInfo,
    WebpageSampleInfo,
    YouTubeChannelInfo,
    YouTubeVideoInfo,
)
from .criterion_category_availability import (
    CriterionCategoryAvailability,
    CriterionCategoryChannelAvailability,
    CriterionCategoryLocaleAvailability,
)
from .custom_parameter import (
    CustomParameter,
)
from .customizer_value import (
    CustomizerValue,
)
from .dates import (
    DateRange,
    YearMonth,
    YearMonthRange,
)
from .extensions import (
    CallFeedItem,
    CalloutFeedItem,
    SitelinkFeedItem,
)
from .feed_common import (
    Money,
)
from .final_app_url import (
    FinalAppUrl,
)
from .frequency_cap import (
    FrequencyCapEntry,
    FrequencyCapKey,
)
from .keyword_plan_common import (
    ConceptGroup,
    HistoricalMetricsOptions,
    KeywordAnnotations,
    KeywordConcept,
    KeywordPlanAggregateMetricResults,
    KeywordPlanAggregateMetrics,
    KeywordPlanDeviceSearches,
    KeywordPlanHistoricalMetrics,
    MonthlySearchVolume,
)
from .lifecycle_goals import (
    LifecycleGoalValueSettings,
)
from .local_services import (
    LocalServicesDocumentReadOnly,
)
from .metric_goal import (
    MetricGoal,
)
from .metrics import (
    Metrics,
    SearchVolumeRange,
)
from .offline_user_data import (
    CustomerMatchUserListMetadata,
    EventAttribute,
    EventItemAttribute,
    ItemAttribute,
    OfflineUserAddressInfo,
    ShoppingLoyalty,
    StoreAttribute,
    StoreSalesMetadata,
    StoreSalesThirdPartyMetadata,
    TransactionAttribute,
    UserAttribute,
    UserData,
    UserIdentifier,
)
from .policy import (
    PolicyTopicConstraint,
    PolicyTopicEntry,
    PolicyTopicEvidence,
    PolicyValidationParameter,
    PolicyViolationKey,
)
from .policy_summary import (
    PolicySummary,
)
from .real_time_bidding_setting import (
    RealTimeBiddingSetting,
)
from .segments import (
    AssetInteractionTarget,
    BudgetCampaignAssociationStatus,
    Keyword,
    Segments,
    SkAdNetworkSourceApp,
)
from .simulation import (
    BudgetSimulationPoint,
    BudgetSimulationPointList,
    CpcBidSimulationPoint,
    CpcBidSimulationPointList,
    CpvBidSimulationPoint,
    CpvBidSimulationPointList,
    PercentCpcBidSimulationPoint,
    PercentCpcBidSimulationPointList,
    TargetCpaSimulationPoint,
    TargetCpaSimulationPointList,
    TargetImpressionShareSimulationPoint,
    TargetImpressionShareSimulationPointList,
    TargetRoasSimulationPoint,
    TargetRoasSimulationPointList,
)
from .tag_snippet import (
    TagSnippet,
)
from .targeting_setting import (
    TargetingSetting,
    TargetRestriction,
    TargetRestrictionOperation,
)
from .text_label import (
    TextLabel,
)
from .url_collection import (
    UrlCollection,
)
from .user_lists import (
    BasicUserListInfo,
    CrmBasedUserListInfo,
    FlexibleRuleOperandInfo,
    FlexibleRuleUserListInfo,
    LogicalUserListInfo,
    LogicalUserListOperandInfo,
    LookalikeUserListInfo,
    RuleBasedUserListInfo,
    SimilarUserListInfo,
    UserListActionInfo,
    UserListDateRuleItemInfo,
    UserListLogicalRuleInfo,
    UserListNumberRuleItemInfo,
    UserListRuleInfo,
    UserListRuleItemGroupInfo,
    UserListRuleItemInfo,
    UserListStringRuleItemInfo,
)
from .value import (
    Value,
)

__all__ = (
    "AdAppDeepLinkAsset",
    "AdCallToActionAsset",
    "AdDemandGenCarouselCardAsset",
    "AdImageAsset",
    "AdMediaBundleAsset",
    "AdTextAsset",
    "AdVideoAsset",
    "AdVideoAssetInfo",
    "AdVideoAssetInventoryPreferences",
    "AppAdInfo",
    "AppEngagementAdInfo",
    "AppPreRegistrationAdInfo",
    "CallAdInfo",
    "DemandGenCarouselAdInfo",
    "DemandGenMultiAssetAdInfo",
    "DemandGenProductAdInfo",
    "DemandGenVideoResponsiveAdInfo",
    "DisplayUploadAdInfo",
    "ExpandedDynamicSearchAdInfo",
    "ExpandedTextAdInfo",
    "HotelAdInfo",
    "ImageAdInfo",
    "InFeedVideoAdInfo",
    "LegacyAppInstallAdInfo",
    "LegacyResponsiveDisplayAdInfo",
    "LocalAdInfo",
    "ResponsiveDisplayAdControlSpec",
    "ResponsiveDisplayAdInfo",
    "ResponsiveSearchAdInfo",
    "ShoppingComparisonListingAdInfo",
    "ShoppingProductAdInfo",
    "ShoppingSmartAdInfo",
    "SmartCampaignAdInfo",
    "TextAdInfo",
    "TravelAdInfo",
    "VideoAdInfo",
    "VideoBumperInStreamAdInfo",
    "VideoNonSkippableInStreamAdInfo",
    "VideoOutstreamAdInfo",
    "VideoResponsiveAdInfo",
    "VideoTrueViewInStreamAdInfo",
    "YouTubeAudioAdInfo",
    "AdAssetPolicySummary",
    "AssetDisapproved",
    "AssetLinkPrimaryStatusDetails",
    "BusinessProfileBusinessNameFilter",
    "BusinessProfileLocationGroup",
    "BusinessProfileLocationSet",
    "ChainFilter",
    "ChainLocationGroup",
    "ChainSet",
    "DynamicBusinessProfileLocationGroupFilter",
    "LocationSet",
    "MapsLocationInfo",
    "MapsLocationSet",
    "AppDeepLinkAsset",
    "BookOnGoogleAsset",
    "BusinessMessageAsset",
    "BusinessMessageCallToActionInfo",
    "BusinessProfileLocation",
    "CallAsset",
    "CalloutAsset",
    "CallToActionAsset",
    "DemandGenCarouselCardAsset",
    "DynamicCustomAsset",
    "DynamicEducationAsset",
    "DynamicFlightsAsset",
    "DynamicHotelsAndRentalsAsset",
    "DynamicJobsAsset",
    "DynamicLocalAsset",
    "DynamicRealEstateAsset",
    "DynamicTravelAsset",
    "HotelCalloutAsset",
    "HotelPropertyAsset",
    "ImageAsset",
    "ImageDimension",
    "LeadFormAsset",
    "LeadFormCustomQuestionField",
    "LeadFormDeliveryMethod",
    "LeadFormField",
    "LeadFormSingleChoiceAnswers",
    "LocationAsset",
    "MediaBundleAsset",
    "MobileAppAsset",
    "PageFeedAsset",
    "PriceAsset",
    "PriceOffering",
    "PromotionAsset",
    "SitelinkAsset",
    "StructuredSnippetAsset",
    "TextAsset",
    "WebhookDelivery",
    "WhatsappBusinessMessageInfo",
    "YoutubeVideoAsset",
    "AssetUsage",
    "AudienceInsightsAttribute",
    "AudienceInsightsAttributeMetadata",
    "AudienceInsightsCategory",
    "AudienceInsightsDynamicLineup",
    "AudienceInsightsEntity",
    "AudienceInsightsTopic",
    "DynamicLineupAttributeMetadata",
    "KnowledgeGraphAttributeMetadata",
    "LocationAttributeMetadata",
    "UserInterestAttributeMetadata",
    "YouTubeChannelAttributeMetadata",
    "YouTubeVideoAttributeMetadata",
    "AgeDimension",
    "AgeSegment",
    "AudienceDimension",
    "AudienceExclusionDimension",
    "AudienceSegment",
    "AudienceSegmentDimension",
    "CustomAudienceSegment",
    "DetailedDemographicSegment",
    "ExclusionSegment",
    "GenderDimension",
    "HouseholdIncomeDimension",
    "LifeEventSegment",
    "ParentalStatusDimension",
    "UserInterestSegment",
    "UserListSegment",
    "Commission",
    "EnhancedCpc",
    "FixedCpm",
    "FixedCpmTargetFrequencyGoalInfo",
    "ManualCpa",
    "ManualCpc",
    "ManualCpm",
    "ManualCpv",
    "MaximizeConversions",
    "MaximizeConversionValue",
    "PercentCpc",
    "TargetCpa",
    "TargetCpm",
    "TargetCpmTargetFrequencyGoal",
    "TargetCpv",
    "TargetImpressionShare",
    "TargetRoas",
    "TargetSpend",
    "ClickLocation",
    "Consent",
    "ActivityCityInfo",
    "ActivityCountryInfo",
    "ActivityIdInfo",
    "ActivityRatingInfo",
    "ActivityStateInfo",
    "AddressInfo",
    "AdScheduleInfo",
    "AgeRangeInfo",
    "AppPaymentModelInfo",
    "AudienceInfo",
    "BrandInfo",
    "BrandListInfo",
    "CarrierInfo",
    "CombinedAudienceInfo",
    "ContentLabelInfo",
    "CustomAffinityInfo",
    "CustomAudienceInfo",
    "CustomIntentInfo",
    "DeviceInfo",
    "GenderInfo",
    "GeoPointInfo",
    "HotelAdvanceBookingWindowInfo",
    "HotelCheckInDateRangeInfo",
    "HotelCheckInDayInfo",
    "HotelCityInfo",
    "HotelClassInfo",
    "HotelCountryRegionInfo",
    "HotelDateSelectionTypeInfo",
    "HotelIdInfo",
    "HotelLengthOfStayInfo",
    "HotelStateInfo",
    "IncomeRangeInfo",
    "InteractionTypeInfo",
    "IpBlockInfo",
    "KeywordInfo",
    "KeywordThemeInfo",
    "LanguageInfo",
    "ListingDimensionInfo",
    "ListingDimensionPath",
    "ListingGroupInfo",
    "ListingScopeInfo",
    "LocalServiceIdInfo",
    "LocationGroupInfo",
    "LocationInfo",
    "MobileAppCategoryInfo",
    "MobileApplicationInfo",
    "MobileDeviceInfo",
    "NegativeKeywordListInfo",
    "OperatingSystemVersionInfo",
    "ParentalStatusInfo",
    "PlacementInfo",
    "ProductBrandInfo",
    "ProductCategoryInfo",
    "ProductChannelExclusivityInfo",
    "ProductChannelInfo",
    "ProductConditionInfo",
    "ProductCustomAttributeInfo",
    "ProductGroupingInfo",
    "ProductItemIdInfo",
    "ProductLabelsInfo",
    "ProductLegacyConditionInfo",
    "ProductTypeFullInfo",
    "ProductTypeInfo",
    "ProximityInfo",
    "SearchThemeInfo",
    "TopicInfo",
    "UnknownListingDimensionInfo",
    "UserInterestInfo",
    "UserListInfo",
    "WebpageConditionInfo",
    "WebpageInfo",
    "WebpageSampleInfo",
    "YouTubeChannelInfo",
    "YouTubeVideoInfo",
    "CriterionCategoryAvailability",
    "CriterionCategoryChannelAvailability",
    "CriterionCategoryLocaleAvailability",
    "CustomParameter",
    "CustomizerValue",
    "DateRange",
    "YearMonth",
    "YearMonthRange",
    "CallFeedItem",
    "CalloutFeedItem",
    "SitelinkFeedItem",
    "Money",
    "FinalAppUrl",
    "FrequencyCapEntry",
    "FrequencyCapKey",
    "ConceptGroup",
    "HistoricalMetricsOptions",
    "KeywordAnnotations",
    "KeywordConcept",
    "KeywordPlanAggregateMetricResults",
    "KeywordPlanAggregateMetrics",
    "KeywordPlanDeviceSearches",
    "KeywordPlanHistoricalMetrics",
    "MonthlySearchVolume",
    "LifecycleGoalValueSettings",
    "LocalServicesDocumentReadOnly",
    "MetricGoal",
    "Metrics",
    "SearchVolumeRange",
    "CustomerMatchUserListMetadata",
    "EventAttribute",
    "EventItemAttribute",
    "ItemAttribute",
    "OfflineUserAddressInfo",
    "ShoppingLoyalty",
    "StoreAttribute",
    "StoreSalesMetadata",
    "StoreSalesThirdPartyMetadata",
    "TransactionAttribute",
    "UserAttribute",
    "UserData",
    "UserIdentifier",
    "PolicyTopicConstraint",
    "PolicyTopicEntry",
    "PolicyTopicEvidence",
    "PolicyValidationParameter",
    "PolicyViolationKey",
    "PolicySummary",
    "RealTimeBiddingSetting",
    "AssetInteractionTarget",
    "BudgetCampaignAssociationStatus",
    "Keyword",
    "Segments",
    "SkAdNetworkSourceApp",
    "BudgetSimulationPoint",
    "BudgetSimulationPointList",
    "CpcBidSimulationPoint",
    "CpcBidSimulationPointList",
    "CpvBidSimulationPoint",
    "CpvBidSimulationPointList",
    "PercentCpcBidSimulationPoint",
    "PercentCpcBidSimulationPointList",
    "TargetCpaSimulationPoint",
    "TargetCpaSimulationPointList",
    "TargetImpressionShareSimulationPoint",
    "TargetImpressionShareSimulationPointList",
    "TargetRoasSimulationPoint",
    "TargetRoasSimulationPointList",
    "TagSnippet",
    "TargetingSetting",
    "TargetRestriction",
    "TargetRestrictionOperation",
    "TextLabel",
    "UrlCollection",
    "BasicUserListInfo",
    "CrmBasedUserListInfo",
    "FlexibleRuleOperandInfo",
    "FlexibleRuleUserListInfo",
    "LogicalUserListInfo",
    "LogicalUserListOperandInfo",
    "LookalikeUserListInfo",
    "RuleBasedUserListInfo",
    "SimilarUserListInfo",
    "UserListActionInfo",
    "UserListDateRuleItemInfo",
    "UserListLogicalRuleInfo",
    "UserListNumberRuleItemInfo",
    "UserListRuleInfo",
    "UserListRuleItemGroupInfo",
    "UserListRuleItemInfo",
    "UserListStringRuleItemInfo",
    "Value",
)
