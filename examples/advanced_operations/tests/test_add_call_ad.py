import pytest
from unittest.mock import MagicMock

from examples.advanced_operations.add_call_ad import main

def test_main_runs_successfully(mock_google_ads_client: MagicMock) -> None:
    """Tests that the main function runs without raising an exception."""
    mock_customer_id = "123"
    mock_ad_group_id = "456"
    mock_phone_number = "(800) 555-0100"
    mock_phone_country = "US"
    mock_conversion_action_id = None  # Or a string "789" if testing that path

    # Mock GoogleAdsService for path helpers
    mock_googleads_service = mock_google_ads_client.get_service("GoogleAdsService")
    mock_googleads_service.ad_group_path.return_value = f"customers/{mock_customer_id}/adGroups/{mock_ad_group_id}"
    if mock_conversion_action_id:
        mock_googleads_service.conversion_action_path.return_value = f"customers/{mock_customer_id}/conversionActions/{mock_conversion_action_id}"

    # Mock AdGroupAdService
    mock_ad_group_ad_service = mock_google_ads_client.get_service("AdGroupAdService")
    mock_mutate_response = MagicMock()
    mock_result = MagicMock()
    mock_result.resource_name = "mock_resource_name_ad_group_ad"
    mock_mutate_response.results = [mock_result]
    mock_ad_group_ad_service.mutate_ad_group_ads.return_value = mock_mutate_response

    # Mock enums
    mock_enums = mock_google_ads_client.enums
    mock_enums.AdGroupAdStatusEnum.PAUSED = "PAUSED"
    mock_enums.CallConversionReportingStateEnum.USE_RESOURCE_LEVEL_CALL_CONVERSION_ACTION = "USE_RESOURCE_LEVEL_CALL_CONVERSION_ACTION"
    # If mock_conversion_action_id is None, this enum below is used.
    mock_enums.CallConversionReportingStateEnum.USE_ACCOUNT_LEVEL_CALL_CONVERSION_ACTION = "USE_ACCOUNT_LEVEL_CALL_CONVERSION_ACTION"


    try:
        main(
            mock_google_ads_client,
            mock_customer_id,
            mock_ad_group_id,
            mock_phone_number,
            mock_phone_country,
            mock_conversion_action_id,
        )
    except Exception as e:
        pytest.fail(f"main function raised an exception: {e}")
