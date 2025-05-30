import pytest
from unittest.mock import MagicMock, PropertyMock

@pytest.fixture
def mock_google_ads_client():
    """Fixture to mock the GoogleAdsClient."""
    mock_client = MagicMock()

    # Mock the get_service method
    # This will return a new MagicMock for any service name requested
    mock_client.get_service = MagicMock(return_value=MagicMock())

    # Mock the get_type method
    # This will return a new MagicMock for any type name requested
    # We can refine this later if specific type behaviors are needed
    mock_client.get_type = MagicMock(return_value=MagicMock())

    # Mock the enums attribute
    # This allows access like client.enums.SomeEnum.VALUE
    # For now, we'll make it a MagicMock. If specific enums are needed,
    # they can be added as properties to this mock_enums object.
    mock_enums = MagicMock()

    # Example of mocking a specific enum if needed for a test:
    # mock_campaign_status_enum = MagicMock()
    # mock_campaign_status_enum.PAUSED = "PAUSED_ENUM_VALUE" # Or an int if that's what the API uses
    # type(mock_enums).CampaignStatusEnum = PropertyMock(return_value=mock_campaign_status_enum)

    mock_client.enums = mock_enums

    return mock_client
