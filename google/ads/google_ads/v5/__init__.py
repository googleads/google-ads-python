# Copyright 2020 Google LLC
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


import importlib
import sys

from google.ads.google_ads import util


if sys.version_info < (3, 7):
    raise ImportError('This module requires Python 3.7 or later.')


_lazy_name_to_package_map = dict(
    account_budget_proposal_service_client='google.ads.google_ads.v5.services',
    account_budget_service_client='google.ads.google_ads.v5.services',
    account_link_service_client='google.ads.google_ads.v5.services',
    ad_group_ad_asset_view_service_client='google.ads.google_ads.v5.services',
    ad_group_ad_label_service_client='google.ads.google_ads.v5.services',
    ad_group_ad_service_client='google.ads.google_ads.v5.services',
    ad_group_audience_view_service_client='google.ads.google_ads.v5.services',
    ad_group_bid_modifier_service_client='google.ads.google_ads.v5.services',
    ad_group_criterion_label_service_client='google.ads.google_ads.v5.services',
    ad_group_criterion_service_client='google.ads.google_ads.v5.services',
    ad_group_criterion_simulation_service_client='google.ads.google_ads.v5.services',
    ad_group_extension_setting_service_client='google.ads.google_ads.v5.services',
    ad_group_feed_service_client='google.ads.google_ads.v5.services',
    ad_group_label_service_client='google.ads.google_ads.v5.services',
    ad_group_service_client='google.ads.google_ads.v5.services',
    ad_group_simulation_service_client='google.ads.google_ads.v5.services',
    ad_parameter_service_client='google.ads.google_ads.v5.services',
    ad_schedule_view_service_client='google.ads.google_ads.v5.services',
    ad_service_client='google.ads.google_ads.v5.services',
    age_range_view_service_client='google.ads.google_ads.v5.services',
    asset_service_client='google.ads.google_ads.v5.services',
    batch_job_service_client='google.ads.google_ads.v5.services',
    bidding_strategy_service_client='google.ads.google_ads.v5.services',
    billing_setup_service_client='google.ads.google_ads.v5.services',
    campaign_asset_service_client='google.ads.google_ads.v5.services',
    campaign_audience_view_service_client='google.ads.google_ads.v5.services',
    campaign_bid_modifier_service_client='google.ads.google_ads.v5.services',
    campaign_budget_service_client='google.ads.google_ads.v5.services',
    campaign_criterion_service_client='google.ads.google_ads.v5.services',
    campaign_criterion_simulation_service_client='google.ads.google_ads.v5.services',
    campaign_draft_service_client='google.ads.google_ads.v5.services',
    campaign_experiment_service_client='google.ads.google_ads.v5.services',
    campaign_extension_setting_service_client='google.ads.google_ads.v5.services',
    campaign_feed_service_client='google.ads.google_ads.v5.services',
    campaign_label_service_client='google.ads.google_ads.v5.services',
    campaign_service_client='google.ads.google_ads.v5.services',
    campaign_shared_set_service_client='google.ads.google_ads.v5.services',
    carrier_constant_service_client='google.ads.google_ads.v5.services',
    change_status_service_client='google.ads.google_ads.v5.services',
    click_view_service_client='google.ads.google_ads.v5.services',
    conversion_action_service_client='google.ads.google_ads.v5.services',
    conversion_adjustment_upload_service_client='google.ads.google_ads.v5.services',
    conversion_upload_service_client='google.ads.google_ads.v5.services',
    currency_constant_service_client='google.ads.google_ads.v5.services',
    custom_interest_service_client='google.ads.google_ads.v5.services',
    customer_client_link_service_client='google.ads.google_ads.v5.services',
    customer_client_service_client='google.ads.google_ads.v5.services',
    customer_extension_setting_service_client='google.ads.google_ads.v5.services',
    customer_feed_service_client='google.ads.google_ads.v5.services',
    customer_label_service_client='google.ads.google_ads.v5.services',
    customer_manager_link_service_client='google.ads.google_ads.v5.services',
    customer_negative_criterion_service_client='google.ads.google_ads.v5.services',
    customer_service_client='google.ads.google_ads.v5.services',
    detail_placement_view_service_client='google.ads.google_ads.v5.services',
    display_keyword_view_service_client='google.ads.google_ads.v5.services',
    distance_view_service_client='google.ads.google_ads.v5.services',
    domain_category_service_client='google.ads.google_ads.v5.services',
    dynamic_search_ads_search_term_view_service_client='google.ads.google_ads.v5.services',
    expanded_landing_page_view_service_client='google.ads.google_ads.v5.services',
    extension_feed_item_service_client='google.ads.google_ads.v5.services',
    feed_item_service_client='google.ads.google_ads.v5.services',
    feed_item_target_service_client='google.ads.google_ads.v5.services',
    feed_mapping_service_client='google.ads.google_ads.v5.services',
    feed_placeholder_view_service_client='google.ads.google_ads.v5.services',
    feed_service_client='google.ads.google_ads.v5.services',
    gender_view_service_client='google.ads.google_ads.v5.services',
    geo_target_constant_service_client='google.ads.google_ads.v5.services',
    geographic_view_service_client='google.ads.google_ads.v5.services',
    google_ads_field_service_client='google.ads.google_ads.v5.services',
    google_ads_service_client='google.ads.google_ads.v5.services',
    group_placement_view_service_client='google.ads.google_ads.v5.services',
    hotel_group_view_service_client='google.ads.google_ads.v5.services',
    hotel_performance_view_service_client='google.ads.google_ads.v5.services',
    income_range_view_service_client='google.ads.google_ads.v5.services',
    invoice_service_client='google.ads.google_ads.v5.services',
    keyword_plan_ad_group_keyword_service_client='google.ads.google_ads.v5.services',
    keyword_plan_ad_group_service_client='google.ads.google_ads.v5.services',
    keyword_plan_campaign_keyword_service_client='google.ads.google_ads.v5.services',
    keyword_plan_campaign_service_client='google.ads.google_ads.v5.services',
    keyword_plan_idea_service_client='google.ads.google_ads.v5.services',
    keyword_plan_service_client='google.ads.google_ads.v5.services',
    keyword_view_service_client='google.ads.google_ads.v5.services',
    label_service_client='google.ads.google_ads.v5.services',
    landing_page_view_service_client='google.ads.google_ads.v5.services',
    language_constant_service_client='google.ads.google_ads.v5.services',
    location_view_service_client='google.ads.google_ads.v5.services',
    managed_placement_view_service_client='google.ads.google_ads.v5.services',
    media_file_service_client='google.ads.google_ads.v5.services',
    merchant_center_link_service_client='google.ads.google_ads.v5.services',
    mobile_app_category_constant_service_client='google.ads.google_ads.v5.services',
    mobile_device_constant_service_client='google.ads.google_ads.v5.services',
    offline_user_data_job_service_client='google.ads.google_ads.v5.services',
    operating_system_version_constant_service_client='google.ads.google_ads.v5.services',
    paid_organic_search_term_view_service_client='google.ads.google_ads.v5.services',
    parental_status_view_service_client='google.ads.google_ads.v5.services',
    payments_account_service_client='google.ads.google_ads.v5.services',
    product_bidding_category_constant_service_client='google.ads.google_ads.v5.services',
    product_group_view_service_client='google.ads.google_ads.v5.services',
    reach_plan_service_client='google.ads.google_ads.v5.services',
    recommendation_service_client='google.ads.google_ads.v5.services',
    remarketing_action_service_client='google.ads.google_ads.v5.services',
    search_term_view_service_client='google.ads.google_ads.v5.services',
    shared_criterion_service_client='google.ads.google_ads.v5.services',
    shared_set_service_client='google.ads.google_ads.v5.services',
    shopping_performance_view_service_client='google.ads.google_ads.v5.services',
    third_party_app_analytics_link_service_client='google.ads.google_ads.v5.services',
    topic_constant_service_client='google.ads.google_ads.v5.services',
    topic_view_service_client='google.ads.google_ads.v5.services',
    user_data_service_client='google.ads.google_ads.v5.services',
    user_interest_service_client='google.ads.google_ads.v5.services',
    user_list_service_client='google.ads.google_ads.v5.services',
    user_location_view_service_client='google.ads.google_ads.v5.services',
    video_service_client='google.ads.google_ads.v5.services',
    account_budget_proposal_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    account_budget_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    account_link_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    ad_group_ad_asset_view_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    ad_group_ad_label_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    ad_group_ad_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    ad_group_audience_view_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    ad_group_bid_modifier_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    ad_group_criterion_label_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    ad_group_criterion_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    ad_group_criterion_simulation_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    ad_group_extension_setting_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    ad_group_feed_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    ad_group_label_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    ad_group_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    ad_group_simulation_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    ad_parameter_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    ad_schedule_view_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    ad_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    age_range_view_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    asset_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    batch_job_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    bidding_strategy_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    billing_setup_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    campaign_asset_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    campaign_audience_view_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    campaign_bid_modifier_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    campaign_budget_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    campaign_criterion_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    campaign_criterion_simulation_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    campaign_draft_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    campaign_experiment_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    campaign_extension_setting_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    campaign_feed_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    campaign_label_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    campaign_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    campaign_shared_set_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    carrier_constant_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    change_status_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    click_view_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    conversion_action_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    conversion_adjustment_upload_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    conversion_upload_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    currency_constant_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    custom_interest_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    customer_client_link_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    customer_client_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    customer_extension_setting_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    customer_feed_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    customer_label_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    customer_manager_link_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    customer_negative_criterion_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    customer_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    detail_placement_view_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    display_keyword_view_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    distance_view_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    domain_category_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    dynamic_search_ads_search_term_view_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    expanded_landing_page_view_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    extension_feed_item_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    feed_item_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    feed_item_target_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    feed_mapping_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    feed_placeholder_view_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    feed_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    gender_view_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    geo_target_constant_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    geographic_view_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    google_ads_field_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    google_ads_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    group_placement_view_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    hotel_group_view_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    hotel_performance_view_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    income_range_view_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    invoice_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    keyword_plan_ad_group_keyword_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    keyword_plan_ad_group_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    keyword_plan_campaign_keyword_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    keyword_plan_campaign_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    keyword_plan_idea_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    keyword_plan_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    keyword_view_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    label_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    landing_page_view_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    language_constant_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    location_view_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    managed_placement_view_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    media_file_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    merchant_center_link_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    mobile_app_category_constant_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    mobile_device_constant_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    offline_user_data_job_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    operating_system_version_constant_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    paid_organic_search_term_view_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    parental_status_view_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    payments_account_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    product_bidding_category_constant_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    product_group_view_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    reach_plan_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    recommendation_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    remarketing_action_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    search_term_view_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    shared_criterion_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    shared_set_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    shopping_performance_view_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    third_party_app_analytics_link_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    topic_constant_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    topic_view_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    user_data_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    user_interest_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    user_list_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    user_location_view_service_grpc_transport='google.ads.google_ads.v5.services.transports',
    video_service_grpc_transport='google.ads.google_ads.v5.services.transports',
)


# Background on how this behaves: https://www.python.org/dev/peps/pep-0562/
def __getattr__(name):  # Requires Python >= 3.7
    """Lazily perform imports and class definitions on first demand."""
    if name == '__all__':
        converted = (util.convert_snake_case_to_upper_case(key) for
                     key in _lazy_name_to_package_map)
        all_names = sorted(converted)
        globals()['__all__'] = all_names
        return all_names
    elif name.endswith('Transport'):
        module = __getattr__(util.convert_upper_case_to_snake_case(name))
        sub_mod_class = getattr(module, name)
        klass = type(name, (sub_mod_class,), {'__doc__': sub_mod_class.__doc__})
        globals()[name] = klass
        return klass
    elif name.endswith('ServiceClient'):
        module = __getattr__(util.convert_upper_case_to_snake_case(name))
        enums = __getattr__('enums')
        sub_mod_class = getattr(module, name)
        klass = type(name, (sub_mod_class,),
                     {'__doc__': sub_mod_class.__doc__, 'enums': enums})
        globals()[name] = klass
        return klass
    elif name == 'enums':
        path = 'google.ads.google_ads.v5.services.enums'
        module = importlib.import_module(path)
        globals()[name] = module
        return module
    elif name == 'types':
        path = 'google.ads.google_ads.v5.types'
        module = importlib.import_module(path)
        globals()[name] = module
        return module
    elif name in _lazy_name_to_package_map:
        module = importlib.import_module(f'{_lazy_name_to_package_map[name]}.{name}')
        globals()[name] = module
        return module
    else:
        raise AttributeError(f'unknown sub-module {name!r}.')


def __dir__():
    return globals().get('__all__') or __getattr__('__all__')
