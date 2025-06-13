import unittest
from unittest.mock import MagicMock, patch, call
import argparse # Added
import sys # Added

from google.ads.googleads.errors import GoogleAdsException # Added

from examples.audience_insights.generate_audience_insights import (
    audience_composition_insights,
    generate_suggested_targeting_insights,
    list_audience_insights_attributes,
    main, # main is already imported
)

# Test Constants
TEST_CUSTOMER_ID = "1234567890"
TEST_LOCATION_ID = "2840"  # US
TEST_USER_INTEREST_ID = "92948"  # Technology
TEST_CUSTOM_NAME = "TestAudienceComposition"
TEST_PRODUCT_NAME = "TestProduct"
EXPECTED_LOCATION_PATH = f"geoTargetConstants/{TEST_LOCATION_ID}"
EXPECTED_USER_INTEREST_PATH = (
    f"customers/{TEST_CUSTOMER_ID}/userInterests/{TEST_USER_INTEREST_ID}"
)


class TestGenerateAudienceInsights(unittest.TestCase):
    # Class-level constants
    TEST_CUSTOMER_ID_CLASS_LEVEL = TEST_CUSTOMER_ID # Renamed to avoid conflict with method-level if any
    TEST_LOCATION_ID_CLASS_LEVEL = TEST_LOCATION_ID
    TEST_USER_INTEREST_ID_CLASS_LEVEL = TEST_USER_INTEREST_ID
    TEST_CUSTOM_NAME_CLASS_LEVEL = TEST_CUSTOM_NAME
    EXPECTED_LOCATION_PATH_CLASS_LEVEL = EXPECTED_LOCATION_PATH
    EXPECTED_USER_INTEREST_PATH_CLASS_LEVEL = EXPECTED_USER_INTEREST_PATH
    TEST_PRODUCT_NAME_CLASS_LEVEL = TEST_PRODUCT_NAME

    def setUp(self):
        self.mock_client = MagicMock() # Renamed from self.mock_googleads_client for clarity with prompt
        self.mock_audience_insights_service = MagicMock()
        self.mock_googleads_service = MagicMock()

        # Updated get_service side_effect
        def get_service_side_effect(service_name_or_type, version=None):
            if service_name_or_type == "AudienceInsightsService":
                return self.mock_audience_insights_service
            elif service_name_or_type == "GoogleAdsService":
                return self.mock_googleads_service
            return MagicMock() # Default mock for other services if any unexpected are called
        self.mock_client.get_service = MagicMock(side_effect=get_service_side_effect)


        # This patch is for GoogleAdsClient.load_from_storage used in the SCRIPT's __main__ block.
        # For direct tests of main(), we pass self.mock_client.
        # For tests that might involve the script's entry point simulation (if any), this would be active.
        self.load_from_storage_patcher = patch(
            "examples.audience_insights.generate_audience_insights.GoogleAdsClient.load_from_storage"
        )
        self.mock_load_from_storage = self.load_from_storage_patcher.start()
        self.mock_load_from_storage.return_value = self.mock_client # Ensure it returns our main mock client

        self.mock_googleads_service.geo_target_constant_path.reset_mock()
        self.mock_googleads_service.user_interest_path.reset_mock()

        self.mock_googleads_service.geo_target_constant_path.return_value = (
            self.EXPECTED_LOCATION_PATH_CLASS_LEVEL
        )
        self.mock_googleads_service.user_interest_path.return_value = (
            self.EXPECTED_USER_INTEREST_PATH_CLASS_LEVEL
        )

        self.mock_audience_insights_service.generate_audience_composition_insights.return_value = MagicMock()
        self.mock_audience_insights_service.generate_suggested_targeting_insights.return_value = MagicMock()

        self.mock_list_attributes_response = MagicMock()
        mock_attribute_1 = MagicMock()
        mock_attribute_1.dimension = 3
        mock_attribute_1.attribute.entity.knowledge_graph_machine_id = "kg_id_1"
        mock_attribute_2 = MagicMock()
        mock_attribute_2.dimension = 1
        mock_attribute_2.attribute.entity.knowledge_graph_machine_id = "kg_id_2"
        self.mock_list_attributes_response.attributes = [mock_attribute_1, mock_attribute_2]
        self.mock_audience_insights_service.list_audience_insights_attributes.return_value = self.mock_list_attributes_response

        self.mock_types = {}
        mock_gacir = MagicMock()
        mock_gacir.audience.topic_audience_combinations = []
        mock_gacir.audience.country_locations = []
        self.mock_types["GenerateAudienceCompositionInsightsRequest"] = mock_gacir

        mock_attr_group = MagicMock()
        mock_attr_group.attributes = []
        self.mock_types["InsightsAudienceAttributeGroup"] = mock_attr_group

        mock_attribute_obj = MagicMock() # Renamed from mock_attribute to avoid conflict
        mock_attribute_obj.user_interest.user_interest_category = None
        self.mock_types["AudienceInsightsAttribute"] = mock_attribute_obj

        mock_gstir = MagicMock()
        mock_gstir.audience_definition.audience.country_locations = []
        self.mock_types["GenerateSuggestedTargetingInsightsRequest"] = mock_gstir

        mock_location_info = MagicMock()
        mock_location_info.geo_target_constant = None
        self.mock_types["LocationInfo"] = mock_location_info

        mock_lair = MagicMock()
        mock_lair.dimensions = []
        self.mock_types["ListAudienceInsightsAttributesRequest"] = mock_lair

        def get_type_side_effect(type_name_string):
            if type_name_string not in self.mock_types:
                self.mock_types[type_name_string] = MagicMock()
            return self.mock_types[type_name_string]

        self.mock_client.get_type.side_effect = get_type_side_effect
        self.mock_client.get_type.reset_mock()

        mock_enum_object = MagicMock()
        mock_enum_object.CATEGORY = 1
        mock_enum_object.KNOWLEDGE_GRAPH = 3
        if not hasattr(self.mock_client, 'enums') or not isinstance(self.mock_client.enums, MagicMock):
            self.mock_client.enums = MagicMock()
        self.mock_client.enums.AudienceInsightsDimensionEnum = mock_enum_object

    def tearDown(self):
        self.load_from_storage_patcher.stop()
        patch.stopall() # Good practice to stop any other patches started with .start()

    # test_placeholder removed

    def test_audience_composition_insights_request_construction(self):
        audience_composition_insights(
            self.mock_client, # Was self.mock_googleads_client
            self.mock_audience_insights_service,
            self.mock_googleads_service,
            self.TEST_CUSTOMER_ID_CLASS_LEVEL,
            self.TEST_LOCATION_ID_CLASS_LEVEL,
            self.TEST_USER_INTEREST_ID_CLASS_LEVEL,
            self.TEST_CUSTOM_NAME_CLASS_LEVEL,
        )
        self.mock_audience_insights_service.generate_audience_composition_insights.assert_called_once()
        actual_request = self.mock_types["GenerateAudienceCompositionInsightsRequest"]
        self.assertEqual(actual_request.customer_id, self.TEST_CUSTOMER_ID_CLASS_LEVEL)
        self.assertEqual(actual_request.customer_insights_group, self.TEST_CUSTOM_NAME_CLASS_LEVEL)
        self.assertEqual(actual_request.dimensions, ("AFFINITY_USER_INTEREST", "IN_MARKET_USER_INTEREST", "YOUTUBE_CHANNEL"))
        self.mock_googleads_service.geo_target_constant_path.assert_called_once_with(self.TEST_LOCATION_ID_CLASS_LEVEL)
        self.mock_googleads_service.user_interest_path.assert_called_once_with(self.TEST_CUSTOMER_ID_CLASS_LEVEL, self.TEST_USER_INTEREST_ID_CLASS_LEVEL)
        self.assertEqual(len(actual_request.audience.country_locations), 1)
        appended_location_info = self.mock_types["LocationInfo"]
        self.assertIn(appended_location_info, actual_request.audience.country_locations)
        self.assertEqual(appended_location_info.geo_target_constant, self.EXPECTED_LOCATION_PATH_CLASS_LEVEL)
        self.assertEqual(len(actual_request.audience.topic_audience_combinations), 1)
        appended_attribute_group = self.mock_types["InsightsAudienceAttributeGroup"]
        self.assertIn(appended_attribute_group, actual_request.audience.topic_audience_combinations)
        self.assertEqual(len(appended_attribute_group.attributes), 1)
        appended_attribute = self.mock_types["AudienceInsightsAttribute"]
        self.assertIn(appended_attribute, appended_attribute_group.attributes)
        self.assertEqual(appended_attribute.user_interest.user_interest_category, self.EXPECTED_USER_INTEREST_PATH_CLASS_LEVEL)
        self.mock_client.get_type.assert_any_call("GenerateAudienceCompositionInsightsRequest")
        self.mock_client.get_type.assert_any_call("InsightsAudienceAttributeGroup")
        self.mock_client.get_type.assert_any_call("AudienceInsightsAttribute")
        self.mock_client.get_type.assert_any_call("LocationInfo")

    def test_generate_suggested_targeting_insights_request_construction(self):
        generate_suggested_targeting_insights(
            self.mock_client, # Was self.mock_googleads_client
            self.mock_audience_insights_service,
            self.mock_googleads_service,
            self.TEST_CUSTOMER_ID_CLASS_LEVEL,
            self.TEST_LOCATION_ID_CLASS_LEVEL,
            self.TEST_CUSTOM_NAME_CLASS_LEVEL
        )
        self.mock_audience_insights_service.generate_suggested_targeting_insights.assert_called_once()
        actual_request = self.mock_types["GenerateSuggestedTargetingInsightsRequest"]
        self.assertEqual(actual_request.customer_id, self.TEST_CUSTOMER_ID_CLASS_LEVEL)
        self.assertEqual(actual_request.customer_insights_group, self.TEST_CUSTOM_NAME_CLASS_LEVEL)
        self.mock_googleads_service.geo_target_constant_path.assert_called_once_with(self.TEST_LOCATION_ID_CLASS_LEVEL)
        self.mock_googleads_service.user_interest_path.assert_not_called()
        self.assertEqual(len(actual_request.audience_definition.audience.country_locations), 1)
        appended_location_info = self.mock_types["LocationInfo"]
        self.assertIn(appended_location_info, actual_request.audience_definition.audience.country_locations)
        self.assertEqual(appended_location_info.geo_target_constant, self.EXPECTED_LOCATION_PATH_CLASS_LEVEL)
        self.assertIsNotNone(actual_request.audience_definition)
        self.mock_client.get_type.assert_any_call("GenerateSuggestedTargetingInsightsRequest")
        self.mock_client.get_type.assert_any_call("LocationInfo")
        calls_to_get_type = self.mock_client.get_type.mock_calls
        unexpected_call = call("GenerateAudienceCompositionInsightsRequest")
        self.assertNotIn(unexpected_call, calls_to_get_type)

    @patch('builtins.print')
    def test_list_audience_insights_attributes_request_and_response(self, mock_print):
        list_audience_insights_attributes(
            self.mock_client, # Was self.mock_googleads_client
            self.mock_audience_insights_service,
            self.TEST_CUSTOMER_ID_CLASS_LEVEL,
            self.TEST_PRODUCT_NAME_CLASS_LEVEL,
            self.TEST_CUSTOM_NAME_CLASS_LEVEL
        )
        self.mock_audience_insights_service.list_audience_insights_attributes.assert_called_once()
        actual_request = self.mock_types["ListAudienceInsightsAttributesRequest"]
        self.assertEqual(actual_request.customer_id, self.TEST_CUSTOMER_ID_CLASS_LEVEL)
        self.assertEqual(actual_request.query_text, self.TEST_PRODUCT_NAME_CLASS_LEVEL)
        self.assertEqual(actual_request.customer_insights_group, self.TEST_CUSTOM_NAME_CLASS_LEVEL)
        self.assertIn(1, actual_request.dimensions)
        self.assertIn(3, actual_request.dimensions)
        self.assertEqual(len(actual_request.dimensions), 2)
        mock_print.assert_called_once_with("kg_id_1")
        self.mock_client.get_type.assert_any_call("ListAudienceInsightsAttributesRequest")
        calls_to_get_type = self.mock_client.get_type.mock_calls
        unexpected_gacir_call = call("GenerateAudienceCompositionInsightsRequest")
        unexpected_gstir_call = call("GenerateSuggestedTargetingInsightsRequest")
        self.assertNotIn(unexpected_gacir_call, calls_to_get_type)
        self.assertNotIn(unexpected_gstir_call, calls_to_get_type)

    @patch('examples.audience_insights.generate_audience_insights.audience_composition_insights')
    @patch('examples.audience_insights.generate_audience_insights.generate_suggested_targeting_insights')
    @patch('examples.audience_insights.generate_audience_insights.list_audience_insights_attributes')
    # No need to patch GoogleAdsClient.load_from_storage here as main receives client directly
    def test_main_success_path(
        self,
        mock_list_attributes,
        mock_generate_suggested,
        mock_audience_composition
    ):
        test_customer_id = "main_test_customer_id"
        test_custom_name = "MainTestCustomName"

        # Act - main function takes client, customer_id, custom_name
        main(self.mock_client, test_customer_id, test_custom_name)

        # Assert
        # Check that get_service was called to retrieve services
        self.mock_client.get_service.assert_any_call("AudienceInsightsService")
        self.mock_client.get_service.assert_any_call("GoogleAdsService")

        mock_audience_composition.assert_called_once_with(
            self.mock_client,
            self.mock_audience_insights_service,
            self.mock_googleads_service,
            test_customer_id,
            "2840",  # Default location_id from main
            "92948", # Default user_interest_category from main
            test_custom_name
        )
        mock_generate_suggested.assert_called_once_with(
            self.mock_client,
            self.mock_audience_insights_service,
            self.mock_googleads_service,
            test_customer_id,
            "2840",  # Default location_id from main
            test_custom_name
        )
        mock_list_attributes.assert_called_once_with(
            self.mock_client,
            self.mock_audience_insights_service,
            test_customer_id,
            "Google", # Default product_name from main
            test_custom_name
        )

    @patch('examples.audience_insights.generate_audience_insights.audience_composition_insights')
    # No longer patching print and sys.exit for this test, as 'main' itself doesn't handle the exception.
    def test_main_propagates_google_ads_exception(self, mock_audience_composition):
        # Arrange
        mock_failure = MagicMock()
        # To ensure the exception object has the necessary structure for any potential formatting
        # if it were caught and printed by a higher level (though not asserted here).
        mock_failure.errors = [MagicMock(message="Test error message.")]
        mock_error_code = MagicMock()
        mock_error_code.name = "TEST_ERROR_CODE"
        mock_error_obj = MagicMock() # Renamed from mock_error to avoid confusion
        mock_error_obj.code.return_value = mock_error_code

        expected_exception = GoogleAdsException(
            "request_id_test",
            mock_failure,
            MagicMock(), # for _call
            mock_error_obj   # Pass mock_error_obj as the 4th positional argument
        )
        mock_audience_composition.side_effect = expected_exception

        test_customer_id = "exception_test_customer_id"
        test_custom_name = "ExceptionTestCustomName"

        # Act & Assert
        # Verify that calling main results in the GoogleAdsException being propagated.
        with self.assertRaises(GoogleAdsException) as cm:
            main(self.mock_client, test_customer_id, test_custom_name)

        # Optionally, assert that the raised exception is the one we expected
        self.assertIs(cm.exception, expected_exception)

        # Ensure the mocked function that raises the exception was indeed called.
        mock_audience_composition.assert_called_once()

if __name__ == "__main__":
    unittest.main()
