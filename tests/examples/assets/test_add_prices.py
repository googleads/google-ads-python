import pytest
from unittest.mock import MagicMock, patch, call
import sys
import uuid

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.v19.services.types.asset_service import AssetOperation
from google.ads.googleads.v19.services.types.customer_asset_service import CustomerAssetOperation
from google.ads.googleads.v19.enums.types.asset_field_type import AssetFieldTypeEnum
from google.ads.googleads.v19.enums.types.price_extension_type import PriceExtensionTypeEnum
from google.ads.googleads.v19.enums.types.price_extension_price_qualifier import PriceExtensionPriceQualifierEnum
from google.ads.googleads.v19.common.types.asset_types import PriceAsset, PriceOffering
from google.ads.googleads.v19.common.types.criteria import Money
from google.ads.googleads.v19.resources.types.asset import Asset
from google.ads.googleads.v19.resources.types.customer_asset import CustomerAsset

from examples.assets.add_prices import (
    create_price_offering,
    create_price_asset,
    add_asset_to_account,
    main as add_prices_main,
)

# Define constants for testing
CUSTOMER_ID = "1234567890"
MOCK_PRICE_ASSET_RESOURCE_NAME = f"customers/{CUSTOMER_ID}/assets/1"
FIXED_UUID = "fixed-uuid-for-prices"
EXPECTED_ASSET_NAME = f"Price Asset #{FIXED_UUID}"

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
        elif type_name == "PriceAsset":
            return PriceAsset
        elif type_name == "PriceOffering":
            return PriceOffering
        elif type_name == "Money":
            return Money
        elif type_name == "CustomerAsset":
            return CustomerAsset
        raise ValueError(f"Unknown type: {type_name}")
    mock_client.get_type.side_effect = get_type_side_effect

    # Mock enums
    mock_client.enums.AssetFieldTypeEnum = AssetFieldTypeEnum
    mock_client.enums.PriceExtensionTypeEnum = PriceExtensionTypeEnum
    mock_client.enums.PriceExtensionPriceQualifierEnum = PriceExtensionPriceQualifierEnum
    return mock_client

# Test for create_price_offering function
def test_create_price_offering_with_mobile_url(mock_google_ads_client):
    """Tests create_price_offering when final_mobile_url is provided."""
    header = "Test Header"
    description = "Test Description"
    final_url = "http://example.com/test"
    final_mobile_url = "http://m.example.com/test"
    price_in_micros = 10000000  # 10 units
    currency_code = "USD"
    unit = "PER_DAY"

    mock_price_offering_type = mock_google_ads_client.get_type("PriceOffering")
    mock_money_type = mock_google_ads_client.get_type("Money")

    price_offering = create_price_offering(
        mock_google_ads_client,
        header,
        description,
        final_url,
        final_mobile_url,
        price_in_micros,
        currency_code,
        unit,
    )

    assert isinstance(price_offering, PriceOffering)
    assert price_offering.header == header
    assert price_offering.description == description
    assert price_offering.final_url == final_url
    assert price_offering.final_mobile_url == final_mobile_url
    assert isinstance(price_offering.price, Money)
    assert price_offering.price.amount_micros == price_in_micros
    assert price_offering.price.currency_code == currency_code
    assert price_offering.unit == unit
    mock_google_ads_client.get_type.assert_any_call("PriceOffering")
    mock_google_ads_client.get_type.assert_any_call("Money")


def test_create_price_offering_without_mobile_url(mock_google_ads_client):
    """Tests create_price_offering when final_mobile_url is None."""
    header = "Test Header No Mobile"
    description = "Test Description No Mobile"
    final_url = "http://example.com/test-no-mobile"
    price_in_micros = 20000000  # 20 units
    currency_code = "EUR"
    unit = "PER_NIGHT"

    mock_price_offering_type = mock_google_ads_client.get_type("PriceOffering")
    mock_money_type = mock_google_ads_client.get_type("Money")

    price_offering = create_price_offering(
        mock_google_ads_client,
        header,
        description,
        final_url,
        None,  # final_mobile_url
        price_in_micros,
        currency_code,
        unit,
    )

    assert isinstance(price_offering, PriceOffering)
    assert price_offering.header == header
    assert price_offering.description == description
    assert price_offering.final_url == final_url
    assert not price_offering.final_mobile_url  # Should be empty or None
    assert isinstance(price_offering.price, Money)
    assert price_offering.price.amount_micros == price_in_micros
    assert price_offering.price.currency_code == currency_code
    assert price_offering.unit == unit
    mock_google_ads_client.get_type.assert_any_call("PriceOffering")
    mock_google_ads_client.get_type.assert_any_call("Money")


# Test for create_price_asset function
@patch("uuid.uuid4", return_value=FIXED_UUID)
@patch("examples.assets.add_prices.create_price_offering")
def test_create_price_asset(
    mock_create_price_offering, mock_uuid, mock_google_ads_client
):
    """Tests the create_price_asset function."""
    mock_asset_service = mock_google_ads_client.get_service("AssetService")
    # Mock the response from mutate_assets
    mock_asset_service.mutate_assets.return_value.results = [
        MagicMock(resource_name=MOCK_PRICE_ASSET_RESOURCE_NAME)
    ]

    # Mock the return value of create_price_offering
    mock_offering = MagicMock(spec=PriceOffering)
    mock_create_price_offering.return_value = mock_offering

    asset_resource_name = create_price_asset(
        mock_google_ads_client, CUSTOMER_ID
    )

    assert asset_resource_name == MOCK_PRICE_ASSET_RESOURCE_NAME
    mock_asset_service.mutate_assets.assert_called_once()
    args, _ = mock_asset_service.mutate_assets.call_args
    assert args[0] == CUSTOMER_ID
    operation = args[1][0]  # Operations is a list
    assert isinstance(operation, AssetOperation)
    assert operation.create is not None
    created_asset = operation.create
    assert isinstance(created_asset, Asset)
    assert created_asset.name == EXPECTED_ASSET_NAME
    assert (
        created_asset.tracking_url_template
        == "http://tracker.example.com/?u={lpurl}"
    )
    assert created_asset.price_asset is not None

    price_asset_data = created_asset.price_asset
    assert isinstance(price_asset_data, PriceAsset)
    assert (
        price_asset_data.type_
        == PriceExtensionTypeEnum.PriceExtensionType.SERVICES
    )
    assert (
        price_asset_data.price_qualifier
        == PriceExtensionPriceQualifierEnum.PriceExtensionPriceQualifier.FROM
    )
    assert price_asset_data.language_code == "en"

    # Verify create_price_offering was called 3 times
    assert mock_create_price_offering.call_count == 3
    expected_calls = [
        call(
            mock_google_ads_client,
            "Scrubs",
            "Top quality scrubs",
            "http://www.example.com/scrubs",
            None,
            25000000,
            "USD",
            PriceExtensionPriceQualifierEnum.PriceExtensionPriceQualifier.FROM,
        ),
        call(
            mock_google_ads_client,
            "Hair Cuts",
            "Once-a-month full haircuts",
            "http://www.example.com/haircuts",
            None,
            60000000,
            "USD",
            PriceExtensionPriceQualifierEnum.PriceExtensionPriceQualifier.AVERAGE,
        ),
        call(
            mock_google_ads_client,
            "Manicures",
            "High quality designer manicures",
            "http://www.example.com/manicures",
            None,
            40000000,
            "USD",
            PriceExtensionPriceQualifierEnum.PriceExtensionPriceQualifier.FROM,
        ),
    ]
    mock_create_price_offering.assert_has_calls(expected_calls, any_order=False)


    # Verify price_offerings were added
    assert len(price_asset_data.price_offerings) == 3
    for offering in price_asset_data.price_offerings:
        assert offering == mock_offering

    mock_uuid.assert_called_once()


# Test for add_asset_to_account function (for price assets)
def test_add_asset_to_account_price(mock_google_ads_client):
    """Tests the add_asset_to_account function for price assets."""
    mock_customer_asset_service = mock_google_ads_client.get_service(
        "CustomerAssetService"
    )
    # Mock the response from mutate_customer_assets
    mock_customer_asset_service.mutate_customer_assets.return_value.results = [
        MagicMock(
            resource_name=f"customers/{CUSTOMER_ID}/customerAssets/{MOCK_PRICE_ASSET_RESOURCE_NAME.split('/')[-1]}"
        )
    ]

    add_asset_to_account(
        mock_google_ads_client, CUSTOMER_ID, MOCK_PRICE_ASSET_RESOURCE_NAME
    )

    mock_customer_asset_service.mutate_customer_assets.assert_called_once()
    args, _ = mock_customer_asset_service.mutate_customer_assets.call_args
    assert args[0] == CUSTOMER_ID
    operation = args[1][0]  # Operations is a list
    assert isinstance(operation, CustomerAssetOperation)
    assert operation.create is not None
    created_customer_asset = operation.create
    assert isinstance(created_customer_asset, CustomerAsset)
    assert created_customer_asset.asset == MOCK_PRICE_ASSET_RESOURCE_NAME
    assert (
        created_customer_asset.field_type
        == AssetFieldTypeEnum.AssetFieldType.PRICE
    )


# Tests for main function and argument parsing
@patch.object(
    sys,
    "argv",
    [
        "examples/assets/add_prices.py",
        f"--customer_id={CUSTOMER_ID}",
    ],
)
@patch("examples.assets.add_prices.GoogleAdsClient.load_from_storage")
@patch("examples.assets.add_prices.create_price_asset")
@patch("examples.assets.add_prices.add_asset_to_account")
def test_main_function_and_args(
    mock_add_asset_to_account,
    mock_create_price_asset,
    mock_load_from_storage,
    mock_google_ads_client,  # Fixture for client
    capsys,
):
    """Tests the main function and argument parsing."""
    mock_load_from_storage.return_value = mock_google_ads_client
    mock_create_price_asset.return_value = MOCK_PRICE_ASSET_RESOURCE_NAME
    # The add_asset_to_account function in the example doesn't return anything
    mock_add_asset_to_account.return_value = None

    add_prices_main()

    mock_load_from_storage.assert_called_once_with(version="v19")
    mock_create_price_asset.assert_called_once_with(
        mock_google_ads_client, CUSTOMER_ID
    )
    mock_add_asset_to_account.assert_called_once_with(
        mock_google_ads_client, CUSTOMER_ID, MOCK_PRICE_ASSET_RESOURCE_NAME
    )

    # Check stdout for printed messages
    captured = capsys.readouterr()
    assert (
        f"Price asset with resource name '{MOCK_PRICE_ASSET_RESOURCE_NAME}' was created."
        in captured.out
    )
    assert (
        f"Price asset with resource name '{MOCK_PRICE_ASSET_RESOURCE_NAME}' "
        f"was added to customer ID '{CUSTOMER_ID}'." in captured.out
    )
