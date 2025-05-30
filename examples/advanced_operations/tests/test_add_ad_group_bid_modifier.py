import pytest
from unittest.mock import MagicMock

from examples.advanced_operations.add_ad_group_bid_modifier import main

def test_main_runs_successfully(mock_google_ads_client: MagicMock) -> None:
    """Tests that the main function runs without raising an exception."""
    mock_customer_id = "1234567890"
    mock_ad_group_id = "0987654321"
    mock_bid_modifier_value = 1.5

    # Mock services and their responses
    mock_ad_group_service = mock_google_ads_client.get_service("AdGroupService")
    mock_ad_group_service.ad_group_path.return_value = "customers/1234567890/adGroups/0987654321"

    mock_ad_group_bm_service = mock_google_ads_client.get_service("AdGroupBidModifierService")
    mock_mutate_response = MagicMock()
    mock_result = MagicMock()
    mock_result.resource_name = "mock_resource_name_ad_group_bid_modifier"
    mock_mutate_response.results = [mock_result]
    mock_ad_group_bm_service.mutate_ad_group_bid_modifiers.return_value = mock_mutate_response

    # Mock enums
    mock_device_enum = MagicMock()
    mock_device_enum.MOBILE = "MOBILE_DEVICE" # Or actual enum value if known/needed
    mock_google_ads_client.enums.DeviceEnum = mock_device_enum

    # Mock types
    # The get_type method in conftest returns a MagicMock by default.
    # We can configure its "create" attribute if necessary, but often not needed
    # if the "create" object is just passed to a service method.
    # mock_ad_group_bid_modifier_operation = mock_google_ads_client.get_type("AdGroupBidModifierOperation")
    # If specific attributes on ad_group_bid_modifier (the .create object) were accessed directly
    # in the script before being passed to the service, we'd mock them here.
    # e.g. mock_ad_group_bid_modifier_operation.create.some_attribute = "some_value"

    try:
        main(
            mock_google_ads_client,
            mock_customer_id,
            mock_ad_group_id,
            mock_bid_modifier_value,
        )
    except Exception as e:
        pytest.fail(f"main function raised an exception: {e}")
