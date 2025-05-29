import pytest
from unittest.mock import MagicMock, patch

from examples.advanced_operations.add_bidding_data_exclusion import main

@patch("examples.advanced_operations.add_bidding_data_exclusion.uuid4", return_value=MagicMock(hex="testuuid"))
def test_main_runs_successfully(mock_uuid4: MagicMock, mock_google_ads_client: MagicMock) -> None:
    """Tests that the main function runs without raising an exception."""
    mock_customer_id = "123"
    mock_start_date_time = "2023-10-01 00:00:00"
    mock_end_date_time = "2023-10-02 00:00:00"

    # Mock BiddingDataExclusionService
    mock_bde_service = mock_google_ads_client.get_service("BiddingDataExclusionService")
    mock_mutate_response = MagicMock()
    mock_result = MagicMock()
    mock_result.resource_name = "mock_resource_name_bde"
    mock_mutate_response.results = [mock_result]
    mock_bde_service.mutate_bidding_data_exclusions.return_value = mock_mutate_response

    # Mock enums
    mock_enums = mock_google_ads_client.enums
    mock_enums.SeasonalityEventScopeEnum.CHANNEL = "CHANNEL"
    mock_enums.AdvertisingChannelTypeEnum.SEARCH = "SEARCH"
    # The script also uses DeviceEnum, but it's commented out, so not strictly needed for this test pass
    # mock_enums.DeviceEnum.MOBILE = "MOBILE" 

    try:
        main(
            mock_google_ads_client,
            mock_customer_id,
            mock_start_date_time,
            mock_end_date_time,
        )
    except Exception as e:
        pytest.fail(f"main function raised an exception: {e}")
