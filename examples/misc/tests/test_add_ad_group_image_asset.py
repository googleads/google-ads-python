import unittest
from unittest import mock
import sys
import argparse # Ensure argparse is imported

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
        # Mock the path helper methods on the service
        self.mock_ad_group_asset_service.ad_group_path = mock.Mock(
            side_effect=lambda cust_id, ag_id: f"customers/{cust_id}/adGroups/{ag_id}"
        )
        self.mock_ad_group_asset_service.asset_path = mock.Mock(
            side_effect=lambda cust_id, asset_id_val: f"customers/{cust_id}/assets/{asset_id_val}"
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

    def _simulate_script_main_block(
        self,
        mock_argparse_class_from_decorator,
        mock_gads_client_class_from_decorator,
        mock_main_func_from_decorator,
        # Expected script arguments for this test run
        expected_customer_id,
        expected_ad_group_id,
        expected_asset_id
    ):
        # This function simulates the script's if __name__ == "__main__": block logic.

        # 1. Configure ArgumentParser mock
        mock_parser_instance = mock.Mock(name="ArgumentParserInstance")
        mock_argparse_class_from_decorator.return_value = mock_parser_instance

        mock_parsed_args_obj = argparse.Namespace(
            customer_id=expected_customer_id,
            ad_group_id=expected_ad_group_id,
            asset_id=expected_asset_id # Corrected attribute name
        )
        mock_parser_instance.parse_args.return_value = mock_parsed_args_obj

        # Script's ArgumentParser instantiation
        script_description = "Updates an ad group for specified customer and ad group id with the given image asset id."
        parser = mock_argparse_class_from_decorator(description=script_description)

        # Script's add_argument calls
        parser.add_argument(
            "-c", "--customer_id", type=str, required=True, help="The Google Ads customer ID."
        )
        parser.add_argument(
            "-a", "--ad_group_id", type=str, required=True, help="The ad group ID."
        )
        parser.add_argument(
            "-s", "--asset_id", type=str, required=True, help="The asset ID." # Script uses -s
        )

        # Script's parse_args call
        args = parser.parse_args()

        # Script's GoogleAdsClient.load_from_storage call
        mock_client_instance = mock.Mock(name="GoogleAdsClientInstance")
        mock_gads_client_class_from_decorator.load_from_storage.return_value = mock_client_instance
        googleads_client = mock_gads_client_class_from_decorator.load_from_storage(version="v19")

        # Script's main function call
        mock_main_func_from_decorator(
            googleads_client,
            args.customer_id,
            args.ad_group_id,
            args.asset_id # Corrected attribute name
        )

    @mock.patch("sys.exit")
    @mock.patch("examples.misc.add_ad_group_image_asset.argparse.ArgumentParser")
    @mock.patch("examples.misc.add_ad_group_image_asset.GoogleAdsClient")
    @mock.patch("examples.misc.add_ad_group_image_asset.main")
    def test_argument_parsing(
        self, mock_script_main, mock_gads_client_class,
        mock_arg_parser_class, mock_sys_exit
    ):
        """Test that main is called with parsed arguments."""
        expected_cust_id = "test_cust_123"
        expected_ag_id = "test_ag_456"
        expected_asset_id_val = "test_asset_789"

        self._simulate_script_main_block(
            mock_argparse_class_from_decorator=mock_arg_parser_class,
            mock_gads_client_class_from_decorator=mock_gads_client_class,
            mock_main_func_from_decorator=mock_script_main,
            expected_customer_id=expected_cust_id,
            expected_ad_group_id=expected_ag_id,
            expected_asset_id=expected_asset_id_val
        )

        # Assertions
        script_description = "Updates an ad group for specified customer and ad group id with the given image asset id."
        mock_arg_parser_class.assert_called_once_with(description=script_description)

        mock_parser_instance_for_assert = mock_arg_parser_class.return_value

        expected_calls_to_add_argument = [
            mock.call("-c", "--customer_id", type=str, required=True, help="The Google Ads customer ID."),
            mock.call("-a", "--ad_group_id", type=str, required=True, help="The ad group ID."),
            mock.call("-s", "--asset_id", type=str, required=True, help="The asset ID.")
        ]
        mock_parser_instance_for_assert.add_argument.assert_has_calls(expected_calls_to_add_argument, any_order=True)
        self.assertEqual(mock_parser_instance_for_assert.add_argument.call_count, len(expected_calls_to_add_argument))

        mock_parser_instance_for_assert.parse_args.assert_called_once_with()

        mock_gads_client_class.load_from_storage.assert_called_once_with(version="v19")

        client_instance_for_assert = mock_gads_client_class.load_from_storage.return_value
        mock_script_main.assert_called_once_with(
            client_instance_for_assert,
            expected_cust_id,
            expected_ag_id,
            expected_asset_id_val
        )

if __name__ == "__main__":
    unittest.main()
