import unittest
from unittest.mock import patch, MagicMock, call, ANY
# import argparse # No longer needed
import sys
# import importlib # No longer needed

sys.path.append(".")
sys.path.append("examples")

from travel import add_performance_max_for_travel_goals_campaign as script_under_test

# Reset global temporary IDs to ensure test predictability
script_under_test.ASSET_TEMPORARY_ID = -1
script_under_test.BUDGET_TEMPORARY_ID = -2
script_under_test.CAMPAIGN_TEMPORARY_ID = -3
script_under_test.ASSET_GROUP_TEMPORARY_ID = -4
# script_under_test.next_temp_id is reset in setUp


class TestAddPerformanceMaxForTravelGoalsCampaign(unittest.TestCase):

    def setUp(self):
        # Reset next_temp_id before each test, as it's modified globally
        script_under_test.next_temp_id = -5 # Initial value consistent with script

    @patch("travel.add_performance_max_for_travel_goals_campaign.get_image_bytes_from_url")
    @patch("travel.add_performance_max_for_travel_goals_campaign.GoogleAdsClient") # Patch class
    # Removed argparse patch as test_script_runner is removed
    def test_main(self, MockGoogleAdsClient, mock_get_image_bytes): # Adjusted order
        mock_client_instance = MockGoogleAdsClient.return_value # Get instance

        customer_id = "test_customer_id"
        place_id = "test_place_id"

        mock_get_image_bytes.return_value = b"image_data"

        # Mock services
        mock_travel_asset_suggestion_service = MagicMock()
        mock_google_ads_service = MagicMock()
        mock_asset_set_service = MagicMock()
        # Other services are not called directly with client.get_service in main flow,
        # but their paths might be used.

        def mock_get_service_side_effect(service_name, version="v19"):
            if service_name == "TravelAssetSuggestionService":
                return mock_travel_asset_suggestion_service
            elif service_name == "GoogleAdsService":
                return mock_google_ads_service
            elif service_name == "AssetSetService":
                return mock_asset_set_service
            # Return a generic mock for other services like CampaignService, AssetService etc.
            # if their .path() methods are needed by the script.
            mock_service = MagicMock(name=service_name)
            # Example: mock_service.campaign_path = lambda cid, id: f"customers/{cid}/campaigns/{id}"
            return mock_service

        mock_client_instance.get_service.side_effect = mock_get_service_side_effect

        # --- Mock Enums correctly ---
        mock_client_instance.enums = MagicMock()

        # For AssetFieldTypeEnum members, ensure their .name attribute returns the string value
        mock_asset_field_type_enum_obj = MagicMock()
        for field_type_str_val in ["HEADLINE", "DESCRIPTION", "BUSINESS_NAME",
                                   "MARKETING_IMAGE", "SQUARE_MARKETING_IMAGE", "LOGO",
                                   "HOTEL_PROPERTY", "CALL_TO_ACTION_SELECTION"]:
            enum_member_mock = MagicMock() # Create a mock for each enum member (e.g., AssetFieldTypeEnum.HEADLINE)
            enum_member_mock.name = field_type_str_val # Set its .name attribute to return the string value
            setattr(mock_asset_field_type_enum_obj, field_type_str_val, enum_member_mock)
        mock_client_instance.enums.AssetFieldTypeEnum = mock_asset_field_type_enum_obj

        # For other enums, if only used for direct comparison or passed as values,
        # MagicMock(name="...") is okay. If .name is accessed, they need similar setup.
        mock_client_instance.enums.HotelAssetSuggestionStatusEnum.SUCCESS = MagicMock(name="SUCCESS")
        mock_client_instance.enums.AssetSetTypeEnum.HOTEL_PROPERTY = MagicMock(name="HOTEL_PROPERTY")
        mock_client_instance.enums.BudgetDeliveryMethodEnum.STANDARD = MagicMock(name="STANDARD")
        mock_client_instance.enums.CampaignStatusEnum.PAUSED = MagicMock(name="PAUSED")
        mock_client_instance.enums.AdvertisingChannelTypeEnum.PERFORMANCE_MAX = MagicMock(name="PERFORMANCE_MAX")
        mock_client_instance.enums.AssetGroupStatusEnum.PAUSED = MagicMock(name="PAUSED")
        mock_client_instance.enums.CallToActionEnum.BOOK_NOW = MagicMock(name="BOOK_NOW") # if used directly

        # --- Mock Types (return mocks that can have attributes set) ---
        # Make get_type return mocks that can have attributes set as needed by the script
        # This helps avoid AttributeErrors if the script tries to set something on a type.
        type_mocks = {}
        def get_type_dynamic(type_name):
            if type_name not in type_mocks:
                mock_type_obj = MagicMock(name=type_name)
                # Pre-configure known attributes if necessary, e.g.
                if type_name == "MutateOperation":
                    mock_type_obj.asset_operation = MagicMock()
                    mock_type_obj.asset_operation.create = MagicMock()
                    mock_type_obj.asset_set_asset_operation = MagicMock()
                    mock_type_obj.asset_set_asset_operation.create = MagicMock()
                    mock_type_obj.campaign_budget_operation = MagicMock()
                    mock_type_obj.campaign_budget_operation.create = MagicMock()
                    mock_type_obj.campaign_operation = MagicMock()
                    mock_type_obj.campaign_operation.create = MagicMock()
                    mock_type_obj.asset_group_operation = MagicMock()
                    mock_type_obj.asset_group_operation.create = MagicMock()
                    mock_type_obj.asset_group_asset_operation = MagicMock()
                    mock_type_obj.asset_group_asset_operation.create = MagicMock()
                elif type_name == "Asset":
                    mock_type_obj.text_asset = MagicMock()
                    mock_type_obj.hotel_property_asset = MagicMock()
                    mock_type_obj.image_asset = MagicMock()
                    mock_type_obj.call_to_action_asset = MagicMock()
                elif type_name == "Campaign":
                    mock_type_obj.maximize_conversion_value = MagicMock() # For target_roas
                # ... add other types as identified by script's usage
                type_mocks[type_name] = mock_type_obj
            return type_mocks[type_name]

        mock_client_instance.get_type.side_effect = get_type_dynamic

        # Mock client.copy_from as it's used in the script
        mock_client_instance.copy_from = MagicMock()


        # --- Mock service responses ---
        mock_suggestion_response = MagicMock()
        mock_hotel_suggestion = MagicMock()
        # Use the mocked enums for status and asset_field_type
        mock_hotel_suggestion.status = mock_client_instance.enums.HotelAssetSuggestionStatusEnum.SUCCESS
        mock_hotel_suggestion.text_assets = [
            MagicMock(asset_field_type=mock_client_instance.enums.AssetFieldTypeEnum.HEADLINE, text="Suggested Headline 1"),
            MagicMock(asset_field_type=mock_client_instance.enums.AssetFieldTypeEnum.DESCRIPTION, text="Suggested Description 1"),
            MagicMock(asset_field_type=mock_client_instance.enums.AssetFieldTypeEnum.BUSINESS_NAME, text="Suggested Business"),
        ]
        mock_hotel_suggestion.image_assets = [
            MagicMock(uri="http://suggested.com/img1.png", asset_field_type=mock_client_instance.enums.AssetFieldTypeEnum.MARKETING_IMAGE)
        ]
        mock_hotel_suggestion.hotel_name = "Suggested Hotel"
        mock_hotel_suggestion.final_url = "http://suggested-final.com"
        mock_hotel_suggestion.call_to_action = mock_client_instance.enums.CallToActionEnum.BOOK_NOW

        mock_suggestion_response.hotel_asset_suggestions = [mock_hotel_suggestion]
        mock_travel_asset_suggestion_service.suggest_travel_assets.return_value = mock_suggestion_response

        # GoogleAdsService.mutate for text assets
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

        mock_asset_set_response = MagicMock()
        # Ensure results is a list for indexing
        mock_asset_set_response.results = [MagicMock(resource_name="assetSets/hotel_set_1")]
        mock_asset_set_service.mutate_asset_sets.return_value = mock_asset_set_response

        mock_hotel_asset_creation_response = MagicMock()
        mock_hotel_asset_creation_response.mutate_operation_responses = [
            MagicMock(asset_result=MagicMock(resource_name=f"customers/test_customer_id/assets/{script_under_test.ASSET_TEMPORARY_ID}")),
            MagicMock(asset_set_asset_result=MagicMock(resource_name="assetSetAssets/link1"))
        ]

        mock_main_mutate_response = MagicMock()
        mock_main_mutate_response.mutate_operation_responses = [
            MagicMock(campaign_budget_result=MagicMock(resource_name=f"customers/test_customer_id/campaignBudgets/{script_under_test.BUDGET_TEMPORARY_ID}")),
            MagicMock(campaign_result=MagicMock(resource_name=f"customers/test_customer_id/campaigns/{script_under_test.CAMPAIGN_TEMPORARY_ID}")),
            MagicMock(asset_group_result=MagicMock(resource_name=f"customers/test_customer_id/assetGroups/{script_under_test.ASSET_GROUP_TEMPORARY_ID}")),
        ] + [MagicMock(asset_group_asset_result=MagicMock(resource_name=f"assetGroupAssets/link_{i}")) for i in range(10)]

        mock_google_ads_service.mutate.side_effect = [
            mock_text_asset_mutate_response_headline,
            mock_text_asset_mutate_response_description,
            mock_hotel_asset_creation_response,
            mock_main_mutate_response
        ]

        # Mock path helpers (these are methods of service clients, but often used via GoogleAdsService for resource names)
        # For this script, paths are mostly constructed directly or using GoogleAdsService instance.
        mock_google_ads_service.asset_path.side_effect = lambda cust_id, id_val: f"customers/{cust_id}/assets/{id_val}"
        mock_google_ads_service.campaign_budget_path.side_effect = lambda cust_id, id_val: f"customers/{cust_id}/campaignBudgets/{id_val}"
        mock_google_ads_service.campaign_path.side_effect = lambda cust_id, id_val: f"customers/{cust_id}/campaigns/{id_val}"
        mock_google_ads_service.asset_group_path.side_effect = lambda cust_id, id_val: f"customers/{cust_id}/assetGroups/{id_val}"


        with patch("builtins.print") as mock_print:
            script_under_test.main(
                mock_client_instance, # Pass instance
                customer_id,
                place_id,
            )

        # Assertions
        mock_travel_asset_suggestion_service.suggest_travel_assets.assert_called_once()
        mock_asset_set_service.mutate_asset_sets.assert_called_once()
        self.assertEqual(mock_google_ads_service.mutate.call_count, 4)

        # Check some details of the main mutate call (last one)
        main_mutate_call_args = mock_google_ads_service.mutate.call_args_list[3]
        main_operations = main_mutate_call_args[1]['mutate_operations']

        # Verify campaign budget operation
        campaign_budget_op = next(op for op in main_operations if op.campaign_budget_operation.create.resource_name)
        self.assertEqual(campaign_budget_op.campaign_budget_operation.create.resource_name, f"customers/{customer_id}/campaignBudgets/{script_under_test.BUDGET_TEMPORARY_ID}")

        # Verify campaign operation
        campaign_op = next(op for op in main_operations if op.campaign_operation.create.resource_name)
        self.assertEqual(campaign_op.campaign_operation.create.resource_name, f"customers/{customer_id}/campaigns/{script_under_test.CAMPAIGN_TEMPORARY_ID}")
        self.assertEqual(campaign_op.campaign_operation.create.hotel_property_asset_set, "assetSets/hotel_set_1") # From mocked response

        # Verify asset group operation
        asset_group_op = next(op for op in main_operations if op.asset_group_operation.create.resource_name)
        self.assertEqual(asset_group_op.asset_group_operation.create.resource_name, f"customers/{customer_id}/assetGroups/{script_under_test.ASSET_GROUP_TEMPORARY_ID}")

        # Check print statements (simplified)
        mock_print.assert_any_call("Fetched a hotel asset suggestion for the place ID: 'test_place_id'.")
        mock_print.assert_any_call(f"Created an asset set with resource name: 'assetSets/hotel_set_1'")
        mock_print.assert_any_call("Created the following entities for a campaign budget, a campaign, and an asset group for Performance Max for travel goals:")


if __name__ == "__main__":
    unittest.main()
