import unittest
from unittest import mock

from google.ads.googleads.errors import GoogleAdsException
from .test_utils import create_mock_google_ads_exception

# Assuming the script to be tested is in the parent directory.
# Adjust the import path as necessary if the script is located elsewhere.
from examples.misc import add_ad_group_image_asset


class TestAddAdGroupImageAsset(unittest.TestCase):
    """Tests for the add_ad_group_image_asset script."""

    @mock.patch("examples.misc.add_ad_group_image_asset.GoogleAdsClient")
    def setUp(self, mock_google_ads_client_class): # Renamed for clarity
        """Set up mock objects for testing."""
        self.mock_client = mock_google_ads_client_class.load_from_storage.return_value
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
        # Create a mock result object that would be in the results list
        mock_result = mock.Mock()
        mock_result.resource_name = "test_resource_name"
        self.mock_mutate_response.results = [mock_result] # Make .results an iterable
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
        # Mock objects needed for GoogleAdsException instantiation
        mock_error = mock.Mock()
        # It's common for error details to be complex; mocking specific attributes
        # that the code under test might access.
        # For example, if the code accesses ex.failure.errors[0].error_code.name
        mock_error_detail = mock.Mock()
        mock_error_detail.error_code.name = "TEST_ERROR" # Example error code name
        mock_error_detail.message = "Test failure message"
        # If the error object has a location, mock that too
        mock_error_detail.location.field_path_elements = []


        mock_failure = self.mock_client.get_type("GoogleAdsFailure")
        mock_failure.errors = [mock_error_detail] # Assign the detailed mock error

        mock_call = mock.Mock()
        mock_request_id = "test_request_id"

        self.mock_ad_group_asset_service.mutate_ad_group_assets.side_effect = (
            GoogleAdsException(mock_error, mock_call, mock_request_id, mock_failure)
        )

        with self.assertRaises(GoogleAdsException):
            add_ad_group_image_asset.main(
                self.mock_client, customer_id, ad_group_id, image_asset_id
            )

    @mock.patch("sys.exit") # Added to prevent SystemExit
    @mock.patch("examples.misc.add_ad_group_image_asset.argparse.ArgumentParser")
    @mock.patch("examples.misc.add_ad_group_image_asset.GoogleAdsClient")
    @mock.patch("examples.misc.add_ad_group_image_asset.main") # Mock the main function in the script
    def test_argument_parsing(
        self, mock_script_main_function, mock_google_ads_client_class, mock_argument_parser_class, mock_sys_exit # Added mock_sys_exit
    ):
        """Test that main is called with parsed arguments."""
        # Set up the mock argument parser
        mock_args = mock.Mock()
        mock_args.customer_id = "test_customer_id"
        mock_args.ad_group_id = "test_ad_group_id"
        mock_args.image_asset_id = "test_image_asset_id"
        mock_argument_parser_class.return_value.parse_args.return_value = mock_args

        # Mock GoogleAdsClient.load_from_storage to prevent it from running
        # and to return the client instance we already have in self.mock_client
        mock_google_ads_client_class.load_from_storage.return_value = self.mock_client

        # Store original sys.argv
        original_argv = sys.argv
        # Set up mocked command line arguments
        sys.argv = [
            "add_ad_group_image_asset.py",
            "-c", mock_args.customer_id,
            "-a", mock_args.ad_group_id,
            "-i", mock_args.image_asset_id,
        ]

        # Execute the main part of the script using runpy
        # This will execute the if __name__ == "__main__": block
        import runpy
        runpy.run_module("examples.misc.add_ad_group_image_asset", run_name="__main__")

        # Assert that the script's main function (which is now mocked by mock_script_main_function)
        # was called with the correct arguments from the parsed command line args.
        mock_script_main_function.assert_called_once_with(
            self.mock_client, # This should be the client from GoogleAdsClient.load_from_storage
            mock_args.customer_id,
            mock_args.ad_group_id,
            mock_args.image_asset_id,
        )
        # Restore original sys.argv
        sys.argv = original_argv
        # Assert that sys.exit was not called if the script ran "successfully"
        # (i.e., if our mocks prevented any actual exceptions that would lead to sys.exit)
        # Depending on the script's structure, sys.exit might be called even on success.
        # If the script is expected to call sys.exit(0) on success, this assertion might need adjustment.
        # Given the context of this test (checking if main is called correctly),
        # we mostly care that it doesn't exit with an error code due to our test setup.
        # The mock_sys_exit will absorb any sys.exit calls.


if __name__ == "__main__":
    unittest.main()
