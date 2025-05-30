import pytest
from unittest.mock import MagicMock, patch

from examples.advanced_operations.add_responsive_search_ad_full import main

# Note: The script uses import uuid and then uuid.uuid4(). So we patch 'uuid.uuid4'
@patch("examples.advanced_operations.add_responsive_search_ad_full.uuid.uuid4", return_value=MagicMock(hex="testuuid"))
def test_main_runs_successfully(mock_uuid4: MagicMock, mock_google_ads_client: MagicMock) -> None:
    """Tests that the main function runs without raising an exception (no customizer)."""
    mock_customer_id = "123"
    mock_customizer_attribute_name = None

    # --- Mock services ---
    # CustomizerAttributeService (not used if customizer_attribute_name is None)
    # CustomerCustomizerService (not used if customizer_attribute_name is None)

    # CampaignBudgetService
    mock_budget_service = mock_google_ads_client.get_service("CampaignBudgetService")
    mock_budget_response = MagicMock()
    mock_budget_result = MagicMock()
    mock_budget_result.resource_name = f"customers/{mock_customer_id}/campaignBudgets/budget_testuuid"
    mock_budget_response.results = [mock_budget_result]
    mock_budget_service.mutate_campaign_budgets.return_value = mock_budget_response

    # CampaignService
    mock_campaign_service = mock_google_ads_client.get_service("CampaignService")
    mock_campaign_response = MagicMock()
    mock_campaign_result = MagicMock()
    mock_campaign_result.resource_name = f"customers/{mock_customer_id}/campaigns/campaign_testuuid"
    mock_campaign_response.results = [mock_campaign_result]
    mock_campaign_service.mutate_campaigns.return_value = mock_campaign_response

    # AdGroupService
    mock_ad_group_service = mock_google_ads_client.get_service("AdGroupService")
    mock_ad_group_response = MagicMock()
    mock_ad_group_result = MagicMock()
    mock_ad_group_result.resource_name = f"customers/{mock_customer_id}/adGroups/adgroup_testuuid"
    mock_ad_group_response.results = [mock_ad_group_result]
    mock_ad_group_service.mutate_ad_groups.return_value = mock_ad_group_response

    # AdGroupAdService
    mock_ad_group_ad_service = mock_google_ads_client.get_service("AdGroupAdService")
    mock_ad_response = MagicMock()
    mock_ad_result = MagicMock()
    mock_ad_result.resource_name = f"customers/{mock_customer_id}/adGroupAds/ad_testuuid"
    mock_ad_response.results = [mock_ad_result]
    mock_ad_group_ad_service.mutate_ad_group_ads.return_value = mock_ad_response

    # AdGroupCriterionService (for keywords)
    mock_criterion_service = mock_google_ads_client.get_service("AdGroupCriterionService")
    mock_criterion_response = MagicMock()
    # Assuming two keywords are created
    mock_criterion_result1 = MagicMock()
    mock_criterion_result1.resource_name = f"customers/{mock_customer_id}/adGroupCriteria/crit1_testuuid"
    mock_criterion_result2 = MagicMock()
    mock_criterion_result2.resource_name = f"customers/{mock_customer_id}/adGroupCriteria/crit2_testuuid"
    mock_criterion_response.results = [mock_criterion_result1, mock_criterion_result2]
    mock_criterion_service.mutate_ad_group_criteria.return_value = mock_criterion_response

    # GeoTargetConstantService
    mock_geo_service = mock_google_ads_client.get_service("GeoTargetConstantService")
    mock_geo_service.geo_target_constant_path.return_value = "geoTargetConstants/2840" # USA

    # GoogleAdsService (for paths like campaign_path in campaign criteria)
    mock_googleads_service = mock_google_ads_client.get_service("GoogleAdsService")
    mock_googleads_service.campaign_path.return_value = f"customers/{mock_customer_id}/campaigns/campaign_testuuid"
    mock_googleads_service.ad_group_path.return_value = f"customers/{mock_customer_id}/adGroups/adgroup_testuuid" # for ad customizer
    mock_googleads_service.customizer_attribute_path.return_value = f"customers/{mock_customer_id}/customizerAttributes/customizer_attr_testuuid" # for ad customizer


    # --- Mock enums ---
    mock_enums = mock_google_ads_client.enums
    # mock_enums.CustomizerAttributeTypeEnum.PRICE = "PRICE" # Not used in this path
    mock_enums.BudgetDeliveryMethodEnum.STANDARD = "STANDARD"
    mock_enums.AdvertisingChannelTypeEnum.SEARCH = "SEARCH"
    mock_enums.CampaignStatusEnum.PAUSED = "PAUSED"
    mock_enums.AdGroupStatusEnum.ENABLED = "ENABLED"
    mock_enums.AdGroupAdStatusEnum.ENABLED = "ENABLED" # Script uses ENABLED for AdGroupAd
    mock_enums.KeywordMatchTypeEnum.EXACT = "EXACT"
    mock_enums.KeywordMatchTypeEnum.BROAD = "BROAD" # Second keyword is BROAD
    mock_enums.ServedAssetFieldTypeEnum.HEADLINE_1 = "HEADLINE_1" # Used in ad customizer part, but won't be hit
    mock_enums.CriterionTypeEnum.LOCATION = "LOCATION" # For campaign criterion
    mock_enums.PositiveGeoTargetTypeEnum = MagicMock() # campaign criterion target type
    mock_enums.PositiveGeoTargetTypeEnum.DONT_CARE = "DONT_CARE" # campaign criterion target type
    mock_enums.LocationSourceTypeEnum = MagicMock() # campaign criterion location source
    mock_enums.LocationSourceTypeEnum.DOMAIN_LOCATION = "DOMAIN_LOCATION" # campaign criterion location source

    try:
        main(
            mock_google_ads_client,
            mock_customer_id,
            mock_customizer_attribute_name,
        )
    except Exception as e:
        pytest.fail(f"main function raised an exception: {e}")


@patch("examples.advanced_operations.add_responsive_search_ad_full.uuid.uuid4", return_value=MagicMock(hex="testuuid_custom"))
def test_main_with_customizer_runs_successfully(mock_uuid4_custom: MagicMock, mock_google_ads_client: MagicMock) -> None:
    """Tests that the main function runs without raising an exception (with customizer)."""
    mock_customer_id = "123"
    mock_customizer_attribute_name = "Price" # Enable customizer path

    # --- Mock services (includes Customizer services now) ---
    mock_customizer_attr_service = mock_google_ads_client.get_service("CustomizerAttributeService")
    mock_cust_attr_response = MagicMock()
    mock_cust_attr_result = MagicMock()
    # The script expects the resource_name to be accessible from results[0]
    mock_cust_attr_result.resource_name = f"customers/{mock_customer_id}/customizerAttributes/customizer_attr_testuuid_custom"
    mock_cust_attr_response.results = [mock_cust_attr_result]
    mock_customizer_attr_service.mutate_customizer_attributes.return_value = mock_cust_attr_response

    mock_customer_customizer_service = mock_google_ads_client.get_service("CustomerCustomizerService")
    mock_cust_cust_response = MagicMock()
    mock_cust_cust_result = MagicMock()
    mock_cust_cust_result.resource_name = f"customers/{mock_customer_id}/customerCustomizers/cust_cust_testuuid_custom"
    mock_cust_cust_response.results = [mock_cust_cust_result]
    mock_customer_customizer_service.mutate_customer_customizers.return_value = mock_cust_cust_response

    # AdCustomizerService (new service for this path)
    mock_ad_customizer_service = mock_google_ads_client.get_service("AdCustomizerService")
    mock_ad_customizer_response = MagicMock()
    mock_ad_customizer_result = MagicMock()
    mock_ad_customizer_result.resource_name = f"customers/{mock_customer_id}/adCustomizers/ad_customizer_testuuid_custom"
    mock_ad_customizer_response.results = [mock_ad_customizer_result]
    mock_ad_customizer_service.mutate_ad_customizers.return_value = mock_ad_customizer_response


    # Re-mock other services as in the first test, potentially with different UUIDs if names clash
    mock_budget_service = mock_google_ads_client.get_service("CampaignBudgetService")
    mock_budget_response = MagicMock()
    mock_budget_result = MagicMock()
    mock_budget_result.resource_name = f"customers/{mock_customer_id}/campaignBudgets/budget_testuuid_custom"
    mock_budget_response.results = [mock_budget_result]
    mock_budget_service.mutate_campaign_budgets.return_value = mock_budget_response

    mock_campaign_service = mock_google_ads_client.get_service("CampaignService")
    # ... (campaign, adgroup, adgroupad, adgroupcriterion, geo, googleads service mocks as above)
    mock_campaign_response = MagicMock()
    mock_campaign_result = MagicMock()
    mock_campaign_result.resource_name = f"customers/{mock_customer_id}/campaigns/campaign_testuuid_custom"
    mock_campaign_response.results = [mock_campaign_result]
    mock_campaign_service.mutate_campaigns.return_value = mock_campaign_response

    mock_ad_group_service = mock_google_ads_client.get_service("AdGroupService")
    mock_ad_group_response = MagicMock()
    mock_ad_group_result = MagicMock()
    mock_ad_group_result.resource_name = f"customers/{mock_customer_id}/adGroups/adgroup_testuuid_custom"
    mock_ad_group_response.results = [mock_ad_group_result]
    mock_ad_group_service.mutate_ad_groups.return_value = mock_ad_group_response

    mock_ad_group_ad_service = mock_google_ads_client.get_service("AdGroupAdService")
    mock_ad_response = MagicMock()
    mock_ad_result = MagicMock()
    mock_ad_result.resource_name = f"customers/{mock_customer_id}/adGroupAds/ad_testuuid_custom"
    mock_ad_response.results = [mock_ad_result] # The ad customizer part references this resource name
    mock_ad_group_ad_service.mutate_ad_group_ads.return_value = mock_ad_response

    mock_criterion_service = mock_google_ads_client.get_service("AdGroupCriterionService")
    mock_criterion_response = MagicMock()
    mock_criterion_result1 = MagicMock()
    mock_criterion_result1.resource_name = f"customers/{mock_customer_id}/adGroupCriteria/crit1_testuuid_custom"
    mock_criterion_result2 = MagicMock()
    mock_criterion_result2.resource_name = f"customers/{mock_customer_id}/adGroupCriteria/crit2_testuuid_custom"
    mock_criterion_response.results = [mock_criterion_result1, mock_criterion_result2]
    mock_criterion_service.mutate_ad_group_criteria.return_value = mock_criterion_response

    mock_geo_service = mock_google_ads_client.get_service("GeoTargetConstantService")
    mock_geo_service.geo_target_constant_path.return_value = "geoTargetConstants/2840"

    mock_googleads_service = mock_google_ads_client.get_service("GoogleAdsService")
    mock_googleads_service.campaign_path.return_value = f"customers/{mock_customer_id}/campaigns/campaign_testuuid_custom"
    # Path for ad customizer (ad_group_ad is needed)
    mock_googleads_service.ad_group_ad_path.return_value = f"customers/{mock_customer_id}/adGroupAds/ad_testuuid_custom"
    mock_googleads_service.customizer_attribute_path.return_value = f"customers/{mock_customer_id}/customizerAttributes/customizer_attr_testuuid_custom"


    # --- Mock enums (includes PRICE now) ---
    mock_enums = mock_google_ads_client.enums
    mock_enums.CustomizerAttributeTypeEnum.PRICE = "PRICE"
    mock_enums.BudgetDeliveryMethodEnum.STANDARD = "STANDARD"
    # ... (all other enums as in the first test)
    mock_enums.AdvertisingChannelTypeEnum.SEARCH = "SEARCH"
    mock_enums.CampaignStatusEnum.PAUSED = "PAUSED"
    mock_enums.AdGroupStatusEnum.ENABLED = "ENABLED"
    mock_enums.AdGroupAdStatusEnum.ENABLED = "ENABLED"
    mock_enums.KeywordMatchTypeEnum.EXACT = "EXACT"
    mock_enums.KeywordMatchTypeEnum.BROAD = "BROAD"
    mock_enums.ServedAssetFieldTypeEnum.HEADLINE_1 = "HEADLINE_1"
    mock_enums.CriterionTypeEnum.LOCATION = "LOCATION"
    mock_enums.PositiveGeoTargetTypeEnum = MagicMock()
    mock_enums.PositiveGeoTargetTypeEnum.DONT_CARE = "DONT_CARE"
    mock_enums.LocationSourceTypeEnum = MagicMock()
    mock_enums.LocationSourceTypeEnum.DOMAIN_LOCATION = "DOMAIN_LOCATION"


    try:
        main(
            mock_google_ads_client,
            mock_customer_id,
            mock_customizer_attribute_name, # "Price"
        )
    except Exception as e:
        pytest.fail(f"main function raised an exception: {e}")
