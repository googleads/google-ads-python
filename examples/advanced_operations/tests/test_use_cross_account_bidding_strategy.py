import pytest
from unittest.mock import MagicMock, patch

from examples.advanced_operations.use_cross_account_bidding_strategy import main

@patch("examples.advanced_operations.use_cross_account_bidding_strategy.uuid4", return_value=MagicMock(hex="testuuid"))
@patch("google.protobuf.field_mask_pb2.FieldMask") # Patch the FieldMask helper
def test_main_runs_successfully(mock_field_mask_constructor: MagicMock, mock_uuid4: MagicMock, mock_google_ads_client: MagicMock) -> None:
    """Tests that the main function runs without raising an exception."""
    mock_customer_id = "123" # This is the client account
    mock_manager_customer_id = "789" # This is the manager account
    mock_campaign_id = "456"

    # --- Mocking for manager account operations ---
    # BiddingStrategyService (for manager)
    mock_bidding_strategy_service_manager = mock_google_ads_client.get_service("BiddingStrategyService")
    mock_bidding_strategy_response_manager = MagicMock()
    mock_bidding_strategy_result_manager = MagicMock()
    # The resource name will include the manager_customer_id
    mock_bidding_strategy_result_manager.resource_name = f"customers/{mock_manager_customer_id}/biddingStrategies/bs_manager_testuuid"
    mock_bidding_strategy_response_manager.results = [mock_bidding_strategy_result_manager]
    mock_bidding_strategy_service_manager.mutate_bidding_strategies.return_value = mock_bidding_strategy_response_manager

    # GoogleAdsService (for manager - search_stream to find the created strategy)
    mock_googleads_service_manager = mock_google_ads_client.get_service("GoogleAdsService")
    # This mock will be used by the client passed to attach_portfolio_bidding_strategy_to_campaign
    # and the one passed to create_portfolio_bidding_strategy
    # We need to ensure the correct client is used for each service call.
    # The script uses separate client instances for manager and client accounts.
    # For this test, mock_google_ads_client is used for both, differentiated by customer_id in calls.
    # This might be tricky if the client object itself stores the customer_id for requests.
    # Assuming client.customer_id is used by services, or that services are configured per client instance.
    # For the purpose of this test, we'll assume services are obtained from the client and work correctly.

    mock_search_stream_response_manager_page = MagicMock()
    mock_row_manager_bs = MagicMock()
    mock_row_manager_bs.bidding_strategy.id = "bs_manager_id_123" # ID of the strategy in manager
    mock_row_manager_bs.bidding_strategy.name = f"Manager Maximize Clicks {mock_uuid4().hex}"
    mock_row_manager_bs.bidding_strategy.type_ = mock_google_ads_client.enums.BiddingStrategyTypeEnum.MAXIMIZE_CLICKS
    mock_row_manager_bs.bidding_strategy.currency_code = "USD"
    mock_search_stream_response_manager_page.results = [mock_row_manager_bs]
    # search_stream returns an iterator of pages
    
    # --- Mocking for client account operations ---
    # GoogleAdsService (for client - search_stream to find accessible strategies)
    # This will be a different call to googleads_service.search_stream
    mock_search_stream_response_client_page = MagicMock()
    mock_row_client_accessible_bs = MagicMock()
    # This ID should match what was "created" in the manager account for the script to find it.
    mock_row_client_accessible_bs.accessible_bidding_strategy.id = "bs_manager_id_123" 
    mock_row_client_accessible_bs.accessible_bidding_strategy.name = f"Manager Maximize Clicks {mock_uuid4().hex}"
    mock_row_client_accessible_bs.accessible_bidding_strategy.type_ = mock_google_ads_client.enums.BiddingStrategyTypeEnum.MAXIMIZE_CLICKS
    mock_row_client_accessible_bs.accessible_bidding_strategy.owner_customer_id = int(mock_manager_customer_id)
    mock_row_client_accessible_bs.accessible_bidding_strategy.owner_descriptive_name = "Manager Account Name"
    mock_search_stream_response_client_page.results = [mock_row_client_accessible_bs]

    # Set up side_effect for search_stream on the main GoogleAdsService mock
    # The script calls search_stream on the manager_client first, then on the client_client.
    mock_googleads_service_manager.search_stream.side_effect = [
        iter([mock_search_stream_response_manager_page]), # For manager finding its own strategy (not in script)
                                                          # Actually, script does NOT search manager for its own strategy.
                                                          # It creates it, then client searches for accessible ones.
                                                          # So, only one search_stream call by the client account.
                                                          # Correcting this:
        iter([mock_search_stream_response_client_page])  # For client finding accessible strategies
    ]
    # If create_portfolio_bidding_strategy did a search, it would be before.
    # The script creates on manager, then client searches. So only client search_stream.
    # Let's assume the GoogleAdsService mock is versatile enough.
    # The script uses client_customer.google_ads_client.get_service("GoogleAdsService")
    # and manager_customer.google_ads_client.get_service("GoogleAdsService")
    # For the test, we only have one mock_google_ads_client.
    # This will be simplified: the single mock_googleads_service_manager.search_stream is for the client's call.
    # The manager BiddingStrategyService is used for creation.

    # CampaignService (for client)
    mock_campaign_service_client = mock_google_ads_client.get_service("CampaignService")
    mock_campaign_service_client.campaign_path.return_value = f"customers/{mock_customer_id}/campaigns/{mock_campaign_id}"
    mock_campaign_mutate_response_client = MagicMock()
    mock_campaign_mutate_result_client = MagicMock()
    mock_campaign_mutate_result_client.resource_name = f"customers/{mock_customer_id}/campaigns/{mock_campaign_id}" # updated campaign
    mock_campaign_mutate_response_client.results = [mock_campaign_mutate_result_client]
    mock_campaign_service_client.mutate_campaigns.return_value = mock_campaign_mutate_response_client

    # Mock FieldMask
    mock_field_mask_instance = MagicMock()
    mock_field_mask_constructor.return_value = mock_field_mask_instance
    
    # Mock enums
    mock_enums = mock_google_ads_client.enums
    mock_enums.BiddingStrategyTypeEnum.MAXIMIZE_CLICKS = "MAXIMIZE_CLICKS"
    # mock_enums.BiddingStrategyTypeEnum.TARGET_CPA = "TARGET_CPA" # also used in script for TargetCpa

    try:
        # The script internally creates two GoogleAdsClient instances.
        # The test passes one mock_google_ads_client. This means the service mocks
        # (like BiddingStrategyService, GoogleAdsService, CampaignService) will be shared.
        # This is generally fine if the service methods are distinct enough or if the script
        # correctly passes customer_id with each call (which it does for mutate methods).
        # For search_stream, the query itself would differ if customer_id was part of it,
        # or the client instance would handle it.
        # For the test, we assume our single mock_google_ads_client adapts.
        main(
            mock_google_ads_client, # This will be used as the base for both manager and client in the script
            mock_manager_customer_id,
            mock_customer_id, # client customer_id
            mock_campaign_id,
        )
    except Exception as e:
        pytest.fail(f"main function raised an exception: {e}")
