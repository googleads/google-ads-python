import pytest
from unittest.mock import MagicMock, patch

from examples.advanced_operations.add_performance_max_campaign import main

# Global temporary IDs used by the script
_BUDGET_TEMPORARY_ID = "-1"
_CAMPAIGN_TEMPORARY_ID = "-2"
_ASSET_GROUP_TEMPORARY_ID = "-3"


@patch("examples.advanced_operations.add_performance_max_campaign.uuid4", return_value=MagicMock(hex="testuuid"))
@patch("examples.utils.example_helpers.get_image_bytes_from_url", return_value=b"dummy_image_bytes")
def test_main_runs_successfully(
    mock_get_image_bytes: MagicMock, mock_uuid4: MagicMock, mock_google_ads_client: MagicMock
) -> None:
    """Tests that the main function runs without raising an exception."""
    mock_customer_id = "123"
    mock_audience_id = None # Test default path first
    mock_brand_guidelines_enabled = False

    # Mock GoogleAdsService for path helpers and the main mutate
    mock_googleads_service = mock_google_ads_client.get_service("GoogleAdsService")
    mock_googleads_service.campaign_budget_path.return_value = f"customers/{mock_customer_id}/campaignBudgets/{_BUDGET_TEMPORARY_ID}"
    mock_googleads_service.campaign_path.return_value = f"customers/{mock_customer_id}/campaigns/{_CAMPAIGN_TEMPORARY_ID}"
    mock_googleads_service.asset_group_path.return_value = f"customers/{mock_customer_id}/assetGroups/{_ASSET_GROUP_TEMPORARY_ID}"
    mock_googleads_service.asset_path.side_effect = lambda cid, aid: f"customers/{cid}/assets/{aid}" # Used for text assets
    # If audience_id is provided, this path is used.
    if mock_audience_id:
        mock_googleads_service.audience_path.return_value = f"customers/{mock_customer_id}/audiences/{mock_audience_id}"


    # Mock CampaignBudgetService (even though budget created via GoogleAdsService.mutate, path might be used)
    # The script uses googleads_service.campaign_budget_path, so direct service mock not strictly needed for path.
    # However, if it made calls like client.get_service("CampaignBudgetService").campaign_budget_path, this would be needed.

    # Mock CampaignService (similar to budget service, paths are via GoogleAdsService)
    # mock_campaign_service = mock_google_ads_client.get_service("CampaignService")

    # Mock AssetGroupService (paths via GoogleAdsService)
    # mock_asset_group_service = mock_google_ads_client.get_service("AssetGroupService")

    # Mock GeoTargetConstantService
    mock_geo_service = mock_google_ads_client.get_service("GeoTargetConstantService")
    mock_geo_service.geo_target_constant_path.return_value = "geoTargetConstants/2840" # USA

    # Mock the main GoogleAdsService.mutate call
    mock_mutate_response = MagicMock()
    # The script creates: 1 budget, 1 campaign, multiple assets (5 text, 5 image), 1 asset group,
    # multiple asset group assets, 1 campaign criterion.
    # The print_response_details function expects mutate_operation_responses.
    responses = []
    responses.append(MagicMock(campaign_budget_result=MagicMock(resource_name=f"customers/{mock_customer_id}/campaignBudgets/budget1")))
    responses.append(MagicMock(campaign_result=MagicMock(resource_name=f"customers/{mock_customer_id}/campaigns/campaign1")))
    # 10 assets (5 text, 5 image)
    for i in range(10):
        responses.append(MagicMock(asset_result=MagicMock(resource_name=f"customers/{mock_customer_id}/assets/asset{i}")))
    responses.append(MagicMock(asset_group_result=MagicMock(resource_name=f"customers/{mock_customer_id}/assetGroups/assetgroup1")))
    # 12 AssetGroupAssets (headlines, descriptions, images, logo, business name)
    for i in range(12):
         responses.append(MagicMock(asset_group_asset_result=MagicMock(resource_name=f"customers/{mock_customer_id}/assetGroupAssets/aga{i}")))
    responses.append(MagicMock(campaign_criterion_result=MagicMock(resource_name=f"customers/{mock_customer_id}/campaignCriteria/crit1")))
    if mock_audience_id:
        responses.append(MagicMock(asset_group_signal_result=MagicMock(resource_name=f"customers/{mock_customer_id}/assetGroupSignals/signal1")))

    mock_mutate_response.mutate_operation_responses = responses
    mock_googleads_service.mutate.return_value = mock_mutate_response

    # Mock enums
    mock_enums = mock_google_ads_client.enums
    mock_enums.BudgetDeliveryMethodEnum.STANDARD = "STANDARD"
    mock_enums.CampaignStatusEnum.PAUSED = "PAUSED"
    mock_enums.AdvertisingChannelTypeEnum.PERFORMANCE_MAX = "PERFORMANCE_MAX"
    mock_enums.BiddingStrategyTypeEnum.MAXIMIZE_CONVERSION_VALUE = "MAXIMIZE_CONVERSION_VALUE"
    mock_enums.AssetFieldTypeEnum.HEADLINE = "HEADLINE"
    mock_enums.AssetFieldTypeEnum.DESCRIPTION = "DESCRIPTION"
    mock_enums.AssetFieldTypeEnum.LONG_HEADLINE = "LONG_HEADLINE"
    mock_enums.AssetFieldTypeEnum.BUSINESS_NAME = "BUSINESS_NAME"
    mock_enums.AssetFieldTypeEnum.MARKETING_IMAGE = "MARKETING_IMAGE"
    mock_enums.AssetFieldTypeEnum.SQUARE_MARKETING_IMAGE = "SQUARE_MARKETING_IMAGE"
    mock_enums.AssetFieldTypeEnum.LOGO = "LOGO"
    mock_enums.AssetGroupStatusEnum.PAUSED = "PAUSED"
    mock_enums.AssetTypeEnum.TEXT = "TEXT" # For text assets created
    mock_enums.AssetTypeEnum.IMAGE = "IMAGE" # For image assets created
    mock_enums.CriterionTypeEnum.LOCATION = "LOCATION" # For campaign criterion
    mock_enums.ConversionGoalCampaignConfig = MagicMock() # For campaign.conversion_goal_setting
    mock_enums.ConversionGoalCampaignConfig.GoalConfigLevelEnum.CUSTOMER = "CUSTOMER"


    try:
        main(
            mock_google_ads_client,
            mock_customer_id,
            mock_audience_id,
            mock_brand_guidelines_enabled
        )
    except Exception as e:
        pytest.fail(f"main function raised an exception: {e}")

# It might be good to have a separate test for the audience_id path if logic significantly diverges.
@patch("examples.advanced_operations.add_performance_max_campaign.uuid4", return_value=MagicMock(hex="testuuid2")) # different uuid for different test
@patch("examples.utils.example_helpers.get_image_bytes_from_url", return_value=b"dummy_image_bytes_2")
def test_main_with_audience_runs_successfully(
    mock_get_image_bytes: MagicMock, mock_uuid4: MagicMock, mock_google_ads_client: MagicMock
) -> None:
    """Tests that the main function runs with an audience ID."""
    mock_customer_id = "123"
    mock_audience_id = "audience789" # Provide an audience ID
    mock_brand_guidelines_enabled = False # Can also test this variation

    # Similar mocking as above, but ensure audience_path is configured and response includes asset_group_signal_result
    mock_googleads_service = mock_google_ads_client.get_service("GoogleAdsService")
    mock_googleads_service.campaign_budget_path.return_value = f"customers/{mock_customer_id}/campaignBudgets/{_BUDGET_TEMPORARY_ID}"
    mock_googleads_service.campaign_path.return_value = f"customers/{mock_customer_id}/campaigns/{_CAMPAIGN_TEMPORARY_ID}"
    mock_googleads_service.asset_group_path.return_value = f"customers/{mock_customer_id}/assetGroups/{_ASSET_GROUP_TEMPORARY_ID}"
    mock_googleads_service.asset_path.side_effect = lambda cid, aid: f"customers/{cid}/assets/{aid}"
    mock_googleads_service.audience_path.return_value = f"customers/{mock_customer_id}/audiences/{mock_audience_id}"


    mock_geo_service = mock_google_ads_client.get_service("GeoTargetConstantService")
    mock_geo_service.geo_target_constant_path.return_value = "geoTargetConstants/2840"

    mock_mutate_response = MagicMock()
    responses = []
    responses.append(MagicMock(campaign_budget_result=MagicMock(resource_name=f"customers/{mock_customer_id}/campaignBudgets/budget2")))
    responses.append(MagicMock(campaign_result=MagicMock(resource_name=f"customers/{mock_customer_id}/campaigns/campaign2")))
    for i in range(10):
        responses.append(MagicMock(asset_result=MagicMock(resource_name=f"customers/{mock_customer_id}/assets/asset_aud_{i}")))
    responses.append(MagicMock(asset_group_result=MagicMock(resource_name=f"customers/{mock_customer_id}/assetGroups/assetgroup2")))
    for i in range(12):
         responses.append(MagicMock(asset_group_asset_result=MagicMock(resource_name=f"customers/{mock_customer_id}/assetGroupAssets/aga_aud_{i}")))
    responses.append(MagicMock(campaign_criterion_result=MagicMock(resource_name=f"customers/{mock_customer_id}/campaignCriteria/crit2")))
    responses.append(MagicMock(asset_group_signal_result=MagicMock(resource_name=f"customers/{mock_customer_id}/assetGroupSignals/signal2"))) # For audience signal

    mock_mutate_response.mutate_operation_responses = responses
    mock_googleads_service.mutate.return_value = mock_mutate_response

    mock_enums = mock_google_ads_client.enums
    mock_enums.BudgetDeliveryMethodEnum.STANDARD = "STANDARD"
    mock_enums.CampaignStatusEnum.PAUSED = "PAUSED"
    mock_enums.AdvertisingChannelTypeEnum.PERFORMANCE_MAX = "PERFORMANCE_MAX"
    mock_enums.BiddingStrategyTypeEnum.MAXIMIZE_CONVERSION_VALUE = "MAXIMIZE_CONVERSION_VALUE"
    mock_enums.AssetFieldTypeEnum.HEADLINE = "HEADLINE"
    # ... (include all other enums as in the first test) ...
    mock_enums.AssetFieldTypeEnum.DESCRIPTION = "DESCRIPTION"
    mock_enums.AssetFieldTypeEnum.LONG_HEADLINE = "LONG_HEADLINE"
    mock_enums.AssetFieldTypeEnum.BUSINESS_NAME = "BUSINESS_NAME"
    mock_enums.AssetFieldTypeEnum.MARKETING_IMAGE = "MARKETING_IMAGE"
    mock_enums.AssetFieldTypeEnum.SQUARE_MARKETING_IMAGE = "SQUARE_MARKETING_IMAGE"
    mock_enums.AssetFieldTypeEnum.LOGO = "LOGO"
    mock_enums.AssetGroupStatusEnum.PAUSED = "PAUSED"
    mock_enums.AssetTypeEnum.TEXT = "TEXT"
    mock_enums.AssetTypeEnum.IMAGE = "IMAGE"
    mock_enums.CriterionTypeEnum.LOCATION = "LOCATION"
    mock_enums.ConversionGoalCampaignConfig = MagicMock()
    mock_enums.ConversionGoalCampaignConfig.GoalConfigLevelEnum.CUSTOMER = "CUSTOMER"
    mock_enums.AudienceSignalTypeEnum.USER_LIST = "USER_LIST" # For asset group signal


    try:
        main(
            mock_google_ads_client,
            mock_customer_id,
            mock_audience_id, # With audience ID
            mock_brand_guidelines_enabled
        )
    except Exception as e:
        pytest.fail(f"main function raised an exception: {e}")
