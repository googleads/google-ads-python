# -*- coding: utf-8 -*-
# Copyright 2026 Google LLC
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
from google.ads.googleads.v25 import gapic_version as package_version

import google.api_core as api_core
import sys

__version__ = package_version.__version__

from importlib import metadata

# PEP 0810: Explicit Lazy Imports
# Python 3.15+ natively intercepts and defers these imports.
# Developers can disable this behavior and force eager imports.
# For more information, see:
# https://docs.python.org/3.15/library/sys.html#sys.set_lazy_imports_filter
# Older Python versions safely ignore this variable.
__lazy_modules__ = {
    "google.ads.googleads.v25.types.access_invitation_status",
    "google.ads.googleads.v25.types.access_reason",
    "google.ads.googleads.v25.types.access_role",
    "google.ads.googleads.v25.types.account_budget_proposal_status",
    "google.ads.googleads.v25.types.account_budget_proposal_type",
    "google.ads.googleads.v25.types.account_budget_status",
    "google.ads.googleads.v25.types.account_link_status",
    "google.ads.googleads.v25.types.ad_destination_type",
    "google.ads.googleads.v25.types.ad_format_type",
    "google.ads.googleads.v25.types.ad_group_ad_primary_status",
    "google.ads.googleads.v25.types.ad_group_ad_primary_status_reason",
    "google.ads.googleads.v25.types.ad_group_ad_rotation_mode",
    "google.ads.googleads.v25.types.ad_group_ad_status",
    "google.ads.googleads.v25.types.ad_group_criterion_approval_status",
    "google.ads.googleads.v25.types.ad_group_criterion_primary_status",
    "google.ads.googleads.v25.types.ad_group_criterion_primary_status_reason",
    "google.ads.googleads.v25.types.ad_group_criterion_status",
    "google.ads.googleads.v25.types.ad_group_primary_status",
    "google.ads.googleads.v25.types.ad_group_primary_status_reason",
    "google.ads.googleads.v25.types.ad_group_status",
    "google.ads.googleads.v25.types.ad_group_type",
    "google.ads.googleads.v25.types.ad_network_type",
    "google.ads.googleads.v25.types.ad_serving_optimization_status",
    "google.ads.googleads.v25.types.ad_strength",
    "google.ads.googleads.v25.types.ad_strength_action_item_type",
    "google.ads.googleads.v25.types.ad_sub_format_type",
    "google.ads.googleads.v25.types.ad_sub_network_type",
    "google.ads.googleads.v25.types.ad_type",
    "google.ads.googleads.v25.types.advertising_channel_sub_type",
    "google.ads.googleads.v25.types.advertising_channel_type",
    "google.ads.googleads.v25.types.age_range_type",
    "google.ads.googleads.v25.types.android_privacy_interaction_type",
    "google.ads.googleads.v25.types.android_privacy_network_type",
    "google.ads.googleads.v25.types.app_bidding_goal",
    "google.ads.googleads.v25.types.app_campaign_app_store",
    "google.ads.googleads.v25.types.app_campaign_bidding_strategy_goal_type",
    "google.ads.googleads.v25.types.app_payment_model_type",
    "google.ads.googleads.v25.types.app_url_operating_system_type",
    "google.ads.googleads.v25.types.application_instance",
    "google.ads.googleads.v25.types.asset_automation_status",
    "google.ads.googleads.v25.types.asset_automation_type",
    "google.ads.googleads.v25.types.asset_coverage_video_aspect_ratio_requirement",
    "google.ads.googleads.v25.types.asset_field_type",
    "google.ads.googleads.v25.types.asset_group_primary_status",
    "google.ads.googleads.v25.types.asset_group_primary_status_reason",
    "google.ads.googleads.v25.types.asset_group_signal_approval_status",
    "google.ads.googleads.v25.types.asset_group_status",
    "google.ads.googleads.v25.types.asset_link_primary_status",
    "google.ads.googleads.v25.types.asset_link_primary_status_reason",
    "google.ads.googleads.v25.types.asset_link_status",
    "google.ads.googleads.v25.types.asset_offline_evaluation_error_reasons",
    "google.ads.googleads.v25.types.asset_orientation",
    "google.ads.googleads.v25.types.asset_performance_label",
    "google.ads.googleads.v25.types.asset_set_asset_status",
    "google.ads.googleads.v25.types.asset_set_link_status",
    "google.ads.googleads.v25.types.asset_set_status",
    "google.ads.googleads.v25.types.asset_set_type",
    "google.ads.googleads.v25.types.asset_source",
    "google.ads.googleads.v25.types.asset_type",
    "google.ads.googleads.v25.types.async_action_status",
    "google.ads.googleads.v25.types.attribution_model",
    "google.ads.googleads.v25.types.audience_insights_dimension",
    "google.ads.googleads.v25.types.audience_insights_marketing_objective",
    "google.ads.googleads.v25.types.audience_scope",
    "google.ads.googleads.v25.types.audience_status",
    "google.ads.googleads.v25.types.batch_job_status",
    "google.ads.googleads.v25.types.benchmarks_marketing_objective",
    "google.ads.googleads.v25.types.benchmarks_source_type",
    "google.ads.googleads.v25.types.benchmarks_time_granularity",
    "google.ads.googleads.v25.types.bid_modifier_source",
    "google.ads.googleads.v25.types.bidding_source",
    "google.ads.googleads.v25.types.bidding_strategy_status",
    "google.ads.googleads.v25.types.bidding_strategy_system_status",
    "google.ads.googleads.v25.types.bidding_strategy_type",
    "google.ads.googleads.v25.types.billing_setup_status",
    "google.ads.googleads.v25.types.booking_status",
    "google.ads.googleads.v25.types.brand_lift_measurement_type",
    "google.ads.googleads.v25.types.brand_request_rejection_reason",
    "google.ads.googleads.v25.types.brand_safety_suitability",
    "google.ads.googleads.v25.types.brand_state",
    "google.ads.googleads.v25.types.budget_campaign_association_status",
    "google.ads.googleads.v25.types.budget_delivery_method",
    "google.ads.googleads.v25.types.budget_period",
    "google.ads.googleads.v25.types.budget_status",
    "google.ads.googleads.v25.types.budget_type",
    "google.ads.googleads.v25.types.business_message_call_to_action_type",
    "google.ads.googleads.v25.types.business_message_provider",
    "google.ads.googleads.v25.types.call_conversion_reporting_state",
    "google.ads.googleads.v25.types.call_to_action_type",
    "google.ads.googleads.v25.types.call_tracking_display_location",
    "google.ads.googleads.v25.types.call_type",
    "google.ads.googleads.v25.types.campaign_criterion_status",
    "google.ads.googleads.v25.types.campaign_draft_status",
    "google.ads.googleads.v25.types.campaign_experiment_type",
    "google.ads.googleads.v25.types.campaign_group_status",
    "google.ads.googleads.v25.types.campaign_keyword_match_type",
    "google.ads.googleads.v25.types.campaign_primary_status",
    "google.ads.googleads.v25.types.campaign_primary_status_reason",
    "google.ads.googleads.v25.types.campaign_serving_status",
    "google.ads.googleads.v25.types.campaign_shared_set_status",
    "google.ads.googleads.v25.types.campaign_status",
    "google.ads.googleads.v25.types.chain_relationship_type",
    "google.ads.googleads.v25.types.change_client_type",
    "google.ads.googleads.v25.types.change_event_resource_type",
    "google.ads.googleads.v25.types.change_status_operation",
    "google.ads.googleads.v25.types.change_status_resource_type",
    "google.ads.googleads.v25.types.click_type",
    "google.ads.googleads.v25.types.combined_audience_status",
    "google.ads.googleads.v25.types.consent_status",
    "google.ads.googleads.v25.types.content_creator_insights_supplemental_data",
    "google.ads.googleads.v25.types.content_label_type",
    "google.ads.googleads.v25.types.conversion_action_category",
    "google.ads.googleads.v25.types.conversion_action_counting_type",
    "google.ads.googleads.v25.types.conversion_action_status",
    "google.ads.googleads.v25.types.conversion_action_type",
    "google.ads.googleads.v25.types.conversion_adjustment_type",
    "google.ads.googleads.v25.types.conversion_attribution_event_type",
    "google.ads.googleads.v25.types.conversion_custom_variable_status",
    "google.ads.googleads.v25.types.conversion_customer_type",
    "google.ads.googleads.v25.types.conversion_environment_enum",
    "google.ads.googleads.v25.types.conversion_lag_bucket",
    "google.ads.googleads.v25.types.conversion_lift_included_conversion_action_types",
    "google.ads.googleads.v25.types.conversion_or_adjustment_lag_bucket",
    "google.ads.googleads.v25.types.conversion_origin",
    "google.ads.googleads.v25.types.conversion_tracking_status_enum",
    "google.ads.googleads.v25.types.conversion_value_rule_primary_dimension",
    "google.ads.googleads.v25.types.conversion_value_rule_set_status",
    "google.ads.googleads.v25.types.conversion_value_rule_status",
    "google.ads.googleads.v25.types.converting_user_prior_engagement_type_and_ltv_bucket",
    "google.ads.googleads.v25.types.criterion_category_channel_availability_mode",
    "google.ads.googleads.v25.types.criterion_category_locale_availability_mode",
    "google.ads.googleads.v25.types.criterion_system_serving_status",
    "google.ads.googleads.v25.types.criterion_type",
    "google.ads.googleads.v25.types.custom_audience_member_type",
    "google.ads.googleads.v25.types.custom_audience_status",
    "google.ads.googleads.v25.types.custom_audience_type",
    "google.ads.googleads.v25.types.custom_conversion_goal_status",
    "google.ads.googleads.v25.types.custom_interest_member_type",
    "google.ads.googleads.v25.types.custom_interest_status",
    "google.ads.googleads.v25.types.custom_interest_type",
    "google.ads.googleads.v25.types.customer_lifecycle_optimization_goal_sub_type",
    "google.ads.googleads.v25.types.customer_lifecycle_optimization_mode",
    "google.ads.googleads.v25.types.customer_match_upload_key_type",
    "google.ads.googleads.v25.types.customer_pay_per_conversion_eligibility_failure_reason",
    "google.ads.googleads.v25.types.customer_status",
    "google.ads.googleads.v25.types.customizer_attribute_status",
    "google.ads.googleads.v25.types.customizer_attribute_type",
    "google.ads.googleads.v25.types.customizer_value_status",
    "google.ads.googleads.v25.types.data_driven_model_status",
    "google.ads.googleads.v25.types.data_link_status",
    "google.ads.googleads.v25.types.data_link_type",
    "google.ads.googleads.v25.types.day_of_week",
    "google.ads.googleads.v25.types.demand_gen_channel_config",
    "google.ads.googleads.v25.types.demand_gen_channel_strategy",
    "google.ads.googleads.v25.types.device",
    "google.ads.googleads.v25.types.display_ad_format_setting",
    "google.ads.googleads.v25.types.display_upload_product_type",
    "google.ads.googleads.v25.types.distance_bucket",
    "google.ads.googleads.v25.types.eu_political_advertising_status",
    "google.ads.googleads.v25.types.experiment_asset_detail_operation",
    "google.ads.googleads.v25.types.experiment_metric",
    "google.ads.googleads.v25.types.experiment_metric_direction",
    "google.ads.googleads.v25.types.experiment_status",
    "google.ads.googleads.v25.types.experiment_type",
    "google.ads.googleads.v25.types.external_conversion_source",
    "google.ads.googleads.v25.types.fixed_cpm_goal",
    "google.ads.googleads.v25.types.fixed_cpm_target_frequency_time_unit",
    "google.ads.googleads.v25.types.frequency_cap_event_type",
    "google.ads.googleads.v25.types.frequency_cap_level",
    "google.ads.googleads.v25.types.frequency_cap_time_unit",
    "google.ads.googleads.v25.types.gender_type",
    "google.ads.googleads.v25.types.geo_target_constant_status",
    "google.ads.googleads.v25.types.geo_targeting_type",
    "google.ads.googleads.v25.types.gls_phone_number_type",
    "google.ads.googleads.v25.types.goal_config_level",
    "google.ads.googleads.v25.types.goal_optimization_eligibility",
    "google.ads.googleads.v25.types.goal_type",
    "google.ads.googleads.v25.types.google_ads_field_category",
    "google.ads.googleads.v25.types.google_ads_field_data_type",
    "google.ads.googleads.v25.types.google_voice_call_status",
    "google.ads.googleads.v25.types.hotel_asset_suggestion_status",
    "google.ads.googleads.v25.types.hotel_date_selection_type",
    "google.ads.googleads.v25.types.hotel_price_bucket",
    "google.ads.googleads.v25.types.hotel_rate_type",
    "google.ads.googleads.v25.types.hotel_reconciliation_status",
    "google.ads.googleads.v25.types.identity_verification_program",
    "google.ads.googleads.v25.types.identity_verification_program_status",
    "google.ads.googleads.v25.types.incentive_offer_type",
    "google.ads.googleads.v25.types.incentive_state",
    "google.ads.googleads.v25.types.incentive_type",
    "google.ads.googleads.v25.types.income_range_type",
    "google.ads.googleads.v25.types.insights_knowledge_graph_entity_capabilities",
    "google.ads.googleads.v25.types.insights_trend",
    "google.ads.googleads.v25.types.interaction_event_type",
    "google.ads.googleads.v25.types.interaction_type",
    "google.ads.googleads.v25.types.invoice_type",
    "google.ads.googleads.v25.types.keyword_match_type",
    "google.ads.googleads.v25.types.keyword_plan_aggregate_metric_type",
    "google.ads.googleads.v25.types.keyword_plan_competition_level",
    "google.ads.googleads.v25.types.keyword_plan_concept_group_type",
    "google.ads.googleads.v25.types.keyword_plan_forecast_interval",
    "google.ads.googleads.v25.types.keyword_plan_keyword_annotation",
    "google.ads.googleads.v25.types.keyword_plan_network",
    "google.ads.googleads.v25.types.label_status",
    "google.ads.googleads.v25.types.landing_page_source",
    "google.ads.googleads.v25.types.lead_form_call_to_action_type",
    "google.ads.googleads.v25.types.lead_form_desired_intent",
    "google.ads.googleads.v25.types.lead_form_field_user_input_type",
    "google.ads.googleads.v25.types.lead_form_post_submit_call_to_action_type",
    "google.ads.googleads.v25.types.legacy_app_install_ad_app_store",
    "google.ads.googleads.v25.types.lift_measurement_flight_status",
    "google.ads.googleads.v25.types.lift_metric_type",
    "google.ads.googleads.v25.types.linked_account_type",
    "google.ads.googleads.v25.types.linked_product_type",
    "google.ads.googleads.v25.types.listing_group_filter_custom_attribute_index",
    "google.ads.googleads.v25.types.listing_group_filter_listing_source",
    "google.ads.googleads.v25.types.listing_group_filter_product_category_level",
    "google.ads.googleads.v25.types.listing_group_filter_product_channel",
    "google.ads.googleads.v25.types.listing_group_filter_product_condition",
    "google.ads.googleads.v25.types.listing_group_filter_product_type_level",
    "google.ads.googleads.v25.types.listing_group_filter_type_enum",
    "google.ads.googleads.v25.types.listing_group_type",
    "google.ads.googleads.v25.types.listing_type",
    "google.ads.googleads.v25.types.local_services_business_registration_check_rejection_reason",
    "google.ads.googleads.v25.types.local_services_business_registration_type",
    "google.ads.googleads.v25.types.local_services_conversation_type",
    "google.ads.googleads.v25.types.local_services_employee_status",
    "google.ads.googleads.v25.types.local_services_employee_type",
    "google.ads.googleads.v25.types.local_services_insurance_rejection_reason",
    "google.ads.googleads.v25.types.local_services_lead_credit_issuance_decision",
    "google.ads.googleads.v25.types.local_services_lead_credit_state",
    "google.ads.googleads.v25.types.local_services_lead_status",
    "google.ads.googleads.v25.types.local_services_lead_survey_answer",
    "google.ads.googleads.v25.types.local_services_lead_survey_dissatisfied_reason",
    "google.ads.googleads.v25.types.local_services_lead_survey_satisfied_reason",
    "google.ads.googleads.v25.types.local_services_lead_type",
    "google.ads.googleads.v25.types.local_services_license_rejection_reason",
    "google.ads.googleads.v25.types.local_services_participant_type",
    "google.ads.googleads.v25.types.local_services_verification_artifact_status",
    "google.ads.googleads.v25.types.local_services_verification_artifact_type",
    "google.ads.googleads.v25.types.local_services_verification_status",
    "google.ads.googleads.v25.types.location_group_radius_units",
    "google.ads.googleads.v25.types.location_ownership_type",
    "google.ads.googleads.v25.types.location_source_type",
    "google.ads.googleads.v25.types.location_string_filter_type",
    "google.ads.googleads.v25.types.lookalike_expansion_level",
    "google.ads.googleads.v25.types.loyalty_membership",
    "google.ads.googleads.v25.types.manager_link_status",
    "google.ads.googleads.v25.types.match_type",
    "google.ads.googleads.v25.types.media_type",
    "google.ads.googleads.v25.types.messaging_restriction_type",
    "google.ads.googleads.v25.types.mime_type",
    "google.ads.googleads.v25.types.minute_of_hour",
    "google.ads.googleads.v25.types.mobile_app_vendor",
    "google.ads.googleads.v25.types.mobile_device_platform",
    "google.ads.googleads.v25.types.mobile_device_type",
    "google.ads.googleads.v25.types.month_of_year",
    "google.ads.googleads.v25.types.multi_party_auth_operation_type",
    "google.ads.googleads.v25.types.multi_party_auth_review_status",
    "google.ads.googleads.v25.types.multi_party_auth_review_target_resource",
    "google.ads.googleads.v25.types.negative_geo_target_type",
    "google.ads.googleads.v25.types.non_skippable_max_duration",
    "google.ads.googleads.v25.types.non_skippable_min_duration",
    "google.ads.googleads.v25.types.offline_conversion_diagnostic_status_enum",
    "google.ads.googleads.v25.types.offline_event_upload_client_enum",
    "google.ads.googleads.v25.types.offline_user_data_job_failure_reason",
    "google.ads.googleads.v25.types.offline_user_data_job_match_rate_range",
    "google.ads.googleads.v25.types.offline_user_data_job_status",
    "google.ads.googleads.v25.types.offline_user_data_job_type",
    "google.ads.googleads.v25.types.operating_system_version_operator_type",
    "google.ads.googleads.v25.types.optimization_goal_type",
    "google.ads.googleads.v25.types.optimize_assets_experiment_subtype",
    "google.ads.googleads.v25.types.parental_status_type",
    "google.ads.googleads.v25.types.partnership_opportunity",
    "google.ads.googleads.v25.types.payment_mode",
    "google.ads.googleads.v25.types.performance_max_upgrade_status",
    "google.ads.googleads.v25.types.placement_type",
    "google.ads.googleads.v25.types.policy_approval_status",
    "google.ads.googleads.v25.types.policy_review_status",
    "google.ads.googleads.v25.types.policy_topic_entry_type",
    "google.ads.googleads.v25.types.policy_topic_evidence_destination_mismatch_url_type",
    "google.ads.googleads.v25.types.policy_topic_evidence_destination_not_working_device",
    "google.ads.googleads.v25.types.policy_topic_evidence_destination_not_working_dns_error_type",
    "google.ads.googleads.v25.types.positive_geo_target_type",
    "google.ads.googleads.v25.types.preview_type",
    "google.ads.googleads.v25.types.price_extension_price_qualifier",
    "google.ads.googleads.v25.types.price_extension_price_unit",
    "google.ads.googleads.v25.types.price_extension_type",
    "google.ads.googleads.v25.types.product_availability",
    "google.ads.googleads.v25.types.product_category_level",
    "google.ads.googleads.v25.types.product_category_state",
    "google.ads.googleads.v25.types.product_channel",
    "google.ads.googleads.v25.types.product_channel_exclusivity",
    "google.ads.googleads.v25.types.product_condition",
    "google.ads.googleads.v25.types.product_custom_attribute_index",
    "google.ads.googleads.v25.types.product_issue_severity",
    "google.ads.googleads.v25.types.product_link_invitation_status",
    "google.ads.googleads.v25.types.product_status",
    "google.ads.googleads.v25.types.product_type_level",
    "google.ads.googleads.v25.types.promotion_barcode_type",
    "google.ads.googleads.v25.types.promotion_extension_discount_modifier",
    "google.ads.googleads.v25.types.promotion_extension_occasion",
    "google.ads.googleads.v25.types.proximity_radius_units",
    "google.ads.googleads.v25.types.quality_score_bucket",
    "google.ads.googleads.v25.types.reach_plan_age_range",
    "google.ads.googleads.v25.types.reach_plan_buying_method",
    "google.ads.googleads.v25.types.reach_plan_conversion_rate_model",
    "google.ads.googleads.v25.types.reach_plan_cost_model",
    "google.ads.googleads.v25.types.reach_plan_marketing_objective",
    "google.ads.googleads.v25.types.reach_plan_network",
    "google.ads.googleads.v25.types.reach_plan_plannable_user_list_status",
    "google.ads.googleads.v25.types.reach_plan_surface",
    "google.ads.googleads.v25.types.recommendation_subscription_status",
    "google.ads.googleads.v25.types.recommendation_type",
    "google.ads.googleads.v25.types.regulatory_fee_type",
    "google.ads.googleads.v25.types.reservation_request_type",
    "google.ads.googleads.v25.types.resource_change_operation",
    "google.ads.googleads.v25.types.resource_limit_type",
    "google.ads.googleads.v25.types.response_content_type",
    "google.ads.googleads.v25.types.search_engine_results_page_type",
    "google.ads.googleads.v25.types.search_term_match_source",
    "google.ads.googleads.v25.types.search_term_match_type",
    "google.ads.googleads.v25.types.search_term_targeting_status",
    "google.ads.googleads.v25.types.seasonality_event_scope",
    "google.ads.googleads.v25.types.seasonality_event_status",
    "google.ads.googleads.v25.types.sentiment",
    "google.ads.googleads.v25.types.served_asset_field_type",
    "google.ads.googleads.v25.types.shared_set_status",
    "google.ads.googleads.v25.types.shared_set_type",
    "google.ads.googleads.v25.types.shopping_add_products_to_campaign_recommendation_enum",
    "google.ads.googleads.v25.types.simulation_modification_method",
    "google.ads.googleads.v25.types.simulation_type",
    "google.ads.googleads.v25.types.sk_ad_network_ad_event_type",
    "google.ads.googleads.v25.types.sk_ad_network_attribution_credit",
    "google.ads.googleads.v25.types.sk_ad_network_coarse_conversion_value",
    "google.ads.googleads.v25.types.sk_ad_network_source_type",
    "google.ads.googleads.v25.types.sk_ad_network_user_type",
    "google.ads.googleads.v25.types.slot",
    "google.ads.googleads.v25.types.smart_campaign_not_eligible_reason",
    "google.ads.googleads.v25.types.smart_campaign_status",
    "google.ads.googleads.v25.types.spending_limit_type",
    "google.ads.googleads.v25.types.summary_row_setting",
    "google.ads.googleads.v25.types.survey_intended_action",
    "google.ads.googleads.v25.types.survey_lift_flight_target_response_mode",
    "google.ads.googleads.v25.types.survey_subject_type",
    "google.ads.googleads.v25.types.synthetic_content_attestation_status",
    "google.ads.googleads.v25.types.synthetic_content_source",
    "google.ads.googleads.v25.types.system_managed_entity_source",
    "google.ads.googleads.v25.types.target_cpa_opt_in_recommendation_goal",
    "google.ads.googleads.v25.types.target_frequency_time_unit",
    "google.ads.googleads.v25.types.target_impression_share_location",
    "google.ads.googleads.v25.types.targeting_dimension",
    "google.ads.googleads.v25.types.third_party_brand_lift_integration_partner",
    "google.ads.googleads.v25.types.third_party_brand_safety_integration_partner",
    "google.ads.googleads.v25.types.third_party_conversion_attribution_integration_partner",
    "google.ads.googleads.v25.types.third_party_reach_integration_partner",
    "google.ads.googleads.v25.types.third_party_viewability_integration_partner",
    "google.ads.googleads.v25.types.time_type",
    "google.ads.googleads.v25.types.tracking_code_page_format",
    "google.ads.googleads.v25.types.tracking_code_type",
    "google.ads.googleads.v25.types.unit_of_measure",
    "google.ads.googleads.v25.types.user_identifier_source",
    "google.ads.googleads.v25.types.user_interest_taxonomy_type",
    "google.ads.googleads.v25.types.user_list_access_status",
    "google.ads.googleads.v25.types.user_list_closing_reason",
    "google.ads.googleads.v25.types.user_list_crm_data_source_type",
    "google.ads.googleads.v25.types.user_list_customer_type_category",
    "google.ads.googleads.v25.types.user_list_date_rule_item_operator",
    "google.ads.googleads.v25.types.user_list_flexible_rule_operator",
    "google.ads.googleads.v25.types.user_list_logical_rule_operator",
    "google.ads.googleads.v25.types.user_list_membership_status",
    "google.ads.googleads.v25.types.user_list_number_rule_item_operator",
    "google.ads.googleads.v25.types.user_list_prepopulation_status",
    "google.ads.googleads.v25.types.user_list_rule_type",
    "google.ads.googleads.v25.types.user_list_size_range",
    "google.ads.googleads.v25.types.user_list_string_rule_item_operator",
    "google.ads.googleads.v25.types.user_list_type",
    "google.ads.googleads.v25.types.value_rule_device_type",
    "google.ads.googleads.v25.types.value_rule_geo_location_match_type",
    "google.ads.googleads.v25.types.value_rule_operation",
    "google.ads.googleads.v25.types.value_rule_set_attachment_type",
    "google.ads.googleads.v25.types.value_rule_set_dimension",
    "google.ads.googleads.v25.types.vanity_pharma_display_url_mode",
    "google.ads.googleads.v25.types.vanity_pharma_text",
    "google.ads.googleads.v25.types.vertical_ads_item_vertical_type",
    "google.ads.googleads.v25.types.video_ad_format_restriction",
    "google.ads.googleads.v25.types.video_ad_sequence_interaction_type",
    "google.ads.googleads.v25.types.video_ad_sequence_minimum_duration",
    "google.ads.googleads.v25.types.video_enhancement_source",
    "google.ads.googleads.v25.types.video_experiment_subtype",
    "google.ads.googleads.v25.types.video_thumbnail",
    "google.ads.googleads.v25.types.webpage_condition_operand",
    "google.ads.googleads.v25.types.webpage_condition_operator",
    "google.ads.googleads.v25.types.youtube_video_privacy",
    "google.ads.googleads.v25.types.youtube_video_property",
    "google.ads.googleads.v25.types.youtube_video_upload_state",
}


from .types.access_invitation_status import AccessInvitationStatusEnum
from .types.access_reason import AccessReasonEnum
from .types.access_role import AccessRoleEnum
from .types.account_budget_proposal_status import (
    AccountBudgetProposalStatusEnum,
)
from .types.account_budget_proposal_type import AccountBudgetProposalTypeEnum
from .types.account_budget_status import AccountBudgetStatusEnum
from .types.account_link_status import AccountLinkStatusEnum
from .types.ad_destination_type import AdDestinationTypeEnum
from .types.ad_format_type import AdFormatTypeEnum
from .types.ad_group_ad_primary_status import AdGroupAdPrimaryStatusEnum
from .types.ad_group_ad_primary_status_reason import (
    AdGroupAdPrimaryStatusReasonEnum,
)
from .types.ad_group_ad_rotation_mode import AdGroupAdRotationModeEnum
from .types.ad_group_ad_status import AdGroupAdStatusEnum
from .types.ad_group_criterion_approval_status import (
    AdGroupCriterionApprovalStatusEnum,
)
from .types.ad_group_criterion_primary_status import (
    AdGroupCriterionPrimaryStatusEnum,
)
from .types.ad_group_criterion_primary_status_reason import (
    AdGroupCriterionPrimaryStatusReasonEnum,
)
from .types.ad_group_criterion_status import AdGroupCriterionStatusEnum
from .types.ad_group_primary_status import AdGroupPrimaryStatusEnum
from .types.ad_group_primary_status_reason import AdGroupPrimaryStatusReasonEnum
from .types.ad_group_status import AdGroupStatusEnum
from .types.ad_group_type import AdGroupTypeEnum
from .types.ad_network_type import AdNetworkTypeEnum
from .types.ad_serving_optimization_status import (
    AdServingOptimizationStatusEnum,
)
from .types.ad_strength import AdStrengthEnum
from .types.ad_strength_action_item_type import AdStrengthActionItemTypeEnum
from .types.ad_sub_format_type import AdSubFormatTypeEnum
from .types.ad_sub_network_type import AdSubNetworkTypeEnum
from .types.ad_type import AdTypeEnum
from .types.advertising_channel_sub_type import AdvertisingChannelSubTypeEnum
from .types.advertising_channel_type import AdvertisingChannelTypeEnum
from .types.age_range_type import AgeRangeTypeEnum
from .types.android_privacy_interaction_type import (
    AndroidPrivacyInteractionTypeEnum,
)
from .types.android_privacy_network_type import AndroidPrivacyNetworkTypeEnum
from .types.app_bidding_goal import AppBiddingGoalEnum
from .types.app_campaign_app_store import AppCampaignAppStoreEnum
from .types.app_campaign_bidding_strategy_goal_type import (
    AppCampaignBiddingStrategyGoalTypeEnum,
)
from .types.app_payment_model_type import AppPaymentModelTypeEnum
from .types.app_url_operating_system_type import AppUrlOperatingSystemTypeEnum
from .types.application_instance import ApplicationInstanceEnum
from .types.asset_automation_status import AssetAutomationStatusEnum
from .types.asset_automation_type import AssetAutomationTypeEnum
from .types.asset_coverage_video_aspect_ratio_requirement import (
    AssetCoverageVideoAspectRatioRequirementEnum,
)
from .types.asset_field_type import AssetFieldTypeEnum
from .types.asset_group_primary_status import AssetGroupPrimaryStatusEnum
from .types.asset_group_primary_status_reason import (
    AssetGroupPrimaryStatusReasonEnum,
)
from .types.asset_group_signal_approval_status import (
    AssetGroupSignalApprovalStatusEnum,
)
from .types.asset_group_status import AssetGroupStatusEnum
from .types.asset_link_primary_status import AssetLinkPrimaryStatusEnum
from .types.asset_link_primary_status_reason import (
    AssetLinkPrimaryStatusReasonEnum,
)
from .types.asset_link_status import AssetLinkStatusEnum
from .types.asset_offline_evaluation_error_reasons import (
    AssetOfflineEvaluationErrorReasonsEnum,
)
from .types.asset_orientation import AssetOrientationEnum
from .types.asset_performance_label import AssetPerformanceLabelEnum
from .types.asset_set_asset_status import AssetSetAssetStatusEnum
from .types.asset_set_link_status import AssetSetLinkStatusEnum
from .types.asset_set_status import AssetSetStatusEnum
from .types.asset_set_type import AssetSetTypeEnum
from .types.asset_source import AssetSourceEnum
from .types.asset_type import AssetTypeEnum
from .types.async_action_status import AsyncActionStatusEnum
from .types.attribution_model import AttributionModelEnum
from .types.audience_insights_dimension import AudienceInsightsDimensionEnum
from .types.audience_insights_marketing_objective import (
    AudienceInsightsMarketingObjectiveEnum,
)
from .types.audience_scope import AudienceScopeEnum
from .types.audience_status import AudienceStatusEnum
from .types.batch_job_status import BatchJobStatusEnum
from .types.benchmarks_marketing_objective import (
    BenchmarksMarketingObjectiveEnum,
)
from .types.benchmarks_source_type import BenchmarksSourceTypeEnum
from .types.benchmarks_time_granularity import BenchmarksTimeGranularityEnum
from .types.bid_modifier_source import BidModifierSourceEnum
from .types.bidding_source import BiddingSourceEnum
from .types.bidding_strategy_status import BiddingStrategyStatusEnum
from .types.bidding_strategy_system_status import (
    BiddingStrategySystemStatusEnum,
)
from .types.bidding_strategy_type import BiddingStrategyTypeEnum
from .types.billing_setup_status import BillingSetupStatusEnum
from .types.booking_status import BookingStatusEnum
from .types.brand_lift_measurement_type import BrandLiftMeasurementTypeEnum
from .types.brand_request_rejection_reason import (
    BrandRequestRejectionReasonEnum,
)
from .types.brand_safety_suitability import BrandSafetySuitabilityEnum
from .types.brand_state import BrandStateEnum
from .types.budget_campaign_association_status import (
    BudgetCampaignAssociationStatusEnum,
)
from .types.budget_delivery_method import BudgetDeliveryMethodEnum
from .types.budget_period import BudgetPeriodEnum
from .types.budget_status import BudgetStatusEnum
from .types.budget_type import BudgetTypeEnum
from .types.business_message_call_to_action_type import (
    BusinessMessageCallToActionTypeEnum,
)
from .types.business_message_provider import BusinessMessageProviderEnum
from .types.call_conversion_reporting_state import (
    CallConversionReportingStateEnum,
)
from .types.call_to_action_type import CallToActionTypeEnum
from .types.call_tracking_display_location import (
    CallTrackingDisplayLocationEnum,
)
from .types.call_type import CallTypeEnum
from .types.campaign_criterion_status import CampaignCriterionStatusEnum
from .types.campaign_draft_status import CampaignDraftStatusEnum
from .types.campaign_experiment_type import CampaignExperimentTypeEnum
from .types.campaign_group_status import CampaignGroupStatusEnum
from .types.campaign_keyword_match_type import CampaignKeywordMatchTypeEnum
from .types.campaign_primary_status import CampaignPrimaryStatusEnum
from .types.campaign_primary_status_reason import (
    CampaignPrimaryStatusReasonEnum,
)
from .types.campaign_serving_status import CampaignServingStatusEnum
from .types.campaign_shared_set_status import CampaignSharedSetStatusEnum
from .types.campaign_status import CampaignStatusEnum
from .types.chain_relationship_type import ChainRelationshipTypeEnum
from .types.change_client_type import ChangeClientTypeEnum
from .types.change_event_resource_type import ChangeEventResourceTypeEnum
from .types.change_status_operation import ChangeStatusOperationEnum
from .types.change_status_resource_type import ChangeStatusResourceTypeEnum
from .types.click_type import ClickTypeEnum
from .types.combined_audience_status import CombinedAudienceStatusEnum
from .types.consent_status import ConsentStatusEnum
from .types.content_creator_insights_supplemental_data import (
    ContentCreatorInsightsSupplementalDataEnum,
)
from .types.content_label_type import ContentLabelTypeEnum
from .types.conversion_action_category import ConversionActionCategoryEnum
from .types.conversion_action_counting_type import (
    ConversionActionCountingTypeEnum,
)
from .types.conversion_action_status import ConversionActionStatusEnum
from .types.conversion_action_type import ConversionActionTypeEnum
from .types.conversion_adjustment_type import ConversionAdjustmentTypeEnum
from .types.conversion_attribution_event_type import (
    ConversionAttributionEventTypeEnum,
)
from .types.conversion_custom_variable_status import (
    ConversionCustomVariableStatusEnum,
)
from .types.conversion_customer_type import ConversionCustomerTypeEnum
from .types.conversion_environment_enum import ConversionEnvironmentEnum
from .types.conversion_lag_bucket import ConversionLagBucketEnum
from .types.conversion_lift_included_conversion_action_types import (
    ConversionLiftIncludedConversionActionTypesEnum,
)
from .types.conversion_or_adjustment_lag_bucket import (
    ConversionOrAdjustmentLagBucketEnum,
)
from .types.conversion_origin import ConversionOriginEnum
from .types.conversion_tracking_status_enum import ConversionTrackingStatusEnum
from .types.conversion_value_rule_primary_dimension import (
    ConversionValueRulePrimaryDimensionEnum,
)
from .types.conversion_value_rule_set_status import (
    ConversionValueRuleSetStatusEnum,
)
from .types.conversion_value_rule_status import ConversionValueRuleStatusEnum
from .types.converting_user_prior_engagement_type_and_ltv_bucket import (
    ConvertingUserPriorEngagementTypeAndLtvBucketEnum,
)
from .types.criterion_category_channel_availability_mode import (
    CriterionCategoryChannelAvailabilityModeEnum,
)
from .types.criterion_category_locale_availability_mode import (
    CriterionCategoryLocaleAvailabilityModeEnum,
)
from .types.criterion_system_serving_status import (
    CriterionSystemServingStatusEnum,
)
from .types.criterion_type import CriterionTypeEnum
from .types.custom_audience_member_type import CustomAudienceMemberTypeEnum
from .types.custom_audience_status import CustomAudienceStatusEnum
from .types.custom_audience_type import CustomAudienceTypeEnum
from .types.custom_conversion_goal_status import CustomConversionGoalStatusEnum
from .types.custom_interest_member_type import CustomInterestMemberTypeEnum
from .types.custom_interest_status import CustomInterestStatusEnum
from .types.custom_interest_type import CustomInterestTypeEnum
from .types.customer_lifecycle_optimization_goal_sub_type import (
    CustomerLifecycleOptimizationGoalSubTypeEnum,
)
from .types.customer_lifecycle_optimization_mode import (
    CustomerLifecycleOptimizationModeEnum,
)
from .types.customer_match_upload_key_type import CustomerMatchUploadKeyTypeEnum
from .types.customer_pay_per_conversion_eligibility_failure_reason import (
    CustomerPayPerConversionEligibilityFailureReasonEnum,
)
from .types.customer_status import CustomerStatusEnum
from .types.customizer_attribute_status import CustomizerAttributeStatusEnum
from .types.customizer_attribute_type import CustomizerAttributeTypeEnum
from .types.customizer_value_status import CustomizerValueStatusEnum
from .types.data_driven_model_status import DataDrivenModelStatusEnum
from .types.data_link_status import DataLinkStatusEnum
from .types.data_link_type import DataLinkTypeEnum
from .types.day_of_week import DayOfWeekEnum
from .types.demand_gen_channel_config import DemandGenChannelConfigEnum
from .types.demand_gen_channel_strategy import DemandGenChannelStrategyEnum
from .types.device import DeviceEnum
from .types.display_ad_format_setting import DisplayAdFormatSettingEnum
from .types.display_upload_product_type import DisplayUploadProductTypeEnum
from .types.distance_bucket import DistanceBucketEnum
from .types.eu_political_advertising_status import (
    EuPoliticalAdvertisingStatusEnum,
)
from .types.experiment_asset_detail_operation import (
    ExperimentAssetDetailOperationEnum,
)
from .types.experiment_metric import ExperimentMetricEnum
from .types.experiment_metric_direction import ExperimentMetricDirectionEnum
from .types.experiment_status import ExperimentStatusEnum
from .types.experiment_type import ExperimentTypeEnum
from .types.external_conversion_source import ExternalConversionSourceEnum
from .types.fixed_cpm_goal import FixedCpmGoalEnum
from .types.fixed_cpm_target_frequency_time_unit import (
    FixedCpmTargetFrequencyTimeUnitEnum,
)
from .types.frequency_cap_event_type import FrequencyCapEventTypeEnum
from .types.frequency_cap_level import FrequencyCapLevelEnum
from .types.frequency_cap_time_unit import FrequencyCapTimeUnitEnum
from .types.gender_type import GenderTypeEnum
from .types.geo_target_constant_status import GeoTargetConstantStatusEnum
from .types.geo_targeting_type import GeoTargetingTypeEnum
from .types.gls_phone_number_type import GlsPhoneNumberTypeEnum
from .types.goal_config_level import GoalConfigLevelEnum
from .types.goal_optimization_eligibility import GoalOptimizationEligibilityEnum
from .types.goal_type import GoalTypeEnum
from .types.google_ads_field_category import GoogleAdsFieldCategoryEnum
from .types.google_ads_field_data_type import GoogleAdsFieldDataTypeEnum
from .types.google_voice_call_status import GoogleVoiceCallStatusEnum
from .types.hotel_asset_suggestion_status import HotelAssetSuggestionStatusEnum
from .types.hotel_date_selection_type import HotelDateSelectionTypeEnum
from .types.hotel_price_bucket import HotelPriceBucketEnum
from .types.hotel_rate_type import HotelRateTypeEnum
from .types.hotel_reconciliation_status import HotelReconciliationStatusEnum
from .types.identity_verification_program import IdentityVerificationProgramEnum
from .types.identity_verification_program_status import (
    IdentityVerificationProgramStatusEnum,
)
from .types.incentive_offer_type import IncentiveOfferTypeEnum
from .types.incentive_state import IncentiveStateEnum
from .types.incentive_type import IncentiveTypeEnum
from .types.income_range_type import IncomeRangeTypeEnum
from .types.insights_knowledge_graph_entity_capabilities import (
    InsightsKnowledgeGraphEntityCapabilitiesEnum,
)
from .types.insights_trend import InsightsTrendEnum
from .types.interaction_event_type import InteractionEventTypeEnum
from .types.interaction_type import InteractionTypeEnum
from .types.invoice_type import InvoiceTypeEnum
from .types.keyword_match_type import KeywordMatchTypeEnum
from .types.keyword_plan_aggregate_metric_type import (
    KeywordPlanAggregateMetricTypeEnum,
)
from .types.keyword_plan_competition_level import (
    KeywordPlanCompetitionLevelEnum,
)
from .types.keyword_plan_concept_group_type import (
    KeywordPlanConceptGroupTypeEnum,
)
from .types.keyword_plan_forecast_interval import (
    KeywordPlanForecastIntervalEnum,
)
from .types.keyword_plan_keyword_annotation import (
    KeywordPlanKeywordAnnotationEnum,
)
from .types.keyword_plan_network import KeywordPlanNetworkEnum
from .types.label_status import LabelStatusEnum
from .types.landing_page_source import LandingPageSourceEnum
from .types.lead_form_call_to_action_type import LeadFormCallToActionTypeEnum
from .types.lead_form_desired_intent import LeadFormDesiredIntentEnum
from .types.lead_form_field_user_input_type import (
    LeadFormFieldUserInputTypeEnum,
)
from .types.lead_form_post_submit_call_to_action_type import (
    LeadFormPostSubmitCallToActionTypeEnum,
)
from .types.legacy_app_install_ad_app_store import (
    LegacyAppInstallAdAppStoreEnum,
)
from .types.lift_measurement_flight_status import (
    LiftMeasurementFlightStatusEnum,
)
from .types.lift_metric_type import LiftMetricTypeEnum
from .types.linked_account_type import LinkedAccountTypeEnum
from .types.linked_product_type import LinkedProductTypeEnum
from .types.listing_group_filter_custom_attribute_index import (
    ListingGroupFilterCustomAttributeIndexEnum,
)
from .types.listing_group_filter_listing_source import (
    ListingGroupFilterListingSourceEnum,
)
from .types.listing_group_filter_product_category_level import (
    ListingGroupFilterProductCategoryLevelEnum,
)
from .types.listing_group_filter_product_channel import (
    ListingGroupFilterProductChannelEnum,
)
from .types.listing_group_filter_product_condition import (
    ListingGroupFilterProductConditionEnum,
)
from .types.listing_group_filter_product_type_level import (
    ListingGroupFilterProductTypeLevelEnum,
)
from .types.listing_group_filter_type_enum import ListingGroupFilterTypeEnum
from .types.listing_group_type import ListingGroupTypeEnum
from .types.listing_type import ListingTypeEnum
from .types.local_services_business_registration_check_rejection_reason import (
    LocalServicesBusinessRegistrationCheckRejectionReasonEnum,
)
from .types.local_services_business_registration_type import (
    LocalServicesBusinessRegistrationTypeEnum,
)
from .types.local_services_conversation_type import (
    LocalServicesLeadConversationTypeEnum,
)
from .types.local_services_employee_status import (
    LocalServicesEmployeeStatusEnum,
)
from .types.local_services_employee_type import LocalServicesEmployeeTypeEnum
from .types.local_services_insurance_rejection_reason import (
    LocalServicesInsuranceRejectionReasonEnum,
)
from .types.local_services_lead_credit_issuance_decision import (
    LocalServicesLeadCreditIssuanceDecisionEnum,
)
from .types.local_services_lead_credit_state import LocalServicesCreditStateEnum
from .types.local_services_lead_status import LocalServicesLeadStatusEnum
from .types.local_services_lead_survey_answer import (
    LocalServicesLeadSurveyAnswerEnum,
)
from .types.local_services_lead_survey_dissatisfied_reason import (
    LocalServicesLeadSurveyDissatisfiedReasonEnum,
)
from .types.local_services_lead_survey_satisfied_reason import (
    LocalServicesLeadSurveySatisfiedReasonEnum,
)
from .types.local_services_lead_type import LocalServicesLeadTypeEnum
from .types.local_services_license_rejection_reason import (
    LocalServicesLicenseRejectionReasonEnum,
)
from .types.local_services_participant_type import (
    LocalServicesParticipantTypeEnum,
)
from .types.local_services_verification_artifact_status import (
    LocalServicesVerificationArtifactStatusEnum,
)
from .types.local_services_verification_artifact_type import (
    LocalServicesVerificationArtifactTypeEnum,
)
from .types.local_services_verification_status import (
    LocalServicesVerificationStatusEnum,
)
from .types.location_group_radius_units import LocationGroupRadiusUnitsEnum
from .types.location_ownership_type import LocationOwnershipTypeEnum
from .types.location_source_type import LocationSourceTypeEnum
from .types.location_string_filter_type import LocationStringFilterTypeEnum
from .types.lookalike_expansion_level import LookalikeExpansionLevelEnum
from .types.loyalty_membership import LoyaltyMembershipEnum
from .types.manager_link_status import ManagerLinkStatusEnum
from .types.match_type import MatchTypeEnum
from .types.media_type import MediaTypeEnum
from .types.messaging_restriction_type import MessagingRestrictionTypeEnum
from .types.mime_type import MimeTypeEnum
from .types.minute_of_hour import MinuteOfHourEnum
from .types.mobile_app_vendor import MobileAppVendorEnum
from .types.mobile_device_platform import MobileDevicePlatformEnum
from .types.mobile_device_type import MobileDeviceTypeEnum
from .types.month_of_year import MonthOfYearEnum
from .types.multi_party_auth_operation_type import (
    MultiPartyAuthOperationTypeEnum,
)
from .types.multi_party_auth_review_status import MultiPartyAuthReviewStatusEnum
from .types.multi_party_auth_review_target_resource import (
    MultiPartyAuthReviewTargetResourceEnum,
)
from .types.negative_geo_target_type import NegativeGeoTargetTypeEnum
from .types.non_skippable_max_duration import NonSkippableMaxDurationEnum
from .types.non_skippable_min_duration import NonSkippableMinDurationEnum
from .types.offline_conversion_diagnostic_status_enum import (
    OfflineConversionDiagnosticStatusEnum,
)
from .types.offline_event_upload_client_enum import OfflineEventUploadClientEnum
from .types.offline_user_data_job_failure_reason import (
    OfflineUserDataJobFailureReasonEnum,
)
from .types.offline_user_data_job_match_rate_range import (
    OfflineUserDataJobMatchRateRangeEnum,
)
from .types.offline_user_data_job_status import OfflineUserDataJobStatusEnum
from .types.offline_user_data_job_type import OfflineUserDataJobTypeEnum
from .types.operating_system_version_operator_type import (
    OperatingSystemVersionOperatorTypeEnum,
)
from .types.optimization_goal_type import OptimizationGoalTypeEnum
from .types.optimize_assets_experiment_subtype import (
    OptimizeAssetsExperimentSubtypeEnum,
)
from .types.parental_status_type import ParentalStatusTypeEnum
from .types.partnership_opportunity import PartnershipOpportunityEnum
from .types.payment_mode import PaymentModeEnum
from .types.performance_max_upgrade_status import (
    PerformanceMaxUpgradeStatusEnum,
)
from .types.placement_type import PlacementTypeEnum
from .types.policy_approval_status import PolicyApprovalStatusEnum
from .types.policy_review_status import PolicyReviewStatusEnum
from .types.policy_topic_entry_type import PolicyTopicEntryTypeEnum
from .types.policy_topic_evidence_destination_mismatch_url_type import (
    PolicyTopicEvidenceDestinationMismatchUrlTypeEnum,
)
from .types.policy_topic_evidence_destination_not_working_device import (
    PolicyTopicEvidenceDestinationNotWorkingDeviceEnum,
)
from .types.policy_topic_evidence_destination_not_working_dns_error_type import (
    PolicyTopicEvidenceDestinationNotWorkingDnsErrorTypeEnum,
)
from .types.positive_geo_target_type import PositiveGeoTargetTypeEnum
from .types.preview_type import PreviewTypeEnum
from .types.price_extension_price_qualifier import (
    PriceExtensionPriceQualifierEnum,
)
from .types.price_extension_price_unit import PriceExtensionPriceUnitEnum
from .types.price_extension_type import PriceExtensionTypeEnum
from .types.product_availability import ProductAvailabilityEnum
from .types.product_category_level import ProductCategoryLevelEnum
from .types.product_category_state import ProductCategoryStateEnum
from .types.product_channel import ProductChannelEnum
from .types.product_channel_exclusivity import ProductChannelExclusivityEnum
from .types.product_condition import ProductConditionEnum
from .types.product_custom_attribute_index import (
    ProductCustomAttributeIndexEnum,
)
from .types.product_issue_severity import ProductIssueSeverityEnum
from .types.product_link_invitation_status import (
    ProductLinkInvitationStatusEnum,
)
from .types.product_status import ProductStatusEnum
from .types.product_type_level import ProductTypeLevelEnum
from .types.promotion_barcode_type import PromotionBarcodeTypeEnum
from .types.promotion_extension_discount_modifier import (
    PromotionExtensionDiscountModifierEnum,
)
from .types.promotion_extension_occasion import PromotionExtensionOccasionEnum
from .types.proximity_radius_units import ProximityRadiusUnitsEnum
from .types.quality_score_bucket import QualityScoreBucketEnum
from .types.reach_plan_age_range import ReachPlanAgeRangeEnum
from .types.reach_plan_buying_method import ReachPlanBuyingMethodEnum
from .types.reach_plan_conversion_rate_model import (
    ReachPlanConversionRateModelEnum,
)
from .types.reach_plan_cost_model import ReachPlanCostModelEnum
from .types.reach_plan_marketing_objective import (
    ReachPlanMarketingObjectiveEnum,
)
from .types.reach_plan_network import ReachPlanNetworkEnum
from .types.reach_plan_plannable_user_list_status import (
    ReachPlanPlannableUserListStatusEnum,
)
from .types.reach_plan_surface import ReachPlanSurfaceEnum
from .types.recommendation_subscription_status import (
    RecommendationSubscriptionStatusEnum,
)
from .types.recommendation_type import RecommendationTypeEnum
from .types.regulatory_fee_type import RegulatoryFeeTypeEnum
from .types.reservation_request_type import ReservationRequestTypeEnum
from .types.resource_change_operation import ResourceChangeOperationEnum
from .types.resource_limit_type import ResourceLimitTypeEnum
from .types.response_content_type import ResponseContentTypeEnum
from .types.search_engine_results_page_type import (
    SearchEngineResultsPageTypeEnum,
)
from .types.search_term_match_source import SearchTermMatchSourceEnum
from .types.search_term_match_type import SearchTermMatchTypeEnum
from .types.search_term_targeting_status import SearchTermTargetingStatusEnum
from .types.seasonality_event_scope import SeasonalityEventScopeEnum
from .types.seasonality_event_status import SeasonalityEventStatusEnum
from .types.sentiment import SentimentEnum
from .types.served_asset_field_type import ServedAssetFieldTypeEnum
from .types.shared_set_status import SharedSetStatusEnum
from .types.shared_set_type import SharedSetTypeEnum
from .types.shopping_add_products_to_campaign_recommendation_enum import (
    ShoppingAddProductsToCampaignRecommendationEnum,
)
from .types.simulation_modification_method import (
    SimulationModificationMethodEnum,
)
from .types.simulation_type import SimulationTypeEnum
from .types.sk_ad_network_ad_event_type import SkAdNetworkAdEventTypeEnum
from .types.sk_ad_network_attribution_credit import (
    SkAdNetworkAttributionCreditEnum,
)
from .types.sk_ad_network_coarse_conversion_value import (
    SkAdNetworkCoarseConversionValueEnum,
)
from .types.sk_ad_network_source_type import SkAdNetworkSourceTypeEnum
from .types.sk_ad_network_user_type import SkAdNetworkUserTypeEnum
from .types.slot import SlotEnum
from .types.smart_campaign_not_eligible_reason import (
    SmartCampaignNotEligibleReasonEnum,
)
from .types.smart_campaign_status import SmartCampaignStatusEnum
from .types.spending_limit_type import SpendingLimitTypeEnum
from .types.summary_row_setting import SummaryRowSettingEnum
from .types.survey_intended_action import SurveyIntendedActionEnum
from .types.survey_lift_flight_target_response_mode import (
    SurveyLiftFlightTargetResponseModeEnum,
)
from .types.survey_subject_type import SurveySubjectTypeEnum
from .types.synthetic_content_attestation_status import (
    SyntheticContentAttestationStatusEnum,
)
from .types.synthetic_content_source import SyntheticContentSourceEnum
from .types.system_managed_entity_source import SystemManagedResourceSourceEnum
from .types.target_cpa_opt_in_recommendation_goal import (
    TargetCpaOptInRecommendationGoalEnum,
)
from .types.target_frequency_time_unit import TargetFrequencyTimeUnitEnum
from .types.target_impression_share_location import (
    TargetImpressionShareLocationEnum,
)
from .types.targeting_dimension import TargetingDimensionEnum
from .types.third_party_brand_lift_integration_partner import (
    ThirdPartyBrandLiftIntegrationPartnerEnum,
)
from .types.third_party_brand_safety_integration_partner import (
    ThirdPartyBrandSafetyIntegrationPartnerEnum,
)
from .types.third_party_conversion_attribution_integration_partner import (
    ThirdPartyConversionAttributionIntegrationPartnerEnum,
)
from .types.third_party_reach_integration_partner import (
    ThirdPartyReachIntegrationPartnerEnum,
)
from .types.third_party_viewability_integration_partner import (
    ThirdPartyViewabilityIntegrationPartnerEnum,
)
from .types.time_type import TimeTypeEnum
from .types.tracking_code_page_format import TrackingCodePageFormatEnum
from .types.tracking_code_type import TrackingCodeTypeEnum
from .types.unit_of_measure import UnitOfMeasureEnum
from .types.user_identifier_source import UserIdentifierSourceEnum
from .types.user_interest_taxonomy_type import UserInterestTaxonomyTypeEnum
from .types.user_list_access_status import UserListAccessStatusEnum
from .types.user_list_closing_reason import UserListClosingReasonEnum
from .types.user_list_crm_data_source_type import UserListCrmDataSourceTypeEnum
from .types.user_list_customer_type_category import (
    UserListCustomerTypeCategoryEnum,
)
from .types.user_list_date_rule_item_operator import (
    UserListDateRuleItemOperatorEnum,
)
from .types.user_list_flexible_rule_operator import (
    UserListFlexibleRuleOperatorEnum,
)
from .types.user_list_logical_rule_operator import (
    UserListLogicalRuleOperatorEnum,
)
from .types.user_list_membership_status import UserListMembershipStatusEnum
from .types.user_list_number_rule_item_operator import (
    UserListNumberRuleItemOperatorEnum,
)
from .types.user_list_prepopulation_status import (
    UserListPrepopulationStatusEnum,
)
from .types.user_list_rule_type import UserListRuleTypeEnum
from .types.user_list_size_range import UserListSizeRangeEnum
from .types.user_list_string_rule_item_operator import (
    UserListStringRuleItemOperatorEnum,
)
from .types.user_list_type import UserListTypeEnum
from .types.value_rule_device_type import ValueRuleDeviceTypeEnum
from .types.value_rule_geo_location_match_type import (
    ValueRuleGeoLocationMatchTypeEnum,
)
from .types.value_rule_operation import ValueRuleOperationEnum
from .types.value_rule_set_attachment_type import ValueRuleSetAttachmentTypeEnum
from .types.value_rule_set_dimension import ValueRuleSetDimensionEnum
from .types.vanity_pharma_display_url_mode import VanityPharmaDisplayUrlModeEnum
from .types.vanity_pharma_text import VanityPharmaTextEnum
from .types.vertical_ads_item_vertical_type import (
    VerticalAdsItemVerticalTypeEnum,
)
from .types.video_ad_format_restriction import VideoAdFormatRestrictionEnum
from .types.video_ad_sequence_interaction_type import (
    VideoAdSequenceInteractionTypeEnum,
)
from .types.video_ad_sequence_minimum_duration import (
    VideoAdSequenceMinimumDurationEnum,
)
from .types.video_enhancement_source import VideoEnhancementSourceEnum
from .types.video_experiment_subtype import VideoExperimentSubtypeEnum
from .types.video_thumbnail import VideoThumbnailEnum
from .types.webpage_condition_operand import WebpageConditionOperandEnum
from .types.webpage_condition_operator import WebpageConditionOperatorEnum
from .types.youtube_video_privacy import YouTubeVideoPrivacyEnum
from .types.youtube_video_property import YouTubeVideoPropertyEnum
from .types.youtube_video_upload_state import YouTubeVideoUploadStateEnum

if hasattr(api_core, "check_python_version") and hasattr(
    api_core, "check_dependency_versions"
):  # pragma: NO COVER
    api_core.check_python_version("google.ads.googleads.v25")  # type: ignore
    api_core.check_dependency_versions("google.ads.googleads.v25")  # type: ignore
else:  # pragma: NO COVER
    # An older version of api_core is installed which does not define the
    # functions above. We do equivalent checks manually.
    try:
        import warnings

        _py_version_str = sys.version.split()[0]
        _package_label = "google.ads.googleads.v25"
        if sys.version_info < (3, 10):
            warnings.warn(
                "You are using a non-supported Python version "
                + f"({_py_version_str}).  Google will not post any further "
                + f"updates to {_package_label} supporting this Python version. "
                + "Please upgrade to the latest Python version, or at "
                + f"least to Python 3.10, and then update {_package_label}.",
                FutureWarning,
            )

        def parse_version_to_tuple(version_string: str):
            """Safely converts a semantic version string to a comparable tuple of integers.
            Example: "6.33.5" -> (6, 33, 5)
            Ignores non-numeric parts and handles common version formats.
            Args:
                version_string: Version string in the format "x.y.z" or "x.y.z<suffix>"
            Returns:
                Tuple of integers for the parsed version string.
            """
            parts = []
            for part in version_string.split("."):
                try:
                    parts.append(int(part))
                except ValueError:
                    # If it's a non-numeric part (e.g., '1.0.0b1' -> 'b1'), stop here.
                    # This is a simplification compared to 'packaging.parse_version', but sufficient
                    # for comparing strictly numeric semantic versions.
                    break
            return tuple(parts)

        def _get_version(dependency_name):
            try:
                version_string: str = metadata.version(dependency_name)
                parsed_version = parse_version_to_tuple(version_string)
                return (parsed_version, version_string)
            except Exception:
                # Catch exceptions from metadata.version() (e.g., PackageNotFoundError)
                # or errors during parse_version_to_tuple
                return (None, "--")

        _dependency_package = "google.protobuf"
        _next_supported_version = "6.33.5"
        _next_supported_version_tuple = (6, 33, 5)
        _recommendation = " (we recommend 7.x)"
        (_version_used, _version_used_string) = _get_version(
            _dependency_package
        )
        if _version_used and _version_used < _next_supported_version_tuple:
            warnings.warn(
                f"Package {_package_label} depends on "
                + f"{_dependency_package}, currently installed at version "
                + f"{_version_used_string}. Future updates to "
                + f"{_package_label} will require {_dependency_package} at "
                + f"version {_next_supported_version} or higher{_recommendation}."
                + " Please ensure "
                + "that either (a) your Python environment doesn't pin the "
                + f"version of {_dependency_package}, so that updates to "
                + f"{_package_label} can require the higher version, or "
                + "(b) you manually update your Python environment to use at "
                + f"least version {_next_supported_version} of "
                + f"{_dependency_package}.",
                FutureWarning,
            )
    except Exception:
        warnings.warn(
            "Could not determine the version of Python "
            + "currently being used. To continue receiving "
            + "updates for {_package_label}, ensure you are "
            + "using a supported version of Python; see "
            + "https://devguide.python.org/versions/"
        )

__all__ = (
    "AccessInvitationStatusEnum",
    "AccessReasonEnum",
    "AccessRoleEnum",
    "AccountBudgetProposalStatusEnum",
    "AccountBudgetProposalTypeEnum",
    "AccountBudgetStatusEnum",
    "AccountLinkStatusEnum",
    "AdDestinationTypeEnum",
    "AdFormatTypeEnum",
    "AdGroupAdPrimaryStatusEnum",
    "AdGroupAdPrimaryStatusReasonEnum",
    "AdGroupAdRotationModeEnum",
    "AdGroupAdStatusEnum",
    "AdGroupCriterionApprovalStatusEnum",
    "AdGroupCriterionPrimaryStatusEnum",
    "AdGroupCriterionPrimaryStatusReasonEnum",
    "AdGroupCriterionStatusEnum",
    "AdGroupPrimaryStatusEnum",
    "AdGroupPrimaryStatusReasonEnum",
    "AdGroupStatusEnum",
    "AdGroupTypeEnum",
    "AdNetworkTypeEnum",
    "AdServingOptimizationStatusEnum",
    "AdStrengthActionItemTypeEnum",
    "AdStrengthEnum",
    "AdSubFormatTypeEnum",
    "AdSubNetworkTypeEnum",
    "AdTypeEnum",
    "AdvertisingChannelSubTypeEnum",
    "AdvertisingChannelTypeEnum",
    "AgeRangeTypeEnum",
    "AndroidPrivacyInteractionTypeEnum",
    "AndroidPrivacyNetworkTypeEnum",
    "AppBiddingGoalEnum",
    "AppCampaignAppStoreEnum",
    "AppCampaignBiddingStrategyGoalTypeEnum",
    "AppPaymentModelTypeEnum",
    "AppUrlOperatingSystemTypeEnum",
    "ApplicationInstanceEnum",
    "AssetAutomationStatusEnum",
    "AssetAutomationTypeEnum",
    "AssetCoverageVideoAspectRatioRequirementEnum",
    "AssetFieldTypeEnum",
    "AssetGroupPrimaryStatusEnum",
    "AssetGroupPrimaryStatusReasonEnum",
    "AssetGroupSignalApprovalStatusEnum",
    "AssetGroupStatusEnum",
    "AssetLinkPrimaryStatusEnum",
    "AssetLinkPrimaryStatusReasonEnum",
    "AssetLinkStatusEnum",
    "AssetOfflineEvaluationErrorReasonsEnum",
    "AssetOrientationEnum",
    "AssetPerformanceLabelEnum",
    "AssetSetAssetStatusEnum",
    "AssetSetLinkStatusEnum",
    "AssetSetStatusEnum",
    "AssetSetTypeEnum",
    "AssetSourceEnum",
    "AssetTypeEnum",
    "AsyncActionStatusEnum",
    "AttributionModelEnum",
    "AudienceInsightsDimensionEnum",
    "AudienceInsightsMarketingObjectiveEnum",
    "AudienceScopeEnum",
    "AudienceStatusEnum",
    "BatchJobStatusEnum",
    "BenchmarksMarketingObjectiveEnum",
    "BenchmarksSourceTypeEnum",
    "BenchmarksTimeGranularityEnum",
    "BidModifierSourceEnum",
    "BiddingSourceEnum",
    "BiddingStrategyStatusEnum",
    "BiddingStrategySystemStatusEnum",
    "BiddingStrategyTypeEnum",
    "BillingSetupStatusEnum",
    "BookingStatusEnum",
    "BrandLiftMeasurementTypeEnum",
    "BrandRequestRejectionReasonEnum",
    "BrandSafetySuitabilityEnum",
    "BrandStateEnum",
    "BudgetCampaignAssociationStatusEnum",
    "BudgetDeliveryMethodEnum",
    "BudgetPeriodEnum",
    "BudgetStatusEnum",
    "BudgetTypeEnum",
    "BusinessMessageCallToActionTypeEnum",
    "BusinessMessageProviderEnum",
    "CallConversionReportingStateEnum",
    "CallToActionTypeEnum",
    "CallTrackingDisplayLocationEnum",
    "CallTypeEnum",
    "CampaignCriterionStatusEnum",
    "CampaignDraftStatusEnum",
    "CampaignExperimentTypeEnum",
    "CampaignGroupStatusEnum",
    "CampaignKeywordMatchTypeEnum",
    "CampaignPrimaryStatusEnum",
    "CampaignPrimaryStatusReasonEnum",
    "CampaignServingStatusEnum",
    "CampaignSharedSetStatusEnum",
    "CampaignStatusEnum",
    "ChainRelationshipTypeEnum",
    "ChangeClientTypeEnum",
    "ChangeEventResourceTypeEnum",
    "ChangeStatusOperationEnum",
    "ChangeStatusResourceTypeEnum",
    "ClickTypeEnum",
    "CombinedAudienceStatusEnum",
    "ConsentStatusEnum",
    "ContentCreatorInsightsSupplementalDataEnum",
    "ContentLabelTypeEnum",
    "ConversionActionCategoryEnum",
    "ConversionActionCountingTypeEnum",
    "ConversionActionStatusEnum",
    "ConversionActionTypeEnum",
    "ConversionAdjustmentTypeEnum",
    "ConversionAttributionEventTypeEnum",
    "ConversionCustomVariableStatusEnum",
    "ConversionCustomerTypeEnum",
    "ConversionEnvironmentEnum",
    "ConversionLagBucketEnum",
    "ConversionLiftIncludedConversionActionTypesEnum",
    "ConversionOrAdjustmentLagBucketEnum",
    "ConversionOriginEnum",
    "ConversionTrackingStatusEnum",
    "ConversionValueRulePrimaryDimensionEnum",
    "ConversionValueRuleSetStatusEnum",
    "ConversionValueRuleStatusEnum",
    "ConvertingUserPriorEngagementTypeAndLtvBucketEnum",
    "CriterionCategoryChannelAvailabilityModeEnum",
    "CriterionCategoryLocaleAvailabilityModeEnum",
    "CriterionSystemServingStatusEnum",
    "CriterionTypeEnum",
    "CustomAudienceMemberTypeEnum",
    "CustomAudienceStatusEnum",
    "CustomAudienceTypeEnum",
    "CustomConversionGoalStatusEnum",
    "CustomInterestMemberTypeEnum",
    "CustomInterestStatusEnum",
    "CustomInterestTypeEnum",
    "CustomerLifecycleOptimizationGoalSubTypeEnum",
    "CustomerLifecycleOptimizationModeEnum",
    "CustomerMatchUploadKeyTypeEnum",
    "CustomerPayPerConversionEligibilityFailureReasonEnum",
    "CustomerStatusEnum",
    "CustomizerAttributeStatusEnum",
    "CustomizerAttributeTypeEnum",
    "CustomizerValueStatusEnum",
    "DataDrivenModelStatusEnum",
    "DataLinkStatusEnum",
    "DataLinkTypeEnum",
    "DayOfWeekEnum",
    "DemandGenChannelConfigEnum",
    "DemandGenChannelStrategyEnum",
    "DeviceEnum",
    "DisplayAdFormatSettingEnum",
    "DisplayUploadProductTypeEnum",
    "DistanceBucketEnum",
    "EuPoliticalAdvertisingStatusEnum",
    "ExperimentAssetDetailOperationEnum",
    "ExperimentMetricDirectionEnum",
    "ExperimentMetricEnum",
    "ExperimentStatusEnum",
    "ExperimentTypeEnum",
    "ExternalConversionSourceEnum",
    "FixedCpmGoalEnum",
    "FixedCpmTargetFrequencyTimeUnitEnum",
    "FrequencyCapEventTypeEnum",
    "FrequencyCapLevelEnum",
    "FrequencyCapTimeUnitEnum",
    "GenderTypeEnum",
    "GeoTargetConstantStatusEnum",
    "GeoTargetingTypeEnum",
    "GlsPhoneNumberTypeEnum",
    "GoalConfigLevelEnum",
    "GoalOptimizationEligibilityEnum",
    "GoalTypeEnum",
    "GoogleAdsFieldCategoryEnum",
    "GoogleAdsFieldDataTypeEnum",
    "GoogleVoiceCallStatusEnum",
    "HotelAssetSuggestionStatusEnum",
    "HotelDateSelectionTypeEnum",
    "HotelPriceBucketEnum",
    "HotelRateTypeEnum",
    "HotelReconciliationStatusEnum",
    "IdentityVerificationProgramEnum",
    "IdentityVerificationProgramStatusEnum",
    "IncentiveOfferTypeEnum",
    "IncentiveStateEnum",
    "IncentiveTypeEnum",
    "IncomeRangeTypeEnum",
    "InsightsKnowledgeGraphEntityCapabilitiesEnum",
    "InsightsTrendEnum",
    "InteractionEventTypeEnum",
    "InteractionTypeEnum",
    "InvoiceTypeEnum",
    "KeywordMatchTypeEnum",
    "KeywordPlanAggregateMetricTypeEnum",
    "KeywordPlanCompetitionLevelEnum",
    "KeywordPlanConceptGroupTypeEnum",
    "KeywordPlanForecastIntervalEnum",
    "KeywordPlanKeywordAnnotationEnum",
    "KeywordPlanNetworkEnum",
    "LabelStatusEnum",
    "LandingPageSourceEnum",
    "LeadFormCallToActionTypeEnum",
    "LeadFormDesiredIntentEnum",
    "LeadFormFieldUserInputTypeEnum",
    "LeadFormPostSubmitCallToActionTypeEnum",
    "LegacyAppInstallAdAppStoreEnum",
    "LiftMeasurementFlightStatusEnum",
    "LiftMetricTypeEnum",
    "LinkedAccountTypeEnum",
    "LinkedProductTypeEnum",
    "ListingGroupFilterCustomAttributeIndexEnum",
    "ListingGroupFilterListingSourceEnum",
    "ListingGroupFilterProductCategoryLevelEnum",
    "ListingGroupFilterProductChannelEnum",
    "ListingGroupFilterProductConditionEnum",
    "ListingGroupFilterProductTypeLevelEnum",
    "ListingGroupFilterTypeEnum",
    "ListingGroupTypeEnum",
    "ListingTypeEnum",
    "LocalServicesBusinessRegistrationCheckRejectionReasonEnum",
    "LocalServicesBusinessRegistrationTypeEnum",
    "LocalServicesCreditStateEnum",
    "LocalServicesEmployeeStatusEnum",
    "LocalServicesEmployeeTypeEnum",
    "LocalServicesInsuranceRejectionReasonEnum",
    "LocalServicesLeadConversationTypeEnum",
    "LocalServicesLeadCreditIssuanceDecisionEnum",
    "LocalServicesLeadStatusEnum",
    "LocalServicesLeadSurveyAnswerEnum",
    "LocalServicesLeadSurveyDissatisfiedReasonEnum",
    "LocalServicesLeadSurveySatisfiedReasonEnum",
    "LocalServicesLeadTypeEnum",
    "LocalServicesLicenseRejectionReasonEnum",
    "LocalServicesParticipantTypeEnum",
    "LocalServicesVerificationArtifactStatusEnum",
    "LocalServicesVerificationArtifactTypeEnum",
    "LocalServicesVerificationStatusEnum",
    "LocationGroupRadiusUnitsEnum",
    "LocationOwnershipTypeEnum",
    "LocationSourceTypeEnum",
    "LocationStringFilterTypeEnum",
    "LookalikeExpansionLevelEnum",
    "LoyaltyMembershipEnum",
    "ManagerLinkStatusEnum",
    "MatchTypeEnum",
    "MediaTypeEnum",
    "MessagingRestrictionTypeEnum",
    "MimeTypeEnum",
    "MinuteOfHourEnum",
    "MobileAppVendorEnum",
    "MobileDevicePlatformEnum",
    "MobileDeviceTypeEnum",
    "MonthOfYearEnum",
    "MultiPartyAuthOperationTypeEnum",
    "MultiPartyAuthReviewStatusEnum",
    "MultiPartyAuthReviewTargetResourceEnum",
    "NegativeGeoTargetTypeEnum",
    "NonSkippableMaxDurationEnum",
    "NonSkippableMinDurationEnum",
    "OfflineConversionDiagnosticStatusEnum",
    "OfflineEventUploadClientEnum",
    "OfflineUserDataJobFailureReasonEnum",
    "OfflineUserDataJobMatchRateRangeEnum",
    "OfflineUserDataJobStatusEnum",
    "OfflineUserDataJobTypeEnum",
    "OperatingSystemVersionOperatorTypeEnum",
    "OptimizationGoalTypeEnum",
    "OptimizeAssetsExperimentSubtypeEnum",
    "ParentalStatusTypeEnum",
    "PartnershipOpportunityEnum",
    "PaymentModeEnum",
    "PerformanceMaxUpgradeStatusEnum",
    "PlacementTypeEnum",
    "PolicyApprovalStatusEnum",
    "PolicyReviewStatusEnum",
    "PolicyTopicEntryTypeEnum",
    "PolicyTopicEvidenceDestinationMismatchUrlTypeEnum",
    "PolicyTopicEvidenceDestinationNotWorkingDeviceEnum",
    "PolicyTopicEvidenceDestinationNotWorkingDnsErrorTypeEnum",
    "PositiveGeoTargetTypeEnum",
    "PreviewTypeEnum",
    "PriceExtensionPriceQualifierEnum",
    "PriceExtensionPriceUnitEnum",
    "PriceExtensionTypeEnum",
    "ProductAvailabilityEnum",
    "ProductCategoryLevelEnum",
    "ProductCategoryStateEnum",
    "ProductChannelEnum",
    "ProductChannelExclusivityEnum",
    "ProductConditionEnum",
    "ProductCustomAttributeIndexEnum",
    "ProductIssueSeverityEnum",
    "ProductLinkInvitationStatusEnum",
    "ProductStatusEnum",
    "ProductTypeLevelEnum",
    "PromotionBarcodeTypeEnum",
    "PromotionExtensionDiscountModifierEnum",
    "PromotionExtensionOccasionEnum",
    "ProximityRadiusUnitsEnum",
    "QualityScoreBucketEnum",
    "ReachPlanAgeRangeEnum",
    "ReachPlanBuyingMethodEnum",
    "ReachPlanConversionRateModelEnum",
    "ReachPlanCostModelEnum",
    "ReachPlanMarketingObjectiveEnum",
    "ReachPlanNetworkEnum",
    "ReachPlanPlannableUserListStatusEnum",
    "ReachPlanSurfaceEnum",
    "RecommendationSubscriptionStatusEnum",
    "RecommendationTypeEnum",
    "RegulatoryFeeTypeEnum",
    "ReservationRequestTypeEnum",
    "ResourceChangeOperationEnum",
    "ResourceLimitTypeEnum",
    "ResponseContentTypeEnum",
    "SearchEngineResultsPageTypeEnum",
    "SearchTermMatchSourceEnum",
    "SearchTermMatchTypeEnum",
    "SearchTermTargetingStatusEnum",
    "SeasonalityEventScopeEnum",
    "SeasonalityEventStatusEnum",
    "SentimentEnum",
    "ServedAssetFieldTypeEnum",
    "SharedSetStatusEnum",
    "SharedSetTypeEnum",
    "ShoppingAddProductsToCampaignRecommendationEnum",
    "SimulationModificationMethodEnum",
    "SimulationTypeEnum",
    "SkAdNetworkAdEventTypeEnum",
    "SkAdNetworkAttributionCreditEnum",
    "SkAdNetworkCoarseConversionValueEnum",
    "SkAdNetworkSourceTypeEnum",
    "SkAdNetworkUserTypeEnum",
    "SlotEnum",
    "SmartCampaignNotEligibleReasonEnum",
    "SmartCampaignStatusEnum",
    "SpendingLimitTypeEnum",
    "SummaryRowSettingEnum",
    "SurveyIntendedActionEnum",
    "SurveyLiftFlightTargetResponseModeEnum",
    "SurveySubjectTypeEnum",
    "SyntheticContentAttestationStatusEnum",
    "SyntheticContentSourceEnum",
    "SystemManagedResourceSourceEnum",
    "TargetCpaOptInRecommendationGoalEnum",
    "TargetFrequencyTimeUnitEnum",
    "TargetImpressionShareLocationEnum",
    "TargetingDimensionEnum",
    "ThirdPartyBrandLiftIntegrationPartnerEnum",
    "ThirdPartyBrandSafetyIntegrationPartnerEnum",
    "ThirdPartyConversionAttributionIntegrationPartnerEnum",
    "ThirdPartyReachIntegrationPartnerEnum",
    "ThirdPartyViewabilityIntegrationPartnerEnum",
    "TimeTypeEnum",
    "TrackingCodePageFormatEnum",
    "TrackingCodeTypeEnum",
    "UnitOfMeasureEnum",
    "UserIdentifierSourceEnum",
    "UserInterestTaxonomyTypeEnum",
    "UserListAccessStatusEnum",
    "UserListClosingReasonEnum",
    "UserListCrmDataSourceTypeEnum",
    "UserListCustomerTypeCategoryEnum",
    "UserListDateRuleItemOperatorEnum",
    "UserListFlexibleRuleOperatorEnum",
    "UserListLogicalRuleOperatorEnum",
    "UserListMembershipStatusEnum",
    "UserListNumberRuleItemOperatorEnum",
    "UserListPrepopulationStatusEnum",
    "UserListRuleTypeEnum",
    "UserListSizeRangeEnum",
    "UserListStringRuleItemOperatorEnum",
    "UserListTypeEnum",
    "ValueRuleDeviceTypeEnum",
    "ValueRuleGeoLocationMatchTypeEnum",
    "ValueRuleOperationEnum",
    "ValueRuleSetAttachmentTypeEnum",
    "ValueRuleSetDimensionEnum",
    "VanityPharmaDisplayUrlModeEnum",
    "VanityPharmaTextEnum",
    "VerticalAdsItemVerticalTypeEnum",
    "VideoAdFormatRestrictionEnum",
    "VideoAdSequenceInteractionTypeEnum",
    "VideoAdSequenceMinimumDurationEnum",
    "VideoEnhancementSourceEnum",
    "VideoExperimentSubtypeEnum",
    "VideoThumbnailEnum",
    "WebpageConditionOperandEnum",
    "WebpageConditionOperatorEnum",
    "YouTubeVideoPrivacyEnum",
    "YouTubeVideoPropertyEnum",
    "YouTubeVideoUploadStateEnum",
)
