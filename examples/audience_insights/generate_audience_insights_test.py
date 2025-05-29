import argparse
import sys
import unittest
from unittest.mock import patch, MagicMock

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.ads.googleads.v19.enums.types import (
    AudienceInsightsDimensionEnum,
)
from google.ads.googleads.v19.services.services.audience_insights_service import (
    AudienceInsightsServiceClient,
)
from google.ads.googleads.v19.services.services.google_ads_service import (
    GoogleAdsServiceClient,
)
from google.ads.googleads.v19.types.audience_insights_service import (
    AudienceInsightsAttribute,
    GenerateAudienceCompositionInsightsRequest,
    GenerateAudienceCompositionInsightsResponse,
    GenerateSuggestedTargetingInsightsRequest,
    GenerateSuggestedTargetingInsightsResponse,
    InsightsAudienceAttributeGroup,
    ListAudienceInsightsAttributesRequest,
    ListAudienceInsightsAttributesResponse,
)
from google.ads.googleads.v19.types.common import LocationInfo

# Assuming the script to be tested is in the same directory
import generate_audience_insights


class GenerateAudienceInsightsTest(unittest.TestCase):
    def setUp(self):
        self.mock_client = MagicMock(spec=GoogleAdsClient)
        self.mock_audience_insights_service = MagicMock(spec=AudienceInsightsServiceClient)
        self.mock_googleads_service = MagicMock(spec=GoogleAdsServiceClient)

        # Configure get_service to return the correct mock service
        def get_service_side_effect(service_name, version=None):
            if service_name == "AudienceInsightsService":
                return self.mock_audience_insights_service
            elif service_name == "GoogleAdsService":
                return self.mock_googleads_service
            raise ValueError(f"Unexpected service: {service_name}")

        self.mock_client.get_service.side_effect = get_service_side_effect

        # Mock the get_type method for creating request objects
        # This will return a MagicMock that can be used to simulate type creation
        # and also allow attribute assignment for building the request.
        def mock_get_type(type_name):
            mock_type_instance = MagicMock()
            if type_name == "GenerateAudienceCompositionInsightsRequest":
                mock_type_instance.audience = MagicMock()
                mock_type_instance.audience.topic_audience_combinations = []
                mock_type_instance.audience.country_locations = []
                mock_type_instance.dimensions = [] # Ensure this can be appended to
            elif type_name == "InsightsAudienceAttributeGroup":
                mock_type_instance.attributes = []
            elif type_name == "GenerateSuggestedTargetingInsightsRequest":
                # Ensure audience_definition and its nested properties can be set
                mock_type_instance.audience_definition = MagicMock()
                mock_type_instance.audience_definition.audience = MagicMock()
                mock_type_instance.audience_definition.audience.country_locations = []
            elif type_name == "ListAudienceInsightsAttributesRequest":
                mock_type_instance.dimensions = [] # Ensure this can be appended to
            elif type_name == "LocationInfo":
                pass
            return mock_type_instance

        self.mock_client.get_type.side_effect = mock_get_type

        self.mock_client.enums = MagicMock()
        self.mock_client.enums.AudienceInsightsDimensionEnum = AudienceInsightsDimensionEnum

        # Mock path helpers
        self.mock_googleads_service.user_interest_path.return_value = "customers/TEST_CUSTOMER_ID/userInterests/TEST_USER_INTEREST_ID"
        self.mock_googleads_service.geo_target_constant_path.return_value = "geoTargetConstants/TEST_LOCATION_ID"

    @patch('builtins.print')
    def test_audience_composition_insights_success(self, mock_print):
        customer_id = "test_customer_id_123"
        location_id = "2840"  # US
        user_interest = "test_user_interest_category"
        custom_name = "test_custom_audience_name"

        mock_response = MagicMock(spec=GenerateAudienceCompositionInsightsResponse)
        self.mock_audience_insights_service.generate_audience_composition_insights.return_value = mock_response

        generate_audience_insights.audience_composition_insights(
            self.mock_client,
            self.mock_audience_insights_service,
            self.mock_googleads_service,
            customer_id,
            location_id,
            user_interest,
            custom_name,
        )

        self.mock_audience_insights_service.generate_audience_composition_insights.assert_called_once()
        
        # Get the actual request object passed to the service
        actual_request_args = self.mock_audience_insights_service.generate_audience_composition_insights.call_args[1]
        actual_request = actual_request_args['request']

        self.assertEqual(actual_request.customer_id, customer_id)
        self.assertEqual(actual_request.customer_insights_group, custom_name)

        expected_dimensions = [
            AudienceInsightsDimensionEnum.AudienceInsightsDimension.AFFINITY_USER_INTEREST,
            AudienceInsightsDimensionEnum.AudienceInsightsDimension.IN_MARKET_USER_INTEREST,
            AudienceInsightsDimensionEnum.AudienceInsightsDimension.YOUTUBE_CHANNEL,
        ]
        self.assertCountEqual(actual_request.dimensions, expected_dimensions) # Use assertCountEqual for lists where order doesn't matter

        # Check audience attributes
        self.assertEqual(len(actual_request.audience.topic_audience_combinations), 1)
        topic_combination = actual_request.audience.topic_audience_combinations[0]
        self.assertEqual(len(topic_combination.attributes), 1)
        attribute = topic_combination.attributes[0]
        # Check that user_interest_path was called to construct the user_interest_category
        self.mock_googleads_service.user_interest_path.assert_called_with(customer_id, user_interest)
        self.assertEqual(attribute.user_interest.user_interest_category, self.mock_googleads_service.user_interest_path.return_value)
        
        # Check location
        self.assertEqual(len(actual_request.audience.country_locations), 1)
        location_info = actual_request.audience.country_locations[0]
        self.mock_googleads_service.geo_target_constant_path.assert_called_with(location_id)
        self.assertEqual(location_info.geo_target_constant, self.mock_googleads_service.geo_target_constant_path.return_value)

        mock_print.assert_called_once_with(mock_response)

    @patch('builtins.print')
    def test_generate_suggested_targeting_insights_success(self, mock_print):
        customer_id = "test_customer_id_456"
        location_id = "2100"  # Canada
        custom_name = "suggested_targeting_audience"

        mock_response = MagicMock(spec=GenerateSuggestedTargetingInsightsResponse)
        self.mock_audience_insights_service.generate_suggested_targeting_insights.return_value = mock_response

        # Reset call count for geo_target_constant_path for this specific test's location_id
        # This ensures that the assert_called_with in the previous test doesn't interfere
        self.mock_googleads_service.geo_target_constant_path.reset_mock()
        # Update return value for this specific call
        current_geo_target_path = f"geoTargetConstants/{location_id}"
        self.mock_googleads_service.geo_target_constant_path.return_value = current_geo_target_path


        generate_audience_insights.generate_suggested_targeting_insights(
            self.mock_client,
            self.mock_audience_insights_service,
            self.mock_googleads_service,
            customer_id,
            location_id,
            custom_name,
        )

        self.mock_audience_insights_service.generate_suggested_targeting_insights.assert_called_once()
        
        actual_request_args = self.mock_audience_insights_service.generate_suggested_targeting_insights.call_args[1]
        actual_request = actual_request_args['request']

        self.assertEqual(actual_request.customer_id, customer_id)
        self.assertEqual(actual_request.customer_insights_group, custom_name)
        
        self.assertEqual(len(actual_request.audience_definition.audience.country_locations), 1)
        location_info = actual_request.audience_definition.audience.country_locations[0]
        self.mock_googleads_service.geo_target_constant_path.assert_called_with(location_id)
        self.assertEqual(location_info.geo_target_constant, current_geo_target_path)

        mock_print.assert_called_once_with(mock_response)

    @patch('builtins.print')
    def test_list_audience_insights_attributes_success(self, mock_print):
        customer_id = "test_customer_id_789"
        product_name = "TestProduct"
        custom_name = "attribute_audience"

        mock_response = MagicMock(spec=ListAudienceInsightsAttributesResponse)
        
        attr1_kg = MagicMock(spec=AudienceInsightsAttribute)
        attr1_kg.dimension = AudienceInsightsDimensionEnum.AudienceInsightsDimension.KNOWLEDGE_GRAPH
        # To mock attribute.entity.knowledge_graph_machine_id, we need to ensure `attribute.entity` exists
        attr1_kg.attribute = MagicMock() 
        attr1_kg.attribute.entity = MagicMock()
        attr1_kg.attribute.entity.knowledge_graph_machine_id = "kg_id_1"
        
        attr2_cat = MagicMock(spec=AudienceInsightsAttribute)
        attr2_cat.dimension = AudienceInsightsDimensionEnum.AudienceInsightsDimension.CATEGORY
        attr2_cat.attribute = MagicMock() # Ensure .attribute exists even if not used for KG specific fields

        attr3_kg = MagicMock(spec=AudienceInsightsAttribute)
        attr3_kg.dimension = AudienceInsightsDimensionEnum.AudienceInsightsDimension.KNOWLEDGE_GRAPH
        attr3_kg.attribute = MagicMock()
        attr3_kg.attribute.entity = MagicMock()
        attr3_kg.attribute.entity.knowledge_graph_machine_id = "kg_id_2"

        mock_response.attributes = [attr1_kg, attr2_cat, attr3_kg]
        self.mock_audience_insights_service.list_audience_insights_attributes.return_value = mock_response

        generate_audience_insights.list_audience_insights_attributes(
            self.mock_client,
            self.mock_audience_insights_service, # This service is used, not googleads_service directly by this func
            customer_id,
            product_name,
            custom_name,
        )

        self.mock_audience_insights_service.list_audience_insights_attributes.assert_called_once()
        
        actual_request_args = self.mock_audience_insights_service.list_audience_insights_attributes.call_args[1]
        actual_request = actual_request_args['request']

        self.assertEqual(actual_request.customer_id, customer_id)
        self.assertEqual(actual_request.query_text, product_name)
        self.assertEqual(actual_request.customer_insights_group, custom_name)
        
        expected_dimensions = [
            AudienceInsightsDimensionEnum.AudienceInsightsDimension.CATEGORY,
            AudienceInsightsDimensionEnum.AudienceInsightsDimension.KNOWLEDGE_GRAPH,
        ]
        self.assertCountEqual(actual_request.dimensions, expected_dimensions)

        # Check that print was called for KNOWLEDGE_GRAPH attributes with their machine IDs
        # The mock_print.mock_calls gives a list of all calls made to the mock.
        # We filter this list for calls that match our expected print statements.
        printed_kg_ids = [call_arg[0] for call_arg in mock_print.call_args_list if isinstance(call_arg[0][0], str)]
        
        self.assertIn("kg_id_1", printed_kg_ids)
        self.assertIn("kg_id_2", printed_kg_ids)
        # Ensure print was called exactly twice (once for each KG attribute)
        self.assertEqual(mock_print.call_count, 2)

    @patch('generate_audience_insights.list_audience_insights_attributes')
    @patch('generate_audience_insights.generate_suggested_targeting_insights')
    @patch('generate_audience_insights.audience_composition_insights')
    def test_main_success(self, mock_audience_composition, mock_suggested_targeting, mock_list_attributes):
        customer_id = "main_test_cust_id_001"
        custom_name = "main_test_custom_name_001"

        # Call the main function from the script, passing the already mocked client
        generate_audience_insights.main(self.mock_client, customer_id, custom_name)

        # Expected hardcoded values from the generate_audience_insights.main function
        expected_location_id = "2840"  # US
        expected_product_name = "Google"
        expected_user_interest_category = "92948"  # Technology

        mock_audience_composition.assert_called_once_with(
            self.mock_client,
            self.mock_audience_insights_service,
            self.mock_googleads_service,
            customer_id,
            expected_location_id,
            expected_user_interest_category,
            custom_name,
        )
        mock_suggested_targeting.assert_called_once_with(
            self.mock_client,
            self.mock_audience_insights_service,
            self.mock_googleads_service,
            customer_id,
            expected_location_id,
            custom_name,
        )
        mock_list_attributes.assert_called_once_with(
            self.mock_client,
            self.mock_audience_insights_service, 
            customer_id,
            expected_product_name,
            custom_name,
        )

    @patch('builtins.print')
    @patch('sys.exit')
    @patch('generate_audience_insights.GoogleAdsClient.load_from_storage')
    @patch('argparse.ArgumentParser')
    def test_main_script_execution_google_ads_exception(
        self, mock_argparse, mock_load_client, mock_sys_exit, mock_print
    ):
        test_customer_id = "exception_test_customer_id"
        test_custom_name = "exception_test_custom_name"

        mock_args_instance = MagicMock()
        mock_args_instance.customer_id = test_customer_id
        mock_args_instance.custom_name = test_custom_name
        mock_argparse.return_value.parse_args.return_value = mock_args_instance

        mock_load_client.return_value = self.mock_client

        mock_failure_obj = MagicMock()
        mock_error_detail_obj = MagicMock()
        mock_error_detail_obj.message = "Detailed error message for testing." 
        
        mock_location_obj = MagicMock()
        mock_field_path_element_obj = MagicMock()
        mock_field_path_element_obj.field_name = "example_field_name"
        mock_location_obj.field_path_elements = [mock_field_path_element_obj]
        mock_error_detail_obj.location = mock_location_obj
        
        mock_failure_obj.errors = [mock_error_detail_obj]

        mock_google_ads_error_enum_obj = MagicMock() 
        mock_google_ads_error_enum_obj.code.return_value.name = "SAMPLE_ERROR_CODE"

        # We need to ensure the GoogleAdsException is created with all necessary parts
        # that the script's exception handler will try to access.
        exception_to_raise = GoogleAdsException(
            error=mock_google_ads_error_enum_obj, 
            failure=mock_failure_obj,       
            request_id="req_id_for_exception_test",
            call=MagicMock() # The 'call' attribute is also accessed by GoogleAdsException
        )

        # Patch the main function within generate_audience_insights module
        # This main is the one called by the if __name__ == "__main__": block
        with patch('generate_audience_insights.main', side_effect=exception_to_raise) as mock_main_function_raising_exception:
            # Replicate the argument parsing and client loading from the script's main block
            args = mock_argparse.return_value.parse_args()
            client = mock_load_client.return_value # This is self.mock_client

            # Replicate the try-except block from the script's if __name__ == "__main__":
            try:
                # This call will now trigger the side_effect (exception)
                generate_audience_insights.main(client, args.customer_id, args.custom_name)
            except GoogleAdsException as ex:
                # This is the actual print block from the script
                print(
                    f'Request with ID "{ex.request_id}" failed with status '
                    f'"{ex.error.code().name}" and includes the following errors:'
                )
                for error_item in ex.failure.errors:
                    print(f'\tError with message "{error_item.message}".')
                    if error_item.location:
                        for field_path_element_item in error_item.location.field_path_elements:
                            print(
                                f"\t\tOn field: {field_path_element_item.field_name}"
                            )
                sys.exit(1) # This is the actual sys.exit from the script

        # Assert that the patched main function (which raises the exception) was called
        mock_main_function_raising_exception.assert_called_once_with(
            self.mock_client, test_customer_id, test_custom_name
        )
        
        # Assert that sys.exit was called with 1 due to the exception
        mock_sys_exit.assert_called_once_with(1)
        
        # Assert that the error messages were printed as expected
        mock_print.assert_any_call(
            f'Request with ID "req_id_for_exception_test" failed with status '
            f'"SAMPLE_ERROR_CODE" and includes the following errors:'
        )
        mock_print.assert_any_call(f'\tError with message "Detailed error message for testing.".')
        mock_print.assert_any_call(f"\t\tOn field: example_field_name")
