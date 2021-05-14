# -*- coding: utf-8 -*-
# Copyright 2020 Google LLC
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
import proto  # type: ignore

from google.ads.googleads.v7.common.types import metrics as gagc_metrics
from google.ads.googleads.v7.common.types import segments as gagc_segments
from google.ads.googleads.v7.enums.types import (
    response_content_type as gage_response_content_type,
)
from google.ads.googleads.v7.enums.types import (
    summary_row_setting as gage_summary_row_setting,
)
from google.ads.googleads.v7.resources.types import (
    account_budget as gagr_account_budget,
)
from google.ads.googleads.v7.resources.types import (
    account_budget_proposal as gagr_account_budget_proposal,
)
from google.ads.googleads.v7.resources.types import (
    account_link as gagr_account_link,
)
from google.ads.googleads.v7.resources.types import ad_group as gagr_ad_group
from google.ads.googleads.v7.resources.types import (
    ad_group_ad as gagr_ad_group_ad,
)
from google.ads.googleads.v7.resources.types import (
    ad_group_ad_asset_view as gagr_ad_group_ad_asset_view,
)
from google.ads.googleads.v7.resources.types import (
    ad_group_ad_label as gagr_ad_group_ad_label,
)
from google.ads.googleads.v7.resources.types import (
    ad_group_asset as gagr_ad_group_asset,
)
from google.ads.googleads.v7.resources.types import (
    ad_group_audience_view as gagr_ad_group_audience_view,
)
from google.ads.googleads.v7.resources.types import (
    ad_group_bid_modifier as gagr_ad_group_bid_modifier,
)
from google.ads.googleads.v7.resources.types import (
    ad_group_criterion as gagr_ad_group_criterion,
)
from google.ads.googleads.v7.resources.types import (
    ad_group_criterion_label as gagr_ad_group_criterion_label,
)
from google.ads.googleads.v7.resources.types import (
    ad_group_criterion_simulation as gagr_ad_group_criterion_simulation,
)
from google.ads.googleads.v7.resources.types import (
    ad_group_extension_setting as gagr_ad_group_extension_setting,
)
from google.ads.googleads.v7.resources.types import (
    ad_group_feed as gagr_ad_group_feed,
)
from google.ads.googleads.v7.resources.types import (
    ad_group_label as gagr_ad_group_label,
)
from google.ads.googleads.v7.resources.types import (
    ad_group_simulation as gagr_ad_group_simulation,
)
from google.ads.googleads.v7.resources.types import (
    ad_parameter as gagr_ad_parameter,
)
from google.ads.googleads.v7.resources.types import (
    ad_schedule_view as gagr_ad_schedule_view,
)
from google.ads.googleads.v7.resources.types import (
    age_range_view as gagr_age_range_view,
)
from google.ads.googleads.v7.resources.types import asset as gagr_asset
from google.ads.googleads.v7.resources.types import batch_job as gagr_batch_job
from google.ads.googleads.v7.resources.types import (
    bidding_strategy as gagr_bidding_strategy,
)
from google.ads.googleads.v7.resources.types import (
    bidding_strategy_simulation as gagr_bidding_strategy_simulation,
)
from google.ads.googleads.v7.resources.types import (
    billing_setup as gagr_billing_setup,
)
from google.ads.googleads.v7.resources.types import call_view as gagr_call_view
from google.ads.googleads.v7.resources.types import campaign as gagr_campaign
from google.ads.googleads.v7.resources.types import (
    campaign_asset as gagr_campaign_asset,
)
from google.ads.googleads.v7.resources.types import (
    campaign_audience_view as gagr_campaign_audience_view,
)
from google.ads.googleads.v7.resources.types import (
    campaign_bid_modifier as gagr_campaign_bid_modifier,
)
from google.ads.googleads.v7.resources.types import (
    campaign_budget as gagr_campaign_budget,
)
from google.ads.googleads.v7.resources.types import (
    campaign_criterion as gagr_campaign_criterion,
)
from google.ads.googleads.v7.resources.types import (
    campaign_criterion_simulation as gagr_campaign_criterion_simulation,
)
from google.ads.googleads.v7.resources.types import (
    campaign_draft as gagr_campaign_draft,
)
from google.ads.googleads.v7.resources.types import (
    campaign_experiment as gagr_campaign_experiment,
)
from google.ads.googleads.v7.resources.types import (
    campaign_extension_setting as gagr_campaign_extension_setting,
)
from google.ads.googleads.v7.resources.types import (
    campaign_feed as gagr_campaign_feed,
)
from google.ads.googleads.v7.resources.types import (
    campaign_label as gagr_campaign_label,
)
from google.ads.googleads.v7.resources.types import (
    campaign_shared_set as gagr_campaign_shared_set,
)
from google.ads.googleads.v7.resources.types import (
    campaign_simulation as gagr_campaign_simulation,
)
from google.ads.googleads.v7.resources.types import (
    carrier_constant as gagr_carrier_constant,
)
from google.ads.googleads.v7.resources.types import (
    change_event as gagr_change_event,
)
from google.ads.googleads.v7.resources.types import (
    change_status as gagr_change_status,
)
from google.ads.googleads.v7.resources.types import (
    click_view as gagr_click_view,
)
from google.ads.googleads.v7.resources.types import (
    combined_audience as gagr_combined_audience,
)
from google.ads.googleads.v7.resources.types import (
    conversion_action as gagr_conversion_action,
)
from google.ads.googleads.v7.resources.types import (
    conversion_custom_variable as gagr_conversion_custom_variable,
)
from google.ads.googleads.v7.resources.types import (
    currency_constant as gagr_currency_constant,
)
from google.ads.googleads.v7.resources.types import (
    custom_audience as gagr_custom_audience,
)
from google.ads.googleads.v7.resources.types import (
    custom_interest as gagr_custom_interest,
)
from google.ads.googleads.v7.resources.types import customer as gagr_customer
from google.ads.googleads.v7.resources.types import (
    customer_asset as gagr_customer_asset,
)
from google.ads.googleads.v7.resources.types import (
    customer_client as gagr_customer_client,
)
from google.ads.googleads.v7.resources.types import (
    customer_client_link as gagr_customer_client_link,
)
from google.ads.googleads.v7.resources.types import (
    customer_extension_setting as gagr_customer_extension_setting,
)
from google.ads.googleads.v7.resources.types import (
    customer_feed as gagr_customer_feed,
)
from google.ads.googleads.v7.resources.types import (
    customer_label as gagr_customer_label,
)
from google.ads.googleads.v7.resources.types import (
    customer_manager_link as gagr_customer_manager_link,
)
from google.ads.googleads.v7.resources.types import (
    customer_negative_criterion as gagr_customer_negative_criterion,
)
from google.ads.googleads.v7.resources.types import (
    customer_user_access as gagr_customer_user_access,
)
from google.ads.googleads.v7.resources.types import (
    customer_user_access_invitation as gagr_customer_user_access_invitation,
)
from google.ads.googleads.v7.resources.types import (
    detail_placement_view as gagr_detail_placement_view,
)
from google.ads.googleads.v7.resources.types import (
    display_keyword_view as gagr_display_keyword_view,
)
from google.ads.googleads.v7.resources.types import (
    distance_view as gagr_distance_view,
)
from google.ads.googleads.v7.resources.types import (
    domain_category as gagr_domain_category,
)
from google.ads.googleads.v7.resources.types import (
    dynamic_search_ads_search_term_view as gagr_dynamic_search_ads_search_term_view,
)
from google.ads.googleads.v7.resources.types import (
    expanded_landing_page_view as gagr_expanded_landing_page_view,
)
from google.ads.googleads.v7.resources.types import (
    extension_feed_item as gagr_extension_feed_item,
)
from google.ads.googleads.v7.resources.types import feed as gagr_feed
from google.ads.googleads.v7.resources.types import feed_item as gagr_feed_item
from google.ads.googleads.v7.resources.types import (
    feed_item_set as gagr_feed_item_set,
)
from google.ads.googleads.v7.resources.types import (
    feed_item_set_link as gagr_feed_item_set_link,
)
from google.ads.googleads.v7.resources.types import (
    feed_item_target as gagr_feed_item_target,
)
from google.ads.googleads.v7.resources.types import (
    feed_mapping as gagr_feed_mapping,
)
from google.ads.googleads.v7.resources.types import (
    feed_placeholder_view as gagr_feed_placeholder_view,
)
from google.ads.googleads.v7.resources.types import (
    gender_view as gagr_gender_view,
)
from google.ads.googleads.v7.resources.types import (
    geo_target_constant as gagr_geo_target_constant,
)
from google.ads.googleads.v7.resources.types import (
    geographic_view as gagr_geographic_view,
)
from google.ads.googleads.v7.resources.types import (
    group_placement_view as gagr_group_placement_view,
)
from google.ads.googleads.v7.resources.types import (
    hotel_group_view as gagr_hotel_group_view,
)
from google.ads.googleads.v7.resources.types import (
    hotel_performance_view as gagr_hotel_performance_view,
)
from google.ads.googleads.v7.resources.types import (
    income_range_view as gagr_income_range_view,
)
from google.ads.googleads.v7.resources.types import (
    keyword_plan as gagr_keyword_plan,
)
from google.ads.googleads.v7.resources.types import (
    keyword_plan_ad_group as gagr_keyword_plan_ad_group,
)
from google.ads.googleads.v7.resources.types import (
    keyword_plan_ad_group_keyword as gagr_keyword_plan_ad_group_keyword,
)
from google.ads.googleads.v7.resources.types import (
    keyword_plan_campaign as gagr_keyword_plan_campaign,
)
from google.ads.googleads.v7.resources.types import (
    keyword_plan_campaign_keyword as gagr_keyword_plan_campaign_keyword,
)
from google.ads.googleads.v7.resources.types import (
    keyword_view as gagr_keyword_view,
)
from google.ads.googleads.v7.resources.types import label as gagr_label
from google.ads.googleads.v7.resources.types import (
    landing_page_view as gagr_landing_page_view,
)
from google.ads.googleads.v7.resources.types import (
    language_constant as gagr_language_constant,
)
from google.ads.googleads.v7.resources.types import (
    life_event as gagr_life_event,
)
from google.ads.googleads.v7.resources.types import (
    location_view as gagr_location_view,
)
from google.ads.googleads.v7.resources.types import (
    managed_placement_view as gagr_managed_placement_view,
)
from google.ads.googleads.v7.resources.types import (
    media_file as gagr_media_file,
)
from google.ads.googleads.v7.resources.types import (
    mobile_app_category_constant as gagr_mobile_app_category_constant,
)
from google.ads.googleads.v7.resources.types import (
    mobile_device_constant as gagr_mobile_device_constant,
)
from google.ads.googleads.v7.resources.types import (
    offline_user_data_job as gagr_offline_user_data_job,
)
from google.ads.googleads.v7.resources.types import (
    operating_system_version_constant as gagr_operating_system_version_constant,
)
from google.ads.googleads.v7.resources.types import (
    paid_organic_search_term_view as gagr_paid_organic_search_term_view,
)
from google.ads.googleads.v7.resources.types import (
    parental_status_view as gagr_parental_status_view,
)
from google.ads.googleads.v7.resources.types import (
    product_bidding_category_constant as gagr_product_bidding_category_constant,
)
from google.ads.googleads.v7.resources.types import (
    product_group_view as gagr_product_group_view,
)
from google.ads.googleads.v7.resources.types import (
    recommendation as gagr_recommendation,
)
from google.ads.googleads.v7.resources.types import (
    remarketing_action as gagr_remarketing_action,
)
from google.ads.googleads.v7.resources.types import (
    search_term_view as gagr_search_term_view,
)
from google.ads.googleads.v7.resources.types import (
    shared_criterion as gagr_shared_criterion,
)
from google.ads.googleads.v7.resources.types import (
    shared_set as gagr_shared_set,
)
from google.ads.googleads.v7.resources.types import (
    shopping_performance_view as gagr_shopping_performance_view,
)
from google.ads.googleads.v7.resources.types import (
    third_party_app_analytics_link as gagr_third_party_app_analytics_link,
)
from google.ads.googleads.v7.resources.types import (
    topic_constant as gagr_topic_constant,
)
from google.ads.googleads.v7.resources.types import (
    topic_view as gagr_topic_view,
)
from google.ads.googleads.v7.resources.types import (
    user_interest as gagr_user_interest,
)
from google.ads.googleads.v7.resources.types import user_list as gagr_user_list
from google.ads.googleads.v7.resources.types import (
    user_location_view as gagr_user_location_view,
)
from google.ads.googleads.v7.resources.types import video as gagr_video
from google.ads.googleads.v7.resources.types import (
    webpage_view as gagr_webpage_view,
)
from google.ads.googleads.v7.services.types import ad_group_ad_label_service
from google.ads.googleads.v7.services.types import ad_group_ad_service
from google.ads.googleads.v7.services.types import ad_group_asset_service
from google.ads.googleads.v7.services.types import ad_group_bid_modifier_service
from google.ads.googleads.v7.services.types import (
    ad_group_criterion_label_service,
)
from google.ads.googleads.v7.services.types import ad_group_criterion_service
from google.ads.googleads.v7.services.types import (
    ad_group_extension_setting_service,
)
from google.ads.googleads.v7.services.types import ad_group_feed_service
from google.ads.googleads.v7.services.types import ad_group_label_service
from google.ads.googleads.v7.services.types import ad_group_service
from google.ads.googleads.v7.services.types import ad_parameter_service
from google.ads.googleads.v7.services.types import ad_service
from google.ads.googleads.v7.services.types import asset_service
from google.ads.googleads.v7.services.types import bidding_strategy_service
from google.ads.googleads.v7.services.types import campaign_asset_service
from google.ads.googleads.v7.services.types import campaign_bid_modifier_service
from google.ads.googleads.v7.services.types import campaign_budget_service
from google.ads.googleads.v7.services.types import campaign_criterion_service
from google.ads.googleads.v7.services.types import campaign_draft_service
from google.ads.googleads.v7.services.types import campaign_experiment_service
from google.ads.googleads.v7.services.types import (
    campaign_extension_setting_service,
)
from google.ads.googleads.v7.services.types import campaign_feed_service
from google.ads.googleads.v7.services.types import campaign_label_service
from google.ads.googleads.v7.services.types import campaign_service
from google.ads.googleads.v7.services.types import campaign_shared_set_service
from google.ads.googleads.v7.services.types import conversion_action_service
from google.ads.googleads.v7.services.types import (
    conversion_custom_variable_service,
)
from google.ads.googleads.v7.services.types import customer_asset_service
from google.ads.googleads.v7.services.types import (
    customer_extension_setting_service,
)
from google.ads.googleads.v7.services.types import customer_feed_service
from google.ads.googleads.v7.services.types import customer_label_service
from google.ads.googleads.v7.services.types import (
    customer_negative_criterion_service,
)
from google.ads.googleads.v7.services.types import customer_service
from google.ads.googleads.v7.services.types import extension_feed_item_service
from google.ads.googleads.v7.services.types import feed_item_service
from google.ads.googleads.v7.services.types import feed_item_set_link_service
from google.ads.googleads.v7.services.types import feed_item_set_service
from google.ads.googleads.v7.services.types import feed_item_target_service
from google.ads.googleads.v7.services.types import feed_mapping_service
from google.ads.googleads.v7.services.types import feed_service
from google.ads.googleads.v7.services.types import (
    keyword_plan_ad_group_keyword_service,
)
from google.ads.googleads.v7.services.types import keyword_plan_ad_group_service
from google.ads.googleads.v7.services.types import (
    keyword_plan_campaign_keyword_service,
)
from google.ads.googleads.v7.services.types import keyword_plan_campaign_service
from google.ads.googleads.v7.services.types import keyword_plan_service
from google.ads.googleads.v7.services.types import label_service
from google.ads.googleads.v7.services.types import media_file_service
from google.ads.googleads.v7.services.types import remarketing_action_service
from google.ads.googleads.v7.services.types import shared_criterion_service
from google.ads.googleads.v7.services.types import shared_set_service
from google.ads.googleads.v7.services.types import user_list_service
from google.protobuf import field_mask_pb2 as gp_field_mask  # type: ignore
from google.rpc import status_pb2 as status  # type: ignore


__protobuf__ = proto.module(
    package="google.ads.googleads.v7.services",
    marshal="google.ads.googleads.v7",
    manifest={
        "SearchGoogleAdsRequest",
        "SearchGoogleAdsResponse",
        "SearchGoogleAdsStreamRequest",
        "SearchGoogleAdsStreamResponse",
        "GoogleAdsRow",
        "MutateGoogleAdsRequest",
        "MutateGoogleAdsResponse",
        "MutateOperation",
        "MutateOperationResponse",
    },
)


class SearchGoogleAdsRequest(proto.Message):
    r"""Request message for
    [GoogleAdsService.Search][google.ads.googleads.v7.services.GoogleAdsService.Search].

    Attributes:
        customer_id (str):
            Required. The ID of the customer being
            queried.
        query (str):
            Required. The query string.
        page_token (str):
            Token of the page to retrieve. If not specified, the first
            page of results will be returned. Use the value obtained
            from ``next_page_token`` in the previous response in order
            to request the next page of results.
        page_size (int):
            Number of elements to retrieve in a single
            page. When too large a page is requested, the
            server may decide to further limit the number of
            returned resources.
        validate_only (bool):
            If true, the request is validated but not
            executed.
        return_total_results_count (bool):
            If true, the total number of results that
            match the query ignoring the LIMIT clause will
            be included in the response. Default is false.
        summary_row_setting (google.ads.googleads.v7.enums.types.SummaryRowSettingEnum.SummaryRowSetting):
            Determines whether a summary row will be
            returned. By default, summary row is not
            returned. If requested, the summary row will be
            sent in a response by itself after all other
            query results are returned.
    """

    customer_id = proto.Field(proto.STRING, number=1,)
    query = proto.Field(proto.STRING, number=2,)
    page_token = proto.Field(proto.STRING, number=3,)
    page_size = proto.Field(proto.INT32, number=4,)
    validate_only = proto.Field(proto.BOOL, number=5,)
    return_total_results_count = proto.Field(proto.BOOL, number=7,)
    summary_row_setting = proto.Field(
        proto.ENUM,
        number=8,
        enum=gage_summary_row_setting.SummaryRowSettingEnum.SummaryRowSetting,
    )


class SearchGoogleAdsResponse(proto.Message):
    r"""Response message for
    [GoogleAdsService.Search][google.ads.googleads.v7.services.GoogleAdsService.Search].

    Attributes:
        results (Sequence[google.ads.googleads.v7.services.types.GoogleAdsRow]):
            The list of rows that matched the query.
        next_page_token (str):
            Pagination token used to retrieve the next page of results.
            Pass the content of this string as the ``page_token``
            attribute of the next request. ``next_page_token`` is not
            returned for the last page.
        total_results_count (int):
            Total number of results that match the query
            ignoring the LIMIT clause.
        field_mask (google.protobuf.field_mask_pb2.FieldMask):
            FieldMask that represents what fields were
            requested by the user.
        summary_row (google.ads.googleads.v7.services.types.GoogleAdsRow):
            Summary row that contains summary of metrics
            in results. Summary of metrics means aggregation
            of metrics across all results, here aggregation
            could be sum, average, rate, etc.
    """

    @property
    def raw_page(self):
        return self

    results = proto.RepeatedField(
        proto.MESSAGE, number=1, message="GoogleAdsRow",
    )
    next_page_token = proto.Field(proto.STRING, number=2,)
    total_results_count = proto.Field(proto.INT64, number=3,)
    field_mask = proto.Field(
        proto.MESSAGE, number=5, message=gp_field_mask.FieldMask,
    )
    summary_row = proto.Field(proto.MESSAGE, number=6, message="GoogleAdsRow",)


class SearchGoogleAdsStreamRequest(proto.Message):
    r"""Request message for
    [GoogleAdsService.SearchStream][google.ads.googleads.v7.services.GoogleAdsService.SearchStream].

    Attributes:
        customer_id (str):
            Required. The ID of the customer being
            queried.
        query (str):
            Required. The query string.
        summary_row_setting (google.ads.googleads.v7.enums.types.SummaryRowSettingEnum.SummaryRowSetting):
            Determines whether a summary row will be
            returned. By default, summary row is not
            returned. If requested, the summary row will be
            sent in a response by itself after all other
            query results are returned.
    """

    customer_id = proto.Field(proto.STRING, number=1,)
    query = proto.Field(proto.STRING, number=2,)
    summary_row_setting = proto.Field(
        proto.ENUM,
        number=3,
        enum=gage_summary_row_setting.SummaryRowSettingEnum.SummaryRowSetting,
    )


class SearchGoogleAdsStreamResponse(proto.Message):
    r"""Response message for
    [GoogleAdsService.SearchStream][google.ads.googleads.v7.services.GoogleAdsService.SearchStream].

    Attributes:
        results (Sequence[google.ads.googleads.v7.services.types.GoogleAdsRow]):
            The list of rows that matched the query.
        field_mask (google.protobuf.field_mask_pb2.FieldMask):
            FieldMask that represents what fields were
            requested by the user.
        summary_row (google.ads.googleads.v7.services.types.GoogleAdsRow):
            Summary row that contains summary of metrics
            in results. Summary of metrics means aggregation
            of metrics across all results, here aggregation
            could be sum, average, rate, etc.
        request_id (str):
            The unique id of the request that is used for
            debugging purposes.
    """

    results = proto.RepeatedField(
        proto.MESSAGE, number=1, message="GoogleAdsRow",
    )
    field_mask = proto.Field(
        proto.MESSAGE, number=2, message=gp_field_mask.FieldMask,
    )
    summary_row = proto.Field(proto.MESSAGE, number=3, message="GoogleAdsRow",)
    request_id = proto.Field(proto.STRING, number=4,)


class GoogleAdsRow(proto.Message):
    r"""A returned row from the query.
    Attributes:
        account_budget (google.ads.googleads.v7.resources.types.AccountBudget):
            The account budget in the query.
        account_budget_proposal (google.ads.googleads.v7.resources.types.AccountBudgetProposal):
            The account budget proposal referenced in the
            query.
        account_link (google.ads.googleads.v7.resources.types.AccountLink):
            The AccountLink referenced in the query.
        ad_group (google.ads.googleads.v7.resources.types.AdGroup):
            The ad group referenced in the query.
        ad_group_ad (google.ads.googleads.v7.resources.types.AdGroupAd):
            The ad referenced in the query.
        ad_group_ad_asset_view (google.ads.googleads.v7.resources.types.AdGroupAdAssetView):
            The ad group ad asset view in the query.
        ad_group_ad_label (google.ads.googleads.v7.resources.types.AdGroupAdLabel):
            The ad group ad label referenced in the
            query.
        ad_group_asset (google.ads.googleads.v7.resources.types.AdGroupAsset):
            The ad group asset referenced in the query.
        ad_group_audience_view (google.ads.googleads.v7.resources.types.AdGroupAudienceView):
            The ad group audience view referenced in the
            query.
        ad_group_bid_modifier (google.ads.googleads.v7.resources.types.AdGroupBidModifier):
            The bid modifier referenced in the query.
        ad_group_criterion (google.ads.googleads.v7.resources.types.AdGroupCriterion):
            The criterion referenced in the query.
        ad_group_criterion_label (google.ads.googleads.v7.resources.types.AdGroupCriterionLabel):
            The ad group criterion label referenced in
            the query.
        ad_group_criterion_simulation (google.ads.googleads.v7.resources.types.AdGroupCriterionSimulation):
            The ad group criterion simulation referenced
            in the query.
        ad_group_extension_setting (google.ads.googleads.v7.resources.types.AdGroupExtensionSetting):
            The ad group extension setting referenced in
            the query.
        ad_group_feed (google.ads.googleads.v7.resources.types.AdGroupFeed):
            The ad group feed referenced in the query.
        ad_group_label (google.ads.googleads.v7.resources.types.AdGroupLabel):
            The ad group label referenced in the query.
        ad_group_simulation (google.ads.googleads.v7.resources.types.AdGroupSimulation):
            The ad group simulation referenced in the
            query.
        ad_parameter (google.ads.googleads.v7.resources.types.AdParameter):
            The ad parameter referenced in the query.
        age_range_view (google.ads.googleads.v7.resources.types.AgeRangeView):
            The age range view referenced in the query.
        ad_schedule_view (google.ads.googleads.v7.resources.types.AdScheduleView):
            The ad schedule view referenced in the query.
        domain_category (google.ads.googleads.v7.resources.types.DomainCategory):
            The domain category referenced in the query.
        asset (google.ads.googleads.v7.resources.types.Asset):
            The asset referenced in the query.
        batch_job (google.ads.googleads.v7.resources.types.BatchJob):
            The batch job referenced in the query.
        bidding_strategy (google.ads.googleads.v7.resources.types.BiddingStrategy):
            The bidding strategy referenced in the query.
        bidding_strategy_simulation (google.ads.googleads.v7.resources.types.BiddingStrategySimulation):
            The bidding strategy simulation referenced in
            the query.
        billing_setup (google.ads.googleads.v7.resources.types.BillingSetup):
            The billing setup referenced in the query.
        call_view (google.ads.googleads.v7.resources.types.CallView):
            The call view referenced in the query.
        campaign_budget (google.ads.googleads.v7.resources.types.CampaignBudget):
            The campaign budget referenced in the query.
        campaign (google.ads.googleads.v7.resources.types.Campaign):
            The campaign referenced in the query.
        campaign_asset (google.ads.googleads.v7.resources.types.CampaignAsset):
            The campaign asset referenced in the query.
        campaign_audience_view (google.ads.googleads.v7.resources.types.CampaignAudienceView):
            The campaign audience view referenced in the
            query.
        campaign_bid_modifier (google.ads.googleads.v7.resources.types.CampaignBidModifier):
            The campaign bid modifier referenced in the
            query.
        campaign_criterion (google.ads.googleads.v7.resources.types.CampaignCriterion):
            The campaign criterion referenced in the
            query.
        campaign_criterion_simulation (google.ads.googleads.v7.resources.types.CampaignCriterionSimulation):
            The campaign criterion simulation referenced
            in the query.
        campaign_draft (google.ads.googleads.v7.resources.types.CampaignDraft):
            The campaign draft referenced in the query.
        campaign_experiment (google.ads.googleads.v7.resources.types.CampaignExperiment):
            The campaign experiment referenced in the
            query.
        campaign_extension_setting (google.ads.googleads.v7.resources.types.CampaignExtensionSetting):
            The campaign extension setting referenced in
            the query.
        campaign_feed (google.ads.googleads.v7.resources.types.CampaignFeed):
            The campaign feed referenced in the query.
        campaign_label (google.ads.googleads.v7.resources.types.CampaignLabel):
            The campaign label referenced in the query.
        campaign_shared_set (google.ads.googleads.v7.resources.types.CampaignSharedSet):
            Campaign Shared Set referenced in AWQL query.
        campaign_simulation (google.ads.googleads.v7.resources.types.CampaignSimulation):
            The campaign simulation referenced in the
            query.
        carrier_constant (google.ads.googleads.v7.resources.types.CarrierConstant):
            The carrier constant referenced in the query.
        change_event (google.ads.googleads.v7.resources.types.ChangeEvent):
            The ChangeEvent referenced in the query.
        change_status (google.ads.googleads.v7.resources.types.ChangeStatus):
            The ChangeStatus referenced in the query.
        combined_audience (google.ads.googleads.v7.resources.types.CombinedAudience):
            The CombinedAudience referenced in the query.
        conversion_action (google.ads.googleads.v7.resources.types.ConversionAction):
            The conversion action referenced in the
            query.
        conversion_custom_variable (google.ads.googleads.v7.resources.types.ConversionCustomVariable):
            The conversion custom variable referenced in
            the query.
        click_view (google.ads.googleads.v7.resources.types.ClickView):
            The ClickView referenced in the query.
        currency_constant (google.ads.googleads.v7.resources.types.CurrencyConstant):
            The currency constant referenced in the
            query.
        custom_audience (google.ads.googleads.v7.resources.types.CustomAudience):
            The CustomAudience referenced in the query.
        custom_interest (google.ads.googleads.v7.resources.types.CustomInterest):
            The CustomInterest referenced in the query.
        customer (google.ads.googleads.v7.resources.types.Customer):
            The customer referenced in the query.
        customer_asset (google.ads.googleads.v7.resources.types.CustomerAsset):
            The customer asset referenced in the query.
        customer_manager_link (google.ads.googleads.v7.resources.types.CustomerManagerLink):
            The CustomerManagerLink referenced in the
            query.
        customer_client_link (google.ads.googleads.v7.resources.types.CustomerClientLink):
            The CustomerClientLink referenced in the
            query.
        customer_client (google.ads.googleads.v7.resources.types.CustomerClient):
            The CustomerClient referenced in the query.
        customer_extension_setting (google.ads.googleads.v7.resources.types.CustomerExtensionSetting):
            The customer extension setting referenced in
            the query.
        customer_feed (google.ads.googleads.v7.resources.types.CustomerFeed):
            The customer feed referenced in the query.
        customer_label (google.ads.googleads.v7.resources.types.CustomerLabel):
            The customer label referenced in the query.
        customer_negative_criterion (google.ads.googleads.v7.resources.types.CustomerNegativeCriterion):
            The customer negative criterion referenced in
            the query.
        customer_user_access (google.ads.googleads.v7.resources.types.CustomerUserAccess):
            The CustomerUserAccess referenced in the
            query.
        customer_user_access_invitation (google.ads.googleads.v7.resources.types.CustomerUserAccessInvitation):
            The CustomerUserAccessInvitation referenced
            in the query.
        detail_placement_view (google.ads.googleads.v7.resources.types.DetailPlacementView):
            The detail placement view referenced in the
            query.
        display_keyword_view (google.ads.googleads.v7.resources.types.DisplayKeywordView):
            The display keyword view referenced in the
            query.
        distance_view (google.ads.googleads.v7.resources.types.DistanceView):
            The distance view referenced in the query.
        dynamic_search_ads_search_term_view (google.ads.googleads.v7.resources.types.DynamicSearchAdsSearchTermView):
            The dynamic search ads search term view
            referenced in the query.
        expanded_landing_page_view (google.ads.googleads.v7.resources.types.ExpandedLandingPageView):
            The expanded landing page view referenced in
            the query.
        extension_feed_item (google.ads.googleads.v7.resources.types.ExtensionFeedItem):
            The extension feed item referenced in the
            query.
        feed (google.ads.googleads.v7.resources.types.Feed):
            The feed referenced in the query.
        feed_item (google.ads.googleads.v7.resources.types.FeedItem):
            The feed item referenced in the query.
        feed_item_set (google.ads.googleads.v7.resources.types.FeedItemSet):
            The feed item set referenced in the query.
        feed_item_set_link (google.ads.googleads.v7.resources.types.FeedItemSetLink):
            The feed item set link referenced in the
            query.
        feed_item_target (google.ads.googleads.v7.resources.types.FeedItemTarget):
            The feed item target referenced in the query.
        feed_mapping (google.ads.googleads.v7.resources.types.FeedMapping):
            The feed mapping referenced in the query.
        feed_placeholder_view (google.ads.googleads.v7.resources.types.FeedPlaceholderView):
            The feed placeholder view referenced in the
            query.
        gender_view (google.ads.googleads.v7.resources.types.GenderView):
            The gender view referenced in the query.
        geo_target_constant (google.ads.googleads.v7.resources.types.GeoTargetConstant):
            The geo target constant referenced in the
            query.
        geographic_view (google.ads.googleads.v7.resources.types.GeographicView):
            The geographic view referenced in the query.
        group_placement_view (google.ads.googleads.v7.resources.types.GroupPlacementView):
            The group placement view referenced in the
            query.
        hotel_group_view (google.ads.googleads.v7.resources.types.HotelGroupView):
            The hotel group view referenced in the query.
        hotel_performance_view (google.ads.googleads.v7.resources.types.HotelPerformanceView):
            The hotel performance view referenced in the
            query.
        income_range_view (google.ads.googleads.v7.resources.types.IncomeRangeView):
            The income range view referenced in the
            query.
        keyword_view (google.ads.googleads.v7.resources.types.KeywordView):
            The keyword view referenced in the query.
        keyword_plan (google.ads.googleads.v7.resources.types.KeywordPlan):
            The keyword plan referenced in the query.
        keyword_plan_campaign (google.ads.googleads.v7.resources.types.KeywordPlanCampaign):
            The keyword plan campaign referenced in the
            query.
        keyword_plan_campaign_keyword (google.ads.googleads.v7.resources.types.KeywordPlanCampaignKeyword):
            The keyword plan campaign keyword referenced
            in the query.
        keyword_plan_ad_group (google.ads.googleads.v7.resources.types.KeywordPlanAdGroup):
            The keyword plan ad group referenced in the
            query.
        keyword_plan_ad_group_keyword (google.ads.googleads.v7.resources.types.KeywordPlanAdGroupKeyword):
            The keyword plan ad group referenced in the
            query.
        label (google.ads.googleads.v7.resources.types.Label):
            The label referenced in the query.
        landing_page_view (google.ads.googleads.v7.resources.types.LandingPageView):
            The landing page view referenced in the
            query.
        language_constant (google.ads.googleads.v7.resources.types.LanguageConstant):
            The language constant referenced in the
            query.
        location_view (google.ads.googleads.v7.resources.types.LocationView):
            The location view referenced in the query.
        managed_placement_view (google.ads.googleads.v7.resources.types.ManagedPlacementView):
            The managed placement view referenced in the
            query.
        media_file (google.ads.googleads.v7.resources.types.MediaFile):
            The media file referenced in the query.
        mobile_app_category_constant (google.ads.googleads.v7.resources.types.MobileAppCategoryConstant):
            The mobile app category constant referenced
            in the query.
        mobile_device_constant (google.ads.googleads.v7.resources.types.MobileDeviceConstant):
            The mobile device constant referenced in the
            query.
        offline_user_data_job (google.ads.googleads.v7.resources.types.OfflineUserDataJob):
            The offline user data job referenced in the
            query.
        operating_system_version_constant (google.ads.googleads.v7.resources.types.OperatingSystemVersionConstant):
            The operating system version constant
            referenced in the query.
        paid_organic_search_term_view (google.ads.googleads.v7.resources.types.PaidOrganicSearchTermView):
            The paid organic search term view referenced
            in the query.
        parental_status_view (google.ads.googleads.v7.resources.types.ParentalStatusView):
            The parental status view referenced in the
            query.
        product_bidding_category_constant (google.ads.googleads.v7.resources.types.ProductBiddingCategoryConstant):
            The Product Bidding Category referenced in
            the query.
        product_group_view (google.ads.googleads.v7.resources.types.ProductGroupView):
            The product group view referenced in the
            query.
        recommendation (google.ads.googleads.v7.resources.types.Recommendation):
            The recommendation referenced in the query.
        search_term_view (google.ads.googleads.v7.resources.types.SearchTermView):
            The search term view referenced in the query.
        shared_criterion (google.ads.googleads.v7.resources.types.SharedCriterion):
            The shared set referenced in the query.
        shared_set (google.ads.googleads.v7.resources.types.SharedSet):
            The shared set referenced in the query.
        shopping_performance_view (google.ads.googleads.v7.resources.types.ShoppingPerformanceView):
            The shopping performance view referenced in
            the query.
        third_party_app_analytics_link (google.ads.googleads.v7.resources.types.ThirdPartyAppAnalyticsLink):
            The AccountLink referenced in the query.
        topic_view (google.ads.googleads.v7.resources.types.TopicView):
            The topic view referenced in the query.
        user_interest (google.ads.googleads.v7.resources.types.UserInterest):
            The user interest referenced in the query.
        life_event (google.ads.googleads.v7.resources.types.LifeEvent):
            The life event referenced in the query.
        user_list (google.ads.googleads.v7.resources.types.UserList):
            The user list referenced in the query.
        user_location_view (google.ads.googleads.v7.resources.types.UserLocationView):
            The user location view referenced in the
            query.
        remarketing_action (google.ads.googleads.v7.resources.types.RemarketingAction):
            The remarketing action referenced in the
            query.
        topic_constant (google.ads.googleads.v7.resources.types.TopicConstant):
            The topic constant referenced in the query.
        video (google.ads.googleads.v7.resources.types.Video):
            The video referenced in the query.
        webpage_view (google.ads.googleads.v7.resources.types.WebpageView):
            The webpage view referenced in the query.
        metrics (google.ads.googleads.v7.common.types.Metrics):
            The metrics.
        segments (google.ads.googleads.v7.common.types.Segments):
            The segments.
    """

    account_budget = proto.Field(
        proto.MESSAGE, number=42, message=gagr_account_budget.AccountBudget,
    )
    account_budget_proposal = proto.Field(
        proto.MESSAGE,
        number=43,
        message=gagr_account_budget_proposal.AccountBudgetProposal,
    )
    account_link = proto.Field(
        proto.MESSAGE, number=143, message=gagr_account_link.AccountLink,
    )
    ad_group = proto.Field(
        proto.MESSAGE, number=3, message=gagr_ad_group.AdGroup,
    )
    ad_group_ad = proto.Field(
        proto.MESSAGE, number=16, message=gagr_ad_group_ad.AdGroupAd,
    )
    ad_group_ad_asset_view = proto.Field(
        proto.MESSAGE,
        number=131,
        message=gagr_ad_group_ad_asset_view.AdGroupAdAssetView,
    )
    ad_group_ad_label = proto.Field(
        proto.MESSAGE,
        number=120,
        message=gagr_ad_group_ad_label.AdGroupAdLabel,
    )
    ad_group_asset = proto.Field(
        proto.MESSAGE, number=154, message=gagr_ad_group_asset.AdGroupAsset,
    )
    ad_group_audience_view = proto.Field(
        proto.MESSAGE,
        number=57,
        message=gagr_ad_group_audience_view.AdGroupAudienceView,
    )
    ad_group_bid_modifier = proto.Field(
        proto.MESSAGE,
        number=24,
        message=gagr_ad_group_bid_modifier.AdGroupBidModifier,
    )
    ad_group_criterion = proto.Field(
        proto.MESSAGE,
        number=17,
        message=gagr_ad_group_criterion.AdGroupCriterion,
    )
    ad_group_criterion_label = proto.Field(
        proto.MESSAGE,
        number=121,
        message=gagr_ad_group_criterion_label.AdGroupCriterionLabel,
    )
    ad_group_criterion_simulation = proto.Field(
        proto.MESSAGE,
        number=110,
        message=gagr_ad_group_criterion_simulation.AdGroupCriterionSimulation,
    )
    ad_group_extension_setting = proto.Field(
        proto.MESSAGE,
        number=112,
        message=gagr_ad_group_extension_setting.AdGroupExtensionSetting,
    )
    ad_group_feed = proto.Field(
        proto.MESSAGE, number=67, message=gagr_ad_group_feed.AdGroupFeed,
    )
    ad_group_label = proto.Field(
        proto.MESSAGE, number=115, message=gagr_ad_group_label.AdGroupLabel,
    )
    ad_group_simulation = proto.Field(
        proto.MESSAGE,
        number=107,
        message=gagr_ad_group_simulation.AdGroupSimulation,
    )
    ad_parameter = proto.Field(
        proto.MESSAGE, number=130, message=gagr_ad_parameter.AdParameter,
    )
    age_range_view = proto.Field(
        proto.MESSAGE, number=48, message=gagr_age_range_view.AgeRangeView,
    )
    ad_schedule_view = proto.Field(
        proto.MESSAGE, number=89, message=gagr_ad_schedule_view.AdScheduleView,
    )
    domain_category = proto.Field(
        proto.MESSAGE, number=91, message=gagr_domain_category.DomainCategory,
    )
    asset = proto.Field(proto.MESSAGE, number=105, message=gagr_asset.Asset,)
    batch_job = proto.Field(
        proto.MESSAGE, number=139, message=gagr_batch_job.BatchJob,
    )
    bidding_strategy = proto.Field(
        proto.MESSAGE, number=18, message=gagr_bidding_strategy.BiddingStrategy,
    )
    bidding_strategy_simulation = proto.Field(
        proto.MESSAGE,
        number=158,
        message=gagr_bidding_strategy_simulation.BiddingStrategySimulation,
    )
    billing_setup = proto.Field(
        proto.MESSAGE, number=41, message=gagr_billing_setup.BillingSetup,
    )
    call_view = proto.Field(
        proto.MESSAGE, number=152, message=gagr_call_view.CallView,
    )
    campaign_budget = proto.Field(
        proto.MESSAGE, number=19, message=gagr_campaign_budget.CampaignBudget,
    )
    campaign = proto.Field(
        proto.MESSAGE, number=2, message=gagr_campaign.Campaign,
    )
    campaign_asset = proto.Field(
        proto.MESSAGE, number=142, message=gagr_campaign_asset.CampaignAsset,
    )
    campaign_audience_view = proto.Field(
        proto.MESSAGE,
        number=69,
        message=gagr_campaign_audience_view.CampaignAudienceView,
    )
    campaign_bid_modifier = proto.Field(
        proto.MESSAGE,
        number=26,
        message=gagr_campaign_bid_modifier.CampaignBidModifier,
    )
    campaign_criterion = proto.Field(
        proto.MESSAGE,
        number=20,
        message=gagr_campaign_criterion.CampaignCriterion,
    )
    campaign_criterion_simulation = proto.Field(
        proto.MESSAGE,
        number=111,
        message=gagr_campaign_criterion_simulation.CampaignCriterionSimulation,
    )
    campaign_draft = proto.Field(
        proto.MESSAGE, number=49, message=gagr_campaign_draft.CampaignDraft,
    )
    campaign_experiment = proto.Field(
        proto.MESSAGE,
        number=84,
        message=gagr_campaign_experiment.CampaignExperiment,
    )
    campaign_extension_setting = proto.Field(
        proto.MESSAGE,
        number=113,
        message=gagr_campaign_extension_setting.CampaignExtensionSetting,
    )
    campaign_feed = proto.Field(
        proto.MESSAGE, number=63, message=gagr_campaign_feed.CampaignFeed,
    )
    campaign_label = proto.Field(
        proto.MESSAGE, number=108, message=gagr_campaign_label.CampaignLabel,
    )
    campaign_shared_set = proto.Field(
        proto.MESSAGE,
        number=30,
        message=gagr_campaign_shared_set.CampaignSharedSet,
    )
    campaign_simulation = proto.Field(
        proto.MESSAGE,
        number=157,
        message=gagr_campaign_simulation.CampaignSimulation,
    )
    carrier_constant = proto.Field(
        proto.MESSAGE, number=66, message=gagr_carrier_constant.CarrierConstant,
    )
    change_event = proto.Field(
        proto.MESSAGE, number=145, message=gagr_change_event.ChangeEvent,
    )
    change_status = proto.Field(
        proto.MESSAGE, number=37, message=gagr_change_status.ChangeStatus,
    )
    combined_audience = proto.Field(
        proto.MESSAGE,
        number=148,
        message=gagr_combined_audience.CombinedAudience,
    )
    conversion_action = proto.Field(
        proto.MESSAGE,
        number=103,
        message=gagr_conversion_action.ConversionAction,
    )
    conversion_custom_variable = proto.Field(
        proto.MESSAGE,
        number=153,
        message=gagr_conversion_custom_variable.ConversionCustomVariable,
    )
    click_view = proto.Field(
        proto.MESSAGE, number=122, message=gagr_click_view.ClickView,
    )
    currency_constant = proto.Field(
        proto.MESSAGE,
        number=134,
        message=gagr_currency_constant.CurrencyConstant,
    )
    custom_audience = proto.Field(
        proto.MESSAGE, number=147, message=gagr_custom_audience.CustomAudience,
    )
    custom_interest = proto.Field(
        proto.MESSAGE, number=104, message=gagr_custom_interest.CustomInterest,
    )
    customer = proto.Field(
        proto.MESSAGE, number=1, message=gagr_customer.Customer,
    )
    customer_asset = proto.Field(
        proto.MESSAGE, number=155, message=gagr_customer_asset.CustomerAsset,
    )
    customer_manager_link = proto.Field(
        proto.MESSAGE,
        number=61,
        message=gagr_customer_manager_link.CustomerManagerLink,
    )
    customer_client_link = proto.Field(
        proto.MESSAGE,
        number=62,
        message=gagr_customer_client_link.CustomerClientLink,
    )
    customer_client = proto.Field(
        proto.MESSAGE, number=70, message=gagr_customer_client.CustomerClient,
    )
    customer_extension_setting = proto.Field(
        proto.MESSAGE,
        number=114,
        message=gagr_customer_extension_setting.CustomerExtensionSetting,
    )
    customer_feed = proto.Field(
        proto.MESSAGE, number=64, message=gagr_customer_feed.CustomerFeed,
    )
    customer_label = proto.Field(
        proto.MESSAGE, number=124, message=gagr_customer_label.CustomerLabel,
    )
    customer_negative_criterion = proto.Field(
        proto.MESSAGE,
        number=88,
        message=gagr_customer_negative_criterion.CustomerNegativeCriterion,
    )
    customer_user_access = proto.Field(
        proto.MESSAGE,
        number=146,
        message=gagr_customer_user_access.CustomerUserAccess,
    )
    customer_user_access_invitation = proto.Field(
        proto.MESSAGE,
        number=150,
        message=gagr_customer_user_access_invitation.CustomerUserAccessInvitation,
    )
    detail_placement_view = proto.Field(
        proto.MESSAGE,
        number=118,
        message=gagr_detail_placement_view.DetailPlacementView,
    )
    display_keyword_view = proto.Field(
        proto.MESSAGE,
        number=47,
        message=gagr_display_keyword_view.DisplayKeywordView,
    )
    distance_view = proto.Field(
        proto.MESSAGE, number=132, message=gagr_distance_view.DistanceView,
    )
    dynamic_search_ads_search_term_view = proto.Field(
        proto.MESSAGE,
        number=106,
        message=gagr_dynamic_search_ads_search_term_view.DynamicSearchAdsSearchTermView,
    )
    expanded_landing_page_view = proto.Field(
        proto.MESSAGE,
        number=128,
        message=gagr_expanded_landing_page_view.ExpandedLandingPageView,
    )
    extension_feed_item = proto.Field(
        proto.MESSAGE,
        number=85,
        message=gagr_extension_feed_item.ExtensionFeedItem,
    )
    feed = proto.Field(proto.MESSAGE, number=46, message=gagr_feed.Feed,)
    feed_item = proto.Field(
        proto.MESSAGE, number=50, message=gagr_feed_item.FeedItem,
    )
    feed_item_set = proto.Field(
        proto.MESSAGE, number=149, message=gagr_feed_item_set.FeedItemSet,
    )
    feed_item_set_link = proto.Field(
        proto.MESSAGE,
        number=151,
        message=gagr_feed_item_set_link.FeedItemSetLink,
    )
    feed_item_target = proto.Field(
        proto.MESSAGE, number=116, message=gagr_feed_item_target.FeedItemTarget,
    )
    feed_mapping = proto.Field(
        proto.MESSAGE, number=58, message=gagr_feed_mapping.FeedMapping,
    )
    feed_placeholder_view = proto.Field(
        proto.MESSAGE,
        number=97,
        message=gagr_feed_placeholder_view.FeedPlaceholderView,
    )
    gender_view = proto.Field(
        proto.MESSAGE, number=40, message=gagr_gender_view.GenderView,
    )
    geo_target_constant = proto.Field(
        proto.MESSAGE,
        number=23,
        message=gagr_geo_target_constant.GeoTargetConstant,
    )
    geographic_view = proto.Field(
        proto.MESSAGE, number=125, message=gagr_geographic_view.GeographicView,
    )
    group_placement_view = proto.Field(
        proto.MESSAGE,
        number=119,
        message=gagr_group_placement_view.GroupPlacementView,
    )
    hotel_group_view = proto.Field(
        proto.MESSAGE, number=51, message=gagr_hotel_group_view.HotelGroupView,
    )
    hotel_performance_view = proto.Field(
        proto.MESSAGE,
        number=71,
        message=gagr_hotel_performance_view.HotelPerformanceView,
    )
    income_range_view = proto.Field(
        proto.MESSAGE,
        number=138,
        message=gagr_income_range_view.IncomeRangeView,
    )
    keyword_view = proto.Field(
        proto.MESSAGE, number=21, message=gagr_keyword_view.KeywordView,
    )
    keyword_plan = proto.Field(
        proto.MESSAGE, number=32, message=gagr_keyword_plan.KeywordPlan,
    )
    keyword_plan_campaign = proto.Field(
        proto.MESSAGE,
        number=33,
        message=gagr_keyword_plan_campaign.KeywordPlanCampaign,
    )
    keyword_plan_campaign_keyword = proto.Field(
        proto.MESSAGE,
        number=140,
        message=gagr_keyword_plan_campaign_keyword.KeywordPlanCampaignKeyword,
    )
    keyword_plan_ad_group = proto.Field(
        proto.MESSAGE,
        number=35,
        message=gagr_keyword_plan_ad_group.KeywordPlanAdGroup,
    )
    keyword_plan_ad_group_keyword = proto.Field(
        proto.MESSAGE,
        number=141,
        message=gagr_keyword_plan_ad_group_keyword.KeywordPlanAdGroupKeyword,
    )
    label = proto.Field(proto.MESSAGE, number=52, message=gagr_label.Label,)
    landing_page_view = proto.Field(
        proto.MESSAGE,
        number=126,
        message=gagr_landing_page_view.LandingPageView,
    )
    language_constant = proto.Field(
        proto.MESSAGE,
        number=55,
        message=gagr_language_constant.LanguageConstant,
    )
    location_view = proto.Field(
        proto.MESSAGE, number=123, message=gagr_location_view.LocationView,
    )
    managed_placement_view = proto.Field(
        proto.MESSAGE,
        number=53,
        message=gagr_managed_placement_view.ManagedPlacementView,
    )
    media_file = proto.Field(
        proto.MESSAGE, number=90, message=gagr_media_file.MediaFile,
    )
    mobile_app_category_constant = proto.Field(
        proto.MESSAGE,
        number=87,
        message=gagr_mobile_app_category_constant.MobileAppCategoryConstant,
    )
    mobile_device_constant = proto.Field(
        proto.MESSAGE,
        number=98,
        message=gagr_mobile_device_constant.MobileDeviceConstant,
    )
    offline_user_data_job = proto.Field(
        proto.MESSAGE,
        number=137,
        message=gagr_offline_user_data_job.OfflineUserDataJob,
    )
    operating_system_version_constant = proto.Field(
        proto.MESSAGE,
        number=86,
        message=gagr_operating_system_version_constant.OperatingSystemVersionConstant,
    )
    paid_organic_search_term_view = proto.Field(
        proto.MESSAGE,
        number=129,
        message=gagr_paid_organic_search_term_view.PaidOrganicSearchTermView,
    )
    parental_status_view = proto.Field(
        proto.MESSAGE,
        number=45,
        message=gagr_parental_status_view.ParentalStatusView,
    )
    product_bidding_category_constant = proto.Field(
        proto.MESSAGE,
        number=109,
        message=gagr_product_bidding_category_constant.ProductBiddingCategoryConstant,
    )
    product_group_view = proto.Field(
        proto.MESSAGE,
        number=54,
        message=gagr_product_group_view.ProductGroupView,
    )
    recommendation = proto.Field(
        proto.MESSAGE, number=22, message=gagr_recommendation.Recommendation,
    )
    search_term_view = proto.Field(
        proto.MESSAGE, number=68, message=gagr_search_term_view.SearchTermView,
    )
    shared_criterion = proto.Field(
        proto.MESSAGE, number=29, message=gagr_shared_criterion.SharedCriterion,
    )
    shared_set = proto.Field(
        proto.MESSAGE, number=27, message=gagr_shared_set.SharedSet,
    )
    shopping_performance_view = proto.Field(
        proto.MESSAGE,
        number=117,
        message=gagr_shopping_performance_view.ShoppingPerformanceView,
    )
    third_party_app_analytics_link = proto.Field(
        proto.MESSAGE,
        number=144,
        message=gagr_third_party_app_analytics_link.ThirdPartyAppAnalyticsLink,
    )
    topic_view = proto.Field(
        proto.MESSAGE, number=44, message=gagr_topic_view.TopicView,
    )
    user_interest = proto.Field(
        proto.MESSAGE, number=59, message=gagr_user_interest.UserInterest,
    )
    life_event = proto.Field(
        proto.MESSAGE, number=161, message=gagr_life_event.LifeEvent,
    )
    user_list = proto.Field(
        proto.MESSAGE, number=38, message=gagr_user_list.UserList,
    )
    user_location_view = proto.Field(
        proto.MESSAGE,
        number=135,
        message=gagr_user_location_view.UserLocationView,
    )
    remarketing_action = proto.Field(
        proto.MESSAGE,
        number=60,
        message=gagr_remarketing_action.RemarketingAction,
    )
    topic_constant = proto.Field(
        proto.MESSAGE, number=31, message=gagr_topic_constant.TopicConstant,
    )
    video = proto.Field(proto.MESSAGE, number=39, message=gagr_video.Video,)
    webpage_view = proto.Field(
        proto.MESSAGE, number=162, message=gagr_webpage_view.WebpageView,
    )
    metrics = proto.Field(
        proto.MESSAGE, number=4, message=gagc_metrics.Metrics,
    )
    segments = proto.Field(
        proto.MESSAGE, number=102, message=gagc_segments.Segments,
    )


class MutateGoogleAdsRequest(proto.Message):
    r"""Request message for
    [GoogleAdsService.Mutate][google.ads.googleads.v7.services.GoogleAdsService.Mutate].

    Attributes:
        customer_id (str):
            Required. The ID of the customer whose
            resources are being modified.
        mutate_operations (Sequence[google.ads.googleads.v7.services.types.MutateOperation]):
            Required. The list of operations to perform
            on individual resources.
        partial_failure (bool):
            If true, successful operations will be
            carried out and invalid operations will return
            errors. If false, all operations will be carried
            out in one transaction if and only if they are
            all valid. Default is false.
        validate_only (bool):
            If true, the request is validated but not
            executed. Only errors are returned, not results.
        response_content_type (google.ads.googleads.v7.enums.types.ResponseContentTypeEnum.ResponseContentType):
            The response content type setting. Determines
            whether the mutable resource or just the
            resource name should be returned post mutation.
            The mutable resource will only be returned if
            the resource has the appropriate response field.
            E.g. MutateCampaignResult.campaign.
    """

    customer_id = proto.Field(proto.STRING, number=1,)
    mutate_operations = proto.RepeatedField(
        proto.MESSAGE, number=2, message="MutateOperation",
    )
    partial_failure = proto.Field(proto.BOOL, number=3,)
    validate_only = proto.Field(proto.BOOL, number=4,)
    response_content_type = proto.Field(
        proto.ENUM,
        number=5,
        enum=gage_response_content_type.ResponseContentTypeEnum.ResponseContentType,
    )


class MutateGoogleAdsResponse(proto.Message):
    r"""Response message for
    [GoogleAdsService.Mutate][google.ads.googleads.v7.services.GoogleAdsService.Mutate].

    Attributes:
        partial_failure_error (google.rpc.status_pb2.Status):
            Errors that pertain to operation failures in the partial
            failure mode. Returned only when partial_failure = true and
            all errors occur inside the operations. If any errors occur
            outside the operations (e.g., auth errors), we return an RPC
            level error.
        mutate_operation_responses (Sequence[google.ads.googleads.v7.services.types.MutateOperationResponse]):
            All responses for the mutate.
    """

    partial_failure_error = proto.Field(
        proto.MESSAGE, number=3, message=status.Status,
    )
    mutate_operation_responses = proto.RepeatedField(
        proto.MESSAGE, number=1, message="MutateOperationResponse",
    )


class MutateOperation(proto.Message):
    r"""A single operation (create, update, remove) on a resource.
    Attributes:
        ad_group_ad_label_operation (google.ads.googleads.v7.services.types.AdGroupAdLabelOperation):
            An ad group ad label mutate operation.
        ad_group_ad_operation (google.ads.googleads.v7.services.types.AdGroupAdOperation):
            An ad group ad mutate operation.
        ad_group_asset_operation (google.ads.googleads.v7.services.types.AdGroupAssetOperation):
            An ad group asset mutate operation.
        ad_group_bid_modifier_operation (google.ads.googleads.v7.services.types.AdGroupBidModifierOperation):
            An ad group bid modifier mutate operation.
        ad_group_criterion_label_operation (google.ads.googleads.v7.services.types.AdGroupCriterionLabelOperation):
            An ad group criterion label mutate operation.
        ad_group_criterion_operation (google.ads.googleads.v7.services.types.AdGroupCriterionOperation):
            An ad group criterion mutate operation.
        ad_group_extension_setting_operation (google.ads.googleads.v7.services.types.AdGroupExtensionSettingOperation):
            An ad group extension setting mutate
            operation.
        ad_group_feed_operation (google.ads.googleads.v7.services.types.AdGroupFeedOperation):
            An ad group feed mutate operation.
        ad_group_label_operation (google.ads.googleads.v7.services.types.AdGroupLabelOperation):
            An ad group label mutate operation.
        ad_group_operation (google.ads.googleads.v7.services.types.AdGroupOperation):
            An ad group mutate operation.
        ad_operation (google.ads.googleads.v7.services.types.AdOperation):
            An ad mutate operation.
        ad_parameter_operation (google.ads.googleads.v7.services.types.AdParameterOperation):
            An ad parameter mutate operation.
        asset_operation (google.ads.googleads.v7.services.types.AssetOperation):
            An asset mutate operation.
        bidding_strategy_operation (google.ads.googleads.v7.services.types.BiddingStrategyOperation):
            A bidding strategy mutate operation.
        campaign_asset_operation (google.ads.googleads.v7.services.types.CampaignAssetOperation):
            A campaign asset mutate operation.
        campaign_bid_modifier_operation (google.ads.googleads.v7.services.types.CampaignBidModifierOperation):
            A campaign bid modifier mutate operation.
        campaign_budget_operation (google.ads.googleads.v7.services.types.CampaignBudgetOperation):
            A campaign budget mutate operation.
        campaign_criterion_operation (google.ads.googleads.v7.services.types.CampaignCriterionOperation):
            A campaign criterion mutate operation.
        campaign_draft_operation (google.ads.googleads.v7.services.types.CampaignDraftOperation):
            A campaign draft mutate operation.
        campaign_experiment_operation (google.ads.googleads.v7.services.types.CampaignExperimentOperation):
            A campaign experiment mutate operation.
        campaign_extension_setting_operation (google.ads.googleads.v7.services.types.CampaignExtensionSettingOperation):
            A campaign extension setting mutate
            operation.
        campaign_feed_operation (google.ads.googleads.v7.services.types.CampaignFeedOperation):
            A campaign feed mutate operation.
        campaign_label_operation (google.ads.googleads.v7.services.types.CampaignLabelOperation):
            A campaign label mutate operation.
        campaign_operation (google.ads.googleads.v7.services.types.CampaignOperation):
            A campaign mutate operation.
        campaign_shared_set_operation (google.ads.googleads.v7.services.types.CampaignSharedSetOperation):
            A campaign shared set mutate operation.
        conversion_action_operation (google.ads.googleads.v7.services.types.ConversionActionOperation):
            A conversion action mutate operation.
        conversion_custom_variable_operation (google.ads.googleads.v7.services.types.ConversionCustomVariableOperation):
            A conversion custom variable mutate
            operation.
        customer_asset_operation (google.ads.googleads.v7.services.types.CustomerAssetOperation):
            A customer asset mutate operation.
        customer_extension_setting_operation (google.ads.googleads.v7.services.types.CustomerExtensionSettingOperation):
            A customer extension setting mutate
            operation.
        customer_feed_operation (google.ads.googleads.v7.services.types.CustomerFeedOperation):
            A customer feed mutate operation.
        customer_label_operation (google.ads.googleads.v7.services.types.CustomerLabelOperation):
            A customer label mutate operation.
        customer_negative_criterion_operation (google.ads.googleads.v7.services.types.CustomerNegativeCriterionOperation):
            A customer negative criterion mutate
            operation.
        customer_operation (google.ads.googleads.v7.services.types.CustomerOperation):
            A customer mutate operation.
        extension_feed_item_operation (google.ads.googleads.v7.services.types.ExtensionFeedItemOperation):
            An extension feed item mutate operation.
        feed_item_operation (google.ads.googleads.v7.services.types.FeedItemOperation):
            A feed item mutate operation.
        feed_item_set_operation (google.ads.googleads.v7.services.types.FeedItemSetOperation):
            A feed item set mutate operation.
        feed_item_set_link_operation (google.ads.googleads.v7.services.types.FeedItemSetLinkOperation):
            A feed item set link mutate operation.
        feed_item_target_operation (google.ads.googleads.v7.services.types.FeedItemTargetOperation):
            A feed item target mutate operation.
        feed_mapping_operation (google.ads.googleads.v7.services.types.FeedMappingOperation):
            A feed mapping mutate operation.
        feed_operation (google.ads.googleads.v7.services.types.FeedOperation):
            A feed mutate operation.
        keyword_plan_ad_group_operation (google.ads.googleads.v7.services.types.KeywordPlanAdGroupOperation):
            A keyword plan ad group operation.
        keyword_plan_ad_group_keyword_operation (google.ads.googleads.v7.services.types.KeywordPlanAdGroupKeywordOperation):
            A keyword plan ad group keyword operation.
        keyword_plan_campaign_keyword_operation (google.ads.googleads.v7.services.types.KeywordPlanCampaignKeywordOperation):
            A keyword plan campaign keyword operation.
        keyword_plan_campaign_operation (google.ads.googleads.v7.services.types.KeywordPlanCampaignOperation):
            A keyword plan campaign operation.
        keyword_plan_operation (google.ads.googleads.v7.services.types.KeywordPlanOperation):
            A keyword plan operation.
        label_operation (google.ads.googleads.v7.services.types.LabelOperation):
            A label mutate operation.
        media_file_operation (google.ads.googleads.v7.services.types.MediaFileOperation):
            A media file mutate operation.
        remarketing_action_operation (google.ads.googleads.v7.services.types.RemarketingActionOperation):
            A remarketing action mutate operation.
        shared_criterion_operation (google.ads.googleads.v7.services.types.SharedCriterionOperation):
            A shared criterion mutate operation.
        shared_set_operation (google.ads.googleads.v7.services.types.SharedSetOperation):
            A shared set mutate operation.
        user_list_operation (google.ads.googleads.v7.services.types.UserListOperation):
            A user list mutate operation.
    """

    ad_group_ad_label_operation = proto.Field(
        proto.MESSAGE,
        number=17,
        oneof="operation",
        message=ad_group_ad_label_service.AdGroupAdLabelOperation,
    )
    ad_group_ad_operation = proto.Field(
        proto.MESSAGE,
        number=1,
        oneof="operation",
        message=ad_group_ad_service.AdGroupAdOperation,
    )
    ad_group_asset_operation = proto.Field(
        proto.MESSAGE,
        number=56,
        oneof="operation",
        message=ad_group_asset_service.AdGroupAssetOperation,
    )
    ad_group_bid_modifier_operation = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="operation",
        message=ad_group_bid_modifier_service.AdGroupBidModifierOperation,
    )
    ad_group_criterion_label_operation = proto.Field(
        proto.MESSAGE,
        number=18,
        oneof="operation",
        message=ad_group_criterion_label_service.AdGroupCriterionLabelOperation,
    )
    ad_group_criterion_operation = proto.Field(
        proto.MESSAGE,
        number=3,
        oneof="operation",
        message=ad_group_criterion_service.AdGroupCriterionOperation,
    )
    ad_group_extension_setting_operation = proto.Field(
        proto.MESSAGE,
        number=19,
        oneof="operation",
        message=ad_group_extension_setting_service.AdGroupExtensionSettingOperation,
    )
    ad_group_feed_operation = proto.Field(
        proto.MESSAGE,
        number=20,
        oneof="operation",
        message=ad_group_feed_service.AdGroupFeedOperation,
    )
    ad_group_label_operation = proto.Field(
        proto.MESSAGE,
        number=21,
        oneof="operation",
        message=ad_group_label_service.AdGroupLabelOperation,
    )
    ad_group_operation = proto.Field(
        proto.MESSAGE,
        number=5,
        oneof="operation",
        message=ad_group_service.AdGroupOperation,
    )
    ad_operation = proto.Field(
        proto.MESSAGE,
        number=49,
        oneof="operation",
        message=ad_service.AdOperation,
    )
    ad_parameter_operation = proto.Field(
        proto.MESSAGE,
        number=22,
        oneof="operation",
        message=ad_parameter_service.AdParameterOperation,
    )
    asset_operation = proto.Field(
        proto.MESSAGE,
        number=23,
        oneof="operation",
        message=asset_service.AssetOperation,
    )
    bidding_strategy_operation = proto.Field(
        proto.MESSAGE,
        number=6,
        oneof="operation",
        message=bidding_strategy_service.BiddingStrategyOperation,
    )
    campaign_asset_operation = proto.Field(
        proto.MESSAGE,
        number=52,
        oneof="operation",
        message=campaign_asset_service.CampaignAssetOperation,
    )
    campaign_bid_modifier_operation = proto.Field(
        proto.MESSAGE,
        number=7,
        oneof="operation",
        message=campaign_bid_modifier_service.CampaignBidModifierOperation,
    )
    campaign_budget_operation = proto.Field(
        proto.MESSAGE,
        number=8,
        oneof="operation",
        message=campaign_budget_service.CampaignBudgetOperation,
    )
    campaign_criterion_operation = proto.Field(
        proto.MESSAGE,
        number=13,
        oneof="operation",
        message=campaign_criterion_service.CampaignCriterionOperation,
    )
    campaign_draft_operation = proto.Field(
        proto.MESSAGE,
        number=24,
        oneof="operation",
        message=campaign_draft_service.CampaignDraftOperation,
    )
    campaign_experiment_operation = proto.Field(
        proto.MESSAGE,
        number=25,
        oneof="operation",
        message=campaign_experiment_service.CampaignExperimentOperation,
    )
    campaign_extension_setting_operation = proto.Field(
        proto.MESSAGE,
        number=26,
        oneof="operation",
        message=campaign_extension_setting_service.CampaignExtensionSettingOperation,
    )
    campaign_feed_operation = proto.Field(
        proto.MESSAGE,
        number=27,
        oneof="operation",
        message=campaign_feed_service.CampaignFeedOperation,
    )
    campaign_label_operation = proto.Field(
        proto.MESSAGE,
        number=28,
        oneof="operation",
        message=campaign_label_service.CampaignLabelOperation,
    )
    campaign_operation = proto.Field(
        proto.MESSAGE,
        number=10,
        oneof="operation",
        message=campaign_service.CampaignOperation,
    )
    campaign_shared_set_operation = proto.Field(
        proto.MESSAGE,
        number=11,
        oneof="operation",
        message=campaign_shared_set_service.CampaignSharedSetOperation,
    )
    conversion_action_operation = proto.Field(
        proto.MESSAGE,
        number=12,
        oneof="operation",
        message=conversion_action_service.ConversionActionOperation,
    )
    conversion_custom_variable_operation = proto.Field(
        proto.MESSAGE,
        number=55,
        oneof="operation",
        message=conversion_custom_variable_service.ConversionCustomVariableOperation,
    )
    customer_asset_operation = proto.Field(
        proto.MESSAGE,
        number=57,
        oneof="operation",
        message=customer_asset_service.CustomerAssetOperation,
    )
    customer_extension_setting_operation = proto.Field(
        proto.MESSAGE,
        number=30,
        oneof="operation",
        message=customer_extension_setting_service.CustomerExtensionSettingOperation,
    )
    customer_feed_operation = proto.Field(
        proto.MESSAGE,
        number=31,
        oneof="operation",
        message=customer_feed_service.CustomerFeedOperation,
    )
    customer_label_operation = proto.Field(
        proto.MESSAGE,
        number=32,
        oneof="operation",
        message=customer_label_service.CustomerLabelOperation,
    )
    customer_negative_criterion_operation = proto.Field(
        proto.MESSAGE,
        number=34,
        oneof="operation",
        message=customer_negative_criterion_service.CustomerNegativeCriterionOperation,
    )
    customer_operation = proto.Field(
        proto.MESSAGE,
        number=35,
        oneof="operation",
        message=customer_service.CustomerOperation,
    )
    extension_feed_item_operation = proto.Field(
        proto.MESSAGE,
        number=36,
        oneof="operation",
        message=extension_feed_item_service.ExtensionFeedItemOperation,
    )
    feed_item_operation = proto.Field(
        proto.MESSAGE,
        number=37,
        oneof="operation",
        message=feed_item_service.FeedItemOperation,
    )
    feed_item_set_operation = proto.Field(
        proto.MESSAGE,
        number=53,
        oneof="operation",
        message=feed_item_set_service.FeedItemSetOperation,
    )
    feed_item_set_link_operation = proto.Field(
        proto.MESSAGE,
        number=54,
        oneof="operation",
        message=feed_item_set_link_service.FeedItemSetLinkOperation,
    )
    feed_item_target_operation = proto.Field(
        proto.MESSAGE,
        number=38,
        oneof="operation",
        message=feed_item_target_service.FeedItemTargetOperation,
    )
    feed_mapping_operation = proto.Field(
        proto.MESSAGE,
        number=39,
        oneof="operation",
        message=feed_mapping_service.FeedMappingOperation,
    )
    feed_operation = proto.Field(
        proto.MESSAGE,
        number=40,
        oneof="operation",
        message=feed_service.FeedOperation,
    )
    keyword_plan_ad_group_operation = proto.Field(
        proto.MESSAGE,
        number=44,
        oneof="operation",
        message=keyword_plan_ad_group_service.KeywordPlanAdGroupOperation,
    )
    keyword_plan_ad_group_keyword_operation = proto.Field(
        proto.MESSAGE,
        number=50,
        oneof="operation",
        message=keyword_plan_ad_group_keyword_service.KeywordPlanAdGroupKeywordOperation,
    )
    keyword_plan_campaign_keyword_operation = proto.Field(
        proto.MESSAGE,
        number=51,
        oneof="operation",
        message=keyword_plan_campaign_keyword_service.KeywordPlanCampaignKeywordOperation,
    )
    keyword_plan_campaign_operation = proto.Field(
        proto.MESSAGE,
        number=45,
        oneof="operation",
        message=keyword_plan_campaign_service.KeywordPlanCampaignOperation,
    )
    keyword_plan_operation = proto.Field(
        proto.MESSAGE,
        number=48,
        oneof="operation",
        message=keyword_plan_service.KeywordPlanOperation,
    )
    label_operation = proto.Field(
        proto.MESSAGE,
        number=41,
        oneof="operation",
        message=label_service.LabelOperation,
    )
    media_file_operation = proto.Field(
        proto.MESSAGE,
        number=42,
        oneof="operation",
        message=media_file_service.MediaFileOperation,
    )
    remarketing_action_operation = proto.Field(
        proto.MESSAGE,
        number=43,
        oneof="operation",
        message=remarketing_action_service.RemarketingActionOperation,
    )
    shared_criterion_operation = proto.Field(
        proto.MESSAGE,
        number=14,
        oneof="operation",
        message=shared_criterion_service.SharedCriterionOperation,
    )
    shared_set_operation = proto.Field(
        proto.MESSAGE,
        number=15,
        oneof="operation",
        message=shared_set_service.SharedSetOperation,
    )
    user_list_operation = proto.Field(
        proto.MESSAGE,
        number=16,
        oneof="operation",
        message=user_list_service.UserListOperation,
    )


class MutateOperationResponse(proto.Message):
    r"""Response message for the resource mutate.
    Attributes:
        ad_group_ad_label_result (google.ads.googleads.v7.services.types.MutateAdGroupAdLabelResult):
            The result for the ad group ad label mutate.
        ad_group_ad_result (google.ads.googleads.v7.services.types.MutateAdGroupAdResult):
            The result for the ad group ad mutate.
        ad_group_asset_result (google.ads.googleads.v7.services.types.MutateAdGroupAssetResult):
            The result for the ad group asset mutate.
        ad_group_bid_modifier_result (google.ads.googleads.v7.services.types.MutateAdGroupBidModifierResult):
            The result for the ad group bid modifier
            mutate.
        ad_group_criterion_label_result (google.ads.googleads.v7.services.types.MutateAdGroupCriterionLabelResult):
            The result for the ad group criterion label
            mutate.
        ad_group_criterion_result (google.ads.googleads.v7.services.types.MutateAdGroupCriterionResult):
            The result for the ad group criterion mutate.
        ad_group_extension_setting_result (google.ads.googleads.v7.services.types.MutateAdGroupExtensionSettingResult):
            The result for the ad group extension setting
            mutate.
        ad_group_feed_result (google.ads.googleads.v7.services.types.MutateAdGroupFeedResult):
            The result for the ad group feed mutate.
        ad_group_label_result (google.ads.googleads.v7.services.types.MutateAdGroupLabelResult):
            The result for the ad group label mutate.
        ad_group_result (google.ads.googleads.v7.services.types.MutateAdGroupResult):
            The result for the ad group mutate.
        ad_parameter_result (google.ads.googleads.v7.services.types.MutateAdParameterResult):
            The result for the ad parameter mutate.
        ad_result (google.ads.googleads.v7.services.types.MutateAdResult):
            The result for the ad mutate.
        asset_result (google.ads.googleads.v7.services.types.MutateAssetResult):
            The result for the asset mutate.
        bidding_strategy_result (google.ads.googleads.v7.services.types.MutateBiddingStrategyResult):
            The result for the bidding strategy mutate.
        campaign_asset_result (google.ads.googleads.v7.services.types.MutateCampaignAssetResult):
            The result for the campaign asset mutate.
        campaign_bid_modifier_result (google.ads.googleads.v7.services.types.MutateCampaignBidModifierResult):
            The result for the campaign bid modifier
            mutate.
        campaign_budget_result (google.ads.googleads.v7.services.types.MutateCampaignBudgetResult):
            The result for the campaign budget mutate.
        campaign_criterion_result (google.ads.googleads.v7.services.types.MutateCampaignCriterionResult):
            The result for the campaign criterion mutate.
        campaign_draft_result (google.ads.googleads.v7.services.types.MutateCampaignDraftResult):
            The result for the campaign draft mutate.
        campaign_experiment_result (google.ads.googleads.v7.services.types.MutateCampaignExperimentResult):
            The result for the campaign experiment
            mutate.
        campaign_extension_setting_result (google.ads.googleads.v7.services.types.MutateCampaignExtensionSettingResult):
            The result for the campaign extension setting
            mutate.
        campaign_feed_result (google.ads.googleads.v7.services.types.MutateCampaignFeedResult):
            The result for the campaign feed mutate.
        campaign_label_result (google.ads.googleads.v7.services.types.MutateCampaignLabelResult):
            The result for the campaign label mutate.
        campaign_result (google.ads.googleads.v7.services.types.MutateCampaignResult):
            The result for the campaign mutate.
        campaign_shared_set_result (google.ads.googleads.v7.services.types.MutateCampaignSharedSetResult):
            The result for the campaign shared set
            mutate.
        conversion_action_result (google.ads.googleads.v7.services.types.MutateConversionActionResult):
            The result for the conversion action mutate.
        conversion_custom_variable_result (google.ads.googleads.v7.services.types.MutateConversionCustomVariableResult):
            The result for the conversion custom variable
            mutate.
        customer_asset_result (google.ads.googleads.v7.services.types.MutateCustomerAssetResult):
            The result for the customer asset mutate.
        customer_extension_setting_result (google.ads.googleads.v7.services.types.MutateCustomerExtensionSettingResult):
            The result for the customer extension setting
            mutate.
        customer_feed_result (google.ads.googleads.v7.services.types.MutateCustomerFeedResult):
            The result for the customer feed mutate.
        customer_label_result (google.ads.googleads.v7.services.types.MutateCustomerLabelResult):
            The result for the customer label mutate.
        customer_negative_criterion_result (google.ads.googleads.v7.services.types.MutateCustomerNegativeCriteriaResult):
            The result for the customer negative
            criterion mutate.
        customer_result (google.ads.googleads.v7.services.types.MutateCustomerResult):
            The result for the customer mutate.
        extension_feed_item_result (google.ads.googleads.v7.services.types.MutateExtensionFeedItemResult):
            The result for the extension feed item
            mutate.
        feed_item_result (google.ads.googleads.v7.services.types.MutateFeedItemResult):
            The result for the feed item mutate.
        feed_item_set_result (google.ads.googleads.v7.services.types.MutateFeedItemSetResult):
            The result for the feed item set mutate.
        feed_item_set_link_result (google.ads.googleads.v7.services.types.MutateFeedItemSetLinkResult):
            The result for the feed item set link mutate.
        feed_item_target_result (google.ads.googleads.v7.services.types.MutateFeedItemTargetResult):
            The result for the feed item target mutate.
        feed_mapping_result (google.ads.googleads.v7.services.types.MutateFeedMappingResult):
            The result for the feed mapping mutate.
        feed_result (google.ads.googleads.v7.services.types.MutateFeedResult):
            The result for the feed mutate.
        keyword_plan_ad_group_result (google.ads.googleads.v7.services.types.MutateKeywordPlanAdGroupResult):
            The result for the keyword plan ad group
            mutate.
        keyword_plan_campaign_result (google.ads.googleads.v7.services.types.MutateKeywordPlanCampaignResult):
            The result for the keyword plan campaign
            mutate.
        keyword_plan_ad_group_keyword_result (google.ads.googleads.v7.services.types.MutateKeywordPlanAdGroupKeywordResult):
            The result for the keyword plan ad group
            keyword mutate.
        keyword_plan_campaign_keyword_result (google.ads.googleads.v7.services.types.MutateKeywordPlanCampaignKeywordResult):
            The result for the keyword plan campaign
            keyword mutate.
        keyword_plan_result (google.ads.googleads.v7.services.types.MutateKeywordPlansResult):
            The result for the keyword plan mutate.
        label_result (google.ads.googleads.v7.services.types.MutateLabelResult):
            The result for the label mutate.
        media_file_result (google.ads.googleads.v7.services.types.MutateMediaFileResult):
            The result for the media file mutate.
        remarketing_action_result (google.ads.googleads.v7.services.types.MutateRemarketingActionResult):
            The result for the remarketing action mutate.
        shared_criterion_result (google.ads.googleads.v7.services.types.MutateSharedCriterionResult):
            The result for the shared criterion mutate.
        shared_set_result (google.ads.googleads.v7.services.types.MutateSharedSetResult):
            The result for the shared set mutate.
        user_list_result (google.ads.googleads.v7.services.types.MutateUserListResult):
            The result for the user list mutate.
    """

    ad_group_ad_label_result = proto.Field(
        proto.MESSAGE,
        number=17,
        oneof="response",
        message=ad_group_ad_label_service.MutateAdGroupAdLabelResult,
    )
    ad_group_ad_result = proto.Field(
        proto.MESSAGE,
        number=1,
        oneof="response",
        message=ad_group_ad_service.MutateAdGroupAdResult,
    )
    ad_group_asset_result = proto.Field(
        proto.MESSAGE,
        number=56,
        oneof="response",
        message=ad_group_asset_service.MutateAdGroupAssetResult,
    )
    ad_group_bid_modifier_result = proto.Field(
        proto.MESSAGE,
        number=2,
        oneof="response",
        message=ad_group_bid_modifier_service.MutateAdGroupBidModifierResult,
    )
    ad_group_criterion_label_result = proto.Field(
        proto.MESSAGE,
        number=18,
        oneof="response",
        message=ad_group_criterion_label_service.MutateAdGroupCriterionLabelResult,
    )
    ad_group_criterion_result = proto.Field(
        proto.MESSAGE,
        number=3,
        oneof="response",
        message=ad_group_criterion_service.MutateAdGroupCriterionResult,
    )
    ad_group_extension_setting_result = proto.Field(
        proto.MESSAGE,
        number=19,
        oneof="response",
        message=ad_group_extension_setting_service.MutateAdGroupExtensionSettingResult,
    )
    ad_group_feed_result = proto.Field(
        proto.MESSAGE,
        number=20,
        oneof="response",
        message=ad_group_feed_service.MutateAdGroupFeedResult,
    )
    ad_group_label_result = proto.Field(
        proto.MESSAGE,
        number=21,
        oneof="response",
        message=ad_group_label_service.MutateAdGroupLabelResult,
    )
    ad_group_result = proto.Field(
        proto.MESSAGE,
        number=5,
        oneof="response",
        message=ad_group_service.MutateAdGroupResult,
    )
    ad_parameter_result = proto.Field(
        proto.MESSAGE,
        number=22,
        oneof="response",
        message=ad_parameter_service.MutateAdParameterResult,
    )
    ad_result = proto.Field(
        proto.MESSAGE,
        number=49,
        oneof="response",
        message=ad_service.MutateAdResult,
    )
    asset_result = proto.Field(
        proto.MESSAGE,
        number=23,
        oneof="response",
        message=asset_service.MutateAssetResult,
    )
    bidding_strategy_result = proto.Field(
        proto.MESSAGE,
        number=6,
        oneof="response",
        message=bidding_strategy_service.MutateBiddingStrategyResult,
    )
    campaign_asset_result = proto.Field(
        proto.MESSAGE,
        number=52,
        oneof="response",
        message=campaign_asset_service.MutateCampaignAssetResult,
    )
    campaign_bid_modifier_result = proto.Field(
        proto.MESSAGE,
        number=7,
        oneof="response",
        message=campaign_bid_modifier_service.MutateCampaignBidModifierResult,
    )
    campaign_budget_result = proto.Field(
        proto.MESSAGE,
        number=8,
        oneof="response",
        message=campaign_budget_service.MutateCampaignBudgetResult,
    )
    campaign_criterion_result = proto.Field(
        proto.MESSAGE,
        number=13,
        oneof="response",
        message=campaign_criterion_service.MutateCampaignCriterionResult,
    )
    campaign_draft_result = proto.Field(
        proto.MESSAGE,
        number=24,
        oneof="response",
        message=campaign_draft_service.MutateCampaignDraftResult,
    )
    campaign_experiment_result = proto.Field(
        proto.MESSAGE,
        number=25,
        oneof="response",
        message=campaign_experiment_service.MutateCampaignExperimentResult,
    )
    campaign_extension_setting_result = proto.Field(
        proto.MESSAGE,
        number=26,
        oneof="response",
        message=campaign_extension_setting_service.MutateCampaignExtensionSettingResult,
    )
    campaign_feed_result = proto.Field(
        proto.MESSAGE,
        number=27,
        oneof="response",
        message=campaign_feed_service.MutateCampaignFeedResult,
    )
    campaign_label_result = proto.Field(
        proto.MESSAGE,
        number=28,
        oneof="response",
        message=campaign_label_service.MutateCampaignLabelResult,
    )
    campaign_result = proto.Field(
        proto.MESSAGE,
        number=10,
        oneof="response",
        message=campaign_service.MutateCampaignResult,
    )
    campaign_shared_set_result = proto.Field(
        proto.MESSAGE,
        number=11,
        oneof="response",
        message=campaign_shared_set_service.MutateCampaignSharedSetResult,
    )
    conversion_action_result = proto.Field(
        proto.MESSAGE,
        number=12,
        oneof="response",
        message=conversion_action_service.MutateConversionActionResult,
    )
    conversion_custom_variable_result = proto.Field(
        proto.MESSAGE,
        number=55,
        oneof="response",
        message=conversion_custom_variable_service.MutateConversionCustomVariableResult,
    )
    customer_asset_result = proto.Field(
        proto.MESSAGE,
        number=57,
        oneof="response",
        message=customer_asset_service.MutateCustomerAssetResult,
    )
    customer_extension_setting_result = proto.Field(
        proto.MESSAGE,
        number=30,
        oneof="response",
        message=customer_extension_setting_service.MutateCustomerExtensionSettingResult,
    )
    customer_feed_result = proto.Field(
        proto.MESSAGE,
        number=31,
        oneof="response",
        message=customer_feed_service.MutateCustomerFeedResult,
    )
    customer_label_result = proto.Field(
        proto.MESSAGE,
        number=32,
        oneof="response",
        message=customer_label_service.MutateCustomerLabelResult,
    )
    customer_negative_criterion_result = proto.Field(
        proto.MESSAGE,
        number=34,
        oneof="response",
        message=customer_negative_criterion_service.MutateCustomerNegativeCriteriaResult,
    )
    customer_result = proto.Field(
        proto.MESSAGE,
        number=35,
        oneof="response",
        message=customer_service.MutateCustomerResult,
    )
    extension_feed_item_result = proto.Field(
        proto.MESSAGE,
        number=36,
        oneof="response",
        message=extension_feed_item_service.MutateExtensionFeedItemResult,
    )
    feed_item_result = proto.Field(
        proto.MESSAGE,
        number=37,
        oneof="response",
        message=feed_item_service.MutateFeedItemResult,
    )
    feed_item_set_result = proto.Field(
        proto.MESSAGE,
        number=53,
        oneof="response",
        message=feed_item_set_service.MutateFeedItemSetResult,
    )
    feed_item_set_link_result = proto.Field(
        proto.MESSAGE,
        number=54,
        oneof="response",
        message=feed_item_set_link_service.MutateFeedItemSetLinkResult,
    )
    feed_item_target_result = proto.Field(
        proto.MESSAGE,
        number=38,
        oneof="response",
        message=feed_item_target_service.MutateFeedItemTargetResult,
    )
    feed_mapping_result = proto.Field(
        proto.MESSAGE,
        number=39,
        oneof="response",
        message=feed_mapping_service.MutateFeedMappingResult,
    )
    feed_result = proto.Field(
        proto.MESSAGE,
        number=40,
        oneof="response",
        message=feed_service.MutateFeedResult,
    )
    keyword_plan_ad_group_result = proto.Field(
        proto.MESSAGE,
        number=44,
        oneof="response",
        message=keyword_plan_ad_group_service.MutateKeywordPlanAdGroupResult,
    )
    keyword_plan_campaign_result = proto.Field(
        proto.MESSAGE,
        number=45,
        oneof="response",
        message=keyword_plan_campaign_service.MutateKeywordPlanCampaignResult,
    )
    keyword_plan_ad_group_keyword_result = proto.Field(
        proto.MESSAGE,
        number=50,
        oneof="response",
        message=keyword_plan_ad_group_keyword_service.MutateKeywordPlanAdGroupKeywordResult,
    )
    keyword_plan_campaign_keyword_result = proto.Field(
        proto.MESSAGE,
        number=51,
        oneof="response",
        message=keyword_plan_campaign_keyword_service.MutateKeywordPlanCampaignKeywordResult,
    )
    keyword_plan_result = proto.Field(
        proto.MESSAGE,
        number=48,
        oneof="response",
        message=keyword_plan_service.MutateKeywordPlansResult,
    )
    label_result = proto.Field(
        proto.MESSAGE,
        number=41,
        oneof="response",
        message=label_service.MutateLabelResult,
    )
    media_file_result = proto.Field(
        proto.MESSAGE,
        number=42,
        oneof="response",
        message=media_file_service.MutateMediaFileResult,
    )
    remarketing_action_result = proto.Field(
        proto.MESSAGE,
        number=43,
        oneof="response",
        message=remarketing_action_service.MutateRemarketingActionResult,
    )
    shared_criterion_result = proto.Field(
        proto.MESSAGE,
        number=14,
        oneof="response",
        message=shared_criterion_service.MutateSharedCriterionResult,
    )
    shared_set_result = proto.Field(
        proto.MESSAGE,
        number=15,
        oneof="response",
        message=shared_set_service.MutateSharedSetResult,
    )
    user_list_result = proto.Field(
        proto.MESSAGE,
        number=16,
        oneof="response",
        message=user_list_service.MutateUserListResult,
    )


__all__ = tuple(sorted(__protobuf__.manifest))
