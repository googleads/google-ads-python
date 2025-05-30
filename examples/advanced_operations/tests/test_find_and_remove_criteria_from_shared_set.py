import pytest
from unittest.mock import MagicMock

from examples.advanced_operations.find_and_remove_criteria_from_shared_set import main

def test_main_runs_successfully(mock_google_ads_client: MagicMock) -> None:
    """Tests that the main function runs without raising an exception."""
    mock_customer_id = "123"
    mock_campaign_id = "456" # This is used to find the shared set name

    # Mock GoogleAdsService for search (called twice)
    mock_googleads_service = mock_google_ads_client.get_service("GoogleAdsService")

    # Mock response for the first search (finding shared set ID)
    mock_search_response_shared_set = MagicMock()
    mock_row_shared_set = MagicMock()
    mock_row_shared_set.shared_set.id = "789012" # Shared set ID
    mock_row_shared_set.shared_set.name = f"Test Shared Set for Campaign {mock_campaign_id}"
    mock_search_response_shared_set.results = [mock_row_shared_set]

    # Mock response for the second search (finding shared criteria)
    mock_search_response_criteria = MagicMock()
    # Simulate two criteria found, one to keep, one to remove
    mock_row_criterion_to_remove = MagicMock()
    mock_row_criterion_to_remove.shared_criterion.resource_name = f"customers/{mock_customer_id}/sharedCriteria/789012~111"
    mock_row_criterion_to_remove.shared_criterion.type_ = mock_google_ads_client.enums.CriterionTypeEnum.KEYWORD
    mock_row_criterion_to_remove.shared_criterion.keyword.text = "keyword to remove"
    mock_row_criterion_to_remove.shared_criterion.keyword.match_type = mock_google_ads_client.enums.KeywordMatchTypeEnum.EXACT

    mock_row_criterion_to_keep = MagicMock()
    mock_row_criterion_to_keep.shared_criterion.resource_name = f"customers/{mock_customer_id}/sharedCriteria/789012~222"
    mock_row_criterion_to_keep.shared_criterion.type_ = mock_google_ads_client.enums.CriterionTypeEnum.KEYWORD
    mock_row_criterion_to_keep.shared_criterion.keyword.text = "keyword to keep" # Script removes based on "remove" in text
    mock_row_criterion_to_keep.shared_criterion.keyword.match_type = mock_google_ads_client.enums.KeywordMatchTypeEnum.BROAD

    mock_search_response_criteria.results = [mock_row_criterion_to_remove, mock_row_criterion_to_keep]

    # Configure side_effect for multiple search calls
    mock_googleads_service.search.side_effect = [
        iter([mock_search_response_shared_set]), # First call returns one page with one result
        iter([mock_search_response_criteria])  # Second call returns one page with two results
    ]

    # Mock SharedCriterionService for mutate_shared_criteria
    mock_shared_criterion_service = mock_google_ads_client.get_service("SharedCriterionService")
    mock_mutate_response = MagicMock()
    mock_removed_criterion_result = MagicMock()
    mock_removed_criterion_result.resource_name = f"customers/{mock_customer_id}/sharedCriteria/789012~111" # resource name of removed criterion
    mock_mutate_response.results = [mock_removed_criterion_result]
    mock_shared_criterion_service.mutate_shared_criteria.return_value = mock_mutate_response

    # Mock enums (CriterionTypeEnum is already on the client mock by default from conftest)
    # client.enums.CriterionTypeEnum.KEYWORD will work.
    # client.enums.KeywordMatchTypeEnum.EXACT and .BROAD will also work.
    # Ensure these enums are configured on the main mock_google_ads_client.enums if not already.
    # For this test, we access them via mock_google_ads_client.enums.CriterionTypeEnum which is fine.

    try:
        main(
            mock_google_ads_client,
            mock_customer_id,
            mock_campaign_id,
        )
    except Exception as e:
        pytest.fail(f"main function raised an exception: {e}")
