# -*- coding: utf-8 -*-
#
# Copyright 2019 Google LLC
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

import sys

from google.api_core.protobuf_helpers import get_messages

from google.ads.google_ads.v1.proto.common import ad_asset_pb2
from google.ads.google_ads.v1.proto.common import ad_type_infos_pb2
from google.ads.google_ads.v1.proto.common import asset_types_pb2
from google.ads.google_ads.v1.proto.common import bidding_pb2
from google.ads.google_ads.v1.proto.common import click_location_pb2
from google.ads.google_ads.v1.proto.common import criteria_pb2
from google.ads.google_ads.v1.proto.common import criterion_category_availability_pb2
from google.ads.google_ads.v1.proto.common import custom_parameter_pb2
from google.ads.google_ads.v1.proto.common import dates_pb2
from google.ads.google_ads.v1.proto.common import explorer_auto_optimizer_setting_pb2
from google.ads.google_ads.v1.proto.common import extensions_pb2
from google.ads.google_ads.v1.proto.common import feed_common_pb2
from google.ads.google_ads.v1.proto.common import final_app_url_pb2
from google.ads.google_ads.v1.proto.common import frequency_cap_pb2
from google.ads.google_ads.v1.proto.common import keyword_plan_common_pb2
from google.ads.google_ads.v1.proto.common import matching_function_pb2
from google.ads.google_ads.v1.proto.common import metrics_pb2
from google.ads.google_ads.v1.proto.common import policy_pb2
from google.ads.google_ads.v1.proto.common import real_time_bidding_setting_pb2
from google.ads.google_ads.v1.proto.common import segments_pb2
from google.ads.google_ads.v1.proto.common import simulation_pb2
from google.ads.google_ads.v1.proto.common import tag_snippet_pb2
from google.ads.google_ads.v1.proto.common import targeting_setting_pb2
from google.ads.google_ads.v1.proto.common import text_label_pb2
from google.ads.google_ads.v1.proto.common import url_collection_pb2
from google.ads.google_ads.v1.proto.common import user_lists_pb2
from google.ads.google_ads.v1.proto.common import value_pb2
from google.ads.google_ads.v1.proto.enums import access_reason_pb2
from google.ads.google_ads.v1.proto.enums import account_budget_proposal_status_pb2
from google.ads.google_ads.v1.proto.enums import account_budget_proposal_type_pb2
from google.ads.google_ads.v1.proto.enums import account_budget_status_pb2
from google.ads.google_ads.v1.proto.enums import ad_customizer_placeholder_field_pb2
from google.ads.google_ads.v1.proto.enums import ad_group_ad_rotation_mode_pb2
from google.ads.google_ads.v1.proto.enums import ad_group_ad_status_pb2
from google.ads.google_ads.v1.proto.enums import ad_group_criterion_approval_status_pb2
from google.ads.google_ads.v1.proto.enums import ad_group_criterion_status_pb2
from google.ads.google_ads.v1.proto.enums import ad_group_status_pb2
from google.ads.google_ads.v1.proto.enums import ad_group_type_pb2
from google.ads.google_ads.v1.proto.enums import ad_network_type_pb2
from google.ads.google_ads.v1.proto.enums import ad_serving_optimization_status_pb2
from google.ads.google_ads.v1.proto.enums import ad_strength_pb2
from google.ads.google_ads.v1.proto.enums import ad_type_pb2
from google.ads.google_ads.v1.proto.enums import advertising_channel_sub_type_pb2
from google.ads.google_ads.v1.proto.enums import advertising_channel_type_pb2
from google.ads.google_ads.v1.proto.enums import affiliate_location_feed_relationship_type_pb2
from google.ads.google_ads.v1.proto.enums import affiliate_location_placeholder_field_pb2
from google.ads.google_ads.v1.proto.enums import age_range_type_pb2
from google.ads.google_ads.v1.proto.enums import app_campaign_app_store_pb2
from google.ads.google_ads.v1.proto.enums import app_campaign_bidding_strategy_goal_type_pb2
from google.ads.google_ads.v1.proto.enums import app_payment_model_type_pb2
from google.ads.google_ads.v1.proto.enums import app_placeholder_field_pb2
from google.ads.google_ads.v1.proto.enums import app_store_pb2
from google.ads.google_ads.v1.proto.enums import app_url_operating_system_type_pb2
from google.ads.google_ads.v1.proto.enums import asset_type_pb2
from google.ads.google_ads.v1.proto.enums import attribution_model_pb2
from google.ads.google_ads.v1.proto.enums import bid_modifier_source_pb2
from google.ads.google_ads.v1.proto.enums import bidding_source_pb2
from google.ads.google_ads.v1.proto.enums import bidding_strategy_status_pb2
from google.ads.google_ads.v1.proto.enums import bidding_strategy_type_pb2
from google.ads.google_ads.v1.proto.enums import billing_setup_status_pb2
from google.ads.google_ads.v1.proto.enums import brand_safety_suitability_pb2
from google.ads.google_ads.v1.proto.enums import budget_delivery_method_pb2
from google.ads.google_ads.v1.proto.enums import budget_period_pb2
from google.ads.google_ads.v1.proto.enums import budget_status_pb2
from google.ads.google_ads.v1.proto.enums import budget_type_pb2
from google.ads.google_ads.v1.proto.enums import call_conversion_reporting_state_pb2
from google.ads.google_ads.v1.proto.enums import call_placeholder_field_pb2
from google.ads.google_ads.v1.proto.enums import callout_placeholder_field_pb2
from google.ads.google_ads.v1.proto.enums import campaign_criterion_status_pb2
from google.ads.google_ads.v1.proto.enums import campaign_draft_status_pb2
from google.ads.google_ads.v1.proto.enums import campaign_experiment_status_pb2
from google.ads.google_ads.v1.proto.enums import campaign_experiment_traffic_split_type_pb2
from google.ads.google_ads.v1.proto.enums import campaign_experiment_type_pb2
from google.ads.google_ads.v1.proto.enums import campaign_serving_status_pb2
from google.ads.google_ads.v1.proto.enums import campaign_shared_set_status_pb2
from google.ads.google_ads.v1.proto.enums import campaign_status_pb2
from google.ads.google_ads.v1.proto.enums import change_status_operation_pb2
from google.ads.google_ads.v1.proto.enums import change_status_resource_type_pb2
from google.ads.google_ads.v1.proto.enums import click_type_pb2
from google.ads.google_ads.v1.proto.enums import content_label_type_pb2
from google.ads.google_ads.v1.proto.enums import conversion_action_category_pb2
from google.ads.google_ads.v1.proto.enums import conversion_action_counting_type_pb2
from google.ads.google_ads.v1.proto.enums import conversion_action_status_pb2
from google.ads.google_ads.v1.proto.enums import conversion_action_type_pb2
from google.ads.google_ads.v1.proto.enums import conversion_adjustment_type_pb2
from google.ads.google_ads.v1.proto.enums import conversion_attribution_event_type_pb2
from google.ads.google_ads.v1.proto.enums import conversion_lag_bucket_pb2
from google.ads.google_ads.v1.proto.enums import conversion_or_adjustment_lag_bucket_pb2
from google.ads.google_ads.v1.proto.enums import criterion_category_channel_availability_mode_pb2
from google.ads.google_ads.v1.proto.enums import criterion_category_locale_availability_mode_pb2
from google.ads.google_ads.v1.proto.enums import criterion_system_serving_status_pb2
from google.ads.google_ads.v1.proto.enums import criterion_type_pb2
from google.ads.google_ads.v1.proto.enums import custom_interest_member_type_pb2
from google.ads.google_ads.v1.proto.enums import custom_interest_status_pb2
from google.ads.google_ads.v1.proto.enums import custom_interest_type_pb2
from google.ads.google_ads.v1.proto.enums import custom_placeholder_field_pb2
from google.ads.google_ads.v1.proto.enums import customer_match_upload_key_type_pb2
from google.ads.google_ads.v1.proto.enums import customer_pay_per_conversion_eligibility_failure_reason_pb2
from google.ads.google_ads.v1.proto.enums import data_driven_model_status_pb2
from google.ads.google_ads.v1.proto.enums import day_of_week_pb2
from google.ads.google_ads.v1.proto.enums import device_pb2
from google.ads.google_ads.v1.proto.enums import display_ad_format_setting_pb2
from google.ads.google_ads.v1.proto.enums import display_upload_product_type_pb2
from google.ads.google_ads.v1.proto.enums import dsa_page_feed_criterion_field_pb2
from google.ads.google_ads.v1.proto.enums import education_placeholder_field_pb2
from google.ads.google_ads.v1.proto.enums import extension_setting_device_pb2
from google.ads.google_ads.v1.proto.enums import extension_type_pb2
from google.ads.google_ads.v1.proto.enums import external_conversion_source_pb2
from google.ads.google_ads.v1.proto.enums import feed_attribute_type_pb2
from google.ads.google_ads.v1.proto.enums import feed_item_quality_approval_status_pb2
from google.ads.google_ads.v1.proto.enums import feed_item_quality_disapproval_reason_pb2
from google.ads.google_ads.v1.proto.enums import feed_item_status_pb2
from google.ads.google_ads.v1.proto.enums import feed_item_target_device_pb2
from google.ads.google_ads.v1.proto.enums import feed_item_target_type_pb2
from google.ads.google_ads.v1.proto.enums import feed_item_validation_status_pb2
from google.ads.google_ads.v1.proto.enums import feed_link_status_pb2
from google.ads.google_ads.v1.proto.enums import feed_mapping_criterion_type_pb2
from google.ads.google_ads.v1.proto.enums import feed_mapping_status_pb2
from google.ads.google_ads.v1.proto.enums import feed_origin_pb2
from google.ads.google_ads.v1.proto.enums import feed_status_pb2
from google.ads.google_ads.v1.proto.enums import flight_placeholder_field_pb2
from google.ads.google_ads.v1.proto.enums import frequency_cap_event_type_pb2
from google.ads.google_ads.v1.proto.enums import frequency_cap_level_pb2
from google.ads.google_ads.v1.proto.enums import frequency_cap_time_unit_pb2
from google.ads.google_ads.v1.proto.enums import gender_type_pb2
from google.ads.google_ads.v1.proto.enums import geo_target_constant_status_pb2
from google.ads.google_ads.v1.proto.enums import geo_targeting_restriction_pb2
from google.ads.google_ads.v1.proto.enums import geo_targeting_type_pb2
from google.ads.google_ads.v1.proto.enums import google_ads_field_category_pb2
from google.ads.google_ads.v1.proto.enums import google_ads_field_data_type_pb2
from google.ads.google_ads.v1.proto.enums import hotel_date_selection_type_pb2
from google.ads.google_ads.v1.proto.enums import hotel_placeholder_field_pb2
from google.ads.google_ads.v1.proto.enums import hotel_rate_type_pb2
from google.ads.google_ads.v1.proto.enums import income_range_type_pb2
from google.ads.google_ads.v1.proto.enums import interaction_event_type_pb2
from google.ads.google_ads.v1.proto.enums import interaction_type_pb2
from google.ads.google_ads.v1.proto.enums import job_placeholder_field_pb2
from google.ads.google_ads.v1.proto.enums import keyword_match_type_pb2
from google.ads.google_ads.v1.proto.enums import keyword_plan_competition_level_pb2
from google.ads.google_ads.v1.proto.enums import keyword_plan_forecast_interval_pb2
from google.ads.google_ads.v1.proto.enums import keyword_plan_network_pb2
from google.ads.google_ads.v1.proto.enums import label_status_pb2
from google.ads.google_ads.v1.proto.enums import legacy_app_install_ad_app_store_pb2
from google.ads.google_ads.v1.proto.enums import listing_custom_attribute_index_pb2
from google.ads.google_ads.v1.proto.enums import listing_group_type_pb2
from google.ads.google_ads.v1.proto.enums import local_placeholder_field_pb2
from google.ads.google_ads.v1.proto.enums import location_extension_targeting_criterion_field_pb2
from google.ads.google_ads.v1.proto.enums import location_group_radius_units_pb2
from google.ads.google_ads.v1.proto.enums import location_placeholder_field_pb2
from google.ads.google_ads.v1.proto.enums import manager_link_status_pb2
from google.ads.google_ads.v1.proto.enums import matching_function_context_type_pb2
from google.ads.google_ads.v1.proto.enums import matching_function_operator_pb2
from google.ads.google_ads.v1.proto.enums import media_type_pb2
from google.ads.google_ads.v1.proto.enums import merchant_center_link_status_pb2
from google.ads.google_ads.v1.proto.enums import message_placeholder_field_pb2
from google.ads.google_ads.v1.proto.enums import mime_type_pb2
from google.ads.google_ads.v1.proto.enums import minute_of_hour_pb2
from google.ads.google_ads.v1.proto.enums import mobile_device_type_pb2
from google.ads.google_ads.v1.proto.enums import month_of_year_pb2
from google.ads.google_ads.v1.proto.enums import mutate_job_status_pb2
from google.ads.google_ads.v1.proto.enums import negative_geo_target_type_pb2
from google.ads.google_ads.v1.proto.enums import operating_system_version_operator_type_pb2
from google.ads.google_ads.v1.proto.enums import page_one_promoted_strategy_goal_pb2
from google.ads.google_ads.v1.proto.enums import parental_status_type_pb2
from google.ads.google_ads.v1.proto.enums import payment_mode_pb2
from google.ads.google_ads.v1.proto.enums import placeholder_type_pb2
from google.ads.google_ads.v1.proto.enums import placement_type_pb2
from google.ads.google_ads.v1.proto.enums import policy_approval_status_pb2
from google.ads.google_ads.v1.proto.enums import policy_review_status_pb2
from google.ads.google_ads.v1.proto.enums import policy_topic_entry_type_pb2
from google.ads.google_ads.v1.proto.enums import policy_topic_evidence_destination_mismatch_url_type_pb2
from google.ads.google_ads.v1.proto.enums import policy_topic_evidence_destination_not_working_device_pb2
from google.ads.google_ads.v1.proto.enums import positive_geo_target_type_pb2
from google.ads.google_ads.v1.proto.enums import preferred_content_type_pb2
from google.ads.google_ads.v1.proto.enums import price_extension_price_qualifier_pb2
from google.ads.google_ads.v1.proto.enums import price_extension_price_unit_pb2
from google.ads.google_ads.v1.proto.enums import price_extension_type_pb2
from google.ads.google_ads.v1.proto.enums import price_placeholder_field_pb2
from google.ads.google_ads.v1.proto.enums import product_bidding_category_level_pb2
from google.ads.google_ads.v1.proto.enums import product_bidding_category_status_pb2
from google.ads.google_ads.v1.proto.enums import product_channel_exclusivity_pb2
from google.ads.google_ads.v1.proto.enums import product_channel_pb2
from google.ads.google_ads.v1.proto.enums import product_condition_pb2
from google.ads.google_ads.v1.proto.enums import product_type_level_pb2
from google.ads.google_ads.v1.proto.enums import promotion_extension_discount_modifier_pb2
from google.ads.google_ads.v1.proto.enums import promotion_extension_occasion_pb2
from google.ads.google_ads.v1.proto.enums import promotion_placeholder_field_pb2
from google.ads.google_ads.v1.proto.enums import proximity_radius_units_pb2
from google.ads.google_ads.v1.proto.enums import quality_score_bucket_pb2
from google.ads.google_ads.v1.proto.enums import real_estate_placeholder_field_pb2
from google.ads.google_ads.v1.proto.enums import recommendation_type_pb2
from google.ads.google_ads.v1.proto.enums import search_engine_results_page_type_pb2
from google.ads.google_ads.v1.proto.enums import search_term_match_type_pb2
from google.ads.google_ads.v1.proto.enums import search_term_targeting_status_pb2
from google.ads.google_ads.v1.proto.enums import served_asset_field_type_pb2
from google.ads.google_ads.v1.proto.enums import shared_set_status_pb2
from google.ads.google_ads.v1.proto.enums import shared_set_type_pb2
from google.ads.google_ads.v1.proto.enums import simulation_modification_method_pb2
from google.ads.google_ads.v1.proto.enums import simulation_type_pb2
from google.ads.google_ads.v1.proto.enums import sitelink_placeholder_field_pb2
from google.ads.google_ads.v1.proto.enums import slot_pb2
from google.ads.google_ads.v1.proto.enums import spending_limit_type_pb2
from google.ads.google_ads.v1.proto.enums import structured_snippet_placeholder_field_pb2
from google.ads.google_ads.v1.proto.enums import system_managed_entity_source_pb2
from google.ads.google_ads.v1.proto.enums import target_cpa_opt_in_recommendation_goal_pb2
from google.ads.google_ads.v1.proto.enums import target_impression_share_location_pb2
from google.ads.google_ads.v1.proto.enums import targeting_dimension_pb2
from google.ads.google_ads.v1.proto.enums import time_type_pb2
from google.ads.google_ads.v1.proto.enums import tracking_code_page_format_pb2
from google.ads.google_ads.v1.proto.enums import tracking_code_type_pb2
from google.ads.google_ads.v1.proto.enums import travel_placeholder_field_pb2
from google.ads.google_ads.v1.proto.enums import user_interest_taxonomy_type_pb2
from google.ads.google_ads.v1.proto.enums import user_list_access_status_pb2
from google.ads.google_ads.v1.proto.enums import user_list_closing_reason_pb2
from google.ads.google_ads.v1.proto.enums import user_list_combined_rule_operator_pb2
from google.ads.google_ads.v1.proto.enums import user_list_crm_data_source_type_pb2
from google.ads.google_ads.v1.proto.enums import user_list_date_rule_item_operator_pb2
from google.ads.google_ads.v1.proto.enums import user_list_logical_rule_operator_pb2
from google.ads.google_ads.v1.proto.enums import user_list_membership_status_pb2
from google.ads.google_ads.v1.proto.enums import user_list_number_rule_item_operator_pb2
from google.ads.google_ads.v1.proto.enums import user_list_prepopulation_status_pb2
from google.ads.google_ads.v1.proto.enums import user_list_rule_type_pb2
from google.ads.google_ads.v1.proto.enums import user_list_size_range_pb2
from google.ads.google_ads.v1.proto.enums import user_list_string_rule_item_operator_pb2
from google.ads.google_ads.v1.proto.enums import user_list_type_pb2
from google.ads.google_ads.v1.proto.enums import vanity_pharma_display_url_mode_pb2
from google.ads.google_ads.v1.proto.enums import vanity_pharma_text_pb2
from google.ads.google_ads.v1.proto.enums import webpage_condition_operand_pb2
from google.ads.google_ads.v1.proto.enums import webpage_condition_operator_pb2
from google.ads.google_ads.v1.proto.errors import account_budget_proposal_error_pb2
from google.ads.google_ads.v1.proto.errors import ad_customizer_error_pb2
from google.ads.google_ads.v1.proto.errors import ad_error_pb2
from google.ads.google_ads.v1.proto.errors import ad_group_ad_error_pb2
from google.ads.google_ads.v1.proto.errors import ad_group_bid_modifier_error_pb2
from google.ads.google_ads.v1.proto.errors import ad_group_criterion_error_pb2
from google.ads.google_ads.v1.proto.errors import ad_group_error_pb2
from google.ads.google_ads.v1.proto.errors import ad_group_feed_error_pb2
from google.ads.google_ads.v1.proto.errors import ad_parameter_error_pb2
from google.ads.google_ads.v1.proto.errors import ad_sharing_error_pb2
from google.ads.google_ads.v1.proto.errors import adx_error_pb2
from google.ads.google_ads.v1.proto.errors import asset_error_pb2
from google.ads.google_ads.v1.proto.errors import authentication_error_pb2
from google.ads.google_ads.v1.proto.errors import authorization_error_pb2
from google.ads.google_ads.v1.proto.errors import bidding_error_pb2
from google.ads.google_ads.v1.proto.errors import bidding_strategy_error_pb2
from google.ads.google_ads.v1.proto.errors import billing_setup_error_pb2
from google.ads.google_ads.v1.proto.errors import campaign_budget_error_pb2
from google.ads.google_ads.v1.proto.errors import campaign_criterion_error_pb2
from google.ads.google_ads.v1.proto.errors import campaign_draft_error_pb2
from google.ads.google_ads.v1.proto.errors import campaign_error_pb2
from google.ads.google_ads.v1.proto.errors import campaign_experiment_error_pb2
from google.ads.google_ads.v1.proto.errors import campaign_feed_error_pb2
from google.ads.google_ads.v1.proto.errors import campaign_shared_set_error_pb2
from google.ads.google_ads.v1.proto.errors import change_status_error_pb2
from google.ads.google_ads.v1.proto.errors import collection_size_error_pb2
from google.ads.google_ads.v1.proto.errors import context_error_pb2
from google.ads.google_ads.v1.proto.errors import conversion_action_error_pb2
from google.ads.google_ads.v1.proto.errors import conversion_adjustment_upload_error_pb2
from google.ads.google_ads.v1.proto.errors import conversion_upload_error_pb2
from google.ads.google_ads.v1.proto.errors import country_code_error_pb2
from google.ads.google_ads.v1.proto.errors import criterion_error_pb2
from google.ads.google_ads.v1.proto.errors import custom_interest_error_pb2
from google.ads.google_ads.v1.proto.errors import customer_client_link_error_pb2
from google.ads.google_ads.v1.proto.errors import customer_error_pb2
from google.ads.google_ads.v1.proto.errors import customer_feed_error_pb2
from google.ads.google_ads.v1.proto.errors import customer_manager_link_error_pb2
from google.ads.google_ads.v1.proto.errors import database_error_pb2
from google.ads.google_ads.v1.proto.errors import date_error_pb2
from google.ads.google_ads.v1.proto.errors import date_range_error_pb2
from google.ads.google_ads.v1.proto.errors import distinct_error_pb2
from google.ads.google_ads.v1.proto.errors import enum_error_pb2
from google.ads.google_ads.v1.proto.errors import errors_pb2
from google.ads.google_ads.v1.proto.errors import extension_feed_item_error_pb2
from google.ads.google_ads.v1.proto.errors import extension_setting_error_pb2
from google.ads.google_ads.v1.proto.errors import feed_attribute_reference_error_pb2
from google.ads.google_ads.v1.proto.errors import feed_error_pb2
from google.ads.google_ads.v1.proto.errors import feed_item_error_pb2
from google.ads.google_ads.v1.proto.errors import feed_item_target_error_pb2
from google.ads.google_ads.v1.proto.errors import feed_item_validation_error_pb2
from google.ads.google_ads.v1.proto.errors import feed_mapping_error_pb2
from google.ads.google_ads.v1.proto.errors import field_error_pb2
from google.ads.google_ads.v1.proto.errors import field_mask_error_pb2
from google.ads.google_ads.v1.proto.errors import function_error_pb2
from google.ads.google_ads.v1.proto.errors import function_parsing_error_pb2
from google.ads.google_ads.v1.proto.errors import geo_target_constant_suggestion_error_pb2
from google.ads.google_ads.v1.proto.errors import header_error_pb2
from google.ads.google_ads.v1.proto.errors import id_error_pb2
from google.ads.google_ads.v1.proto.errors import image_error_pb2
from google.ads.google_ads.v1.proto.errors import internal_error_pb2
from google.ads.google_ads.v1.proto.errors import keyword_plan_ad_group_error_pb2
from google.ads.google_ads.v1.proto.errors import keyword_plan_campaign_error_pb2
from google.ads.google_ads.v1.proto.errors import keyword_plan_error_pb2
from google.ads.google_ads.v1.proto.errors import keyword_plan_idea_error_pb2
from google.ads.google_ads.v1.proto.errors import keyword_plan_keyword_error_pb2
from google.ads.google_ads.v1.proto.errors import keyword_plan_negative_keyword_error_pb2
from google.ads.google_ads.v1.proto.errors import label_error_pb2
from google.ads.google_ads.v1.proto.errors import language_code_error_pb2
from google.ads.google_ads.v1.proto.errors import list_operation_error_pb2
from google.ads.google_ads.v1.proto.errors import manager_link_error_pb2
from google.ads.google_ads.v1.proto.errors import media_bundle_error_pb2
from google.ads.google_ads.v1.proto.errors import media_file_error_pb2
from google.ads.google_ads.v1.proto.errors import media_upload_error_pb2
from google.ads.google_ads.v1.proto.errors import multiplier_error_pb2
from google.ads.google_ads.v1.proto.errors import mutate_error_pb2
from google.ads.google_ads.v1.proto.errors import mutate_job_error_pb2
from google.ads.google_ads.v1.proto.errors import new_resource_creation_error_pb2
from google.ads.google_ads.v1.proto.errors import not_empty_error_pb2
from google.ads.google_ads.v1.proto.errors import not_whitelisted_error_pb2
from google.ads.google_ads.v1.proto.errors import null_error_pb2
from google.ads.google_ads.v1.proto.errors import operation_access_denied_error_pb2
from google.ads.google_ads.v1.proto.errors import operator_error_pb2
from google.ads.google_ads.v1.proto.errors import partial_failure_error_pb2
from google.ads.google_ads.v1.proto.errors import policy_finding_error_pb2
from google.ads.google_ads.v1.proto.errors import policy_validation_parameter_error_pb2
from google.ads.google_ads.v1.proto.errors import policy_violation_error_pb2
from google.ads.google_ads.v1.proto.errors import query_error_pb2
from google.ads.google_ads.v1.proto.errors import quota_error_pb2
from google.ads.google_ads.v1.proto.errors import range_error_pb2
from google.ads.google_ads.v1.proto.errors import recommendation_error_pb2
from google.ads.google_ads.v1.proto.errors import region_code_error_pb2
from google.ads.google_ads.v1.proto.errors import request_error_pb2
from google.ads.google_ads.v1.proto.errors import resource_access_denied_error_pb2
from google.ads.google_ads.v1.proto.errors import resource_count_limit_exceeded_error_pb2
from google.ads.google_ads.v1.proto.errors import setting_error_pb2
from google.ads.google_ads.v1.proto.errors import shared_criterion_error_pb2
from google.ads.google_ads.v1.proto.errors import shared_set_error_pb2
from google.ads.google_ads.v1.proto.errors import size_limit_error_pb2
from google.ads.google_ads.v1.proto.errors import string_format_error_pb2
from google.ads.google_ads.v1.proto.errors import string_length_error_pb2
from google.ads.google_ads.v1.proto.errors import url_field_error_pb2
from google.ads.google_ads.v1.proto.errors import user_list_error_pb2
from google.ads.google_ads.v1.proto.errors import youtube_video_registration_error_pb2
from google.ads.google_ads.v1.proto.resources import account_budget_pb2
from google.ads.google_ads.v1.proto.resources import account_budget_proposal_pb2
from google.ads.google_ads.v1.proto.resources import ad_group_ad_label_pb2
from google.ads.google_ads.v1.proto.resources import ad_group_ad_pb2
from google.ads.google_ads.v1.proto.resources import ad_group_audience_view_pb2
from google.ads.google_ads.v1.proto.resources import ad_group_bid_modifier_pb2
from google.ads.google_ads.v1.proto.resources import ad_group_criterion_label_pb2
from google.ads.google_ads.v1.proto.resources import ad_group_criterion_pb2
from google.ads.google_ads.v1.proto.resources import ad_group_criterion_simulation_pb2
from google.ads.google_ads.v1.proto.resources import ad_group_extension_setting_pb2
from google.ads.google_ads.v1.proto.resources import ad_group_feed_pb2
from google.ads.google_ads.v1.proto.resources import ad_group_label_pb2
from google.ads.google_ads.v1.proto.resources import ad_group_pb2
from google.ads.google_ads.v1.proto.resources import ad_group_simulation_pb2
from google.ads.google_ads.v1.proto.resources import ad_parameter_pb2
from google.ads.google_ads.v1.proto.resources import ad_pb2
from google.ads.google_ads.v1.proto.resources import ad_schedule_view_pb2
from google.ads.google_ads.v1.proto.resources import age_range_view_pb2
from google.ads.google_ads.v1.proto.resources import asset_pb2
from google.ads.google_ads.v1.proto.resources import bidding_strategy_pb2
from google.ads.google_ads.v1.proto.resources import billing_setup_pb2
from google.ads.google_ads.v1.proto.resources import campaign_audience_view_pb2
from google.ads.google_ads.v1.proto.resources import campaign_bid_modifier_pb2
from google.ads.google_ads.v1.proto.resources import campaign_budget_pb2
from google.ads.google_ads.v1.proto.resources import campaign_criterion_pb2
from google.ads.google_ads.v1.proto.resources import campaign_criterion_simulation_pb2
from google.ads.google_ads.v1.proto.resources import campaign_draft_pb2
from google.ads.google_ads.v1.proto.resources import campaign_experiment_pb2
from google.ads.google_ads.v1.proto.resources import campaign_extension_setting_pb2
from google.ads.google_ads.v1.proto.resources import campaign_feed_pb2
from google.ads.google_ads.v1.proto.resources import campaign_label_pb2
from google.ads.google_ads.v1.proto.resources import campaign_pb2
from google.ads.google_ads.v1.proto.resources import campaign_shared_set_pb2
from google.ads.google_ads.v1.proto.resources import carrier_constant_pb2
from google.ads.google_ads.v1.proto.resources import change_status_pb2
from google.ads.google_ads.v1.proto.resources import click_view_pb2
from google.ads.google_ads.v1.proto.resources import conversion_action_pb2
from google.ads.google_ads.v1.proto.resources import custom_interest_pb2
from google.ads.google_ads.v1.proto.resources import customer_client_link_pb2
from google.ads.google_ads.v1.proto.resources import customer_client_pb2
from google.ads.google_ads.v1.proto.resources import customer_extension_setting_pb2
from google.ads.google_ads.v1.proto.resources import customer_feed_pb2
from google.ads.google_ads.v1.proto.resources import customer_label_pb2
from google.ads.google_ads.v1.proto.resources import customer_manager_link_pb2
from google.ads.google_ads.v1.proto.resources import customer_negative_criterion_pb2
from google.ads.google_ads.v1.proto.resources import customer_pb2
from google.ads.google_ads.v1.proto.resources import detail_placement_view_pb2
from google.ads.google_ads.v1.proto.resources import display_keyword_view_pb2
from google.ads.google_ads.v1.proto.resources import domain_category_pb2
from google.ads.google_ads.v1.proto.resources import dynamic_search_ads_search_term_view_pb2
from google.ads.google_ads.v1.proto.resources import expanded_landing_page_view_pb2
from google.ads.google_ads.v1.proto.resources import extension_feed_item_pb2
from google.ads.google_ads.v1.proto.resources import feed_item_pb2
from google.ads.google_ads.v1.proto.resources import feed_item_target_pb2
from google.ads.google_ads.v1.proto.resources import feed_mapping_pb2
from google.ads.google_ads.v1.proto.resources import feed_pb2
from google.ads.google_ads.v1.proto.resources import feed_placeholder_view_pb2
from google.ads.google_ads.v1.proto.resources import gender_view_pb2
from google.ads.google_ads.v1.proto.resources import geo_target_constant_pb2
from google.ads.google_ads.v1.proto.resources import geographic_view_pb2
from google.ads.google_ads.v1.proto.resources import google_ads_field_pb2
from google.ads.google_ads.v1.proto.resources import group_placement_view_pb2
from google.ads.google_ads.v1.proto.resources import hotel_group_view_pb2
from google.ads.google_ads.v1.proto.resources import hotel_performance_view_pb2
from google.ads.google_ads.v1.proto.resources import keyword_plan_ad_group_pb2
from google.ads.google_ads.v1.proto.resources import keyword_plan_campaign_pb2
from google.ads.google_ads.v1.proto.resources import keyword_plan_keyword_pb2
from google.ads.google_ads.v1.proto.resources import keyword_plan_negative_keyword_pb2
from google.ads.google_ads.v1.proto.resources import keyword_plan_pb2
from google.ads.google_ads.v1.proto.resources import keyword_view_pb2
from google.ads.google_ads.v1.proto.resources import label_pb2
from google.ads.google_ads.v1.proto.resources import landing_page_view_pb2
from google.ads.google_ads.v1.proto.resources import language_constant_pb2
from google.ads.google_ads.v1.proto.resources import location_view_pb2
from google.ads.google_ads.v1.proto.resources import managed_placement_view_pb2
from google.ads.google_ads.v1.proto.resources import media_file_pb2
from google.ads.google_ads.v1.proto.resources import merchant_center_link_pb2
from google.ads.google_ads.v1.proto.resources import mobile_app_category_constant_pb2
from google.ads.google_ads.v1.proto.resources import mobile_device_constant_pb2
from google.ads.google_ads.v1.proto.resources import mutate_job_pb2
from google.ads.google_ads.v1.proto.resources import operating_system_version_constant_pb2
from google.ads.google_ads.v1.proto.resources import paid_organic_search_term_view_pb2
from google.ads.google_ads.v1.proto.resources import parental_status_view_pb2
from google.ads.google_ads.v1.proto.resources import payments_account_pb2
from google.ads.google_ads.v1.proto.resources import product_bidding_category_constant_pb2
from google.ads.google_ads.v1.proto.resources import product_group_view_pb2
from google.ads.google_ads.v1.proto.resources import recommendation_pb2
from google.ads.google_ads.v1.proto.resources import remarketing_action_pb2
from google.ads.google_ads.v1.proto.resources import search_term_view_pb2
from google.ads.google_ads.v1.proto.resources import shared_criterion_pb2
from google.ads.google_ads.v1.proto.resources import shared_set_pb2
from google.ads.google_ads.v1.proto.resources import shopping_performance_view_pb2
from google.ads.google_ads.v1.proto.resources import topic_constant_pb2
from google.ads.google_ads.v1.proto.resources import topic_view_pb2
from google.ads.google_ads.v1.proto.resources import user_interest_pb2
from google.ads.google_ads.v1.proto.resources import user_list_pb2
from google.ads.google_ads.v1.proto.resources import video_pb2
from google.ads.google_ads.v1.proto.services import account_budget_proposal_service_pb2
from google.ads.google_ads.v1.proto.services import account_budget_service_pb2
from google.ads.google_ads.v1.proto.services import ad_group_ad_label_service_pb2
from google.ads.google_ads.v1.proto.services import ad_group_ad_service_pb2
from google.ads.google_ads.v1.proto.services import ad_group_audience_view_service_pb2
from google.ads.google_ads.v1.proto.services import ad_group_bid_modifier_service_pb2
from google.ads.google_ads.v1.proto.services import ad_group_criterion_label_service_pb2
from google.ads.google_ads.v1.proto.services import ad_group_criterion_service_pb2
from google.ads.google_ads.v1.proto.services import ad_group_criterion_simulation_service_pb2
from google.ads.google_ads.v1.proto.services import ad_group_extension_setting_service_pb2
from google.ads.google_ads.v1.proto.services import ad_group_feed_service_pb2
from google.ads.google_ads.v1.proto.services import ad_group_label_service_pb2
from google.ads.google_ads.v1.proto.services import ad_group_service_pb2
from google.ads.google_ads.v1.proto.services import ad_group_simulation_service_pb2
from google.ads.google_ads.v1.proto.services import ad_parameter_service_pb2
from google.ads.google_ads.v1.proto.services import ad_schedule_view_service_pb2
from google.ads.google_ads.v1.proto.services import age_range_view_service_pb2
from google.ads.google_ads.v1.proto.services import asset_service_pb2
from google.ads.google_ads.v1.proto.services import bidding_strategy_service_pb2
from google.ads.google_ads.v1.proto.services import billing_setup_service_pb2
from google.ads.google_ads.v1.proto.services import campaign_audience_view_service_pb2
from google.ads.google_ads.v1.proto.services import campaign_bid_modifier_service_pb2
from google.ads.google_ads.v1.proto.services import campaign_budget_service_pb2
from google.ads.google_ads.v1.proto.services import campaign_criterion_service_pb2
from google.ads.google_ads.v1.proto.services import campaign_criterion_simulation_service_pb2
from google.ads.google_ads.v1.proto.services import campaign_draft_service_pb2
from google.ads.google_ads.v1.proto.services import campaign_experiment_service_pb2
from google.ads.google_ads.v1.proto.services import campaign_extension_setting_service_pb2
from google.ads.google_ads.v1.proto.services import campaign_feed_service_pb2
from google.ads.google_ads.v1.proto.services import campaign_label_service_pb2
from google.ads.google_ads.v1.proto.services import campaign_service_pb2
from google.ads.google_ads.v1.proto.services import campaign_shared_set_service_pb2
from google.ads.google_ads.v1.proto.services import carrier_constant_service_pb2
from google.ads.google_ads.v1.proto.services import change_status_service_pb2
from google.ads.google_ads.v1.proto.services import click_view_service_pb2
from google.ads.google_ads.v1.proto.services import conversion_action_service_pb2
from google.ads.google_ads.v1.proto.services import conversion_adjustment_upload_service_pb2
from google.ads.google_ads.v1.proto.services import conversion_upload_service_pb2
from google.ads.google_ads.v1.proto.services import custom_interest_service_pb2
from google.ads.google_ads.v1.proto.services import customer_client_link_service_pb2
from google.ads.google_ads.v1.proto.services import customer_client_service_pb2
from google.ads.google_ads.v1.proto.services import customer_extension_setting_service_pb2
from google.ads.google_ads.v1.proto.services import customer_feed_service_pb2
from google.ads.google_ads.v1.proto.services import customer_label_service_pb2
from google.ads.google_ads.v1.proto.services import customer_manager_link_service_pb2
from google.ads.google_ads.v1.proto.services import customer_negative_criterion_service_pb2
from google.ads.google_ads.v1.proto.services import customer_service_pb2
from google.ads.google_ads.v1.proto.services import detail_placement_view_service_pb2
from google.ads.google_ads.v1.proto.services import display_keyword_view_service_pb2
from google.ads.google_ads.v1.proto.services import domain_category_service_pb2
from google.ads.google_ads.v1.proto.services import dynamic_search_ads_search_term_view_service_pb2
from google.ads.google_ads.v1.proto.services import expanded_landing_page_view_service_pb2
from google.ads.google_ads.v1.proto.services import extension_feed_item_service_pb2
from google.ads.google_ads.v1.proto.services import feed_item_service_pb2
from google.ads.google_ads.v1.proto.services import feed_item_target_service_pb2
from google.ads.google_ads.v1.proto.services import feed_mapping_service_pb2
from google.ads.google_ads.v1.proto.services import feed_placeholder_view_service_pb2
from google.ads.google_ads.v1.proto.services import feed_service_pb2
from google.ads.google_ads.v1.proto.services import gender_view_service_pb2
from google.ads.google_ads.v1.proto.services import geo_target_constant_service_pb2
from google.ads.google_ads.v1.proto.services import geographic_view_service_pb2
from google.ads.google_ads.v1.proto.services import google_ads_field_service_pb2
from google.ads.google_ads.v1.proto.services import google_ads_service_pb2
from google.ads.google_ads.v1.proto.services import group_placement_view_service_pb2
from google.ads.google_ads.v1.proto.services import hotel_group_view_service_pb2
from google.ads.google_ads.v1.proto.services import hotel_performance_view_service_pb2
from google.ads.google_ads.v1.proto.services import keyword_plan_ad_group_service_pb2
from google.ads.google_ads.v1.proto.services import keyword_plan_campaign_service_pb2
from google.ads.google_ads.v1.proto.services import keyword_plan_idea_service_pb2
from google.ads.google_ads.v1.proto.services import keyword_plan_keyword_service_pb2
from google.ads.google_ads.v1.proto.services import keyword_plan_negative_keyword_service_pb2
from google.ads.google_ads.v1.proto.services import keyword_plan_service_pb2
from google.ads.google_ads.v1.proto.services import keyword_view_service_pb2
from google.ads.google_ads.v1.proto.services import label_service_pb2
from google.ads.google_ads.v1.proto.services import landing_page_view_service_pb2
from google.ads.google_ads.v1.proto.services import language_constant_service_pb2
from google.ads.google_ads.v1.proto.services import location_view_service_pb2
from google.ads.google_ads.v1.proto.services import managed_placement_view_service_pb2
from google.ads.google_ads.v1.proto.services import media_file_service_pb2
from google.ads.google_ads.v1.proto.services import merchant_center_link_service_pb2
from google.ads.google_ads.v1.proto.services import mobile_app_category_constant_service_pb2
from google.ads.google_ads.v1.proto.services import mobile_device_constant_service_pb2
from google.ads.google_ads.v1.proto.services import mutate_job_service_pb2
from google.ads.google_ads.v1.proto.services import operating_system_version_constant_service_pb2
from google.ads.google_ads.v1.proto.services import paid_organic_search_term_view_service_pb2
from google.ads.google_ads.v1.proto.services import parental_status_view_service_pb2
from google.ads.google_ads.v1.proto.services import payments_account_service_pb2
from google.ads.google_ads.v1.proto.services import product_bidding_category_constant_service_pb2
from google.ads.google_ads.v1.proto.services import product_group_view_service_pb2
from google.ads.google_ads.v1.proto.services import recommendation_service_pb2
from google.ads.google_ads.v1.proto.services import remarketing_action_service_pb2
from google.ads.google_ads.v1.proto.services import search_term_view_service_pb2
from google.ads.google_ads.v1.proto.services import shared_criterion_service_pb2
from google.ads.google_ads.v1.proto.services import shared_set_service_pb2
from google.ads.google_ads.v1.proto.services import shopping_performance_view_service_pb2
from google.ads.google_ads.v1.proto.services import topic_constant_service_pb2
from google.ads.google_ads.v1.proto.services import topic_view_service_pb2
from google.ads.google_ads.v1.proto.services import user_interest_service_pb2
from google.ads.google_ads.v1.proto.services import user_list_service_pb2
from google.ads.google_ads.v1.proto.services import video_service_pb2
from google.longrunning import operations_pb2
from google.protobuf import any_pb2
from google.protobuf import empty_pb2
from google.protobuf import field_mask_pb2
from google.protobuf import wrappers_pb2
from google.rpc import status_pb2

_shared_modules = [
    ad_asset_pb2,
    ad_type_infos_pb2,
    asset_types_pb2,
    bidding_pb2,
    click_location_pb2,
    criteria_pb2,
    criterion_category_availability_pb2,
    custom_parameter_pb2,
    dates_pb2,
    explorer_auto_optimizer_setting_pb2,
    extensions_pb2,
    feed_common_pb2,
    final_app_url_pb2,
    frequency_cap_pb2,
    keyword_plan_common_pb2,
    matching_function_pb2,
    metrics_pb2,
    policy_pb2,
    real_time_bidding_setting_pb2,
    segments_pb2,
    simulation_pb2,
    tag_snippet_pb2,
    targeting_setting_pb2,
    text_label_pb2,
    url_collection_pb2,
    user_lists_pb2,
    value_pb2,
    access_reason_pb2,
    account_budget_proposal_status_pb2,
    account_budget_proposal_type_pb2,
    account_budget_status_pb2,
    ad_customizer_placeholder_field_pb2,
    ad_group_ad_rotation_mode_pb2,
    ad_group_ad_status_pb2,
    ad_group_criterion_approval_status_pb2,
    ad_group_criterion_status_pb2,
    ad_group_status_pb2,
    ad_group_type_pb2,
    ad_network_type_pb2,
    ad_serving_optimization_status_pb2,
    ad_strength_pb2,
    ad_type_pb2,
    advertising_channel_sub_type_pb2,
    advertising_channel_type_pb2,
    affiliate_location_feed_relationship_type_pb2,
    affiliate_location_placeholder_field_pb2,
    age_range_type_pb2,
    app_campaign_app_store_pb2,
    app_campaign_bidding_strategy_goal_type_pb2,
    app_payment_model_type_pb2,
    app_placeholder_field_pb2,
    app_store_pb2,
    app_url_operating_system_type_pb2,
    asset_type_pb2,
    attribution_model_pb2,
    bid_modifier_source_pb2,
    bidding_source_pb2,
    bidding_strategy_status_pb2,
    bidding_strategy_type_pb2,
    billing_setup_status_pb2,
    brand_safety_suitability_pb2,
    budget_delivery_method_pb2,
    budget_period_pb2,
    budget_status_pb2,
    budget_type_pb2,
    call_conversion_reporting_state_pb2,
    call_placeholder_field_pb2,
    callout_placeholder_field_pb2,
    campaign_criterion_status_pb2,
    campaign_draft_status_pb2,
    campaign_experiment_status_pb2,
    campaign_experiment_traffic_split_type_pb2,
    campaign_experiment_type_pb2,
    campaign_serving_status_pb2,
    campaign_shared_set_status_pb2,
    campaign_status_pb2,
    change_status_operation_pb2,
    change_status_resource_type_pb2,
    click_type_pb2,
    content_label_type_pb2,
    conversion_action_category_pb2,
    conversion_action_counting_type_pb2,
    conversion_action_status_pb2,
    conversion_action_type_pb2,
    conversion_adjustment_type_pb2,
    conversion_attribution_event_type_pb2,
    conversion_lag_bucket_pb2,
    conversion_or_adjustment_lag_bucket_pb2,
    criterion_category_channel_availability_mode_pb2,
    criterion_category_locale_availability_mode_pb2,
    criterion_system_serving_status_pb2,
    criterion_type_pb2,
    custom_interest_member_type_pb2,
    custom_interest_status_pb2,
    custom_interest_type_pb2,
    custom_placeholder_field_pb2,
    customer_match_upload_key_type_pb2,
    customer_pay_per_conversion_eligibility_failure_reason_pb2,
    data_driven_model_status_pb2,
    day_of_week_pb2,
    device_pb2,
    display_ad_format_setting_pb2,
    display_upload_product_type_pb2,
    dsa_page_feed_criterion_field_pb2,
    education_placeholder_field_pb2,
    extension_setting_device_pb2,
    extension_type_pb2,
    external_conversion_source_pb2,
    feed_attribute_type_pb2,
    feed_item_quality_approval_status_pb2,
    feed_item_quality_disapproval_reason_pb2,
    feed_item_status_pb2,
    feed_item_target_device_pb2,
    feed_item_target_type_pb2,
    feed_item_validation_status_pb2,
    feed_link_status_pb2,
    feed_mapping_criterion_type_pb2,
    feed_mapping_status_pb2,
    feed_origin_pb2,
    feed_status_pb2,
    flight_placeholder_field_pb2,
    frequency_cap_event_type_pb2,
    frequency_cap_level_pb2,
    frequency_cap_time_unit_pb2,
    gender_type_pb2,
    geo_target_constant_status_pb2,
    geo_targeting_restriction_pb2,
    geo_targeting_type_pb2,
    google_ads_field_category_pb2,
    google_ads_field_data_type_pb2,
    hotel_date_selection_type_pb2,
    hotel_placeholder_field_pb2,
    hotel_rate_type_pb2,
    income_range_type_pb2,
    interaction_event_type_pb2,
    interaction_type_pb2,
    job_placeholder_field_pb2,
    keyword_match_type_pb2,
    keyword_plan_competition_level_pb2,
    keyword_plan_forecast_interval_pb2,
    keyword_plan_network_pb2,
    label_status_pb2,
    legacy_app_install_ad_app_store_pb2,
    listing_custom_attribute_index_pb2,
    listing_group_type_pb2,
    local_placeholder_field_pb2,
    location_extension_targeting_criterion_field_pb2,
    location_group_radius_units_pb2,
    location_placeholder_field_pb2,
    manager_link_status_pb2,
    matching_function_context_type_pb2,
    matching_function_operator_pb2,
    media_type_pb2,
    merchant_center_link_status_pb2,
    message_placeholder_field_pb2,
    mime_type_pb2,
    minute_of_hour_pb2,
    mobile_device_type_pb2,
    month_of_year_pb2,
    mutate_job_status_pb2,
    negative_geo_target_type_pb2,
    operating_system_version_operator_type_pb2,
    page_one_promoted_strategy_goal_pb2,
    parental_status_type_pb2,
    payment_mode_pb2,
    placeholder_type_pb2,
    placement_type_pb2,
    policy_approval_status_pb2,
    policy_review_status_pb2,
    policy_topic_entry_type_pb2,
    policy_topic_evidence_destination_mismatch_url_type_pb2,
    policy_topic_evidence_destination_not_working_device_pb2,
    positive_geo_target_type_pb2,
    preferred_content_type_pb2,
    price_extension_price_qualifier_pb2,
    price_extension_price_unit_pb2,
    price_extension_type_pb2,
    price_placeholder_field_pb2,
    product_bidding_category_level_pb2,
    product_bidding_category_status_pb2,
    product_channel_exclusivity_pb2,
    product_channel_pb2,
    product_condition_pb2,
    product_type_level_pb2,
    promotion_extension_discount_modifier_pb2,
    promotion_extension_occasion_pb2,
    promotion_placeholder_field_pb2,
    proximity_radius_units_pb2,
    quality_score_bucket_pb2,
    real_estate_placeholder_field_pb2,
    recommendation_type_pb2,
    search_engine_results_page_type_pb2,
    search_term_match_type_pb2,
    search_term_targeting_status_pb2,
    served_asset_field_type_pb2,
    shared_set_status_pb2,
    shared_set_type_pb2,
    simulation_modification_method_pb2,
    simulation_type_pb2,
    sitelink_placeholder_field_pb2,
    slot_pb2,
    spending_limit_type_pb2,
    structured_snippet_placeholder_field_pb2,
    system_managed_entity_source_pb2,
    target_cpa_opt_in_recommendation_goal_pb2,
    target_impression_share_location_pb2,
    targeting_dimension_pb2,
    time_type_pb2,
    tracking_code_page_format_pb2,
    tracking_code_type_pb2,
    travel_placeholder_field_pb2,
    user_interest_taxonomy_type_pb2,
    user_list_access_status_pb2,
    user_list_closing_reason_pb2,
    user_list_combined_rule_operator_pb2,
    user_list_crm_data_source_type_pb2,
    user_list_date_rule_item_operator_pb2,
    user_list_logical_rule_operator_pb2,
    user_list_membership_status_pb2,
    user_list_number_rule_item_operator_pb2,
    user_list_prepopulation_status_pb2,
    user_list_rule_type_pb2,
    user_list_size_range_pb2,
    user_list_string_rule_item_operator_pb2,
    user_list_type_pb2,
    vanity_pharma_display_url_mode_pb2,
    vanity_pharma_text_pb2,
    webpage_condition_operand_pb2,
    webpage_condition_operator_pb2,
    account_budget_proposal_error_pb2,
    ad_customizer_error_pb2,
    ad_error_pb2,
    ad_group_ad_error_pb2,
    ad_group_bid_modifier_error_pb2,
    ad_group_criterion_error_pb2,
    ad_group_error_pb2,
    ad_group_feed_error_pb2,
    ad_parameter_error_pb2,
    ad_sharing_error_pb2,
    adx_error_pb2,
    asset_error_pb2,
    authentication_error_pb2,
    authorization_error_pb2,
    bidding_error_pb2,
    bidding_strategy_error_pb2,
    billing_setup_error_pb2,
    campaign_budget_error_pb2,
    campaign_criterion_error_pb2,
    campaign_draft_error_pb2,
    campaign_error_pb2,
    campaign_experiment_error_pb2,
    campaign_feed_error_pb2,
    campaign_shared_set_error_pb2,
    change_status_error_pb2,
    collection_size_error_pb2,
    context_error_pb2,
    conversion_action_error_pb2,
    conversion_adjustment_upload_error_pb2,
    conversion_upload_error_pb2,
    country_code_error_pb2,
    criterion_error_pb2,
    custom_interest_error_pb2,
    customer_client_link_error_pb2,
    customer_error_pb2,
    customer_feed_error_pb2,
    customer_manager_link_error_pb2,
    database_error_pb2,
    date_error_pb2,
    date_range_error_pb2,
    distinct_error_pb2,
    enum_error_pb2,
    errors_pb2,
    extension_feed_item_error_pb2,
    extension_setting_error_pb2,
    feed_attribute_reference_error_pb2,
    feed_error_pb2,
    feed_item_error_pb2,
    feed_item_target_error_pb2,
    feed_item_validation_error_pb2,
    feed_mapping_error_pb2,
    field_error_pb2,
    field_mask_error_pb2,
    function_error_pb2,
    function_parsing_error_pb2,
    geo_target_constant_suggestion_error_pb2,
    header_error_pb2,
    id_error_pb2,
    image_error_pb2,
    internal_error_pb2,
    keyword_plan_ad_group_error_pb2,
    keyword_plan_campaign_error_pb2,
    keyword_plan_error_pb2,
    keyword_plan_idea_error_pb2,
    keyword_plan_keyword_error_pb2,
    keyword_plan_negative_keyword_error_pb2,
    label_error_pb2,
    language_code_error_pb2,
    list_operation_error_pb2,
    manager_link_error_pb2,
    media_bundle_error_pb2,
    media_file_error_pb2,
    media_upload_error_pb2,
    multiplier_error_pb2,
    mutate_error_pb2,
    mutate_job_error_pb2,
    new_resource_creation_error_pb2,
    not_empty_error_pb2,
    not_whitelisted_error_pb2,
    null_error_pb2,
    operation_access_denied_error_pb2,
    operator_error_pb2,
    partial_failure_error_pb2,
    policy_finding_error_pb2,
    policy_validation_parameter_error_pb2,
    policy_violation_error_pb2,
    query_error_pb2,
    quota_error_pb2,
    range_error_pb2,
    recommendation_error_pb2,
    region_code_error_pb2,
    request_error_pb2,
    resource_access_denied_error_pb2,
    resource_count_limit_exceeded_error_pb2,
    setting_error_pb2,
    shared_criterion_error_pb2,
    shared_set_error_pb2,
    size_limit_error_pb2,
    string_format_error_pb2,
    string_length_error_pb2,
    url_field_error_pb2,
    user_list_error_pb2,
    youtube_video_registration_error_pb2,
    account_budget_pb2,
    account_budget_proposal_pb2,
    ad_group_ad_label_pb2,
    ad_group_ad_pb2,
    ad_group_audience_view_pb2,
    ad_group_bid_modifier_pb2,
    ad_group_criterion_label_pb2,
    ad_group_criterion_pb2,
    ad_group_criterion_simulation_pb2,
    ad_group_extension_setting_pb2,
    ad_group_feed_pb2,
    ad_group_label_pb2,
    ad_group_pb2,
    ad_group_simulation_pb2,
    ad_parameter_pb2,
    ad_pb2,
    ad_schedule_view_pb2,
    age_range_view_pb2,
    asset_pb2,
    bidding_strategy_pb2,
    billing_setup_pb2,
    campaign_audience_view_pb2,
    campaign_bid_modifier_pb2,
    campaign_budget_pb2,
    campaign_criterion_pb2,
    campaign_criterion_simulation_pb2,
    campaign_draft_pb2,
    campaign_experiment_pb2,
    campaign_extension_setting_pb2,
    campaign_feed_pb2,
    campaign_label_pb2,
    campaign_pb2,
    campaign_shared_set_pb2,
    carrier_constant_pb2,
    change_status_pb2,
    click_view_pb2,
    conversion_action_pb2,
    custom_interest_pb2,
    customer_client_link_pb2,
    customer_client_pb2,
    customer_extension_setting_pb2,
    customer_feed_pb2,
    customer_label_pb2,
    customer_manager_link_pb2,
    customer_negative_criterion_pb2,
    customer_pb2,
    detail_placement_view_pb2,
    display_keyword_view_pb2,
    domain_category_pb2,
    dynamic_search_ads_search_term_view_pb2,
    expanded_landing_page_view_pb2,
    extension_feed_item_pb2,
    feed_item_pb2,
    feed_item_target_pb2,
    feed_mapping_pb2,
    feed_pb2,
    feed_placeholder_view_pb2,
    gender_view_pb2,
    geo_target_constant_pb2,
    geographic_view_pb2,
    google_ads_field_pb2,
    group_placement_view_pb2,
    hotel_group_view_pb2,
    hotel_performance_view_pb2,
    keyword_plan_ad_group_pb2,
    keyword_plan_campaign_pb2,
    keyword_plan_keyword_pb2,
    keyword_plan_negative_keyword_pb2,
    keyword_plan_pb2,
    keyword_view_pb2,
    label_pb2,
    landing_page_view_pb2,
    language_constant_pb2,
    location_view_pb2,
    managed_placement_view_pb2,
    media_file_pb2,
    merchant_center_link_pb2,
    mobile_app_category_constant_pb2,
    mobile_device_constant_pb2,
    mutate_job_pb2,
    operating_system_version_constant_pb2,
    paid_organic_search_term_view_pb2,
    parental_status_view_pb2,
    payments_account_pb2,
    product_bidding_category_constant_pb2,
    product_group_view_pb2,
    recommendation_pb2,
    remarketing_action_pb2,
    search_term_view_pb2,
    shared_criterion_pb2,
    shared_set_pb2,
    shopping_performance_view_pb2,
    topic_constant_pb2,
    topic_view_pb2,
    user_interest_pb2,
    user_list_pb2,
    video_pb2,
    operations_pb2,
    any_pb2,
    empty_pb2,
    field_mask_pb2,
    wrappers_pb2,
    status_pb2,
]

_local_modules = [
    account_budget_proposal_service_pb2,
    account_budget_service_pb2,
    ad_group_ad_label_service_pb2,
    ad_group_ad_service_pb2,
    ad_group_audience_view_service_pb2,
    ad_group_bid_modifier_service_pb2,
    ad_group_criterion_label_service_pb2,
    ad_group_criterion_service_pb2,
    ad_group_criterion_simulation_service_pb2,
    ad_group_extension_setting_service_pb2,
    ad_group_feed_service_pb2,
    ad_group_label_service_pb2,
    ad_group_service_pb2,
    ad_group_simulation_service_pb2,
    ad_parameter_service_pb2,
    ad_schedule_view_service_pb2,
    age_range_view_service_pb2,
    asset_service_pb2,
    bidding_strategy_service_pb2,
    billing_setup_service_pb2,
    campaign_audience_view_service_pb2,
    campaign_bid_modifier_service_pb2,
    campaign_budget_service_pb2,
    campaign_criterion_service_pb2,
    campaign_criterion_simulation_service_pb2,
    campaign_draft_service_pb2,
    campaign_experiment_service_pb2,
    campaign_extension_setting_service_pb2,
    campaign_feed_service_pb2,
    campaign_label_service_pb2,
    campaign_service_pb2,
    campaign_shared_set_service_pb2,
    carrier_constant_service_pb2,
    change_status_service_pb2,
    click_view_service_pb2,
    conversion_action_service_pb2,
    conversion_adjustment_upload_service_pb2,
    conversion_upload_service_pb2,
    custom_interest_service_pb2,
    customer_client_link_service_pb2,
    customer_client_service_pb2,
    customer_extension_setting_service_pb2,
    customer_feed_service_pb2,
    customer_label_service_pb2,
    customer_manager_link_service_pb2,
    customer_negative_criterion_service_pb2,
    customer_service_pb2,
    detail_placement_view_service_pb2,
    display_keyword_view_service_pb2,
    domain_category_service_pb2,
    dynamic_search_ads_search_term_view_service_pb2,
    expanded_landing_page_view_service_pb2,
    extension_feed_item_service_pb2,
    feed_item_service_pb2,
    feed_item_target_service_pb2,
    feed_mapping_service_pb2,
    feed_placeholder_view_service_pb2,
    feed_service_pb2,
    gender_view_service_pb2,
    geo_target_constant_service_pb2,
    geographic_view_service_pb2,
    google_ads_field_service_pb2,
    google_ads_service_pb2,
    group_placement_view_service_pb2,
    hotel_group_view_service_pb2,
    hotel_performance_view_service_pb2,
    keyword_plan_ad_group_service_pb2,
    keyword_plan_campaign_service_pb2,
    keyword_plan_idea_service_pb2,
    keyword_plan_keyword_service_pb2,
    keyword_plan_negative_keyword_service_pb2,
    keyword_plan_service_pb2,
    keyword_view_service_pb2,
    label_service_pb2,
    landing_page_view_service_pb2,
    language_constant_service_pb2,
    location_view_service_pb2,
    managed_placement_view_service_pb2,
    media_file_service_pb2,
    merchant_center_link_service_pb2,
    mobile_app_category_constant_service_pb2,
    mobile_device_constant_service_pb2,
    mutate_job_service_pb2,
    operating_system_version_constant_service_pb2,
    paid_organic_search_term_view_service_pb2,
    parental_status_view_service_pb2,
    payments_account_service_pb2,
    product_bidding_category_constant_service_pb2,
    product_group_view_service_pb2,
    recommendation_service_pb2,
    remarketing_action_service_pb2,
    search_term_view_service_pb2,
    shared_criterion_service_pb2,
    shared_set_service_pb2,
    shopping_performance_view_service_pb2,
    topic_constant_service_pb2,
    topic_view_service_pb2,
    user_interest_service_pb2,
    user_list_service_pb2,
    video_service_pb2,
]

names = []

for module in _shared_modules:
    for name, message in get_messages(module).items():
        setattr(sys.modules[__name__], name, message)
        names.append(name)
for module in _local_modules:
    for name, message in get_messages(module).items():
        message.__module__ = 'google.ads.googleads_v1.types'
        setattr(sys.modules[__name__], name, message)
        names.append(name)

__all__ = tuple(sorted(names))
