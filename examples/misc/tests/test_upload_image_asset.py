import unittest
from unittest import mock
import argparse
import sys

# Assuming the script to be tested is in the parent directory.
# Adjust the import path as necessary.
from examples.misc import upload_image_asset
from google.ads.googleads.errors import GoogleAdsException
from google.ads.googleads.v19.enums.types.asset_type import AssetTypeEnum
from google.ads.googleads.v19.enums.types.mime_type import MimeTypeEnum


class TestUploadImageAsset(unittest.TestCase):
    """Tests for the upload_image_asset script."""

    @mock.patch("examples.misc.upload_image_asset.GoogleAdsClient")
    @mock.patch("examples.misc.upload_image_asset.get_image_bytes_from_url")
    def setUp(self, mock_get_image_bytes, mock_google_ads_client_class):
        # Mock GoogleAdsClient and its methods
        self.mock_client = mock_google_ads_client_class.load_from_storage.return_value
        self.mock_asset_service = self.mock_client.get_service("AssetService")
        self.mock_asset_operation = self.mock_client.get_type("AssetOperation")

        # Mock enums
        self.mock_client.enums.AssetTypeEnum = AssetTypeEnum
        self.mock_client.enums.MimeTypeEnum = MimeTypeEnum

        # Mock get_image_bytes_from_url
        self.mock_get_image_bytes_from_url = mock_get_image_bytes
        self.mock_image_bytes = b"mock_image_data"
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
            upload_image_asset.IMAGE_URL
        )
        self.mock_asset_service.mutate_assets.assert_called_once()

        # Get the call arguments to inspect them
        call_args = self.mock_asset_service.mutate_assets.call_args
        # Check customer_id
        self.assertEqual(call_args[1]["customer_id"], customer_id)
        # Check operation
        actual_operation = call_args[1]["operations"][0]

        # Assertions on the asset operation
        self.assertEqual(actual_operation.create.type_, AssetTypeEnum.IMAGE)
        self.assertEqual(actual_operation.create.image_asset.data, self.mock_image_bytes)
        self.assertEqual(actual_operation.create.image_asset.file_size, len(self.mock_image_bytes))
        self.assertEqual(actual_operation.create.image_asset.mime_type, MimeTypeEnum.IMAGE_JPEG)
        self.assertEqual(actual_operation.create.name, "Marketing Image")

        mock_print.assert_any_call(
            f"Uploaded image asset with resource name: '{self.mock_mutate_response.results[0].resource_name}'"
        )

    @mock.patch("sys.exit")
    @mock.patch("builtins.print") # To check error messages if needed
    def test_main_google_ads_exception(self, mock_print, mock_sys_exit):
        """Tests handling of GoogleAdsException."""
        customer_id = "1234567890"
        mock_google_ads_exception = GoogleAdsException(None, None, mock.Mock()) # Mock error details

        self.mock_asset_service.mutate_assets.side_effect = mock_google_ads_exception

        upload_image_asset.main(self.mock_client, customer_id)

        # Assert that sys.exit was called, indicating the exception was caught
        mock_sys_exit.assert_called_with(1)
        # Optionally, check if specific error messages were printed
        # This depends on the exact error printing logic in the script
        # For example: mock_print.assert_any_call(...)


    @mock.patch("examples.misc.upload_image_asset.argparse.ArgumentParser")
    @mock.patch("examples.misc.upload_image_asset.GoogleAdsClient")
    def test_argument_parsing_and_script_execution(
        self, mock_google_ads_client_class_in_script, mock_argument_parser_class
    ):
        """Tests argument parsing and the script's main execution block."""
        mock_parser_instance = mock.Mock()
        mock_args = argparse.Namespace(customer_id="test_customer_id_cli")
        mock_parser_instance.parse_args.return_value = mock_args
        mock_argument_parser_class.return_value = mock_parser_instance

        mock_script_client_instance = mock_google_ads_client_class_in_script.load_from_storage.return_value

        original_argv = sys.argv
        sys.argv = ["upload_image_asset.py", "-c", "test_customer_id_cli"]

        import runpy
        with mock.patch.object(upload_image_asset, "main") as mock_script_main_function:
            runpy.run_module("examples.misc.upload_image_asset", run_name="__main__")

        mock_argument_parser_class.assert_called_once_with(
            description="Uploads an image asset from a URL."
        )
        mock_parser_instance.add_argument.assert_called_once_with(
            "-c",
            "--customer_id",
            type=str,
            required=True,
            help="The Google Ads customer ID.",
        )
        mock_parser_instance.parse_args.assert_called_once()

        mock_google_ads_client_class_in_script.load_from_storage.assert_called_once_with(
            version="v19" # As specified in the script
        )

        mock_script_main_function.assert_called_once_with(
            mock_script_client_instance, "test_customer_id_cli"
        )

        sys.argv = original_argv


if __name__ == "__main__":
    unittest.main()
