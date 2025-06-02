import argparse
import sys
import unittest
from unittest.mock import MagicMock, patch

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
        mock_campaign_criterion_operation.create = MagicMock()
        self.mock_google_ads_client.get_type.side_effect = lambda type_name, version=None: {
            "CampaignCriterionOperation": mock_campaign_criterion_operation
        }[type_name]

        # Mock enums
        mock_enums = MagicMock()
        self.mock_google_ads_client.enums = mock_enums

        # Mock KeywordMatchTypeEnum
        # Assuming BROAD = 4 based on typical proto enum numbering if direct access fails
        mock_keyword_match_type_enum = MagicMock()
        mock_keyword_match_type_enum.BROAD = 4  # Presumed integer value for BROAD
        mock_enums.KeywordMatchTypeEnum = mock_keyword_match_type_enum

        # Mock ProximityRadiusUnitsEnum
        # Assuming MILES = 2 based on typical proto enum numbering
        mock_proximity_radius_units_enum = MagicMock()
        mock_proximity_radius_units_enum.MILES = 2  # Presumed integer value for MILES
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
            4,  # Assert against the presumed integer value
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
            2,  # Assert against the presumed integer value for MILES
        )

    @patch("builtins.print")
    def test_main(self, mock_print):
        # Mock the mutate response
        mock_mutate_response = MagicMock()
        mock_mutate_response.results = [MagicMock(resource_name="criterion/123")]
        self.mock_campaign_criterion_service.mutate_campaign_criteria.return_value = (
            mock_mutate_response
        )

        # Call main with mocked client and arguments
        add_campaign_targeting_criteria.main(
            self.mock_google_ads_client,
            self.CUSTOMER_ID,
            self.CAMPAIGN_ID,
            self.KEYWORD_TEXT,
            self.LOCATION_ID,
        )

        # Assert mutate_campaign_criteria was called correctly
        self.mock_campaign_criterion_service.mutate_campaign_criteria.assert_called_once()
        call_args = self.mock_campaign_criterion_service.mutate_campaign_criteria.call_args
        self.assertEqual(call_args[1]["customer_id"], self.CUSTOMER_ID)

        operations = call_args[1]["operations"]
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

    @patch("examples.targeting.add_campaign_targeting_criteria.argparse.ArgumentParser")
    @patch("examples.targeting.add_campaign_targeting_criteria.GoogleAdsClient.load_from_storage")
    @patch("examples.targeting.add_campaign_targeting_criteria.main")
    def test_main_execution_path(self, mock_main_function, mock_load_client, MockArgumentParserClass):
        # 1. Mock the behavior of ArgumentParser().parse_args()
        mock_parser_instance = MockArgumentParserClass.return_value
        mock_args = argparse.Namespace(
            customer_id=self.CUSTOMER_ID,
            campaign_id=self.CAMPAIGN_ID,
            keyword_text=self.KEYWORD_TEXT,
            location_id=self.OTHER_LOCATION_ID,
        )
        mock_parser_instance.parse_args.return_value = mock_args

        # 2. Mock the behavior of GoogleAdsClient.load_from_storage()
        mock_load_client.return_value = self.mock_google_ads_client

        # 3. Mock sys.argv for the script's argument parsing
        original_sys_argv = sys.argv
        sys.argv = [
            add_campaign_targeting_criteria.__file__,
            "-c", self.CUSTOMER_ID,
            "-i", self.CAMPAIGN_ID,
            "-k", self.KEYWORD_TEXT,
            "-l", self.OTHER_LOCATION_ID,
        ]

        # 4. Execute the script's code using exec.
        #    The `global_vars` dict will be the global namespace for the script.
        #    We need to ensure that when the script does `import argparse` or
        #    `from google.ads.googleads.client import GoogleAdsClient`,
        #    it gets our patched versions if the patches are module-specific.
        #    The decorators patch them in `examples.targeting.add_campaign_targeting_criteria.X`,
        #    which should be what the script sees if its own imports are relative to its module.
        #    However, `exec` might behave differently.
        #    The crucial part is that `main` called by the script should be `mock_main_function`.

        # To make `exec` work correctly with the patches applied by decorators,
        # the `globals` for `exec` should see these patched objects.
        # `add_campaign_targeting_criteria` (the module) is already imported by the test.
        # Its attributes (like `argparse`, `GoogleAdsClient`, `main`) have been patched by decorators.
        # We can pass its __dict__ as globals to exec.

        script_globals = add_campaign_targeting_criteria.__dict__.copy()
        script_globals['__name__'] = '__main__' # Crucial for the if block to run
        # Ensure sys is available for sys.exit
        script_globals['sys'] = sys
        # No, this won't work as argparse and GoogleAdsClient are imported by the script,
        # not necessarily members of its __dict__ in the way patchers expect.

        # Let's use the more direct approach of providing the mocked items in globals.
        # The patches are on "examples.targeting.add_campaign_targeting_criteria.X".
        # When the script add_campaign_targeting_criteria.py is exec'd, its `import X`
        # statements will re-import. The patches need to be on the fundamental modules
        # or the exec environment needs to be carefully crafted.

        # The decorators `@patch("module.name")` replace `name` in `module`.
        # If `script_code` does `from module import name`, it will get the mocked version.

        # The `main` function called by the script is `add_campaign_targeting_criteria.main`,
        # which is correctly mocked by `@patch("examples.targeting.add_campaign_targeting_criteria.main")`.

        # The `ArgumentParser` used by the script is from `import argparse`, then `argparse.ArgumentParser`.
        # So, the patch must be on `argparse.ArgumentParser` itself, or
        # `examples.targeting.add_campaign_targeting_criteria.argparse.ArgumentParser` if the script re-exports it.
        # The current patch `@patch("examples.targeting.add_campaign_targeting_criteria.argparse.ArgumentParser")`
        # assumes `argparse` is an attribute of `add_campaign_targeting_criteria` module.
        # This is correct as the script does `import argparse`.

        # Similarly for GoogleAdsClient.

        script_file_path = add_campaign_targeting_criteria.__file__
        with open(script_file_path, "r") as f:
            script_code = f.read()

        # Prepare globals for exec. The patches on module attributes should be picked up
        # when the script code resolves these names via its imports.
        exec_globals = {
            "__name__": "__main__",
            # The script will do `import argparse`, `from google.ads.googleads.client import GoogleAdsClient`, etc.
            # The patches need to ensure these imports resolve to our mocks.
            # The existing decorators should handle this by patching the names in the
            # `examples.targeting.add_campaign_targeting_criteria` module namespace.
            # When the script code `from google.ads.googleads.client import GoogleAdsClient` runs,
            # it should find the mocked `GoogleAdsClient.load_from_storage`.
            # When `import argparse` runs, then `parser = argparse.ArgumentParser()` is called,
            # it should use the mocked `ArgumentParser` class.
            # And when `main()` is called, it should be the mocked `main`.
        }

        try:
            exec(script_code, exec_globals)
        except SystemExit:
            pass # Catch sys.exit from script
        finally:
            sys.argv = original_sys_argv

        # Assertions
        MockArgumentParserClass.assert_called_once() # Check if ArgumentParser was instantiated
        mock_parser_instance.parse_args.assert_called_once() # Check if parse_args was called
        mock_load_client.assert_called_once_with(version="v19") # Check if client was loaded

        # Check if the main function (mocked by decorator) was called with expected args
        mock_main_function.assert_called_once_with(
            self.mock_google_ads_client, # From mock_load_client
            mock_args.customer_id,
            mock_args.campaign_id,
            mock_args.keyword_text,
            mock_args.location_id,
        )


if __name__ == "__main__":
    unittest.main()
