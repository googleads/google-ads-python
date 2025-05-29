import pytest
from unittest.mock import MagicMock, patch

from examples.advanced_operations.add_app_campaign import main

@patch("examples.advanced_operations.add_app_campaign.uuid4", return_value=MagicMock(hex="testuuid"))
def test_main_runs_successfully(mock_uuid4: MagicMock, mock_google_ads_client: MagicMock) -> None:
    """Tests that the main function runs without raising an exception."""
    mock_customer_id = "1234567890"

    # --- Mock service responses ---
    # CampaignBudgetService
    mock_budget_service = mock_google_ads_client.get_service("CampaignBudgetService")
    mock_budget_response = MagicMock()
    mock_budget_result = MagicMock()
    mock_budget_result.resource_name = "customers/1234567890/campaignBudgets/budget_testuuid"
    mock_budget_response.results = [mock_budget_result]
    mock_budget_service.mutate_campaign_budgets.return_value = mock_budget_response

    # CampaignService
    mock_campaign_service = mock_google_ads_client.get_service("CampaignService")
    mock_campaign_response = MagicMock()
    mock_campaign_result = MagicMock()
    mock_campaign_result.resource_name = "customers/1234567890/campaigns/campaign_testuuid"
    mock_campaign_response.results = [mock_campaign_result]
    mock_campaign_service.mutate_campaigns.return_value = mock_campaign_response

    # GeoTargetConstantService
    mock_geo_service = mock_google_ads_client.get_service("GeoTargetConstantService")
    mock_geo_service.geo_target_constant_path.side_effect = lambda x: f"geoTargetConstants/{x}"

    # GoogleAdsService (for language_constant_path)
    mock_googleads_service = mock_google_ads_client.get_service("GoogleAdsService")
    mock_googleads_service.language_constant_path.side_effect = lambda x: f"languageConstants/{x}"

    # CampaignCriterionService
    mock_campaign_criterion_service = mock_google_ads_client.get_service("CampaignCriterionService")
    mock_criterion_response = MagicMock()
    # Simulate multiple results for campaign criteria
    mock_criterion_result_loc1 = MagicMock()
    mock_criterion_result_loc1.resource_name = "criterion_loc1"
    mock_criterion_result_loc2 = MagicMock()
    mock_criterion_result_loc2.resource_name = "criterion_loc2"
    mock_criterion_result_lang1 = MagicMock()
    mock_criterion_result_lang1.resource_name = "criterion_lang1"
    mock_criterion_result_lang2 = MagicMock()
    mock_criterion_result_lang2.resource_name = "criterion_lang2"
    mock_criterion_response.results = [
        mock_criterion_result_loc1, 
        mock_criterion_result_loc2,
        mock_criterion_result_lang1,
        mock_criterion_result_lang2
    ]
    mock_campaign_criterion_service.mutate_campaign_criteria.return_value = mock_criterion_response

    # AdGroupService
    mock_ad_group_service = mock_google_ads_client.get_service("AdGroupService")
    mock_ad_group_response = MagicMock()
    mock_ad_group_result = MagicMock()
    mock_ad_group_result.resource_name = "customers/1234567890/adGroups/adgroup_testuuid"
    mock_ad_group_response.results = [mock_ad_group_result]
    mock_ad_group_service.mutate_ad_groups.return_value = mock_ad_group_response

    # AdGroupAdService
    mock_ad_group_ad_service = mock_google_ads_client.get_service("AdGroupAdService")
    mock_ad_group_ad_response = MagicMock()
    mock_ad_group_ad_result = MagicMock()
    mock_ad_group_ad_result.resource_name = "customers/1234567890/adGroupAds/ad_testuuid"
    mock_ad_group_ad_response.results = [mock_ad_group_ad_result]
    mock_ad_group_ad_service.mutate_ad_group_ads.return_value = mock_ad_group_ad_response

    # --- Mock enums used by the script ---
    mock_enums = mock_google_ads_client.enums
    mock_enums.BudgetDeliveryMethodEnum.STANDARD = "STANDARD"
    mock_enums.CampaignStatusEnum.PAUSED = "PAUSED"
    mock_enums.AdvertisingChannelTypeEnum.MULTI_CHANNEL = "MULTI_CHANNEL"
    mock_enums.AdvertisingChannelSubTypeEnum.APP_CAMPAIGN = "APP_CAMPAIGN"
    mock_enums.AppCampaignAppStoreEnum.GOOGLE_APP_STORE = "GOOGLE_APP_STORE"
    mock_enums.AppCampaignBiddingStrategyGoalTypeEnum.OPTIMIZE_INSTALLS_TARGET_INSTALL_COST = "OPTIMIZE_INSTALLS_TARGET_INSTALL_COST"
    mock_enums.AdGroupStatusEnum.ENABLED = "ENABLED"
    mock_enums.AdGroupAdStatusEnum.ENABLED = "ENABLED"
    
    # --- Mock types ---
    # Most types are simple containers, MagicMock default behavior is often sufficient.
    # For AdTextAsset, it's created and then its `text` attribute is set.
    # The default MagicMock returned by get_type will handle this.
    # mock_ad_text_asset = mock_google_ads_client.get_type("AdTextAsset")
    # If create_ad_text_asset returned something complex that was then used,
    # we would mock that type more specifically.

    try:
        main(
            mock_google_ads_client,
            mock_customer_id,
        )
    except Exception as e:
        pytest.fail(f"main function raised an exception: {e}")
