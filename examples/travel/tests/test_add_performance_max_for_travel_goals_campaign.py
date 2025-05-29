import unittest
from unittest import mock
import sys
import runpy
import argparse

# Alias for the script under test
from examples.travel import add_performance_max_for_travel_goals_campaign as pmax_travel_script
# For patching helpers
from examples.utils import example_helpers 

# Define fixed values for patched temporary IDs for predictability in tests
PATCHED_ASSET_TEMPORARY_ID = -10
PATCHED_BUDGET_TEMPORARY_ID = -20
PATCHED_CAMPAIGN_TEMPORARY_ID = -30
PATCHED_ASSET_GROUP_TEMPORARY_ID = -40
# next_temp_id in the script starts from ASSET_GROUP_TEMPORARY_ID - 1
PATCHED_INITIAL_NEXT_TEMP_ID = PATCHED_ASSET_GROUP_TEMPORARY_ID -1 

FIXED_PRINTABLE_DATETIME = "YYYY-MM-DDTHHMMSS"
MOCK_IMAGE_BYTES = b"mock_image_content"

# Helper function to apply all necessary patches for global constants and helpers
def patch_global_constants_and_helpers(func):
    @mock.patch.object(pmax_travel_script, 'ASSET_TEMPORARY_ID', PATCHED_ASSET_TEMPORARY_ID)
    @mock.patch.object(pmax_travel_script, 'BUDGET_TEMPORARY_ID', PATCHED_BUDGET_TEMPORARY_ID)
    @mock.patch.object(pmax_travel_script, 'CAMPAIGN_TEMPORARY_ID', PATCHED_CAMPAIGN_TEMPORARY_ID)
    @mock.patch.object(pmax_travel_script, 'ASSET_GROUP_TEMPORARY_ID', PATCHED_ASSET_GROUP_TEMPORARY_ID)
    @mock.patch.object(pmax_travel_script, 'next_temp_id', PATCHED_INITIAL_NEXT_TEMP_ID) # Initial value
    @mock.patch.object(example_helpers, 'get_printable_datetime', return_value=FIXED_PRINTABLE_DATETIME)
    @mock.patch.object(example_helpers, 'get_image_bytes_from_url', return_value=MOCK_IMAGE_BYTES)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


class TestAddPerformanceMaxForTravelGoals(unittest.TestCase):

    def setUp(self):
        self.mock_google_ads_client = mock.Mock(spec=pmax_travel_script.GoogleAdsClient)

        # Mock Services
        self.mock_google_ads_service = mock.Mock()
        self.mock_travel_asset_suggestion_service = mock.Mock()
        self.mock_asset_set_service = mock.Mock()

        def get_service_side_effect(service_name, version=None):
            if service_name == "GoogleAdsService":
                return self.mock_google_ads_service
            elif service_name == "TravelAssetSuggestionService":
                return self.mock_travel_asset_suggestion_service
            elif service_name == "AssetSetService":
                return self.mock_asset_set_service
            return mock.DEFAULT
        self.mock_google_ads_client.get_service.side_effect = get_service_side_effect

        # Mock GoogleAdsService path methods to use patched temp IDs
        # These need to be configured to return strings that reflect the patched IDs
        self.mock_google_ads_service.asset_path.side_effect = \
            lambda cust_id, asset_id: f"customers/{cust_id}/assets/{asset_id}"
        self.mock_google_ads_service.campaign_budget_path.side_effect = \
            lambda cust_id, budget_id: f"customers/{cust_id}/campaignBudgets/{budget_id}"
        self.mock_google_ads_service.campaign_path.side_effect = \
            lambda cust_id, camp_id: f"customers/{cust_id}/campaigns/{camp_id}"
        self.mock_google_ads_service.asset_group_path.side_effect = \
            lambda cust_id, ag_id: f"customers/{cust_id}/assetGroups/{ag_id}"
        
        # Mock GoogleAdsService.mutate (default behavior, can be overridden in tests)
        self.mock_google_ads_service.mutate.return_value = mock.Mock(mutate_operation_responses=[])


        # Mock AssetSetService.mutate_asset_sets
        self.mock_asset_set_service.mutate_asset_sets.return_value = mock.Mock(results=[])
        
        # Mock TravelAssetSuggestionService.suggest_travel_assets
        self.mock_travel_asset_suggestion_service.suggest_travel_assets.return_value = mock.Mock(hotel_asset_suggestions=[])

        # Mock Enums (add more as needed by specific tests)
        self.mock_google_ads_client.enums.AssetFieldTypeEnum = mock.MagicMock()
        self.mock_google_ads_client.enums.AssetSetTypeEnum = mock.MagicMock()
        self.mock_google_ads_client.enums.HotelAssetSuggestionStatusEnum = mock.MagicMock()
        self.mock_google_ads_client.enums.HotelAssetSuggestionStatusEnum.SUCCESS = "SUCCESS"
        self.mock_google_ads_client.enums.HotelAssetSuggestionStatusEnum.HOTEL_NOT_FOUND = "HOTEL_NOT_FOUND" # Example
        self.mock_google_ads_client.enums.BudgetDeliveryMethodEnum = mock.MagicMock()
        self.mock_google_ads_client.enums.CampaignStatusEnum = mock.MagicMock()
        self.mock_google_ads_client.enums.AdvertisingChannelTypeEnum = mock.MagicMock()
        self.mock_google_ads_client.enums.AssetGroupStatusEnum = mock.MagicMock()
        self.mock_google_ads_client.enums.CallToActionTypeEnum = mock.MagicMock()


        # Mock GetType (return simple mocks, as copy_from is not used)
        # Attributes will be set directly on these mocks by the script.
        def get_type_side_effect(type_name, version=None):
            mock_obj = mock.Mock(name=type_name)
            # For operations, ensure 'create' attribute exists if script uses it like op.create.field = ...
            # Based on script, it's usually op.operation_type.create.field = ...
            # e.g., operation.asset_operation.create
            if type_name == "MutateOperation":
                mock_obj.asset_operation = mock.Mock(create=mock.Mock(name="Asset"))
                mock_obj.asset_set_asset_operation = mock.Mock(create=mock.Mock(name="AssetSetAsset"))
                mock_obj.campaign_budget_operation = mock.Mock(create=mock.Mock(name="CampaignBudget"))
                mock_obj.campaign_operation = mock.Mock(create=mock.Mock(name="Campaign"))
                mock_obj.asset_group_operation = mock.Mock(create=mock.Mock(name="AssetGroup"))
                mock_obj.asset_group_asset_operation = mock.Mock(create=mock.Mock(name="AssetGroupAsset"))
            elif type_name == "AssetSetOperation": # For create_hotel_asset_set
                 mock_obj.create = mock.Mock(name="AssetSet")
            elif type_name == "SuggestTravelAssetsRequest": # For get_hotel_asset_suggestion
                mock_obj.place_ids = [] # It's a repeated field
            return mock_obj
        self.mock_google_ads_client.get_type.side_effect = get_type_side_effect

    @patch_global_constants_and_helpers
    @mock.patch.object(pmax_travel_script, 'main') # Mock the script's main
    @mock.patch.object(pmax_travel_script, 'GoogleAdsClient') # Mock the client class itself
    def test_google_ads_client_load(self, mock_google_ads_client_class, mock_main_script_func, *_): # Capture patched args
        # Configure the class mock's load_from_storage method
        mock_ads_client_instance = mock.Mock()
        mock_google_ads_client_class.load_from_storage.return_value = mock_ads_client_instance
        
        original_argv = sys.argv
        test_argv = [
            'add_performance_max_for_travel_goals_campaign.py',
            '--customer_id', 'cust123',
            '--place_id', 'placeABC'
        ]
        sys.argv = test_argv
        try:
            # runpy will execute the __main__ block of the script
            runpy.run_module('examples.travel.add_performance_max_for_travel_goals_campaign', run_name='__main__', alter_sys=True)
        finally:
            sys.argv = original_argv
            
        mock_google_ads_client_class.load_from_storage.assert_called_once_with(version="v19")
        mock_main_script_func.assert_called_once_with(
            mock_ads_client_instance,
            'cust123',
            'placeABC'
        )

    @patch_global_constants_and_helpers
    @mock.patch.object(pmax_travel_script, 'main')
    @mock.patch.object(pmax_travel_script, 'GoogleAdsClient')
    def test_argument_parsing(self, mock_google_ads_client_class, mock_main_script_func, *_):
        mock_ads_client_instance = mock.Mock()
        mock_google_ads_client_class.load_from_storage.return_value = mock_ads_client_instance

        expected_customer_id = "customer_test_789"
        expected_place_id = "ChIJN1t_tDeuEmsRUsoyG83frY4" # Example Place ID

        original_argv = sys.argv
        test_argv = [
            'add_performance_max_for_travel_goals_campaign.py',
            '--customer_id', expected_customer_id,
            '--place_id', expected_place_id
        ]
        sys.argv = test_argv
        try:
            runpy.run_module('examples.travel.add_performance_max_for_travel_goals_campaign', run_name='__main__', alter_sys=True)
        finally:
            sys.argv = original_argv
        
        mock_main_script_func.assert_called_once_with(
            mock_ads_client_instance,
            expected_customer_id,
            expected_place_id
        )

    @patch_global_constants_and_helpers
    def test_get_hotel_asset_suggestion_success(self, *_): # Patched args
        mock_suggestion = mock.Mock()
        mock_suggestion.status = self.mock_google_ads_client.enums.HotelAssetSuggestionStatusEnum.SUCCESS
        mock_suggestion.hotel_name = "Test Hotel"
        
        self.mock_travel_asset_suggestion_service.suggest_travel_assets.return_value = mock.Mock(
            hotel_asset_suggestions=[mock_suggestion]
        )
        
        customer_id = "cust123"
        place_id = "place_abc"
        
        result = pmax_travel_script.get_hotel_asset_suggestion(
            self.mock_google_ads_client, customer_id, place_id
        )
        
        self.mock_travel_asset_suggestion_service.suggest_travel_assets.assert_called_once()
        call_args = self.mock_travel_asset_suggestion_service.suggest_travel_assets.call_args
        request_arg = call_args[1]['request'] # request is a keyword argument
        
        self.assertEqual(request_arg.customer_id, customer_id)
        self.assertEqual(request_arg.language_option, "en-US")
        self.assertIn(place_id, request_arg.place_ids)
        self.assertEqual(result, mock_suggestion)

    @patch_global_constants_and_helpers
    def test_get_hotel_asset_suggestion_with_non_success_status(self, *_):
        mock_suggestion_non_success = mock.Mock()
        # Example of a non-SUCCESS status; the actual enum values would be on the client mock
        self.mock_google_ads_client.enums.HotelAssetSuggestionStatusEnum.HOTEL_NOT_FOUND = "HOTEL_NOT_FOUND"
        mock_suggestion_non_success.status = self.mock_google_ads_client.enums.HotelAssetSuggestionStatusEnum.HOTEL_NOT_FOUND
        
        self.mock_travel_asset_suggestion_service.suggest_travel_assets.return_value = mock.Mock(
            hotel_asset_suggestions=[mock_suggestion_non_success]
        )
        
        customer_id = "cust456"
        place_id = "place_xyz"
        
        result = pmax_travel_script.get_hotel_asset_suggestion(
            self.mock_google_ads_client, customer_id, place_id
        )
        
        self.mock_travel_asset_suggestion_service.suggest_travel_assets.assert_called_once()
        self.assertEqual(result, mock_suggestion_non_success)
        self.assertEqual(result.status, "HOTEL_NOT_FOUND")

    @patch_global_constants_and_helpers
    def test_create_multiple_text_assets_suggestions_only_headline(self, *_):
        customer_id = "cust_text_assets"
        asset_field_type_headline = self.mock_google_ads_client.enums.AssetFieldTypeEnum.HEADLINE
        
        # Mock hotel_asset_suggestion
        mock_suggestion = mock.Mock()
        mock_suggestion.status = self.mock_google_ads_client.enums.HotelAssetSuggestionStatusEnum.SUCCESS
        
        # Provide 3 headline suggestions (assuming MIN_REQUIRED is 3 for HEADLINE)
        suggested_texts = ["Suggested Headline 1", "Suggested Headline 2", "Suggested Headline 3"]
        mock_suggestion.text_assets = [
            mock.Mock(asset_field_type=asset_field_type_headline, text=t) for t in suggested_texts
        ]
        
        # Mock GoogleAdsService.mutate response
        expected_resource_names = [f"assets/res_headline_{i+1}" for i in range(len(suggested_texts))]
        mock_responses = []
        for name in expected_resource_names:
            op_res = mock.Mock()
            op_res.asset_result.resource_name = name
            mock_responses.append(op_res)
        self.mock_google_ads_service.mutate.return_value = mock.Mock(mutate_operation_responses=mock_responses)
        
        # Call the function
        result_resource_names = pmax_travel_script.create_multiple_text_assets(
            self.mock_google_ads_client,
            customer_id,
            asset_field_type_headline,
            mock_suggestion
        )
        
        self.assertEqual(result_resource_names, expected_resource_names)
        self.mock_google_ads_service.mutate.assert_called_once()
        call_args = self.mock_google_ads_service.mutate.call_args
        self.assertEqual(call_args[1]['customer_id'], customer_id)
        
        operations = call_args[1]['mutate_operations']
        self.assertEqual(len(operations), len(suggested_texts))
        
        for i, operation in enumerate(operations):
            self.assertTrue(operation.asset_operation.create)
            self.assertEqual(operation.asset_operation.create.text_asset.text, suggested_texts[i])
            # Check other asset fields if necessary, e.g., name, type
            
    @patch_global_constants_and_helpers
    def test_create_multiple_text_assets_defaults_only_description(self, *_):
        customer_id = "cust_defaults"
        asset_field_type_desc = self.mock_google_ads_client.enums.AssetFieldTypeEnum.DESCRIPTION
        self.mock_google_ads_client.enums.AssetFieldTypeEnum.DESCRIPTION.name = "DESCRIPTION" # Needed for dict key

        # Mock hotel_asset_suggestion with no relevant suggestions
        mock_suggestion = mock.Mock()
        mock_suggestion.status = self.mock_google_ads_client.enums.HotelAssetSuggestionStatusEnum.SUCCESS
        mock_suggestion.text_assets = [] # No description suggestions
        
        # Determine expected number of default descriptions
        # From script: MIN_REQUIRED_TEXT_ASSET_COUNTS["DESCRIPTION"] = 2
        # DEFAULT_TEXT_ASSETS_INFO["DESCRIPTION"] = ["Great deal...", "Best rate..."]
        num_default_descriptions = pmax_travel_script.MIN_REQUIRED_TEXT_ASSET_COUNTS["DESCRIPTION"]
        default_descriptions = pmax_travel_script.DEFAULT_TEXT_ASSETS_INFO["DESCRIPTION"][:num_default_descriptions]

        expected_resource_names = [f"assets/res_desc_default_{i+1}" for i in range(num_default_descriptions)]
        mock_responses = []
        for name in expected_resource_names:
            op_res = mock.Mock()
            op_res.asset_result.resource_name = name
            mock_responses.append(op_res)
        self.mock_google_ads_service.mutate.return_value = mock.Mock(mutate_operation_responses=mock_responses)

        result_resource_names = pmax_travel_script.create_multiple_text_assets(
            self.mock_google_ads_client,
            customer_id,
            asset_field_type_desc,
            mock_suggestion
        )

        self.assertEqual(result_resource_names, expected_resource_names)
        self.mock_google_ads_service.mutate.assert_called_once()
        call_args = self.mock_google_ads_service.mutate.call_args
        operations = call_args[1]['mutate_operations']
        self.assertEqual(len(operations), num_default_descriptions)

        for i, operation in enumerate(operations):
            self.assertTrue(operation.asset_operation.create)
            self.assertEqual(operation.asset_operation.create.text_asset.text, default_descriptions[i])

    @patch_global_constants_and_helpers
    def test_create_multiple_text_assets_mixed_headline(self, *_):
        customer_id = "cust_mixed_headline"
        asset_field_type_headline = self.mock_google_ads_client.enums.AssetFieldTypeEnum.HEADLINE
        self.mock_google_ads_client.enums.AssetFieldTypeEnum.HEADLINE.name = "HEADLINE"

        # Provide 1 headline suggestion (MIN_REQUIRED is 3)
        suggested_headline = "Suggested Unique Headline"
        mock_suggestion = mock.Mock()
        mock_suggestion.status = self.mock_google_ads_client.enums.HotelAssetSuggestionStatusEnum.SUCCESS
        mock_suggestion.text_assets = [
            mock.Mock(asset_field_type=asset_field_type_headline, text=suggested_headline)
        ]

        # Expected: 1 suggested + 2 defaults
        num_expected_assets = pmax_travel_script.MIN_REQUIRED_TEXT_ASSET_COUNTS["HEADLINE"]
        default_headlines_needed = num_expected_assets - 1
        default_headlines = pmax_travel_script.DEFAULT_TEXT_ASSETS_INFO["HEADLINE"][:default_headlines_needed]
        
        all_expected_texts = [suggested_headline] + default_headlines

        expected_resource_names = [f"assets/res_mixed_hl_{i+1}" for i in range(num_expected_assets)]
        mock_responses = []
        for name in expected_resource_names:
            op_res = mock.Mock()
            op_res.asset_result.resource_name = name
            mock_responses.append(op_res)
        self.mock_google_ads_service.mutate.return_value = mock.Mock(mutate_operation_responses=mock_responses)

        result_resource_names = pmax_travel_script.create_multiple_text_assets(
            self.mock_google_ads_client,
            customer_id,
            asset_field_type_headline,
            mock_suggestion
        )
        self.assertEqual(result_resource_names, expected_resource_names)
        self.mock_google_ads_service.mutate.assert_called_once()
        call_args = self.mock_google_ads_service.mutate.call_args
        operations = call_args[1]['mutate_operations']
        self.assertEqual(len(operations), num_expected_assets)

        for i, operation in enumerate(operations):
            self.assertTrue(operation.asset_operation.create)
            self.assertEqual(operation.asset_operation.create.text_asset.text, all_expected_texts[i])

    @patch_global_constants_and_helpers
    def test_create_hotel_asset_set(self, *_):
        customer_id = "cust_asset_set"
        expected_asset_set_resource_name = f"assetSets/asset_set_1"
        
        # Mock AssetSetService.mutate_asset_sets response
        mock_result = mock.Mock()
        mock_result.resource_name = expected_asset_set_resource_name
        self.mock_asset_set_service.mutate_asset_sets.return_value = mock.Mock(results=[mock_result])

        # Call the function
        returned_resource_name = pmax_travel_script.create_hotel_asset_set(
            self.mock_google_ads_client, customer_id
        )

        self.assertEqual(returned_resource_name, expected_asset_set_resource_name)
        self.mock_asset_set_service.mutate_asset_sets.assert_called_once()
        call_args = self.mock_asset_set_service.mutate_asset_sets.call_args
        self.assertEqual(call_args[1]['customer_id'], customer_id)
        
        operations = call_args[1]['operations']
        self.assertEqual(len(operations), 1)
        
        created_asset_set = operations[0].create
        self.assertIn(FIXED_PRINTABLE_DATETIME, created_asset_set.name)
        self.assertEqual(created_asset_set.type_, self.mock_google_ads_client.enums.AssetSetTypeEnum.HOTEL_PROPERTY)

    @patch_global_constants_and_helpers
    def test_create_hotel_asset(self, *_):
        customer_id = "cust_hotel_asset"
        place_id = "place_for_hotel_asset"
        asset_set_resource_name = "assetSets/linked_asset_set"
        
        # Expected temporary asset resource name using the patched ASSET_TEMPORARY_ID
        expected_temp_asset_res_name = f"customers/{customer_id}/assets/{PATCHED_ASSET_TEMPORARY_ID}"
        
        # Mock GoogleAdsService.mutate response
        # The function returns the resource name from the first operation (asset creation)
        mock_asset_result = mock.Mock()
        mock_asset_result.asset_result.resource_name = "assets/final_hotel_prop_asset_id" # Final, not temp
        
        # The second operation is AssetSetAsset, its result is not directly returned by function but is part of the call
        mock_asset_set_asset_result = mock.Mock() 
        mock_asset_set_asset_result.asset_set_asset_result.resource_name = "assetSetAssets/link_id"

        self.mock_google_ads_service.mutate.return_value = mock.Mock(
            mutate_operation_responses=[mock_asset_result, mock_asset_set_asset_result]
        )

        returned_asset_name = pmax_travel_script.create_hotel_asset(
            self.mock_google_ads_client, customer_id, place_id, asset_set_resource_name
        )

        self.assertEqual(returned_asset_name, "assets/final_hotel_prop_asset_id")
        self.mock_google_ads_service.mutate.assert_called_once()
        call_args = self.mock_google_ads_service.mutate.call_args
        self.assertEqual(call_args[1]['customer_id'], customer_id)
        
        operations = call_args[1]['mutate_operations']
        self.assertEqual(len(operations), 2)

        # Check AssetOperation
        asset_op_create = operations[0].asset_operation.create
        self.assertEqual(asset_op_create.resource_name, expected_temp_asset_res_name)
        self.assertEqual(asset_op_create.hotel_property_asset.place_id, place_id)

        # Check AssetSetAssetOperation
        asset_set_asset_op_create = operations[1].asset_set_asset_operation.create
        self.assertEqual(asset_set_asset_op_create.asset, expected_temp_asset_res_name)
        self.assertEqual(asset_set_asset_op_create.asset_set, asset_set_resource_name)

    @patch_global_constants_and_helpers
    def test_create_campaign_budget_operation(self, *_):
        customer_id = "cust_budget_op"
        
        # Expected resource name using patched BUDGET_TEMPORARY_ID
        expected_budget_res_name = f"customers/{customer_id}/campaignBudgets/{PATCHED_BUDGET_TEMPORARY_ID}"

        operation = pmax_travel_script.create_campaign_budget_operation(
            self.mock_google_ads_client, customer_id
        )

        self.assertIsNotNone(operation.campaign_budget_operation)
        budget_create = operation.campaign_budget_operation.create
        
        self.assertEqual(budget_create.resource_name, expected_budget_res_name)
        self.assertIn(FIXED_PRINTABLE_DATETIME, budget_create.name)
        self.assertEqual(budget_create.amount_micros, 50000000)
        self.assertEqual(budget_create.delivery_method, self.mock_google_ads_client.enums.BudgetDeliveryMethodEnum.STANDARD)
        self.assertEqual(budget_create.explicitly_shared, False)

    @patch_global_constants_and_helpers
    def test_create_campaign_operation(self, *_):
        customer_id = "cust_camp_op"
        hotel_property_asset_set_resource_name = "assetSets/hotel_set_123"

        # Expected resource names using patched temporary IDs
        expected_campaign_res_name = f"customers/{customer_id}/campaigns/{PATCHED_CAMPAIGN_TEMPORARY_ID}"
        expected_budget_res_name = f"customers/{customer_id}/campaignBudgets/{PATCHED_BUDGET_TEMPORARY_ID}"

        # Mock the get_printable_datetime directly for campaign name as it's called inside the function
        # The decorator patches the one in example_helpers, but the script might have its own import or direct call.
        # The script uses from examples.utils.example_helpers import get_printable_datetime, so decorator is fine.

        operation = pmax_travel_script.create_campaign_operation(
            self.mock_google_ads_client, customer_id, hotel_property_asset_set_resource_name
        )

        self.assertIsNotNone(operation.campaign_operation)
        campaign_create = operation.campaign_operation.create

        self.assertEqual(campaign_create.resource_name, expected_campaign_res_name)
        self.assertIn(FIXED_PRINTABLE_DATETIME, campaign_create.name) # Check if fixed datetime is used
        self.assertEqual(campaign_create.campaign_budget, expected_budget_res_name)
        self.assertEqual(campaign_create.status, self.mock_google_ads_client.enums.CampaignStatusEnum.PAUSED)
        self.assertEqual(campaign_create.advertising_channel_type, self.mock_google_ads_client.enums.AdvertisingChannelTypeEnum.PERFORMANCE_MAX)
        self.assertEqual(campaign_create.hotel_property_asset_set, hotel_property_asset_set_resource_name)
        self.assertIsNotNone(campaign_create.maximize_conversion_value)
        self.assertEqual(campaign_create.maximize_conversion_value.target_roas, 3.5)

    @patch_global_constants_and_helpers
    def test_create_text_asset_and_asset_group_asset_operations(self, *_):
        customer_id = "cust_text_aga_op"
        text_content = "Amazing Text Asset"
        field_type_enum = self.mock_google_ads_client.enums.AssetFieldTypeEnum.BUSINESS_NAME
        
        # next_temp_id is patched to PATCHED_INITIAL_NEXT_TEMP_ID (-41) by the decorator for each test.
        # This function will use this ID and then decrement it.
        current_temp_id_val = PATCHED_INITIAL_NEXT_TEMP_ID 
        
        expected_asset_res_name = f"customers/{customer_id}/assets/{current_temp_id_val}"
        expected_asset_group_res_name = f"customers/{customer_id}/assetGroups/{PATCHED_ASSET_GROUP_TEMPORARY_ID}"

        operations = pmax_travel_script.create_text_asset_and_asset_group_asset_operations(
            self.mock_google_ads_client, customer_id, text_content, field_type_enum
        )
        self.assertEqual(len(operations), 2)

        # Check AssetOperation
        asset_op = operations[0]
        self.assertIsNotNone(asset_op.asset_operation.create)
        created_asset = asset_op.asset_operation.create
        self.assertEqual(created_asset.resource_name, expected_asset_res_name)
        self.assertEqual(created_asset.text_asset.text, text_content)

        # Check AssetGroupAssetOperation
        aga_op = operations[1]
        self.assertIsNotNone(aga_op.asset_group_asset_operation.create)
        created_aga = aga_op.asset_group_asset_operation.create
        self.assertEqual(created_aga.asset, expected_asset_res_name)
        self.assertEqual(created_aga.asset_group, expected_asset_group_res_name)
        self.assertEqual(created_aga.field_type, field_type_enum)
        
        # Verify that next_temp_id was decremented in the script's module
        # This requires next_temp_id to be patched in a way that allows reading its value,
        # or by checking the ID used in a subsequent call.
        # The decorator patches it. We can check its value after the call if the patch allows.
        # For a simple value patch, this check is tricky.
        # A more robust check is to see if a subsequent call uses the decremented ID.
        
        # Call it again to see if next_temp_id was decremented
        next_expected_temp_id_val = PATCHED_INITIAL_NEXT_TEMP_ID - 1
        expected_asset_res_name_2 = f"customers/{customer_id}/assets/{next_expected_temp_id_val}"

        # Temporarily re-patch next_temp_id in the script module to what it should be *after* the first call
        # This is because the decorator resets it to PATCHED_INITIAL_NEXT_TEMP_ID for each test *method*,
        # not for each call within the method. The script's global is modified.
        with mock.patch.object(pmax_travel_script, 'next_temp_id', current_temp_id_val -1):
            operations2 = pmax_travel_script.create_text_asset_and_asset_group_asset_operations(
                self.mock_google_ads_client, customer_id, "Second Text", field_type_enum
            )
            self.assertEqual(operations2[0].asset_operation.create.resource_name, expected_asset_res_name_2)


    @patch_global_constants_and_helpers
    def test_create_image_asset_and_asset_group_asset_operations(self, *_):
        customer_id = "cust_img_aga_op"
        image_url = "http://example.com/image.png"
        asset_name = "My Test Image"
        field_type_enum = self.mock_google_ads_client.enums.AssetFieldTypeEnum.MARKETING_IMAGE
        
        current_temp_id_val = PATCHED_INITIAL_NEXT_TEMP_ID

        expected_asset_res_name = f"customers/{customer_id}/assets/{current_temp_id_val}"
        expected_asset_group_res_name = f"customers/{customer_id}/assetGroups/{PATCHED_ASSET_GROUP_TEMPORARY_ID}"

        operations = pmax_travel_script.create_image_asset_and_image_asset_group_asset_operations(
            self.mock_google_ads_client, customer_id, image_url, field_type_enum, asset_name
        )
        self.assertEqual(len(operations), 2)
        
        # Check AssetOperation
        asset_op = operations[0]
        created_asset = asset_op.asset_operation.create
        self.assertEqual(created_asset.resource_name, expected_asset_res_name)
        self.assertEqual(created_asset.name, asset_name)
        self.assertEqual(created_asset.image_asset.data, MOCK_IMAGE_BYTES) # from patched get_image_bytes_from_url

        # Check AssetGroupAssetOperation
        aga_op = operations[1]
        created_aga = aga_op.asset_group_asset_operation.create
        self.assertEqual(created_aga.asset, expected_asset_res_name)
        self.assertEqual(created_aga.asset_group, expected_asset_group_res_name)
        self.assertEqual(created_aga.field_type, field_type_enum)
        
        # Check if get_image_bytes_from_url was called
        # The decorator patches example_helpers.get_image_bytes_from_url
        example_helpers.get_image_bytes_from_url.assert_called_once_with(image_url)

    @patch_global_constants_and_helpers
    @mock.patch.object(pmax_travel_script, 'create_text_asset_and_asset_group_asset_operations')
    def test_create_text_assets_for_asset_group(self, mock_create_text_aga_ops, *_):
        customer_id = "cust_text_assets_for_ag"
        
        # Let the mocked helper return a unique pair of operations for each call
        mock_op_pair1 = [mock.Mock(name="AssetOp1_TextForAG"), mock.Mock(name="AGAssetOp1_TextForAG")]
        mock_op_pair2 = [mock.Mock(name="AssetOp2_TextForAG"), mock.Mock(name="AGAssetOp2_TextForAG")]
        mock_create_text_aga_ops.side_effect = [mock_op_pair1, mock_op_pair2] # Example for 2 calls

        # Mock hotel_asset_suggestion
        # Scenario: One suggested BUSINESS_NAME, LONG_HEADLINE will come from defaults.
        # HEADLINE and DESCRIPTION are skipped by this function.
        mock_suggestion = mock.Mock()
        mock_suggestion.status = self.mock_google_ads_client.enums.HotelAssetSuggestionStatusEnum.SUCCESS
        
        suggested_business_name_text = "Suggested Business Name"
        mock_suggestion.text_assets = [
            mock.Mock(
                asset_field_type=self.mock_google_ads_client.enums.AssetFieldTypeEnum.BUSINESS_NAME, 
                text=suggested_business_name_text
            ),
            mock.Mock( # This headline should be ignored by this function
                asset_field_type=self.mock_google_ads_client.enums.AssetFieldTypeEnum.HEADLINE,
                text="Ignored Suggested Headline"
            )
        ]
        
        # Configure enum names for dictionary lookups in the script
        self.mock_google_ads_client.enums.AssetFieldTypeEnum.BUSINESS_NAME.name = "BUSINESS_NAME"
        self.mock_google_ads_client.enums.AssetFieldTypeEnum.LONG_HEADLINE.name = "LONG_HEADLINE"
        # Ensure HEADLINE and DESCRIPTION are also configured if the loop touches them before skipping
        self.mock_google_ads_client.enums.AssetFieldTypeEnum.HEADLINE.name = "HEADLINE"
        self.mock_google_ads_client.enums.AssetFieldTypeEnum.DESCRIPTION.name = "DESCRIPTION"


        # MIN_REQUIRED_TEXT_ASSET_COUNTS: HEADLINE:3, LONG_HEADLINE:1, DESCRIPTION:2, BUSINESS_NAME:1
        # DEFAULT_TEXT_ASSETS_INFO: LONG_HEADLINE: ["Travel the World"]
        
        # Expected calls to the helper:
        # 1. For suggested BUSINESS_NAME
        # 2. For default LONG_HEADLINE (since it's in MIN_REQUIRED and not HEADLINE/DESCRIPTION)
        
        operations = pmax_travel_script.create_text_assets_for_asset_group(
            self.mock_google_ads_client, customer_id, mock_suggestion
        )

        self.assertEqual(len(operations), 4) # 2 calls to helper, each returns 2 ops
        self.assertEqual(operations, mock_op_pair1 + mock_op_pair2)
        
        expected_calls_to_helper = [
            # Call 1: For suggested BUSINESS_NAME
            mock.call(
                self.mock_google_ads_client,
                customer_id,
                suggested_business_name_text,
                self.mock_google_ads_client.enums.AssetFieldTypeEnum.BUSINESS_NAME
            ),
            # Call 2: For default LONG_HEADLINE
            mock.call(
                self.mock_google_ads_client,
                customer_id,
                pmax_travel_script.DEFAULT_TEXT_ASSETS_INFO["LONG_HEADLINE"][0],
                self.mock_google_ads_client.enums.AssetFieldTypeEnum.LONG_HEADLINE # resolved from "LONG_HEADLINE" string
            ),
        ]
        mock_create_text_aga_ops.assert_has_calls(expected_calls_to_helper)
        self.assertEqual(mock_create_text_aga_ops.call_count, 2)

    @patch_global_constants_and_helpers
    @mock.patch.object(pmax_travel_script, 'create_image_asset_and_image_asset_group_asset_operations')
    def test_create_image_assets_for_asset_group(self, mock_create_image_aga_ops, *_):
        customer_id = "cust_img_assets_for_ag"

        # Mock return value for the helper
        mock_op_pairs = [
            [mock.Mock(name=f"AssetOp{i+1}_ImgForAG"), mock.Mock(name=f"AGAssetOp{i+1}_ImgForAG")] 
            for i in range(3) # Assuming 3 calls to the helper in this scenario
        ]
        mock_create_image_aga_ops.side_effect = mock_op_pairs

        # Mock hotel_asset_suggestion
        # Scenario: One suggested MARKETING_IMAGE. SQUARE_MARKETING_IMAGE and LOGO from defaults.
        mock_suggestion = mock.Mock()
        # Suggestion status doesn't directly affect this function's logic for image assets, 
        # but good to set for consistency.
        mock_suggestion.status = self.mock_google_ads_client.enums.HotelAssetSuggestionStatusEnum.SUCCESS 
        
        suggested_marketing_image_url = "http://example.com/suggested_marketing.jpg"
        mock_suggestion.image_assets = [
            mock.Mock(
                asset_field_type=self.mock_google_ads_client.enums.AssetFieldTypeEnum.MARKETING_IMAGE,
                uri=suggested_marketing_image_url
            )
        ]

        # Configure enum names for dictionary lookups
        self.mock_google_ads_client.enums.AssetFieldTypeEnum.MARKETING_IMAGE.name = "MARKETING_IMAGE"
        self.mock_google_ads_client.enums.AssetFieldTypeEnum.SQUARE_MARKETING_IMAGE.name = "SQUARE_MARKETING_IMAGE"
        self.mock_google_ads_client.enums.AssetFieldTypeEnum.LOGO.name = "LOGO"

        # MIN_REQUIRED_IMAGE_ASSET_COUNTS: MARKETING_IMAGE:1, SQUARE_MARKETING_IMAGE:1, LOGO:1
        # DEFAULT_IMAGE_ASSETS_INFO provides URLs for these.

        # Expected calls to the helper:
        # 1. For suggested MARKETING_IMAGE
        # 2. For default SQUARE_MARKETING_IMAGE
        # 3. For default LOGO

        operations = pmax_travel_script.create_image_assets_for_asset_group(
            self.mock_google_ads_client, customer_id, mock_suggestion
        )

        self.assertEqual(len(operations), 6) # 3 calls to helper, each returns 2 ops
        self.assertEqual(operations, mock_op_pairs[0] + mock_op_pairs[1] + mock_op_pairs[2])

        expected_calls_to_helper = [
            # Call 1: For suggested MARKETING_IMAGE
            mock.call(
                self.mock_google_ads_client,
                customer_id,
                suggested_marketing_image_url,
                self.mock_google_ads_client.enums.AssetFieldTypeEnum.MARKETING_IMAGE,
                mock.ANY # Asset name is generated with datetime
            ),
            # Call 2: For default SQUARE_MARKETING_IMAGE
            mock.call(
                self.mock_google_ads_client,
                customer_id,
                pmax_travel_script.DEFAULT_IMAGE_ASSETS_INFO["SQUARE_MARKETING_IMAGE"][0],
                self.mock_google_ads_client.enums.AssetFieldTypeEnum.SQUARE_MARKETING_IMAGE,
                mock.ANY # Asset name
            ),
            # Call 3: For default LOGO
            mock.call(
                self.mock_google_ads_client,
                customer_id,
                pmax_travel_script.DEFAULT_IMAGE_ASSETS_INFO["LOGO"][0],
                self.mock_google_ads_client.enums.AssetFieldTypeEnum.LOGO,
                mock.ANY # Asset name
            ),
        ]
        
        # Check asset names for containing FIXED_PRINTABLE_DATETIME for default assets
        # For the suggested one, the name is "Suggested image asset #YYYY-MM-DDTHHMMSS"
        # For defaults, it's like "square_marketing_image YYYY-MM-DDTHHMMSS"
        self.assertIn(FIXED_PRINTABLE_DATETIME, mock_create_image_aga_ops.call_args_list[0][0][4]) # Suggested name
        self.assertIn("square_marketing_image", mock_create_image_aga_ops.call_args_list[1][0][4].lower())
        self.assertIn(FIXED_PRINTABLE_DATETIME, mock_create_image_aga_ops.call_args_list[1][0][4])
        self.assertIn("logo", mock_create_image_aga_ops.call_args_list[2][0][4].lower())
        self.assertIn(FIXED_PRINTABLE_DATETIME, mock_create_image_aga_ops.call_args_list[2][0][4])
        
        # Check calls (order might matter if not using assert_has_calls with any_order=True)
        # The current implementation iterates through suggestions first, then through MIN_REQUIRED.
        # So the order of calls should be: suggested, then defaults based on MIN_REQUIRED iteration order.
        # The `expected_calls_to_helper` list assumes this order.
        self.assertEqual(mock_create_image_aga_ops.call_args_list, expected_calls_to_helper)
        self.assertEqual(mock_create_image_aga_ops.call_count, 3)

    @patch_global_constants_and_helpers
    @mock.patch.object(pmax_travel_script, 'create_text_assets_for_asset_group')
    @mock.patch.object(pmax_travel_script, 'create_image_assets_for_asset_group')
    def test_create_asset_group_operations_with_cta(
        self, mock_create_image_ops_func, mock_create_text_ops_func, *_
    ):
        customer_id = "cust_ag_ops"
        hotel_property_asset_res_name = "assets/hotel_prop_asset"
        headline_res_names = ["assets/h1", "assets/h2"]
        description_res_names = ["assets/d1"]

        # Mock return values for helpers that create asset ops lists
        mock_text_ops_list = [mock.Mock(name="TextOp1"), mock.Mock(name="TextOp2")]
        mock_create_text_ops_func.return_value = mock_text_ops_list
        
        mock_image_ops_list = [mock.Mock(name="ImageOp1"), mock.Mock(name="ImageOp2")]
        mock_create_image_ops_func.return_value = mock_image_ops_list

        # Mock hotel_asset_suggestion with CTA
        mock_suggestion = mock.Mock()
        mock_suggestion.status = self.mock_google_ads_client.enums.HotelAssetSuggestionStatusEnum.SUCCESS
        mock_suggestion.hotel_name = "Grand Test Hotel"
        mock_suggestion.final_url = "http://grandtest.example.com"
        # Set up a specific mock for CallToActionTypeEnum.BOOK_NOW if not already general
        self.mock_google_ads_client.enums.CallToActionTypeEnum.BOOK_NOW = "BOOK_NOW_ENUM"
        mock_suggestion.call_to_action = self.mock_google_ads_client.enums.CallToActionTypeEnum.BOOK_NOW
        
        # Expected resource names using patched temp IDs
        expected_ag_res_name = f"customers/{customer_id}/assetGroups/{PATCHED_ASSET_GROUP_TEMPORARY_ID}"
        expected_campaign_res_name = f"customers/{customer_id}/campaigns/{PATCHED_CAMPAIGN_TEMPORARY_ID}"
        # CTA asset will use next_temp_id, which is PATCHED_INITIAL_NEXT_TEMP_ID for the first such use in this function
        expected_cta_asset_res_name = f"customers/{customer_id}/assets/{PATCHED_INITIAL_NEXT_TEMP_ID}"

        operations = pmax_travel_script.create_asset_group_operations(
            self.mock_google_ads_client,
            customer_id,
            hotel_property_asset_res_name,
            headline_res_names,
            description_res_names,
            mock_suggestion
        )
        
        # Expected operations:
        # 1 (AssetGroup)
        # + len(headline_res_names) (AssetGroupAsset for headlines)
        # + len(description_res_names) (AssetGroupAsset for descriptions)
        # + 1 (AssetGroupAsset for hotel_property_asset)
        # + len(mock_text_ops_list) (from create_text_assets_for_asset_group)
        # + len(mock_image_ops_list) (from create_image_assets_for_asset_group)
        # + 2 (AssetOperation for CTA, AssetGroupAsset for CTA)
        expected_op_count = 1 + len(headline_res_names) + len(description_res_names) + 1 \
                            + len(mock_text_ops_list) + len(mock_image_ops_list) + 2
        self.assertEqual(len(operations), expected_op_count)

        # 1. AssetGroupOperation
        ag_op = operations[0].asset_group_operation.create
        self.assertEqual(ag_op.resource_name, expected_ag_res_name)
        self.assertEqual(ag_op.name, "Grand Test Hotel")
        self.assertEqual(ag_op.campaign, expected_campaign_res_name)
        self.assertIn("http://grandtest.example.com", ag_op.final_urls)
        self.assertEqual(ag_op.status, self.mock_google_ads_client.enums.AssetGroupStatusEnum.PAUSED)

        # 2. AssetGroupAsset for headlines
        op_idx = 1
        for i, h_res_name in enumerate(headline_res_names):
            aga_h_op = operations[op_idx + i].asset_group_asset_operation.create
            self.assertEqual(aga_h_op.asset, h_res_name)
            self.assertEqual(aga_h_op.asset_group, expected_ag_res_name)
            self.assertEqual(aga_h_op.field_type, self.mock_google_ads_client.enums.AssetFieldTypeEnum.HEADLINE)
        op_idx += len(headline_res_names)

        # 3. AssetGroupAsset for descriptions
        for i, d_res_name in enumerate(description_res_names):
            aga_d_op = operations[op_idx + i].asset_group_asset_operation.create
            self.assertEqual(aga_d_op.asset, d_res_name)
            self.assertEqual(aga_d_op.asset_group, expected_ag_res_name)
            self.assertEqual(aga_d_op.field_type, self.mock_google_ads_client.enums.AssetFieldTypeEnum.DESCRIPTION)
        op_idx += len(description_res_names)
        
        # 4. AssetGroupAsset for Hotel Property
        aga_hp_op = operations[op_idx].asset_group_asset_operation.create
        self.assertEqual(aga_hp_op.asset, hotel_property_asset_res_name)
        self.assertEqual(aga_hp_op.asset_group, expected_ag_res_name)
        self.assertEqual(aga_hp_op.field_type, self.mock_google_ads_client.enums.AssetFieldTypeEnum.HOTEL_PROPERTY)
        op_idx += 1

        # 5. Operations from create_text_assets_for_asset_group mock
        for i in range(len(mock_text_ops_list)):
            self.assertEqual(operations[op_idx + i], mock_text_ops_list[i])
        op_idx += len(mock_text_ops_list)
        mock_create_text_ops_func.assert_called_once_with(self.mock_google_ads_client, customer_id, mock_suggestion)

        # 6. Operations from create_image_assets_for_asset_group mock
        for i in range(len(mock_image_ops_list)):
            self.assertEqual(operations[op_idx + i], mock_image_ops_list[i])
        op_idx += len(mock_image_ops_list)
        mock_create_image_ops_func.assert_called_once_with(self.mock_google_ads_client, customer_id, mock_suggestion)

        # 7. CallToAction AssetOperation
        cta_asset_op = operations[op_idx].asset_operation.create
        self.assertEqual(cta_asset_op.resource_name, expected_cta_asset_res_name)
        self.assertIn(FIXED_PRINTABLE_DATETIME, cta_asset_op.name)
        self.assertEqual(cta_asset_op.call_to_action_asset.call_to_action, self.mock_google_ads_client.enums.CallToActionTypeEnum.BOOK_NOW)
        op_idx += 1
        
        # 8. CallToAction AssetGroupAssetOperation
        cta_aga_op = operations[op_idx].asset_group_asset_operation.create
        self.assertEqual(cta_aga_op.asset, expected_cta_asset_res_name)
        self.assertEqual(cta_aga_op.asset_group, expected_ag_res_name)
        self.assertEqual(cta_aga_op.field_type, self.mock_google_ads_client.enums.AssetFieldTypeEnum.CALL_TO_ACTION_SELECTION)

    @patch_global_constants_and_helpers # Though not strictly needed here, good for consistency
    @mock.patch('builtins.print')
    def test_print_response_details(self, mock_print, *_):
        mock_response = mock.Mock()
        
        # Simulate various result types
        res_names = {
            "asset_result": "assets/my_asset",
            "asset_set_asset_result": "assetSetAssets/my_asa",
            "campaign_budget_result": "campaignBudgets/my_budget",
            "campaign_result": "campaigns/my_campaign",
            "asset_group_result": "assetGroups/my_ag",
            "asset_group_asset_result": "assetGroupAssets/my_aga"
        }
        
        mock_op_responses = []
        expected_print_calls = []

        for result_field, res_name_val in res_names.items():
            op_res = mock.Mock()
            # Clear all other potential result fields by setting them to None or a non-triggering value
            for key in res_names.keys():
                if key != result_field:
                    setattr(op_res, key, None) # Or mock.PropertyMock(side_effect=AttributeError) to be strict
                else: # Set the actual result field
                    res_obj = mock.Mock()
                    res_obj.resource_name = res_name_val
                    setattr(op_res, result_field, res_obj)
            mock_op_responses.append(op_res)
            
            # Determine resource_type string as per the function's logic
            resource_type_map = {
                "asset_result": "Asset", "asset_set_asset_result": "AssetSetAsset",
                "campaign_budget_result": "CampaignBudget", "campaign_result": "Campaign",
                "asset_group_result": "AssetGroup", "asset_group_asset_result": "AssetGroupAsset"
            }
            expected_print_calls.append(
                mock.call(f"Created a(n) {resource_type_map[result_field]} with resource_name: '{res_name_val}'.")
            )
            
        mock_response.mutate_operation_responses = mock_op_responses
        
        pmax_travel_script.print_response_details(mock_response)
        
        mock_print.assert_has_calls(expected_print_calls, any_order=False)
        self.assertEqual(mock_print.call_count, len(expected_print_calls))

    @patch_global_constants_and_helpers
    @mock.patch.object(pmax_travel_script, 'get_hotel_asset_suggestion')
    @mock.patch.object(pmax_travel_script, 'create_multiple_text_assets')
    @mock.patch.object(pmax_travel_script, 'create_hotel_asset_set')
    @mock.patch.object(pmax_travel_script, 'create_hotel_asset')
    @mock.patch.object(pmax_travel_script, 'create_campaign_budget_operation')
    @mock.patch.object(pmax_travel_script, 'create_campaign_operation')
    @mock.patch.object(pmax_travel_script, 'create_asset_group_operations')
    @mock.patch.object(pmax_travel_script, 'print_response_details')
    def test_main_combined_mutate_call(
        self, mock_print_details, mock_create_ag_ops, mock_create_camp_op, 
        mock_create_budget_op, mock_create_hotel_asset, mock_create_hotel_asset_set,
        mock_create_multi_text, mock_get_suggestion, *_):
        
        customer_id = "main_cust_id"
        place_id = "main_place_id"

        # Configure return values for mocked helpers
        mock_suggestion_obj = mock.Mock(name="HotelSuggestion")
        mock_get_suggestion.return_value = mock_suggestion_obj
        
        headline_names = ["assets/h1", "assets/h2"]
        desc_names = ["assets/d1", "assets/d2"]
        # create_multiple_text_assets is called twice
        mock_create_multi_text.side_effect = [headline_names, desc_names] 
        
        hotel_asset_set_name = "assetSets/hotel_set_main"
        mock_create_hotel_asset_set.return_value = hotel_asset_set_name
        
        hotel_property_asset_name = "assets/hotel_prop_main"
        mock_create_hotel_asset.return_value = hotel_property_asset_name
        
        mock_budget_op_obj = mock.Mock(name="BudgetOp")
        mock_create_budget_op.return_value = mock_budget_op_obj
        
        mock_camp_op_obj = mock.Mock(name="CampaignOp")
        mock_create_camp_op.return_value = mock_camp_op_obj
        
        mock_ag_ops_list = [mock.Mock(name="AG_Op1"), mock.Mock(name="AG_Op2")]
        mock_create_ag_ops.return_value = mock_ag_ops_list

        # Mock the final mutate call
        mock_final_mutate_response = mock.Mock(name="FinalMutateResponse")
        self.mock_google_ads_service.mutate.return_value = mock_final_mutate_response

        # Call main
        pmax_travel_script.main(self.mock_google_ads_client, customer_id, place_id)

        # Assert helpers were called
        mock_get_suggestion.assert_called_once_with(self.mock_google_ads_client, customer_id, place_id)
        mock_create_multi_text.assert_any_call(self.mock_google_ads_client, customer_id, self.mock_google_ads_client.enums.AssetFieldTypeEnum.HEADLINE, mock_suggestion_obj)
        mock_create_multi_text.assert_any_call(self.mock_google_ads_client, customer_id, self.mock_google_ads_client.enums.AssetFieldTypeEnum.DESCRIPTION, mock_suggestion_obj)
        mock_create_hotel_asset_set.assert_called_once_with(self.mock_google_ads_client, customer_id)
        mock_create_hotel_asset.assert_called_once_with(self.mock_google_ads_client, customer_id, place_id, hotel_asset_set_name)
        mock_create_budget_op.assert_called_once_with(self.mock_google_ads_client, customer_id)
        mock_create_camp_op.assert_called_once_with(self.mock_google_ads_client, customer_id, hotel_asset_set_name)
        mock_create_ag_ops.assert_called_once_with(
            self.mock_google_ads_client, customer_id, hotel_property_asset_name,
            headline_names, desc_names, mock_suggestion_obj
        )

        # Assert the main mutate call
        expected_operations = [
            mock_budget_op_obj,
            mock_camp_op_obj,
            *mock_ag_ops_list
        ]
        self.mock_google_ads_service.mutate.assert_called_once_with(
            customer_id=customer_id,
            mutate_operations=expected_operations
        )
        
        # Assert print_response_details was called
        mock_print_details.assert_called_once_with(mock_final_mutate_response)


if __name__ == '__main__':
    unittest.main()
