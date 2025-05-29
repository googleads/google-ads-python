import unittest
from unittest.mock import MagicMock, patch, call
import sys

# Add the examples directory to the system path to import the script
sys.path.append(".")

from examples.targeting.get_geo_target_constants_by_names import main

class TestGetGeoTargetConstantsByNames(unittest.TestCase):
    @patch("examples.targeting.get_geo_target_constants_by_names.GoogleAdsClient.load_from_storage")
    def test_main_function_calls(self, mock_load_client):
        # Create a mock GoogleAdsClient
        mock_google_ads_client = MagicMock()
        mock_load_client.return_value = mock_google_ads_client

        # Mock the GeoTargetConstantService
        mock_geo_target_constant_service = MagicMock()
        mock_google_ads_client.get_service.return_value = mock_geo_target_constant_service

        # Mock the GeoTargetConstantService
        mock_geo_target_constant_service = MagicMock()
        mock_google_ads_client.get_service.return_value = mock_geo_target_constant_service

        # Mock the SuggestGeoTargetConstantsRequest object that client.get_type will return.
        # client.get_type("SuggestGeoTargetConstantsRequest") returns an instance, not a class.
        mock_request_instance = MagicMock(name="SuggestGeoTargetConstantsRequestInstance")
        mock_google_ads_client.get_type.return_value = mock_request_instance
        
        # Set up the nested structure for location_names.names on this instance.
        # The script accesses request.location_names.names
        mock_location_names_object = MagicMock(name="LocationNamesObject")
        mock_request_instance.location_names = mock_location_names_object
        # Initialize .names as a list on this mock_location_names_object because the script appends to it.
        mock_location_names_object.names = []


        # Mock the response from suggest_geo_target_constants
        # This should be an iterable where each item has the attributes accessed in the script's loop
        mock_suggestion_1 = MagicMock()
        mock_suggestion_1.resource_name = "geoTargetConstants/1000"
        mock_suggestion_1.name = "Paris"
        mock_suggestion_1.country_code = "FR"
        mock_suggestion_1.target_type = "City"
        mock_suggestion_1.status = "ENABLED"
        
        mock_suggestion_2 = MagicMock()
        mock_suggestion_2.resource_name = "geoTargetConstants/2000"
        mock_suggestion_2.name = "Quebec"
        mock_suggestion_2.country_code = "CA"
        mock_suggestion_2.target_type = "Province"
        mock_suggestion_2.status = "ENABLED"

        # Mock the response from suggest_geo_target_constants
        mock_response = MagicMock()
        mock_response.geo_target_constant_suggestions = [
            mock_suggestion_1, mock_suggestion_2
        ]
        mock_geo_target_constant_service.suggest_geo_target_constants.return_value = mock_response
        
        # Call the main function
        main(mock_google_ads_client)

        # Assert that suggest_geo_target_constants was called
        mock_geo_target_constant_service.suggest_geo_target_constants.assert_called_once()

        # The first argument to suggest_geo_target_constants is the request object
        # In the script, this is constructed and then passed.
        # Our mock_request_instance should be what was passed.
        passed_request = mock_geo_target_constant_service.suggest_geo_target_constants.call_args[0][0]
        
        # Verify the attributes of the passed request object
        self.assertEqual(passed_request.locale, "en")
        self.assertEqual(passed_request.country_code, "FR")
        
        # Verify location_names.names
        # The script does: request.location_names.names.extend(["Paris", "Quebec", "Spain", "Deutschland"])
        # We check the final state of this list on mock_location_names_object.names
        self.assertListEqual(
            mock_location_names_object.names, 
            ["Paris", "Quebec", "Spain", "Deutschland"]
        )
        
        # Also, ensure the request object passed to the service call is the one we configured
        self.assertEqual(passed_request, mock_request_instance)


if __name__ == "__main__":
    unittest.main()
