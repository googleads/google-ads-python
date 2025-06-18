import unittest
from unittest.mock import MagicMock, patch

from examples.assets import upload_image_asset


class TestUploadImageAsset(unittest.TestCase):

    @patch("examples.assets.upload_image_asset.get_image_bytes_from_url")
    @patch(
        "examples.assets.upload_image_asset.GoogleAdsClient"
    )  # Mocking where it's used in the module
    def test_main_function_logic(
        self, mock_google_ads_client_constructor, mock_get_image_bytes
    ):
        mock_client_instance = mock_google_ads_client_constructor.return_value
        mock_asset_service = MagicMock()
        mock_client_instance.get_service.return_value = mock_asset_service

        mock_asset_operation = MagicMock()
        mock_client_instance.get_type.return_value = mock_asset_operation
        mock_created_asset = mock_asset_operation.create

        mock_client_instance.enums.AssetTypeEnum.IMAGE = "IMAGE_ASSET_TYPE_ENUM"
        mock_client_instance.enums.MimeTypeEnum.IMAGE_JPEG = (
            "IMAGE_JPEG_MIME_TYPE_ENUM"
        )

        fake_image_bytes = b"fake_image_data_bytes"
        mock_get_image_bytes.return_value = fake_image_bytes

        mock_mutate_asset_response = MagicMock()
        mock_mutate_asset_response.results = [
            MagicMock(resource_name="asset_resource_name_123")
        ]
        mock_asset_service.mutate_assets.return_value = (
            mock_mutate_asset_response
        )

        customer_id = "test_customer_id_123"
        expected_asset_name = "Marketing Image"
        expected_image_url = "https://gaagl.page.link/Eit5"

        upload_image_asset.main(mock_client_instance, customer_id)

        mock_get_image_bytes.assert_called_once_with(expected_image_url)
        mock_client_instance.get_service.assert_called_once_with("AssetService")
        mock_client_instance.get_type.assert_called_once_with("AssetOperation")

        self.assertEqual(mock_created_asset.type_, "IMAGE_ASSET_TYPE_ENUM")
        self.assertEqual(mock_created_asset.name, expected_asset_name)

        image_asset_mock = mock_created_asset.image_asset
        self.assertEqual(image_asset_mock.data, fake_image_bytes)
        self.assertEqual(image_asset_mock.file_size, len(fake_image_bytes))
        self.assertEqual(
            image_asset_mock.mime_type, "IMAGE_JPEG_MIME_TYPE_ENUM"
        )
        self.assertEqual(image_asset_mock.full_size.height_pixels, 315)
        self.assertEqual(image_asset_mock.full_size.width_pixels, 600)
        self.assertEqual(image_asset_mock.full_size.url, expected_image_url)

        mock_asset_service.mutate_assets.assert_called_once_with(
            customer_id=customer_id, operations=[mock_asset_operation]
        )
