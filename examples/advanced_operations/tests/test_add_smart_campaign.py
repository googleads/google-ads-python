import unittest
from unittest import mock
import sys

# sys.path.insert(0, '/app') # For subtask environment - REMOVED

from examples.advanced_operations import add_smart_campaign

# Temporary IDs from the script
_BUDGET_TEMPORARY_ID = "-1"
_SMART_CAMPAIGN_TEMPORARY_ID = "-2"
_AD_GROUP_TEMPORARY_ID = "-3"

# Constants from script for default values (used in assertions)
_COUNTRY_CODE = "US"
_LANGUAGE_CODE = "en"
_LANDING_PAGE_URL = "http://www.example.com"
_PHONE_NUMBER = "800-555-0100"
_GEO_TARGET_CONSTANT = "1023191" # NYC


class TestAddSmartCampaign(unittest.TestCase):

    def _setup_common_mocks(self, mock_google_ads_client):
        mock_google_ads_client.version = "v19"
        self.mock_objects_created_by_get_type = {}

        # Mock Services
        self.mock_smart_campaign_suggest_service = mock.Mock(name="SmartCampaignSuggestService")
        self.mock_keyword_theme_constant_service = mock.Mock(name="KeywordThemeConstantService")
        self.mock_geo_target_constant_service = mock.Mock(name="GeoTargetConstantService")
        self.mock_google_ads_service = mock.Mock(name="GoogleAdsService")

        def get_service_side_effect(service_name, version=None):
            self.assertEqual("v19", version if version else mock_google_ads_client.version)
            service_map = {
                "SmartCampaignSuggestService": self.mock_smart_campaign_suggest_service,
                "KeywordThemeConstantService": self.mock_keyword_theme_constant_service,
                "GeoTargetConstantService": self.mock_geo_target_constant_service,
                "GoogleAdsService": self.mock_google_ads_service,
                # For resource name creation like campaign_budget_path, campaign_path etc.
                "CampaignBudgetService": mock.Mock(name="CampaignBudgetService"),
                "CampaignService": mock.Mock(name="CampaignService"),
                "SmartCampaignSettingService": mock.Mock(name="SmartCampaignSettingService"),
                "AdGroupService": mock.Mock(name="AdGroupService"),
            }
            if service_name in service_map:
                # Ensure path methods return expected strings
                if service_name == "CampaignBudgetService":
                    service_map[service_name].campaign_budget_path.return_value = f"customers/{{customer_id}}/campaignBudgets/{_BUDGET_TEMPORARY_ID}"
                elif service_name == "CampaignService":
                    service_map[service_name].campaign_path.return_value = f"customers/{{customer_id}}/campaigns/{_SMART_CAMPAIGN_TEMPORARY_ID}"
                elif service_name == "SmartCampaignSettingService":
                    service_map[service_name].smart_campaign_setting_path.return_value = f"customers/{{customer_id}}/smartCampaignSettings/{_SMART_CAMPAIGN_TEMPORARY_ID}"
                elif service_name == "AdGroupService":
                     service_map[service_name].ad_group_path.return_value = f"customers/{{customer_id}}/adGroups/{_AD_GROUP_TEMPORARY_ID}"

                return service_map[service_name]
            return mock.Mock(name=f"UnexpectedService_{service_name}")
        mock_google_ads_client.get_service.side_effect = get_service_side_effect

        # Mock Enums
        enums_to_mock = {
            "CampaignStatusEnum": {"PAUSED": "CAMPAIGN_PAUSED", "ENABLED": "CAMPAIGN_ENABLED"},
            "AdvertisingChannelTypeEnum": {"SMART": "SMART_CHANNEL"},
            "AdvertisingChannelSubTypeEnum": {"SMART_CAMPAIGN": "SMART_CAMPAIGN_SUBTYPE"},
            "BudgetTypeEnum": {"SMART_CAMPAIGN": "BUDGET_SMART_CAMPAIGN"},
            "AdGroupTypeEnum": {"SMART_CAMPAIGN_ADS": "ADGROUP_SMART_CAMPAIGN_ADS"},
            "CriterionTypeEnum": {"KEYWORD_THEME": "CRITERION_KEYWORD_THEME", "LOCATION": "CRITERION_LOCATION"},
            "DayOfWeekEnum": {"MONDAY": "MONDAY_DOW"}, # For AdScheduleInfo
            "MinuteOfHourEnum": {"ZERO": "MINUTE_ZERO"}, # For AdScheduleInfo
            "AdTypeEnum": {"SMART_CAMPAIGN_AD": "AD_TYPE_SMART_CAMPAIGN"},
        }
        for enum_name, members in enums_to_mock.items():
            enum_mock = mock.Mock(name=enum_name)
            for member_name, str_val in members.items():
                setattr(enum_mock, member_name, str_val)
            setattr(mock_google_ads_client.enums, enum_name, enum_mock)

        # Mock client.get_type()
        self.ad_text_asset_mocks = []
        def get_type_side_effect(type_name, version=None):
            if type_name.endswith("Operation"):
                base_name = type_name.replace("Operation", "")
                op_mock = mock.Mock(name=type_name)
                create_mock = mock.Mock(name=f"{base_name}_Payload") # Renamed for clarity

                if base_name == "SmartCampaignSetting":
                    op_mock.update = create_mock
                    op_mock.update_mask = mock.Mock(name="FieldMask")
                    op_mock.update_mask.paths = []

                    # Setup _pb.DESCRIPTOR.fields_by_name for field_mask helper for SmartCampaignSetting payload
                    mock_pb = mock.Mock(name="_pb_for_SCS_Payload")
                    mock_descriptor = mock.Mock(name="DESCRIPTOR_for_SCS_pb")
                    # Set fields_by_name to an empty dictionary (which is iterable)
                    mock_descriptor.fields_by_name = {}
                    mock_pb.DESCRIPTOR = mock_descriptor
                    create_mock._pb = mock_pb
                    create_mock.phone_number = mock.Mock(name="PhoneNumber_on_SCS")
                else:
                    op_mock.create = create_mock

                self.mock_objects_created_by_get_type.setdefault(base_name, []).append(create_mock)

                if base_name == "CampaignCriterion":
                    create_mock.keyword_theme = mock.Mock(name="KeywordThemeInfo_via_Criterion")
                    create_mock.location = mock.Mock(name="LocationInfo_via_Criterion")
                elif base_name == "AdGroupAd":
                    ad_mock = mock.Mock(name="Ad_on_AdGroupAd")
                    ad_mock.smart_campaign_ad = mock.Mock(name="SmartCampaignAdInfo")
                    ad_mock.smart_campaign_ad.headlines = []
                    ad_mock.smart_campaign_ad.descriptions = []
                    create_mock.ad = ad_mock
                # No need for specific SmartCampaignSetting pre-creation here as it's handled above for .update
                return op_mock
            elif type_name == "SmartCampaignSuggestionInfo":
                suggestion_info_mock = mock.Mock(name="SmartCampaignSuggestionInfo")
                suggestion_info_mock.location_list = mock.Mock(name="LocationList")
                suggestion_info_mock.location_list.locations = [] # For appending LocationInfo
                suggestion_info_mock.ad_schedules = [] # For appending AdScheduleInfo
                suggestion_info_mock.keyword_themes = [] # For assigning KeywordThemeInfo list
                suggestion_info_mock.business_context = mock.Mock(name="BusinessContext") # For business_name
                return suggestion_info_mock
            elif type_name == "KeywordThemeInfo":
                return mock.Mock(name="KeywordThemeInfo")
            elif type_name == "LocationInfo":
                return mock.Mock(name="LocationInfo")
            elif type_name == "AdScheduleInfo":
                return mock.Mock(name="AdScheduleInfo")
            elif type_name == "AdTextAsset":
                asset_mock = mock.Mock(name=f"AdTextAsset_Instance_{len(self.ad_text_asset_mocks)+1}")
                self.ad_text_asset_mocks.append(asset_mock)
                return asset_mock
            elif type_name == "SuggestKeywordThemeConstantsRequest": # For get_keyword_text_auto_completions
                return mock.Mock(name="SuggestKeywordThemeConstantsRequest")
            elif type_name == "SuggestKeywordThemesRequest": # For get_keyword_theme_suggestions
                return mock.Mock(name="SuggestKeywordThemesRequest")
            elif type_name == "SuggestSmartCampaignBudgetOptionsRequest":
                return mock.Mock(name="SuggestSmartCampaignBudgetOptionsRequest")
            elif type_name == "SuggestSmartCampaignAdRequest":
                return mock.Mock(name="SuggestSmartCampaignAdRequest")
            elif type_name == "SuggestKeywordThemesResponse": # Added this case
                response_mock = mock.Mock(name="SuggestKeywordThemesResponse_Type")
                response_mock.KeywordTheme = mock.Mock(name="KeywordTheme_Class_From_Response")

                def create_keyword_theme_instance_mock():
                    instance_mock = mock.MagicMock(name="KeywordTheme_Instance")
                    instance_mock.keyword_theme_constant = None
                    instance_mock.free_form_keyword_theme = None
                    def instance_contains(item):
                        if item == "keyword_theme_constant":
                            return hasattr(instance_mock, "keyword_theme_constant") and instance_mock.keyword_theme_constant is not None
                        if item == "free_form_keyword_theme":
                            return hasattr(instance_mock, "free_form_keyword_theme") and instance_mock.free_form_keyword_theme is not None
                        return False
                    instance_mock.__contains__ = mock.Mock(side_effect=instance_contains)
                    return instance_mock
                # Use side_effect to return a new, specially configured MagicMock each time KeywordTheme() is called
                response_mock.KeywordTheme.side_effect = create_keyword_theme_instance_mock
                return response_mock

            self.fail(f"Unexpected type requested by script: {type_name}")
        mock_google_ads_client.get_type.side_effect = get_type_side_effect

        # Mock main mutate call response (script iterates over it for printing)
        mock_main_mutate_response = mock.Mock(name="MainMutateResponse")
        # Simulate some results for print_response_details to iterate
        mock_result1 = mock.Mock()
        mock_result1._pb = mock.Mock() # To avoid error in result._pb.HasField
        mock_result1._pb.HasField.return_value = True # Assume first field is set
        type(mock_result1).campaign_budget_result = mock.PropertyMock(return_value=mock.Mock(resource_name="budget_res_name_from_print"))
        mock_main_mutate_response.mutate_operation_responses = [mock_result1]
        self.mock_google_ads_service.mutate.return_value = mock_main_mutate_response


    def _configure_suggestion_service_responses(self, customer_id, keyword_text=None, free_form_keyword_text=None):
        # Suggest Keyword Themes (if keyword_text is None in main, and free_form_keyword_text is None)
        # Or, if keyword_text is provided, this is called by get_keyword_theme_suggestions for initial set
        mock_sks_response = mock.Mock(name="SuggestKeywordThemesResponse")
        sks_kt1 = mock.MagicMock(name="SKS_KeywordTheme1")
        sks_kt1.keyword_theme_constant = mock.Mock(resource_name="keywordThemeConstants/suggested123")
        sks_kt1.free_form_keyword_theme = None # To make it defined for hasattr

        def sks_kt1_contains(item):
            if item == "keyword_theme_constant":
                return hasattr(sks_kt1, "keyword_theme_constant") and sks_kt1.keyword_theme_constant is not None
            if item == "free_form_keyword_theme":
                return hasattr(sks_kt1, "free_form_keyword_theme") and sks_kt1.free_form_keyword_theme is not None
            return False
        sks_kt1.__contains__ = mock.Mock(side_effect=sks_kt1_contains)
        mock_sks_response.keyword_themes = [sks_kt1]
        self.mock_smart_campaign_suggest_service.suggest_keyword_themes.return_value = mock_sks_response

        # Suggest Keyword Theme Constants (if keyword_text is provided in main)
        if keyword_text:
            mock_ktc_response = mock.Mock(name="SuggestKeywordThemeConstantsResponse")
            ktc1 = mock.Mock(name="KTC_Constant1")
            ktc1.resource_name = f"keywordThemeConstants/{keyword_text.replace(' ', '')}"
            ktc1.country_code = _COUNTRY_CODE
            ktc1.language_code = _LANGUAGE_CODE
            ktc1.display_name = keyword_text
            mock_ktc_response.keyword_theme_constants = [ktc1]
            self.mock_keyword_theme_constant_service.suggest_keyword_theme_constants.return_value = mock_ktc_response

        # Suggest Budget Options
        mock_budget_response = mock.Mock(name="SuggestSmartCampaignBudgetOptionsResponse")
        recommended_budget = mock.Mock(name="RecommendedBudgetOption")
        recommended_budget.daily_amount_micros = 20000000 # 20 currency units
        recommended_budget.metrics = mock.Mock(min_daily_clicks=10, max_daily_clicks=20)
        mock_budget_response.recommended = recommended_budget
        self.mock_smart_campaign_suggest_service.suggest_smart_campaign_budget_options.return_value = mock_budget_response

        # Suggest Smart Campaign Ad
        mock_ad_suggestion_response = mock.Mock(name="SuggestSmartCampaignAdResponse")
        ad_suggestion = mock.Mock(name="AdSuggestion")
        headline1 = mock.Mock(text="Suggested Headline 1");
        headline2 = mock.Mock(text="Suggested Headline 2");
        headline3 = mock.Mock(text="Suggested Headline 3");
        desc1 = mock.Mock(text="Suggested Description 1");
        desc2 = mock.Mock(text="Suggested Description 2");
        ad_suggestion.headlines = [headline1, headline2, headline3] # Script expects up to 3
        ad_suggestion.descriptions = [desc1, desc2] # Script expects up to 2
        mock_ad_suggestion_response.ad_info = ad_suggestion # Script uses ad_info
        self.mock_smart_campaign_suggest_service.suggest_smart_campaign_ad.return_value = mock_ad_suggestion_response

        # Mock GeoTargetConstantService for geo target paths used in suggestion info
        self.mock_geo_target_constant_service.geo_target_constant_path.return_value = f"geoTargetConstants/{_GEO_TARGET_CONSTANT}"


    @mock.patch("examples.advanced_operations.add_smart_campaign.GoogleAdsClient.load_from_storage")
    def test_main_with_keyword_text_and_business_name(self, mock_load_from_storage):
        mock_google_ads_client = mock.Mock()
        mock_load_from_storage.return_value = mock_google_ads_client
        self._setup_common_mocks(mock_google_ads_client)

        customer_id = "smartCust1"
        keyword_text = "flowers"
        business_name = "My Test Business"
        self._configure_suggestion_service_responses(customer_id, keyword_text=keyword_text)


        # Corrected main call with 6 arguments
        add_smart_campaign.main(
            mock_google_ads_client,
            customer_id,
            keyword_text,
            None, # free_form_keyword_text
            None, # business_profile_location
            business_name
        )

        # --- Assertions ---
        # Suggestion service calls
        self.mock_smart_campaign_suggest_service.suggest_keyword_themes.assert_called_once()
        self.mock_keyword_theme_constant_service.suggest_keyword_theme_constants.assert_called_once() # Called because keyword_text is provided
        self.mock_smart_campaign_suggest_service.suggest_smart_campaign_budget_options.assert_called_once()
        self.mock_smart_campaign_suggest_service.suggest_smart_campaign_ad.assert_called_once()

        # Main mutate call
        self.mock_google_ads_service.mutate.assert_called_once()
        mutate_ops = self.mock_google_ads_service.mutate.call_args[1]['operations']

        def find_op_payloads(op_field_name): # op_field_name like "campaign_budget_operation"
            payloads = []
            for op_wrapper in mutate_ops:
                if op_wrapper.WhichOneof("operation") == op_field_name:
                    specific_op_message = getattr(op_wrapper, op_field_name)
                    if op_field_name == "smart_campaign_setting_operation":
                        payloads.append(specific_op_message.update)
                    else:
                        payloads.append(specific_op_message.create)
            return payloads

        # Budget
        budget_payloads = find_op_payloads("campaign_budget_operation")
        self.assertEqual(len(budget_payloads), 1)
        self.assertEqual(budget_payloads[0].type_, "BUDGET_SMART_CAMPAIGN")
        self.assertEqual(budget_payloads[0].resource_name, f"customers/{customer_id}/campaignBudgets/{_BUDGET_TEMPORARY_ID}")
        self.assertEqual(budget_payloads[0].amount_micros, 20000000) # From mock suggestion

        # Campaign
        campaign_payloads = find_op_payloads("campaign_operation")
        self.assertEqual(len(campaign_payloads), 1)
        self.assertEqual(campaign_payloads[0].campaign_budget, f"customers/{customer_id}/campaignBudgets/{_BUDGET_TEMPORARY_ID}")
        self.assertEqual(campaign_payloads[0].advertising_channel_type, "SMART_CHANNEL")
        self.assertEqual(campaign_payloads[0].status, "CAMPAIGN_PAUSED") # Script default

        # SmartCampaignSetting (Update operation)
        scs_payloads = find_op_payloads("smart_campaign_setting_operation")
        self.assertEqual(len(scs_payloads), 1)
        scs_update_obj = scs_payloads[0]
        self.assertEqual(scs_update_obj.resource_name, f"customers/{customer_id}/smartCampaignSettings/{_SMART_CAMPAIGN_TEMPORARY_ID}")
        self.assertEqual(scs_update_obj.business_name, business_name)
        self.assertFalse(scs_update_obj.business_profile_location) # Should not be set
        self.assertEqual(scs_update_obj.final_url, _LANDING_PAGE_URL)
        self.assertEqual(scs_update_obj.phone_number.country_code, _COUNTRY_CODE)
        self.assertEqual(scs_update_obj.phone_number.phone_number, _PHONE_NUMBER)


        # CampaignCriterion (Keywords + Location)
        cc_payloads = find_op_payloads("campaign_criterion_operation")
        # 1 from get_keyword_theme_suggestions (mocked to return 1)
        # + 1 from get_keyword_text_auto_completions (mocked to return 1 via keyword_text)
        # + 1 for location from suggestion_info
        self.assertEqual(len(cc_payloads), 3)

        # AdGroup
        ag_payloads = find_op_payloads("ad_group_operation")
        self.assertEqual(len(ag_payloads), 1)
        self.assertEqual(ag_payloads[0].type_, "ADGROUP_SMART_CAMPAIGN_ADS")
        self.assertEqual(ag_payloads[0].resource_name, f"customers/{customer_id}/adGroups/{_AD_GROUP_TEMPORARY_ID}")

        # AdGroupAd
        aga_payloads = find_op_payloads("ad_group_ad_operation")
        self.assertEqual(len(aga_payloads), 1)
        smart_ad_info = aga_payloads[0].ad.smart_campaign_ad
        self.assertEqual(len(smart_ad_info.headlines), 3) # Script ensures 3
        self.assertEqual(len(smart_ad_info.descriptions), 2) # Script ensures 2
        self.assertTrue(any(h.text == "Suggested Headline 1" for h in smart_ad_info.headlines))
        self.assertTrue(any(d.text == "Suggested Description 1" for d in smart_ad_info.descriptions))

if __name__ == '__main__':
    unittest.main()
