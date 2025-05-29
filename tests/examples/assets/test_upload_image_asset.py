import pytest
from unittest.mock import MagicMock, patch
import sys

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.v19.services.types.asset_service import AssetOperation
from google.ads.googleads.v19.resources.types.asset import Asset
from google.ads.googleads.v19.common.types.asset_types import ImageAsset, ImageDimension
from google.ads.googleads.v19.enums.types.asset_type import AssetTypeEnum
from google.ads.googleads.v19.enums.types.mime_type import MimeTypeEnum

from examples.assets.upload_image_asset import main as upload_image_asset_main
# The example_helpers module is in examples/utils/
# We need to adjust the path for the import if tests are run from the root directory
# or add examples to sys.path if necessary. For now, assume it can be found.
from examples.utils import example_helpers


# Define constants for testing
CUSTOMER_ID = "1234567890"
IMAGE_URL = "https://gaagl.page.link/Eit5"
MOCK_IMAGE_BYTES = b"test_image_data_for_upload_asset"
EXPECTED_ASSET_NAME = "Marketing Image"

@pytest.fixture
def mock_google_ads_client():
    """Provides a mock GoogleAdsClient."""
    mock_client = MagicMock(spec=GoogleAdsClient)
    mock_client.get_service = MagicMock()
    mock_client.get_type = MagicMock()
    mock_client.enums = MagicMock()
    return mock_client

# Test for main function of upload_image_asset.py
@patch.object(
    sys,
    "argv",
    [
        "examples/assets/upload_image_asset.py",
        f"--customer_id={CUSTOMER_ID}",
    ],
)
@patch("examples.assets.upload_image_asset.GoogleAdsClient.load_from_storage")
@patch("examples.utils.example_helpers.get_image_bytes_from_url")
def test_main_upload_image_asset(
    mock_get_image_bytes,
    mock_load_from_storage,
    mock_google_ads_client,  # Fixture
    capsys,
):
    """Tests the main function of upload_image_asset.py."""
    mock_load_from_storage.return_value = mock_google_ads_client
    mock_get_image_bytes.return_value = MOCK_IMAGE_BYTES

    # Configure mock client services and types
    mock_asset_service = MagicMock()
    mock_google_ads_client.get_service.return_value = mock_asset_service

    def get_type_side_effect(type_name, version=None):
        if type_name == "AssetOperation":
            return AssetOperation
        elif type_name == "Asset":
            return Asset
        elif type_name == "ImageAsset":
            return ImageAsset
        elif type_name == "ImageDimension":
            return ImageDimension
        raise ValueError(f"Unknown type: {type_name}")

    mock_google_ads_client.get_type.side_effect = get_type_side_effect
    mock_google_ads_client.enums.AssetTypeEnum = AssetTypeEnum
    mock_google_ads_client.enums.MimeTypeEnum = MimeTypeEnum

    # Mock the response from mutate_assets
    mock_asset_service.mutate_assets.return_value.results = [
        MagicMock(resource_name=f"customers/{CUSTOMER_ID}/assets/12345")
    ]

    upload_image_asset_main()

    # Verify GoogleAdsClient.load_from_storage was called correctly
    mock_load_from_storage.assert_called_once_with(version="v19")

    # Verify get_image_bytes_from_url was called correctly
    mock_get_image_bytes.assert_called_once_with(IMAGE_URL)

    # Verify AssetService.mutate_assets was called correctly
    mock_google_ads_client.get_service.assert_called_once_with("AssetService")
    mock_asset_service.mutate_assets.assert_called_once()
    args, _ = mock_asset_service.mutate_assets.call_args
    assert args[0] == CUSTOMER_ID  # customer_id
    operations = args[1]  # operations list
    assert len(operations) == 1
    operation = operations[0]
    assert isinstance(operation, AssetOperation)
    assert operation.create is not None
    created_asset = operation.create
    assert isinstance(created_asset, Asset)

    # Verify the structure of the Asset
    assert created_asset.type_ == AssetTypeEnum.AssetType.IMAGE
    assert created_asset.name == EXPECTED_ASSET_NAME
    assert created_asset.image_asset is not None

    image_asset_data = created_asset.image_asset
    assert isinstance(image_asset_data, ImageAsset)
    assert image_asset_data.data == MOCK_IMAGE_BYTES
    assert image_asset_data.file_size == len(MOCK_IMAGE_BYTES)
    assert image_asset_data.mime_type == MimeTypeEnum.MimeType.IMAGE_JPEG
    assert image_asset_data.full_size is not None
    assert isinstance(image_asset_data.full_size, ImageDimension)
    assert image_asset_data.full_size.height_pixels == 315
    assert image_asset_data.full_size.width_pixels == 600
    assert image_asset_data.full_size.url == IMAGE_URL

    # Verify stdout messages (optional, but good for completeness)
    captured = capsys.readouterr()
    assert (
        f"Image asset with resource name 'customers/{CUSTOMER_ID}/assets/12345' was created."
        in captured.out
    )
