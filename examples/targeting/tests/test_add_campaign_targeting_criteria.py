import unittest
from unittest.mock import MagicMock, patch, call
import sys

# Add the examples directory to the system path to import the script
sys.path.append(".")

from examples.targeting.add_campaign_targeting_criteria import main

class TestAddCampaignTargetingCriteria(unittest.TestCase):
    @patch("examples.targeting.add_campaign_targeting_criteria.GoogleAdsClient.load_from_storage")
    def test_main_function_calls(self, mock_load_client):
        # Mock customer and campaign IDs
        MOCK_CUSTOMER_ID = "1234567890"
        MOCK_CAMPAIGN_ID = "9876543210"
        MOCK_KEYWORD_TEXT = "negative keyword"
        MOCK_LOCATION_ID = "21167"  # New York

        # Create a mock GoogleAdsClient
        mock_google_ads_client = MagicMock()
        mock_load_client.return_value = mock_google_ads_client

        # Mock the CampaignCriterionService
        mock_campaign_criterion_service = MagicMock()
        mock_google_ads_client.get_service.return_value = mock_campaign_criterion_service

        # Mock the get_type method for various types
        mock_campaign_criterion_operation = MagicMock()
        mock_keyword_info = MagicMock()
        mock_location_info = MagicMock()
        mock_proximity_info = MagicMock()
        mock_address_info = MagicMock()

        # Configure client.get_type to return appropriate mocks
        def get_type_side_effect(type_name, version=None):
            if type_name == "CampaignCriterionOperation":
                # Return a new MagicMock each time to ensure operations are distinct
                return MagicMock()
            elif type_name == "KeywordInfo":
                return mock_keyword_info
            elif type_name == "LocationInfo":
                return mock_location_info
            elif type_name == "ProximityInfo":
                return mock_proximity_info
            elif type_name == "AddressInfo":
                return mock_address_info
            return MagicMock()

        mock_google_ads_client.get_type.side_effect = get_type_side_effect

        # Call the main function
        main(
            mock_google_ads_client,
            MOCK_CUSTOMER_ID,
            MOCK_CAMPAIGN_ID,
            MOCK_KEYWORD_TEXT,
            MOCK_LOCATION_ID,
        )

        # Assert that mutate_campaign_criteria was called
        mock_campaign_criterion_service.mutate_campaign_criteria.assert_called_once()

        # Get the arguments passed to mutate_campaign_criteria
        args, kwargs = mock_campaign_criterion_service.mutate_campaign_criteria.call_args
        
        self.assertEqual(kwargs["customer_id"], MOCK_CUSTOMER_ID)
        operations = kwargs["operations"]
        self.assertEqual(len(operations), 3) # Location, Negative Keyword, Proximity

        # Expected campaign resource name format
        expected_campaign_rname = mock_google_ads_client.get_service(
            "CampaignService"
        ).campaign_path(MOCK_CUSTOMER_ID, MOCK_CAMPAIGN_ID)


        # --- Verify Location Operation ---
        location_operation = operations[0]
        self.assertEqual(location_operation.create.campaign, expected_campaign_rname)
        # LocationInfo is set directly on the criterion, not via client.get_type in the script for create
        # We need to access it from the actual operation object passed to the service
        created_location_criterion = location_operation.create
        self.assertEqual(
            created_location_criterion.location.geo_target_constant,
            mock_google_ads_client.get_service(
                "GeoTargetConstantService"
            ).geo_target_constant_path(MOCK_LOCATION_ID),
        )

        # --- Verify Negative Keyword Operation ---
        keyword_operation = operations[1]
        self.assertEqual(keyword_operation.create.campaign, expected_campaign_rname)
        created_keyword_criterion = keyword_operation.create
        self.assertTrue(created_keyword_criterion.negative)
        self.assertEqual(created_keyword_criterion.keyword.text, MOCK_KEYWORD_TEXT)
        # Access KeywordMatchTypeEnum from the GoogleAdsClient's enums
        KeywordMatchTypeEnum = mock_google_ads_client.enums.KeywordMatchTypeEnum
        self.assertEqual(created_keyword_criterion.keyword.match_type, KeywordMatchTypeEnum.BROAD)

        # --- Verify Proximity Operation ---
        proximity_operation = operations[2]
        self.assertEqual(proximity_operation.create.campaign, expected_campaign_rname)
        created_proximity_criterion = proximity_operation.create
        
        # AddressInfo
        self.assertEqual(created_proximity_criterion.proximity.address.street_address, "38 avenue de l'Opera")
        self.assertEqual(created_proximity_criterion.proximity.address.city_name, "Paris")
        self.assertEqual(created_proximity_criterion.proximity.address.postal_code, "75002")
        self.assertEqual(created_proximity_criterion.proximity.address.country_code, "FR")
        
        # Radius
        self.assertEqual(created_proximity_criterion.proximity.radius, 10.0)
        # Access ProximityRadiusUnitsEnum from the GoogleAdsClient's enums
        ProximityRadiusUnitsEnum = mock_google_ads_client.enums.ProximityRadiusUnitsEnum
        self.assertEqual(created_proximity_criterion.proximity.radius_units, ProximityRadiusUnitsEnum.MILES)


if __name__ == "__main__":
    unittest.main()
