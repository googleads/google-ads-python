import pytest
from unittest.mock import MagicMock, patch

from examples.advanced_operations.add_display_upload_ad import main

@patch("examples.advanced_operations.add_display_upload_ad.requests.get")
def test_main_runs_successfully(mock_requests_get: MagicMock, mock_google_ads_client: MagicMock) -> None:
    """Tests that the main function runs without raising an exception."""
    mock_customer_id = "123"
    mock_ad_group_id = "456"

    # Configure the mock for requests.get
    mock_response = MagicMock()
    mock_response.content = b"dummy_bundle_content"
    mock_requests_get.return_value = mock_response

    # Mock AssetService
    mock_asset_service = mock_google_ads_client.get_service("AssetService")
    mock_asset_mutate_response = MagicMock()
    mock_asset_result = MagicMock()
    mock_asset_result.resource_name = "mock_resource_name_asset"
    mock_asset_mutate_response.results = [mock_asset_result]
    mock_asset_service.mutate_assets.return_value = mock_asset_mutate_response

    # Mock AdGroupService for ad_group_path
    mock_ad_group_service_path_helper = mock_google_ads_client.get_service("AdGroupService")
    mock_ad_group_service_path_helper.ad_group_path.return_value = f"customers/{mock_customer_id}/adGroups/{mock_ad_group_id}"
    
    # Mock AdGroupAdService
    mock_ad_group_ad_service = mock_google_ads_client.get_service("AdGroupAdService")
    mock_ad_mutate_response = MagicMock()
    mock_ad_result = MagicMock()
    mock_ad_result.resource_name = "mock_resource_name_ad_group_ad"
    mock_ad_mutate_response.results = [mock_ad_result]
    mock_ad_group_ad_service.mutate_ad_group_ads.return_value = mock_ad_mutate_response

    # Mock enums
    mock_enums = mock_google_ads_client.enums
    mock_enums.AssetTypeEnum.MEDIA_BUNDLE = "MEDIA_BUNDLE"
    mock_enums.AdGroupAdStatusEnum.PAUSED = "PAUSED"
    mock_enums.DisplayUploadProductTypeEnum.HTML5_UPLOAD_AD = "HTML5_UPLOAD_AD"
    
    # Mock types
    # mock_asset_operation = mock_google_ads_client.get_type("AssetOperation")
    # mock_ad_group_ad_operation = mock_google_ads_client.get_type("AdGroupAdOperation")
    # Default MagicMock for types should be sufficient.

    try:
        main(
            mock_google_ads_client,
            mock_customer_id,
            mock_ad_group_id,
        )
    except Exception as e:
        pytest.fail(f"main function raised an exception: {e}")
