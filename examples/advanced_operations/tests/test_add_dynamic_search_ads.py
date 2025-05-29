import pytest
from unittest.mock import MagicMock, patch

from examples.advanced_operations.add_dynamic_search_ads import main

@patch("examples.advanced_operations.add_dynamic_search_ads.uuid4", return_value=MagicMock(hex="testuuid"))
def test_main_runs_successfully(mock_uuid4: MagicMock, mock_google_ads_client: MagicMock) -> None:
    """Tests that the main function runs without raising an exception."""
    mock_customer_id = "123"

    # Mock CampaignBudgetService
    mock_budget_service = mock_google_ads_client.get_service("CampaignBudgetService")
    mock_budget_response = MagicMock()
    mock_budget_result = MagicMock()
    mock_budget_result.resource_name = f"customers/{mock_customer_id}/campaignBudgets/budget_testuuid"
    mock_budget_response.results = [mock_budget_result]
    mock_budget_service.mutate_campaign_budgets.return_value = mock_budget_response

    # Mock CampaignService
    mock_campaign_service = mock_google_ads_client.get_service("CampaignService")
    mock_campaign_response = MagicMock()
    mock_campaign_result = MagicMock()
    mock_campaign_result.resource_name = f"customers/{mock_customer_id}/campaigns/campaign_testuuid"
    mock_campaign_response.results = [mock_campaign_result]
    mock_campaign_service.mutate_campaigns.return_value = mock_campaign_response

    # Mock AdGroupService
    mock_ad_group_service = mock_google_ads_client.get_service("AdGroupService")
    mock_ad_group_response = MagicMock()
    mock_ad_group_result = MagicMock()
    mock_ad_group_result.resource_name = f"customers/{mock_customer_id}/adGroups/adgroup_testuuid"
    mock_ad_group_response.results = [mock_ad_group_result]
    mock_ad_group_service.mutate_ad_groups.return_value = mock_ad_group_response

    # Mock AdGroupAdService
    mock_ad_group_ad_service = mock_google_ads_client.get_service("AdGroupAdService")
    mock_ad_response = MagicMock()
    mock_ad_result = MagicMock()
    mock_ad_result.resource_name = f"customers/{mock_customer_id}/adGroupAds/ad_testuuid"
    mock_ad_response.results = [mock_ad_result]
    mock_ad_group_ad_service.mutate_ad_group_ads.return_value = mock_ad_response

    # Mock AdGroupCriterionService (for webpage targeting)
    mock_ad_group_criterion_service = mock_google_ads_client.get_service("AdGroupCriterionService")
    mock_criterion_response = MagicMock()
    mock_criterion_result = MagicMock()
    mock_criterion_result.resource_name = f"customers/{mock_customer_id}/adGroupCriteria/criterion_testuuid"
    mock_criterion_response.results = [mock_criterion_result]
    mock_ad_group_criterion_service.mutate_ad_group_criteria.return_value = mock_criterion_response
    
    # Mock GoogleAdsService for campaign_path (used in _create_campaign_level_targeting)
    mock_googleads_service = mock_google_ads_client.get_service("GoogleAdsService")
    mock_googleads_service.campaign_path.return_value = f"customers/{mock_customer_id}/campaigns/campaign_testuuid"


    # Mock enums
    mock_enums = mock_google_ads_client.enums
    mock_enums.BudgetDeliveryMethodEnum.STANDARD = "STANDARD"
    mock_enums.AdvertisingChannelTypeEnum.SEARCH = "SEARCH"
    mock_enums.CampaignStatusEnum.PAUSED = "PAUSED"
    mock_enums.BiddingStrategyTypeEnum.MANUAL_CPC = "MANUAL_CPC" # Used in campaign bidding strategy
    mock_enums.AdGroupTypeEnum.SEARCH_DYNAMIC_ADS = "SEARCH_DYNAMIC_ADS"
    mock_enums.AdGroupStatusEnum.PAUSED = "PAUSED"
    mock_enums.AdGroupAdStatusEnum.PAUSED = "PAUSED"
    mock_enums.AdGroupCriterionStatusEnum.PAUSED = "PAUSED" # For webpage criteria
    mock_enums.WebpageConditionOperandEnum.URL = "URL"
    mock_enums.WebpageConditionOperatorEnum.EQUALS = "EQUALS"
    mock_enums.CriterionTypeEnum.WEBPAGE = "WEBPAGE" # For AdGroupCriterion


    try:
        main(
            mock_google_ads_client,
            mock_customer_id,
        )
    except Exception as e:
        pytest.fail(f"main function raised an exception: {e}")
