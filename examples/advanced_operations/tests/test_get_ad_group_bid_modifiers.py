import pytest
from unittest.mock import MagicMock

from examples.advanced_operations.get_ad_group_bid_modifiers import main

def test_main_runs_successfully(mock_google_ads_client: MagicMock) -> None:
    """Tests that the main function runs without raising an exception with an ad_group_id."""
    mock_customer_id = "123"
    mock_ad_group_id = "456"

    # Mock GoogleAdsService for search
    mock_googleads_service = mock_google_ads_client.get_service("GoogleAdsService")
    
    mock_search_response_page = MagicMock() # Represents one page of results
    mock_row1 = MagicMock()
    mock_row1.ad_group_bid_modifier.criterion_id = 12345
    mock_row1.ad_group_bid_modifier.bid_modifier = 1.5
    mock_row1.ad_group_bid_modifier.device.type_ = mock_google_ads_client.enums.DeviceEnum.MOBILE
    mock_row1.ad_group.id = int(mock_ad_group_id)
    mock_row1.campaign.id = 789

    mock_row2 = MagicMock() # Example for a non-device modifier (e.g. hotel)
    mock_row2.ad_group_bid_modifier.criterion_id = 67890
    mock_row2.ad_group_bid_modifier.bid_modifier = 0.8
    # For hotel check-in day, the device field won't be populated.
    # Instead, hotel_check_in_day field would be, for example:
    mock_row2.ad_group_bid_modifier.hotel_check_in_day.day_of_week = mock_google_ads_client.enums.DayOfWeekEnum.MONDAY
    # Clear other oneof fields like device for this specific row if the script checks for their absence
    delattr(mock_row2.ad_group_bid_modifier, 'device') 
    mock_row2.ad_group.id = int(mock_ad_group_id)
    mock_row2.campaign.id = 789
    
    mock_search_response_page.results = [mock_row1, mock_row2]
    # The search method returns an iterable of pages (MagicMock with results)
    mock_googleads_service.search.return_value = iter([mock_search_response_page])

    # Ensure enums used in results and script are available (DeviceEnum, DayOfWeekEnum)
    # These should be on mock_google_ads_client.enums from conftest.
    # e.g. mock_google_ads_client.enums.DeviceEnum.MOBILE
    # e.g. mock_google_ads_client.enums.DayOfWeekEnum.MONDAY

    try:
        main(
            mock_google_ads_client,
            mock_customer_id,
            mock_ad_group_id,
        )
    except Exception as e:
        pytest.fail(f"main function raised an exception: {e}")

def test_main_runs_without_ad_group_id(mock_google_ads_client: MagicMock) -> None:
    """Tests that the main function runs without an ad_group_id (fetches for all ad groups)."""
    mock_customer_id = "123"
    mock_ad_group_id = None

    mock_googleads_service = mock_google_ads_client.get_service("GoogleAdsService")
    
    mock_search_response_page = MagicMock()
    mock_row1 = MagicMock()
    mock_row1.ad_group_bid_modifier.criterion_id = 54321
    mock_row1.ad_group_bid_modifier.bid_modifier = 1.2
    mock_row1.ad_group_bid_modifier.device.type_ = mock_google_ads_client.enums.DeviceEnum.TABLET
    mock_row1.ad_group.id = 987 # Different ad group ID
    mock_row1.campaign.id = 654
    
    mock_search_response_page.results = [mock_row1]
    mock_googleads_service.search.return_value = iter([mock_search_response_page])

    try:
        main(
            mock_google_ads_client,
            mock_customer_id,
            mock_ad_group_id, # None
        )
    except Exception as e:
        pytest.fail(f"main function raised an exception: {e}")
