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
import sys

from google.api_core.protobuf_helpers import get_messages

from google.api import http_pb2
from google.ads.google_ads.v0.proto.errors import ad_customizer_error_pb2
from google.ads.google_ads.v0.proto.errors import ad_error_pb2
from google.ads.google_ads.v0.proto.errors import ad_group_ad_error_pb2
from google.ads.google_ads.v0.proto.resources import ad_group_ad_pb2
from google.ads.google_ads.v0.proto.services import ad_group_ad_service_pb2
from google.ads.google_ads.v0.proto.enums import ad_group_ad_status_pb2
from google.ads.google_ads.v0.proto.errors import ad_group_bid_modifier_error_pb2
from google.ads.google_ads.v0.proto.resources import ad_group_bid_modifier_pb2
from google.ads.google_ads.v0.proto.services import ad_group_bid_modifier_service_pb2
from google.ads.google_ads.v0.proto.errors import ad_group_criterion_error_pb2
from google.ads.google_ads.v0.proto.resources import ad_group_criterion_pb2
from google.ads.google_ads.v0.proto.services import ad_group_criterion_service_pb2
from google.ads.google_ads.v0.proto.enums import ad_group_criterion_status_pb2
from google.ads.google_ads.v0.proto.errors import ad_group_error_pb2
from google.ads.google_ads.v0.proto.resources import ad_group_pb2
from google.ads.google_ads.v0.proto.services import ad_group_service_pb2
from google.ads.google_ads.v0.proto.enums import ad_group_status_pb2
from google.ads.google_ads.v0.proto.enums import ad_group_type_pb2
from google.ads.google_ads.v0.proto.enums import ad_network_type_pb2
from google.ads.google_ads.v0.proto.resources import ad_pb2
from google.ads.google_ads.v0.proto.enums import ad_serving_optimization_status_pb2
from google.ads.google_ads.v0.proto.errors import ad_sharing_error_pb2
from google.ads.google_ads.v0.proto.common import ad_type_infos_pb2
from google.ads.google_ads.v0.proto.enums import ad_type_pb2
from google.ads.google_ads.v0.proto.enums import advertising_channel_sub_type_pb2
from google.ads.google_ads.v0.proto.enums import advertising_channel_type_pb2
from google.ads.google_ads.v0.proto.errors import adx_error_pb2
from google.ads.google_ads.v0.proto.errors import authentication_error_pb2
from google.ads.google_ads.v0.proto.errors import authorization_error_pb2
from google.ads.google_ads.v0.proto.errors import bidding_error_pb2
from google.ads.google_ads.v0.proto.common import bidding_pb2
from google.ads.google_ads.v0.proto.enums import bid_modifier_source_pb2
from google.ads.google_ads.v0.proto.enums import bidding_source_pb2
from google.ads.google_ads.v0.proto.errors import bidding_strategy_error_pb2
from google.ads.google_ads.v0.proto.resources import bidding_strategy_pb2
from google.ads.google_ads.v0.proto.services import bidding_strategy_service_pb2
from google.ads.google_ads.v0.proto.enums import bidding_strategy_type_pb2
from google.ads.google_ads.v0.proto.enums import budget_delivery_method_pb2
from google.ads.google_ads.v0.proto.enums import budget_status_pb2
from google.ads.google_ads.v0.proto.resources import campaign_bid_modifier_pb2
from google.ads.google_ads.v0.proto.services import campaign_bid_modifier_service_pb2
from google.ads.google_ads.v0.proto.errors import campaign_budget_error_pb2
from google.ads.google_ads.v0.proto.resources import campaign_budget_pb2
from google.ads.google_ads.v0.proto.services import campaign_budget_service_pb2
from google.ads.google_ads.v0.proto.errors import campaign_criterion_error_pb2
from google.ads.google_ads.v0.proto.resources import campaign_criterion_pb2
from google.ads.google_ads.v0.proto.services import campaign_criterion_service_pb2
from google.ads.google_ads.v0.proto.errors import campaign_error_pb2
from google.ads.google_ads.v0.proto.errors import campaign_group_error_pb2
from google.ads.google_ads.v0.proto.resources import campaign_group_pb2
from google.ads.google_ads.v0.proto.services import campaign_group_service_pb2
from google.ads.google_ads.v0.proto.enums import campaign_group_status_pb2
from google.ads.google_ads.v0.proto.resources import campaign_pb2
from google.ads.google_ads.v0.proto.services import campaign_service_pb2
from google.ads.google_ads.v0.proto.enums import campaign_serving_status_pb2
from google.ads.google_ads.v0.proto.errors import campaign_shared_set_error_pb2
from google.ads.google_ads.v0.proto.resources import campaign_shared_set_pb2
from google.ads.google_ads.v0.proto.services import campaign_shared_set_service_pb2
from google.ads.google_ads.v0.proto.enums import campaign_shared_set_status_pb2
from google.ads.google_ads.v0.proto.enums import campaign_status_pb2
from google.ads.google_ads.v0.proto.errors import collection_size_error_pb2
from google.ads.google_ads.v0.proto.errors import context_error_pb2
from google.ads.google_ads.v0.proto.common import criteria_pb2
from google.ads.google_ads.v0.proto.errors import criterion_error_pb2
from google.ads.google_ads.v0.proto.enums import criterion_type_pb2
from google.ads.google_ads.v0.proto.common import custom_parameter_pb2
from google.ads.google_ads.v0.proto.resources import customer_pb2
from google.ads.google_ads.v0.proto.services import customer_service_pb2
from google.ads.google_ads.v0.proto.errors import database_error_pb2
from google.ads.google_ads.v0.proto.errors import date_error_pb2
from google.ads.google_ads.v0.proto.errors import date_range_error_pb2
from google.ads.google_ads.v0.proto.enums import day_of_week_pb2
from google.ads.google_ads.v0.proto.enums import device_pb2
from google.ads.google_ads.v0.proto.errors import distinct_error_pb2
from google.ads.google_ads.v0.proto.errors import enum_error_pb2
from google.ads.google_ads.v0.proto.errors import errors_pb2
from google.ads.google_ads.v0.proto.errors import feed_attribute_reference_error_pb2
from google.ads.google_ads.v0.proto.errors import field_error_pb2
from google.ads.google_ads.v0.proto.errors import field_mask_error_pb2
from google.ads.google_ads.v0.proto.errors import function_error_pb2
from google.ads.google_ads.v0.proto.errors import function_parsing_error_pb2
from google.ads.google_ads.v0.proto.resources import geo_target_constant_pb2
from google.ads.google_ads.v0.proto.services import geo_target_constant_service_pb2
from google.ads.google_ads.v0.proto.enums import google_ads_field_category_pb2
from google.ads.google_ads.v0.proto.enums import google_ads_field_data_type_pb2
from google.ads.google_ads.v0.proto.resources import google_ads_field_pb2
from google.ads.google_ads.v0.proto.services import google_ads_field_service_pb2
from google.ads.google_ads.v0.proto.services import google_ads_service_pb2
from google.ads.google_ads.v0.proto.errors import header_error_pb2
from google.ads.google_ads.v0.proto.enums import hotel_date_selection_type_pb2
from google.ads.google_ads.v0.proto.errors import id_error_pb2
from google.ads.google_ads.v0.proto.errors import image_error_pb2
from google.ads.google_ads.v0.proto.enums import interaction_type_pb2
from google.ads.google_ads.v0.proto.errors import internal_error_pb2
from google.ads.google_ads.v0.proto.enums import keyword_match_type_pb2
from google.ads.google_ads.v0.proto.resources import keyword_view_pb2
from google.ads.google_ads.v0.proto.services import keyword_view_service_pb2
from google.ads.google_ads.v0.proto.errors import list_operation_error_pb2
from google.ads.google_ads.v0.proto.enums import listing_custom_attribute_index_pb2
from google.ads.google_ads.v0.proto.enums import listing_group_type_pb2
from google.ads.google_ads.v0.proto.errors import media_bundle_error_pb2
from google.ads.google_ads.v0.proto.errors import media_error_pb2
from google.ads.google_ads.v0.proto.common import metrics_pb2
from google.ads.google_ads.v0.proto.enums import minute_of_hour_pb2
from google.ads.google_ads.v0.proto.enums import month_of_year_pb2
from google.ads.google_ads.v0.proto.errors import multiplier_error_pb2
from google.ads.google_ads.v0.proto.errors import mutate_error_pb2
from google.ads.google_ads.v0.proto.errors import new_resource_creation_error_pb2
from google.ads.google_ads.v0.proto.errors import not_empty_error_pb2
from google.ads.google_ads.v0.proto.errors import null_error_pb2
from google.ads.google_ads.v0.proto.errors import operation_access_denied_error_pb2
from google.ads.google_ads.v0.proto.errors import operator_error_pb2
from google.ads.google_ads.v0.proto.enums import page_one_promoted_strategy_goal_pb2
from google.ads.google_ads.v0.proto.errors import policy_finding_error_pb2
from google.ads.google_ads.v0.proto.common import policy_pb2
from google.ads.google_ads.v0.proto.enums import policy_topic_entry_type_pb2
from google.ads.google_ads.v0.proto.enums import policy_topic_evidence_destination_mismatch_url_type_pb2
from google.ads.google_ads.v0.proto.enums import product_condition_pb2
from google.ads.google_ads.v0.proto.enums import product_type_level_pb2
from google.ads.google_ads.v0.proto.enums import quality_score_bucket_pb2
from google.ads.google_ads.v0.proto.errors import query_error_pb2
from google.ads.google_ads.v0.proto.errors import quota_error_pb2
from google.ads.google_ads.v0.proto.errors import range_error_pb2
from google.ads.google_ads.v0.proto.errors import recommendation_error_pb2
from google.ads.google_ads.v0.proto.resources import recommendation_pb2
from google.ads.google_ads.v0.proto.services import recommendation_service_pb2
from google.ads.google_ads.v0.proto.enums import recommendation_type_pb2
from google.ads.google_ads.v0.proto.errors import region_code_error_pb2
from google.ads.google_ads.v0.proto.errors import request_error_pb2
from google.ads.google_ads.v0.proto.errors import resource_access_denied_error_pb2
from google.ads.google_ads.v0.proto.errors import resource_count_limit_exceeded_error_pb2
from google.ads.google_ads.v0.proto.errors import setting_error_pb2
from google.ads.google_ads.v0.proto.errors import shared_criterion_error_pb2
from google.ads.google_ads.v0.proto.resources import shared_criterion_pb2
from google.ads.google_ads.v0.proto.services import shared_criterion_service_pb2
from google.ads.google_ads.v0.proto.errors import shared_set_error_pb2
from google.ads.google_ads.v0.proto.resources import shared_set_pb2
from google.ads.google_ads.v0.proto.services import shared_set_service_pb2
from google.ads.google_ads.v0.proto.enums import shared_set_status_pb2
from google.ads.google_ads.v0.proto.enums import shared_set_type_pb2
from google.ads.google_ads.v0.proto.enums import slot_pb2
from google.ads.google_ads.v0.proto.errors import string_format_error_pb2
from google.ads.google_ads.v0.proto.errors import string_length_error_pb2
from google.ads.google_ads.v0.proto.enums import target_cpa_opt_in_recommendation_goal_pb2
from google.ads.google_ads.v0.proto.errors import url_field_error_pb2
from google.ads.google_ads.v0.proto.common import value_pb2
from google.protobuf import any_pb2
from google.protobuf import descriptor_pb2
from google.protobuf import field_mask_pb2
from google.protobuf import wrappers_pb2
from google.rpc import status_pb2

_shared_modules = [
    http_pb2,
    ad_customizer_error_pb2,
    ad_error_pb2,
    ad_group_ad_error_pb2,
    ad_group_ad_pb2,
    ad_group_ad_status_pb2,
    ad_group_bid_modifier_error_pb2,
    ad_group_bid_modifier_pb2,
    ad_group_criterion_error_pb2,
    ad_group_criterion_pb2,
    ad_group_criterion_status_pb2,
    ad_group_error_pb2,
    ad_group_pb2,
    ad_group_status_pb2,
    ad_group_type_pb2,
    ad_network_type_pb2,
    ad_pb2,
    ad_serving_optimization_status_pb2,
    ad_sharing_error_pb2,
    ad_type_infos_pb2,
    ad_type_pb2,
    advertising_channel_sub_type_pb2,
    advertising_channel_type_pb2,
    adx_error_pb2,
    authentication_error_pb2,
    authorization_error_pb2,
    bid_modifier_source_pb2,
    bidding_error_pb2,
    bidding_pb2,
    bidding_source_pb2,
    bidding_strategy_error_pb2,
    bidding_strategy_pb2,
    bidding_strategy_type_pb2,
    budget_delivery_method_pb2,
    budget_status_pb2,
    campaign_bid_modifier_pb2,
    campaign_budget_error_pb2,
    campaign_budget_pb2,
    campaign_criterion_error_pb2,
    campaign_criterion_pb2,
    campaign_error_pb2,
    campaign_group_error_pb2,
    campaign_group_pb2,
    campaign_group_status_pb2,
    campaign_pb2,
    campaign_serving_status_pb2,
    campaign_shared_set_error_pb2,
    campaign_shared_set_pb2,
    campaign_shared_set_status_pb2,
    campaign_status_pb2,
    collection_size_error_pb2,
    context_error_pb2,
    criteria_pb2,
    criterion_error_pb2,
    criterion_type_pb2,
    custom_parameter_pb2,
    customer_pb2,
    database_error_pb2,
    date_error_pb2,
    date_range_error_pb2,
    day_of_week_pb2,
    device_pb2,
    distinct_error_pb2,
    enum_error_pb2,
    errors_pb2,
    feed_attribute_reference_error_pb2,
    field_error_pb2,
    field_mask_error_pb2,
    function_error_pb2,
    function_parsing_error_pb2,
    geo_target_constant_pb2,
    google_ads_field_category_pb2,
    google_ads_field_data_type_pb2,
    google_ads_field_pb2,
    header_error_pb2,
    hotel_date_selection_type_pb2,
    id_error_pb2,
    image_error_pb2,
    interaction_type_pb2,
    internal_error_pb2,
    keyword_match_type_pb2,
    keyword_view_pb2,
    list_operation_error_pb2,
    listing_custom_attribute_index_pb2,
    listing_group_type_pb2,
    media_bundle_error_pb2,
    media_error_pb2,
    metrics_pb2,
    minute_of_hour_pb2,
    month_of_year_pb2,
    multiplier_error_pb2,
    mutate_error_pb2,
    new_resource_creation_error_pb2,
    not_empty_error_pb2,
    null_error_pb2,
    operation_access_denied_error_pb2,
    operator_error_pb2,
    page_one_promoted_strategy_goal_pb2,
    policy_finding_error_pb2,
    policy_pb2,
    policy_topic_entry_type_pb2,
    policy_topic_evidence_destination_mismatch_url_type_pb2,
    product_condition_pb2,
    product_type_level_pb2,
    quality_score_bucket_pb2,
    query_error_pb2,
    quota_error_pb2,
    range_error_pb2,
    recommendation_error_pb2,
    recommendation_pb2,
    recommendation_type_pb2,
    region_code_error_pb2,
    request_error_pb2,
    resource_access_denied_error_pb2,
    resource_count_limit_exceeded_error_pb2,
    setting_error_pb2,
    shared_criterion_error_pb2,
    shared_criterion_pb2,
    shared_set_error_pb2,
    shared_set_pb2,
    shared_set_status_pb2,
    shared_set_type_pb2,
    slot_pb2,
    string_format_error_pb2,
    string_length_error_pb2,
    target_cpa_opt_in_recommendation_goal_pb2,
    url_field_error_pb2,
    value_pb2,
    any_pb2,
    descriptor_pb2,
    field_mask_pb2,
    wrappers_pb2,
    status_pb2,
]

_local_modules = [
    ad_group_ad_service_pb2,
    ad_group_bid_modifier_service_pb2,
    ad_group_criterion_service_pb2,
    ad_group_service_pb2,
    bidding_strategy_service_pb2,
    campaign_bid_modifier_service_pb2,
    campaign_budget_service_pb2,
    campaign_criterion_service_pb2,
    campaign_group_service_pb2,
    campaign_service_pb2,
    campaign_shared_set_service_pb2,
    customer_service_pb2,
    geo_target_constant_service_pb2,
    google_ads_field_service_pb2,
    google_ads_service_pb2,
    keyword_view_service_pb2,
    recommendation_service_pb2,
    shared_criterion_service_pb2,
    shared_set_service_pb2,
]

names = []

for module in _shared_modules:
    for name, message in get_messages(module).items():
        setattr(sys.modules[__name__], name, message)
        names.append(name)
for module in _local_modules:
    for name, message in get_messages(module).items():
        message.__module__ = 'google.cloud.ads.googleads_v0.types'
        setattr(sys.modules[__name__], name, message)
        names.append(name)

__all__ = tuple(sorted(names))
