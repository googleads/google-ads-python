import pytest
from unittest.mock import MagicMock, patch

# Note: The script uses "import uuid" and then "uuid.uuid4()"
from examples.advanced_operations.create_and_attach_shared_keyword_set import main

@patch("examples.advanced_operations.create_and_attach_shared_keyword_set.uuid.uuid4", return_value=MagicMock(hex="testuuid"))
def test_main_runs_successfully(mock_uuid4: MagicMock, mock_google_ads_client: MagicMock) -> None:
    """Tests that the main function runs without raising an exception."""
    mock_customer_id = "123"
    mock_campaign_id = "456"

    # Mock CampaignService for campaign_path
    mock_campaign_service_path_helper = mock_google_ads_client.get_service("CampaignService")
    mock_campaign_service_path_helper.campaign_path.return_value = f"customers/{mock_customer_id}/campaigns/{mock_campaign_id}"

    # Mock SharedSetService
    mock_shared_set_service = mock_google_ads_client.get_service("SharedSetService")
    mock_shared_set_response = MagicMock()
    mock_shared_set_result = MagicMock()
    mock_shared_set_result.resource_name = f"customers/{mock_customer_id}/sharedSets/shared_set_testuuid"
    mock_shared_set_response.results = [mock_shared_set_result]
    mock_shared_set_service.mutate_shared_sets.return_value = mock_shared_set_response

    # Mock SharedCriterionService
    mock_shared_criterion_service = mock_google_ads_client.get_service("SharedCriterionService")
    mock_shared_criterion_response = MagicMock()
    # Assuming 3 keywords are added to the shared set
    mock_shared_criterion_results = [MagicMock(resource_name=f"customers/{mock_customer_id}/sharedCriteria/sc_{i}_testuuid") for i in range(3)]
    mock_shared_criterion_response.results = mock_shared_criterion_results
    mock_shared_criterion_service.mutate_shared_criteria.return_value = mock_shared_criterion_response

    # Mock CampaignSharedSetService
    mock_campaign_shared_set_service = mock_google_ads_client.get_service("CampaignSharedSetService")
    mock_campaign_shared_set_response = MagicMock()
    mock_campaign_shared_set_result = MagicMock()
    mock_campaign_shared_set_result.resource_name = f"customers/{mock_customer_id}/campaignSharedSets/css_testuuid"
    mock_campaign_shared_set_response.results = [mock_campaign_shared_set_result]
    mock_campaign_shared_set_service.mutate_campaign_shared_sets.return_value = mock_campaign_shared_set_response

    # Mock enums
    mock_enums = mock_google_ads_client.enums
    mock_enums.SharedSetTypeEnum.NEGATIVE_KEYWORDS = "NEGATIVE_KEYWORDS"
    mock_enums.KeywordMatchTypeEnum.BROAD = "BROAD"
    # The script also defines KeywordMatchTypeEnum.EXACT and .PHRASE but doesn't seem to use them in the example keywords.

    try:
        main(
            mock_google_ads_client,
            mock_customer_id,
            mock_campaign_id,
        )
    except Exception as e:
        pytest.fail(f"main function raised an exception: {e}")
