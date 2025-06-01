import unittest
from unittest import mock

from google.ads.googleads.errors import GoogleAdsException

# Assuming the script to be tested is in the parent directory.
# Adjust the import path as necessary if the script is located elsewhere.
from examples.misc import add_ad_group_image_asset


class TestAddAdGroupImageAsset(unittest.TestCase):
    """Tests for the add_ad_group_image_asset script."""

    @mock.patch("examples.misc.add_ad_group_image_asset.GoogleAdsClient")
    def setUp(self, mock_google_ads_client):
        """Set up mock objects for testing."""
        self.mock_client = mock_google_ads_client.load_from_storage.return_value
        self.mock_ad_group_asset_service = self.mock_client.get_service(
            "AdGroupAssetService"
        )
        self.mock_ad_group_asset_operation = self.mock_client.get_type(
            "AdGroupAssetOperation"
        )
        # Mock the constructor for AdGroupAsset
        self.mock_ad_group_asset = self.mock_client.get_type("AdGroupAsset")

        # Mock the response from mutate_ad_group_assets
        self.mock_mutate_response = mock.Mock()
        self.mock_ad_group_asset_service.mutate_ad_group_assets.return_value = (
            self.mock_mutate_response
        )

    def test_main_success(self):
        """Test a successful run of the main function."""
        customer_id = "1234567890"
        ad_group_id = "9876543210"
        image_asset_id = "1122334455"

        add_ad_group_image_asset.main(
            self.mock_client, customer_id, ad_group_id, image_asset_id
        )

        self.mock_ad_group_asset_service.mutate_ad_group_assets.assert_called_once()
        # Get the call arguments to inspect them
        call_args = self.mock_ad_group_asset_service.mutate_ad_group_assets.call_args
        # Expected operation
        expected_operation = self.mock_ad_group_asset_operation.return_value
        # Check that the customer_id in the call matches
        self.assertEqual(call_args[1]["customer_id"], customer_id)
        # Check that the operation passed to the service matches expectations
        # This requires checking the attributes of the operation object
        # that was passed to mutate_ad_group_assets
        actual_operation = call_args[1]["operations"][0]
        self.assertEqual(actual_operation.create.ad_group, f"customers/{customer_id}/adGroups/{ad_group_id}")
        self.assertEqual(actual_operation.create.asset, f"customers/{customer_id}/assets/{image_asset_id}")


    def test_main_google_ads_exception(self):
        """Test handling of GoogleAdsException."""
        customer_id = "1234567890"
        ad_group_id = "9876543210"
        image_asset_id = "1122334455"

        # Configure the mock service to raise GoogleAdsException
        self.mock_ad_group_asset_service.mutate_ad_group_assets.side_effect = (
            GoogleAdsException(None, None, None)
        )

        with self.assertRaises(GoogleAdsException):
            add_ad_group_image_asset.main(
                self.mock_client, customer_id, ad_group_id, image_asset_id
            )

    @mock.patch("examples.misc.add_ad_group_image_asset.argparse.ArgumentParser")
    @mock.patch("examples.misc.add_ad_group_image_asset.GoogleAdsClient")
    def test_argument_parsing(
        self, mock_google_ads_client, mock_argument_parser
    ):
        """Test that main is called with parsed arguments."""
        # Set up the mock argument parser
        mock_args = mock.Mock()
        mock_args.customer_id = "test_customer_id"
        mock_args.ad_group_id = "test_ad_group_id"
        mock_args.image_asset_id = "test_image_asset_id"
        mock_argument_parser.return_value.parse_args.return_value = mock_args

        # Mock GoogleAdsClient.load_from_storage to prevent it from running
        mock_google_ads_client.load_from_storage.return_value = self.mock_client

        # Call the script's entry point, which should trigger argument parsing
        # We need to mock `main` itself to check how it's called by the script's own `if __name__ == "__main__":` block
        with mock.patch("examples.misc.add_ad_group_image_asset.main") as mock_main:
            # This simulates running the script from the command line
            # The actual add_ad_group_image_asset.py needs to have the standard
            # if __name__ == "__main__": block that calls main with parsed args.
            # We need to trigger that part of the script.
            # A simple way is to import it again or use runpy.
            import importlib
            import sys
            # To ensure the if __name__ == "__main__": block runs, we can temporarily
            # set the __name__ attribute of the module and then reload it.
            # However, a more straightforward way for testing is to directly call
            # the function that would be invoked by the script's entry point,
            # assuming it's structured to allow this. If the script directly calls
            # main() after parsing args, we can simulate that.

            # For this test, we'll assume the script calls main() after parsing.
            # We need to ensure that the `if __name__ == "__main__":` block in
            # add_ad_group_image_asset.py gets executed.
            # One way to do this is to use runpy.run_module

            # Let's refine this. The goal is to check if add_ad_group_image_asset.main
            # is called with arguments from the parser.
            # The script add_ad_group_image_asset.py itself will call its own main().
            # We need to ensure our mocks are in place when that happens.

            # Simulate command line execution context
            # Store original sys.argv
            original_argv = sys.argv
            # Set up mocked command line arguments
            sys.argv = [
                "add_ad_group_image_asset.py",
                "-c", mock_args.customer_id,
                "-a", mock_args.ad_group_id,
                "-i", mock_args.image_asset_id,
            ]

            # Execute the main part of the script.
            # This relies on add_ad_group_image_asset.py having a block like:
            # if __name__ == "__main__":
            #   parser = argparse.ArgumentParser(...)
            #   args = parser.parse_args()
            #   googleads_client = GoogleAdsClient.load_from_storage()
            #   main(googleads_client, args.customer_id, args.ad_group_id, args.image_asset_id)

            # To test this, we need to ensure that when the script is run,
            # our mocked ArgumentParser is used.
            # The @mock.patch for ArgumentParser should handle this.
            # We also need to ensure our mocked GoogleAdsClient is used.

            # The most direct way to test the script's argument parsing and main invocation
            # is to use runpy.run_module, which executes a module as if it were run from the CLI.
            import runpy
            with mock.patch.object(add_ad_group_image_asset, "main") as mock_script_main:
                 runpy.run_module("examples.misc.add_ad_group_image_asset", run_name="__main__")


            # Assert that our mock_main (inside the script) was called with the correct arguments
            mock_script_main.assert_called_once_with(
                self.mock_client, # This comes from mock_google_ads_client
                mock_args.customer_id,
                mock_args.ad_group_id,
                mock_args.image_asset_id,
            )
            # Restore original sys.argv
            sys.argv = original_argv


if __name__ == "__main__":
    unittest.main()
