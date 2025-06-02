import unittest
from unittest.mock import patch, MagicMock, call, ANY
import argparse
import sys

# Add examples to sys.path to be able to import the script and its utils
sys.path.append(".") # For `examples.utils.example_helpers`
sys.path.append("examples") # For `travel.add_performance_max_for_travel_goals_campaign`

from travel import add_performance_max_for_travel_goals_campaign as script_under_test

# Mock values for global temporary IDs to ensure test predictability
script_under_test.ASSET_TEMPORARY_ID = -1
script_under_test.BUDGET_TEMPORARY_ID = -2
script_under_test.CAMPAIGN_TEMPORARY_ID = -3
script_under_test.ASSET_GROUP_TEMPORARY_ID = -4
script_under_test.next_temp_id = -5 # Initial value for other temp IDs


class TestAddPerformanceMaxForTravelGoalsCampaign(unittest.TestCase):

    def setUp(self):
        # Reset next_temp_id before each test, as it's modified globally
        script_under_test.next_temp_id = -5

    @patch("travel.add_performance_max_for_travel_goals_campaign.get_image_bytes_from_url")
    @patch("travel.add_performance_max_for_travel_goals_campaign.GoogleAdsClient.load_from_storage")
    @patch("travel.add_performance_max_for_travel_goals_campaign.argparse.ArgumentParser")
    def test_main(self, mock_argument_parser, mock_load_client, mock_get_image_bytes):
        mock_args = MagicMock()
        mock_args.customer_id = "test_customer_id"
        mock_args.place_id = "test_place_id"

        mock_parser_instance = mock_argument_parser.return_value
        mock_parser_instance.parse_args.return_value = mock_args

        mock_client = MagicMock()
        mock_load_client.return_value = mock_client

        mock_get_image_bytes.return_value = b"image_data"

        # Mock services
        mock_travel_asset_suggestion_service = MagicMock()
        mock_google_ads_service = MagicMock()
        mock_asset_set_service = MagicMock()
        mock_campaign_budget_service = MagicMock() # Though not directly used in main, operations are created
        mock_campaign_service = MagicMock() # Though not directly used in main, operations are created
        mock_asset_service = MagicMock() # Though not directly used in main, operations are created
        mock_asset_group_service = MagicMock() # Though not directly used in main, operations are created
        mock_asset_group_asset_service = MagicMock() # Though not directly used in main, operations are created


        def mock_get_service(service_name, version="v19"): # Add version default
            if service_name == "TravelAssetSuggestionService":
                return mock_travel_asset_suggestion_service
            elif service_name == "GoogleAdsService":
                return mock_google_ads_service
            elif service_name == "AssetSetService":
                return mock_asset_set_service
            # Add other services if they are directly called via client.get_service in main or helpers
            # For now, assuming operations are built and then sent via GoogleAdsService.mutate
            return MagicMock()

        mock_client.get_service.side_effect = mock_get_service

        # --- Mock responses ---
        # SuggestTravelAssets response
        mock_suggestion_response = MagicMock()
        mock_hotel_suggestion = MagicMock()
        mock_hotel_suggestion.status = mock_client.enums.HotelAssetSuggestionStatusEnum.SUCCESS
        mock_hotel_suggestion.text_assets = [
            MagicMock(asset_field_type=mock_client.enums.AssetFieldTypeEnum.HEADLINE, text="Suggested Headline 1"),
            MagicMock(asset_field_type=mock_client.enums.AssetFieldTypeEnum.DESCRIPTION, text="Suggested Description 1"),
            MagicMock(asset_field_type=mock_client.enums.AssetFieldTypeEnum.BUSINESS_NAME, text="Suggested Business"),
        ]
        mock_hotel_suggestion.image_assets = [
            MagicMock(uri="http://suggested.com/img1.png", asset_field_type=mock_client.enums.AssetFieldTypeEnum.MARKETING_IMAGE)
        ]
        mock_hotel_suggestion.hotel_name = "Suggested Hotel"
        mock_hotel_suggestion.final_url = "http://suggested-final.com"
        mock_hotel_suggestion.call_to_action = mock_client.enums.CallToActionEnum.BOOK_NOW


        mock_suggestion_response.hotel_asset_suggestions = [mock_hotel_suggestion]
        mock_travel_asset_suggestion_service.suggest_travel_assets.return_value = mock_suggestion_response

        # GoogleAdsService.mutate for text assets (headlines, descriptions)
        # This will be called multiple times, once for headlines, once for descriptions
        mock_text_asset_mutate_response_headline = MagicMock()
        mock_text_asset_mutate_response_headline.mutate_operation_responses = [
            MagicMock(asset_result=MagicMock(resource_name="assets/headline1")),
            MagicMock(asset_result=MagicMock(resource_name="assets/headline2")),
            MagicMock(asset_result=MagicMock(resource_name="assets/headline3")),
        ]
        mock_text_asset_mutate_response_description = MagicMock()
        mock_text_asset_mutate_response_description.mutate_operation_responses = [
            MagicMock(asset_result=MagicMock(resource_name="assets/description1")),
            MagicMock(asset_result=MagicMock(resource_name="assets/description2")),
        ]

        # AssetSetService.mutate_asset_sets response
        mock_asset_set_response = MagicMock()
        mock_asset_set_response.results[0].resource_name = "assetSets/hotel_set_1"
        mock_asset_set_service.mutate_asset_sets.return_value = mock_asset_set_response

        # GoogleAdsService.mutate for hotel property asset and asset_set_asset
        mock_hotel_asset_creation_response = MagicMock()
        mock_hotel_asset_creation_response.mutate_operation_responses = [
            MagicMock(asset_result=MagicMock(resource_name=f"customers/test_customer_id/assets/{script_under_test.ASSET_TEMPORARY_ID}")),
            MagicMock(asset_set_asset_result=MagicMock(resource_name="assetSetAssets/link1"))
        ]

        # GoogleAdsService.mutate for main campaign entities
        mock_main_mutate_response = MagicMock()
        # Simplistic; in reality, each operation in the batch would have a response
        mock_main_mutate_response.mutate_operation_responses = [
            MagicMock(campaign_budget_result=MagicMock(resource_name=f"customers/test_customer_id/campaignBudgets/{script_under_test.BUDGET_TEMPORARY_ID}")),
            MagicMock(campaign_result=MagicMock(resource_name=f"customers/test_customer_id/campaigns/{script_under_test.CAMPAIGN_TEMPORARY_ID}")),
            MagicMock(asset_group_result=MagicMock(resource_name=f"customers/test_customer_id/assetGroups/{script_under_test.ASSET_GROUP_TEMPORARY_ID}")),
            # ... responses for asset_group_asset operations
        ] * 10 # Placeholder for multiple asset group asset results

        # Configure side_effect for GoogleAdsService.mutate
        # It's called for: headlines, descriptions, hotel_asset, main campaign batch
        mock_google_ads_service.mutate.side_effect = [
            mock_text_asset_mutate_response_headline, # Headlines
            mock_text_asset_mutate_response_description, # Descriptions
            mock_hotel_asset_creation_response, # Hotel Property Asset + Link
            mock_main_mutate_response # Main batch
        ]


        # Mock path helpers (needed by operation creation functions)
        mock_google_ads_service.campaign_budget_path.side_effect = lambda cust_id, id: f"customers/{cust_id}/campaignBudgets/{id}"
        mock_google_ads_service.campaign_path.side_effect = lambda cust_id, id: f"customers/{cust_id}/campaigns/{id}"
        mock_google_ads_service.asset_path.side_effect = lambda cust_id, id: f"customers/{cust_id}/assets/{id}"
        mock_google_ads_service.asset_group_path.side_effect = lambda cust_id, id: f"customers/{cust_id}/assetGroups/{id}"

        # Mock types and enums (very basic, expand as needed by functions)
        mock_client.get_type.side_effect = lambda type_name: MagicMock(name=type_name)
        mock_client.enums.AssetFieldTypeEnum.HEADLINE = "HEADLINE"
        mock_client.enums.AssetFieldTypeEnum.DESCRIPTION = "DESCRIPTION"
        mock_client.enums.AssetFieldTypeEnum.BUSINESS_NAME = "BUSINESS_NAME"
        mock_client.enums.AssetFieldTypeEnum.MARKETING_IMAGE = "MARKETING_IMAGE"
        mock_client.enums.AssetFieldTypeEnum.SQUARE_MARKETING_IMAGE = "SQUARE_MARKETING_IMAGE"
        mock_client.enums.AssetFieldTypeEnum.LOGO = "LOGO"
        mock_client.enums.AssetFieldTypeEnum.HOTEL_PROPERTY = "HOTEL_PROPERTY"
        mock_client.enums.AssetFieldTypeEnum.CALL_TO_ACTION_SELECTION = "CALL_TO_ACTION_SELECTION"

        mock_client.enums.AssetSetTypeEnum.HOTEL_PROPERTY = "HOTEL_PROPERTY"
        mock_client.enums.BudgetDeliveryMethodEnum.STANDARD = "STANDARD"
        mock_client.enums.CampaignStatusEnum.PAUSED = "PAUSED"
        mock_client.enums.AdvertisingChannelTypeEnum.PERFORMANCE_MAX = "PERFORMANCE_MAX"
        mock_client.enums.AssetGroupStatusEnum.PAUSED = "PAUSED"
        mock_client.enums.HotelAssetSuggestionStatusEnum.SUCCESS = "SUCCESS"
        mock_client.enums.CallToActionEnum.BOOK_NOW = "BOOK_NOW"


        with patch("builtins.print") as mock_print:
            script_under_test.main(
                mock_client,
                mock_args.customer_id,
                mock_args.place_id,
            )

        mock_load_client.assert_called_once_with(version="v19")

        # Check that TravelAssetSuggestionService was called
        mock_travel_asset_suggestion_service.suggest_travel_assets.assert_called_once()
        suggest_request = mock_travel_asset_suggestion_service.suggest_travel_assets.call_args[1]['request']
        self.assertEqual(suggest_request.customer_id, "test_customer_id")
        self.assertEqual(suggest_request.place_ids[0], "test_place_id")

        # Check AssetSetService was called
        mock_asset_set_service.mutate_asset_sets.assert_called_once()

        # Check GoogleAdsService.mutate calls
        self.assertEqual(mock_google_ads_service.mutate.call_count, 4) # Headlines, Descriptions, Hotel Asset, Main Batch

        # Further checks on the operations passed to the main mutate call
        main_mutate_call_args = mock_google_ads_service.mutate.call_args_list[3] # Last call is the main one
        main_operations = main_mutate_call_args[1]['mutate_operations']

        # Check for campaign budget operation
        self.assertTrue(any(op.campaign_budget_operation.create.resource_name == f"customers/test_customer_id/campaignBudgets/{script_under_test.BUDGET_TEMPORARY_ID}" for op in main_operations))
        # Check for campaign operation
        self.assertTrue(any(op.campaign_operation.create.resource_name == f"customers/test_customer_id/campaigns/{script_under_test.CAMPAIGN_TEMPORARY_ID}" for op in main_operations))
        # Check for asset group operation
        self.assertTrue(any(op.asset_group_operation.create.resource_name == f"customers/test_customer_id/assetGroups/{script_under_test.ASSET_GROUP_TEMPORARY_ID}" for op in main_operations))

        # Check print statements (simplified)
        mock_print.assert_any_call("Fetched a hotel asset suggestion for the place ID: 'test_place_id'.")
        mock_print.assert_any_call(f"Created an asset set with resource name: 'assetSets/hotel_set_1'")
        mock_print.assert_any_call("Created the following entities for a campaign budget, a campaign, and an asset group for Performance Max for travel goals:")


    @patch("travel.add_performance_max_for_travel_goals_campaign.main")
    @patch("travel.add_performance_max_for_travel_goals_campaign.GoogleAdsClient.load_from_storage")
    @patch("argparse.ArgumentParser")
    def test_script_runner(self, mock_argument_parser, mock_load_client, mock_main_function):
        mock_args = MagicMock()
        mock_args.customer_id = "test_customer_id_script"
        mock_args.place_id = "test_place_id_script"

        mock_parser_instance = mock_argument_parser.return_value
        mock_parser_instance.parse_args.return_value = mock_args

        mock_client = MagicMock()
        mock_load_client.return_value = mock_client

        with patch.object(script_under_test, "__name__", "__main__"):
            import importlib
            # Reload the script to ensure its __main__ block is triggered
            # and also to reset any global state within the script if necessary (like next_temp_id)
            importlib.reload(script_under_test)
            # Re-apply global mocks after reload if they are defined in the script
            script_under_test.ASSET_TEMPORARY_ID = -1
            script_under_test.BUDGET_TEMPORARY_ID = -2
            script_under_test.CAMPAIGN_TEMPORARY_ID = -3
            script_under_test.ASSET_GROUP_TEMPORARY_ID = -4
            script_under_test.next_temp_id = -5


        mock_main_function.assert_called_once_with(
            mock_client,
            "test_customer_id_script",
            "test_place_id_script"
        )

if __name__ == "__main__":
    unittest.main()
