import argparse
import unittest
from unittest import mock

# Import the script to be tested.
# This assumes that the script is in the parent directory and the parent directory is a package (has __init__.py)
from .. import generate_audience_insights

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.v19.services.services.audience_insights_service import AudienceInsightsServiceClient
from google.ads.googleads.v19.services.services.google_ads_service import GoogleAdsServiceClient
# Import other necessary v19 types/enums as they become needed for tests
from google.ads.googleads.v19.enums.types import (
    AudienceInsightsDimensionEnum,
)
# from google.ads.googleads.v19.types.audience_insights_service import (
#     AudienceInsightsAttribute,
#     GenerateAudienceCompositionInsightsRequest,
#     GenerateAudienceCompositionInsightsResponse,
#     GenerateSuggestedTargetingInsightsRequest,
#     GenerateSuggestedTargetingInsightsResponse,
#     InsightsAudienceAttributeGroup,
#     ListAudienceInsightsAttributesRequest,
#     ListAudienceInsightsAttributesResponse,
# )
# from google.ads.googleads.v19.types.common import LocationInfo

class TestGenerateAudienceInsights(unittest.TestCase):
    def setUp(self):
        # Create a mock for the GoogleAdsClient
        self.mock_ads_client = mock.create_autospec(GoogleAdsClient, instance=True)

        # Create mocks for the service clients
        self.mock_audience_insights_service = mock.create_autospec(AudienceInsightsServiceClient, instance=True)
        self.mock_google_ads_service = mock.create_autospec(GoogleAdsServiceClient, instance=True)

        # Configure the mock_ads_client.get_service method
        self.mock_ads_client.get_service.side_effect = lambda service_name, version="v19": {
            "AudienceInsightsService": self.mock_audience_insights_service,
            "GoogleAdsService": self.mock_google_ads_service,
        }.get(service_name)
        
        # Mock GoogleAdsClient.load_from_storage to return our mock_ads_client
        self.patcher_load_from_storage = mock.patch(
            "google.ads.googleads.client.GoogleAdsClient.load_from_storage",
            return_value=self.mock_ads_client
        )
        self.mock_load_from_storage = self.patcher_load_from_storage.start()
        self.addCleanup(self.patcher_load_from_storage.stop)

        # Mock client.get_type to return a basic mock object for any type name.
        # Specific types can be further customized in individual tests if needed.
        self.mock_ads_client.get_type.side_effect = lambda name: mock.Mock(name=name)
        
        # Mock client.enums to access enum values.
        # This makes actual enum objects available for use in tests.
        self.mock_ads_client.enums = mock.Mock()
        self.mock_ads_client.enums.AudienceInsightsDimensionEnum = AudienceInsightsDimensionEnum


    # Test cases will be added here in subsequent steps.
    def test_setup_works(self):
        # A simple placeholder test to ensure the setup works.
        self.assertIsNotNone(self.mock_ads_client)
        self.assertIsNotNone(self.mock_audience_insights_service)
        self.assertIsNotNone(self.mock_google_ads_service)
        
        # Test if get_service returns the correct mock
        ais_service = self.mock_ads_client.get_service("AudienceInsightsService")
        self.assertEqual(ais_service, self.mock_audience_insights_service)
        
        gas_service = self.mock_ads_client.get_service("GoogleAdsService")
        self.assertEqual(gas_service, self.mock_google_ads_service)

        # Test if load_from_storage mock is working
        # In the script, GoogleAdsClient.load_from_storage() is called.
        # We can't directly test its return value here without calling the script's main,
        # but self.mock_load_from_storage.called can be checked if we trigger its usage.
        # For now, the presence of the mock is enough.
        self.assertIsNotNone(self.mock_load_from_storage)

    def test_audience_composition_insights(self):
        customer_id = "test-customer-id"
        location_id = "2840"  # US
        user_interest_category_id = "test-interest-id"
        custom_name = "test-custom-audience-name"

        mock_user_interest_path = f"customers/{customer_id}/userInterests/{user_interest_category_id}"
        self.mock_google_ads_service.user_interest_path.return_value = mock_user_interest_path

        mock_geo_target_path = f"geoTargetConstants/{location_id}"
        self.mock_google_ads_service.geo_target_constant_path.return_value = mock_geo_target_path
        
        # Mock the response from the service
        mock_api_response = mock.Mock(name="GenerateAudienceCompositionInsightsResponse")
        self.mock_audience_insights_service.generate_audience_composition_insights.return_value = mock_api_response

        # Patch builtins.print to check its calls
        with mock.patch("builtins.print") as mock_print:
            generate_audience_insights.audience_composition_insights(
                self.mock_ads_client,
                self.mock_audience_insights_service,
                self.mock_google_ads_service,
                customer_id,
                location_id,
                user_interest_category_id,
                custom_name,
            )

        # Assert that the service method was called once
        self.mock_audience_insights_service.generate_audience_composition_insights.assert_called_once()
        
        # Get the actual request made to the service
        # call_args is a tuple (args, kwargs), we want kwargs['request']
        actual_request = self.mock_audience_insights_service.generate_audience_composition_insights.call_args[1]['request']

        # Assertions on the request object
        self.assertEqual(actual_request.customer_id, customer_id)
        self.assertEqual(actual_request.customer_insights_group, custom_name)
        
        # Check dimensions (ensure AudienceInsightsDimensionEnum is correctly used)
        # Based on the script, these are the dimensions requested.
        expected_dimensions = [
            self.mock_ads_client.enums.AudienceInsightsDimensionEnum.AFFINITY_USER_INTEREST,
            self.mock_ads_client.enums.AudienceInsightsDimensionEnum.IN_MARKET_USER_INTEREST,
            self.mock_ads_client.enums.AudienceInsightsDimensionEnum.YOUTUBE_CHANNEL,
        ]
        self.assertCountEqual(list(actual_request.dimensions), expected_dimensions)

        # Assert audience attributes
        # The script creates one InsightsAudience, which has one topic_audience_combinations.
        # This combination has one attribute (the user interest).
        self.assertEqual(len(actual_request.audience.topic_audience_combinations), 1)
        # The script assigns the result of client.get_type("InsightsAudience") to audience_obj
        # then audience_obj.topic_audience_combinations.append(insights_attribute_group)
        # then insights_attribute_group.attributes.append(user_interest_attribute)
        # So, actual_request.audience.topic_audience_combinations[0] is the insights_attribute_group mock
        insights_attribute_group_mock = actual_request.audience.topic_audience_combinations[0]
        self.assertEqual(len(insights_attribute_group_mock.attributes), 1)
        attribute_mock = insights_attribute_group_mock.attributes[0]
        # The script sets attribute.user_interest.user_interest_category
        self.assertEqual(attribute_mock.user_interest.user_interest_category, mock_user_interest_path)
        
        # Assert country locations
        # The script creates one LocationInfo and appends it to audience.country_locations
        self.assertEqual(len(actual_request.audience.country_locations), 1)
        location_info_mock = actual_request.audience.country_locations[0]
        # The script sets location_info.geo_target_constant
        self.assertEqual(location_info_mock.geo_target_constant, mock_geo_target_path)

        # Assert that print was called with the response
        mock_print.assert_called_once_with(mock_api_response)

    def test_generate_suggested_targeting_insights(self):
        customer_id = "test-customer-id"
        location_id = "2840"  # US
        custom_name = "test-custom-audience-name"

        mock_geo_target_path = f"geoTargetConstants/{location_id}"
        self.mock_google_ads_service.geo_target_constant_path.return_value = mock_geo_target_path
        
        mock_api_response = mock.Mock(name="GenerateSuggestedTargetingInsightsResponse")
        self.mock_audience_insights_service.generate_suggested_targeting_insights.return_value = mock_api_response

        with mock.patch("builtins.print") as mock_print:
            generate_audience_insights.generate_suggested_targeting_insights(
                self.mock_ads_client,
                self.mock_audience_insights_service,
                self.mock_google_ads_service,
                customer_id,
                location_id,
                custom_name,
            )

        self.mock_audience_insights_service.generate_suggested_targeting_insights.assert_called_once()
        actual_request = self.mock_audience_insights_service.generate_suggested_targeting_insights.call_args[1]['request']

        self.assertEqual(actual_request.customer_id, customer_id)
        self.assertEqual(actual_request.customer_insights_group, custom_name)
        
        # Assert audience definition (country locations)
        # The script directly modifies request.audience_definition.audience.country_locations.
        # client.get_type("GenerateSuggestedTargetingInsightsRequest") returns a mock,
        # and this mock needs to have audience_definition.audience.country_locations as a list
        # or a mock that behaves like a list for the .append() call to work.
        # The generic mock.Mock() from client.get_type should allow arbitrary attribute access
        # and list appends if the attribute is treated as a list.
        
        # To ensure the .append works as in the script, we can pre-set these attributes on the mock
        # returned by get_type if it were specific to this request type.
        # However, the current generic get_type mock should work because mock.Mock() creates attributes on the fly.
        # Let's verify the structure.
        # request_obj = client.get_type("GenerateSuggestedTargetingInsightsRequest")
        # location_info_obj = client.get_type("LocationInfo")
        # location_info_obj.geo_target_constant = geo_target_constant_path
        # request_obj.audience_definition.audience.country_locations.append(location_info_obj)

        self.assertTrue(hasattr(actual_request, 'audience_definition'))
        self.assertTrue(hasattr(actual_request.audience_definition, 'audience'))
        self.assertTrue(hasattr(actual_request.audience_definition.audience, 'country_locations'))
        
        # Ensure country_locations is a list or behaves like one (e.g. a mock that recorded an append)
        # If client.get_type returns a fresh Mock(), actual_request.audience_definition.audience.country_locations
        # will be a Mock itself. Accessing it (e.g. .append) will make that Mock record the call.
        # The actual list of locations will be on that mock's .append.call_args_list or similar,
        # or the mock itself if it was pre-configured to be a list.
        # Given the script code: `request_obj.audience_definition.audience.country_locations.append(location_info_obj)`
        # `country_locations` itself becomes a mock, and `append` is a method called on that mock.
        # So, we check the arguments passed to that `append` call.
        
        # The mock returned by get_type("GenerateSuggestedTargetingInsightsRequest") is actual_request.
        # actual_request.audience_definition.audience.country_locations is a Mock.
        # We need to check what append was called with on that mock.
        append_mock = actual_request.audience_definition.audience.country_locations.append
        append_mock.assert_called_once() # Ensure append was called
        
        # The argument to append should be the location_info_obj
        appended_location_info = append_mock.call_args[0][0] # args[0] is the first arg to append

        self.assertEqual(appended_location_info.geo_target_constant, mock_geo_target_path)

        mock_print.assert_called_once_with(mock_api_response)

    def test_list_audience_insights_attributes(self):
        customer_id = "test-customer-id"
        product_name = "Test Product"
        custom_name = "test-custom-audience-name"

        # Prepare a mock response
        mock_api_response = mock.Mock(name="ListAudienceInsightsAttributesResponse")
        
        # Mock attribute that will be printed
        mock_kg_attribute = mock.Mock()
        mock_kg_attribute.dimension = self.mock_ads_client.enums.AudienceInsightsDimensionEnum.KNOWLEDGE_GRAPH
        # To make the nested attribute access work in the SUT:
        # for attribute in response.attributes:
        #   if attribute.dimension == client.enums.AudienceInsightsDimensionEnum.KNOWLEDGE_GRAPH:
        #     print(attribute.attribute.entity.knowledge_graph_machine_id)
        # We need to ensure that `attribute.attribute.entity.knowledge_graph_machine_id` path exists on the mock.
        mock_kg_attribute.attribute = mock.Mock()
        mock_kg_attribute.attribute.entity = mock.Mock()
        mock_kg_attribute.attribute.entity.knowledge_graph_machine_id = "test-kg-machine-id"

        # Mock other attribute that won't be printed
        mock_other_attribute = mock.Mock()
        mock_other_attribute.dimension = self.mock_ads_client.enums.AudienceInsightsDimensionEnum.CATEGORY
        
        mock_api_response.attributes = [mock_kg_attribute, mock_other_attribute]
        
        self.mock_audience_insights_service.list_audience_insights_attributes.return_value = mock_api_response

        with mock.patch("builtins.print") as mock_print:
            generate_audience_insights.list_audience_insights_attributes(
                self.mock_ads_client,
                self.mock_audience_insights_service,
                customer_id,
                product_name,
                custom_name,
            )

        self.mock_audience_insights_service.list_audience_insights_attributes.assert_called_once()
        actual_request = self.mock_audience_insights_service.list_audience_insights_attributes.call_args[1]['request']

        self.assertEqual(actual_request.customer_id, customer_id)
        self.assertEqual(actual_request.query_text, product_name)
        self.assertEqual(actual_request.customer_insights_group, custom_name)
        
        expected_dimensions = [
            self.mock_ads_client.enums.AudienceInsightsDimensionEnum.CATEGORY,
            self.mock_ads_client.enums.AudienceInsightsDimensionEnum.KNOWLEDGE_GRAPH,
        ]
        # The script appends dimensions to the request object.
        # So, actual_request.dimensions will be a list (or a mock that acts like a list).
        self.assertCountEqual(list(actual_request.dimensions), expected_dimensions)

        # Assert that print was called with the knowledge_graph_machine_id
        mock_print.assert_called_once_with("test-kg-machine-id")

    @mock.patch("examples.audience_insights.generate_audience_insights.list_audience_insights_attributes")
    @mock.patch("examples.audience_insights.generate_audience_insights.generate_suggested_targeting_insights")
    @mock.patch("examples.audience_insights.generate_audience_insights.audience_composition_insights")
    def test_main_function_logic(
        self,
        mock_audience_composition_insights,
        mock_generate_suggested_targeting_insights,
        mock_list_audience_insights_attributes,
    ):
        test_customer_id = "test-main-customer-id"
        test_custom_name = "test-main-custom-name"

        # Hardcoded values from the script's main() function
        expected_location_id = "2840"  # Corresponds to United States
        expected_product_name = "Google"
        expected_user_interest_category_id = "92948"  # Corresponds to "Technology/Software/Internet Software"

        # Call the main function with the mocked client and test IDs
        generate_audience_insights.main(
            self.mock_ads_client, test_customer_id, test_custom_name
        )

        # Assert that audience_composition_insights was called correctly
        mock_audience_composition_insights.assert_called_once_with(
            self.mock_ads_client,
            self.mock_audience_insights_service,
            self.mock_google_ads_service,
            test_customer_id,
            expected_location_id,
            expected_user_interest_category_id,
            test_custom_name,
        )

        # Assert that generate_suggested_targeting_insights was called correctly
        mock_generate_suggested_targeting_insights.assert_called_once_with(
            self.mock_ads_client,
            self.mock_audience_insights_service,
            self.mock_google_ads_service,
            test_customer_id,
            expected_location_id,
            test_custom_name,
        )

        # Assert that list_audience_insights_attributes was called correctly
        mock_list_audience_insights_attributes.assert_called_once_with(
            self.mock_ads_client,
            self.mock_audience_insights_service,
            test_customer_id,
            expected_product_name,
            test_custom_name,
        )

    @mock.patch("argparse.ArgumentParser")
    @mock.patch("examples.audience_insights.generate_audience_insights.main") # Mock the main function itself
    def test_script_entry_point(
        self,
        mock_main_function, 
        mock_argparse,
    ):
        # This test focuses on the script's behavior when run from the command line,
        # specifically the logic within the `if __name__ == "__main__":` block.

        test_customer_id = "test-script-entry-customer-id"
        test_custom_name = "test-script-entry-custom-name"

        # Configure the mock ArgumentParser
        # The script creates an ArgumentParser, adds arguments, then calls parse_args.
        mock_args_object = mock.Mock()
        mock_args_object.customer_id = test_customer_id
        mock_args_object.custom_name = test_custom_name
        
        mock_parser_instance = mock.Mock()
        mock_parser_instance.parse_args.return_value = mock_args_object
        mock_argparse.return_value = mock_parser_instance

        # self.mock_load_from_storage is already set up in self.setUp()
        # to mock "google.ads.googleads.client.GoogleAdsClient.load_from_storage"
        # and return self.mock_ads_client.

        # Execute the script's entry-point code.
        # We use runpy.run_path to simulate running the script.
        # This will execute the `if __name__ == "__main__":` block in generate_audience_insights.py
        import runpy
        script_path = "examples/audience_insights/generate_audience_insights.py"
        
        # Store the original value of __name__ for generate_audience_insights if it's already imported
        # and reset it later to avoid side effects if tests are run multiple times in the same session.
        # However, runpy.run_path handles this by running in a fresh module namespace for `run_name`.
        
        runpy.run_path(script_path, run_name="__main__")

        # --- Assertions ---

        # 1. ArgumentParser was used correctly
        mock_argparse.assert_called_once()
        # Check that add_argument was called for customer_id and custom_name
        # The order of these calls can vary, so use assert_any_call
        mock_parser_instance.add_argument.assert_any_call(
            "-c", "--customer_id", type=str, required=True, help="The Google Ads customer ID."
        )
        mock_parser_instance.add_argument.assert_any_call(
            "-n", "--custom_name", type=str, required=True, help="Custom name to indentify audiences"
        )
        mock_parser_instance.parse_args.assert_called_once()

        # 2. GoogleAdsClient.load_from_storage was called
        # This mock is self.mock_load_from_storage, configured in setUp.
        self.mock_load_from_storage.assert_called_once()

        # 3. The script's main function (which we've mocked) was called with the correct arguments
        mock_main_function.assert_called_once_with(
            self.mock_ads_client,  # This is what self.mock_load_from_storage should return
            test_customer_id,      # From mock_args_object.customer_id
            test_custom_name       # From mock_args_object.custom_name
        )


if __name__ == "__main__":
    unittest.main()
