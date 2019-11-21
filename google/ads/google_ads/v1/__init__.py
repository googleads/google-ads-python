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




from google.ads.google_ads.v1 import types
from google.ads.google_ads.v1.services import account_budget_proposal_service_client
from google.ads.google_ads.v1.services import account_budget_service_client
from google.ads.google_ads.v1.services import ad_group_ad_label_service_client
from google.ads.google_ads.v1.services import ad_group_ad_service_client
from google.ads.google_ads.v1.services import ad_group_audience_view_service_client
from google.ads.google_ads.v1.services import ad_group_bid_modifier_service_client
from google.ads.google_ads.v1.services import ad_group_criterion_label_service_client
from google.ads.google_ads.v1.services import ad_group_criterion_service_client
from google.ads.google_ads.v1.services import ad_group_criterion_simulation_service_client
from google.ads.google_ads.v1.services import ad_group_extension_setting_service_client
from google.ads.google_ads.v1.services import ad_group_feed_service_client
from google.ads.google_ads.v1.services import ad_group_label_service_client
from google.ads.google_ads.v1.services import ad_group_service_client
from google.ads.google_ads.v1.services import ad_group_simulation_service_client
from google.ads.google_ads.v1.services import ad_parameter_service_client
from google.ads.google_ads.v1.services import ad_schedule_view_service_client
from google.ads.google_ads.v1.services import age_range_view_service_client
from google.ads.google_ads.v1.services import asset_service_client
from google.ads.google_ads.v1.services import bidding_strategy_service_client
from google.ads.google_ads.v1.services import billing_setup_service_client
from google.ads.google_ads.v1.services import campaign_audience_view_service_client
from google.ads.google_ads.v1.services import campaign_bid_modifier_service_client
from google.ads.google_ads.v1.services import campaign_budget_service_client
from google.ads.google_ads.v1.services import campaign_criterion_service_client
from google.ads.google_ads.v1.services import campaign_criterion_simulation_service_client
from google.ads.google_ads.v1.services import campaign_draft_service_client
from google.ads.google_ads.v1.services import campaign_experiment_service_client
from google.ads.google_ads.v1.services import campaign_extension_setting_service_client
from google.ads.google_ads.v1.services import campaign_feed_service_client
from google.ads.google_ads.v1.services import campaign_label_service_client
from google.ads.google_ads.v1.services import campaign_service_client
from google.ads.google_ads.v1.services import campaign_shared_set_service_client
from google.ads.google_ads.v1.services import carrier_constant_service_client
from google.ads.google_ads.v1.services import change_status_service_client
from google.ads.google_ads.v1.services import click_view_service_client
from google.ads.google_ads.v1.services import conversion_action_service_client
from google.ads.google_ads.v1.services import conversion_adjustment_upload_service_client
from google.ads.google_ads.v1.services import conversion_upload_service_client
from google.ads.google_ads.v1.services import customer_client_link_service_client
from google.ads.google_ads.v1.services import customer_client_service_client
from google.ads.google_ads.v1.services import customer_extension_setting_service_client
from google.ads.google_ads.v1.services import customer_feed_service_client
from google.ads.google_ads.v1.services import customer_label_service_client
from google.ads.google_ads.v1.services import customer_manager_link_service_client
from google.ads.google_ads.v1.services import customer_negative_criterion_service_client
from google.ads.google_ads.v1.services import customer_service_client
from google.ads.google_ads.v1.services import custom_interest_service_client
from google.ads.google_ads.v1.services import detail_placement_view_service_client
from google.ads.google_ads.v1.services import display_keyword_view_service_client
from google.ads.google_ads.v1.services import domain_category_service_client
from google.ads.google_ads.v1.services import dynamic_search_ads_search_term_view_service_client
from google.ads.google_ads.v1.services import enums
from google.ads.google_ads.v1.services import expanded_landing_page_view_service_client
from google.ads.google_ads.v1.services import extension_feed_item_service_client
from google.ads.google_ads.v1.services import feed_item_service_client
from google.ads.google_ads.v1.services import feed_item_target_service_client
from google.ads.google_ads.v1.services import feed_mapping_service_client
from google.ads.google_ads.v1.services import feed_placeholder_view_service_client
from google.ads.google_ads.v1.services import feed_service_client
from google.ads.google_ads.v1.services import gender_view_service_client
from google.ads.google_ads.v1.services import geographic_view_service_client
from google.ads.google_ads.v1.services import geo_target_constant_service_client
from google.ads.google_ads.v1.services import google_ads_field_service_client
from google.ads.google_ads.v1.services import google_ads_service_client
from google.ads.google_ads.v1.services import group_placement_view_service_client
from google.ads.google_ads.v1.services import hotel_group_view_service_client
from google.ads.google_ads.v1.services import hotel_performance_view_service_client
from google.ads.google_ads.v1.services import keyword_plan_ad_group_service_client
from google.ads.google_ads.v1.services import keyword_plan_campaign_service_client
from google.ads.google_ads.v1.services import keyword_plan_idea_service_client
from google.ads.google_ads.v1.services import keyword_plan_keyword_service_client
from google.ads.google_ads.v1.services import keyword_plan_negative_keyword_service_client
from google.ads.google_ads.v1.services import keyword_plan_service_client
from google.ads.google_ads.v1.services import keyword_view_service_client
from google.ads.google_ads.v1.services import label_service_client
from google.ads.google_ads.v1.services import landing_page_view_service_client
from google.ads.google_ads.v1.services import language_constant_service_client
from google.ads.google_ads.v1.services import location_view_service_client
from google.ads.google_ads.v1.services import managed_placement_view_service_client
from google.ads.google_ads.v1.services import media_file_service_client
from google.ads.google_ads.v1.services import merchant_center_link_service_client
from google.ads.google_ads.v1.services import mobile_app_category_constant_service_client
from google.ads.google_ads.v1.services import mobile_device_constant_service_client
from google.ads.google_ads.v1.services import mutate_job_service_client
from google.ads.google_ads.v1.services import operating_system_version_constant_service_client
from google.ads.google_ads.v1.services import paid_organic_search_term_view_service_client
from google.ads.google_ads.v1.services import parental_status_view_service_client
from google.ads.google_ads.v1.services import payments_account_service_client
from google.ads.google_ads.v1.services import product_bidding_category_constant_service_client
from google.ads.google_ads.v1.services import product_group_view_service_client
from google.ads.google_ads.v1.services import recommendation_service_client
from google.ads.google_ads.v1.services import remarketing_action_service_client
from google.ads.google_ads.v1.services import search_term_view_service_client
from google.ads.google_ads.v1.services import shared_criterion_service_client
from google.ads.google_ads.v1.services import shared_set_service_client
from google.ads.google_ads.v1.services import shopping_performance_view_service_client
from google.ads.google_ads.v1.services import topic_constant_service_client
from google.ads.google_ads.v1.services import topic_view_service_client
from google.ads.google_ads.v1.services import user_interest_service_client
from google.ads.google_ads.v1.services import user_list_service_client
from google.ads.google_ads.v1.services import video_service_client
from google.ads.google_ads.v1.services.transports import account_budget_proposal_service_grpc_transport
from google.ads.google_ads.v1.services.transports import account_budget_service_grpc_transport
from google.ads.google_ads.v1.services.transports import ad_group_ad_label_service_grpc_transport
from google.ads.google_ads.v1.services.transports import ad_group_ad_service_grpc_transport
from google.ads.google_ads.v1.services.transports import ad_group_audience_view_service_grpc_transport
from google.ads.google_ads.v1.services.transports import ad_group_bid_modifier_service_grpc_transport
from google.ads.google_ads.v1.services.transports import ad_group_criterion_label_service_grpc_transport
from google.ads.google_ads.v1.services.transports import ad_group_criterion_service_grpc_transport
from google.ads.google_ads.v1.services.transports import ad_group_criterion_simulation_service_grpc_transport
from google.ads.google_ads.v1.services.transports import ad_group_extension_setting_service_grpc_transport
from google.ads.google_ads.v1.services.transports import ad_group_feed_service_grpc_transport
from google.ads.google_ads.v1.services.transports import ad_group_label_service_grpc_transport
from google.ads.google_ads.v1.services.transports import ad_group_service_grpc_transport
from google.ads.google_ads.v1.services.transports import ad_group_simulation_service_grpc_transport
from google.ads.google_ads.v1.services.transports import ad_parameter_service_grpc_transport
from google.ads.google_ads.v1.services.transports import ad_schedule_view_service_grpc_transport
from google.ads.google_ads.v1.services.transports import age_range_view_service_grpc_transport
from google.ads.google_ads.v1.services.transports import asset_service_grpc_transport
from google.ads.google_ads.v1.services.transports import bidding_strategy_service_grpc_transport
from google.ads.google_ads.v1.services.transports import billing_setup_service_grpc_transport
from google.ads.google_ads.v1.services.transports import campaign_audience_view_service_grpc_transport
from google.ads.google_ads.v1.services.transports import campaign_bid_modifier_service_grpc_transport
from google.ads.google_ads.v1.services.transports import campaign_budget_service_grpc_transport
from google.ads.google_ads.v1.services.transports import campaign_criterion_service_grpc_transport
from google.ads.google_ads.v1.services.transports import campaign_criterion_simulation_service_grpc_transport
from google.ads.google_ads.v1.services.transports import campaign_draft_service_grpc_transport
from google.ads.google_ads.v1.services.transports import campaign_experiment_service_grpc_transport
from google.ads.google_ads.v1.services.transports import campaign_extension_setting_service_grpc_transport
from google.ads.google_ads.v1.services.transports import campaign_feed_service_grpc_transport
from google.ads.google_ads.v1.services.transports import campaign_label_service_grpc_transport
from google.ads.google_ads.v1.services.transports import campaign_service_grpc_transport
from google.ads.google_ads.v1.services.transports import campaign_shared_set_service_grpc_transport
from google.ads.google_ads.v1.services.transports import carrier_constant_service_grpc_transport
from google.ads.google_ads.v1.services.transports import change_status_service_grpc_transport
from google.ads.google_ads.v1.services.transports import click_view_service_grpc_transport
from google.ads.google_ads.v1.services.transports import conversion_action_service_grpc_transport
from google.ads.google_ads.v1.services.transports import conversion_adjustment_upload_service_grpc_transport
from google.ads.google_ads.v1.services.transports import conversion_upload_service_grpc_transport
from google.ads.google_ads.v1.services.transports import customer_client_link_service_grpc_transport
from google.ads.google_ads.v1.services.transports import customer_client_service_grpc_transport
from google.ads.google_ads.v1.services.transports import customer_extension_setting_service_grpc_transport
from google.ads.google_ads.v1.services.transports import customer_feed_service_grpc_transport
from google.ads.google_ads.v1.services.transports import customer_label_service_grpc_transport
from google.ads.google_ads.v1.services.transports import customer_manager_link_service_grpc_transport
from google.ads.google_ads.v1.services.transports import customer_negative_criterion_service_grpc_transport
from google.ads.google_ads.v1.services.transports import customer_service_grpc_transport
from google.ads.google_ads.v1.services.transports import custom_interest_service_grpc_transport
from google.ads.google_ads.v1.services.transports import detail_placement_view_service_grpc_transport
from google.ads.google_ads.v1.services.transports import display_keyword_view_service_grpc_transport
from google.ads.google_ads.v1.services.transports import domain_category_service_grpc_transport
from google.ads.google_ads.v1.services.transports import dynamic_search_ads_search_term_view_service_grpc_transport
from google.ads.google_ads.v1.services.transports import expanded_landing_page_view_service_grpc_transport
from google.ads.google_ads.v1.services.transports import extension_feed_item_service_grpc_transport
from google.ads.google_ads.v1.services.transports import feed_item_service_grpc_transport
from google.ads.google_ads.v1.services.transports import feed_item_target_service_grpc_transport
from google.ads.google_ads.v1.services.transports import feed_mapping_service_grpc_transport
from google.ads.google_ads.v1.services.transports import feed_placeholder_view_service_grpc_transport
from google.ads.google_ads.v1.services.transports import feed_service_grpc_transport
from google.ads.google_ads.v1.services.transports import gender_view_service_grpc_transport
from google.ads.google_ads.v1.services.transports import geographic_view_service_grpc_transport
from google.ads.google_ads.v1.services.transports import geo_target_constant_service_grpc_transport
from google.ads.google_ads.v1.services.transports import google_ads_field_service_grpc_transport
from google.ads.google_ads.v1.services.transports import google_ads_service_grpc_transport
from google.ads.google_ads.v1.services.transports import group_placement_view_service_grpc_transport
from google.ads.google_ads.v1.services.transports import hotel_group_view_service_grpc_transport
from google.ads.google_ads.v1.services.transports import hotel_performance_view_service_grpc_transport
from google.ads.google_ads.v1.services.transports import keyword_plan_ad_group_service_grpc_transport
from google.ads.google_ads.v1.services.transports import keyword_plan_campaign_service_grpc_transport
from google.ads.google_ads.v1.services.transports import keyword_plan_idea_service_grpc_transport
from google.ads.google_ads.v1.services.transports import keyword_plan_keyword_service_grpc_transport
from google.ads.google_ads.v1.services.transports import keyword_plan_negative_keyword_service_grpc_transport
from google.ads.google_ads.v1.services.transports import keyword_plan_service_grpc_transport
from google.ads.google_ads.v1.services.transports import keyword_view_service_grpc_transport
from google.ads.google_ads.v1.services.transports import label_service_grpc_transport
from google.ads.google_ads.v1.services.transports import landing_page_view_service_grpc_transport
from google.ads.google_ads.v1.services.transports import language_constant_service_grpc_transport
from google.ads.google_ads.v1.services.transports import location_view_service_grpc_transport
from google.ads.google_ads.v1.services.transports import managed_placement_view_service_grpc_transport
from google.ads.google_ads.v1.services.transports import media_file_service_grpc_transport
from google.ads.google_ads.v1.services.transports import merchant_center_link_service_grpc_transport
from google.ads.google_ads.v1.services.transports import mobile_app_category_constant_service_grpc_transport
from google.ads.google_ads.v1.services.transports import mobile_device_constant_service_grpc_transport
from google.ads.google_ads.v1.services.transports import mutate_job_service_grpc_transport
from google.ads.google_ads.v1.services.transports import operating_system_version_constant_service_grpc_transport
from google.ads.google_ads.v1.services.transports import paid_organic_search_term_view_service_grpc_transport
from google.ads.google_ads.v1.services.transports import parental_status_view_service_grpc_transport
from google.ads.google_ads.v1.services.transports import payments_account_service_grpc_transport
from google.ads.google_ads.v1.services.transports import product_bidding_category_constant_service_grpc_transport
from google.ads.google_ads.v1.services.transports import product_group_view_service_grpc_transport
from google.ads.google_ads.v1.services.transports import recommendation_service_grpc_transport
from google.ads.google_ads.v1.services.transports import remarketing_action_service_grpc_transport
from google.ads.google_ads.v1.services.transports import search_term_view_service_grpc_transport
from google.ads.google_ads.v1.services.transports import shared_criterion_service_grpc_transport
from google.ads.google_ads.v1.services.transports import shared_set_service_grpc_transport
from google.ads.google_ads.v1.services.transports import shopping_performance_view_service_grpc_transport
from google.ads.google_ads.v1.services.transports import topic_constant_service_grpc_transport
from google.ads.google_ads.v1.services.transports import topic_view_service_grpc_transport
from google.ads.google_ads.v1.services.transports import user_interest_service_grpc_transport
from google.ads.google_ads.v1.services.transports import user_list_service_grpc_transport
from google.ads.google_ads.v1.services.transports import video_service_grpc_transport


class AccountBudgetProposalServiceClient(
    account_budget_proposal_service_client.AccountBudgetProposalServiceClient):
    __doc__ = account_budget_proposal_service_client.AccountBudgetProposalServiceClient.__doc__
    enums = enums


class AccountBudgetServiceClient(
    account_budget_service_client.AccountBudgetServiceClient):
    __doc__ = account_budget_service_client.AccountBudgetServiceClient.__doc__
    enums = enums


class AdGroupAdLabelServiceClient(
    ad_group_ad_label_service_client.AdGroupAdLabelServiceClient):
    __doc__ = ad_group_ad_label_service_client.AdGroupAdLabelServiceClient.__doc__
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


class AdGroupCriterionLabelServiceClient(
    ad_group_criterion_label_service_client.AdGroupCriterionLabelServiceClient):
    __doc__ = ad_group_criterion_label_service_client.AdGroupCriterionLabelServiceClient.__doc__
    enums = enums


class AdGroupCriterionServiceClient(
    ad_group_criterion_service_client.AdGroupCriterionServiceClient):
    __doc__ = ad_group_criterion_service_client.AdGroupCriterionServiceClient.__doc__
    enums = enums


class AdGroupCriterionSimulationServiceClient(
    ad_group_criterion_simulation_service_client.AdGroupCriterionSimulationServiceClient):
    __doc__ = ad_group_criterion_simulation_service_client.AdGroupCriterionSimulationServiceClient.__doc__
    enums = enums


class AdGroupExtensionSettingServiceClient(
    ad_group_extension_setting_service_client.AdGroupExtensionSettingServiceClient):
    __doc__ = ad_group_extension_setting_service_client.AdGroupExtensionSettingServiceClient.__doc__
    enums = enums


class AdGroupFeedServiceClient(
    ad_group_feed_service_client.AdGroupFeedServiceClient):
    __doc__ = ad_group_feed_service_client.AdGroupFeedServiceClient.__doc__
    enums = enums


class AdGroupLabelServiceClient(
    ad_group_label_service_client.AdGroupLabelServiceClient):
    __doc__ = ad_group_label_service_client.AdGroupLabelServiceClient.__doc__
    enums = enums


class AdGroupServiceClient(
    ad_group_service_client.AdGroupServiceClient):
    __doc__ = ad_group_service_client.AdGroupServiceClient.__doc__
    enums = enums


class AdGroupSimulationServiceClient(
    ad_group_simulation_service_client.AdGroupSimulationServiceClient):
    __doc__ = ad_group_simulation_service_client.AdGroupSimulationServiceClient.__doc__
    enums = enums


class AdParameterServiceClient(
    ad_parameter_service_client.AdParameterServiceClient):
    __doc__ = ad_parameter_service_client.AdParameterServiceClient.__doc__
    enums = enums


class AdScheduleViewServiceClient(
    ad_schedule_view_service_client.AdScheduleViewServiceClient):
    __doc__ = ad_schedule_view_service_client.AdScheduleViewServiceClient.__doc__
    enums = enums


class AgeRangeViewServiceClient(
    age_range_view_service_client.AgeRangeViewServiceClient):
    __doc__ = age_range_view_service_client.AgeRangeViewServiceClient.__doc__
    enums = enums


class AssetServiceClient(
    asset_service_client.AssetServiceClient):
    __doc__ = asset_service_client.AssetServiceClient.__doc__
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


class CampaignCriterionSimulationServiceClient(
    campaign_criterion_simulation_service_client.CampaignCriterionSimulationServiceClient):
    __doc__ = campaign_criterion_simulation_service_client.CampaignCriterionSimulationServiceClient.__doc__
    enums = enums


class CampaignDraftServiceClient(
    campaign_draft_service_client.CampaignDraftServiceClient):
    __doc__ = campaign_draft_service_client.CampaignDraftServiceClient.__doc__
    enums = enums


class CampaignExperimentServiceClient(
    campaign_experiment_service_client.CampaignExperimentServiceClient):
    __doc__ = campaign_experiment_service_client.CampaignExperimentServiceClient.__doc__
    enums = enums


class CampaignExtensionSettingServiceClient(
    campaign_extension_setting_service_client.CampaignExtensionSettingServiceClient):
    __doc__ = campaign_extension_setting_service_client.CampaignExtensionSettingServiceClient.__doc__
    enums = enums


class CampaignFeedServiceClient(
    campaign_feed_service_client.CampaignFeedServiceClient):
    __doc__ = campaign_feed_service_client.CampaignFeedServiceClient.__doc__
    enums = enums


class CampaignLabelServiceClient(
    campaign_label_service_client.CampaignLabelServiceClient):
    __doc__ = campaign_label_service_client.CampaignLabelServiceClient.__doc__
    enums = enums


class CampaignServiceClient(
    campaign_service_client.CampaignServiceClient):
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


class ClickViewServiceClient(
    click_view_service_client.ClickViewServiceClient):
    __doc__ = click_view_service_client.ClickViewServiceClient.__doc__
    enums = enums


class ConversionActionServiceClient(
    conversion_action_service_client.ConversionActionServiceClient):
    __doc__ = conversion_action_service_client.ConversionActionServiceClient.__doc__
    enums = enums


class ConversionAdjustmentUploadServiceClient(
    conversion_adjustment_upload_service_client.ConversionAdjustmentUploadServiceClient):
    __doc__ = conversion_adjustment_upload_service_client.ConversionAdjustmentUploadServiceClient.__doc__
    enums = enums


class ConversionUploadServiceClient(
    conversion_upload_service_client.ConversionUploadServiceClient):
    __doc__ = conversion_upload_service_client.ConversionUploadServiceClient.__doc__
    enums = enums


class CustomerClientLinkServiceClient(
    customer_client_link_service_client.CustomerClientLinkServiceClient):
    __doc__ = customer_client_link_service_client.CustomerClientLinkServiceClient.__doc__
    enums = enums


class CustomerClientServiceClient(
    customer_client_service_client.CustomerClientServiceClient):
    __doc__ = customer_client_service_client.CustomerClientServiceClient.__doc__
    enums = enums


class CustomerExtensionSettingServiceClient(
    customer_extension_setting_service_client.CustomerExtensionSettingServiceClient):
    __doc__ = customer_extension_setting_service_client.CustomerExtensionSettingServiceClient.__doc__
    enums = enums


class CustomerFeedServiceClient(
    customer_feed_service_client.CustomerFeedServiceClient):
    __doc__ = customer_feed_service_client.CustomerFeedServiceClient.__doc__
    enums = enums


class CustomerLabelServiceClient(
    customer_label_service_client.CustomerLabelServiceClient):
    __doc__ = customer_label_service_client.CustomerLabelServiceClient.__doc__
    enums = enums


class CustomerManagerLinkServiceClient(
    customer_manager_link_service_client.CustomerManagerLinkServiceClient):
    __doc__ = customer_manager_link_service_client.CustomerManagerLinkServiceClient.__doc__
    enums = enums


class CustomerNegativeCriterionServiceClient(
    customer_negative_criterion_service_client.CustomerNegativeCriterionServiceClient):
    __doc__ = customer_negative_criterion_service_client.CustomerNegativeCriterionServiceClient.__doc__
    enums = enums


class CustomerServiceClient(
    customer_service_client.CustomerServiceClient):
    __doc__ = customer_service_client.CustomerServiceClient.__doc__
    enums = enums


class CustomInterestServiceClient(
    custom_interest_service_client.CustomInterestServiceClient):
    __doc__ = custom_interest_service_client.CustomInterestServiceClient.__doc__
    enums = enums


class DetailPlacementViewServiceClient(
    detail_placement_view_service_client.DetailPlacementViewServiceClient):
    __doc__ = detail_placement_view_service_client.DetailPlacementViewServiceClient.__doc__
    enums = enums


class DisplayKeywordViewServiceClient(
    display_keyword_view_service_client.DisplayKeywordViewServiceClient):
    __doc__ = display_keyword_view_service_client.DisplayKeywordViewServiceClient.__doc__
    enums = enums


class DomainCategoryServiceClient(
    domain_category_service_client.DomainCategoryServiceClient):
    __doc__ = domain_category_service_client.DomainCategoryServiceClient.__doc__
    enums = enums


class DynamicSearchAdsSearchTermViewServiceClient(
    dynamic_search_ads_search_term_view_service_client.DynamicSearchAdsSearchTermViewServiceClient):
    __doc__ = dynamic_search_ads_search_term_view_service_client.DynamicSearchAdsSearchTermViewServiceClient.__doc__
    enums = enums


class ExpandedLandingPageViewServiceClient(
    expanded_landing_page_view_service_client.ExpandedLandingPageViewServiceClient):
    __doc__ = expanded_landing_page_view_service_client.ExpandedLandingPageViewServiceClient.__doc__
    enums = enums


class ExtensionFeedItemServiceClient(
    extension_feed_item_service_client.ExtensionFeedItemServiceClient):
    __doc__ = extension_feed_item_service_client.ExtensionFeedItemServiceClient.__doc__
    enums = enums


class FeedItemServiceClient(
    feed_item_service_client.FeedItemServiceClient):
    __doc__ = feed_item_service_client.FeedItemServiceClient.__doc__
    enums = enums


class FeedItemTargetServiceClient(
    feed_item_target_service_client.FeedItemTargetServiceClient):
    __doc__ = feed_item_target_service_client.FeedItemTargetServiceClient.__doc__
    enums = enums


class FeedMappingServiceClient(
    feed_mapping_service_client.FeedMappingServiceClient):
    __doc__ = feed_mapping_service_client.FeedMappingServiceClient.__doc__
    enums = enums


class FeedPlaceholderViewServiceClient(
    feed_placeholder_view_service_client.FeedPlaceholderViewServiceClient):
    __doc__ = feed_placeholder_view_service_client.FeedPlaceholderViewServiceClient.__doc__
    enums = enums


class FeedServiceClient(
    feed_service_client.FeedServiceClient):
    __doc__ = feed_service_client.FeedServiceClient.__doc__
    enums = enums


class GenderViewServiceClient(
    gender_view_service_client.GenderViewServiceClient):
    __doc__ = gender_view_service_client.GenderViewServiceClient.__doc__
    enums = enums


class GeographicViewServiceClient(
    geographic_view_service_client.GeographicViewServiceClient):
    __doc__ = geographic_view_service_client.GeographicViewServiceClient.__doc__
    enums = enums


class GeoTargetConstantServiceClient(
    geo_target_constant_service_client.GeoTargetConstantServiceClient):
    __doc__ = geo_target_constant_service_client.GeoTargetConstantServiceClient.__doc__
    enums = enums


class GoogleAdsFieldServiceClient(
    google_ads_field_service_client.GoogleAdsFieldServiceClient):
    __doc__ = google_ads_field_service_client.GoogleAdsFieldServiceClient.__doc__
    enums = enums


class GoogleAdsServiceClient(
    google_ads_service_client.GoogleAdsServiceClient):
    __doc__ = google_ads_service_client.GoogleAdsServiceClient.__doc__
    enums = enums


class GroupPlacementViewServiceClient(
    group_placement_view_service_client.GroupPlacementViewServiceClient):
    __doc__ = group_placement_view_service_client.GroupPlacementViewServiceClient.__doc__
    enums = enums


class HotelGroupViewServiceClient(
    hotel_group_view_service_client.HotelGroupViewServiceClient):
    __doc__ = hotel_group_view_service_client.HotelGroupViewServiceClient.__doc__
    enums = enums


class HotelPerformanceViewServiceClient(
    hotel_performance_view_service_client.HotelPerformanceViewServiceClient):
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
    keyword_plan_negative_keyword_service_client.KeywordPlanNegativeKeywordServiceClient):
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


class LabelServiceClient(
    label_service_client.LabelServiceClient):
    __doc__ = label_service_client.LabelServiceClient.__doc__
    enums = enums


class LandingPageViewServiceClient(
    landing_page_view_service_client.LandingPageViewServiceClient):
    __doc__ = landing_page_view_service_client.LandingPageViewServiceClient.__doc__
    enums = enums


class LanguageConstantServiceClient(
    language_constant_service_client.LanguageConstantServiceClient):
    __doc__ = language_constant_service_client.LanguageConstantServiceClient.__doc__
    enums = enums


class LocationViewServiceClient(
    location_view_service_client.LocationViewServiceClient):
    __doc__ = location_view_service_client.LocationViewServiceClient.__doc__
    enums = enums


class ManagedPlacementViewServiceClient(
    managed_placement_view_service_client.ManagedPlacementViewServiceClient):
    __doc__ = managed_placement_view_service_client.ManagedPlacementViewServiceClient.__doc__
    enums = enums


class MediaFileServiceClient(
    media_file_service_client.MediaFileServiceClient):
    __doc__ = media_file_service_client.MediaFileServiceClient.__doc__
    enums = enums


class MerchantCenterLinkServiceClient(
    merchant_center_link_service_client.MerchantCenterLinkServiceClient):
    __doc__ = merchant_center_link_service_client.MerchantCenterLinkServiceClient.__doc__
    enums = enums


class MobileAppCategoryConstantServiceClient(
    mobile_app_category_constant_service_client.MobileAppCategoryConstantServiceClient):
    __doc__ = mobile_app_category_constant_service_client.MobileAppCategoryConstantServiceClient.__doc__
    enums = enums


class MobileDeviceConstantServiceClient(
    mobile_device_constant_service_client.MobileDeviceConstantServiceClient):
    __doc__ = mobile_device_constant_service_client.MobileDeviceConstantServiceClient.__doc__
    enums = enums


class MutateJobServiceClient(
    mutate_job_service_client.MutateJobServiceClient):
    __doc__ = mutate_job_service_client.MutateJobServiceClient.__doc__
    enums = enums


class OperatingSystemVersionConstantServiceClient(
    operating_system_version_constant_service_client.OperatingSystemVersionConstantServiceClient):
    __doc__ = operating_system_version_constant_service_client.OperatingSystemVersionConstantServiceClient.__doc__
    enums = enums


class PaidOrganicSearchTermViewServiceClient(
    paid_organic_search_term_view_service_client.PaidOrganicSearchTermViewServiceClient):
    __doc__ = paid_organic_search_term_view_service_client.PaidOrganicSearchTermViewServiceClient.__doc__
    enums = enums


class ParentalStatusViewServiceClient(
    parental_status_view_service_client.ParentalStatusViewServiceClient):
    __doc__ = parental_status_view_service_client.ParentalStatusViewServiceClient.__doc__
    enums = enums


class PaymentsAccountServiceClient(
    payments_account_service_client.PaymentsAccountServiceClient):
    __doc__ = payments_account_service_client.PaymentsAccountServiceClient.__doc__
    enums = enums


class ProductBiddingCategoryConstantServiceClient(
    product_bidding_category_constant_service_client.ProductBiddingCategoryConstantServiceClient):
    __doc__ = product_bidding_category_constant_service_client.ProductBiddingCategoryConstantServiceClient.__doc__
    enums = enums


class ProductGroupViewServiceClient(
    product_group_view_service_client.ProductGroupViewServiceClient):
    __doc__ = product_group_view_service_client.ProductGroupViewServiceClient.__doc__
    enums = enums


class RecommendationServiceClient(
    recommendation_service_client.RecommendationServiceClient):
    __doc__ = recommendation_service_client.RecommendationServiceClient.__doc__
    enums = enums


class RemarketingActionServiceClient(
    remarketing_action_service_client.RemarketingActionServiceClient):
    __doc__ = remarketing_action_service_client.RemarketingActionServiceClient.__doc__
    enums = enums


class SearchTermViewServiceClient(
    search_term_view_service_client.SearchTermViewServiceClient):
    __doc__ = search_term_view_service_client.SearchTermViewServiceClient.__doc__
    enums = enums


class SharedCriterionServiceClient(
    shared_criterion_service_client.SharedCriterionServiceClient):
    __doc__ = shared_criterion_service_client.SharedCriterionServiceClient.__doc__
    enums = enums


class SharedSetServiceClient(
    shared_set_service_client.SharedSetServiceClient):
    __doc__ = shared_set_service_client.SharedSetServiceClient.__doc__
    enums = enums


class ShoppingPerformanceViewServiceClient(
    shopping_performance_view_service_client.ShoppingPerformanceViewServiceClient):
    __doc__ = shopping_performance_view_service_client.ShoppingPerformanceViewServiceClient.__doc__
    enums = enums


class TopicConstantServiceClient(
    topic_constant_service_client.TopicConstantServiceClient):
    __doc__ = topic_constant_service_client.TopicConstantServiceClient.__doc__
    enums = enums


class TopicViewServiceClient(
    topic_view_service_client.TopicViewServiceClient):
    __doc__ = topic_view_service_client.TopicViewServiceClient.__doc__
    enums = enums


class UserInterestServiceClient(
    user_interest_service_client.UserInterestServiceClient):
    __doc__ = user_interest_service_client.UserInterestServiceClient.__doc__
    enums = enums


class UserListServiceClient(
    user_list_service_client.UserListServiceClient):
    __doc__ = user_list_service_client.UserListServiceClient.__doc__
    enums = enums


class VideoServiceClient(
    video_service_client.VideoServiceClient):
    __doc__ = video_service_client.VideoServiceClient.__doc__
    enums = enums


class AccountBudgetProposalServiceGrpcTransport(
    account_budget_proposal_service_grpc_transport.AccountBudgetProposalServiceGrpcTransport):
    __doc__ = account_budget_proposal_service_grpc_transport.AccountBudgetProposalServiceGrpcTransport.__doc__


class AccountBudgetServiceGrpcTransport(
    account_budget_service_grpc_transport.AccountBudgetServiceGrpcTransport):
    __doc__ = account_budget_service_grpc_transport.AccountBudgetServiceGrpcTransport.__doc__


class AdGroupAdLabelServiceGrpcTransport(
    ad_group_ad_label_service_grpc_transport.AdGroupAdLabelServiceGrpcTransport):
    __doc__ = ad_group_ad_label_service_grpc_transport.AdGroupAdLabelServiceGrpcTransport.__doc__


class AdGroupAdServiceGrpcTransport(
    ad_group_ad_service_grpc_transport.AdGroupAdServiceGrpcTransport):
    __doc__ = ad_group_ad_service_grpc_transport.AdGroupAdServiceGrpcTransport.__doc__


class AdGroupAudienceViewServiceGrpcTransport(
    ad_group_audience_view_service_grpc_transport.AdGroupAudienceViewServiceGrpcTransport):
    __doc__ = ad_group_audience_view_service_grpc_transport.AdGroupAudienceViewServiceGrpcTransport.__doc__


class AdGroupBidModifierServiceGrpcTransport(
    ad_group_bid_modifier_service_grpc_transport.AdGroupBidModifierServiceGrpcTransport):
    __doc__ = ad_group_bid_modifier_service_grpc_transport.AdGroupBidModifierServiceGrpcTransport.__doc__


class AdGroupCriterionLabelServiceGrpcTransport(
    ad_group_criterion_label_service_grpc_transport.AdGroupCriterionLabelServiceGrpcTransport):
    __doc__ = ad_group_criterion_label_service_grpc_transport.AdGroupCriterionLabelServiceGrpcTransport.__doc__


class AdGroupCriterionServiceGrpcTransport(
    ad_group_criterion_service_grpc_transport.AdGroupCriterionServiceGrpcTransport):
    __doc__ = ad_group_criterion_service_grpc_transport.AdGroupCriterionServiceGrpcTransport.__doc__


class AdGroupCriterionSimulationServiceGrpcTransport(
    ad_group_criterion_simulation_service_grpc_transport.AdGroupCriterionSimulationServiceGrpcTransport):
    __doc__ = ad_group_criterion_simulation_service_grpc_transport.AdGroupCriterionSimulationServiceGrpcTransport.__doc__


class AdGroupExtensionSettingServiceGrpcTransport(
    ad_group_extension_setting_service_grpc_transport.AdGroupExtensionSettingServiceGrpcTransport):
    __doc__ = ad_group_extension_setting_service_grpc_transport.AdGroupExtensionSettingServiceGrpcTransport.__doc__


class AdGroupFeedServiceGrpcTransport(
    ad_group_feed_service_grpc_transport.AdGroupFeedServiceGrpcTransport):
    __doc__ = ad_group_feed_service_grpc_transport.AdGroupFeedServiceGrpcTransport.__doc__


class AdGroupLabelServiceGrpcTransport(
    ad_group_label_service_grpc_transport.AdGroupLabelServiceGrpcTransport):
    __doc__ = ad_group_label_service_grpc_transport.AdGroupLabelServiceGrpcTransport.__doc__


class AdGroupServiceGrpcTransport(
    ad_group_service_grpc_transport.AdGroupServiceGrpcTransport):
    __doc__ = ad_group_service_grpc_transport.AdGroupServiceGrpcTransport.__doc__


class AdGroupSimulationServiceGrpcTransport(
    ad_group_simulation_service_grpc_transport.AdGroupSimulationServiceGrpcTransport):
    __doc__ = ad_group_simulation_service_grpc_transport.AdGroupSimulationServiceGrpcTransport.__doc__


class AdParameterServiceGrpcTransport(
    ad_parameter_service_grpc_transport.AdParameterServiceGrpcTransport):
    __doc__ = ad_parameter_service_grpc_transport.AdParameterServiceGrpcTransport.__doc__


class AdScheduleViewServiceGrpcTransport(
    ad_schedule_view_service_grpc_transport.AdScheduleViewServiceGrpcTransport):
    __doc__ = ad_schedule_view_service_grpc_transport.AdScheduleViewServiceGrpcTransport.__doc__


class AgeRangeViewServiceGrpcTransport(
    age_range_view_service_grpc_transport.AgeRangeViewServiceGrpcTransport):
    __doc__ = age_range_view_service_grpc_transport.AgeRangeViewServiceGrpcTransport.__doc__


class AssetServiceGrpcTransport(
    asset_service_grpc_transport.AssetServiceGrpcTransport):
    __doc__ = asset_service_grpc_transport.AssetServiceGrpcTransport.__doc__


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


class CampaignCriterionSimulationServiceGrpcTransport(
    campaign_criterion_simulation_service_grpc_transport.CampaignCriterionSimulationServiceGrpcTransport):
    __doc__ = campaign_criterion_simulation_service_grpc_transport.CampaignCriterionSimulationServiceGrpcTransport.__doc__


class CampaignDraftServiceGrpcTransport(
    campaign_draft_service_grpc_transport.CampaignDraftServiceGrpcTransport):
    __doc__ = campaign_draft_service_grpc_transport.CampaignDraftServiceGrpcTransport.__doc__


class CampaignExperimentServiceGrpcTransport(
    campaign_experiment_service_grpc_transport.CampaignExperimentServiceGrpcTransport):
    __doc__ = campaign_experiment_service_grpc_transport.CampaignExperimentServiceGrpcTransport.__doc__


class CampaignExtensionSettingServiceGrpcTransport(
    campaign_extension_setting_service_grpc_transport.CampaignExtensionSettingServiceGrpcTransport):
    __doc__ = campaign_extension_setting_service_grpc_transport.CampaignExtensionSettingServiceGrpcTransport.__doc__


class CampaignFeedServiceGrpcTransport(
    campaign_feed_service_grpc_transport.CampaignFeedServiceGrpcTransport):
    __doc__ = campaign_feed_service_grpc_transport.CampaignFeedServiceGrpcTransport.__doc__


class CampaignLabelServiceGrpcTransport(
    campaign_label_service_grpc_transport.CampaignLabelServiceGrpcTransport):
    __doc__ = campaign_label_service_grpc_transport.CampaignLabelServiceGrpcTransport.__doc__


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


class ClickViewServiceGrpcTransport(
    click_view_service_grpc_transport.ClickViewServiceGrpcTransport):
    __doc__ = click_view_service_grpc_transport.ClickViewServiceGrpcTransport.__doc__


class ConversionActionServiceGrpcTransport(
    conversion_action_service_grpc_transport.ConversionActionServiceGrpcTransport):
    __doc__ = conversion_action_service_grpc_transport.ConversionActionServiceGrpcTransport.__doc__


class ConversionAdjustmentUploadServiceGrpcTransport(
    conversion_adjustment_upload_service_grpc_transport.ConversionAdjustmentUploadServiceGrpcTransport):
    __doc__ = conversion_adjustment_upload_service_grpc_transport.ConversionAdjustmentUploadServiceGrpcTransport.__doc__


class ConversionUploadServiceGrpcTransport(
    conversion_upload_service_grpc_transport.ConversionUploadServiceGrpcTransport):
    __doc__ = conversion_upload_service_grpc_transport.ConversionUploadServiceGrpcTransport.__doc__


class CustomerClientLinkServiceGrpcTransport(
    customer_client_link_service_grpc_transport.CustomerClientLinkServiceGrpcTransport):
    __doc__ = customer_client_link_service_grpc_transport.CustomerClientLinkServiceGrpcTransport.__doc__


class CustomerClientServiceGrpcTransport(
    customer_client_service_grpc_transport.CustomerClientServiceGrpcTransport):
    __doc__ = customer_client_service_grpc_transport.CustomerClientServiceGrpcTransport.__doc__


class CustomerExtensionSettingServiceGrpcTransport(
    customer_extension_setting_service_grpc_transport.CustomerExtensionSettingServiceGrpcTransport):
    __doc__ = customer_extension_setting_service_grpc_transport.CustomerExtensionSettingServiceGrpcTransport.__doc__


class CustomerFeedServiceGrpcTransport(
    customer_feed_service_grpc_transport.CustomerFeedServiceGrpcTransport):
    __doc__ = customer_feed_service_grpc_transport.CustomerFeedServiceGrpcTransport.__doc__


class CustomerLabelServiceGrpcTransport(
    customer_label_service_grpc_transport.CustomerLabelServiceGrpcTransport):
    __doc__ = customer_label_service_grpc_transport.CustomerLabelServiceGrpcTransport.__doc__


class CustomerManagerLinkServiceGrpcTransport(
    customer_manager_link_service_grpc_transport.CustomerManagerLinkServiceGrpcTransport):
    __doc__ = customer_manager_link_service_grpc_transport.CustomerManagerLinkServiceGrpcTransport.__doc__


class CustomerNegativeCriterionServiceGrpcTransport(
    customer_negative_criterion_service_grpc_transport.CustomerNegativeCriterionServiceGrpcTransport):
    __doc__ = customer_negative_criterion_service_grpc_transport.CustomerNegativeCriterionServiceGrpcTransport.__doc__


class CustomerServiceGrpcTransport(
    customer_service_grpc_transport.CustomerServiceGrpcTransport):
    __doc__ = customer_service_grpc_transport.CustomerServiceGrpcTransport.__doc__


class CustomInterestServiceGrpcTransport(
    custom_interest_service_grpc_transport.CustomInterestServiceGrpcTransport):
    __doc__ = custom_interest_service_grpc_transport.CustomInterestServiceGrpcTransport.__doc__


class DetailPlacementViewServiceGrpcTransport(
    detail_placement_view_service_grpc_transport.DetailPlacementViewServiceGrpcTransport):
    __doc__ = detail_placement_view_service_grpc_transport.DetailPlacementViewServiceGrpcTransport.__doc__


class DisplayKeywordViewServiceGrpcTransport(
    display_keyword_view_service_grpc_transport.DisplayKeywordViewServiceGrpcTransport):
    __doc__ = display_keyword_view_service_grpc_transport.DisplayKeywordViewServiceGrpcTransport.__doc__


class DomainCategoryServiceGrpcTransport(
    domain_category_service_grpc_transport.DomainCategoryServiceGrpcTransport):
    __doc__ = domain_category_service_grpc_transport.DomainCategoryServiceGrpcTransport.__doc__


class DynamicSearchAdsSearchTermViewServiceGrpcTransport(
    dynamic_search_ads_search_term_view_service_grpc_transport.DynamicSearchAdsSearchTermViewServiceGrpcTransport):
    __doc__ = dynamic_search_ads_search_term_view_service_grpc_transport.DynamicSearchAdsSearchTermViewServiceGrpcTransport.__doc__


class ExpandedLandingPageViewServiceGrpcTransport(
    expanded_landing_page_view_service_grpc_transport.ExpandedLandingPageViewServiceGrpcTransport):
    __doc__ = expanded_landing_page_view_service_grpc_transport.ExpandedLandingPageViewServiceGrpcTransport.__doc__


class ExtensionFeedItemServiceGrpcTransport(
    extension_feed_item_service_grpc_transport.ExtensionFeedItemServiceGrpcTransport):
    __doc__ = extension_feed_item_service_grpc_transport.ExtensionFeedItemServiceGrpcTransport.__doc__


class FeedItemServiceGrpcTransport(
    feed_item_service_grpc_transport.FeedItemServiceGrpcTransport):
    __doc__ = feed_item_service_grpc_transport.FeedItemServiceGrpcTransport.__doc__


class FeedItemTargetServiceGrpcTransport(
    feed_item_target_service_grpc_transport.FeedItemTargetServiceGrpcTransport):
    __doc__ = feed_item_target_service_grpc_transport.FeedItemTargetServiceGrpcTransport.__doc__


class FeedMappingServiceGrpcTransport(
    feed_mapping_service_grpc_transport.FeedMappingServiceGrpcTransport):
    __doc__ = feed_mapping_service_grpc_transport.FeedMappingServiceGrpcTransport.__doc__


class FeedPlaceholderViewServiceGrpcTransport(
    feed_placeholder_view_service_grpc_transport.FeedPlaceholderViewServiceGrpcTransport):
    __doc__ = feed_placeholder_view_service_grpc_transport.FeedPlaceholderViewServiceGrpcTransport.__doc__


class FeedServiceGrpcTransport(
    feed_service_grpc_transport.FeedServiceGrpcTransport):
    __doc__ = feed_service_grpc_transport.FeedServiceGrpcTransport.__doc__


class GenderViewServiceGrpcTransport(
    gender_view_service_grpc_transport.GenderViewServiceGrpcTransport):
    __doc__ = gender_view_service_grpc_transport.GenderViewServiceGrpcTransport.__doc__


class GeographicViewServiceGrpcTransport(
    geographic_view_service_grpc_transport.GeographicViewServiceGrpcTransport):
    __doc__ = geographic_view_service_grpc_transport.GeographicViewServiceGrpcTransport.__doc__


class GeoTargetConstantServiceGrpcTransport(
    geo_target_constant_service_grpc_transport.GeoTargetConstantServiceGrpcTransport):
    __doc__ = geo_target_constant_service_grpc_transport.GeoTargetConstantServiceGrpcTransport.__doc__


class GoogleAdsFieldServiceGrpcTransport(
    google_ads_field_service_grpc_transport.GoogleAdsFieldServiceGrpcTransport):
    __doc__ = google_ads_field_service_grpc_transport.GoogleAdsFieldServiceGrpcTransport.__doc__


class GoogleAdsServiceGrpcTransport(
    google_ads_service_grpc_transport.GoogleAdsServiceGrpcTransport):
    __doc__ = google_ads_service_grpc_transport.GoogleAdsServiceGrpcTransport.__doc__


class GroupPlacementViewServiceGrpcTransport(
    group_placement_view_service_grpc_transport.GroupPlacementViewServiceGrpcTransport):
    __doc__ = group_placement_view_service_grpc_transport.GroupPlacementViewServiceGrpcTransport.__doc__


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


class LabelServiceGrpcTransport(
    label_service_grpc_transport.LabelServiceGrpcTransport):
    __doc__ = label_service_grpc_transport.LabelServiceGrpcTransport.__doc__


class LandingPageViewServiceGrpcTransport(
    landing_page_view_service_grpc_transport.LandingPageViewServiceGrpcTransport):
    __doc__ = landing_page_view_service_grpc_transport.LandingPageViewServiceGrpcTransport.__doc__


class LanguageConstantServiceGrpcTransport(
    language_constant_service_grpc_transport.LanguageConstantServiceGrpcTransport):
    __doc__ = language_constant_service_grpc_transport.LanguageConstantServiceGrpcTransport.__doc__


class LocationViewServiceGrpcTransport(
    location_view_service_grpc_transport.LocationViewServiceGrpcTransport):
    __doc__ = location_view_service_grpc_transport.LocationViewServiceGrpcTransport.__doc__


class ManagedPlacementViewServiceGrpcTransport(
    managed_placement_view_service_grpc_transport.ManagedPlacementViewServiceGrpcTransport):
    __doc__ = managed_placement_view_service_grpc_transport.ManagedPlacementViewServiceGrpcTransport.__doc__


class MediaFileServiceGrpcTransport(
    media_file_service_grpc_transport.MediaFileServiceGrpcTransport):
    __doc__ = media_file_service_grpc_transport.MediaFileServiceGrpcTransport.__doc__


class MerchantCenterLinkServiceGrpcTransport(
    merchant_center_link_service_grpc_transport.MerchantCenterLinkServiceGrpcTransport):
    __doc__ = merchant_center_link_service_grpc_transport.MerchantCenterLinkServiceGrpcTransport.__doc__


class MobileAppCategoryConstantServiceGrpcTransport(
    mobile_app_category_constant_service_grpc_transport.MobileAppCategoryConstantServiceGrpcTransport):
    __doc__ = mobile_app_category_constant_service_grpc_transport.MobileAppCategoryConstantServiceGrpcTransport.__doc__


class MobileDeviceConstantServiceGrpcTransport(
    mobile_device_constant_service_grpc_transport.MobileDeviceConstantServiceGrpcTransport):
    __doc__ = mobile_device_constant_service_grpc_transport.MobileDeviceConstantServiceGrpcTransport.__doc__


class MutateJobServiceGrpcTransport(
    mutate_job_service_grpc_transport.MutateJobServiceGrpcTransport):
    __doc__ = mutate_job_service_grpc_transport.MutateJobServiceGrpcTransport.__doc__


class OperatingSystemVersionConstantServiceGrpcTransport(
    operating_system_version_constant_service_grpc_transport.OperatingSystemVersionConstantServiceGrpcTransport):
    __doc__ = operating_system_version_constant_service_grpc_transport.OperatingSystemVersionConstantServiceGrpcTransport.__doc__


class PaidOrganicSearchTermViewServiceGrpcTransport(
    paid_organic_search_term_view_service_grpc_transport.PaidOrganicSearchTermViewServiceGrpcTransport):
    __doc__ = paid_organic_search_term_view_service_grpc_transport.PaidOrganicSearchTermViewServiceGrpcTransport.__doc__


class ParentalStatusViewServiceGrpcTransport(
    parental_status_view_service_grpc_transport.ParentalStatusViewServiceGrpcTransport):
    __doc__ = parental_status_view_service_grpc_transport.ParentalStatusViewServiceGrpcTransport.__doc__


class PaymentsAccountServiceGrpcTransport(
    payments_account_service_grpc_transport.PaymentsAccountServiceGrpcTransport):
    __doc__ = payments_account_service_grpc_transport.PaymentsAccountServiceGrpcTransport.__doc__


class ProductBiddingCategoryConstantServiceGrpcTransport(
    product_bidding_category_constant_service_grpc_transport.ProductBiddingCategoryConstantServiceGrpcTransport):
    __doc__ = product_bidding_category_constant_service_grpc_transport.ProductBiddingCategoryConstantServiceGrpcTransport.__doc__


class ProductGroupViewServiceGrpcTransport(
    product_group_view_service_grpc_transport.ProductGroupViewServiceGrpcTransport):
    __doc__ = product_group_view_service_grpc_transport.ProductGroupViewServiceGrpcTransport.__doc__


class RecommendationServiceGrpcTransport(
    recommendation_service_grpc_transport.RecommendationServiceGrpcTransport):
    __doc__ = recommendation_service_grpc_transport.RecommendationServiceGrpcTransport.__doc__


class RemarketingActionServiceGrpcTransport(
    remarketing_action_service_grpc_transport.RemarketingActionServiceGrpcTransport):
    __doc__ = remarketing_action_service_grpc_transport.RemarketingActionServiceGrpcTransport.__doc__


class SearchTermViewServiceGrpcTransport(
    search_term_view_service_grpc_transport.SearchTermViewServiceGrpcTransport):
    __doc__ = search_term_view_service_grpc_transport.SearchTermViewServiceGrpcTransport.__doc__


class SharedCriterionServiceGrpcTransport(
    shared_criterion_service_grpc_transport.SharedCriterionServiceGrpcTransport):
    __doc__ = shared_criterion_service_grpc_transport.SharedCriterionServiceGrpcTransport.__doc__


class SharedSetServiceGrpcTransport(
    shared_set_service_grpc_transport.SharedSetServiceGrpcTransport):
    __doc__ = shared_set_service_grpc_transport.SharedSetServiceGrpcTransport.__doc__


class ShoppingPerformanceViewServiceGrpcTransport(
    shopping_performance_view_service_grpc_transport.ShoppingPerformanceViewServiceGrpcTransport):
    __doc__ = shopping_performance_view_service_grpc_transport.ShoppingPerformanceViewServiceGrpcTransport.__doc__


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


class VideoServiceGrpcTransport(
    video_service_grpc_transport.VideoServiceGrpcTransport):
    __doc__ = video_service_grpc_transport.VideoServiceGrpcTransport.__doc__


__all__ = (
    'enums',
    'types',
    'AccountBudgetProposalServiceClient',
    'AccountBudgetServiceClient',
    'AdGroupAdLabelServiceClient',
    'AdGroupAdServiceClient',
    'AdGroupAudienceViewServiceClient',
    'AdGroupBidModifierServiceClient',
    'AdGroupCriterionLabelServiceClient',
    'AdGroupCriterionServiceClient',
    'AdGroupCriterionSimulationServiceClient',
    'AdGroupExtensionSettingServiceClient',
    'AdGroupFeedServiceClient',
    'AdGroupLabelServiceClient',
    'AdGroupServiceClient',
    'AdGroupSimulationServiceClient',
    'AdParameterServiceClient',
    'AdScheduleViewServiceClient',
    'AgeRangeViewServiceClient',
    'AssetServiceClient',
    'BiddingStrategyServiceClient',
    'BillingSetupServiceClient',
    'CampaignAudienceViewServiceClient',
    'CampaignBidModifierServiceClient',
    'CampaignBudgetServiceClient',
    'CampaignCriterionServiceClient',
    'CampaignCriterionSimulationServiceClient',
    'CampaignDraftServiceClient',
    'CampaignExperimentServiceClient',
    'CampaignExtensionSettingServiceClient',
    'CampaignFeedServiceClient',
    'CampaignLabelServiceClient',
    'CampaignServiceClient',
    'CampaignSharedSetServiceClient',
    'CarrierConstantServiceClient',
    'ChangeStatusServiceClient',
    'ClickViewServiceClient',
    'ConversionActionServiceClient',
    'ConversionAdjustmentUploadServiceClient',
    'ConversionUploadServiceClient',
    'CustomerClientLinkServiceClient',
    'CustomerClientServiceClient',
    'CustomerExtensionSettingServiceClient',
    'CustomerFeedServiceClient',
    'CustomerLabelServiceClient',
    'CustomerManagerLinkServiceClient',
    'CustomerNegativeCriterionServiceClient',
    'CustomerServiceClient',
    'CustomInterestServiceClient',
    'DetailPlacementViewServiceClient',
    'DisplayKeywordViewServiceClient',
    'DomainCategoryServiceClient',
    'DynamicSearchAdsSearchTermViewServiceClient',
    'ExpandedLandingPageViewServiceClient',
    'ExtensionFeedItemServiceClient',
    'FeedItemServiceClient',
    'FeedItemTargetServiceClient',
    'FeedMappingServiceClient',
    'FeedPlaceholderViewServiceClient',
    'FeedServiceClient',
    'GenderViewServiceClient',
    'GeographicViewServiceClient',
    'GeoTargetConstantServiceClient',
    'GoogleAdsFieldServiceClient',
    'GoogleAdsServiceClient',
    'GroupPlacementViewServiceClient',
    'HotelGroupViewServiceClient',
    'HotelPerformanceViewServiceClient',
    'KeywordPlanAdGroupServiceClient',
    'KeywordPlanCampaignServiceClient',
    'KeywordPlanIdeaServiceClient',
    'KeywordPlanKeywordServiceClient',
    'KeywordPlanNegativeKeywordServiceClient',
    'KeywordPlanServiceClient',
    'KeywordViewServiceClient',
    'LabelServiceClient',
    'LandingPageViewServiceClient',
    'LanguageConstantServiceClient',
    'LocationViewServiceClient',
    'ManagedPlacementViewServiceClient',
    'MediaFileServiceClient',
    'MerchantCenterLinkServiceClient',
    'MobileAppCategoryConstantServiceClient',
    'MobileDeviceConstantServiceClient',
    'MutateJobServiceClient',
    'OperatingSystemVersionConstantServiceClient',
    'PaidOrganicSearchTermViewServiceClient',
    'ParentalStatusViewServiceClient',
    'PaymentsAccountServiceClient',
    'ProductBiddingCategoryConstantServiceClient',
    'ProductGroupViewServiceClient',
    'RecommendationServiceClient',
    'RemarketingActionServiceClient',
    'SearchTermViewServiceClient',
    'SharedCriterionServiceClient',
    'SharedSetServiceClient',
    'ShoppingPerformanceViewServiceClient',
    'TopicConstantServiceClient',
    'TopicViewServiceClient',
    'UserInterestServiceClient',
    'UserListServiceClient',
    'VideoServiceClient',
    'AccountBudgetProposalServiceGrpcTransport',
    'AccountBudgetServiceGrpcTransport',
    'AdGroupAdLabelServiceGrpcTransport',
    'AdGroupAdServiceGrpcTransport',
    'AdGroupAudienceViewServiceGrpcTransport',
    'AdGroupBidModifierServiceGrpcTransport',
    'AdGroupCriterionLabelServiceGrpcTransport',
    'AdGroupCriterionServiceGrpcTransport',
    'AdGroupCriterionSimulationServiceGrpcTransport',
    'AdGroupExtensionSettingServiceGrpcTransport',
    'AdGroupFeedServiceGrpcTransport',
    'AdGroupLabelServiceGrpcTransport',
    'AdGroupServiceGrpcTransport',
    'AdGroupSimulationServiceGrpcTransport',
    'AdParameterServiceGrpcTransport',
    'AdScheduleViewServiceGrpcTransport',
    'AgeRangeViewServiceGrpcTransport',
    'AssetServiceGrpcTransport',
    'BiddingStrategyServiceGrpcTransport',
    'BillingSetupServiceGrpcTransport',
    'CampaignAudienceViewServiceGrpcTransport',
    'CampaignBidModifierServiceGrpcTransport',
    'CampaignBudgetServiceGrpcTransport',
    'CampaignCriterionServiceGrpcTransport',
    'CampaignCriterionSimulationServiceGrpcTransport',
    'CampaignDraftServiceGrpcTransport',
    'CampaignExperimentServiceGrpcTransport',
    'CampaignExtensionSettingServiceGrpcTransport',
    'CampaignFeedServiceGrpcTransport',
    'CampaignLabelServiceGrpcTransport',
    'CampaignServiceGrpcTransport',
    'CampaignSharedSetServiceGrpcTransport',
    'CarrierConstantServiceGrpcTransport',
    'ChangeStatusServiceGrpcTransport',
    'ClickViewServiceGrpcTransport',
    'ConversionActionServiceGrpcTransport',
    'ConversionAdjustmentUploadServiceGrpcTransport',
    'ConversionUploadServiceGrpcTransport',
    'CustomerClientLinkServiceGrpcTransport',
    'CustomerClientServiceGrpcTransport',
    'CustomerExtensionSettingServiceGrpcTransport',
    'CustomerFeedServiceGrpcTransport',
    'CustomerLabelServiceGrpcTransport',
    'CustomerManagerLinkServiceGrpcTransport',
    'CustomerNegativeCriterionServiceGrpcTransport',
    'CustomerServiceGrpcTransport',
    'CustomInterestServiceGrpcTransport',
    'DetailPlacementViewServiceGrpcTransport',
    'DisplayKeywordViewServiceGrpcTransport',
    'DomainCategoryServiceGrpcTransport',
    'DynamicSearchAdsSearchTermViewServiceGrpcTransport',
    'ExpandedLandingPageViewServiceGrpcTransport',
    'ExtensionFeedItemServiceGrpcTransport',
    'FeedItemServiceGrpcTransport',
    'FeedItemTargetServiceGrpcTransport',
    'FeedMappingServiceGrpcTransport',
    'FeedPlaceholderViewServiceGrpcTransport',
    'FeedServiceGrpcTransport',
    'GenderViewServiceGrpcTransport',
    'GeographicViewServiceGrpcTransport',
    'GeoTargetConstantServiceGrpcTransport',
    'GoogleAdsFieldServiceGrpcTransport',
    'GoogleAdsServiceGrpcTransport',
    'GroupPlacementViewServiceGrpcTransport',
    'HotelGroupViewServiceGrpcTransport',
    'HotelPerformanceViewServiceGrpcTransport',
    'KeywordPlanAdGroupServiceGrpcTransport',
    'KeywordPlanCampaignServiceGrpcTransport',
    'KeywordPlanIdeaServiceGrpcTransport',
    'KeywordPlanKeywordServiceGrpcTransport',
    'KeywordPlanNegativeKeywordServiceGrpcTransport',
    'KeywordPlanServiceGrpcTransport',
    'KeywordViewServiceGrpcTransport',
    'LabelServiceGrpcTransport',
    'LandingPageViewServiceGrpcTransport',
    'LanguageConstantServiceGrpcTransport',
    'LocationViewServiceGrpcTransport',
    'ManagedPlacementViewServiceGrpcTransport',
    'MediaFileServiceGrpcTransport',
    'MerchantCenterLinkServiceGrpcTransport',
    'MobileAppCategoryConstantServiceGrpcTransport',
    'MobileDeviceConstantServiceGrpcTransport',
    'MutateJobServiceGrpcTransport',
    'OperatingSystemVersionConstantServiceGrpcTransport',
    'PaidOrganicSearchTermViewServiceGrpcTransport',
    'ParentalStatusViewServiceGrpcTransport',
    'PaymentsAccountServiceGrpcTransport',
    'ProductBiddingCategoryConstantServiceGrpcTransport',
    'ProductGroupViewServiceGrpcTransport',
    'RecommendationServiceGrpcTransport',
    'RemarketingActionServiceGrpcTransport',
    'SearchTermViewServiceGrpcTransport',
    'SharedCriterionServiceGrpcTransport',
    'SharedSetServiceGrpcTransport',
    'ShoppingPerformanceViewServiceGrpcTransport',
    'TopicConstantServiceGrpcTransport',
    'TopicViewServiceGrpcTransport',
    'UserInterestServiceGrpcTransport',
    'UserListServiceGrpcTransport',
    'VideoServiceGrpcTransport',
)
