import pytest
from unittest.mock import MagicMock, patch, call
import sys

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.v19.services.types.asset_service import AssetOperation
from google.ads.googleads.v19.services.types.customer_asset_service import CustomerAssetOperation
from google.ads.googleads.v19.enums.types.asset_field_type import AssetFieldTypeEnum

from examples.assets.add_hotel_callout import (
    add_hotel_callout_assets,
    link_asset_to_account,
    main as add_hotel_callout_main,
)
from google.ads.googleads.v19.resources.types.asset import Asset
from google.ads.googleads.v19.common.types.asset_types import HotelCalloutAsset
from google.ads.googleads.v19.resources.types.customer_asset import CustomerAsset

# Define constants for testing
CUSTOMER_ID = "1234567890"
LANGUAGE_CODE = "en"
MOCK_ASSET_RESOURCE_NAME_1 = f"customers/{CUSTOMER_ID}/assets/1"
MOCK_ASSET_RESOURCE_NAME_2 = f"customers/{CUSTOMER_ID}/assets/2"
MOCK_ASSET_RESOURCE_NAMES = [
    MOCK_ASSET_RESOURCE_NAME_1,
    MOCK_ASSET_RESOURCE_NAME_2,
]

@pytest.fixture
def mock_google_ads_client():
    """Provides a mock GoogleAdsClient."""
    mock_client = MagicMock(spec=GoogleAdsClient)
    mock_client.get_service = MagicMock()
    mock_client.get_type = MagicMock()
    mock_client.enums = MagicMock()
    # Mock get_service
    mock_asset_service = MagicMock()
    mock_customer_asset_service = MagicMock()
    mock_client.get_service.side_effect = lambda service_name: {
        "AssetService": mock_asset_service,
        "CustomerAssetService": mock_customer_asset_service,
    }.get(service_name)

    # Mock get_type
    def get_type_side_effect(type_name, version=None):
        if type_name == "AssetOperation":
            return AssetOperation
        elif type_name == "CustomerAssetOperation":
            return CustomerAssetOperation
        elif type_name == "Asset":
            return Asset
        elif type_name == "HotelCalloutAsset":
            return HotelCalloutAsset
        elif type_name == "CustomerAsset":
            return CustomerAsset
        raise ValueError(f"Unknown type: {type_name}")
    mock_client.get_type.side_effect = get_type_side_effect

    # Mock enums
    mock_client.enums.AssetFieldTypeEnum = AssetFieldTypeEnum
    return mock_client

# Test for add_hotel_callout_assets function
def test_add_hotel_callout_assets(mock_google_ads_client):
    """Tests the add_hotel_callout_assets function."""
    mock_asset_service = mock_google_ads_client.get_service("AssetService")
    # Mock the response from mutate_assets
    mock_asset_service.mutate_assets.return_value.results = [
        MagicMock(resource_name=MOCK_ASSET_RESOURCE_NAME_1),
        MagicMock(resource_name=MOCK_ASSET_RESOURCE_NAME_2),
    ]

    # Expected texts for hotel callout assets
    hotel_callout_asset_texts = [
        "Activities",
        "Facilities",
    ]

    asset_resource_names = add_hotel_callout_assets(
        mock_google_ads_client, CUSTOMER_ID, LANGUAGE_CODE
    )

    assert asset_resource_names == MOCK_ASSET_RESOURCE_NAMES
    mock_asset_service.mutate_assets.assert_called_once()
    args, _ = mock_asset_service.mutate_assets.call_args
    assert args[0] == CUSTOMER_ID
    operations = args[1] # Operations is a list
    assert len(operations) == 2

    for i, operation in enumerate(operations):
        assert isinstance(operation, AssetOperation)
        assert operation.create is not None
        created_asset = operation.create
        assert isinstance(created_asset, Asset)
        assert created_asset.hotel_callout_asset is not None
        hotel_callout = created_asset.hotel_callout_asset
        assert isinstance(hotel_callout, HotelCalloutAsset)
        assert hotel_callout.text == hotel_callout_asset_texts[i]
        assert hotel_callout.language_code == LANGUAGE_CODE


# Test for link_asset_to_account function (for hotel callouts)
def test_link_asset_to_account_hotel_callout(mock_google_ads_client):
    """Tests the link_asset_to_account function for hotel callouts."""
    mock_customer_asset_service = mock_google_ads_client.get_service(
        "CustomerAssetService"
    )
    # Mock the response from mutate_customer_assets
    # We expect two results, one for each asset linked.
    mock_customer_asset_service.mutate_customer_assets.return_value.results = [
        MagicMock(
            resource_name=f"customers/{CUSTOMER_ID}/customerAssets/1_HOTEL_CALLOUT"
        ),
        MagicMock(
            resource_name=f"customers/{CUSTOMER_ID}/customerAssets/2_HOTEL_CALLOUT"
        ),
    ]

    link_asset_to_account(
        mock_google_ads_client, CUSTOMER_ID, MOCK_ASSET_RESOURCE_NAMES
    )

    mock_customer_asset_service.mutate_customer_assets.assert_called_once()
    args, _ = mock_customer_asset_service.mutate_customer_assets.call_args
    assert args[0] == CUSTOMER_ID
    operations = args[1]  # Operations is a list
    assert len(operations) == len(MOCK_ASSET_RESOURCE_NAMES)

    for i, operation in enumerate(operations):
        assert isinstance(operation, CustomerAssetOperation)
        assert operation.create is not None
        created_customer_asset = operation.create
        assert isinstance(created_customer_asset, CustomerAsset)
        assert (
            created_customer_asset.asset == MOCK_ASSET_RESOURCE_NAMES[i]
        )
        assert (
            created_customer_asset.field_type
            == AssetFieldTypeEnum.AssetFieldType.HOTEL_CALLOUT
        )


# Tests for main function and argument parsing
@patch.object(
    sys,
    "argv",
    [
        "examples/assets/add_hotel_callout.py",
        f"--customer_id={CUSTOMER_ID}",
        f"--language_code={LANGUAGE_CODE}",
    ],
)
@patch("examples.assets.add_hotel_callout.GoogleAdsClient.load_from_storage")
@patch("examples.assets.add_hotel_callout.add_hotel_callout_assets")
@patch("examples.assets.add_hotel_callout.link_asset_to_account")
def test_main_function_and_args(
    mock_link_asset_to_account,
    mock_add_hotel_callout_assets,
    mock_load_from_storage,
    mock_google_ads_client,  # Fixture for client
    capsys,
):
    """Tests the main function and argument parsing."""
    mock_load_from_storage.return_value = mock_google_ads_client
    mock_add_hotel_callout_assets.return_value = MOCK_ASSET_RESOURCE_NAMES

    add_hotel_callout_main()

    mock_load_from_storage.assert_called_once_with(version="v19")
    mock_add_hotel_callout_assets.assert_called_once_with(
        mock_google_ads_client, CUSTOMER_ID, LANGUAGE_CODE
    )
    mock_link_asset_to_account.assert_called_once_with(
        mock_google_ads_client, CUSTOMER_ID, MOCK_ASSET_RESOURCE_NAMES
    )

    # Check stdout for printed messages
    captured = capsys.readouterr()
    for resource_name in MOCK_ASSET_RESOURCE_NAMES:
        assert (
            f"Created hotel callout asset with resource name '{resource_name}'"
            in captured.out
        )
    assert (
        f"Linked {len(MOCK_ASSET_RESOURCE_NAMES)} hotel callout assets "
        f"to customer '{CUSTOMER_ID}'." in captured.out
    )
