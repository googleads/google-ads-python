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
from google.ads.googleads.v18 import gapic_version as package_version

__version__ = package_version.__version__


from .types.ad_asset import AdCallToActionAsset
from .types.ad_asset import AdDemandGenCarouselCardAsset
from .types.ad_asset import AdImageAsset
from .types.ad_asset import AdMediaBundleAsset
from .types.ad_asset import AdTextAsset
from .types.ad_asset import AdVideoAsset
from .types.ad_asset import AdVideoAssetInfo
from .types.ad_asset import AdVideoAssetInventoryPreferences
from .types.ad_type_infos import AppAdInfo
from .types.ad_type_infos import AppEngagementAdInfo
from .types.ad_type_infos import AppPreRegistrationAdInfo
from .types.ad_type_infos import CallAdInfo
from .types.ad_type_infos import DemandGenCarouselAdInfo
from .types.ad_type_infos import DemandGenMultiAssetAdInfo
from .types.ad_type_infos import DemandGenProductAdInfo
from .types.ad_type_infos import DemandGenVideoResponsiveAdInfo
from .types.ad_type_infos import DisplayUploadAdInfo
from .types.ad_type_infos import ExpandedDynamicSearchAdInfo
from .types.ad_type_infos import ExpandedTextAdInfo
from .types.ad_type_infos import HotelAdInfo
from .types.ad_type_infos import ImageAdInfo
from .types.ad_type_infos import InFeedVideoAdInfo
from .types.ad_type_infos import LegacyAppInstallAdInfo
from .types.ad_type_infos import LegacyResponsiveDisplayAdInfo
from .types.ad_type_infos import LocalAdInfo
from .types.ad_type_infos import ResponsiveDisplayAdControlSpec
from .types.ad_type_infos import ResponsiveDisplayAdInfo
from .types.ad_type_infos import ResponsiveSearchAdInfo
from .types.ad_type_infos import ShoppingComparisonListingAdInfo
from .types.ad_type_infos import ShoppingProductAdInfo
from .types.ad_type_infos import ShoppingSmartAdInfo
from .types.ad_type_infos import SmartCampaignAdInfo
from .types.ad_type_infos import TextAdInfo
from .types.ad_type_infos import TravelAdInfo
from .types.ad_type_infos import VideoAdInfo
from .types.ad_type_infos import VideoBumperInStreamAdInfo
from .types.ad_type_infos import VideoNonSkippableInStreamAdInfo
from .types.ad_type_infos import VideoOutstreamAdInfo
from .types.ad_type_infos import VideoResponsiveAdInfo
from .types.ad_type_infos import VideoTrueViewInStreamAdInfo
from .types.asset_policy import AdAssetPolicySummary
from .types.asset_policy import AssetDisapproved
from .types.asset_policy import AssetLinkPrimaryStatusDetails
from .types.asset_set_types import BusinessProfileBusinessNameFilter
from .types.asset_set_types import BusinessProfileLocationGroup
from .types.asset_set_types import BusinessProfileLocationSet
from .types.asset_set_types import ChainFilter
from .types.asset_set_types import ChainLocationGroup
from .types.asset_set_types import ChainSet
from .types.asset_set_types import DynamicBusinessProfileLocationGroupFilter
from .types.asset_set_types import LocationSet
from .types.asset_set_types import MapsLocationInfo
from .types.asset_set_types import MapsLocationSet
from .types.asset_types import BookOnGoogleAsset
from .types.asset_types import BusinessProfileLocation
from .types.asset_types import CallAsset
from .types.asset_types import CalloutAsset
from .types.asset_types import CallToActionAsset
from .types.asset_types import DemandGenCarouselCardAsset
from .types.asset_types import DynamicCustomAsset
from .types.asset_types import DynamicEducationAsset
from .types.asset_types import DynamicFlightsAsset
from .types.asset_types import DynamicHotelsAndRentalsAsset
from .types.asset_types import DynamicJobsAsset
from .types.asset_types import DynamicLocalAsset
from .types.asset_types import DynamicRealEstateAsset
from .types.asset_types import DynamicTravelAsset
from .types.asset_types import HotelCalloutAsset
from .types.asset_types import HotelPropertyAsset
from .types.asset_types import ImageAsset
from .types.asset_types import ImageDimension
from .types.asset_types import LeadFormAsset
from .types.asset_types import LeadFormCustomQuestionField
from .types.asset_types import LeadFormDeliveryMethod
from .types.asset_types import LeadFormField
from .types.asset_types import LeadFormSingleChoiceAnswers
from .types.asset_types import LocationAsset
from .types.asset_types import MediaBundleAsset
from .types.asset_types import MobileAppAsset
from .types.asset_types import PageFeedAsset
from .types.asset_types import PriceAsset
from .types.asset_types import PriceOffering
from .types.asset_types import PromotionAsset
from .types.asset_types import SitelinkAsset
from .types.asset_types import StructuredSnippetAsset
from .types.asset_types import TextAsset
from .types.asset_types import WebhookDelivery
from .types.asset_types import YoutubeVideoAsset
from .types.asset_usage import AssetUsage
from .types.audience_insights_attribute import AudienceInsightsAttribute
from .types.audience_insights_attribute import AudienceInsightsAttributeMetadata
from .types.audience_insights_attribute import AudienceInsightsCategory
from .types.audience_insights_attribute import AudienceInsightsDynamicLineup
from .types.audience_insights_attribute import AudienceInsightsEntity
from .types.audience_insights_attribute import DynamicLineupAttributeMetadata
from .types.audience_insights_attribute import LocationAttributeMetadata
from .types.audience_insights_attribute import YouTubeChannelAttributeMetadata
from .types.audiences import AgeDimension
from .types.audiences import AgeSegment
from .types.audiences import AudienceDimension
from .types.audiences import AudienceExclusionDimension
from .types.audiences import AudienceSegment
from .types.audiences import AudienceSegmentDimension
from .types.audiences import CustomAudienceSegment
from .types.audiences import DetailedDemographicSegment
from .types.audiences import ExclusionSegment
from .types.audiences import GenderDimension
from .types.audiences import HouseholdIncomeDimension
from .types.audiences import LifeEventSegment
from .types.audiences import ParentalStatusDimension
from .types.audiences import UserInterestSegment
from .types.audiences import UserListSegment
from .types.bidding import Commission
from .types.bidding import EnhancedCpc
from .types.bidding import FixedCpm
from .types.bidding import FixedCpmTargetFrequencyGoalInfo
from .types.bidding import ManualCpa
from .types.bidding import ManualCpc
from .types.bidding import ManualCpm
from .types.bidding import ManualCpv
from .types.bidding import MaximizeConversions
from .types.bidding import MaximizeConversionValue
from .types.bidding import PercentCpc
from .types.bidding import TargetCpa
from .types.bidding import TargetCpm
from .types.bidding import TargetCpmTargetFrequencyGoal
from .types.bidding import TargetCpv
from .types.bidding import TargetImpressionShare
from .types.bidding import TargetRoas
from .types.bidding import TargetSpend
from .types.click_location import ClickLocation
from .types.consent import Consent
from .types.criteria import ActivityCityInfo
from .types.criteria import ActivityCountryInfo
from .types.criteria import ActivityIdInfo
from .types.criteria import ActivityRatingInfo
from .types.criteria import ActivityStateInfo
from .types.criteria import AddressInfo
from .types.criteria import AdScheduleInfo
from .types.criteria import AgeRangeInfo
from .types.criteria import AppPaymentModelInfo
from .types.criteria import AudienceInfo
from .types.criteria import BrandInfo
from .types.criteria import BrandListInfo
from .types.criteria import CarrierInfo
from .types.criteria import CombinedAudienceInfo
from .types.criteria import ContentLabelInfo
from .types.criteria import CustomAffinityInfo
from .types.criteria import CustomAudienceInfo
from .types.criteria import CustomIntentInfo
from .types.criteria import DeviceInfo
from .types.criteria import GenderInfo
from .types.criteria import GeoPointInfo
from .types.criteria import HotelAdvanceBookingWindowInfo
from .types.criteria import HotelCheckInDateRangeInfo
from .types.criteria import HotelCheckInDayInfo
from .types.criteria import HotelCityInfo
from .types.criteria import HotelClassInfo
from .types.criteria import HotelCountryRegionInfo
from .types.criteria import HotelDateSelectionTypeInfo
from .types.criteria import HotelIdInfo
from .types.criteria import HotelLengthOfStayInfo
from .types.criteria import HotelStateInfo
from .types.criteria import IncomeRangeInfo
from .types.criteria import InteractionTypeInfo
from .types.criteria import IpBlockInfo
from .types.criteria import KeywordInfo
from .types.criteria import KeywordThemeInfo
from .types.criteria import LanguageInfo
from .types.criteria import ListingDimensionInfo
from .types.criteria import ListingDimensionPath
from .types.criteria import ListingGroupInfo
from .types.criteria import ListingScopeInfo
from .types.criteria import LocalServiceIdInfo
from .types.criteria import LocationGroupInfo
from .types.criteria import LocationInfo
from .types.criteria import MobileAppCategoryInfo
from .types.criteria import MobileApplicationInfo
from .types.criteria import MobileDeviceInfo
from .types.criteria import NegativeKeywordListInfo
from .types.criteria import OperatingSystemVersionInfo
from .types.criteria import ParentalStatusInfo
from .types.criteria import PlacementInfo
from .types.criteria import ProductBrandInfo
from .types.criteria import ProductCategoryInfo
from .types.criteria import ProductChannelExclusivityInfo
from .types.criteria import ProductChannelInfo
from .types.criteria import ProductConditionInfo
from .types.criteria import ProductCustomAttributeInfo
from .types.criteria import ProductGroupingInfo
from .types.criteria import ProductItemIdInfo
from .types.criteria import ProductLabelsInfo
from .types.criteria import ProductLegacyConditionInfo
from .types.criteria import ProductTypeFullInfo
from .types.criteria import ProductTypeInfo
from .types.criteria import ProximityInfo
from .types.criteria import SearchThemeInfo
from .types.criteria import TopicInfo
from .types.criteria import UnknownListingDimensionInfo
from .types.criteria import UserInterestInfo
from .types.criteria import UserListInfo
from .types.criteria import WebpageConditionInfo
from .types.criteria import WebpageInfo
from .types.criteria import WebpageSampleInfo
from .types.criteria import YouTubeChannelInfo
from .types.criteria import YouTubeVideoInfo
from .types.criterion_category_availability import CriterionCategoryAvailability
from .types.criterion_category_availability import (
    CriterionCategoryChannelAvailability,
)
from .types.criterion_category_availability import (
    CriterionCategoryLocaleAvailability,
)
from .types.custom_parameter import CustomParameter
from .types.customizer_value import CustomizerValue
from .types.dates import DateRange
from .types.dates import YearMonth
from .types.dates import YearMonthRange
from .types.extensions import AffiliateLocationFeedItem
from .types.extensions import AppFeedItem
from .types.extensions import CallFeedItem
from .types.extensions import CalloutFeedItem
from .types.extensions import HotelCalloutFeedItem
from .types.extensions import ImageFeedItem
from .types.extensions import LocationFeedItem
from .types.extensions import PriceFeedItem
from .types.extensions import PriceOffer
from .types.extensions import PromotionFeedItem
from .types.extensions import SitelinkFeedItem
from .types.extensions import StructuredSnippetFeedItem
from .types.extensions import TextMessageFeedItem
from .types.feed_common import Money
from .types.feed_item_set_filter_type_infos import BusinessNameFilter
from .types.feed_item_set_filter_type_infos import (
    DynamicAffiliateLocationSetFilter,
)
from .types.feed_item_set_filter_type_infos import DynamicLocationSetFilter
from .types.final_app_url import FinalAppUrl
from .types.frequency_cap import FrequencyCapEntry
from .types.frequency_cap import FrequencyCapKey
from .types.keyword_plan_common import ConceptGroup
from .types.keyword_plan_common import HistoricalMetricsOptions
from .types.keyword_plan_common import KeywordAnnotations
from .types.keyword_plan_common import KeywordConcept
from .types.keyword_plan_common import KeywordPlanAggregateMetricResults
from .types.keyword_plan_common import KeywordPlanAggregateMetrics
from .types.keyword_plan_common import KeywordPlanDeviceSearches
from .types.keyword_plan_common import KeywordPlanHistoricalMetrics
from .types.keyword_plan_common import MonthlySearchVolume
from .types.lifecycle_goals import LifecycleGoalValueSettings
from .types.local_services import LocalServicesDocumentReadOnly
from .types.matching_function import MatchingFunction
from .types.matching_function import Operand
from .types.metric_goal import MetricGoal
from .types.metrics import Metrics
from .types.metrics import SearchVolumeRange
from .types.offline_user_data import CustomerMatchUserListMetadata
from .types.offline_user_data import EventAttribute
from .types.offline_user_data import EventItemAttribute
from .types.offline_user_data import ItemAttribute
from .types.offline_user_data import OfflineUserAddressInfo
from .types.offline_user_data import ShoppingLoyalty
from .types.offline_user_data import StoreAttribute
from .types.offline_user_data import StoreSalesMetadata
from .types.offline_user_data import StoreSalesThirdPartyMetadata
from .types.offline_user_data import TransactionAttribute
from .types.offline_user_data import UserAttribute
from .types.offline_user_data import UserData
from .types.offline_user_data import UserIdentifier
from .types.policy import PolicyTopicConstraint
from .types.policy import PolicyTopicEntry
from .types.policy import PolicyTopicEvidence
from .types.policy import PolicyValidationParameter
from .types.policy import PolicyViolationKey
from .types.policy_summary import PolicySummary
from .types.real_time_bidding_setting import RealTimeBiddingSetting
from .types.segments import AssetInteractionTarget
from .types.segments import BudgetCampaignAssociationStatus
from .types.segments import Keyword
from .types.segments import Segments
from .types.segments import SkAdNetworkSourceApp
from .types.simulation import BudgetSimulationPoint
from .types.simulation import BudgetSimulationPointList
from .types.simulation import CpcBidSimulationPoint
from .types.simulation import CpcBidSimulationPointList
from .types.simulation import CpvBidSimulationPoint
from .types.simulation import CpvBidSimulationPointList
from .types.simulation import PercentCpcBidSimulationPoint
from .types.simulation import PercentCpcBidSimulationPointList
from .types.simulation import TargetCpaSimulationPoint
from .types.simulation import TargetCpaSimulationPointList
from .types.simulation import TargetImpressionShareSimulationPoint
from .types.simulation import TargetImpressionShareSimulationPointList
from .types.simulation import TargetRoasSimulationPoint
from .types.simulation import TargetRoasSimulationPointList
from .types.tag_snippet import TagSnippet
from .types.targeting_setting import TargetingSetting
from .types.targeting_setting import TargetRestriction
from .types.targeting_setting import TargetRestrictionOperation
from .types.text_label import TextLabel
from .types.url_collection import UrlCollection
from .types.user_lists import BasicUserListInfo
from .types.user_lists import CrmBasedUserListInfo
from .types.user_lists import FlexibleRuleOperandInfo
from .types.user_lists import FlexibleRuleUserListInfo
from .types.user_lists import LogicalUserListInfo
from .types.user_lists import LogicalUserListOperandInfo
from .types.user_lists import LookalikeUserListInfo
from .types.user_lists import RuleBasedUserListInfo
from .types.user_lists import SimilarUserListInfo
from .types.user_lists import UserListActionInfo
from .types.user_lists import UserListDateRuleItemInfo
from .types.user_lists import UserListLogicalRuleInfo
from .types.user_lists import UserListNumberRuleItemInfo
from .types.user_lists import UserListRuleInfo
from .types.user_lists import UserListRuleItemGroupInfo
from .types.user_lists import UserListRuleItemInfo
from .types.user_lists import UserListStringRuleItemInfo
from .types.value import Value

__all__ = (
    "ActivityCityInfo",
    "ActivityCountryInfo",
    "ActivityIdInfo",
    "ActivityRatingInfo",
    "ActivityStateInfo",
    "AdAssetPolicySummary",
    "AdCallToActionAsset",
    "AdDemandGenCarouselCardAsset",
    "AdImageAsset",
    "AdMediaBundleAsset",
    "AdScheduleInfo",
    "AdTextAsset",
    "AdVideoAsset",
    "AdVideoAssetInfo",
    "AdVideoAssetInventoryPreferences",
    "AddressInfo",
    "AffiliateLocationFeedItem",
    "AgeDimension",
    "AgeRangeInfo",
    "AgeSegment",
    "AppAdInfo",
    "AppEngagementAdInfo",
    "AppFeedItem",
    "AppPaymentModelInfo",
    "AppPreRegistrationAdInfo",
    "AssetDisapproved",
    "AssetInteractionTarget",
    "AssetLinkPrimaryStatusDetails",
    "AssetUsage",
    "AudienceDimension",
    "AudienceExclusionDimension",
    "AudienceInfo",
    "AudienceInsightsAttribute",
    "AudienceInsightsAttributeMetadata",
    "AudienceInsightsCategory",
    "AudienceInsightsDynamicLineup",
    "AudienceInsightsEntity",
    "AudienceSegment",
    "AudienceSegmentDimension",
    "BasicUserListInfo",
    "BookOnGoogleAsset",
    "BrandInfo",
    "BrandListInfo",
    "BudgetCampaignAssociationStatus",
    "BudgetSimulationPoint",
    "BudgetSimulationPointList",
    "BusinessNameFilter",
    "BusinessProfileBusinessNameFilter",
    "BusinessProfileLocation",
    "BusinessProfileLocationGroup",
    "BusinessProfileLocationSet",
    "CallAdInfo",
    "CallAsset",
    "CallFeedItem",
    "CallToActionAsset",
    "CalloutAsset",
    "CalloutFeedItem",
    "CarrierInfo",
    "ChainFilter",
    "ChainLocationGroup",
    "ChainSet",
    "ClickLocation",
    "CombinedAudienceInfo",
    "Commission",
    "ConceptGroup",
    "Consent",
    "ContentLabelInfo",
    "CpcBidSimulationPoint",
    "CpcBidSimulationPointList",
    "CpvBidSimulationPoint",
    "CpvBidSimulationPointList",
    "CriterionCategoryAvailability",
    "CriterionCategoryChannelAvailability",
    "CriterionCategoryLocaleAvailability",
    "CrmBasedUserListInfo",
    "CustomAffinityInfo",
    "CustomAudienceInfo",
    "CustomAudienceSegment",
    "CustomIntentInfo",
    "CustomParameter",
    "CustomerMatchUserListMetadata",
    "CustomizerValue",
    "DateRange",
    "DemandGenCarouselAdInfo",
    "DemandGenCarouselCardAsset",
    "DemandGenMultiAssetAdInfo",
    "DemandGenProductAdInfo",
    "DemandGenVideoResponsiveAdInfo",
    "DetailedDemographicSegment",
    "DeviceInfo",
    "DisplayUploadAdInfo",
    "DynamicAffiliateLocationSetFilter",
    "DynamicBusinessProfileLocationGroupFilter",
    "DynamicCustomAsset",
    "DynamicEducationAsset",
    "DynamicFlightsAsset",
    "DynamicHotelsAndRentalsAsset",
    "DynamicJobsAsset",
    "DynamicLineupAttributeMetadata",
    "DynamicLocalAsset",
    "DynamicLocationSetFilter",
    "DynamicRealEstateAsset",
    "DynamicTravelAsset",
    "EnhancedCpc",
    "EventAttribute",
    "EventItemAttribute",
    "ExclusionSegment",
    "ExpandedDynamicSearchAdInfo",
    "ExpandedTextAdInfo",
    "FinalAppUrl",
    "FixedCpm",
    "FixedCpmTargetFrequencyGoalInfo",
    "FlexibleRuleOperandInfo",
    "FlexibleRuleUserListInfo",
    "FrequencyCapEntry",
    "FrequencyCapKey",
    "GenderDimension",
    "GenderInfo",
    "GeoPointInfo",
    "HistoricalMetricsOptions",
    "HotelAdInfo",
    "HotelAdvanceBookingWindowInfo",
    "HotelCalloutAsset",
    "HotelCalloutFeedItem",
    "HotelCheckInDateRangeInfo",
    "HotelCheckInDayInfo",
    "HotelCityInfo",
    "HotelClassInfo",
    "HotelCountryRegionInfo",
    "HotelDateSelectionTypeInfo",
    "HotelIdInfo",
    "HotelLengthOfStayInfo",
    "HotelPropertyAsset",
    "HotelStateInfo",
    "HouseholdIncomeDimension",
    "ImageAdInfo",
    "ImageAsset",
    "ImageDimension",
    "ImageFeedItem",
    "InFeedVideoAdInfo",
    "IncomeRangeInfo",
    "InteractionTypeInfo",
    "IpBlockInfo",
    "ItemAttribute",
    "Keyword",
    "KeywordAnnotations",
    "KeywordConcept",
    "KeywordInfo",
    "KeywordPlanAggregateMetricResults",
    "KeywordPlanAggregateMetrics",
    "KeywordPlanDeviceSearches",
    "KeywordPlanHistoricalMetrics",
    "KeywordThemeInfo",
    "LanguageInfo",
    "LeadFormAsset",
    "LeadFormCustomQuestionField",
    "LeadFormDeliveryMethod",
    "LeadFormField",
    "LeadFormSingleChoiceAnswers",
    "LegacyAppInstallAdInfo",
    "LegacyResponsiveDisplayAdInfo",
    "LifeEventSegment",
    "LifecycleGoalValueSettings",
    "ListingDimensionInfo",
    "ListingDimensionPath",
    "ListingGroupInfo",
    "ListingScopeInfo",
    "LocalAdInfo",
    "LocalServiceIdInfo",
    "LocalServicesDocumentReadOnly",
    "LocationAsset",
    "LocationAttributeMetadata",
    "LocationFeedItem",
    "LocationGroupInfo",
    "LocationInfo",
    "LocationSet",
    "LogicalUserListInfo",
    "LogicalUserListOperandInfo",
    "LookalikeUserListInfo",
    "ManualCpa",
    "ManualCpc",
    "ManualCpm",
    "ManualCpv",
    "MapsLocationInfo",
    "MapsLocationSet",
    "MatchingFunction",
    "MaximizeConversionValue",
    "MaximizeConversions",
    "MediaBundleAsset",
    "MetricGoal",
    "Metrics",
    "MobileAppAsset",
    "MobileAppCategoryInfo",
    "MobileApplicationInfo",
    "MobileDeviceInfo",
    "Money",
    "MonthlySearchVolume",
    "NegativeKeywordListInfo",
    "OfflineUserAddressInfo",
    "Operand",
    "OperatingSystemVersionInfo",
    "PageFeedAsset",
    "ParentalStatusDimension",
    "ParentalStatusInfo",
    "PercentCpc",
    "PercentCpcBidSimulationPoint",
    "PercentCpcBidSimulationPointList",
    "PlacementInfo",
    "PolicySummary",
    "PolicyTopicConstraint",
    "PolicyTopicEntry",
    "PolicyTopicEvidence",
    "PolicyValidationParameter",
    "PolicyViolationKey",
    "PriceAsset",
    "PriceFeedItem",
    "PriceOffer",
    "PriceOffering",
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
    "PromotionAsset",
    "PromotionFeedItem",
    "ProximityInfo",
    "RealTimeBiddingSetting",
    "ResponsiveDisplayAdControlSpec",
    "ResponsiveDisplayAdInfo",
    "ResponsiveSearchAdInfo",
    "RuleBasedUserListInfo",
    "SearchThemeInfo",
    "SearchVolumeRange",
    "Segments",
    "ShoppingComparisonListingAdInfo",
    "ShoppingLoyalty",
    "ShoppingProductAdInfo",
    "ShoppingSmartAdInfo",
    "SimilarUserListInfo",
    "SitelinkAsset",
    "SitelinkFeedItem",
    "SkAdNetworkSourceApp",
    "SmartCampaignAdInfo",
    "StoreAttribute",
    "StoreSalesMetadata",
    "StoreSalesThirdPartyMetadata",
    "StructuredSnippetAsset",
    "StructuredSnippetFeedItem",
    "TagSnippet",
    "TargetCpa",
    "TargetCpaSimulationPoint",
    "TargetCpaSimulationPointList",
    "TargetCpm",
    "TargetCpmTargetFrequencyGoal",
    "TargetCpv",
    "TargetImpressionShare",
    "TargetImpressionShareSimulationPoint",
    "TargetImpressionShareSimulationPointList",
    "TargetRestriction",
    "TargetRestrictionOperation",
    "TargetRoas",
    "TargetRoasSimulationPoint",
    "TargetRoasSimulationPointList",
    "TargetSpend",
    "TargetingSetting",
    "TextAdInfo",
    "TextAsset",
    "TextLabel",
    "TextMessageFeedItem",
    "TopicInfo",
    "TransactionAttribute",
    "TravelAdInfo",
    "UnknownListingDimensionInfo",
    "UrlCollection",
    "UserAttribute",
    "UserData",
    "UserIdentifier",
    "UserInterestInfo",
    "UserInterestSegment",
    "UserListActionInfo",
    "UserListDateRuleItemInfo",
    "UserListInfo",
    "UserListLogicalRuleInfo",
    "UserListNumberRuleItemInfo",
    "UserListRuleInfo",
    "UserListRuleItemGroupInfo",
    "UserListRuleItemInfo",
    "UserListSegment",
    "UserListStringRuleItemInfo",
    "Value",
    "VideoAdInfo",
    "VideoBumperInStreamAdInfo",
    "VideoNonSkippableInStreamAdInfo",
    "VideoOutstreamAdInfo",
    "VideoResponsiveAdInfo",
    "VideoTrueViewInStreamAdInfo",
    "WebhookDelivery",
    "WebpageConditionInfo",
    "WebpageInfo",
    "WebpageSampleInfo",
    "YearMonth",
    "YearMonthRange",
    "YouTubeChannelAttributeMetadata",
    "YouTubeChannelInfo",
    "YouTubeVideoInfo",
    "YoutubeVideoAsset",
)
