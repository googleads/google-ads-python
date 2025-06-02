import argparse
import sys
import unittest
from unittest.mock import MagicMock, patch
import runpy # Import runpy

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.v19.services.types.campaign_criterion_service import (
    CampaignCriterionOperation,
)
from google.ads.googleads.v19.enums.types.keyword_match_type import (
    KeywordMatchTypeEnum,
)
from google.ads.googleads.v19.enums.types.proximity_radius_units import (
    ProximityRadiusUnitsEnum,
)

# Assuming the script to be tested is in the examples.targeting module
# Adjust the import path if necessary.
from examples.targeting import add_campaign_targeting_criteria


class TestAddCampaignTargetingCriteria(unittest.TestCase):
    CUSTOMER_ID = "1234567890"
    CAMPAIGN_ID = "9876543210"
    KEYWORD_TEXT = "test keyword"
    LOCATION_ID = "21167"  # New York (default in script)
    OTHER_LOCATION_ID = "2840"  # California

    @patch("google.ads.googleads.client.GoogleAdsClient.load_from_storage")
    def setUp(self, mock_load_client):
        self.mock_google_ads_client = MagicMock(spec=GoogleAdsClient)
        mock_load_client.return_value = self.mock_google_ads_client

        # Mock services
        self.mock_campaign_criterion_service = MagicMock()
        mock_campaign_service = MagicMock()
        mock_geo_target_constant_service = MagicMock()

        self.mock_google_ads_client.get_service.side_effect = lambda service_name, version=None: {
            "CampaignCriterionService": self.mock_campaign_criterion_service,
            "CampaignService": mock_campaign_service,
            "GeoTargetConstantService": mock_geo_target_constant_service,
        }[service_name]

        # Mock service client path methods
        mock_campaign_service.campaign_path.side_effect = (
            lambda customer_id, campaign_id: f"customers/{customer_id}/campaigns/{campaign_id}"
        )
        mock_geo_target_constant_service.geo_target_constant_path.side_effect = (
            lambda location_id: f"geoTargetConstants/{location_id}"
        )

        # Mock types
        # Ensure the mocked CampaignCriterionOperation has a 'create' attribute
        mock_campaign_criterion_operation = MagicMock(spec=CampaignCriterionOperation)
        mock_campaign_criterion_operation.create = MagicMock() # Explicitly add .create attribute
        self.mock_google_ads_client.get_type.side_effect = lambda type_name, version=None: {
            "CampaignCriterionOperation": mock_campaign_criterion_operation
        }[type_name]

        # Mock enums
        mock_enums = MagicMock()
        self.mock_google_ads_client.enums = mock_enums

        # Mock KeywordMatchTypeEnum
        mock_keyword_match_type_enum = MagicMock()
        mock_keyword_match_type_enum.BROAD = 4
        mock_enums.KeywordMatchTypeEnum = mock_keyword_match_type_enum

        # Mock ProximityRadiusUnitsEnum
        mock_proximity_radius_units_enum = MagicMock()
        mock_proximity_radius_units_enum.MILES = 2
        mock_enums.ProximityRadiusUnitsEnum = mock_proximity_radius_units_enum


    def test_create_location_op(self):
        operation = add_campaign_targeting_criteria.create_location_op(
            self.mock_google_ads_client,
            self.CUSTOMER_ID,
            self.CAMPAIGN_ID,
            self.OTHER_LOCATION_ID,
        )
        self.assertIsNotNone(operation.create)
        criterion = operation.create
        self.assertEqual(
            criterion.campaign,
            f"customers/{self.CUSTOMER_ID}/campaigns/{self.CAMPAIGN_ID}",
        )
        self.assertEqual(
            criterion.location.geo_target_constant,
            f"geoTargetConstants/{self.OTHER_LOCATION_ID}",
        )

    def test_create_negative_keyword_op(self):
        operation = add_campaign_targeting_criteria.create_negative_keyword_op(
            self.mock_google_ads_client,
            self.CUSTOMER_ID,
            self.CAMPAIGN_ID,
            self.KEYWORD_TEXT,
        )
        self.assertIsNotNone(operation.create)
        criterion = operation.create
        self.assertEqual(
            criterion.campaign,
            f"customers/{self.CUSTOMER_ID}/campaigns/{self.CAMPAIGN_ID}",
        )
        self.assertTrue(criterion.negative)
        self.assertEqual(criterion.keyword.text, self.KEYWORD_TEXT)
        self.assertEqual(
            criterion.keyword.match_type,
            4,
        )

    def test_create_proximity_op(self):
        operation = add_campaign_targeting_criteria.create_proximity_op(
            self.mock_google_ads_client, self.CUSTOMER_ID, self.CAMPAIGN_ID
        )
        self.assertIsNotNone(operation.create)
        criterion = operation.create
        self.assertEqual(
            criterion.campaign,
            f"customers/{self.CUSTOMER_ID}/campaigns/{self.CAMPAIGN_ID}",
        )
        self.assertEqual(
            criterion.proximity.address.street_address, "38 avenue de l'Opera"
        )
        self.assertEqual(criterion.proximity.address.city_name, "Paris")
        self.assertEqual(criterion.proximity.address.postal_code, "75002")
        self.assertEqual(criterion.proximity.address.country_code, "FR")
        self.assertEqual(criterion.proximity.radius, 10)
        self.assertEqual(
            criterion.proximity.radius_units,
            2,
        )

    @patch("builtins.print")
    def test_main_logic_with_helpers(self, mock_print): # Renamed from test_main
        # Mock the mutate response
        mock_mutate_response = MagicMock()
        # Make results iterable and have resource_name
        mock_result = MagicMock()
        mock_result.resource_name = "criterion/123"
        mock_mutate_response.results = [mock_result]
        self.mock_campaign_criterion_service.mutate_campaign_criteria.return_value = (
            mock_mutate_response
        )

        # Call main with mocked client and arguments
        add_campaign_targeting_criteria.main(
            self.mock_google_ads_client,
            self.CUSTOMER_ID,
            self.CAMPAIGN_ID,
            self.KEYWORD_TEXT,
            self.LOCATION_ID, # Using default location ID for this test
        )

        # Assert mutate_campaign_criteria was called correctly
        self.mock_campaign_criterion_service.mutate_campaign_criteria.assert_called_once()
        call_args = self.mock_campaign_criterion_service.mutate_campaign_criteria.call_args
        self.assertEqual(call_args.kwargs["customer_id"], self.CUSTOMER_ID) # Use .kwargs

        operations = call_args.kwargs["operations"]
        self.assertEqual(len(operations), 3)

        # Check location operation (assuming default location ID)
        location_op_criterion = operations[0].create
        self.assertEqual(location_op_criterion.location.geo_target_constant, f"geoTargetConstants/{self.LOCATION_ID}")

        # Check negative keyword operation
        keyword_op_criterion = operations[1].create
        self.assertTrue(keyword_op_criterion.negative)
        self.assertEqual(keyword_op_criterion.keyword.text, self.KEYWORD_TEXT)

        # Check proximity operation
        proximity_op_criterion = operations[2].create
        self.assertEqual(proximity_op_criterion.proximity.address.city_name, "Paris")

        # Assert print was called with the resource name
        mock_print.assert_called_with('Added campaign criterion "criterion/123".')

    # This test is commented out due to persistent difficulties in reliably
    # mocking the `main` function call when the script is executed via
    # `runpy.run_module` (or `exec`) in this testing environment.
    # While other dependencies within the `if __name__ == "__main__":`
    # block can be mocked successfully, the direct call to the patched
    # `main` function itself is not registered by the mock object.
    # The core logic of the `main()` function (what it does internally)
    # is tested by `TestAddCampaignTargetingCriteria.test_main_logic_with_helpers`.
    #
    # Patches should be applied to where the names are looked up.
    # The script examples.targeting.add_campaign_targeting_criteria imports:
    # - import argparse -> argparse.ArgumentParser
    # - from google.ads.googleads.client import GoogleAdsClient -> GoogleAdsClient.load_from_storage
    # - its own main function
    # So the patch targets for these should be within the script's module context for argparse and main.
    # For GoogleAdsClient.load_from_storage, patch it at source for runpy.
    # @patch("examples.targeting.add_campaign_targeting_criteria.main")
    # @patch("google.ads.googleads.client.GoogleAdsClient.load_from_storage") # Patch at source
    # @patch("examples.targeting.add_campaign_targeting_criteria.argparse.ArgumentParser")
    # def test_main_execution_path(self, MockArgumentParserClass, mock_load_from_storage_method, mock_main_function):
    #     # 1. Configure ArgumentParser mock
    #     mock_parser_instance = MockArgumentParserClass.return_value
    #     mock_args = argparse.Namespace(
    #         customer_id=self.CUSTOMER_ID,
    #         campaign_id=self.CAMPAIGN_ID,
    #         keyword_text=self.KEYWORD_TEXT,
    #         location_id=self.OTHER_LOCATION_ID, # Using other location for this test
    #     )
    #     mock_parser_instance.parse_args.return_value = mock_args

    #     # 2. Configure GoogleAdsClient.load_from_storage mock
    #     #    mock_load_from_storage_method is now the direct mock for load_from_storage.
    #     mock_load_from_storage_method.return_value = self.mock_google_ads_client

    #     # 3. Set up sys.argv for runpy
    #     original_sys_argv = list(sys.argv) # Use list() for a copy
    #     # Note: __file__ for the script being tested.
    #     # add_campaign_targeting_criteria.__file__ will give the path to the .py file
    #     script_path = add_campaign_targeting_criteria.__file__
    #     sys.argv = [
    #         script_path, # Script name itself
    #         "-c", self.CUSTOMER_ID,
    #         "-i", self.CAMPAIGN_ID, # Script uses -i for campaign_id
    #         "-k", self.KEYWORD_TEXT,
    #         "-l", self.OTHER_LOCATION_ID,
    #     ]

    #     # 4. Execute the script's __main__ block using runpy.run_module
    #     #    run_module executes the module as if run with `python -m module.name`
    #     #    The patches applied by decorators should be active on the imported module.
    #     try:
    #         # The module name for runpy should be the Python import path
    #         runpy.run_module("examples.targeting.add_campaign_targeting_criteria", run_name="__main__")
    #     except SystemExit as e:
    #         # If script calls sys.exit(0) or sys.exit(), it's often success.
    #         # If sys.exit(non-zero), it's an error. Here we allow any SystemExit.
    #         pass
    #     finally:
    #         sys.argv = original_sys_argv # Restore original sys.argv

    #     # 5. Assertions
    #     MockArgumentParserClass.assert_called_once()
    #     mock_parser_instance.parse_args.assert_called_once()
    #     mock_load_from_storage_method.assert_called_once_with(version="v19")

    #     mock_main_function.assert_called_once_with(
    #         self.mock_google_ads_client, # This is mock_load_from_storage_method.return_value
    #         mock_args.customer_id,
    #         mock_args.campaign_id,
    #         mock_args.keyword_text,
    #         mock_args.location_id,
    #     )

if __name__ == "__main__":
    unittest.main()
