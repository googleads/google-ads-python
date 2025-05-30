import pytest
from unittest.mock import MagicMock, patch

from examples.advanced_operations.add_dynamic_page_feed_asset import main

@patch("examples.utils.example_helpers.get_printable_datetime", return_value="2023-10-26 10:00:00")
def test_main_runs_successfully(mock_get_printable_datetime: MagicMock, mock_google_ads_client: MagicMock) -> None:
    """Tests that the main function runs without raising an exception."""
    mock_customer_id = "123"
    mock_campaign_id = "456"
    mock_ad_group_id = "789"

    # Mock GoogleAdsService for path helpers
    mock_googleads_service = mock_google_ads_client.get_service("GoogleAdsService")
    mock_googleads_service.asset_path.side_effect = lambda cid, aid: f"customers/{cid}/assets/{aid}"
    mock_googleads_service.asset_set_path.side_effect = lambda cid, asset_set_id: f"customers/{cid}/assetSets/{asset_set_id}"
    mock_googleads_service.campaign_path.side_effect = lambda cid, camp_id: f"customers/{cid}/campaigns/{camp_id}"
    mock_googleads_service.ad_group_path.side_effect = lambda cid, adg_id: f"customers/{cid}/adGroups/{adg_id}"


    # Mock AssetService
    mock_asset_service = mock_google_ads_client.get_service("AssetService")
    mock_asset_response = MagicMock()
    mock_asset_result = MagicMock()
    mock_asset_result.resource_name = "customers/123/assets/asset123"
    mock_asset_response.results = [mock_asset_result]
    mock_asset_service.mutate_assets.return_value = mock_asset_response

    # Mock AssetSetService
    mock_asset_set_service = mock_google_ads_client.get_service("AssetSetService")
    mock_asset_set_response = MagicMock()
    mock_asset_set_result = MagicMock()
    mock_asset_set_result.resource_name = "customers/123/assetSets/asset_set123"
    mock_asset_set_response.results = [mock_asset_set_result]
    mock_asset_set_service.mutate_asset_sets.return_value = mock_asset_set_response

    # Mock AssetSetAssetService
    mock_asset_set_asset_service = mock_google_ads_client.get_service("AssetSetAssetService")
    mock_asset_set_asset_response = MagicMock()
    mock_asset_set_asset_result = MagicMock()
    mock_asset_set_asset_result.resource_name = "customers/123/assetSetAssets/asset_set_asset123"
    mock_asset_set_asset_response.results = [mock_asset_set_asset_result]
    mock_asset_set_asset_service.mutate_asset_set_assets.return_value = mock_asset_set_asset_response

    # Mock CampaignAssetSetService
    mock_campaign_asset_set_service = mock_google_ads_client.get_service("CampaignAssetSetService")
    mock_campaign_asset_set_response = MagicMock()
    mock_campaign_asset_set_result = MagicMock()
    mock_campaign_asset_set_result.resource_name = "customers/123/campaignAssetSets/campaign_asset_set123"
    mock_campaign_asset_set_response.results = [mock_campaign_asset_set_result]
    mock_campaign_asset_set_service.mutate_campaign_asset_sets.return_value = mock_campaign_asset_set_response

    # Mock AdGroupCriterionService
    mock_ad_group_criterion_service = mock_google_ads_client.get_service("AdGroupCriterionService")
    mock_ad_group_criterion_response = MagicMock()
    mock_ad_group_criterion_result = MagicMock()
    mock_ad_group_criterion_result.resource_name = "customers/123/adGroupCriteria/ad_group_criterion123"
    mock_ad_group_criterion_response.results = [mock_ad_group_criterion_result]
    mock_ad_group_criterion_service.mutate_ad_group_criteria.return_value = mock_ad_group_criterion_response


    # Mock enums
    mock_enums = mock_google_ads_client.enums
    mock_enums.AssetSetTypeEnum.PAGE_FEED = "PAGE_FEED"
    mock_enums.AssetTypeEnum.PAGE_FEED = "PAGE_FEED" # Used when creating asset
    mock_enums.WebpageConditionOperandEnum.CUSTOM_LABEL = "CUSTOM_LABEL"
    mock_enums.WebpageConditionOperatorEnum.EQUALS = "EQUALS" # Used in WebpageConditionInfo

    try:
        main(
            mock_google_ads_client,
            mock_customer_id,
            mock_campaign_id,
            mock_ad_group_id,
        )
    except Exception as e:
        pytest.fail(f"main function raised an exception: {e}")
