import pytest
from unittest.mock import MagicMock, patch

from examples.advanced_operations.add_smart_campaign import main

# Global temporary IDs used by the script
_BUDGET_TEMPORARY_ID = "-1"
_SMART_CAMPAIGN_TEMPORARY_ID = "-2"
_AD_GROUP_TEMPORARY_ID = "-3"

@patch("examples.advanced_operations.add_smart_campaign.uuid4", return_value=MagicMock(hex="testuuid"))
def test_main_runs_successfully(mock_uuid4: MagicMock, mock_google_ads_client: MagicMock) -> None:
    """Tests that the main function runs without raising an exception."""
    mock_customer_id = "123"
    mock_keyword_text = "some keywords"
    mock_free_form_keyword_text = "more free keywords"
    mock_business_profile_location = None # Test default path first
    mock_business_name = "TestBiz"


    # --- Mock services ---
    # SmartCampaignSuggestService
    mock_suggest_service = mock_google_ads_client.get_service("SmartCampaignSuggestService")
    # Suggest Keyword Themes
    mock_kw_theme_response = MagicMock()
    mock_kw_theme1 = MagicMock()
    mock_kw_theme1.keyword_theme_constant.resource_name = "keywordThemeConstants/theme1"
    mock_kw_theme1.keyword_theme_constant.name = "Theme 1"
    mock_kw_theme2 = MagicMock()
    mock_kw_theme2.keyword_theme_constant.resource_name = "keywordThemeConstants/theme2"
    mock_kw_theme2.keyword_theme_constant.name = "Theme 2"
    mock_kw_theme_response.keyword_themes = [mock_kw_theme1, mock_kw_theme2]
    # Suggestion for free-form keyword
    mock_free_form_suggestion = MagicMock()
    mock_free_form_suggestion.keyword_theme_constant.resource_name = "keywordThemeConstants/freeform"
    mock_free_form_suggestion.keyword_theme_constant.name = "FreeForm Theme"
    
    # Side effect to handle different request types for suggest_keyword_themes
    def suggest_keyword_themes_side_effect(request):
        if request.suggestion_info.free_form_text:
            response = MagicMock()
            response.keyword_themes = [mock_free_form_suggestion]
            return response
        return mock_kw_theme_response
    mock_suggest_service.suggest_keyword_themes.side_effect = suggest_keyword_themes_side_effect

    # Suggest Budget Options
    mock_budget_options_response = MagicMock()
    mock_recommended_budget = MagicMock()
    mock_recommended_budget.daily_amount_micros = 50000000 # 50 units of currency
    mock_budget_options_response.recommended_daily_budget_options.high.daily_amount_micros = 60000000
    mock_budget_options_response.recommended_daily_budget_options.low.daily_amount_micros = 40000000
    mock_budget_options_response.recommended_daily_budget_options.recommended.daily_amount_micros = mock_recommended_budget.daily_amount_micros # ensure this matches
    mock_suggest_service.suggest_smart_campaign_budget_options.return_value = mock_budget_options_response
    
    # Suggest Smart Campaign Ad
    mock_ad_suggestion_response = MagicMock()
    mock_ad_info = MagicMock()
    mock_headline1 = MagicMock()
    mock_headline1.text = "Suggested Headline 1"
    mock_desc1 = MagicMock()
    mock_desc1.text = "Suggested Description 1"
    mock_ad_info.headlines = [mock_headline1]
    mock_ad_info.descriptions = [mock_desc1]
    mock_ad_suggestion_response.ad_info = mock_ad_info
    mock_suggest_service.suggest_smart_campaign_ad.return_value = mock_ad_suggestion_response

    # KeywordThemeConstantService
    mock_ktc_service = mock_google_ads_client.get_service("KeywordThemeConstantService")
    mock_ktc_service.keyword_theme_constant_path.side_effect = lambda ktc_id: f"keywordThemeConstants/{ktc_id}"

    # GeoTargetConstantService
    mock_geo_service = mock_google_ads_client.get_service("GeoTargetConstantService")
    # The script uses a hardcoded geo target "2840" (USA)
    mock_geo_service.geo_target_constant_path.return_value = "geoTargetConstants/2840"
    
    # GoogleAdsService (for mutate and paths)
    mock_googleads_service = mock_google_ads_client.get_service("GoogleAdsService")
    mock_googleads_service.campaign_budget_path.return_value = f"customers/{mock_customer_id}/campaignBudgets/{_BUDGET_TEMPORARY_ID}"
    mock_googleads_service.campaign_path.return_value = f"customers/{mock_customer_id}/campaigns/{_SMART_CAMPAIGN_TEMPORARY_ID}"
    mock_googleads_service.ad_group_path.return_value = f"customers/{mock_customer_id}/adGroups/{_AD_GROUP_TEMPORARY_ID}"
    # Path for business profile location if provided
    if mock_business_profile_location:
         mock_googleads_service.business_profile_location_path.return_value = f"businessProfileLocations/{mock_business_profile_location.split('/')[-1]}"


    # Mock the main GoogleAdsService.mutate call
    mock_mutate_response = MagicMock()
    # Expected operations: CampaignBudget, Campaign, SmartCampaignSetting, AdGroup, AdGroupAd, multiple CampaignCriterion
    responses = []
    responses.append(MagicMock(campaign_budget_result=MagicMock(resource_name=f"customers/{mock_customer_id}/campaignBudgets/budget1")))
    responses.append(MagicMock(campaign_result=MagicMock(resource_name=f"customers/{mock_customer_id}/campaigns/campaign1")))
    responses.append(MagicMock(smart_campaign_setting_result=MagicMock(resource_name=f"customers/{mock_customer_id}/smartCampaignSettings/scs1")))
    responses.append(MagicMock(ad_group_result=MagicMock(resource_name=f"customers/{mock_customer_id}/adGroups/adgroup1")))
    responses.append(MagicMock(ad_group_ad_result=MagicMock(resource_name=f"customers/{mock_customer_id}/adGroupAds/ad1")))
    # For keyword theme criteria (2 from suggestion + 1 free form) and 1 location criterion
    for i in range(4): # 3 keyword themes + 1 location
        responses.append(MagicMock(campaign_criterion_result=MagicMock(resource_name=f"customers/{mock_customer_id}/campaignCriteria/crit{i}")))
    
    mock_mutate_response.mutate_operation_responses = responses
    mock_googleads_service.mutate.return_value = mock_mutate_response

    # --- Mock enums ---
    mock_enums = mock_google_ads_client.enums
    mock_enums.BudgetDeliveryMethodEnum.STANDARD = "STANDARD"
    mock_enums.AdvertisingChannelTypeEnum.SMART = "SMART"
    mock_enums.CampaignStatusEnum.PAUSED = "PAUSED"
    mock_enums.AdGroupTypeEnum.SMART_CAMPAIGN_ADS = "SMART_CAMPAIGN_ADS" # for AdGroup
    mock_enums.AdGroupStatusEnum.ENABLED = "ENABLED" # for AdGroup
    mock_enums.AdGroupAdStatusEnum.ENABLED = "ENABLED" # for AdGroupAd
    mock_enums.CriterionTypeEnum.KEYWORD_THEME = "KEYWORD_THEME"
    mock_enums.CriterionTypeEnum.LOCATION = "LOCATION"


    try:
        main(
            mock_google_ads_client,
            mock_customer_id,
            mock_keyword_text,
            mock_free_form_keyword_text,
            mock_business_profile_location,
            mock_business_name
        )
    except Exception as e:
        pytest.fail(f"main function raised an exception: {e}")

# Consider a separate test if business_profile_location path is significantly different
@patch("examples.advanced_operations.add_smart_campaign.uuid4", return_value=MagicMock(hex="testuuid_biz"))
def test_main_with_business_location_runs_successfully(mock_uuid4_biz: MagicMock, mock_google_ads_client: MagicMock) -> None:
    """Tests main with a business profile location."""
    mock_customer_id = "123"
    mock_keyword_text = "other keywords"
    mock_free_form_keyword_text = "other free keywords"
    mock_business_profile_location = "businessProfileLocations/12345" # Example path
    mock_business_name = None # Business name is not used if profile location is set

    # Most mocks can be similar to the first test, just ensure business_profile_location_path is set up
    # SmartCampaignSuggestService
    mock_suggest_service = mock_google_ads_client.get_service("SmartCampaignSuggestService")
    mock_kw_theme_response = MagicMock() # Define as in first test
    mock_kw_theme1 = MagicMock()
    mock_kw_theme1.keyword_theme_constant.resource_name = "keywordThemeConstants/theme_biz1"
    mock_kw_theme1.keyword_theme_constant.name = "Theme Biz 1"
    mock_kw_theme_response.keyword_themes = [mock_kw_theme1]
    def suggest_keyword_themes_side_effect_biz(request): # Simplified for this test variation
        return mock_kw_theme_response
    mock_suggest_service.suggest_keyword_themes.side_effect = suggest_keyword_themes_side_effect_biz

    mock_budget_options_response = MagicMock() # Define as in first test
    mock_recommended_budget = MagicMock()
    mock_recommended_budget.daily_amount_micros = 55000000 
    mock_budget_options_response.recommended_daily_budget_options.high.daily_amount_micros = 65000000
    mock_budget_options_response.recommended_daily_budget_options.low.daily_amount_micros = 45000000
    mock_budget_options_response.recommended_daily_budget_options.recommended.daily_amount_micros = mock_recommended_budget.daily_amount_micros
    mock_suggest_service.suggest_smart_campaign_budget_options.return_value = mock_budget_options_response
    
    mock_ad_suggestion_response = MagicMock() # Define as in first test
    mock_ad_info = MagicMock()
    mock_headline1 = MagicMock()
    mock_headline1.text = "Biz Suggested Headline 1"
    mock_desc1 = MagicMock()
    mock_desc1.text = "Biz Suggested Description 1"
    mock_ad_info.headlines = [mock_headline1]
    mock_ad_info.descriptions = [mock_desc1]
    mock_ad_suggestion_response.ad_info = mock_ad_info
    mock_suggest_service.suggest_smart_campaign_ad.return_value = mock_ad_suggestion_response

    mock_ktc_service = mock_google_ads_client.get_service("KeywordThemeConstantService")
    mock_ktc_service.keyword_theme_constant_path.side_effect = lambda ktc_id: f"keywordThemeConstants/{ktc_id}"
    
    mock_geo_service = mock_google_ads_client.get_service("GeoTargetConstantService")
    mock_geo_service.geo_target_constant_path.return_value = "geoTargetConstants/2840"
    
    mock_googleads_service = mock_google_ads_client.get_service("GoogleAdsService")
    mock_googleads_service.campaign_budget_path.return_value = f"customers/{mock_customer_id}/campaignBudgets/{_BUDGET_TEMPORARY_ID}"
    mock_googleads_service.campaign_path.return_value = f"customers/{mock_customer_id}/campaigns/{_SMART_CAMPAIGN_TEMPORARY_ID}"
    mock_googleads_service.ad_group_path.return_value = f"customers/{mock_customer_id}/adGroups/{_AD_GROUP_TEMPORARY_ID}"
    mock_googleads_service.business_profile_location_path.return_value = mock_business_profile_location # Key change for this test

    mock_mutate_response = MagicMock()
    responses = [] # Define as in first test, potentially with different resource names if needed for clarity
    responses.append(MagicMock(campaign_budget_result=MagicMock(resource_name=f"customers/{mock_customer_id}/campaignBudgets/budget_biz")))
    responses.append(MagicMock(campaign_result=MagicMock(resource_name=f"customers/{mock_customer_id}/campaigns/campaign_biz")))
    responses.append(MagicMock(smart_campaign_setting_result=MagicMock(resource_name=f"customers/{mock_customer_id}/smartCampaignSettings/scs_biz")))
    responses.append(MagicMock(ad_group_result=MagicMock(resource_name=f"customers/{mock_customer_id}/adGroups/adgroup_biz")))
    responses.append(MagicMock(ad_group_ad_result=MagicMock(resource_name=f"customers/{mock_customer_id}/adGroupAds/ad_biz")))
    # Fewer keyword themes in this simplified version for biz profile path (1 suggested + 0 free-form) + 1 location
    for i in range(2): 
        responses.append(MagicMock(campaign_criterion_result=MagicMock(resource_name=f"customers/{mock_customer_id}/campaignCriteria/crit_biz{i}")))
    mock_mutate_response.mutate_operation_responses = responses
    mock_googleads_service.mutate.return_value = mock_mutate_response

    mock_enums = mock_google_ads_client.enums # Define as in first test
    mock_enums.BudgetDeliveryMethodEnum.STANDARD = "STANDARD"
    mock_enums.AdvertisingChannelTypeEnum.SMART = "SMART"
    mock_enums.CampaignStatusEnum.PAUSED = "PAUSED"
    mock_enums.AdGroupTypeEnum.SMART_CAMPAIGN_ADS = "SMART_CAMPAIGN_ADS"
    mock_enums.AdGroupStatusEnum.ENABLED = "ENABLED"
    mock_enums.AdGroupAdStatusEnum.ENABLED = "ENABLED"
    mock_enums.CriterionTypeEnum.KEYWORD_THEME = "KEYWORD_THEME"
    mock_enums.CriterionTypeEnum.LOCATION = "LOCATION"
    mock_enums.SmartCampaignNotEligibleReasonEnum = MagicMock() # For printing errors, not critical for success path
    mock_enums.SmartCampaignNotEligibleReasonEnum.BUSINESS_PROFILE_LOCATION_REMOVED = "BUSINESS_PROFILE_LOCATION_REMOVED"

    try:
        main(
            mock_google_ads_client,
            mock_customer_id,
            mock_keyword_text,
            None, # No free_form_keyword_text when business profile is used, per script logic
            mock_business_profile_location,
            mock_business_name # Should be None or ignored by script when biz profile is set
        )
    except Exception as e:
        pytest.fail(f"main function raised an exception: {e}")
