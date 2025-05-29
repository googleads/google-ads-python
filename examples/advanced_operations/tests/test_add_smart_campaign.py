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
    mock_kw_theme1.keyword_theme_constant = MagicMock() # Simulate protobuf message structure
    mock_kw_theme1.keyword_theme_constant.resource_name = "keywordThemeConstants/theme1"
    # Ensure 'oneof' behavior; if keyword_theme_constant is set, free_form_keyword_theme is not.
    # MagicMock by default would create these attributes if accessed.
    # Explicitly deleting or ensuring they are None if not the active 'oneof' field.
    # However, the script checks hasattr(theme, "keyword_theme_constant"), so direct assignment is enough.

    mock_kw_theme2 = MagicMock()
    mock_kw_theme2.keyword_theme_constant = MagicMock()
    mock_kw_theme2.keyword_theme_constant.resource_name = "keywordThemeConstants/theme2"

    mock_kw_theme_response.keyword_themes = [mock_kw_theme1, mock_kw_theme2]
    
    # Suggestion for free-form keyword (this path is hit by the script)
    # This mock should return a KeywordTheme message where free_form_keyword_theme is set.
    mock_free_form_response = MagicMock()
    mock_free_form_theme = MagicMock()
    mock_free_form_theme.free_form_keyword_theme = "free form keyword theme text" # This is the actual text value
    # Ensure 'oneof' behavior for this mock too
    delattr(mock_free_form_theme, 'keyword_theme_constant') 
    mock_free_form_response.keyword_themes = [mock_free_form_theme]

    # Side effect to handle different request types for suggest_keyword_themes
    def suggest_keyword_themes_side_effect(request):
        if request.suggestion_info.free_form_text:
            return mock_free_form_response
        # This case is for request.suggestion_info.keyword_seed
        # The script does not use this path for suggest_keyword_themes.
        # It uses suggest_keyword_theme_constants for keyword_text.
        # However, to be safe, if it were called with keyword_seed:
        # return mock_kw_theme_response # This was the previous behavior
        # For now, let's assume it's not called with keyword_seed for suggest_keyword_themes
        # and the free_form_text path is the only one used by suggest_keyword_themes.
        # If suggest_keyword_themes is called for the seed, it should also return KeywordThemes.
        # The script calls:
        # 1. suggest_keyword_theme_constants with keyword_text (mocked below)
        # 2. suggest_keyword_themes with free_form_keyword_text (mocked by mock_free_form_response)
        # So, the keyword_seed path for suggest_keyword_themes is actually NOT hit.
        # Let's simplify the side_effect or remove it if only one path is hit.
        # Re-checking script: _get_keyword_theme_infos calls suggest_keyword_themes for free_form_keyword_text
        # and _get_keyword_theme_auto_suggestions calls suggest_keyword_theme_constants for keyword_text
        # This means the side_effect for suggest_keyword_themes only needs to handle the free_form_text case.
        if hasattr(request.suggestion_info, "free_form_text") and request.suggestion_info.free_form_text:
             return mock_free_form_response
        # Fallback if called unexpectedly (should not happen based on script logic)
        empty_response = MagicMock()
        empty_response.keyword_themes = []
        return empty_response

    mock_suggest_service.suggest_keyword_themes.side_effect = suggest_keyword_themes_side_effect # Keep existing side effect logic for now

    # --- Mocking client.get_type for various types used in the script ---
    mock_google_ads_client.get_type = MagicMock() # Reset to a simple mock first

    # Mock for KeywordTheme objects produced by KeywordTheme()
    # This instance will be returned when KeywordTheme() is called in the script.
    mock_keyword_theme_instance = MagicMock(spec=['keyword_theme_constant', 'free_form_keyword_theme'])
    mock_keyword_theme_instance.keyword_theme_constant = None
    mock_keyword_theme_instance.free_form_keyword_theme = None
    # This is the mock for the KeywordTheme "class" or "constructor"
    mock_keyword_theme_constructor = MagicMock(return_value=mock_keyword_theme_instance)
    
    # This is the mock for the type that *contains* KeywordTheme 
    # (i.e., what client.get_type("SuggestKeywordThemesResponse") returns)
    mock_suggest_keyword_themes_response_type = MagicMock()
    mock_suggest_keyword_themes_response_type.KeywordTheme = mock_keyword_theme_constructor

    # Mock for SmartCampaignSuggestionInfo
    mock_smart_campaign_suggestion_info_instance = MagicMock()
    mock_smart_campaign_suggestion_info_instance.location_list = MagicMock()
    mock_smart_campaign_suggestion_info_instance.location_list.locations = [] # Must be a list for .append()
    mock_smart_campaign_suggestion_info_instance.ad_schedules = [] # Must be a list for .append()

    # Mock for LocationInfo and AdScheduleInfo (simple mocks are fine)
    mock_location_info_instance = MagicMock()
    mock_ad_schedule_info_instance = MagicMock()

    def new_get_type_side_effect(type_name):
        if type_name == "SuggestKeywordThemesResponse":
            return mock_suggest_keyword_themes_response_type
        elif type_name == "SmartCampaignSuggestionInfo":
            # Important: return the instance directly if the script does client.get_type("SmartCampaignSuggestionInfo")
            # and expects to set attributes on it. If it calls it like a constructor, then this should return a mock constructor.
            # The script does: suggestion_info = client.get_type("SmartCampaignSuggestionInfo")
            # then suggestion_info.location_list = ...
            # So, returning the instance directly is correct.
            return mock_smart_campaign_suggestion_info_instance
        elif type_name == "LocationInfo":
            # Script does: location = client.get_type("LocationInfo")
            return mock_location_info_instance
        elif type_name == "AdScheduleInfo":
            # Script does: ad_schedule = client.get_type("AdScheduleInfo")
            return mock_ad_schedule_info_instance
        else:
            # Fallback for any other type
            return MagicMock()

    mock_google_ads_client.get_type.side_effect = new_get_type_side_effect
    # --- End of get_type mocking ---

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
    # Mock for suggest_keyword_theme_constants (called by _get_keyword_theme_auto_suggestions)
    mock_ktc_suggest_response = MagicMock()
    mock_ktc_constant1_from_suggest = MagicMock() # Simulates KeywordThemeConstant
    mock_ktc_constant1_from_suggest.resource_name = "keywordThemeConstants/from_text_search1"
    # mock_ktc_constant1_from_suggest.name = "From Text Search 1" # Name is not directly used by script
    mock_ktc_suggest_response.keyword_theme_constants = [mock_ktc_constant1_from_suggest]
    mock_ktc_service.suggest_keyword_theme_constants.return_value = mock_ktc_suggest_response
    # Mock for keyword_theme_constant_path (used by _get_keyword_theme_infos if keyword_theme_ids are present)
    # This path is not hit with current main() args as keyword_theme_ids is not passed.
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
    # For keyword theme criteria:
    # 1 from suggest_keyword_theme_constants (mock_ktc_constant1_from_suggest)
    # 1 from suggest_keyword_themes (mock_free_form_theme)
    # Total 2 keyword theme criteria + 1 location criterion
    for i in range(3): 
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
    
    # Mock for suggest_keyword_themes (called for free_form_keyword_text if provided)
    # In this test, free_form_keyword_text is None, so suggest_keyword_themes might not be called,
    # or if called, request.suggestion_info.free_form_text will be empty.
    # The script's _get_keyword_theme_infos checks if free_form_keyword_text:
    # if free_form_keyword_text:
    #   response = smart_campaign_suggest_service.suggest_keyword_themes(request)
    #   keyword_theme_infos.extend(map_keyword_themes_to_keyword_infos(response.keyword_themes))
    # So, if free_form_keyword_text is None, suggest_keyword_themes is NOT called by _get_keyword_theme_infos.
    # The script path for this test case:
    # 1. _get_keyword_text_auto_completions IS called with keyword_text.
    #    - It calls KeywordThemeConstantService.suggest_keyword_theme_constants.
    #    - It then creates KeywordTheme objects using client.get_type("SuggestKeywordThemesResponse").KeywordTheme().
    #      These instances will now be created by our mock_keyword_theme_constructor.
    # 2. _get_keyword_theme_infos is called.
    #    - If keyword_theme_ids are provided (not in this test), it uses them.
    #    - If free_form_keyword_text is provided (None in this test), it calls suggest_keyword_themes.
    #      Since free_form_keyword_text is None, suggest_keyword_themes is NOT called here.
    # Therefore, the mock for suggest_keyword_themes for this test can return an empty list.
    mock_empty_kw_theme_response = MagicMock()
    mock_empty_kw_theme_response.keyword_themes = [] # No themes from this service for this test path
    mock_suggest_service.suggest_keyword_themes.return_value = mock_empty_kw_theme_response

    # --- Mocking client.get_type for various types (similar to the first test) ---
    mock_google_ads_client.get_type = MagicMock() # Reset to a simple mock

    mock_keyword_theme_instance_biz = MagicMock(spec=['keyword_theme_constant', 'free_form_keyword_theme'])
    mock_keyword_theme_instance_biz.keyword_theme_constant = None
    mock_keyword_theme_instance_biz.free_form_keyword_theme = None
    mock_keyword_theme_constructor_biz = MagicMock(return_value=mock_keyword_theme_instance_biz)

    mock_suggest_keyword_themes_response_type_biz = MagicMock()
    mock_suggest_keyword_themes_response_type_biz.KeywordTheme = mock_keyword_theme_constructor_biz

    mock_smart_campaign_suggestion_info_instance_biz = MagicMock()
    mock_smart_campaign_suggestion_info_instance_biz.location_list = MagicMock()
    mock_smart_campaign_suggestion_info_instance_biz.location_list.locations = []
    mock_smart_campaign_suggestion_info_instance_biz.ad_schedules = []
    
    mock_location_info_instance_biz = MagicMock()
    mock_ad_schedule_info_instance_biz = MagicMock()

    def new_get_type_side_effect_biz(type_name):
        if type_name == "SuggestKeywordThemesResponse":
            return mock_suggest_keyword_themes_response_type_biz
        elif type_name == "SmartCampaignSuggestionInfo":
            return mock_smart_campaign_suggestion_info_instance_biz
        elif type_name == "LocationInfo":
            return mock_location_info_instance_biz
        elif type_name == "AdScheduleInfo":
            return mock_ad_schedule_info_instance_biz
        else:
            return MagicMock()

    mock_google_ads_client.get_type.side_effect = new_get_type_side_effect_biz
    # --- End of get_type mocking for biz test ---

    mock_budget_options_response = MagicMock()
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
    # Mock for suggest_keyword_theme_constants (called by _get_keyword_theme_auto_suggestions for keyword_text)
    mock_ktc_suggest_response_biz = MagicMock()
    mock_ktc_constant1_biz = MagicMock() # Simulates KeywordThemeConstant
    mock_ktc_constant1_biz.resource_name = "keywordThemeConstants/from_text_search_biz1"
    mock_ktc_suggest_response_biz.keyword_theme_constants = [mock_ktc_constant1_biz]
    mock_ktc_service.suggest_keyword_theme_constants.return_value = mock_ktc_suggest_response_biz
    # Mock for keyword_theme_constant_path (not hit with current args)
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
    # Keyword themes for criteria:
    # 1 from suggest_keyword_theme_constants (mock_ktc_constant1_biz)
    # 0 from suggest_keyword_themes (because free_form_keyword_text is None)
    # Total 1 keyword theme criterion + 1 location criterion
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
            None, # No free_form_keyword_text for this test case
            mock_business_profile_location,
            None # Business name is ignored by script when business profile location is set
        )
    except Exception as e:
        pytest.fail(f"main function raised an exception: {e}")
