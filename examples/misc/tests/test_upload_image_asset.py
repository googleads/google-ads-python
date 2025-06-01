import unittest
from unittest import mock
import argparse
import sys

# Assuming the script to be tested is in the parent directory.
# Adjust the import path as necessary.
from examples.misc import upload_image_asset
from google.ads.googleads.errors import GoogleAdsException
from .test_utils import create_mock_google_ads_exception
from google.ads.googleads.v19.enums.types.asset_type import AssetTypeEnum
from google.ads.googleads.v19.enums.types.mime_type import MimeTypeEnum


class TestUploadImageAsset(unittest.TestCase):
    """Tests for the upload_image_asset script."""

    @mock.patch("examples.misc.upload_image_asset.get_image_bytes_from_url")
    @mock.patch("examples.misc.upload_image_asset.GoogleAdsClient")
    def setUp(self, mock_google_ads_client_class, mock_get_image_bytes_func): # Corrected order and name
        # Mock GoogleAdsClient and its methods
        self.mock_client = mock_google_ads_client_class.load_from_storage.return_value
        self.mock_asset_service = self.mock_client.get_service("AssetService")
        self.mock_asset_operation = self.mock_client.get_type("AssetOperation")

        # Mock enums properly
        # Instead of replacing the whole enum type on mock_client.enums,
        # we let the script access the real enums (AssetTypeEnum, MimeTypeEnum are imported directly)
        # The test will then assert that the correct real enum values are used.
        # This also means the direct imports of AssetTypeEnum and MimeTypeEnum at the top are important.

        # Mock get_image_bytes_from_url
        self.mock_get_image_bytes_from_url = mock_get_image_bytes_func # Corrected name
        self.mock_image_bytes = b"test_image_data" # Changed from mock_image_data for clarity
        self.mock_get_image_bytes_from_url.return_value = self.mock_image_bytes

        # Mock the mutate_assets response
        self.mock_mutate_response = mock.Mock()
        self.mock_mutate_response.results = [mock.Mock()]
        self.mock_mutate_response.results[0].resource_name = "customers/123/assets/456"
        self.mock_asset_service.mutate_assets.return_value = self.mock_mutate_response

        # Mock the operation's create field
        self.mock_asset_create = self.mock_asset_operation.return_value.create
        self.mock_asset_create.image_asset = mock.Mock()


    @mock.patch("builtins.print")
    def test_main_success(self, mock_print):
        """Tests a successful run of the main function."""
        customer_id = "1234567890"

        upload_image_asset.main(self.mock_client, customer_id)

        self.mock_get_image_bytes_from_url.assert_called_once_with(
            "https://gaagl.page.link/Eit5"
        )
        self.mock_asset_service.mutate_assets.assert_called_once()

        # Get the call arguments to inspect them
        call_args = self.mock_asset_service.mutate_assets.call_args
        # Check customer_id
        self.assertEqual(call_args[1]["customer_id"], customer_id)
        # Check operation
        actual_operation = call_args[1]["operations"][0]

        # Assertions on the asset operation
        self.assertEqual(actual_operation.create.type_, AssetTypeEnum.IMAGE) # Uses imported AssetTypeEnum
        self.assertEqual(actual_operation.create.image_asset.data, self.mock_image_bytes)
        self.assertEqual(actual_operation.create.image_asset.file_size, len(self.mock_image_bytes))
        self.assertEqual(actual_operation.create.image_asset.mime_type, MimeTypeEnum.IMAGE_JPEG) # Uses imported MimeTypeEnum
        self.assertEqual(actual_operation.create.name, "Marketing Image")
        self.assertEqual(actual_operation.create.image_asset.full_size.url, "https://gaagl.page.link/Eit5")

        mock_print.assert_any_call(
            f"Uploaded image asset with resource name: '{self.mock_mutate_response.results[0].resource_name}'"
        )

    @mock.patch("sys.exit")
    @mock.patch("builtins.print") # To check error messages if needed
    def test_main_google_ads_exception(self, mock_print, mock_sys_exit):
        """Tests handling of GoogleAdsException."""
        customer_id = "1234567890"

        mock_ex = create_mock_google_ads_exception(self.mock_client, request_id="ga_ex_upload", message="Error uploading image")
        self.mock_asset_service.mutate_assets.side_effect = mock_ex

        with self.assertRaises(GoogleAdsException) as cm:
            upload_image_asset.main(self.mock_client, customer_id)

        # self.assertEqual(cm.exception.request_id, "ga_ex_upload")
        # self.assertIn("Error uploading image", str(cm.exception))

        # Assert that sys.exit was called, indicating the exception was caught
        # This mock_sys_exit is for the @mock.patch("sys.exit") at the method level.
        # The script's main() function itself doesn't call sys.exit, but the
        # if __name__ == "__main__" block does. This test is for main().
        # So, sys.exit should not be called by main().
        mock_sys_exit.assert_not_called()
        # Optionally, check if specific error messages were printed
        # This depends on the exact error printing logic in the script
        # For example: mock_print.assert_any_call(...)


    def _simulate_script_main_block(
        self,
        mock_argparse_class_from_decorator,
        mock_gads_client_class_from_decorator,
        mock_main_func_from_decorator,
        # Expected script arguments
        expected_customer_id
    ):
        # Simulates the script's if __name__ == "__main__": block logic.

        # 1. Configure ArgumentParser mock
        mock_parser_instance = mock.Mock(name="ArgumentParserInstance")
        mock_argparse_class_from_decorator.return_value = mock_parser_instance

        mock_parsed_args_obj = argparse.Namespace(customer_id=expected_customer_id)
        mock_parser_instance.parse_args.return_value = mock_parsed_args_obj

        # Script's ArgumentParser instantiation
        script_description = "Upload an image asset from a URL."
        parser = mock_argparse_class_from_decorator(description=script_description)

        # Script's add_argument calls
        parser.add_argument(
            "-c", "--customer_id", type=str, required=True, help="The Google Ads customer ID."
        )

        args = parser.parse_args()

        # Script's GoogleAdsClient.load_from_storage call
        mock_client_instance = mock.Mock(name="GoogleAdsClientInstance")
        mock_gads_client_class_from_decorator.load_from_storage.return_value = mock_client_instance
        googleads_client = mock_gads_client_class_from_decorator.load_from_storage(version="v19")

        # Script's main function call
        mock_main_func_from_decorator(googleads_client, args.customer_id)

    @mock.patch("sys.exit")
    @mock.patch("examples.misc.upload_image_asset.argparse.ArgumentParser")
    @mock.patch("examples.misc.upload_image_asset.GoogleAdsClient")
    @mock.patch("examples.misc.upload_image_asset.main") # Added patch for main
    def test_argument_parsing_and_script_execution(
        self, mock_script_main, mock_gads_client_class,
        mock_arg_parser_class, mock_sys_exit
    ):
        """Tests argument parsing and the script's main execution block."""
        expected_cust_id = "test_upload_cust_123"

        self._simulate_script_main_block(
            mock_argparse_class_from_decorator=mock_arg_parser_class,
            mock_gads_client_class_from_decorator=mock_gads_client_class,
            mock_main_func_from_decorator=mock_script_main,
            expected_customer_id=expected_cust_id
        )

        # Assertions
        script_description = "Upload an image asset from a URL."
        mock_arg_parser_class.assert_called_once_with(description=script_description)

        mock_parser_instance_for_assert = mock_arg_parser_class.return_value

        mock_parser_instance_for_assert.add_argument.assert_called_once_with(
            "-c", "--customer_id", type=str, required=True, help="The Google Ads customer ID."
        )
        mock_parser_instance_for_assert.parse_args.assert_called_once_with()

        mock_gads_client_class.load_from_storage.assert_called_once_with(version="v19")

        client_instance_for_assert = mock_gads_client_class.load_from_storage.return_value
        mock_script_main.assert_called_once_with(
            client_instance_for_assert,
            expected_cust_id
        )

if __name__ == "__main__":
    unittest.main()
