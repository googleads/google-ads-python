import unittest
from unittest.mock import patch, MagicMock, ANY
import sys
import os

# Adjust sys.path to allow import of the script under test and its utils
_PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from examples.misc import upload_image_asset

class TestUploadImageAsset(unittest.TestCase):

    # Patch the hardcoded URL in the script for predictable get_image_bytes_from_url call
    @patch('examples.misc.upload_image_asset.get_image_bytes_from_url')
    @patch('examples.misc.upload_image_asset.GoogleAdsClient.load_from_storage')
    @patch('builtins.print')
    def test_main_upload_logic(self, mock_print, mock_load_from_storage, mock_get_image_bytes):
        # --- Setup Mocks ---
        mock_ads_client = MagicMock()
        mock_load_from_storage.return_value = mock_ads_client
        
        mock_asset_service = mock_ads_client.get_service.return_value
        
        # Mock the image fetching utility
        mock_image_bytes = b"mock_image_data_bytes_here_123"
        mock_get_image_bytes.return_value = mock_image_bytes
        
        # Mock the response from mutate_assets
        mock_mutate_response = MagicMock()
        mock_asset_resource_name = "customers/1234567890/assets/9876543210"
        mock_mutate_response.results = [MagicMock(resource_name=mock_asset_resource_name)]
        mock_asset_service.mutate_assets.return_value = mock_mutate_response

        # --- Test Parameters (customer_id is the only arg to script's main) ---
        customer_id = "1234567890"

        # --- Script's Hardcoded Values ---
        script_image_url = "https://gaagl.page.link/Eit5"
        script_asset_name = "Marketing Image"
        script_image_width = 600
        script_image_height = 315

        # --- Mock Enums needed by the script ---
        mock_ads_client.enums.AssetTypeEnum.IMAGE = "IMAGE_ENUM_VALUE" 
        # Script uses client.enums.MimeTypeEnum.IMAGE_JPEG directly
        mock_ads_client.enums.MimeTypeEnum.IMAGE_JPEG = "MIME_IMAGE_JPEG_ENUM_VALUE"
        
        # --- Call the main function of the script ---
        # Script's main: main(client, customer_id)
        upload_image_asset.main(
            mock_ads_client,
            customer_id
        )

        # --- Assertions ---
        # Assert that get_image_bytes_from_url was called with the script's hardcoded URL
        mock_get_image_bytes.assert_called_once_with(script_image_url)
        mock_ads_client.get_service.assert_called_once_with("AssetService")
        
        # Verify mutate_assets call
        mock_asset_service.mutate_assets.assert_called_once()
        # Check arguments using call_args.kwargs as script uses named arguments
        args, kwargs = mock_asset_service.mutate_assets.call_args
        
        self.assertEqual(kwargs['customer_id'], customer_id)
        
        operations = kwargs['operations']
        self.assertEqual(len(operations), 1)
        operation = operations[0]

        # Verify the created asset details against script's hardcoded values
        created_asset = operation.create
        self.assertEqual(created_asset.type_, mock_ads_client.enums.AssetTypeEnum.IMAGE)
        self.assertEqual(created_asset.name, script_asset_name)
        
        # Verify image_asset details
        image_asset = created_asset.image_asset
        self.assertEqual(image_asset.data, mock_image_bytes)
        self.assertEqual(image_asset.file_size, len(mock_image_bytes))
        self.assertEqual(image_asset.mime_type, mock_ads_client.enums.MimeTypeEnum.IMAGE_JPEG)
        
        # Check full_size attributes
        self.assertEqual(image_asset.full_size.url, script_image_url)
        self.assertEqual(image_asset.full_size.width_pixels, script_image_width)
        self.assertEqual(image_asset.full_size.height_pixels, script_image_height)

        # Verify print output
        mock_print.assert_any_call("Uploaded file(s):")
        mock_print.assert_any_call(f"\tResource name: {mock_asset_resource_name}")

if __name__ == "__main__":
    unittest.main()
