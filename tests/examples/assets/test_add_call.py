import pytest
from unittest.mock import MagicMock, patch, call

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.v19.services.types.asset_service import AssetOperation
from google.ads.googleads.v19.services.types.customer_asset_service import CustomerAssetOperation
from google.ads.googleads.v19.enums.types.asset_field_type import AssetFieldTypeEnum
from google.ads.googleads.v19.enums.types.call_conversion_reporting_state import CallConversionReportingStateEnum

from examples.assets.add_call import add_call_asset, link_asset_to_account, main
from google.ads.googleads.v19.common.types.asset_types import CallAsset
from google.ads.googleads.v19.resources.types.asset import Asset
from google.ads.googleads.v19.resources.types.customer_asset import CustomerAsset


# Define constants for testing
CUSTOMER_ID = "1234567890"
PHONE_NUMBER = "555-555-5555"
COUNTRY_CODE = "US"
CONVERSION_ACTION_ID = "987654321"
AD_GROUP_ID = "111222333"
# Mock resource name for the created asset
CALL_ASSET_RESOURCE_NAME = f"customers/{CUSTOMER_ID}/assets/123"

@pytest.fixture
def mock_google_ads_client():
    """Provides a mock GoogleAdsClient."""
    mock_client = MagicMock(spec=GoogleAdsClient)
    # Mock get_service
    mock_asset_service = MagicMock()
    mock_customer_asset_service = MagicMock()
    mock_googleads_service = MagicMock()
    mock_client.get_service.side_effect = lambda service_name: {
        "AssetService": mock_asset_service,
        "CustomerAssetService": mock_customer_asset_service,
        "GoogleAdsService": mock_googleads_service,
    }.get(service_name)

    # Mock get_type
    def get_type_side_effect(type_name, version=None):
        if type_name == "AssetOperation":
            return AssetOperation
        elif type_name == "CustomerAssetOperation":
            return CustomerAssetOperation
        elif type_name == "Asset":
            return Asset
        elif type_name == "CallAsset":
            return CallAsset
        elif type_name == "CustomerAsset":
            return CustomerAsset
        raise ValueError(f"Unknown type: {type_name}")
    mock_client.get_type.side_effect = get_type_side_effect

    # Mock enums
    mock_client.enums.AssetFieldTypeEnum = AssetFieldTypeEnum
    mock_client.enums.CallConversionReportingStateEnum = CallConversionReportingStateEnum
    # Mock conversion_action_path for GoogleAdsService
    mock_googleads_service.conversion_action_path.return_value = f"customers/{CUSTOMER_ID}/conversionActions/{CONVERSION_ACTION_ID}"


    return mock_client

# Test for add_call_asset function
def test_add_call_asset_without_conversion_action(mock_google_ads_client):
    """Tests add_call_asset when conversion_action_id is None."""
    mock_asset_service = mock_google_ads_client.get_service("AssetService")
    # Mock the response from mutate_assets
    mock_asset_service.mutate_assets.return_value.results = [
        MagicMock(resource_name=CALL_ASSET_RESOURCE_NAME)
    ]

    asset_resource_name = add_call_asset(
        mock_google_ads_client, CUSTOMER_ID, PHONE_NUMBER, COUNTRY_CODE, None
    )

    assert asset_resource_name == CALL_ASSET_RESOURCE_NAME
    mock_asset_service.mutate_assets.assert_called_once()
    args, _ = mock_asset_service.mutate_assets.call_args
    assert args[0] == CUSTOMER_ID
    # Check the operation
    operation = args[1][0] # Operations is a list
    assert isinstance(operation, AssetOperation)
    assert operation.create is not None
    created_asset = operation.create
    assert isinstance(created_asset, Asset)
    assert created_asset.name == ""  # Name is set by the server
    assert created_asset.call_asset is not None
    call_asset = created_asset.call_asset
    assert isinstance(call_asset, CallAsset)
    assert call_asset.phone_number == PHONE_NUMBER
    assert call_asset.country_code == COUNTRY_CODE
    assert not call_asset.call_conversion_action  # Should be empty
    assert call_asset.call_conversion_reporting_state == CallConversionReportingStateEnum.CallConversionReportingState.USE_ACCOUNT_LEVEL_CALL_CONVERSION_ACTION


def test_add_call_asset_with_conversion_action(mock_google_ads_client):
    """Tests add_call_asset when conversion_action_id is provided."""
    mock_asset_service = mock_google_ads_client.get_service("AssetService")
    mock_googleads_service = mock_google_ads_client.get_service("GoogleAdsService")
    # Mock the response from mutate_assets
    mock_asset_service.mutate_assets.return_value.results = [
        MagicMock(resource_name=CALL_ASSET_RESOURCE_NAME)
    ]
    expected_conversion_action_path = (
        f"customers/{CUSTOMER_ID}/conversionActions/{CONVERSION_ACTION_ID}"
    )
    mock_googleads_service.conversion_action_path.return_value = (
        expected_conversion_action_path
    )

    asset_resource_name = add_call_asset(
        mock_google_ads_client,
        CUSTOMER_ID,
        PHONE_NUMBER,
        COUNTRY_CODE,
        CONVERSION_ACTION_ID,
    )

    assert asset_resource_name == CALL_ASSET_RESOURCE_NAME
    mock_asset_service.mutate_assets.assert_called_once()
    args, _ = mock_asset_service.mutate_assets.call_args
    assert args[0] == CUSTOMER_ID
    # Check the operation
    operation = args[1][0]
    assert isinstance(operation, AssetOperation)
    assert operation.create is not None
    created_asset = operation.create
    assert isinstance(created_asset, Asset)
    assert created_asset.call_asset is not None
    call_asset = created_asset.call_asset
    assert isinstance(call_asset, CallAsset)
    assert call_asset.phone_number == PHONE_NUMBER
    assert call_asset.country_code == COUNTRY_CODE
    assert call_asset.call_conversion_action == expected_conversion_action_path
    assert call_asset.call_conversion_reporting_state == CallConversionReportingStateEnum.CallConversionReportingState.USE_RESOURCE_LEVEL_CALL_CONVERSION_ACTION
    mock_googleads_service.conversion_action_path.assert_called_once_with(
        CUSTOMER_ID, CONVERSION_ACTION_ID
    )

# Test for link_asset_to_account function
def test_link_asset_to_account(mock_google_ads_client):
    """Tests the link_asset_to_account function."""
    mock_customer_asset_service = mock_google_ads_client.get_service(
        "CustomerAssetService"
    )
    # Mock the response from mutate_customer_assets
    mock_customer_asset_service.mutate_customer_assets.return_value.results = [
        MagicMock(resource_name=f"customers/{CUSTOMER_ID}/customerAssets/123_CALL")
    ]

    link_asset_to_account(
        mock_google_ads_client, CUSTOMER_ID, CALL_ASSET_RESOURCE_NAME
    )

    mock_customer_asset_service.mutate_customer_assets.assert_called_once()
    args, _ = mock_customer_asset_service.mutate_customer_assets.call_args
    assert args[0] == CUSTOMER_ID
    # Check the operation
    operation = args[1][0] # Operations is a list
    assert isinstance(operation, CustomerAssetOperation)
    assert operation.create is not None
    created_customer_asset = operation.create
    assert isinstance(created_customer_asset, CustomerAsset)
    assert created_customer_asset.asset == CALL_ASSET_RESOURCE_NAME
    assert created_customer_asset.field_type == AssetFieldTypeEnum.AssetFieldType.CALL


# Tests for main function and argument parsing
@patch("sys.argv", [
    "examples/assets/add_call.py",
    f"--customer_id={CUSTOMER_ID}",
    f"--phone_number={PHONE_NUMBER}",
    f"--country_code={COUNTRY_CODE}",
])
@patch("examples.assets.add_call.GoogleAdsClient.load_from_storage")
@patch("examples.assets.add_call.add_call_asset")
@patch("examples.assets.add_call.link_asset_to_account")
def test_main_without_conversion_action_id(
    mock_link_asset_to_account,
    mock_add_call_asset,
    mock_load_from_storage,
    mock_google_ads_client, # Use the fixture for the client
    capsys,
):
    """Tests the main function when conversion_action_id is not provided."""
    mock_load_from_storage.return_value = mock_google_ads_client
    mock_add_call_asset.return_value = CALL_ASSET_RESOURCE_NAME

    main()

    mock_load_from_storage.assert_called_once_with(version="v19")
    mock_add_call_asset.assert_called_once_with(
        mock_google_ads_client,
        CUSTOMER_ID,
        PHONE_NUMBER,
        COUNTRY_CODE,
        None, # conversion_action_id
        None, # ad_group_id - not testing this here
    )
    mock_link_asset_to_account.assert_called_once_with(
        mock_google_ads_client, CUSTOMER_ID, CALL_ASSET_RESOURCE_NAME, None # ad_group_id
    )
    # Check stdout for printed messages (optional, but good practice)
    captured = capsys.readouterr()
    assert f"Created call asset with resource name '{CALL_ASSET_RESOURCE_NAME}'" in captured.out
    assert f"Linked call asset to customer '{CUSTOMER_ID}'." in captured.out


@patch("sys.argv", [
    "examples/assets/add_call.py",
    f"--customer_id={CUSTOMER_ID}",
    f"--phone_number={PHONE_NUMBER}",
    f"--country_code={COUNTRY_CODE}",
    f"--conversion_action_id={CONVERSION_ACTION_ID}",
])
@patch("examples.assets.add_call.GoogleAdsClient.load_from_storage")
@patch("examples.assets.add_call.add_call_asset")
@patch("examples.assets.add_call.link_asset_to_account")
def test_main_with_conversion_action_id(
    mock_link_asset_to_account,
    mock_add_call_asset,
    mock_load_from_storage,
    mock_google_ads_client, # Use the fixture
    capsys,
):
    """Tests the main function when conversion_action_id is provided."""
    mock_load_from_storage.return_value = mock_google_ads_client
    mock_add_call_asset.return_value = CALL_ASSET_RESOURCE_NAME

    main()

    mock_load_from_storage.assert_called_once_with(version="v19")
    mock_add_call_asset.assert_called_once_with(
        mock_google_ads_client,
        CUSTOMER_ID,
        PHONE_NUMBER,
        COUNTRY_CODE,
        CONVERSION_ACTION_ID,
        None, # ad_group_id
    )
    mock_link_asset_to_account.assert_called_once_with(
        mock_google_ads_client, CUSTOMER_ID, CALL_ASSET_RESOURCE_NAME, None # ad_group_id
    )
    captured = capsys.readouterr()
    assert f"Created call asset with resource name '{CALL_ASSET_RESOURCE_NAME}'" in captured.out
    assert f"Linked call asset to customer '{CUSTOMER_ID}'." in captured.out


@patch("sys.argv", [
    "examples/assets/add_call.py",
    f"--customer_id={CUSTOMER_ID}",
    f"--phone_number={PHONE_NUMBER}",
    f"--country_code={COUNTRY_CODE}",
    f"--ad_group_id={AD_GROUP_ID}",
])
@patch("examples.assets.add_call.GoogleAdsClient.load_from_storage")
@patch("examples.assets.add_call.add_call_asset")
@patch("examples.assets.add_call.link_asset_to_account") # This should be link_asset_to_ad_group
@patch("examples.assets.add_call.link_asset_to_ad_group") # Add this mock
def test_main_with_ad_group_id(
    mock_link_asset_to_ad_group, # Corrected mock name
    mock_link_asset_to_account, # Keep this for now, though it might not be called
    mock_add_call_asset,
    mock_load_from_storage,
    mock_google_ads_client, # Use the fixture
    capsys,
):
    """Tests the main function when ad_group_id is provided."""
    mock_load_from_storage.return_value = mock_google_ads_client
    mock_add_call_asset.return_value = CALL_ASSET_RESOURCE_NAME

    main()

    mock_load_from_storage.assert_called_once_with(version="v19")
    mock_add_call_asset.assert_called_once_with(
        mock_google_ads_client,
        CUSTOMER_ID,
        PHONE_NUMBER,
        COUNTRY_CODE,
        None, # conversion_action_id
        AD_GROUP_ID,
    )
    # Assert that link_asset_to_account was NOT called
    mock_link_asset_to_account.assert_not_called()
    # Assert that link_asset_to_ad_group was called
    mock_link_asset_to_ad_group.assert_called_once_with(
        mock_google_ads_client, CUSTOMER_ID, CALL_ASSET_RESOURCE_NAME, AD_GROUP_ID
    )
    captured = capsys.readouterr()
    assert f"Created call asset with resource name '{CALL_ASSET_RESOURCE_NAME}'" in captured.out
    assert f"Linked call asset to ad group '{AD_GROUP_ID}'." in captured.out
