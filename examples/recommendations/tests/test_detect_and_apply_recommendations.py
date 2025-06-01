import argparse
import unittest
from unittest.mock import MagicMock, patch
import io

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

# Assuming the script to be tested is accessible in the path
# This might need adjustment based on the actual project structure
from examples.recommendations.detect_and_apply_recommendations import (
    detect_and_apply_recommendations,
    build_recommendation_operation,
    apply_recommendations,
    main as detect_and_apply_main
)


class TestDetectAndApplyRecommendations(unittest.TestCase):

    @patch("examples.recommendations.detect_and_apply_recommendations.GoogleAdsClient")
    def test_detect_and_apply_recommendations_retrieves_and_applies(self, mock_google_ads_client_constructor):
        # Mock the GoogleAdsClient instance and its services
        mock_client = MagicMock(spec=GoogleAdsClient)
        mock_google_ads_client_constructor.load_from_storage.return_value = mock_client

        mock_googleads_service = mock_client.get_service.return_value
        mock_recommendation_service = mock_client.get_service.return_value

        # Simulate a recommendation being returned by GoogleAdsService
        mock_recommendation = MagicMock()
        mock_recommendation.resource_name = "customers/12345/recommendations/67890"
        mock_recommendation.campaign = "customers/12345/campaigns/111"
        mock_recommendation.keyword_recommendation.keyword.text = "test keyword"
        mock_recommendation.keyword_recommendation.keyword.match_type = "BROAD"

        mock_search_response_row = MagicMock()
        mock_search_response_row.recommendation = mock_recommendation

        mock_search_response = MagicMock()
        mock_search_response.results = [mock_search_response_row]
        mock_googleads_service.search.return_value = mock_search_response

        # Simulate a successful application response
        mock_apply_response_result = MagicMock()
        mock_apply_response_result.resource_name = "customers/12345/recommendations/67890"
        mock_apply_response = MagicMock()
        # The result from apply_recommendation is a list of ApplyRecommendationResult
        # where each result itself doesn't have a resource_name directly, but is the result object.
        # Let's assume the example prints the resource_name of the first result object if successful.
        # The actual API might return a list of results, and each has a resource_name.
        # The example code is `for result in response.results: print(f"Applied a recommendation with resource name: '{result[0].resource_name}'.")`
        # This implies response.results is a list of lists/tuples where the first element has resource_name.
        # This seems unusual for the API. Let's adjust based on typical API behavior: response.results is a list of result objects.
        # The example code `result[0].resource_name` is likely a typo and should be `result.resource_name`.
        # For now, I will mock according to the provided example code's expectation.

        # Correction: The ApplyRecommendationResponse contains a list of ApplyRecommendationResult messages.
        # Each ApplyRecommendationResult has a resource_name field.
        # So response.results should be a list of objects, each with a resource_name.
        mock_individual_apply_result = MagicMock()
        mock_individual_apply_result.resource_name = "customers/12345/recommendations/67890"
        mock_apply_response.results = [mock_individual_apply_result]
        mock_recommendation_service.apply_recommendation.return_value = mock_apply_response

        # Mock the operation type
        mock_operation = MagicMock()
        mock_client.get_type.return_value = mock_operation

        customer_id = "12345"
        detect_and_apply_recommendations(mock_client, customer_id)

        # Assertions
        mock_googleads_service.search.assert_called_once()
        # Check if build_recommendation_operation was called (implicitly via operations.append)
        self.assertTrue(mock_client.get_type.called)
        # Check if apply_recommendation was called
        mock_recommendation_service.apply_recommendation.assert_called_once()
        args, kwargs = mock_recommendation_service.apply_recommendation.call_args
        self.assertEqual(kwargs["customer_id"], customer_id)
        self.assertEqual(len(kwargs["operations"]), 1) # Ensure one operation was created and passed


    @patch("examples.recommendations.detect_and_apply_recommendations.GoogleAdsClient")
    def test_detect_and_apply_recommendations_no_recommendations_found(self, mock_google_ads_client_constructor):
        mock_client = MagicMock(spec=GoogleAdsClient)
        mock_google_ads_client_constructor.load_from_storage.return_value = mock_client
        mock_googleads_service = mock_client.get_service.return_value
        mock_recommendation_service = mock_client.get_service.return_value

        # Simulate no recommendations being returned
        mock_search_response = MagicMock()
        mock_search_response.results = [] # Empty results
        mock_googleads_service.search.return_value = mock_search_response

        customer_id = "12345"
        detect_and_apply_recommendations(mock_client, customer_id)

        mock_googleads_service.search.assert_called_once()
        # apply_recommendations should not be called if no recommendations are found
        mock_recommendation_service.apply_recommendation.assert_not_called()

    def test_build_recommendation_operation(self):
        mock_client = MagicMock(spec=GoogleAdsClient)
        mock_operation_type = MagicMock()
        mock_client.get_type.return_value = mock_operation_type

        recommendation_resource_name = "customers/123/recommendations/456"
        operation = build_recommendation_operation(mock_client, recommendation_resource_name)

        mock_client.get_type.assert_called_once_with("ApplyRecommendationOperation")
        self.assertEqual(operation.resource_name, recommendation_resource_name)


    def test_apply_recommendations(self):
        mock_client = MagicMock(spec=GoogleAdsClient)
        mock_recommendation_service = mock_client.get_service.return_value

        mock_apply_response_result = MagicMock()
        mock_apply_response_result.resource_name = "customers/123/recommendations/789"
        mock_apply_response = MagicMock()
        # If script uses result[0].resource_name, results should be list of lists/tuples
        mock_apply_response.results = [[mock_apply_response_result]]
        mock_recommendation_service.apply_recommendation.return_value = mock_apply_response

        customer_id = "123"
        operations = [MagicMock()] # List of mock operations

        # Capture stdout to check print statements
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            apply_recommendations(mock_client, customer_id, operations)

        mock_recommendation_service.apply_recommendation.assert_called_once_with(
            customer_id=customer_id, operations=operations
        )
        # Check if the success message was printed
        self.assertIn("Applied a recommendation with resource name: 'customers/123/recommendations/789'", mock_stdout.getvalue())

    @patch("examples.recommendations.detect_and_apply_recommendations.argparse.ArgumentParser")
    @patch("examples.recommendations.detect_and_apply_recommendations.GoogleAdsClient")
    @patch("examples.recommendations.detect_and_apply_recommendations.detect_and_apply_recommendations")
    def test_main_function(self, mock_detect_and_apply, mock_google_ads_client_constructor, mock_argparse):
        # Mock command line arguments
        mock_args = MagicMock()
        mock_args.customer_id = "test_customer_id"
        mock_argparse.return_value.parse_args.return_value = mock_args

        # Mock GoogleAdsClient
        mock_client_instance = MagicMock()
        mock_google_ads_client_constructor.load_from_storage.return_value = mock_client_instance

        detect_and_apply_main(mock_client_instance, "test_customer_id") # Use string directly

        # The main function `detect_and_apply_main` calls `detect_and_apply_recommendations`.
        # `load_from_storage` is not called by `detect_and_apply_main`.
        mock_detect_and_apply.assert_called_once_with(mock_client_instance, "test_customer_id")
        # Ensure load_from_storage was NOT called by this specific test path
        mock_google_ads_client_constructor.load_from_storage.assert_not_called()

    @patch("examples.recommendations.detect_and_apply_recommendations.GoogleAdsClient.load_from_storage")
    @patch("examples.recommendations.detect_and_apply_recommendations.detect_and_apply_recommendations")
    @patch("examples.recommendations.detect_and_apply_recommendations.sys.exit") # To prevent test runner from exiting
    @patch("builtins.print") # To capture print output for errors
    def test_main_function_handles_google_ads_exception(self, mock_print, mock_sys_exit, mock_detect_and_apply, mock_load_from_storage):
        # Mock command line arguments
        # To simulate calling the script directly, we need to patch the main invocation part.
        # The main() function itself is called with client and customer_id.
        # The if __name__ == "__main__": block is what we need to simulate for CLI arg parsing.

        # For this test, let's assume main() is called and detect_and_apply_recommendations raises an exception.
        mock_client = MagicMock()
        customer_id = "test_customer_id"

        # Configure the mocked function to raise GoogleAdsException
        mock_failure = MagicMock()
        mock_error = MagicMock()
        mock_error.message = "Test error message"
        mock_error.location.field_path_elements = [MagicMock(field_name="test_field")]
        mock_failure.errors = [mock_error]

        # Ensure ex.error.code().name is a valid callable chain
        mock_error_code = MagicMock()
        mock_error_code.name = "INTERNAL_ERROR" # Example error code name

        mock_ex = GoogleAdsException(
            error=MagicMock(code=lambda: mock_error_code), # error.code() should return an object with a name attribute
            failure=mock_failure,
            request_id="test_request_id",
            call=None # Not strictly necessary for this test
        )

        # For the main function within the script (not the test_main_function)
        # We need to simulate the `if __name__ == "__main__":` block
        # This means we'd patch `argparse.ArgumentParser`, `GoogleAdsClient.load_from_storage`, and the `main` function itself if testing that block.
        # However, the current `main` function in the script calls `detect_and_apply_recommendations`.
        # Let's test the exception handling within the `if __name__ == "__main__":` block.

        # To do this, we need to patch where GoogleAdsClient.load_from_storage is called in the script's main execution block
        # and where the script's main function is called.

        mock_load_from_storage.return_value = mock_client
        mock_detect_and_apply.side_effect = mock_ex
        mock_configured_client = mock_load_from_storage.return_value

        with self.assertRaises(GoogleAdsException) as cm:
            detect_and_apply_main(mock_configured_client, customer_id)

        self.assertEqual(cm.exception, mock_ex)
        # The following lines were intended to test the script's __main__ block behavior,
        # which is complex for a unit test. This part of the test primarily ensures
        # that if detect_and_apply_main (via detect_and_apply_recommendations)
        # raises, it propagates the GoogleAdsException.

        # To test a simpler exception raising:
        # mock_detect_and_apply.side_effect = ValueError("Test Value Error")
        # with self.assertRaises(ValueError) as ve:
        #    detect_and_apply_main(mock_configured_client, customer_id)
        # self.assertEqual(str(ve.exception), "Test Value Error")


if __name__ == "__main__":
    unittest.main()
