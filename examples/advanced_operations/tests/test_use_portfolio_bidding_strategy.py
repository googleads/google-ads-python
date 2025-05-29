import pytest
from unittest.mock import MagicMock, patch

# Note: The script uses "import uuid" and then "uuid.uuid4()"
from examples.advanced_operations.use_portfolio_bidding_strategy import main

@patch("examples.advanced_operations.use_portfolio_bidding_strategy.uuid.uuid4", return_value=MagicMock(hex="testuuid"))
def test_main_runs_successfully(mock_uuid4: MagicMock, mock_google_ads_client: MagicMock) -> None:
    """Tests that the main function runs without raising an exception."""
    mock_customer_id = "123"
    # The script creates two campaigns, so we'll need resource names for them.
    mock_campaign_id_1 = "456001"
    mock_campaign_id_2 = "456002" # Script uses same ID with different suffix, but test needs unique if checked
                                 # Script actually uses same campaign_resource_name for both operations,
                                 # which is fine if it's just updating the same campaign twice with different strategies.
                                 # Re-reading: creates ONE campaign, then updates it.

    # Mock CampaignBudgetService
    mock_budget_service = mock_google_ads_client.get_service("CampaignBudgetService")
    mock_budget_response = MagicMock()
    mock_budget_result = MagicMock()
    mock_budget_result.resource_name = f"customers/{mock_customer_id}/campaignBudgets/budget_testuuid"
    mock_budget_response.results = [mock_budget_result]
    mock_budget_service.mutate_campaign_budgets.return_value = mock_budget_response

    # Mock BiddingStrategyService (for portfolio strategy)
    mock_bidding_strategy_service = mock_google_ads_client.get_service("BiddingStrategyService")
    mock_bidding_strategy_response = MagicMock()
    mock_bidding_strategy_result = MagicMock()
    mock_bidding_strategy_result.resource_name = f"customers/{mock_customer_id}/biddingStrategies/bs_testuuid"
    mock_bidding_strategy_response.results = [mock_bidding_strategy_result]
    mock_bidding_strategy_service.mutate_bidding_strategies.return_value = mock_bidding_strategy_response

    # Mock CampaignService
    mock_campaign_service = mock_google_ads_client.get_service("CampaignService")
    # This service is mutated twice: once to create the campaign, once to update it.
    # Create campaign response
    mock_campaign_create_response = MagicMock()
    mock_campaign_create_result = MagicMock()
    mock_campaign_create_result.resource_name = f"customers/{mock_customer_id}/campaigns/{mock_campaign_id_1}"
    mock_campaign_create_response.results = [mock_campaign_create_result]
    
    # Update campaign response
    mock_campaign_update_response = MagicMock()
    mock_campaign_update_result = MagicMock()
    mock_campaign_update_result.resource_name = f"customers/{mock_customer_id}/campaigns/{mock_campaign_id_1}" # Same campaign
    mock_campaign_update_response.results = [mock_campaign_update_result]

    mock_campaign_service.mutate_campaigns.side_effect = [
        mock_campaign_create_response,
        mock_campaign_update_response
    ]
    # Path helper for campaign
    mock_campaign_service.campaign_path.return_value = f"customers/{mock_customer_id}/campaigns/{mock_campaign_id_1}"


    # Mock enums
    mock_enums = mock_google_ads_client.enums
    mock_enums.BudgetDeliveryMethodEnum.STANDARD = "STANDARD"
    mock_enums.AdvertisingChannelTypeEnum.SEARCH = "SEARCH"
    mock_enums.CampaignStatusEnum.PAUSED = "PAUSED"
    mock_enums.BiddingStrategyTypeEnum.MANUAL_CPC = "MANUAL_CPC" # Used in initial campaign creation
    mock_enums.BiddingStrategyTypeEnum.TARGET_SPEND = "TARGET_SPEND" # Portfolio strategy type

    try:
        main(
            mock_google_ads_client,
            mock_customer_id,
        )
    except Exception as e:
        pytest.fail(f"main function raised an exception: {e}")
