import pytest
from unittest.mock import MagicMock

from examples.advanced_operations.get_ad_group_bid_modifiers import main

# --- Helper Mock Class ---
class MockAdGroupBidModifierModel:
    def __init__(self, client_enums):
        # Attributes accessed directly by the script's print statement
        self.criterion_id = MagicMock(name="criterion_id")
        self.bid_modifier = MagicMock(name="bid_modifier")
        
        self.device = MagicMock(name="device_criterion")
        # Ensure type_ itself can have .name called on it
        self.device.type_ = MagicMock(name="device_type_enum_value")
        self.device.type_.name = "UNKNOWN_DEVICE" # Default .name for the enum value

        # Hotel criteria attributes
        self.hotel_date_selection_type = MagicMock(name="hotel_date_selection_type_criterion")
        self.hotel_date_selection_type.type_ = MagicMock(name="hotel_date_selection_type_enum_value")
        self.hotel_date_selection_type.type_.name = "UNKNOWN_HOTEL_DATE_SELECTION"

        self.hotel_advance_booking_window = MagicMock(name="hotel_advance_booking_window_criterion")
        self.hotel_advance_booking_window.min_days = None
        self.hotel_advance_booking_window.max_days = None

        self.hotel_length_of_stay = MagicMock(name="hotel_length_of_stay_criterion")
        self.hotel_length_of_stay.min_nights = None
        self.hotel_length_of_stay.max_nights = None

        self.hotel_check_in_day = MagicMock(name="hotel_check_in_day_criterion")
        self.hotel_check_in_day.day_of_week = MagicMock(name="day_of_week_enum_value")
        self.hotel_check_in_day.day_of_week.name = "UNSPECIFIED_DAY"
        
        self.hotel_check_in_date_range = MagicMock(name="hotel_check_in_date_range_criterion")
        self.hotel_check_in_date_range.start_date = None
        self.hotel_check_in_date_range.end_date = None
        
        # This will store the name of the 'oneof' criterion field (e.g., "device")
        self._active_criterion_field = None # Default to None, must be set by test

    @classmethod
    def pb(cls, instance_self):
        mock_pb_message = MagicMock(name="pb_message")
        mock_pb_message.WhichOneof.return_value = instance_self._active_criterion_field
        return mock_pb_message

    def set_active_criterion_field(self, field_name):
        self._active_criterion_field = field_name
        # Basic way to somewhat mimic oneof: clear other fields if one is set.
        # More robust would be to ensure only the active field has a non-default/non-None value.
        # For this mock, primarily WhichOneof matters for the script's logic.
        all_criteria_fields = [
            "device", "hotel_date_selection_type", "hotel_advance_booking_window",
            "hotel_length_of_stay", "hotel_check_in_day", "hotel_check_in_date_range"
        ]
        if field_name not in all_criteria_fields and field_name is not None:
            raise ValueError(f"Unknown criterion field: {field_name}")
        return self

# --- Test Functions ---
def test_main_runs_successfully(mock_google_ads_client: MagicMock) -> None:
    """Tests that the main function runs without raising an exception with an ad_group_id."""
    mock_customer_id = "123"
    mock_ad_group_id = "456"

    # --- Mock Enums (ensure they have .name attribute) ---
    mock_google_ads_client.enums.DeviceEnum.MOBILE.name = "MOBILE_DEVICE"
    mock_google_ads_client.enums.DeviceEnum.TABLET.name = "TABLET_DEVICE" # Just in case
    mock_google_ads_client.enums.DeviceEnum.DESKTOP.name = "DESKTOP_DEVICE" # Just in case
    mock_google_ads_client.enums.DeviceEnum.UNKNOWN.name = "UNKNOWN_DEVICE" # Default

    mock_google_ads_client.enums.DayOfWeekEnum.MONDAY.name = "MONDAY"
    mock_google_ads_client.enums.DayOfWeekEnum.UNSPECIFIED.name = "UNSPECIFIED_DOW" # Default
    
    # Add other hotel enums if specific paths are tested, e.g., HotelDateSelectionTypeEnum
    mock_google_ads_client.enums.HotelDateSelectionTypeEnum.DEFAULT_SELECTION.name = "DEFAULT_SELECTION"
    mock_google_ads_client.enums.HotelDateSelectionTypeEnum.UNKNOWN.name = "UNKNOWN_HDST" # Default

    # --- Mock GoogleAdsService for search ---
    mock_googleads_service = mock_google_ads_client.get_service("GoogleAdsService")
    
    # Row 1: Device Modifier
    mock_row1 = MagicMock()
    modifier1 = MockAdGroupBidModifierModel(mock_google_ads_client.enums)
    modifier1.criterion_id = "1001"
    modifier1.bid_modifier = 1.5
    modifier1.set_active_criterion_field("device")
    modifier1.device.type_ = mock_google_ads_client.enums.DeviceEnum.MOBILE
    mock_row1.ad_group_bid_modifier = modifier1
    mock_row1.ad_group.id = int(mock_ad_group_id)
    mock_row1.campaign.id = "789"

    # Row 2: Hotel Check-in Day Modifier
    mock_row2 = MagicMock()
    modifier2 = MockAdGroupBidModifierModel(mock_google_ads_client.enums)
    modifier2.criterion_id = "2002"
    modifier2.bid_modifier = 0.8
    modifier2.set_active_criterion_field("hotel_check_in_day")
    modifier2.hotel_check_in_day.day_of_week = mock_google_ads_client.enums.DayOfWeekEnum.MONDAY
    mock_row2.ad_group_bid_modifier = modifier2
    mock_row2.ad_group.id = int(mock_ad_group_id)
    mock_row2.campaign.id = "790"
    
    mock_search_response_page = MagicMock()
    mock_search_response_page.results = [mock_row1, mock_row2]
    mock_googleads_service.search.return_value = iter([mock_search_response_page])

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
    mock_ad_group_id = None # Key difference for this test

    # --- Mock Enums (ensure they have .name attribute) ---
    # Ensure these are available on the mock_google_ads_client.enums object
    # The conftest should provide the base enums, we just need to ensure .name is on values.
    mock_google_ads_client.enums.DeviceEnum.TABLET.name = "TABLET_DEVICE"
    mock_google_ads_client.enums.DeviceEnum.UNKNOWN.name = "UNKNOWN_DEVICE"

    # --- Mock GoogleAdsService for search ---
    mock_googleads_service = mock_google_ads_client.get_service("GoogleAdsService")
    
    mock_row1 = MagicMock()
    modifier1 = MockAdGroupBidModifierModel(mock_google_ads_client.enums)
    modifier1.criterion_id = "3003"
    modifier1.bid_modifier = 1.2
    modifier1.set_active_criterion_field("device")
    modifier1.device.type_ = mock_google_ads_client.enums.DeviceEnum.TABLET
    mock_row1.ad_group_bid_modifier = modifier1
    mock_row1.ad_group.id = "987" # Different ad group ID
    mock_row1.campaign.id = "654"
    
    mock_search_response_page = MagicMock()
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
