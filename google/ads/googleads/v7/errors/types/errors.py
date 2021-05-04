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

from google.ads.googleads.v7.common.types import policy as gagc_policy
from google.ads.googleads.v7.common.types import value
from google.ads.googleads.v7.enums.types import resource_limit_type
from google.ads.googleads.v7.errors.types import (
    access_invitation_error as gage_access_invitation_error,
)
from google.ads.googleads.v7.errors.types import (
    account_budget_proposal_error as gage_account_budget_proposal_error,
)
from google.ads.googleads.v7.errors.types import (
    account_link_error as gage_account_link_error,
)
from google.ads.googleads.v7.errors.types import (
    ad_customizer_error as gage_ad_customizer_error,
)
from google.ads.googleads.v7.errors.types import ad_error as gage_ad_error
from google.ads.googleads.v7.errors.types import (
    ad_group_ad_error as gage_ad_group_ad_error,
)
from google.ads.googleads.v7.errors.types import (
    ad_group_bid_modifier_error as gage_ad_group_bid_modifier_error,
)
from google.ads.googleads.v7.errors.types import (
    ad_group_criterion_error as gage_ad_group_criterion_error,
)
from google.ads.googleads.v7.errors.types import (
    ad_group_error as gage_ad_group_error,
)
from google.ads.googleads.v7.errors.types import (
    ad_group_feed_error as gage_ad_group_feed_error,
)
from google.ads.googleads.v7.errors.types import (
    ad_parameter_error as gage_ad_parameter_error,
)
from google.ads.googleads.v7.errors.types import (
    ad_sharing_error as gage_ad_sharing_error,
)
from google.ads.googleads.v7.errors.types import adx_error as gage_adx_error
from google.ads.googleads.v7.errors.types import asset_error as gage_asset_error
from google.ads.googleads.v7.errors.types import (
    asset_link_error as gage_asset_link_error,
)
from google.ads.googleads.v7.errors.types import (
    authentication_error as gage_authentication_error,
)
from google.ads.googleads.v7.errors.types import (
    authorization_error as gage_authorization_error,
)
from google.ads.googleads.v7.errors.types import (
    batch_job_error as gage_batch_job_error,
)
from google.ads.googleads.v7.errors.types import (
    bidding_error as gage_bidding_error,
)
from google.ads.googleads.v7.errors.types import (
    bidding_strategy_error as gage_bidding_strategy_error,
)
from google.ads.googleads.v7.errors.types import (
    billing_setup_error as gage_billing_setup_error,
)
from google.ads.googleads.v7.errors.types import (
    campaign_budget_error as gage_campaign_budget_error,
)
from google.ads.googleads.v7.errors.types import (
    campaign_criterion_error as gage_campaign_criterion_error,
)
from google.ads.googleads.v7.errors.types import (
    campaign_draft_error as gage_campaign_draft_error,
)
from google.ads.googleads.v7.errors.types import (
    campaign_error as gage_campaign_error,
)
from google.ads.googleads.v7.errors.types import (
    campaign_experiment_error as gage_campaign_experiment_error,
)
from google.ads.googleads.v7.errors.types import (
    campaign_feed_error as gage_campaign_feed_error,
)
from google.ads.googleads.v7.errors.types import (
    campaign_shared_set_error as gage_campaign_shared_set_error,
)
from google.ads.googleads.v7.errors.types import (
    change_event_error as gage_change_event_error,
)
from google.ads.googleads.v7.errors.types import (
    change_status_error as gage_change_status_error,
)
from google.ads.googleads.v7.errors.types import (
    collection_size_error as gage_collection_size_error,
)
from google.ads.googleads.v7.errors.types import (
    context_error as gage_context_error,
)
from google.ads.googleads.v7.errors.types import (
    conversion_action_error as gage_conversion_action_error,
)
from google.ads.googleads.v7.errors.types import (
    conversion_adjustment_upload_error as gage_conversion_adjustment_upload_error,
)
from google.ads.googleads.v7.errors.types import (
    conversion_custom_variable_error as gage_conversion_custom_variable_error,
)
from google.ads.googleads.v7.errors.types import (
    conversion_upload_error as gage_conversion_upload_error,
)
from google.ads.googleads.v7.errors.types import (
    country_code_error as gage_country_code_error,
)
from google.ads.googleads.v7.errors.types import (
    criterion_error as gage_criterion_error,
)
from google.ads.googleads.v7.errors.types import (
    currency_code_error as gage_currency_code_error,
)
from google.ads.googleads.v7.errors.types import (
    custom_audience_error as gage_custom_audience_error,
)
from google.ads.googleads.v7.errors.types import (
    custom_interest_error as gage_custom_interest_error,
)
from google.ads.googleads.v7.errors.types import (
    customer_client_link_error as gage_customer_client_link_error,
)
from google.ads.googleads.v7.errors.types import (
    customer_error as gage_customer_error,
)
from google.ads.googleads.v7.errors.types import (
    customer_feed_error as gage_customer_feed_error,
)
from google.ads.googleads.v7.errors.types import (
    customer_manager_link_error as gage_customer_manager_link_error,
)
from google.ads.googleads.v7.errors.types import (
    customer_user_access_error as gage_customer_user_access_error,
)
from google.ads.googleads.v7.errors.types import (
    database_error as gage_database_error,
)
from google.ads.googleads.v7.errors.types import date_error as gage_date_error
from google.ads.googleads.v7.errors.types import (
    date_range_error as gage_date_range_error,
)
from google.ads.googleads.v7.errors.types import (
    distinct_error as gage_distinct_error,
)
from google.ads.googleads.v7.errors.types import enum_error as gage_enum_error
from google.ads.googleads.v7.errors.types import (
    extension_feed_item_error as gage_extension_feed_item_error,
)
from google.ads.googleads.v7.errors.types import (
    extension_setting_error as gage_extension_setting_error,
)
from google.ads.googleads.v7.errors.types import (
    feed_attribute_reference_error as gage_feed_attribute_reference_error,
)
from google.ads.googleads.v7.errors.types import feed_error as gage_feed_error
from google.ads.googleads.v7.errors.types import (
    feed_item_error as gage_feed_item_error,
)
from google.ads.googleads.v7.errors.types import (
    feed_item_set_error as gage_feed_item_set_error,
)
from google.ads.googleads.v7.errors.types import (
    feed_item_set_link_error as gage_feed_item_set_link_error,
)
from google.ads.googleads.v7.errors.types import (
    feed_item_target_error as gage_feed_item_target_error,
)
from google.ads.googleads.v7.errors.types import (
    feed_item_validation_error as gage_feed_item_validation_error,
)
from google.ads.googleads.v7.errors.types import (
    feed_mapping_error as gage_feed_mapping_error,
)
from google.ads.googleads.v7.errors.types import field_error as gage_field_error
from google.ads.googleads.v7.errors.types import (
    field_mask_error as gage_field_mask_error,
)
from google.ads.googleads.v7.errors.types import (
    function_error as gage_function_error,
)
from google.ads.googleads.v7.errors.types import (
    function_parsing_error as gage_function_parsing_error,
)
from google.ads.googleads.v7.errors.types import (
    geo_target_constant_suggestion_error as gage_geo_target_constant_suggestion_error,
)
from google.ads.googleads.v7.errors.types import (
    header_error as gage_header_error,
)
from google.ads.googleads.v7.errors.types import id_error as gage_id_error
from google.ads.googleads.v7.errors.types import image_error as gage_image_error
from google.ads.googleads.v7.errors.types import (
    internal_error as gage_internal_error,
)
from google.ads.googleads.v7.errors.types import (
    invoice_error as gage_invoice_error,
)
from google.ads.googleads.v7.errors.types import (
    keyword_plan_ad_group_error as gage_keyword_plan_ad_group_error,
)
from google.ads.googleads.v7.errors.types import (
    keyword_plan_ad_group_keyword_error as gage_keyword_plan_ad_group_keyword_error,
)
from google.ads.googleads.v7.errors.types import (
    keyword_plan_campaign_error as gage_keyword_plan_campaign_error,
)
from google.ads.googleads.v7.errors.types import (
    keyword_plan_campaign_keyword_error as gage_keyword_plan_campaign_keyword_error,
)
from google.ads.googleads.v7.errors.types import (
    keyword_plan_error as gage_keyword_plan_error,
)
from google.ads.googleads.v7.errors.types import (
    keyword_plan_idea_error as gage_keyword_plan_idea_error,
)
from google.ads.googleads.v7.errors.types import label_error as gage_label_error
from google.ads.googleads.v7.errors.types import (
    language_code_error as gage_language_code_error,
)
from google.ads.googleads.v7.errors.types import (
    list_operation_error as gage_list_operation_error,
)
from google.ads.googleads.v7.errors.types import (
    manager_link_error as gage_manager_link_error,
)
from google.ads.googleads.v7.errors.types import (
    media_bundle_error as gage_media_bundle_error,
)
from google.ads.googleads.v7.errors.types import (
    media_file_error as gage_media_file_error,
)
from google.ads.googleads.v7.errors.types import (
    media_upload_error as gage_media_upload_error,
)
from google.ads.googleads.v7.errors.types import (
    multiplier_error as gage_multiplier_error,
)
from google.ads.googleads.v7.errors.types import (
    mutate_error as gage_mutate_error,
)
from google.ads.googleads.v7.errors.types import (
    new_resource_creation_error as gage_new_resource_creation_error,
)
from google.ads.googleads.v7.errors.types import (
    not_allowlisted_error as gage_not_allowlisted_error,
)
from google.ads.googleads.v7.errors.types import (
    not_empty_error as gage_not_empty_error,
)
from google.ads.googleads.v7.errors.types import null_error as gage_null_error
from google.ads.googleads.v7.errors.types import (
    offline_user_data_job_error as gage_offline_user_data_job_error,
)
from google.ads.googleads.v7.errors.types import (
    operation_access_denied_error as gage_operation_access_denied_error,
)
from google.ads.googleads.v7.errors.types import (
    operator_error as gage_operator_error,
)
from google.ads.googleads.v7.errors.types import (
    partial_failure_error as gage_partial_failure_error,
)
from google.ads.googleads.v7.errors.types import (
    payments_account_error as gage_payments_account_error,
)
from google.ads.googleads.v7.errors.types import (
    policy_finding_error as gage_policy_finding_error,
)
from google.ads.googleads.v7.errors.types import (
    policy_validation_parameter_error as gage_policy_validation_parameter_error,
)
from google.ads.googleads.v7.errors.types import (
    policy_violation_error as gage_policy_violation_error,
)
from google.ads.googleads.v7.errors.types import query_error as gage_query_error
from google.ads.googleads.v7.errors.types import quota_error as gage_quota_error
from google.ads.googleads.v7.errors.types import range_error as gage_range_error
from google.ads.googleads.v7.errors.types import (
    reach_plan_error as gage_reach_plan_error,
)
from google.ads.googleads.v7.errors.types import (
    recommendation_error as gage_recommendation_error,
)
from google.ads.googleads.v7.errors.types import (
    region_code_error as gage_region_code_error,
)
from google.ads.googleads.v7.errors.types import (
    request_error as gage_request_error,
)
from google.ads.googleads.v7.errors.types import (
    resource_access_denied_error as gage_resource_access_denied_error,
)
from google.ads.googleads.v7.errors.types import (
    resource_count_limit_exceeded_error as gage_resource_count_limit_exceeded_error,
)
from google.ads.googleads.v7.errors.types import (
    setting_error as gage_setting_error,
)
from google.ads.googleads.v7.errors.types import (
    shared_criterion_error as gage_shared_criterion_error,
)
from google.ads.googleads.v7.errors.types import (
    shared_set_error as gage_shared_set_error,
)
from google.ads.googleads.v7.errors.types import (
    size_limit_error as gage_size_limit_error,
)
from google.ads.googleads.v7.errors.types import (
    string_format_error as gage_string_format_error,
)
from google.ads.googleads.v7.errors.types import (
    string_length_error as gage_string_length_error,
)
from google.ads.googleads.v7.errors.types import (
    third_party_app_analytics_link_error as gage_third_party_app_analytics_link_error,
)
from google.ads.googleads.v7.errors.types import (
    time_zone_error as gage_time_zone_error,
)
from google.ads.googleads.v7.errors.types import (
    url_field_error as gage_url_field_error,
)
from google.ads.googleads.v7.errors.types import (
    user_data_error as gage_user_data_error,
)
from google.ads.googleads.v7.errors.types import (
    user_list_error as gage_user_list_error,
)
from google.ads.googleads.v7.errors.types import (
    youtube_video_registration_error as gage_youtube_video_registration_error,
)
from google.protobuf import duration_pb2 as duration  # type: ignore


__protobuf__ = proto.module(
    package="google.ads.googleads.v7.errors",
    marshal="google.ads.googleads.v7",
    manifest={
        "GoogleAdsFailure",
        "GoogleAdsError",
        "ErrorCode",
        "ErrorLocation",
        "ErrorDetails",
        "PolicyViolationDetails",
        "PolicyFindingDetails",
        "QuotaErrorDetails",
        "ResourceCountDetails",
    },
)


class GoogleAdsFailure(proto.Message):
    r"""Describes how a GoogleAds API call failed. It's returned
    inside google.rpc.Status.details when a call fails.

    Attributes:
        errors (Sequence[google.ads.googleads.v7.errors.types.GoogleAdsError]):
            The list of errors that occurred.
        request_id (str):
            The unique id of the request that is used for
            debugging purposes.
    """

    errors = proto.RepeatedField(
        proto.MESSAGE, number=1, message="GoogleAdsError",
    )
    request_id = proto.Field(proto.STRING, number=2,)


class GoogleAdsError(proto.Message):
    r"""GoogleAds-specific error.
    Attributes:
        error_code (google.ads.googleads.v7.errors.types.ErrorCode):
            An enum value that indicates which error
            occurred.
        message (str):
            A human-readable description of the error.
        trigger (google.ads.googleads.v7.common.types.Value):
            The value that triggered the error.
        location (google.ads.googleads.v7.errors.types.ErrorLocation):
            Describes the part of the request proto that
            caused the error.
        details (google.ads.googleads.v7.errors.types.ErrorDetails):
            Additional error details, which are returned
            by certain error codes. Most error codes do not
            include details.
    """

    error_code = proto.Field(proto.MESSAGE, number=1, message="ErrorCode",)
    message = proto.Field(proto.STRING, number=2,)
    trigger = proto.Field(proto.MESSAGE, number=3, message=value.Value,)
    location = proto.Field(proto.MESSAGE, number=4, message="ErrorLocation",)
    details = proto.Field(proto.MESSAGE, number=5, message="ErrorDetails",)


class ErrorCode(proto.Message):
    r"""The error reason represented by type and enum.
    Attributes:
        request_error (google.ads.googleads.v7.errors.types.RequestErrorEnum.RequestError):
            An error caused by the request
        bidding_strategy_error (google.ads.googleads.v7.errors.types.BiddingStrategyErrorEnum.BiddingStrategyError):
            An error with a Bidding Strategy mutate.
        url_field_error (google.ads.googleads.v7.errors.types.UrlFieldErrorEnum.UrlFieldError):
            An error with a URL field mutate.
        list_operation_error (google.ads.googleads.v7.errors.types.ListOperationErrorEnum.ListOperationError):
            An error with a list operation.
        query_error (google.ads.googleads.v7.errors.types.QueryErrorEnum.QueryError):
            An error with an AWQL query
        mutate_error (google.ads.googleads.v7.errors.types.MutateErrorEnum.MutateError):
            An error with a mutate
        field_mask_error (google.ads.googleads.v7.errors.types.FieldMaskErrorEnum.FieldMaskError):
            An error with a field mask
        authorization_error (google.ads.googleads.v7.errors.types.AuthorizationErrorEnum.AuthorizationError):
            An error encountered when trying to authorize
            a user.
        internal_error (google.ads.googleads.v7.errors.types.InternalErrorEnum.InternalError):
            An unexpected server-side error.
        quota_error (google.ads.googleads.v7.errors.types.QuotaErrorEnum.QuotaError):
            An error with the amonut of quota remaining.
        ad_error (google.ads.googleads.v7.errors.types.AdErrorEnum.AdError):
            An error with an Ad Group Ad mutate.
        ad_group_error (google.ads.googleads.v7.errors.types.AdGroupErrorEnum.AdGroupError):
            An error with an Ad Group mutate.
        campaign_budget_error (google.ads.googleads.v7.errors.types.CampaignBudgetErrorEnum.CampaignBudgetError):
            An error with a Campaign Budget mutate.
        campaign_error (google.ads.googleads.v7.errors.types.CampaignErrorEnum.CampaignError):
            An error with a Campaign mutate.
        authentication_error (google.ads.googleads.v7.errors.types.AuthenticationErrorEnum.AuthenticationError):
            Indicates failure to properly authenticate
            user.
        ad_group_criterion_error (google.ads.googleads.v7.errors.types.AdGroupCriterionErrorEnum.AdGroupCriterionError):
            Indicates failure to properly authenticate
            user.
        ad_customizer_error (google.ads.googleads.v7.errors.types.AdCustomizerErrorEnum.AdCustomizerError):
            The reasons for the ad customizer error
        ad_group_ad_error (google.ads.googleads.v7.errors.types.AdGroupAdErrorEnum.AdGroupAdError):
            The reasons for the ad group ad error
        ad_sharing_error (google.ads.googleads.v7.errors.types.AdSharingErrorEnum.AdSharingError):
            The reasons for the ad sharing error
        adx_error (google.ads.googleads.v7.errors.types.AdxErrorEnum.AdxError):
            The reasons for the adx error
        asset_error (google.ads.googleads.v7.errors.types.AssetErrorEnum.AssetError):
            The reasons for the asset error
        bidding_error (google.ads.googleads.v7.errors.types.BiddingErrorEnum.BiddingError):
            The reasons for the bidding errors
        campaign_criterion_error (google.ads.googleads.v7.errors.types.CampaignCriterionErrorEnum.CampaignCriterionError):
            The reasons for the campaign criterion error
        collection_size_error (google.ads.googleads.v7.errors.types.CollectionSizeErrorEnum.CollectionSizeError):
            The reasons for the collection size error
        country_code_error (google.ads.googleads.v7.errors.types.CountryCodeErrorEnum.CountryCodeError):
            The reasons for the country code error
        criterion_error (google.ads.googleads.v7.errors.types.CriterionErrorEnum.CriterionError):
            The reasons for the criterion error
        customer_error (google.ads.googleads.v7.errors.types.CustomerErrorEnum.CustomerError):
            The reasons for the customer error
        date_error (google.ads.googleads.v7.errors.types.DateErrorEnum.DateError):
            The reasons for the date error
        date_range_error (google.ads.googleads.v7.errors.types.DateRangeErrorEnum.DateRangeError):
            The reasons for the date range error
        distinct_error (google.ads.googleads.v7.errors.types.DistinctErrorEnum.DistinctError):
            The reasons for the distinct error
        feed_attribute_reference_error (google.ads.googleads.v7.errors.types.FeedAttributeReferenceErrorEnum.FeedAttributeReferenceError):
            The reasons for the feed attribute reference
            error
        function_error (google.ads.googleads.v7.errors.types.FunctionErrorEnum.FunctionError):
            The reasons for the function error
        function_parsing_error (google.ads.googleads.v7.errors.types.FunctionParsingErrorEnum.FunctionParsingError):
            The reasons for the function parsing error
        id_error (google.ads.googleads.v7.errors.types.IdErrorEnum.IdError):
            The reasons for the id error
        image_error (google.ads.googleads.v7.errors.types.ImageErrorEnum.ImageError):
            The reasons for the image error
        language_code_error (google.ads.googleads.v7.errors.types.LanguageCodeErrorEnum.LanguageCodeError):
            The reasons for the language code error
        media_bundle_error (google.ads.googleads.v7.errors.types.MediaBundleErrorEnum.MediaBundleError):
            The reasons for the media bundle error
        media_upload_error (google.ads.googleads.v7.errors.types.MediaUploadErrorEnum.MediaUploadError):
            The reasons for media uploading errors.
        media_file_error (google.ads.googleads.v7.errors.types.MediaFileErrorEnum.MediaFileError):
            The reasons for the media file error
        multiplier_error (google.ads.googleads.v7.errors.types.MultiplierErrorEnum.MultiplierError):
            The reasons for the multiplier error
        new_resource_creation_error (google.ads.googleads.v7.errors.types.NewResourceCreationErrorEnum.NewResourceCreationError):
            The reasons for the new resource creation
            error
        not_empty_error (google.ads.googleads.v7.errors.types.NotEmptyErrorEnum.NotEmptyError):
            The reasons for the not empty error
        null_error (google.ads.googleads.v7.errors.types.NullErrorEnum.NullError):
            The reasons for the null error
        operator_error (google.ads.googleads.v7.errors.types.OperatorErrorEnum.OperatorError):
            The reasons for the operator error
        range_error (google.ads.googleads.v7.errors.types.RangeErrorEnum.RangeError):
            The reasons for the range error
        recommendation_error (google.ads.googleads.v7.errors.types.RecommendationErrorEnum.RecommendationError):
            The reasons for error in applying a
            recommendation
        region_code_error (google.ads.googleads.v7.errors.types.RegionCodeErrorEnum.RegionCodeError):
            The reasons for the region code error
        setting_error (google.ads.googleads.v7.errors.types.SettingErrorEnum.SettingError):
            The reasons for the setting error
        string_format_error (google.ads.googleads.v7.errors.types.StringFormatErrorEnum.StringFormatError):
            The reasons for the string format error
        string_length_error (google.ads.googleads.v7.errors.types.StringLengthErrorEnum.StringLengthError):
            The reasons for the string length error
        operation_access_denied_error (google.ads.googleads.v7.errors.types.OperationAccessDeniedErrorEnum.OperationAccessDeniedError):
            The reasons for the operation access denied
            error
        resource_access_denied_error (google.ads.googleads.v7.errors.types.ResourceAccessDeniedErrorEnum.ResourceAccessDeniedError):
            The reasons for the resource access denied
            error
        resource_count_limit_exceeded_error (google.ads.googleads.v7.errors.types.ResourceCountLimitExceededErrorEnum.ResourceCountLimitExceededError):
            The reasons for the resource count limit
            exceeded error
        youtube_video_registration_error (google.ads.googleads.v7.errors.types.YoutubeVideoRegistrationErrorEnum.YoutubeVideoRegistrationError):
            The reasons for YouTube video registration
            errors.
        ad_group_bid_modifier_error (google.ads.googleads.v7.errors.types.AdGroupBidModifierErrorEnum.AdGroupBidModifierError):
            The reasons for the ad group bid modifier
            error
        context_error (google.ads.googleads.v7.errors.types.ContextErrorEnum.ContextError):
            The reasons for the context error
        field_error (google.ads.googleads.v7.errors.types.FieldErrorEnum.FieldError):
            The reasons for the field error
        shared_set_error (google.ads.googleads.v7.errors.types.SharedSetErrorEnum.SharedSetError):
            The reasons for the shared set error
        shared_criterion_error (google.ads.googleads.v7.errors.types.SharedCriterionErrorEnum.SharedCriterionError):
            The reasons for the shared criterion error
        campaign_shared_set_error (google.ads.googleads.v7.errors.types.CampaignSharedSetErrorEnum.CampaignSharedSetError):
            The reasons for the campaign shared set error
        conversion_action_error (google.ads.googleads.v7.errors.types.ConversionActionErrorEnum.ConversionActionError):
            The reasons for the conversion action error
        conversion_adjustment_upload_error (google.ads.googleads.v7.errors.types.ConversionAdjustmentUploadErrorEnum.ConversionAdjustmentUploadError):
            The reasons for the conversion adjustment
            upload error
        conversion_custom_variable_error (google.ads.googleads.v7.errors.types.ConversionCustomVariableErrorEnum.ConversionCustomVariableError):
            The reasons for the conversion custom
            variable error
        conversion_upload_error (google.ads.googleads.v7.errors.types.ConversionUploadErrorEnum.ConversionUploadError):
            The reasons for the conversion upload error
        header_error (google.ads.googleads.v7.errors.types.HeaderErrorEnum.HeaderError):
            The reasons for the header error.
        database_error (google.ads.googleads.v7.errors.types.DatabaseErrorEnum.DatabaseError):
            The reasons for the database error.
        policy_finding_error (google.ads.googleads.v7.errors.types.PolicyFindingErrorEnum.PolicyFindingError):
            The reasons for the policy finding error.
        enum_error (google.ads.googleads.v7.errors.types.EnumErrorEnum.EnumError):
            The reason for enum error.
        keyword_plan_error (google.ads.googleads.v7.errors.types.KeywordPlanErrorEnum.KeywordPlanError):
            The reason for keyword plan error.
        keyword_plan_campaign_error (google.ads.googleads.v7.errors.types.KeywordPlanCampaignErrorEnum.KeywordPlanCampaignError):
            The reason for keyword plan campaign error.
        keyword_plan_campaign_keyword_error (google.ads.googleads.v7.errors.types.KeywordPlanCampaignKeywordErrorEnum.KeywordPlanCampaignKeywordError):
            The reason for keyword plan campaign keyword
            error.
        keyword_plan_ad_group_error (google.ads.googleads.v7.errors.types.KeywordPlanAdGroupErrorEnum.KeywordPlanAdGroupError):
            The reason for keyword plan ad group error.
        keyword_plan_ad_group_keyword_error (google.ads.googleads.v7.errors.types.KeywordPlanAdGroupKeywordErrorEnum.KeywordPlanAdGroupKeywordError):
            The reason for keyword plan ad group keyword
            error.
        keyword_plan_idea_error (google.ads.googleads.v7.errors.types.KeywordPlanIdeaErrorEnum.KeywordPlanIdeaError):
            The reason for keyword idea error.
        account_budget_proposal_error (google.ads.googleads.v7.errors.types.AccountBudgetProposalErrorEnum.AccountBudgetProposalError):
            The reasons for account budget proposal
            errors.
        user_list_error (google.ads.googleads.v7.errors.types.UserListErrorEnum.UserListError):
            The reasons for the user list error
        change_event_error (google.ads.googleads.v7.errors.types.ChangeEventErrorEnum.ChangeEventError):
            The reasons for the change event error
        change_status_error (google.ads.googleads.v7.errors.types.ChangeStatusErrorEnum.ChangeStatusError):
            The reasons for the change status error
        feed_error (google.ads.googleads.v7.errors.types.FeedErrorEnum.FeedError):
            The reasons for the feed error
        geo_target_constant_suggestion_error (google.ads.googleads.v7.errors.types.GeoTargetConstantSuggestionErrorEnum.GeoTargetConstantSuggestionError):
            The reasons for the geo target constant
            suggestion error.
        campaign_draft_error (google.ads.googleads.v7.errors.types.CampaignDraftErrorEnum.CampaignDraftError):
            The reasons for the campaign draft error
        feed_item_error (google.ads.googleads.v7.errors.types.FeedItemErrorEnum.FeedItemError):
            The reasons for the feed item error
        label_error (google.ads.googleads.v7.errors.types.LabelErrorEnum.LabelError):
            The reason for the label error.
        billing_setup_error (google.ads.googleads.v7.errors.types.BillingSetupErrorEnum.BillingSetupError):
            The reasons for the billing setup error
        customer_client_link_error (google.ads.googleads.v7.errors.types.CustomerClientLinkErrorEnum.CustomerClientLinkError):
            The reasons for the customer client link
            error
        customer_manager_link_error (google.ads.googleads.v7.errors.types.CustomerManagerLinkErrorEnum.CustomerManagerLinkError):
            The reasons for the customer manager link
            error
        feed_mapping_error (google.ads.googleads.v7.errors.types.FeedMappingErrorEnum.FeedMappingError):
            The reasons for the feed mapping error
        customer_feed_error (google.ads.googleads.v7.errors.types.CustomerFeedErrorEnum.CustomerFeedError):
            The reasons for the customer feed error
        ad_group_feed_error (google.ads.googleads.v7.errors.types.AdGroupFeedErrorEnum.AdGroupFeedError):
            The reasons for the ad group feed error
        campaign_feed_error (google.ads.googleads.v7.errors.types.CampaignFeedErrorEnum.CampaignFeedError):
            The reasons for the campaign feed error
        custom_interest_error (google.ads.googleads.v7.errors.types.CustomInterestErrorEnum.CustomInterestError):
            The reasons for the custom interest error
        campaign_experiment_error (google.ads.googleads.v7.errors.types.CampaignExperimentErrorEnum.CampaignExperimentError):
            The reasons for the campaign experiment error
        extension_feed_item_error (google.ads.googleads.v7.errors.types.ExtensionFeedItemErrorEnum.ExtensionFeedItemError):
            The reasons for the extension feed item error
        ad_parameter_error (google.ads.googleads.v7.errors.types.AdParameterErrorEnum.AdParameterError):
            The reasons for the ad parameter error
        feed_item_validation_error (google.ads.googleads.v7.errors.types.FeedItemValidationErrorEnum.FeedItemValidationError):
            The reasons for the feed item validation
            error
        extension_setting_error (google.ads.googleads.v7.errors.types.ExtensionSettingErrorEnum.ExtensionSettingError):
            The reasons for the extension setting error
        feed_item_set_error (google.ads.googleads.v7.errors.types.FeedItemSetErrorEnum.FeedItemSetError):
            The reasons for the feed item set error
        feed_item_set_link_error (google.ads.googleads.v7.errors.types.FeedItemSetLinkErrorEnum.FeedItemSetLinkError):
            The reasons for the feed item set link error
        feed_item_target_error (google.ads.googleads.v7.errors.types.FeedItemTargetErrorEnum.FeedItemTargetError):
            The reasons for the feed item target error
        policy_violation_error (google.ads.googleads.v7.errors.types.PolicyViolationErrorEnum.PolicyViolationError):
            The reasons for the policy violation error
        partial_failure_error (google.ads.googleads.v7.errors.types.PartialFailureErrorEnum.PartialFailureError):
            The reasons for the mutate job error
        policy_validation_parameter_error (google.ads.googleads.v7.errors.types.PolicyValidationParameterErrorEnum.PolicyValidationParameterError):
            The reasons for the policy validation
            parameter error
        size_limit_error (google.ads.googleads.v7.errors.types.SizeLimitErrorEnum.SizeLimitError):
            The reasons for the size limit error
        offline_user_data_job_error (google.ads.googleads.v7.errors.types.OfflineUserDataJobErrorEnum.OfflineUserDataJobError):
            The reasons for the offline user data job
            error.
        not_allowlisted_error (google.ads.googleads.v7.errors.types.NotAllowlistedErrorEnum.NotAllowlistedError):
            The reasons for the not allowlisted error
        manager_link_error (google.ads.googleads.v7.errors.types.ManagerLinkErrorEnum.ManagerLinkError):
            The reasons for the manager link error
        currency_code_error (google.ads.googleads.v7.errors.types.CurrencyCodeErrorEnum.CurrencyCodeError):
            The reasons for the currency code error
        access_invitation_error (google.ads.googleads.v7.errors.types.AccessInvitationErrorEnum.AccessInvitationError):
            The reasons for the access invitation error
        reach_plan_error (google.ads.googleads.v7.errors.types.ReachPlanErrorEnum.ReachPlanError):
            The reasons for the reach plan error
        invoice_error (google.ads.googleads.v7.errors.types.InvoiceErrorEnum.InvoiceError):
            The reasons for the invoice error
        payments_account_error (google.ads.googleads.v7.errors.types.PaymentsAccountErrorEnum.PaymentsAccountError):
            The reasons for errors in payments accounts
            service
        time_zone_error (google.ads.googleads.v7.errors.types.TimeZoneErrorEnum.TimeZoneError):
            The reasons for the time zone error
        asset_link_error (google.ads.googleads.v7.errors.types.AssetLinkErrorEnum.AssetLinkError):
            The reasons for the asset link error
        user_data_error (google.ads.googleads.v7.errors.types.UserDataErrorEnum.UserDataError):
            The reasons for the user data error.
        batch_job_error (google.ads.googleads.v7.errors.types.BatchJobErrorEnum.BatchJobError):
            The reasons for the batch job error
        account_link_error (google.ads.googleads.v7.errors.types.AccountLinkErrorEnum.AccountLinkError):
            The reasons for the account link status
            change error
        third_party_app_analytics_link_error (google.ads.googleads.v7.errors.types.ThirdPartyAppAnalyticsLinkErrorEnum.ThirdPartyAppAnalyticsLinkError):
            The reasons for the third party app analytics
            link mutate error
        customer_user_access_error (google.ads.googleads.v7.errors.types.CustomerUserAccessErrorEnum.CustomerUserAccessError):
            The reasons for the customer user access
            mutate error
        custom_audience_error (google.ads.googleads.v7.errors.types.CustomAudienceErrorEnum.CustomAudienceError):
            The reasons for the custom audience error
    """

    request_error = proto.Field(
        proto.ENUM,
        number=1,
        oneof="error_code",
        enum=gage_request_error.RequestErrorEnum.RequestError,
    )
    bidding_strategy_error = proto.Field(
        proto.ENUM,
        number=2,
        oneof="error_code",
        enum=gage_bidding_strategy_error.BiddingStrategyErrorEnum.BiddingStrategyError,
    )
    url_field_error = proto.Field(
        proto.ENUM,
        number=3,
        oneof="error_code",
        enum=gage_url_field_error.UrlFieldErrorEnum.UrlFieldError,
    )
    list_operation_error = proto.Field(
        proto.ENUM,
        number=4,
        oneof="error_code",
        enum=gage_list_operation_error.ListOperationErrorEnum.ListOperationError,
    )
    query_error = proto.Field(
        proto.ENUM,
        number=5,
        oneof="error_code",
        enum=gage_query_error.QueryErrorEnum.QueryError,
    )
    mutate_error = proto.Field(
        proto.ENUM,
        number=7,
        oneof="error_code",
        enum=gage_mutate_error.MutateErrorEnum.MutateError,
    )
    field_mask_error = proto.Field(
        proto.ENUM,
        number=8,
        oneof="error_code",
        enum=gage_field_mask_error.FieldMaskErrorEnum.FieldMaskError,
    )
    authorization_error = proto.Field(
        proto.ENUM,
        number=9,
        oneof="error_code",
        enum=gage_authorization_error.AuthorizationErrorEnum.AuthorizationError,
    )
    internal_error = proto.Field(
        proto.ENUM,
        number=10,
        oneof="error_code",
        enum=gage_internal_error.InternalErrorEnum.InternalError,
    )
    quota_error = proto.Field(
        proto.ENUM,
        number=11,
        oneof="error_code",
        enum=gage_quota_error.QuotaErrorEnum.QuotaError,
    )
    ad_error = proto.Field(
        proto.ENUM,
        number=12,
        oneof="error_code",
        enum=gage_ad_error.AdErrorEnum.AdError,
    )
    ad_group_error = proto.Field(
        proto.ENUM,
        number=13,
        oneof="error_code",
        enum=gage_ad_group_error.AdGroupErrorEnum.AdGroupError,
    )
    campaign_budget_error = proto.Field(
        proto.ENUM,
        number=14,
        oneof="error_code",
        enum=gage_campaign_budget_error.CampaignBudgetErrorEnum.CampaignBudgetError,
    )
    campaign_error = proto.Field(
        proto.ENUM,
        number=15,
        oneof="error_code",
        enum=gage_campaign_error.CampaignErrorEnum.CampaignError,
    )
    authentication_error = proto.Field(
        proto.ENUM,
        number=17,
        oneof="error_code",
        enum=gage_authentication_error.AuthenticationErrorEnum.AuthenticationError,
    )
    ad_group_criterion_error = proto.Field(
        proto.ENUM,
        number=18,
        oneof="error_code",
        enum=gage_ad_group_criterion_error.AdGroupCriterionErrorEnum.AdGroupCriterionError,
    )
    ad_customizer_error = proto.Field(
        proto.ENUM,
        number=19,
        oneof="error_code",
        enum=gage_ad_customizer_error.AdCustomizerErrorEnum.AdCustomizerError,
    )
    ad_group_ad_error = proto.Field(
        proto.ENUM,
        number=21,
        oneof="error_code",
        enum=gage_ad_group_ad_error.AdGroupAdErrorEnum.AdGroupAdError,
    )
    ad_sharing_error = proto.Field(
        proto.ENUM,
        number=24,
        oneof="error_code",
        enum=gage_ad_sharing_error.AdSharingErrorEnum.AdSharingError,
    )
    adx_error = proto.Field(
        proto.ENUM,
        number=25,
        oneof="error_code",
        enum=gage_adx_error.AdxErrorEnum.AdxError,
    )
    asset_error = proto.Field(
        proto.ENUM,
        number=107,
        oneof="error_code",
        enum=gage_asset_error.AssetErrorEnum.AssetError,
    )
    bidding_error = proto.Field(
        proto.ENUM,
        number=26,
        oneof="error_code",
        enum=gage_bidding_error.BiddingErrorEnum.BiddingError,
    )
    campaign_criterion_error = proto.Field(
        proto.ENUM,
        number=29,
        oneof="error_code",
        enum=gage_campaign_criterion_error.CampaignCriterionErrorEnum.CampaignCriterionError,
    )
    collection_size_error = proto.Field(
        proto.ENUM,
        number=31,
        oneof="error_code",
        enum=gage_collection_size_error.CollectionSizeErrorEnum.CollectionSizeError,
    )
    country_code_error = proto.Field(
        proto.ENUM,
        number=109,
        oneof="error_code",
        enum=gage_country_code_error.CountryCodeErrorEnum.CountryCodeError,
    )
    criterion_error = proto.Field(
        proto.ENUM,
        number=32,
        oneof="error_code",
        enum=gage_criterion_error.CriterionErrorEnum.CriterionError,
    )
    customer_error = proto.Field(
        proto.ENUM,
        number=90,
        oneof="error_code",
        enum=gage_customer_error.CustomerErrorEnum.CustomerError,
    )
    date_error = proto.Field(
        proto.ENUM,
        number=33,
        oneof="error_code",
        enum=gage_date_error.DateErrorEnum.DateError,
    )
    date_range_error = proto.Field(
        proto.ENUM,
        number=34,
        oneof="error_code",
        enum=gage_date_range_error.DateRangeErrorEnum.DateRangeError,
    )
    distinct_error = proto.Field(
        proto.ENUM,
        number=35,
        oneof="error_code",
        enum=gage_distinct_error.DistinctErrorEnum.DistinctError,
    )
    feed_attribute_reference_error = proto.Field(
        proto.ENUM,
        number=36,
        oneof="error_code",
        enum=gage_feed_attribute_reference_error.FeedAttributeReferenceErrorEnum.FeedAttributeReferenceError,
    )
    function_error = proto.Field(
        proto.ENUM,
        number=37,
        oneof="error_code",
        enum=gage_function_error.FunctionErrorEnum.FunctionError,
    )
    function_parsing_error = proto.Field(
        proto.ENUM,
        number=38,
        oneof="error_code",
        enum=gage_function_parsing_error.FunctionParsingErrorEnum.FunctionParsingError,
    )
    id_error = proto.Field(
        proto.ENUM,
        number=39,
        oneof="error_code",
        enum=gage_id_error.IdErrorEnum.IdError,
    )
    image_error = proto.Field(
        proto.ENUM,
        number=40,
        oneof="error_code",
        enum=gage_image_error.ImageErrorEnum.ImageError,
    )
    language_code_error = proto.Field(
        proto.ENUM,
        number=110,
        oneof="error_code",
        enum=gage_language_code_error.LanguageCodeErrorEnum.LanguageCodeError,
    )
    media_bundle_error = proto.Field(
        proto.ENUM,
        number=42,
        oneof="error_code",
        enum=gage_media_bundle_error.MediaBundleErrorEnum.MediaBundleError,
    )
    media_upload_error = proto.Field(
        proto.ENUM,
        number=116,
        oneof="error_code",
        enum=gage_media_upload_error.MediaUploadErrorEnum.MediaUploadError,
    )
    media_file_error = proto.Field(
        proto.ENUM,
        number=86,
        oneof="error_code",
        enum=gage_media_file_error.MediaFileErrorEnum.MediaFileError,
    )
    multiplier_error = proto.Field(
        proto.ENUM,
        number=44,
        oneof="error_code",
        enum=gage_multiplier_error.MultiplierErrorEnum.MultiplierError,
    )
    new_resource_creation_error = proto.Field(
        proto.ENUM,
        number=45,
        oneof="error_code",
        enum=gage_new_resource_creation_error.NewResourceCreationErrorEnum.NewResourceCreationError,
    )
    not_empty_error = proto.Field(
        proto.ENUM,
        number=46,
        oneof="error_code",
        enum=gage_not_empty_error.NotEmptyErrorEnum.NotEmptyError,
    )
    null_error = proto.Field(
        proto.ENUM,
        number=47,
        oneof="error_code",
        enum=gage_null_error.NullErrorEnum.NullError,
    )
    operator_error = proto.Field(
        proto.ENUM,
        number=48,
        oneof="error_code",
        enum=gage_operator_error.OperatorErrorEnum.OperatorError,
    )
    range_error = proto.Field(
        proto.ENUM,
        number=49,
        oneof="error_code",
        enum=gage_range_error.RangeErrorEnum.RangeError,
    )
    recommendation_error = proto.Field(
        proto.ENUM,
        number=58,
        oneof="error_code",
        enum=gage_recommendation_error.RecommendationErrorEnum.RecommendationError,
    )
    region_code_error = proto.Field(
        proto.ENUM,
        number=51,
        oneof="error_code",
        enum=gage_region_code_error.RegionCodeErrorEnum.RegionCodeError,
    )
    setting_error = proto.Field(
        proto.ENUM,
        number=52,
        oneof="error_code",
        enum=gage_setting_error.SettingErrorEnum.SettingError,
    )
    string_format_error = proto.Field(
        proto.ENUM,
        number=53,
        oneof="error_code",
        enum=gage_string_format_error.StringFormatErrorEnum.StringFormatError,
    )
    string_length_error = proto.Field(
        proto.ENUM,
        number=54,
        oneof="error_code",
        enum=gage_string_length_error.StringLengthErrorEnum.StringLengthError,
    )
    operation_access_denied_error = proto.Field(
        proto.ENUM,
        number=55,
        oneof="error_code",
        enum=gage_operation_access_denied_error.OperationAccessDeniedErrorEnum.OperationAccessDeniedError,
    )
    resource_access_denied_error = proto.Field(
        proto.ENUM,
        number=56,
        oneof="error_code",
        enum=gage_resource_access_denied_error.ResourceAccessDeniedErrorEnum.ResourceAccessDeniedError,
    )
    resource_count_limit_exceeded_error = proto.Field(
        proto.ENUM,
        number=57,
        oneof="error_code",
        enum=gage_resource_count_limit_exceeded_error.ResourceCountLimitExceededErrorEnum.ResourceCountLimitExceededError,
    )
    youtube_video_registration_error = proto.Field(
        proto.ENUM,
        number=117,
        oneof="error_code",
        enum=gage_youtube_video_registration_error.YoutubeVideoRegistrationErrorEnum.YoutubeVideoRegistrationError,
    )
    ad_group_bid_modifier_error = proto.Field(
        proto.ENUM,
        number=59,
        oneof="error_code",
        enum=gage_ad_group_bid_modifier_error.AdGroupBidModifierErrorEnum.AdGroupBidModifierError,
    )
    context_error = proto.Field(
        proto.ENUM,
        number=60,
        oneof="error_code",
        enum=gage_context_error.ContextErrorEnum.ContextError,
    )
    field_error = proto.Field(
        proto.ENUM,
        number=61,
        oneof="error_code",
        enum=gage_field_error.FieldErrorEnum.FieldError,
    )
    shared_set_error = proto.Field(
        proto.ENUM,
        number=62,
        oneof="error_code",
        enum=gage_shared_set_error.SharedSetErrorEnum.SharedSetError,
    )
    shared_criterion_error = proto.Field(
        proto.ENUM,
        number=63,
        oneof="error_code",
        enum=gage_shared_criterion_error.SharedCriterionErrorEnum.SharedCriterionError,
    )
    campaign_shared_set_error = proto.Field(
        proto.ENUM,
        number=64,
        oneof="error_code",
        enum=gage_campaign_shared_set_error.CampaignSharedSetErrorEnum.CampaignSharedSetError,
    )
    conversion_action_error = proto.Field(
        proto.ENUM,
        number=65,
        oneof="error_code",
        enum=gage_conversion_action_error.ConversionActionErrorEnum.ConversionActionError,
    )
    conversion_adjustment_upload_error = proto.Field(
        proto.ENUM,
        number=115,
        oneof="error_code",
        enum=gage_conversion_adjustment_upload_error.ConversionAdjustmentUploadErrorEnum.ConversionAdjustmentUploadError,
    )
    conversion_custom_variable_error = proto.Field(
        proto.ENUM,
        number=143,
        oneof="error_code",
        enum=gage_conversion_custom_variable_error.ConversionCustomVariableErrorEnum.ConversionCustomVariableError,
    )
    conversion_upload_error = proto.Field(
        proto.ENUM,
        number=111,
        oneof="error_code",
        enum=gage_conversion_upload_error.ConversionUploadErrorEnum.ConversionUploadError,
    )
    header_error = proto.Field(
        proto.ENUM,
        number=66,
        oneof="error_code",
        enum=gage_header_error.HeaderErrorEnum.HeaderError,
    )
    database_error = proto.Field(
        proto.ENUM,
        number=67,
        oneof="error_code",
        enum=gage_database_error.DatabaseErrorEnum.DatabaseError,
    )
    policy_finding_error = proto.Field(
        proto.ENUM,
        number=68,
        oneof="error_code",
        enum=gage_policy_finding_error.PolicyFindingErrorEnum.PolicyFindingError,
    )
    enum_error = proto.Field(
        proto.ENUM,
        number=70,
        oneof="error_code",
        enum=gage_enum_error.EnumErrorEnum.EnumError,
    )
    keyword_plan_error = proto.Field(
        proto.ENUM,
        number=71,
        oneof="error_code",
        enum=gage_keyword_plan_error.KeywordPlanErrorEnum.KeywordPlanError,
    )
    keyword_plan_campaign_error = proto.Field(
        proto.ENUM,
        number=72,
        oneof="error_code",
        enum=gage_keyword_plan_campaign_error.KeywordPlanCampaignErrorEnum.KeywordPlanCampaignError,
    )
    keyword_plan_campaign_keyword_error = proto.Field(
        proto.ENUM,
        number=132,
        oneof="error_code",
        enum=gage_keyword_plan_campaign_keyword_error.KeywordPlanCampaignKeywordErrorEnum.KeywordPlanCampaignKeywordError,
    )
    keyword_plan_ad_group_error = proto.Field(
        proto.ENUM,
        number=74,
        oneof="error_code",
        enum=gage_keyword_plan_ad_group_error.KeywordPlanAdGroupErrorEnum.KeywordPlanAdGroupError,
    )
    keyword_plan_ad_group_keyword_error = proto.Field(
        proto.ENUM,
        number=133,
        oneof="error_code",
        enum=gage_keyword_plan_ad_group_keyword_error.KeywordPlanAdGroupKeywordErrorEnum.KeywordPlanAdGroupKeywordError,
    )
    keyword_plan_idea_error = proto.Field(
        proto.ENUM,
        number=76,
        oneof="error_code",
        enum=gage_keyword_plan_idea_error.KeywordPlanIdeaErrorEnum.KeywordPlanIdeaError,
    )
    account_budget_proposal_error = proto.Field(
        proto.ENUM,
        number=77,
        oneof="error_code",
        enum=gage_account_budget_proposal_error.AccountBudgetProposalErrorEnum.AccountBudgetProposalError,
    )
    user_list_error = proto.Field(
        proto.ENUM,
        number=78,
        oneof="error_code",
        enum=gage_user_list_error.UserListErrorEnum.UserListError,
    )
    change_event_error = proto.Field(
        proto.ENUM,
        number=136,
        oneof="error_code",
        enum=gage_change_event_error.ChangeEventErrorEnum.ChangeEventError,
    )
    change_status_error = proto.Field(
        proto.ENUM,
        number=79,
        oneof="error_code",
        enum=gage_change_status_error.ChangeStatusErrorEnum.ChangeStatusError,
    )
    feed_error = proto.Field(
        proto.ENUM,
        number=80,
        oneof="error_code",
        enum=gage_feed_error.FeedErrorEnum.FeedError,
    )
    geo_target_constant_suggestion_error = proto.Field(
        proto.ENUM,
        number=81,
        oneof="error_code",
        enum=gage_geo_target_constant_suggestion_error.GeoTargetConstantSuggestionErrorEnum.GeoTargetConstantSuggestionError,
    )
    campaign_draft_error = proto.Field(
        proto.ENUM,
        number=82,
        oneof="error_code",
        enum=gage_campaign_draft_error.CampaignDraftErrorEnum.CampaignDraftError,
    )
    feed_item_error = proto.Field(
        proto.ENUM,
        number=83,
        oneof="error_code",
        enum=gage_feed_item_error.FeedItemErrorEnum.FeedItemError,
    )
    label_error = proto.Field(
        proto.ENUM,
        number=84,
        oneof="error_code",
        enum=gage_label_error.LabelErrorEnum.LabelError,
    )
    billing_setup_error = proto.Field(
        proto.ENUM,
        number=87,
        oneof="error_code",
        enum=gage_billing_setup_error.BillingSetupErrorEnum.BillingSetupError,
    )
    customer_client_link_error = proto.Field(
        proto.ENUM,
        number=88,
        oneof="error_code",
        enum=gage_customer_client_link_error.CustomerClientLinkErrorEnum.CustomerClientLinkError,
    )
    customer_manager_link_error = proto.Field(
        proto.ENUM,
        number=91,
        oneof="error_code",
        enum=gage_customer_manager_link_error.CustomerManagerLinkErrorEnum.CustomerManagerLinkError,
    )
    feed_mapping_error = proto.Field(
        proto.ENUM,
        number=92,
        oneof="error_code",
        enum=gage_feed_mapping_error.FeedMappingErrorEnum.FeedMappingError,
    )
    customer_feed_error = proto.Field(
        proto.ENUM,
        number=93,
        oneof="error_code",
        enum=gage_customer_feed_error.CustomerFeedErrorEnum.CustomerFeedError,
    )
    ad_group_feed_error = proto.Field(
        proto.ENUM,
        number=94,
        oneof="error_code",
        enum=gage_ad_group_feed_error.AdGroupFeedErrorEnum.AdGroupFeedError,
    )
    campaign_feed_error = proto.Field(
        proto.ENUM,
        number=96,
        oneof="error_code",
        enum=gage_campaign_feed_error.CampaignFeedErrorEnum.CampaignFeedError,
    )
    custom_interest_error = proto.Field(
        proto.ENUM,
        number=97,
        oneof="error_code",
        enum=gage_custom_interest_error.CustomInterestErrorEnum.CustomInterestError,
    )
    campaign_experiment_error = proto.Field(
        proto.ENUM,
        number=98,
        oneof="error_code",
        enum=gage_campaign_experiment_error.CampaignExperimentErrorEnum.CampaignExperimentError,
    )
    extension_feed_item_error = proto.Field(
        proto.ENUM,
        number=100,
        oneof="error_code",
        enum=gage_extension_feed_item_error.ExtensionFeedItemErrorEnum.ExtensionFeedItemError,
    )
    ad_parameter_error = proto.Field(
        proto.ENUM,
        number=101,
        oneof="error_code",
        enum=gage_ad_parameter_error.AdParameterErrorEnum.AdParameterError,
    )
    feed_item_validation_error = proto.Field(
        proto.ENUM,
        number=102,
        oneof="error_code",
        enum=gage_feed_item_validation_error.FeedItemValidationErrorEnum.FeedItemValidationError,
    )
    extension_setting_error = proto.Field(
        proto.ENUM,
        number=103,
        oneof="error_code",
        enum=gage_extension_setting_error.ExtensionSettingErrorEnum.ExtensionSettingError,
    )
    feed_item_set_error = proto.Field(
        proto.ENUM,
        number=140,
        oneof="error_code",
        enum=gage_feed_item_set_error.FeedItemSetErrorEnum.FeedItemSetError,
    )
    feed_item_set_link_error = proto.Field(
        proto.ENUM,
        number=141,
        oneof="error_code",
        enum=gage_feed_item_set_link_error.FeedItemSetLinkErrorEnum.FeedItemSetLinkError,
    )
    feed_item_target_error = proto.Field(
        proto.ENUM,
        number=104,
        oneof="error_code",
        enum=gage_feed_item_target_error.FeedItemTargetErrorEnum.FeedItemTargetError,
    )
    policy_violation_error = proto.Field(
        proto.ENUM,
        number=105,
        oneof="error_code",
        enum=gage_policy_violation_error.PolicyViolationErrorEnum.PolicyViolationError,
    )
    partial_failure_error = proto.Field(
        proto.ENUM,
        number=112,
        oneof="error_code",
        enum=gage_partial_failure_error.PartialFailureErrorEnum.PartialFailureError,
    )
    policy_validation_parameter_error = proto.Field(
        proto.ENUM,
        number=114,
        oneof="error_code",
        enum=gage_policy_validation_parameter_error.PolicyValidationParameterErrorEnum.PolicyValidationParameterError,
    )
    size_limit_error = proto.Field(
        proto.ENUM,
        number=118,
        oneof="error_code",
        enum=gage_size_limit_error.SizeLimitErrorEnum.SizeLimitError,
    )
    offline_user_data_job_error = proto.Field(
        proto.ENUM,
        number=119,
        oneof="error_code",
        enum=gage_offline_user_data_job_error.OfflineUserDataJobErrorEnum.OfflineUserDataJobError,
    )
    not_allowlisted_error = proto.Field(
        proto.ENUM,
        number=137,
        oneof="error_code",
        enum=gage_not_allowlisted_error.NotAllowlistedErrorEnum.NotAllowlistedError,
    )
    manager_link_error = proto.Field(
        proto.ENUM,
        number=121,
        oneof="error_code",
        enum=gage_manager_link_error.ManagerLinkErrorEnum.ManagerLinkError,
    )
    currency_code_error = proto.Field(
        proto.ENUM,
        number=122,
        oneof="error_code",
        enum=gage_currency_code_error.CurrencyCodeErrorEnum.CurrencyCodeError,
    )
    access_invitation_error = proto.Field(
        proto.ENUM,
        number=124,
        oneof="error_code",
        enum=gage_access_invitation_error.AccessInvitationErrorEnum.AccessInvitationError,
    )
    reach_plan_error = proto.Field(
        proto.ENUM,
        number=125,
        oneof="error_code",
        enum=gage_reach_plan_error.ReachPlanErrorEnum.ReachPlanError,
    )
    invoice_error = proto.Field(
        proto.ENUM,
        number=126,
        oneof="error_code",
        enum=gage_invoice_error.InvoiceErrorEnum.InvoiceError,
    )
    payments_account_error = proto.Field(
        proto.ENUM,
        number=127,
        oneof="error_code",
        enum=gage_payments_account_error.PaymentsAccountErrorEnum.PaymentsAccountError,
    )
    time_zone_error = proto.Field(
        proto.ENUM,
        number=128,
        oneof="error_code",
        enum=gage_time_zone_error.TimeZoneErrorEnum.TimeZoneError,
    )
    asset_link_error = proto.Field(
        proto.ENUM,
        number=129,
        oneof="error_code",
        enum=gage_asset_link_error.AssetLinkErrorEnum.AssetLinkError,
    )
    user_data_error = proto.Field(
        proto.ENUM,
        number=130,
        oneof="error_code",
        enum=gage_user_data_error.UserDataErrorEnum.UserDataError,
    )
    batch_job_error = proto.Field(
        proto.ENUM,
        number=131,
        oneof="error_code",
        enum=gage_batch_job_error.BatchJobErrorEnum.BatchJobError,
    )
    account_link_error = proto.Field(
        proto.ENUM,
        number=134,
        oneof="error_code",
        enum=gage_account_link_error.AccountLinkErrorEnum.AccountLinkError,
    )
    third_party_app_analytics_link_error = proto.Field(
        proto.ENUM,
        number=135,
        oneof="error_code",
        enum=gage_third_party_app_analytics_link_error.ThirdPartyAppAnalyticsLinkErrorEnum.ThirdPartyAppAnalyticsLinkError,
    )
    customer_user_access_error = proto.Field(
        proto.ENUM,
        number=138,
        oneof="error_code",
        enum=gage_customer_user_access_error.CustomerUserAccessErrorEnum.CustomerUserAccessError,
    )
    custom_audience_error = proto.Field(
        proto.ENUM,
        number=139,
        oneof="error_code",
        enum=gage_custom_audience_error.CustomAudienceErrorEnum.CustomAudienceError,
    )


class ErrorLocation(proto.Message):
    r"""Describes the part of the request proto that caused the
    error.

    Attributes:
        field_path_elements (Sequence[google.ads.googleads.v7.errors.types.ErrorLocation.FieldPathElement]):
            A field path that indicates which field was
            invalid in the request.
    """

    class FieldPathElement(proto.Message):
        r"""A part of a field path.
        Attributes:
            field_name (str):
                The name of a field or a oneof
            index (int):
                If field_name is a repeated field, this is the element that
                failed
        """

        field_name = proto.Field(proto.STRING, number=1,)
        index = proto.Field(proto.INT32, number=3, optional=True,)

    field_path_elements = proto.RepeatedField(
        proto.MESSAGE, number=2, message=FieldPathElement,
    )


class ErrorDetails(proto.Message):
    r"""Additional error details.
    Attributes:
        unpublished_error_code (str):
            The error code that should have been
            returned, but wasn't. This is used when the
            error code is not published in the client
            specified version.
        policy_violation_details (google.ads.googleads.v7.errors.types.PolicyViolationDetails):
            Describes an ad policy violation.
        policy_finding_details (google.ads.googleads.v7.errors.types.PolicyFindingDetails):
            Describes policy violation findings.
        quota_error_details (google.ads.googleads.v7.errors.types.QuotaErrorDetails):
            Details on the quota error, including the
            scope (account or developer), the rate bucket
            name and the retry delay.
        resource_count_details (google.ads.googleads.v7.errors.types.ResourceCountDetails):
            Details for a resource count limit exceeded
            error.
    """

    unpublished_error_code = proto.Field(proto.STRING, number=1,)
    policy_violation_details = proto.Field(
        proto.MESSAGE, number=2, message="PolicyViolationDetails",
    )
    policy_finding_details = proto.Field(
        proto.MESSAGE, number=3, message="PolicyFindingDetails",
    )
    quota_error_details = proto.Field(
        proto.MESSAGE, number=4, message="QuotaErrorDetails",
    )
    resource_count_details = proto.Field(
        proto.MESSAGE, number=5, message="ResourceCountDetails",
    )


class PolicyViolationDetails(proto.Message):
    r"""Error returned as part of a mutate response.
    This error indicates single policy violation by some text in one
    of the fields.

    Attributes:
        external_policy_description (str):
            Human readable description of policy
            violation.
        key (google.ads.googleads.v7.common.types.PolicyViolationKey):
            Unique identifier for this violation.
            If policy is exemptible, this key may be used to
            request exemption.
        external_policy_name (str):
            Human readable name of the policy.
        is_exemptible (bool):
            Whether user can file an exemption request
            for this violation.
    """

    external_policy_description = proto.Field(proto.STRING, number=2,)
    key = proto.Field(
        proto.MESSAGE, number=4, message=gagc_policy.PolicyViolationKey,
    )
    external_policy_name = proto.Field(proto.STRING, number=5,)
    is_exemptible = proto.Field(proto.BOOL, number=6,)


class PolicyFindingDetails(proto.Message):
    r"""Error returned as part of a mutate response.
    This error indicates one or more policy findings in the fields
    of a resource.

    Attributes:
        policy_topic_entries (Sequence[google.ads.googleads.v7.common.types.PolicyTopicEntry]):
            The list of policy topics for the resource. Contains the
            PROHIBITED or FULLY_LIMITED policy topic entries that
            prevented the resource from being saved (among any other
            entries the resource may also have).
    """

    policy_topic_entries = proto.RepeatedField(
        proto.MESSAGE, number=1, message=gagc_policy.PolicyTopicEntry,
    )


class QuotaErrorDetails(proto.Message):
    r"""Additional quota error details when there is QuotaError.
    Attributes:
        rate_scope (google.ads.googleads.v7.errors.types.QuotaErrorDetails.QuotaRateScope):
            The rate scope of the quota limit.
        rate_name (str):
            The high level description of the quota
            bucket. Examples are "Get requests for standard
            access" or "Requests per account".
        retry_delay (google.protobuf.duration_pb2.Duration):
            Backoff period that customers should wait
            before sending next request.
    """

    class QuotaRateScope(proto.Enum):
        r"""Enum of possible scopes that quota buckets belong to."""
        UNSPECIFIED = 0
        UNKNOWN = 1
        ACCOUNT = 2
        DEVELOPER = 3

    rate_scope = proto.Field(proto.ENUM, number=1, enum=QuotaRateScope,)
    rate_name = proto.Field(proto.STRING, number=2,)
    retry_delay = proto.Field(
        proto.MESSAGE, number=3, message=duration.Duration,
    )


class ResourceCountDetails(proto.Message):
    r"""Error details returned when an resource count limit was
    exceeded.

    Attributes:
        enclosing_id (str):
            The ID of the resource whose limit was
            exceeded. External customer ID if the limit is
            for a customer.
        enclosing_resource (str):
            The name of the resource (Customer, Campaign
            etc.) whose limit was exceeded.
        limit (int):
            The limit which was exceeded.
        limit_type (google.ads.googleads.v7.enums.types.ResourceLimitTypeEnum.ResourceLimitType):
            The resource limit type which was exceeded.
        existing_count (int):
            The count of existing entities.
    """

    enclosing_id = proto.Field(proto.STRING, number=1,)
    enclosing_resource = proto.Field(proto.STRING, number=5,)
    limit = proto.Field(proto.INT32, number=2,)
    limit_type = proto.Field(
        proto.ENUM,
        number=3,
        enum=resource_limit_type.ResourceLimitTypeEnum.ResourceLimitType,
    )
    existing_count = proto.Field(proto.INT32, number=4,)


__all__ = tuple(sorted(__protobuf__.manifest))
