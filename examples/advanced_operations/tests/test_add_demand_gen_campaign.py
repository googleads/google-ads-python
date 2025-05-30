import pytest
from unittest.mock import MagicMock, patch

from examples.advanced_operations.add_demand_gen_campaign import main

@patch("examples.advanced_operations.add_demand_gen_campaign.uuid4", return_value=MagicMock(hex="testuuid"))
@patch("examples.utils.example_helpers.get_image_bytes_from_url", return_value=b"dummy_image_bytes")
def test_main_runs_successfully(
    mock_get_image_bytes: MagicMock, mock_uuid4: MagicMock, mock_google_ads_client: MagicMock
) -> None:
    """Tests that the main function runs without raising an exception."""
    mock_customer_id = "123"
    # The script uses manager_customer_id and account_customer_id, for this test we'll assume they are the same
    # as the customer_id unless specific cross-account logic needs to be tested.
    # For now, the example script itself doesn't seem to use manager_customer_id for any calls.
    mock_video_id = "video123"


    # Mock GoogleAdsService for path helpers and the main mutate
    mock_googleads_service = mock_google_ads_client.get_service("GoogleAdsService")
    mock_googleads_service.campaign_budget_path.side_effect = lambda cid, bid: f"customers/{cid}/campaignBudgets/{bid}"
    mock_googleads_service.campaign_path.side_effect = lambda cid, camp_id: f"customers/{cid}/campaigns/{camp_id}"
    mock_googleads_service.ad_group_path.side_effect = lambda cid, ag_id: f"customers/{cid}/adGroups/{ag_id}"
    mock_googleads_service.asset_path.side_effect = lambda cid, asset_id: f"customers/{cid}/assets/{asset_id}"

    # Mock the main mutate call
    mock_mutate_response = MagicMock()
    # For a batch job, response might have individual responses per operation.
    # Let's assume it has a list of MutateOperationResponse messages.
    # Each of these would have a field corresponding to the operation type,
    # e.g., campaign_budget_result, campaign_result etc.
    # For simplicity, we'll mock a generic response that doesn't cause errors.
    # If the script checks specific results, this needs to be more detailed.
    mock_op_response_budget = MagicMock()
    mock_op_response_budget.campaign_budget_result.resource_name = "customers/123/campaignBudgets/temp_budget_testuuid"
    mock_op_response_campaign = MagicMock()
    mock_op_response_campaign.campaign_result.resource_name = "customers/123/campaigns/temp_campaign_testuuid"
    # ... and so on for other operations (assets, ad group, ad group ad, campaign criterion)
    # The script creates 5 assets, 1 budget, 1 campaign, 1 ad group, 1 ad group ad, 1 campaign criterion
    # Total of 10 operations.
    mock_mutate_response.mutate_operation_responses = [
        MagicMock(asset_result=MagicMock(resource_name=f"asset_{i}")) for i in range(5)
    ]  # 5 Assets
    mock_mutate_response.mutate_operation_responses.append(mock_op_response_budget) # Budget
    mock_mutate_response.mutate_operation_responses.append(mock_op_response_campaign) # Campaign
    mock_mutate_response.mutate_operation_responses.append(MagicMock(ad_group_result=MagicMock(resource_name="ad_group_1"))) # Ad Group
    mock_mutate_response.mutate_operation_responses.append(MagicMock(ad_group_ad_result=MagicMock(resource_name="ad_group_ad_1"))) # Ad Group Ad
    mock_mutate_response.mutate_operation_responses.append(MagicMock(campaign_criterion_result=MagicMock(resource_name="campaign_criterion_1"))) # Campaign Criterion

    mock_googleads_service.mutate.return_value = mock_mutate_response

    # Mock SearchStream for finding existing assets (assumed not found for simplicity of this test)
    mock_search_response = MagicMock()
    mock_search_response.results = [] # No existing assets found
    mock_googleads_service.search_stream.return_value = [mock_search_response]


    # Mock enums
    mock_enums = mock_google_ads_client.enums
    mock_enums.BudgetDeliveryMethodEnum.STANDARD = "STANDARD"
    mock_enums.CampaignStatusEnum.PAUSED = "PAUSED"
    mock_enums.AdvertisingChannelTypeEnum.DEMAND_GEN = "DEMAND_GEN"
    mock_enums.BiddingStrategyTypeEnum.TARGET_CPA = "TARGET_CPA"
    mock_enums.AdGroupStatusEnum.ENABLED = "ENABLED"
    mock_enums.AssetTypeEnum.IMAGE = "IMAGE"
    mock_enums.AssetTypeEnum.TEXT = "TEXT" # Used for headlines/descriptions
    mock_enums.AssetTypeEnum.YOUTUBE_VIDEO = "YOUTUBE_VIDEO"
    mock_enums.PerformanceMaxUpgradeStatusEnum.UPGRADE_ELIGIBLE = "UPGRADE_ELIGIBLE" # for campaign.demand_gen_campaign
    mock_enums.LocationSourceEnum.GOOGLE_MY_BUSINESS = "GOOGLE_MY_BUSINESS" # for campaign.demand_gen_campaign
    mock_enums.CriterionTypeEnum.LANGUAGE = "LANGUAGE" # for campaign criterion
    mock_enums.LanguageInfo = MagicMock() # for campaign criterion language

    # Mock types
    # For the batch mutate, operations are created and added to a list.
    # e.g., client.get_type("CampaignBudgetOperation")
    # The default MagicMock returned by get_type should be sufficient.

    try:
        main(
            mock_google_ads_client,
            mock_customer_id, # customer_id
            # mock_customer_id, # manager_customer_id (assuming same for this test) # This was the incorrect argument
            mock_video_id
        )
    except Exception as e:
        pytest.fail(f"main function raised an exception: {e}")
