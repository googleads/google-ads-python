import unittest
from unittest.mock import Mock, patch, call
import sys

try:
    from examples.targeting import get_geo_target_constants_by_names
except ImportError:
    import get_geo_target_constants_by_names

# Script constants used in requests
_LOCALE = "en"
_COUNTRY_CODE = "FR"
_LOCATION_NAMES = ["Paris", "Quebec", "Spain", "Deutschland"]

class TestGetGeoTargetConstantsByNames(unittest.TestCase):

    @patch("examples.targeting.get_geo_target_constants_by_names.GoogleAdsClient.load_from_storage")
    def setUp(self, mock_load_from_storage):
        self.mock_google_ads_client = Mock()
        mock_load_from_storage.return_value = self.mock_google_ads_client

        self.mock_gtc_service = Mock()
        self.mock_google_ads_client.get_service.return_value = self.mock_gtc_service

        self.mock_gtc_request = Mock()
        # Ensure location_names.names can be extended
        self.mock_gtc_request.location_names = Mock()
        self.mock_gtc_request.location_names.names = [] # Initialize as a list

        self.mock_google_ads_client.get_type.return_value = self.mock_gtc_request

        # Prepare mock response for suggest_geo_target_constants
        self.mock_suggestion_response = Mock()

        # Create mock suggestions
        status_enabled_mock = Mock()
        status_enabled_mock.name = "ENABLED"

        suggestion1_geo_constant = Mock()
        suggestion1_geo_constant.configure_mock(
            resource_name="geoTargetConstants/1", name="Paris", country_code="FR",
            target_type="City", status=status_enabled_mock
        )
        suggestion1 = Mock()
        suggestion1.configure_mock(
            geo_target_constant=suggestion1_geo_constant, locale="en", reach=1000000, search_term="Paris"
        )

        suggestion2_geo_constant = Mock()
        suggestion2_geo_constant.configure_mock(
            resource_name="geoTargetConstants/2", name="Quebec", country_code="CA",
            target_type="Province", status=status_enabled_mock # Can reuse the same status mock if appropriate
        )
        suggestion2 = Mock()
        suggestion2.configure_mock(
            geo_target_constant=suggestion2_geo_constant, locale="en", reach=500000, search_term="Quebec"
        )

        self.mock_suggestion_response.geo_target_constant_suggestions = [suggestion1, suggestion2]
        self.mock_gtc_service.suggest_geo_target_constants.return_value = self.mock_suggestion_response

    @patch("builtins.print")
    def test_main_logic(self, mock_print):
        get_geo_target_constants_by_names.main(self.mock_google_ads_client)

        # Verify get_service call
        self.mock_google_ads_client.get_service.assert_called_once_with("GeoTargetConstantService")

        # Verify get_type call for request object
        self.mock_google_ads_client.get_type.assert_called_once_with("SuggestGeoTargetConstantsRequest")

        # Verify request attributes
        self.assertEqual(self.mock_gtc_request.locale, _LOCALE)
        self.assertEqual(self.mock_gtc_request.country_code, _COUNTRY_CODE)
        # Check that extend was called on the mock list correctly or check final state
        # For simplicity, check final state:
        self.assertListEqual(list(self.mock_gtc_request.location_names.names), _LOCATION_NAMES)


        # Verify suggest_geo_target_constants call
        self.mock_gtc_service.suggest_geo_target_constants.assert_called_once_with(self.mock_gtc_request)

        # Verify print calls
        expected_print_calls = [
            call(
                f"geoTargetConstants/1 (Paris, FR, City, ENABLED) "
                f"is found in locale (en) with reach (1000000) from search term (Paris)."
            ),
            call(
                f"geoTargetConstants/2 (Quebec, CA, Province, ENABLED) " # Using CA from mock data
                f"is found in locale (en) with reach (500000) from search term (Quebec)."
            ),
        ]
        mock_print.assert_has_calls(expected_print_calls, any_order=False)

    @patch("examples.targeting.get_geo_target_constants_by_names.GoogleAdsClient.load_from_storage")
    @patch("examples.targeting.get_geo_target_constants_by_names.main")
    def test_main_execution_path(self, mock_main_function, mock_load_from_storage):
        mock_client_instance_main = Mock()
        mock_load_from_storage.return_value = mock_client_instance_main

        # Configure mock_client_instance_main to handle calls made by the script's main()
        mock_main_gtc_service = Mock()
        mock_client_instance_main.get_service.return_value = mock_main_gtc_service

        mock_main_gtc_request = Mock()
        mock_main_gtc_request.location_names = Mock()
        mock_main_gtc_request.location_names.names = [] # Ensure it's extendable
        mock_client_instance_main.get_type.return_value = mock_main_gtc_request

        mock_main_suggestions_response = Mock()
        # Make geo_target_constant_suggestions iterable, e.g., an empty list for simplicity,
        # as we are not checking print output for this test, only that main is called.
        mock_main_suggestions_response.geo_target_constant_suggestions = []
        mock_main_gtc_service.suggest_geo_target_constants.return_value = mock_main_suggestions_response

        # Execute the script's __main__ block
        # This script doesn't have command line args for main() itself.
        # We can directly run the __main__ part of the script,
        # or use runpy if we need to simulate full module execution context.
        # Using runpy for consistency.
        import runpy
        runpy.run_module("examples.targeting.get_geo_target_constants_by_names", run_name="__main__")

        mock_main_function.assert_called_once_with(mock_client_instance_main)
        mock_load_from_storage.assert_called_once() # Ensure client loading was attempted

if __name__ == "__main__":
    unittest.main()
