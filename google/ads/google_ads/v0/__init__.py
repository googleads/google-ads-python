# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import

from google.ads.google_ads.v0 import types
from google.ads.google_ads.v0.services import account_budget_proposal_service_client
from google.ads.google_ads.v0.services import account_budget_service_client
from google.ads.google_ads.v0.services import ad_group_ad_service_client
from google.ads.google_ads.v0.services import ad_group_audience_view_service_client
from google.ads.google_ads.v0.services import ad_group_bid_modifier_service_client
from google.ads.google_ads.v0.services import ad_group_criterion_service_client
from google.ads.google_ads.v0.services import ad_group_feed_service_client
from google.ads.google_ads.v0.services import ad_group_service_client
from google.ads.google_ads.v0.services import age_range_view_service_client
from google.ads.google_ads.v0.services import bidding_strategy_service_client
from google.ads.google_ads.v0.services import billing_setup_service_client
from google.ads.google_ads.v0.services import campaign_audience_view_service_client
from google.ads.google_ads.v0.services import campaign_bid_modifier_service_client
from google.ads.google_ads.v0.services import campaign_budget_service_client
from google.ads.google_ads.v0.services import campaign_criterion_service_client
from google.ads.google_ads.v0.services import campaign_feed_service_client
from google.ads.google_ads.v0.services import campaign_group_service_client
from google.ads.google_ads.v0.services import campaign_service_client
from google.ads.google_ads.v0.services import campaign_shared_set_service_client
from google.ads.google_ads.v0.services import carrier_constant_service_client
from google.ads.google_ads.v0.services import change_status_service_client
from google.ads.google_ads.v0.services import conversion_action_service_client
from google.ads.google_ads.v0.services import customer_client_link_service_client
from google.ads.google_ads.v0.services import customer_client_service_client
from google.ads.google_ads.v0.services import customer_feed_service_client
from google.ads.google_ads.v0.services import customer_manager_link_service_client
from google.ads.google_ads.v0.services import customer_service_client
from google.ads.google_ads.v0.services import display_keyword_view_service_client
from google.ads.google_ads.v0.services import enums
from google.ads.google_ads.v0.services import feed_item_service_client
from google.ads.google_ads.v0.services import feed_mapping_service_client
from google.ads.google_ads.v0.services import feed_service_client
from google.ads.google_ads.v0.services import gender_view_service_client
from google.ads.google_ads.v0.services import geo_target_constant_service_client
from google.ads.google_ads.v0.services import google_ads_field_service_client
from google.ads.google_ads.v0.services import google_ads_service_client
from google.ads.google_ads.v0.services import hotel_group_view_service_client
from google.ads.google_ads.v0.services import hotel_performance_view_service_client
from google.ads.google_ads.v0.services import keyword_plan_ad_group_service_client
from google.ads.google_ads.v0.services import keyword_plan_campaign_service_client
from google.ads.google_ads.v0.services import keyword_plan_idea_service_client
from google.ads.google_ads.v0.services import keyword_plan_keyword_service_client
from google.ads.google_ads.v0.services import keyword_plan_negative_keyword_service_client
from google.ads.google_ads.v0.services import keyword_plan_service_client
from google.ads.google_ads.v0.services import keyword_view_service_client
from google.ads.google_ads.v0.services import language_constant_service_client
from google.ads.google_ads.v0.services import managed_placement_view_service_client
from google.ads.google_ads.v0.services import media_file_service_client
from google.ads.google_ads.v0.services import parental_status_view_service_client
from google.ads.google_ads.v0.services import payments_account_service_client
from google.ads.google_ads.v0.services import product_group_view_service_client
from google.ads.google_ads.v0.services import recommendation_service_client
from google.ads.google_ads.v0.services import search_term_view_service_client
from google.ads.google_ads.v0.services import shared_criterion_service_client
from google.ads.google_ads.v0.services import shared_set_service_client
from google.ads.google_ads.v0.services import topic_constant_service_client
from google.ads.google_ads.v0.services import topic_view_service_client
from google.ads.google_ads.v0.services import user_list_service_client
from google.ads.google_ads.v0.services import user_interest_service_client
from google.ads.google_ads.v0.services import video_service_client
from google.ads.google_ads.v0.services.transports import account_budget_proposal_service_grpc_transport
from google.ads.google_ads.v0.services.transports import account_budget_service_grpc_transport
from google.ads.google_ads.v0.services.transports import ad_group_ad_service_grpc_transport
from google.ads.google_ads.v0.services.transports import ad_group_audience_view_service_grpc_transport
from google.ads.google_ads.v0.services.transports import ad_group_bid_modifier_service_grpc_transport
from google.ads.google_ads.v0.services.transports import ad_group_criterion_service_grpc_transport
from google.ads.google_ads.v0.services.transports import ad_group_feed_service_grpc_transport
from google.ads.google_ads.v0.services.transports import ad_group_service_grpc_transport
from google.ads.google_ads.v0.services.transports import age_range_view_service_grpc_transport
from google.ads.google_ads.v0.services.transports import bidding_strategy_service_grpc_transport
from google.ads.google_ads.v0.services.transports import billing_setup_service_grpc_transport
from google.ads.google_ads.v0.services.transports import campaign_audience_view_service_grpc_transport
from google.ads.google_ads.v0.services.transports import campaign_bid_modifier_service_grpc_transport
from google.ads.google_ads.v0.services.transports import campaign_budget_service_grpc_transport
from google.ads.google_ads.v0.services.transports import campaign_criterion_service_grpc_transport
from google.ads.google_ads.v0.services.transports import campaign_feed_service_grpc_transport
from google.ads.google_ads.v0.services.transports import campaign_group_service_grpc_transport
from google.ads.google_ads.v0.services.transports import campaign_service_grpc_transport
from google.ads.google_ads.v0.services.transports import campaign_shared_set_service_grpc_transport
from google.ads.google_ads.v0.services.transports import carrier_constant_service_grpc_transport
from google.ads.google_ads.v0.services.transports import change_status_service_grpc_transport
from google.ads.google_ads.v0.services.transports import conversion_action_service_grpc_transport
from google.ads.google_ads.v0.services.transports import customer_client_link_service_grpc_transport
from google.ads.google_ads.v0.services.transports import customer_client_service_grpc_transport
from google.ads.google_ads.v0.services.transports import customer_feed_service_grpc_transport
from google.ads.google_ads.v0.services.transports import customer_manager_link_service_grpc_transport
from google.ads.google_ads.v0.services.transports import customer_service_grpc_transport
from google.ads.google_ads.v0.services.transports import display_keyword_view_service_grpc_transport
from google.ads.google_ads.v0.services.transports import feed_item_service_grpc_transport
from google.ads.google_ads.v0.services.transports import feed_mapping_service_grpc_transport
from google.ads.google_ads.v0.services.transports import feed_service_grpc_transport
from google.ads.google_ads.v0.services.transports import gender_view_service_grpc_transport
from google.ads.google_ads.v0.services.transports import geo_target_constant_service_grpc_transport
from google.ads.google_ads.v0.services.transports import google_ads_field_service_grpc_transport
from google.ads.google_ads.v0.services.transports import google_ads_service_grpc_transport
from google.ads.google_ads.v0.services.transports import hotel_group_view_service_grpc_transport
from google.ads.google_ads.v0.services.transports import hotel_performance_view_service_grpc_transport
from google.ads.google_ads.v0.services.transports import keyword_plan_ad_group_service_grpc_transport
from google.ads.google_ads.v0.services.transports import keyword_plan_campaign_service_grpc_transport
from google.ads.google_ads.v0.services.transports import keyword_plan_idea_service_grpc_transport
from google.ads.google_ads.v0.services.transports import keyword_plan_keyword_service_grpc_transport
from google.ads.google_ads.v0.services.transports import keyword_plan_negative_keyword_service_grpc_transport
from google.ads.google_ads.v0.services.transports import keyword_plan_service_grpc_transport
from google.ads.google_ads.v0.services.transports import keyword_view_service_grpc_transport
from google.ads.google_ads.v0.services.transports import language_constant_service_grpc_transport
from google.ads.google_ads.v0.services.transports import managed_placement_view_service_grpc_transport
from google.ads.google_ads.v0.services.transports import media_file_service_grpc_transport
from google.ads.google_ads.v0.services.transports import parental_status_view_service_grpc_transport
from google.ads.google_ads.v0.services.transports import payments_account_service_grpc_transport
from google.ads.google_ads.v0.services.transports import product_group_view_service_grpc_transport
from google.ads.google_ads.v0.services.transports import recommendation_service_grpc_transport
from google.ads.google_ads.v0.services.transports import search_term_view_service_grpc_transport
from google.ads.google_ads.v0.services.transports import shared_criterion_service_grpc_transport
from google.ads.google_ads.v0.services.transports import shared_set_service_grpc_transport
from google.ads.google_ads.v0.services.transports import topic_constant_service_grpc_transport
from google.ads.google_ads.v0.services.transports import topic_view_service_grpc_transport
from google.ads.google_ads.v0.services.transports import user_list_service_grpc_transport
from google.ads.google_ads.v0.services.transports import user_interest_service_grpc_transport
from google.ads.google_ads.v0.services.transports import video_service_grpc_transport


class AccountBudgetProposalServiceClient(
        account_budget_proposal_service_client.
        AccountBudgetProposalServiceClient):
    __doc__ = account_budget_proposal_service_client.AccountBudgetProposalServiceClient.__doc__
    enums = enums


class AccountBudgetServiceClient(
        account_budget_service_client.AccountBudgetServiceClient):
    __doc__ = account_budget_service_client.AccountBudgetServiceClient.__doc__
    enums = enums


class AdGroupAdServiceClient(
        ad_group_ad_service_client.AdGroupAdServiceClient):
    __doc__ = ad_group_ad_service_client.AdGroupAdServiceClient.__doc__
    enums = enums


class AdGroupAudienceViewServiceClient(
        ad_group_audience_view_service_client.AdGroupAudienceViewServiceClient):
    __doc__ = ad_group_audience_view_service_client.AdGroupAudienceViewServiceClient.__doc__
    enums = enums


class AdGroupBidModifierServiceClient(
        ad_group_bid_modifier_service_client.AdGroupBidModifierServiceClient):
    __doc__ = ad_group_bid_modifier_service_client.AdGroupBidModifierServiceClient.__doc__
    enums = enums


class AdGroupCriterionServiceClient(
        ad_group_criterion_service_client.AdGroupCriterionServiceClient):
    __doc__ = ad_group_criterion_service_client.AdGroupCriterionServiceClient.__doc__
    enums = enums


class AdGroupFeedServiceClient(
        ad_group_feed_service_client.AdGroupFeedServiceClient):
    __doc__ = ad_group_feed_service_client.AdGroupFeedServiceClient.__doc__
    enums = enums


class AdGroupServiceClient(ad_group_service_client.AdGroupServiceClient):
    __doc__ = ad_group_service_client.AdGroupServiceClient.__doc__
    enums = enums


class AgeRangeViewServiceClient(
        age_range_view_service_client.AgeRangeViewServiceClient):
    __doc__ = age_range_view_service_client.AgeRangeViewServiceClient.__doc__
    enums = enums


class BiddingStrategyServiceClient(
        bidding_strategy_service_client.BiddingStrategyServiceClient):
    __doc__ = bidding_strategy_service_client.BiddingStrategyServiceClient.__doc__
    enums = enums


class BillingSetupServiceClient(
        billing_setup_service_client.BillingSetupServiceClient):
    __doc__ = billing_setup_service_client.BillingSetupServiceClient.__doc__
    enums = enums


class CampaignAudienceViewServiceClient(
        campaign_audience_view_service_client.CampaignAudienceViewServiceClient):
    __doc__ = campaign_audience_view_service_client.CampaignAudienceViewServiceClient.__doc__
    enums = enums


class CampaignBidModifierServiceClient(
        campaign_bid_modifier_service_client.CampaignBidModifierServiceClient):
    __doc__ = campaign_bid_modifier_service_client.CampaignBidModifierServiceClient.__doc__
    enums = enums


class CampaignBudgetServiceClient(
        campaign_budget_service_client.CampaignBudgetServiceClient):
    __doc__ = campaign_budget_service_client.CampaignBudgetServiceClient.__doc__
    enums = enums


class CampaignCriterionServiceClient(
        campaign_criterion_service_client.CampaignCriterionServiceClient):
    __doc__ = campaign_criterion_service_client.CampaignCriterionServiceClient.__doc__
    enums = enums


class CampaignFeedServiceClient(
        campaign_feed_service_client.CampaignFeedServiceClient):
    __doc__ = campaign_feed_service_client.CampaignFeedServiceClient.__doc__
    enums = enums


class CampaignGroupServiceClient(
        campaign_group_service_client.CampaignGroupServiceClient):
    __doc__ = campaign_group_service_client.CampaignGroupServiceClient.__doc__
    enums = enums


class CampaignServiceClient(campaign_service_client.CampaignServiceClient):
    __doc__ = campaign_service_client.CampaignServiceClient.__doc__
    enums = enums


class CampaignSharedSetServiceClient(
        campaign_shared_set_service_client.CampaignSharedSetServiceClient):
    __doc__ = campaign_shared_set_service_client.CampaignSharedSetServiceClient.__doc__
    enums = enums


class CarrierConstantServiceClient(
        carrier_constant_service_client.CarrierConstantServiceClient):
    __doc__ = carrier_constant_service_client.CarrierConstantServiceClient.__doc__
    enums = enums


class ChangeStatusServiceClient(
        change_status_service_client.ChangeStatusServiceClient):
    __doc__ = change_status_service_client.ChangeStatusServiceClient.__doc__
    enums = enums


class ConversionActionServiceClient(
        conversion_action_service_client.ConversionActionServiceClient):
    __doc__ = conversion_action_service_client.ConversionActionServiceClient.__doc__
    enums = enums


class CustomerClientLinkServiceClient(
        customer_client_link_service_client.CustomerClientLinkServiceClient):
    __doc__ = customer_client_link_service_client.CustomerClientLinkServiceClient.__doc__
    enums = enums


class CustomerClientServiceClient(
        customer_client_service_client.CustomerClientServiceClient):
    __doc__ = customer_client_service_client.CustomerClientServiceClient.__doc__
    enums = enums


class CustomerFeedServiceClient(
        customer_feed_service_client.CustomerFeedServiceClient):
    __doc__ = customer_feed_service_client.CustomerFeedServiceClient.__doc__
    enums = enums


class CustomerManagerLinkServiceClient(
        customer_manager_link_service_client.CustomerManagerLinkServiceClient):
    __doc__ = customer_manager_link_service_client.CustomerManagerLinkServiceClient.__doc__
    enums = enums


class CustomerServiceClient(customer_service_client.CustomerServiceClient):
    __doc__ = customer_service_client.CustomerServiceClient.__doc__
    enums = enums


class DisplayKeywordViewServiceClient(
        display_keyword_view_service_client.DisplayKeywordViewServiceClient):
    __doc__ = display_keyword_view_service_client.DisplayKeywordViewServiceClient.__doc__
    enums = enums


class FeedItemServiceClient(feed_item_service_client.FeedItemServiceClient):
    __doc__ = feed_item_service_client.FeedItemServiceClient.__doc__
    enums = enums


class FeedMappingServiceClient(
        feed_mapping_service_client.FeedMappingServiceClient):
    __doc__ = feed_mapping_service_client.FeedMappingServiceClient.__doc__
    enums = enums


class FeedServiceClient(feed_service_client.FeedServiceClient):
    __doc__ = feed_service_client.FeedServiceClient.__doc__
    enums = enums


class GenderViewServiceClient(
        gender_view_service_client.GenderViewServiceClient):
    __doc__ = gender_view_service_client.GenderViewServiceClient.__doc__
    enums = enums


class GeoTargetConstantServiceClient(
        geo_target_constant_service_client.GeoTargetConstantServiceClient):
    __doc__ = geo_target_constant_service_client.GeoTargetConstantServiceClient.__doc__
    enums = enums


class GoogleAdsFieldServiceClient(
        google_ads_field_service_client.GoogleAdsFieldServiceClient):
    __doc__ = google_ads_field_service_client.GoogleAdsFieldServiceClient.__doc__
    enums = enums


class GoogleAdsServiceClient(google_ads_service_client.GoogleAdsServiceClient):
    __doc__ = google_ads_service_client.GoogleAdsServiceClient.__doc__
    enums = enums


class HotelGroupViewServiceClient(
        hotel_group_view_service_client.HotelGroupViewServiceClient):
    __doc__ = hotel_group_view_service_client.HotelGroupViewServiceClient.__doc__
    enums = enums


class HotelPerformanceViewServiceClient(
        hotel_performance_view_service_client.HotelPerformanceViewServiceClient
):
    __doc__ = hotel_performance_view_service_client.HotelPerformanceViewServiceClient.__doc__
    enums = enums


class KeywordPlanAdGroupServiceClient(
        keyword_plan_ad_group_service_client.KeywordPlanAdGroupServiceClient):
    __doc__ = keyword_plan_ad_group_service_client.KeywordPlanAdGroupServiceClient.__doc__
    enums = enums


class KeywordPlanCampaignServiceClient(
        keyword_plan_campaign_service_client.KeywordPlanCampaignServiceClient):
    __doc__ = keyword_plan_campaign_service_client.KeywordPlanCampaignServiceClient.__doc__
    enums = enums


class KeywordPlanIdeaServiceClient(
        keyword_plan_idea_service_client.KeywordPlanIdeaServiceClient):
    __doc__ = keyword_plan_idea_service_client.KeywordPlanIdeaServiceClient.__doc__
    enums = enums


class KeywordPlanKeywordServiceClient(
        keyword_plan_keyword_service_client.KeywordPlanKeywordServiceClient):
    __doc__ = keyword_plan_keyword_service_client.KeywordPlanKeywordServiceClient.__doc__
    enums = enums


class KeywordPlanNegativeKeywordServiceClient(
        keyword_plan_negative_keyword_service_client.
        KeywordPlanNegativeKeywordServiceClient):
    __doc__ = keyword_plan_negative_keyword_service_client.KeywordPlanNegativeKeywordServiceClient.__doc__
    enums = enums


class KeywordPlanServiceClient(
        keyword_plan_service_client.KeywordPlanServiceClient):
    __doc__ = keyword_plan_service_client.KeywordPlanServiceClient.__doc__
    enums = enums


class KeywordViewServiceClient(
        keyword_view_service_client.KeywordViewServiceClient):
    __doc__ = keyword_view_service_client.KeywordViewServiceClient.__doc__
    enums = enums


class LanguageConstantServiceClient(
        language_constant_service_client.LanguageConstantServiceClient):
    __doc__ = language_constant_service_client.LanguageConstantServiceClient.__doc__
    enums = enums


class ManagedPlacementViewServiceClient(
        managed_placement_view_service_client.ManagedPlacementViewServiceClient):
    __doc__ = managed_placement_view_service_client.ManagedPlacementViewServiceClient.__doc__
    enums = enums


class MediaFileServiceClient(media_file_service_client.MediaFileServiceClient):
    __doc__ = media_file_service_client.MediaFileServiceClient.__doc__
    enums = enums


class ParentalStatusViewServiceClient(
        parental_status_view_service_client.ParentalStatusViewServiceClient):
    __doc__ = parental_status_view_service_client.ParentalStatusViewServiceClient.__doc__
    enums = enums


class PaymentsAccountServiceClient(
        payments_account_service_client.PaymentsAccountServiceClient):
    __doc__ = payments_account_service_client.PaymentsAccountServiceClient.__doc__
    enums = enums


class ProductGroupViewServiceClient(
        product_group_view_service_client.ProductGroupViewServiceClient):
    __doc__ = product_group_view_service_client.ProductGroupViewServiceClient.__doc__
    enums = enums


class RecommendationServiceClient(
        recommendation_service_client.RecommendationServiceClient):
    __doc__ = recommendation_service_client.RecommendationServiceClient.__doc__
    enums = enums


class SearchTermViewServiceClient(
        search_term_view_service_client.SearchTermViewServiceClient):
    __doc__ = search_term_view_service_client.SearchTermViewServiceClient.__doc__
    enums = enums


class SharedCriterionServiceClient(
        shared_criterion_service_client.SharedCriterionServiceClient):
    __doc__ = shared_criterion_service_client.SharedCriterionServiceClient.__doc__
    enums = enums


class SharedSetServiceClient(shared_set_service_client.SharedSetServiceClient):
    __doc__ = shared_set_service_client.SharedSetServiceClient.__doc__
    enums = enums


class TopicConstantServiceClient(
        topic_constant_service_client.TopicConstantServiceClient):
    __doc__ = topic_constant_service_client.TopicConstantServiceClient.__doc__
    enums = enums


class TopicViewServiceClient(topic_view_service_client.TopicViewServiceClient):
    __doc__ = topic_view_service_client.TopicViewServiceClient.__doc__
    enums = enums


class UserListServiceClient(user_list_service_client.UserListServiceClient):
    __doc__ = user_list_service_client.UserListServiceClient.__doc__
    enums = enums


class UserInterestServiceClient(
        user_interest_service_client.UserInterestServiceClient):
    __doc__ = user_interest_service_client.UserInterestServiceClient.__doc__
    enums = enums


class VideoServiceClient(video_service_client.VideoServiceClient):
    __doc__ = video_service_client.VideoServiceClient.__doc__
    enums = enums


class AccountBudgetProposalServiceGrpcTransport(
      account_budget_proposal_service_grpc_transport.AccountBudgetProposalServiceGrpcTransport):
    __doc__ = account_budget_proposal_service_grpc_transport.AccountBudgetProposalServiceGrpcTransport.__doc__


class AccountBudgetServiceGrpcTransport(
      account_budget_service_grpc_transport.AccountBudgetServiceGrpcTransport):
    __doc__ = account_budget_service_grpc_transport.AccountBudgetServiceGrpcTransport.__doc__


class AdGroupAdServiceGrpcTransport(
      ad_group_ad_service_grpc_transport.AdGroupAdServiceGrpcTransport):
    __doc__ = ad_group_ad_service_grpc_transport.AdGroupAdServiceGrpcTransport.__doc__


class AdGroupAudienceViewServiceGrpcTransport(
      ad_group_audience_view_service_grpc_transport.AdGroupAudienceViewServiceGrpcTransport):
    __doc__ = ad_group_audience_view_service_grpc_transport.AdGroupAudienceViewServiceGrpcTransport.__doc__


class AdGroupBidModifierServiceGrpcTransport(
      ad_group_bid_modifier_service_grpc_transport.AdGroupBidModifierServiceGrpcTransport):
    __doc__ = ad_group_bid_modifier_service_grpc_transport.AdGroupBidModifierServiceGrpcTransport.__doc__


class AdGroupCriterionServiceGrpcTransport(
      ad_group_criterion_service_grpc_transport.AdGroupCriterionServiceGrpcTransport):
    __doc__ = ad_group_criterion_service_grpc_transport.AdGroupCriterionServiceGrpcTransport.__doc__


class AdGroupFeedServiceGrpcTransport(
      ad_group_feed_service_grpc_transport.AdGroupFeedServiceGrpcTransport):
    __doc__ = ad_group_feed_service_grpc_transport.AdGroupFeedServiceGrpcTransport.__doc__


class AdGroupServiceGrpcTransport(
      ad_group_service_grpc_transport.AdGroupServiceGrpcTransport):
    __doc__ = ad_group_service_grpc_transport.AdGroupServiceGrpcTransport.__doc__


class AgeRangeViewServiceGrpcTransport(
      age_range_view_service_grpc_transport.AgeRangeViewServiceGrpcTransport):
    __doc__ = age_range_view_service_grpc_transport.AgeRangeViewServiceGrpcTransport.__doc__


class BiddingStrategyServiceGrpcTransport(
      bidding_strategy_service_grpc_transport.BiddingStrategyServiceGrpcTransport):
    __doc__ = bidding_strategy_service_grpc_transport.BiddingStrategyServiceGrpcTransport.__doc__


class BillingSetupServiceGrpcTransport(
      billing_setup_service_grpc_transport.BillingSetupServiceGrpcTransport):
    __doc__ = billing_setup_service_grpc_transport.BillingSetupServiceGrpcTransport.__doc__


class CampaignAudienceViewServiceGrpcTransport(
      campaign_audience_view_service_grpc_transport.CampaignAudienceViewServiceGrpcTransport):
    __doc__ = campaign_audience_view_service_grpc_transport.CampaignAudienceViewServiceGrpcTransport.__doc__


class CampaignBidModifierServiceGrpcTransport(
      campaign_bid_modifier_service_grpc_transport.CampaignBidModifierServiceGrpcTransport):
    __doc__ = campaign_bid_modifier_service_grpc_transport.CampaignBidModifierServiceGrpcTransport.__doc__


class CampaignBudgetServiceGrpcTransport(
      campaign_budget_service_grpc_transport.CampaignBudgetServiceGrpcTransport):
    __doc__ = campaign_budget_service_grpc_transport.CampaignBudgetServiceGrpcTransport.__doc__


class CampaignCriterionServiceGrpcTransport(
      campaign_criterion_service_grpc_transport.CampaignCriterionServiceGrpcTransport):
    __doc__ = campaign_criterion_service_grpc_transport.CampaignCriterionServiceGrpcTransport.__doc__


class CampaignFeedServiceGrpcTransport(
      campaign_feed_service_grpc_transport.CampaignFeedServiceGrpcTransport):
    __doc__ = campaign_feed_service_grpc_transport.CampaignFeedServiceGrpcTransport.__doc__


class CampaignGroupServiceGrpcTransport(
      campaign_group_service_grpc_transport.CampaignGroupServiceGrpcTransport):
    __doc__ = campaign_group_service_grpc_transport.CampaignGroupServiceGrpcTransport.__doc__


class CampaignServiceGrpcTransport(
      campaign_service_grpc_transport.CampaignServiceGrpcTransport):
    __doc__ = campaign_service_grpc_transport.CampaignServiceGrpcTransport.__doc__


class CampaignSharedSetServiceGrpcTransport(
      campaign_shared_set_service_grpc_transport.CampaignSharedSetServiceGrpcTransport):
    __doc__ = campaign_shared_set_service_grpc_transport.CampaignSharedSetServiceGrpcTransport.__doc__


class CarrierConstantServiceGrpcTransport(
      carrier_constant_service_grpc_transport.CarrierConstantServiceGrpcTransport):
    __doc__ = carrier_constant_service_grpc_transport.CarrierConstantServiceGrpcTransport.__doc__


class ChangeStatusServiceGrpcTransport(
      change_status_service_grpc_transport.ChangeStatusServiceGrpcTransport):
    __doc__ = change_status_service_grpc_transport.ChangeStatusServiceGrpcTransport.__doc__


class ConversionActionServiceGrpcTransport(
      conversion_action_service_grpc_transport.ConversionActionServiceGrpcTransport):
    __doc__ = conversion_action_service_grpc_transport.ConversionActionServiceGrpcTransport.__doc__


class CustomerClientLinkServiceGrpcTransport(
      customer_client_link_service_grpc_transport.CustomerClientLinkServiceGrpcTransport):
    __doc__ = customer_client_link_service_grpc_transport.CustomerClientLinkServiceGrpcTransport.__doc__


class CustomerClientServiceGrpcTransport(
      customer_client_service_grpc_transport.CustomerClientServiceGrpcTransport):
    __doc__ = customer_client_service_grpc_transport.CustomerClientServiceGrpcTransport.__doc__


class CustomerFeedServiceGrpcTransport(
      customer_feed_service_grpc_transport.CustomerFeedServiceGrpcTransport):
    __doc__ = customer_feed_service_grpc_transport.CustomerFeedServiceGrpcTransport.__doc__


class CustomerManagerLinkServiceGrpcTransport(
      customer_manager_link_service_grpc_transport.CustomerManagerLinkServiceGrpcTransport):
    __doc__ = customer_manager_link_service_grpc_transport.CustomerManagerLinkServiceGrpcTransport.__doc__


class CustomerServiceGrpcTransport(
      customer_service_grpc_transport.CustomerServiceGrpcTransport):
    __doc__ = customer_service_grpc_transport.CustomerServiceGrpcTransport.__doc__


class DisplayKeywordViewServiceGrpcTransport(
      display_keyword_view_service_grpc_transport.DisplayKeywordViewServiceGrpcTransport):
    __doc__ = display_keyword_view_service_grpc_transport.DisplayKeywordViewServiceGrpcTransport.__doc__


class FeedItemServiceGrpcTransport(
      feed_item_service_grpc_transport.FeedItemServiceGrpcTransport):
    __doc__ = feed_item_service_grpc_transport.FeedItemServiceGrpcTransport.__doc__


class FeedMappingServiceGrpcTransport(
      feed_mapping_service_grpc_transport.FeedMappingServiceGrpcTransport):
    __doc__ = feed_mapping_service_grpc_transport.FeedMappingServiceGrpcTransport.__doc__


class FeedServiceGrpcTransport(
      feed_service_grpc_transport.FeedServiceGrpcTransport):
    __doc__ = feed_service_grpc_transport.FeedServiceGrpcTransport.__doc__


class GenderViewServiceGrpcTransport(
      gender_view_service_grpc_transport.GenderViewServiceGrpcTransport):
    __doc__ = gender_view_service_grpc_transport.GenderViewServiceGrpcTransport.__doc__


class GeoTargetConstantServiceGrpcTransport(
      geo_target_constant_service_grpc_transport.GeoTargetConstantServiceGrpcTransport):
    __doc__ = geo_target_constant_service_grpc_transport.GeoTargetConstantServiceGrpcTransport.__doc__


class GoogleAdsFieldServiceGrpcTransport(
      google_ads_field_service_grpc_transport.GoogleAdsFieldServiceGrpcTransport):
    __doc__ = google_ads_field_service_grpc_transport.GoogleAdsFieldServiceGrpcTransport.__doc__


class GoogleAdsServiceGrpcTransport(
      google_ads_service_grpc_transport.GoogleAdsServiceGrpcTransport):
    __doc__ = google_ads_service_grpc_transport.GoogleAdsServiceGrpcTransport.__doc__


class HotelGroupViewServiceGrpcTransport(
      hotel_group_view_service_grpc_transport.HotelGroupViewServiceGrpcTransport):
    __doc__ = hotel_group_view_service_grpc_transport.HotelGroupViewServiceGrpcTransport.__doc__


class HotelPerformanceViewServiceGrpcTransport(
      hotel_performance_view_service_grpc_transport.HotelPerformanceViewServiceGrpcTransport):
    __doc__ = hotel_performance_view_service_grpc_transport.HotelPerformanceViewServiceGrpcTransport.__doc__


class KeywordPlanAdGroupServiceGrpcTransport(
      keyword_plan_ad_group_service_grpc_transport.KeywordPlanAdGroupServiceGrpcTransport):
    __doc__ = keyword_plan_ad_group_service_grpc_transport.KeywordPlanAdGroupServiceGrpcTransport.__doc__


class KeywordPlanCampaignServiceGrpcTransport(
      keyword_plan_campaign_service_grpc_transport.KeywordPlanCampaignServiceGrpcTransport):
    __doc__ = keyword_plan_campaign_service_grpc_transport.KeywordPlanCampaignServiceGrpcTransport.__doc__


class KeywordPlanIdeaServiceGrpcTransport(
      keyword_plan_idea_service_grpc_transport.KeywordPlanIdeaServiceGrpcTransport):
    __doc__ = keyword_plan_idea_service_grpc_transport.KeywordPlanIdeaServiceGrpcTransport.__doc__


class KeywordPlanKeywordServiceGrpcTransport(
      keyword_plan_keyword_service_grpc_transport.KeywordPlanKeywordServiceGrpcTransport):
    __doc__ = keyword_plan_keyword_service_grpc_transport.KeywordPlanKeywordServiceGrpcTransport.__doc__


class KeywordPlanNegativeKeywordServiceGrpcTransport(
      keyword_plan_negative_keyword_service_grpc_transport.KeywordPlanNegativeKeywordServiceGrpcTransport):
    __doc__ = keyword_plan_negative_keyword_service_grpc_transport.KeywordPlanNegativeKeywordServiceGrpcTransport.__doc__


class KeywordPlanServiceGrpcTransport(
      keyword_plan_service_grpc_transport.KeywordPlanServiceGrpcTransport):
    __doc__ = keyword_plan_service_grpc_transport.KeywordPlanServiceGrpcTransport.__doc__


class KeywordViewServiceGrpcTransport(
      keyword_view_service_grpc_transport.KeywordViewServiceGrpcTransport):
    __doc__ = keyword_view_service_grpc_transport.KeywordViewServiceGrpcTransport.__doc__


class LanguageConstantServiceGrpcTransport(
      language_constant_service_grpc_transport.LanguageConstantServiceGrpcTransport):
    __doc__ = language_constant_service_grpc_transport.LanguageConstantServiceGrpcTransport.__doc__


class ManagedPlacementViewServiceGrpcTransport(
      managed_placement_view_service_grpc_transport.ManagedPlacementViewServiceGrpcTransport):
    __doc__ = managed_placement_view_service_grpc_transport.ManagedPlacementViewServiceGrpcTransport.__doc__


class MediaFileServiceGrpcTransport(
      media_file_service_grpc_transport.MediaFileServiceGrpcTransport):
    __doc__ = media_file_service_grpc_transport.MediaFileServiceGrpcTransport.__doc__


class ParentalStatusViewServiceGrpcTransport(
      parental_status_view_service_grpc_transport.ParentalStatusViewServiceGrpcTransport):
    __doc__ = parental_status_view_service_grpc_transport.ParentalStatusViewServiceGrpcTransport.__doc__


class PaymentsAccountServiceGrpcTransport(
      payments_account_service_grpc_transport.PaymentsAccountServiceGrpcTransport):
    __doc__ = payments_account_service_grpc_transport.PaymentsAccountServiceGrpcTransport.__doc__
    enums = enums


class ProductGroupViewServiceGrpcTransport(
      product_group_view_service_grpc_transport.ProductGroupViewServiceGrpcTransport):
    __doc__ = product_group_view_service_grpc_transport.ProductGroupViewServiceGrpcTransport.__doc__


class RecommendationServiceGrpcTransport(
      recommendation_service_grpc_transport.RecommendationServiceGrpcTransport):
    __doc__ = recommendation_service_grpc_transport.RecommendationServiceGrpcTransport.__doc__


class SearchTermViewServiceGrpcTransport(
      search_term_view_service_grpc_transport.SearchTermViewServiceGrpcTransport):
    __doc__ = search_term_view_service_grpc_transport.SearchTermViewServiceGrpcTransport.__doc__


class SharedCriterionServiceGrpcTransport(
      shared_criterion_service_grpc_transport.SharedCriterionServiceGrpcTransport):
    __doc__ = shared_criterion_service_grpc_transport.SharedCriterionServiceGrpcTransport.__doc__


class SharedSetServiceGrpcTransport(
      shared_set_service_grpc_transport.SharedSetServiceGrpcTransport):
    __doc__ = shared_set_service_grpc_transport.SharedSetServiceGrpcTransport.__doc__


class TopicConstantServiceGrpcTransport(
      topic_constant_service_grpc_transport.TopicConstantServiceGrpcTransport):
    __doc__ = topic_constant_service_grpc_transport.TopicConstantServiceGrpcTransport.__doc__


class TopicViewServiceGrpcTransport(
      topic_view_service_grpc_transport.TopicViewServiceGrpcTransport):
    __doc__ = topic_view_service_grpc_transport.TopicViewServiceGrpcTransport.__doc__


class UserInterestServiceGrpcTransport(
      user_interest_service_grpc_transport.UserInterestServiceGrpcTransport):
    __doc__ = user_interest_service_grpc_transport.UserInterestServiceGrpcTransport.__doc__


class UserListServiceGrpcTransport(
      user_list_service_grpc_transport.UserListServiceGrpcTransport):
    __doc__ = user_list_service_grpc_transport.UserListServiceGrpcTransport.__doc__
    enums = enums


class VideoServiceGrpcTransport(
      video_service_grpc_transport.VideoServiceGrpcTransport):
    __doc__ = video_service_grpc_transport.VideoServiceGrpcTransport.__doc__



__all__ = (
    'enums',
    'types',
    'AccountBudgetProposalServiceClient',
    'AccountBudgetProposalServiceGrpcTransport',
    'AccountBudgetServiceClient',
    'AccountBudgetServiceGrpcTransport',
    'AdGroupAdServiceClient',
    'AdGroupAdServiceGrpcTransport',
    'AdGroupAudienceViewServiceClient',
    'AdGroupAudienceViewServiceGrpcTransport',
    'AdGroupBidModifierServiceClient',
    'AdGroupBidModifierServiceGrpcTransport',
    'AdGroupCriterionServiceClient',
    'AdGroupCriterionServiceGrpcTransport',
    'AdGroupFeedServiceClient',
    'AdGroupFeedServiceGrpcTransport',
    'AdGroupServiceClient',
    'AdGroupServiceGrpcTransport',
    'AgeRangeViewServiceClient',
    'AgeRangeViewServiceGrpcTransport',
    'BiddingStrategyServiceClient',
    'BiddingStrategyServiceGrpcTransport',
    'BillingSetupServiceClient',
    'BillingSetupServiceGrpcTransport',
    'CampaignAudienceViewServiceClient',
    'CampaignAudienceViewServiceGrpcTransport',
    'CampaignBidModifierServiceClient',
    'CampaignBidModifierServiceGrpcTransport',
    'CampaignBudgetServiceClient',
    'CampaignBudgetServiceGrpcTransport',
    'CampaignCriterionServiceClient',
    'CampaignCriterionServiceGrpcTransport',
    'CampaignFeedServiceClient',
    'CampaignFeedServiceGrpcTransport',
    'CampaignGroupServiceClient',
    'CampaignGroupServiceGrpcTransport',
    'CampaignServiceClient',
    'CampaignServiceGrpcTransport',
    'CampaignSharedSetServiceClient',
    'CampaignSharedSetServiceGrpcTransport',
    'CarrierConstantServiceClient',
    'CarrierConstantServiceGrpcTransport',
    'ChangeStatusServiceClient',
    'ChangeStatusServiceGrpcTransport',
    'ConversionActionServiceClient',
    'ConversionActionServiceGrpcTransport',
    'CustomerClientLinkServiceClient',
    'CustomerClientLinkServiceGrpcTransport',
    'CustomerClientServiceClient',
    'CustomerClientServiceGrpcTransport',
    'CustomerFeedServiceClient',
    'CustomerFeedServiceGrpcTransport',
    'CustomerManagerLinkServiceClient',
    'CustomerManagerLinkServiceGrpcTransport',
    'CustomerServiceClient',
    'CustomerServiceGrpcTransport',
    'DisplayKeywordViewServiceClient',
    'DisplayKeywordViewServiceGrpcTransport',
    'FeedItemServiceClient',
    'FeedItemServiceGrpcTransport',
    'FeedMappingServiceClient',
    'FeedMappingServiceGrpcTransport',
    'FeedServiceClient',
    'FeedServiceGrpcTransport',
    'GenderViewServiceClient',
    'GenderViewServiceGrpcTransport',
    'GeoTargetConstantServiceClient',
    'GeoTargetConstantServiceGrpcTransport',
    'GoogleAdsFieldServiceClient',
    'GoogleAdsFieldServiceGrpcTransport',
    'GoogleAdsServiceClient',
    'GoogleAdsServiceGrpcTransport',
    'HotelGroupViewServiceClient',
    'HotelGroupViewServiceGrpcTransport',
    'HotelPerformanceViewServiceClient',
    'HotelPerformanceViewServiceGrpcTransport',
    'KeywordPlanAdGroupServiceClient',
    'KeywordPlanAdGroupServiceGrpcTransport',
    'KeywordPlanCampaignServiceClient',
    'KeywordPlanCampaignServiceGrpcTransport',
    'KeywordPlanIdeaServiceClient',
    'KeywordPlanIdeaServiceGrpcTransport',
    'KeywordPlanKeywordServiceClient',
    'KeywordPlanKeywordServiceGrpcTransport',
    'KeywordPlanNegativeKeywordServiceClient',
    'KeywordPlanNegativeKeywordServiceGrpcTransport',
    'KeywordPlanServiceClient',
    'KeywordPlanServiceGrpcTransport',
    'KeywordViewServiceClient',
    'KeywordViewServiceGrpcTransport',
    'LanguageConstantServiceClient',
    'LanguageConstantServiceClientGrpcTransport',
    'ManagedPlacementViewServiceClient',
    'ManagedPlacementViewServiceGrpcTransport',
    'MediaFileServiceClient',
    'MediaFileServiceGrpcTransport',
    'ParentalStatusViewServiceClient',
    'ParentalStatusViewServiceGrpcTransport',
    'PaymentsAccountServiceClient',
    'PaymentsAccountServiceClientGrpcTransport',
    'ProductGroupViewServiceClient',
    'ProductGroupViewServiceGrpcTransport',
    'RecommendationServiceClient',
    'RecommendationServiceGrpcTransport',
    'SearchTermViewServiceClient',
    'SearchTermViewServiceGrpcTransport',
    'SharedCriterionServiceClient',
    'SharedCriterionServiceGrpcTransport',
    'SharedSetServiceClient',
    'SharedSetServiceGrpcTransport',
    'TopicConstantServiceClient',
    'TopicConstantServiceGrpcTransport',
    'TopicViewServiceClient',
    'TopicViewServiceGrpcTransport',
    'UserInterestServiceClient',
    'UserInterestServiceGrpcTransport',
    'UserListServiceClient',
    'UserListServiceClientGrpcTransport',
    'VideoServiceClient',
    'VideoServiceGrpcTransport',
)
