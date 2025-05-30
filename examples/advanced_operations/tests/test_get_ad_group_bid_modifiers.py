import pytest
from unittest.mock import MagicMock
import pytest # Ensure pytest is imported if not already

from examples.advanced_operations.get_ad_group_bid_modifiers import main

class MockAdGroupBidModifierModel:
    def __init__(self, client_enums_mock): # Renamed to avoid conflict with client fixture
        # --- Begin: Attributes accessed directly by the script's print statement or logic ---
        self.criterion_id = MagicMock(name="criterion_id_attr")
        self.bid_modifier = MagicMock(name="bid_modifier_attr")

        self.device = MagicMock(name="device_attr")
        # Ensure type_ itself is a mock that has a .name attribute
        self.device.type_ = MagicMock(name="device_type_attr")
        self.device.type_.name = "DEFAULT_DEVICE_NAME" # Default .name

        # Hotel criteria attributes (initialize them as MagicMocks)
        self.hotel_date_selection_type = MagicMock(name="hotel_date_selection_type_attr")
        self.hotel_date_selection_type.type_ = MagicMock(name="hotel_date_selection_type_type_attr")
        self.hotel_date_selection_type.type_.name = "DEFAULT_HOTEL_DATE_NAME"


        self.hotel_advance_booking_window = MagicMock(name="hotel_advance_booking_window_attr")
        self.hotel_advance_booking_window.min_days = None
        self.hotel_advance_booking_window.max_days = None

        self.hotel_length_of_stay = MagicMock(name="hotel_length_of_stay_attr")
        self.hotel_length_of_stay.min_nights = None
        self.hotel_length_of_stay.max_nights = None

        self.hotel_check_in_day = MagicMock(name="hotel_check_in_day_attr")
        self.hotel_check_in_day.day_of_week = MagicMock(name="hotel_check_in_day_day_of_week_attr")
        self.hotel_check_in_day.day_of_week.name = "DEFAULT_DAY_OF_WEEK_NAME"

        self.hotel_check_in_date_range = MagicMock(name="hotel_check_in_date_range_attr")
        self.hotel_check_in_date_range.start_date = None
        self.hotel_check_in_date_range.end_date = None

        # This will store the name of the 'oneof' criterion field (e.g., "device")
        self._active_criterion_field = "device" # Default active field

    # This class method mimics the real .pb() class method on Google Ads model classes.
    @classmethod
    def pb(cls, instance_self):
        # instance_self here is an instance of MockAdGroupBidModifierModel
        mock_pb_message = MagicMock(name="pb_message_obj_from_class")
        # WhichOneof should return the active criterion field name for this instance
        mock_pb_message.WhichOneof.return_value = instance_self._active_criterion_field
        return mock_pb_message

    # Helper to set the active criterion field for testing different types
    def set_active_criterion_field(self, field_name_str):
        self._active_criterion_field = field_name_str
        # Example: If setting device, ensure device attributes are primary
        if field_name_str == "device":
            # self.device.type_ is already a mock, its .name can be set in test
            pass
        # Add similar logic if other criterion types need specific default setup when activated
        return self

# --- Test Functions ---
def test_main_runs_successfully(mock_google_ads_client: MagicMock) -> None:
    """Tests that the main function runs without raising an exception with an ad_group_id."""
    mock_customer_id = "123"
    mock_ad_group_id = "456"

    # --- Mock Enums (ensure they have .name attribute) ---
    mock_enums = mock_google_ads_client.enums

    # DeviceEnum setup
    mock_enums.DeviceEnum.MOBILE = MagicMock(name="DeviceEnum.MOBILE"); mock_enums.DeviceEnum.MOBILE.name = "MOBILE"
    mock_enums.DeviceEnum.TABLET = MagicMock(name="DeviceEnum.TABLET"); mock_enums.DeviceEnum.TABLET.name = "TABLET"
    mock_enums.DeviceEnum.DESKTOP = MagicMock(name="DeviceEnum.DESKTOP"); mock_enums.DeviceEnum.DESKTOP.name = "DESKTOP"
    mock_enums.DeviceEnum.UNKNOWN = MagicMock(name="DeviceEnum.UNKNOWN"); mock_enums.DeviceEnum.UNKNOWN.name = "UNKNOWN_DEVICE_FOR_PRINT" # Default in class constructor matched

    # HotelDateSelectionTypeEnum setup
    mock_enums.HotelDateSelectionTypeEnum.DEFAULT_SELECTION = MagicMock(name="HotelDateSelectionTypeEnum.DEFAULT_SELECTION"); mock_enums.HotelDateSelectionTypeEnum.DEFAULT_SELECTION.name = "DEFAULT_SELECTION"
    mock_enums.HotelDateSelectionTypeEnum.USER_SELECTED = MagicMock(name="HotelDateSelectionTypeEnum.USER_SELECTED"); mock_enums.HotelDateSelectionTypeEnum.USER_SELECTED.name = "USER_SELECTED"
    mock_enums.HotelDateSelectionTypeEnum.UNKNOWN = MagicMock(name="HotelDateSelectionTypeEnum.UNKNOWN"); mock_enums.HotelDateSelectionTypeEnum.UNKNOWN.name = "UNKNOWN_HOTEL_DATE_FOR_PRINT"

    # DayOfWeekEnum setup
    mock_enums.DayOfWeekEnum.MONDAY = MagicMock(name="DayOfWeekEnum.MONDAY"); mock_enums.DayOfWeekEnum.MONDAY.name = "MONDAY"
    mock_enums.DayOfWeekEnum.UNSPECIFIED = MagicMock(name="DayOfWeekEnum.UNSPECIFIED"); mock_enums.DayOfWeekEnum.UNSPECIFIED.name = "UNSPECIFIED_DAY_FOR_PRINT"

    # --- Mock GoogleAdsService for search ---
    mock_googleads_service = mock_google_ads_client.get_service("GoogleAdsService")

    # Row 1: Device Modifier
    row1 = MagicMock()
    row1.campaign.id = "campaign1"
    row1.ad_group.id = int(mock_ad_group_id) # Match ad_group_id if provided

    modifier_device = MockAdGroupBidModifierModel(mock_google_ads_client.enums)
    modifier_device.criterion_id = "100"
    modifier_device.bid_modifier = 1.5
    modifier_device.set_active_criterion_field("device")
    modifier_device.device.type_ = mock_google_ads_client.enums.DeviceEnum.MOBILE
    row1.ad_group_bid_modifier = modifier_device

    # Row 2: Hotel Check-in Day Modifier
    row2 = MagicMock()
    row2.campaign.id = "campaign2"
    row2.ad_group.id = int(mock_ad_group_id)

    modifier_hotel_day = MockAdGroupBidModifierModel(mock_google_ads_client.enums)
    modifier_hotel_day.criterion_id = "200"
    modifier_hotel_day.bid_modifier = 0.8
    modifier_hotel_day.set_active_criterion_field("hotel_check_in_day")
    modifier_hotel_day.hotel_check_in_day.day_of_week = mock_google_ads_client.enums.DayOfWeekEnum.MONDAY
    row2.ad_group_bid_modifier = modifier_hotel_day

    mock_search_response_page = MagicMock()
    mock_search_response_page.results = [row1, row2]
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
    mock_enums = mock_google_ads_client.enums
    mock_enums.DeviceEnum.TABLET = MagicMock(name="DeviceEnum.TABLET"); mock_enums.DeviceEnum.TABLET.name = "TABLET"
    mock_enums.DeviceEnum.UNKNOWN = MagicMock(name="DeviceEnum.UNKNOWN"); mock_enums.DeviceEnum.UNKNOWN.name = "UNKNOWN_DEVICE_FOR_PRINT" # Default in class constructor matched

    # --- Mock GoogleAdsService for search ---
    mock_googleads_service = mock_google_ads_client.get_service("GoogleAdsService")

    row1 = MagicMock()
    row1.campaign.id = "campaign3"
    row1.ad_group.id = "987" # Script expects ad_group.id to be populated

    modifier1 = MockAdGroupBidModifierModel(mock_google_ads_client.enums)
    modifier1.criterion_id = "3003"
    modifier1.bid_modifier = 1.2
    modifier1.set_active_criterion_field("device")
    modifier1.device.type_ = mock_google_ads_client.enums.DeviceEnum.TABLET
    row1.ad_group_bid_modifier = modifier1

    mock_search_response_page = MagicMock()
    mock_search_response_page.results = [row1]
    mock_googleads_service.search.return_value = iter([mock_search_response_page])

    try:
        main(
            mock_google_ads_client,
            mock_customer_id,
            mock_ad_group_id, # None
        )
    except Exception as e:
        pytest.fail(f"main function raised an exception: {e}")
