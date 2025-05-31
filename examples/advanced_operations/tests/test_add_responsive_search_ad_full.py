import unittest
from unittest import mock
import sys

sys.path.insert(0, '/app') # For subtask environment

from examples.advanced_operations import add_responsive_search_ad_full

class TestAddResponsiveSearchAdFull(unittest.TestCase):

    def _setup_common_mocks(self, mock_google_ads_client):
        mock_google_ads_client.version = "v19"
        self.mock_objects = {}  # To store .create objects from operations
        self.ad_text_asset_mocks = [] # To store AdTextAsset mocks in order of creation
        self.suggest_geo_request_mocks = [] # To store SuggestGeoTargetConstantsRequest mocks

        # Mock Services
        services_to_mock = [
            "CustomizerAttributeService", "CustomerCustomizerService",
            "CampaignBudgetService", "CampaignService", "AdGroupService",
            "AdGroupAdService", "AdGroupCriterionService",
            "GeoTargetConstantService", "CampaignCriterionService"
        ]
        self.mocked_services = {}
        for service_name in services_to_mock:
            self.mocked_services[service_name] = mock.Mock(name=service_name)

        def get_service_side_effect(service_name, version=None):
            self.assertEqual("v19", version if version else mock_google_ads_client.version)
            if service_name in self.mocked_services:
                return self.mocked_services[service_name]
            self.fail(f"Unexpected service requested: {service_name}")
        mock_google_ads_client.get_service.side_effect = get_service_side_effect

        # Mock Enums (selected relevant enums)
        mock_google_ads_client.enums.BudgetDeliveryMethodEnum.STANDARD = "BUDGET_STANDARD"
        mock_google_ads_client.enums.CampaignStatusEnum.PAUSED = "CAMPAIGN_PAUSED"
        mock_google_ads_client.enums.AdvertisingChannelTypeEnum.SEARCH = "SEARCH_CHANNEL"
        # Script sets AdGroup status to ENABLED
        ad_group_status_enum_mock = mock.Mock()
        ad_group_status_enum_mock.ENABLED = "ADGROUP_ENABLED"
        ad_group_status_enum_mock.PAUSED = "ADGROUP_PAUSED"
        mock_google_ads_client.enums.AdGroupStatusEnum = ad_group_status_enum_mock
        # Script sets AdGroupAd status to ENABLED
        ad_group_ad_status_enum_mock = mock.Mock()
        ad_group_ad_status_enum_mock.ENABLED = "ADGROUPAD_ENABLED"
        ad_group_ad_status_enum_mock.PAUSED = "ADGROUPAD_PAUSED"
        mock_google_ads_client.enums.AdGroupAdStatusEnum = ad_group_ad_status_enum_mock
        mock_google_ads_client.enums.KeywordMatchTypeEnum.BROAD = "KEYWORD_BROAD"
        mock_google_ads_client.enums.KeywordMatchTypeEnum.PHRASE = "KEYWORD_PHRASE"
        mock_google_ads_client.enums.KeywordMatchTypeEnum.EXACT = "KEYWORD_EXACT"
        # Script uses PRICE for customizer type
        customizer_type_enum_mock = mock.Mock()
        customizer_type_enum_mock.PRICE = "CUSTOMIZER_PRICE"
        customizer_type_enum_mock.TEXT = "CUSTOMIZER_TEXT" # Keep if other parts use it
        mock_google_ads_client.enums.CustomizerAttributeTypeEnum = customizer_type_enum_mock
        mock_google_ads_client.enums.ServedAssetFieldTypeEnum.HEADLINE_1 = "SERVED_HEADLINE_1"
        mock_google_ads_client.enums.ServedAssetFieldTypeEnum.HEADLINE_2 = "SERVED_HEADLINE_2"
        mock_google_ads_client.enums.ServedAssetFieldTypeEnum.HEADLINE_3 = "SERVED_HEADLINE_3"
        mock_google_ads_client.enums.ServedAssetFieldTypeEnum.DESCRIPTION_1 = "SERVED_DESCRIPTION_1"
        mock_google_ads_client.enums.ServedAssetFieldTypeEnum.DESCRIPTION_2 = "SERVED_DESCRIPTION_2"
        mock_google_ads_client.enums.CriterionTypeEnum.LOCATION = "CRITERION_LOCATION"
        # Script uses AdGroupCriterionStatusEnum.ENABLED
        ad_group_criterion_status_enum_mock = mock.Mock()
        ad_group_criterion_status_enum_mock.ENABLED = "ADGROUPCRITERION_ENABLED"
        mock_google_ads_client.enums.AdGroupCriterionStatusEnum = ad_group_criterion_status_enum_mock


        def get_type_side_effect(type_name, version=None):
            mock_op_suffix = "_Operation"
            create_obj_suffix = "_CreateObject"

            if type_name.endswith("Operation"):
                mock_op = mock.Mock(name=f"{type_name}")
                base_type_name = type_name.replace("Operation", "")
                mock_create_obj = mock.Mock(name=f"{base_type_name}{create_obj_suffix}")
                mock_op.create = mock_create_obj
                self.mock_objects[base_type_name] = mock_create_obj

                # Pre-create nested structures based on script usage
                if base_type_name == "Campaign":
                    mock_create_obj.network_settings = mock.Mock(name="NetworkSettings")
                    mock_create_obj.target_spend = mock.Mock(name="TargetSpend") # Script uses target_spend
                elif base_type_name == "AdGroupAd":
                    ad_mock = mock.Mock(name="Ad")
                    ad_mock.responsive_search_ad = mock.Mock(name="ResponsiveSearchAdInfo")
                    ad_mock.responsive_search_ad.headlines = []
                    ad_mock.responsive_search_ad.descriptions = []
                    ad_mock.final_urls = [] # Initialize as list
                    mock_create_obj.ad = ad_mock
                elif base_type_name == "AdGroupCriterion": # For keywords
                    mock_create_obj.keyword = mock.Mock(name="KeywordInfo")
                elif base_type_name == "CampaignCriterion": # For geo-targeting
                    mock_create_obj.location = mock.Mock(name="LocationInfo")
                elif base_type_name == "CustomerCustomizer": # For customizers
                    mock_create_obj.value = mock.Mock(name="CustomizerValue") # Corrected from customizer_value

                return mock_op
            elif type_name == "AdTextAsset":
                asset_mock = mock.Mock(name=f"AdTextAsset_{len(self.ad_text_asset_mocks)+1}")
                self.ad_text_asset_mocks.append(asset_mock)
                return asset_mock
            elif type_name == "SuggestGeoTargetConstantsRequest":
                req_mock = mock.Mock(name=f"SuggestGeoRequest_{len(self.suggest_geo_request_mocks)+1}")
                # Mock the location_names.names structure
                req_mock.location_names = mock.Mock()
                req_mock.location_names.names = [] # This is the list to extend
                req_mock.country_code = ""
                self.suggest_geo_request_mocks.append(req_mock)
                return req_mock

            self.fail(f"Unexpected type requested: {type_name}")
        mock_google_ads_client.get_type.side_effect = get_type_side_effect


    def _configure_service_mutate_responses(self, customer_id, has_customizer=False):
        # Budget
        self.mocked_services["CampaignBudgetService"].mutate_campaign_budgets.return_value = mock.Mock(
            results=[mock.Mock(resource_name=f"customers/{customer_id}/campaignBudgets/budgetRSA")]
        )
        # Campaign
        self.mocked_services["CampaignService"].mutate_campaigns.return_value = mock.Mock(
            results=[mock.Mock(resource_name=f"customers/{customer_id}/campaigns/campaignRSA")]
        )
        # AdGroup
        self.mocked_services["AdGroupService"].mutate_ad_groups.return_value = mock.Mock(
            results=[mock.Mock(resource_name=f"customers/{customer_id}/adGroups/adGroupRSA")]
        )
        # AdGroupAd
        self.mocked_services["AdGroupAdService"].mutate_ad_group_ads.return_value = mock.Mock(
            results=[mock.Mock(resource_name=f"customers/{customer_id}/adGroupAds/adRSA")]
        )
        # AdGroupCriteria (Keywords) - script creates 3 keywords
        self.mocked_services["AdGroupCriterionService"].mutate_ad_group_criteria.return_value = mock.Mock(
            results=[
                mock.Mock(resource_name=f"customers/{customer_id}/adGroupCriteria/keyword1"),
                mock.Mock(resource_name=f"customers/{customer_id}/adGroupCriteria/keyword2"),
                mock.Mock(resource_name=f"customers/{customer_id}/adGroupCriteria/keyword3"),
            ]
        )
        # GeoTargetConstantService - suggest (script uses 3 locations)
        geo_suggestion1 = mock.Mock()
        geo_suggestion1.geo_target_constant = mock.Mock() # Ensure geo_target_constant itself is a mock
        geo_suggestion1.geo_target_constant.resource_name = "geoTargetConstants/mockId1" # Use mock IDs
        geo_suggestion1.locale = add_responsive_search_ad_full.LOCALE
        geo_suggestion1.reach = 1000
        geo_suggestion1.search_term = add_responsive_search_ad_full.GEO_LOCATION_1

        geo_suggestion2 = mock.Mock()
        geo_suggestion2.geo_target_constant = mock.Mock()
        geo_suggestion2.geo_target_constant.resource_name = "geoTargetConstants/mockId2"
        geo_suggestion2.locale = add_responsive_search_ad_full.LOCALE
        geo_suggestion2.reach = 2000
        geo_suggestion2.search_term = add_responsive_search_ad_full.GEO_LOCATION_2

        geo_suggestion3 = mock.Mock()
        geo_suggestion3.geo_target_constant = mock.Mock()
        geo_suggestion3.geo_target_constant.resource_name = "geoTargetConstants/mockId3"
        geo_suggestion3.locale = add_responsive_search_ad_full.LOCALE
        geo_suggestion3.reach = 3000
        geo_suggestion3.search_term = add_responsive_search_ad_full.GEO_LOCATION_3

        mock_geo_response = mock.Mock()
        mock_geo_response.geo_target_constant_suggestions = [geo_suggestion1, geo_suggestion2, geo_suggestion3]
        self.mocked_services["GeoTargetConstantService"].suggest_geo_target_constants.return_value = mock_geo_response

        # CampaignCriterionService (Geo-targeting) - script adds up to 3 locations
        self.mocked_services["CampaignCriterionService"].mutate_campaign_criteria.return_value = mock.Mock(
             results=[
                mock.Mock(resource_name=f"customers/{customer_id}/campaignCriteria/geo1"),
                mock.Mock(resource_name=f"customers/{customer_id}/campaignCriteria/geo2"),
                mock.Mock(resource_name=f"customers/{customer_id}/campaignCriteria/geo3"),
            ]
        )

        if has_customizer:
            self.mocked_services["CustomizerAttributeService"].mutate_customizer_attributes.return_value = mock.Mock(
                results=[mock.Mock(resource_name=f"customers/{customer_id}/customizerAttributes/customizerAttr1")]
            )
            self.mocked_services["CustomerCustomizerService"].mutate_customer_customizers.return_value = mock.Mock(
                results=[mock.Mock(resource_name=f"customers/{customer_id}/customerCustomizers/customerCustomizer1")]
            )

    def _assert_budget_campaign_adgroup_common(self, customer_id):
        # Budget
        self.mocked_services["CampaignBudgetService"].mutate_campaign_budgets.assert_called_once()
        budget_obj = self.mock_objects.get("CampaignBudget")
        self.assertEqual(budget_obj.delivery_method, "BUDGET_STANDARD")
        self.assertEqual(budget_obj.amount_micros, 500000) # Script uses 500,000

        # Campaign
        self.mocked_services["CampaignService"].mutate_campaigns.assert_called_once()
        campaign_obj = self.mock_objects.get("Campaign")
        self.assertEqual(campaign_obj.status, "CAMPAIGN_PAUSED")
        self.assertEqual(campaign_obj.advertising_channel_type, "SEARCH_CHANNEL")
        self.assertTrue(campaign_obj.network_settings.target_google_search)
        self.assertEqual(campaign_obj.target_spend.target_spend_micros, 0) # Script uses 0

        # AdGroup
        self.mocked_services["AdGroupService"].mutate_ad_groups.assert_called_once()
        ad_group_obj = self.mock_objects.get("AdGroup")
        self.assertEqual(ad_group_obj.status, "ADGROUP_ENABLED") # Script uses ENABLED

    @mock.patch("examples.advanced_operations.add_responsive_search_ad_full.GoogleAdsClient.load_from_storage")
    def test_main_without_customizer(self, mock_load_from_storage):
        mock_google_ads_client = mock.Mock()
        self._setup_common_mocks(mock_google_ads_client)
        customer_id = "custRSA_no_customizer"
        self._configure_service_mutate_responses(customer_id, has_customizer=False)

        add_responsive_search_ad_full.main(mock_google_ads_client, customer_id, None) # No customizer_attribute_name

        self._assert_budget_campaign_adgroup_common(customer_id)

        # AdGroupAd (RSA)
        self.mocked_services["AdGroupAdService"].mutate_ad_group_ads.assert_called_once()
        ad_group_ad_obj = self.mock_objects.get("AdGroupAd")
        self.assertEqual(ad_group_ad_obj.status, "ADGROUPAD_ENABLED") # Script uses ENABLED
        rsa_info = ad_group_ad_obj.ad.responsive_search_ad
        self.assertIn("https://www.example.com/", ad_group_ad_obj.ad.final_urls) # Script adds trailing /
        self.assertGreaterEqual(len(rsa_info.headlines), 3)
        self.assertTrue(any(h.text == "Headline 1 testing" for h in rsa_info.headlines))
        self.assertGreaterEqual(len(rsa_info.descriptions), 2)
        self.assertTrue(any(d.text == "Desc 2 testing" for d in rsa_info.descriptions)) # Default without customizer

        # Keywords
        self.assertEqual(self.mocked_services["AdGroupCriterionService"].mutate_ad_group_criteria.call_count, 1)
        # Geo-targeting
        self.mocked_services["GeoTargetConstantService"].suggest_geo_target_constants.assert_called_once()
        suggest_request_mock = self.suggest_geo_request_mocks[0]
        self.assertIn(add_responsive_search_ad_full.GEO_LOCATION_1, suggest_request_mock.location_names.names)
        self.assertIn(add_responsive_search_ad_full.GEO_LOCATION_2, suggest_request_mock.location_names.names)
        self.assertIn(add_responsive_search_ad_full.GEO_LOCATION_3, suggest_request_mock.location_names.names)
        self.assertEqual(suggest_request_mock.locale, add_responsive_search_ad_full.LOCALE)
        self.assertEqual(suggest_request_mock.country_code, add_responsive_search_ad_full.COUNTRY_CODE)
        self.assertEqual(self.mocked_services["CampaignCriterionService"].mutate_campaign_criteria.call_count, 1)

        # Customizer services should not be called
        self.mocked_services["CustomizerAttributeService"].mutate_customizer_attributes.assert_not_called()
        self.mocked_services["CustomerCustomizerService"].mutate_customer_customizers.assert_not_called()

    @mock.patch("examples.advanced_operations.add_responsive_search_ad_full.GoogleAdsClient.load_from_storage")
    def test_main_with_customizer(self, mock_load_from_storage):
        mock_google_ads_client = mock.Mock()
        self._setup_common_mocks(mock_google_ads_client)
        customer_id = "custRSA_with_customizer"
        customizer_attr_name = "TestRSAStrings" # Script uses this as base for customizer value
        self._configure_service_mutate_responses(customer_id, has_customizer=True)

        # Expected resource name for customizer attribute, used in description
        expected_customizer_attr_rn = f"customers/{customer_id}/customizerAttributes/customizerAttr1"

        add_responsive_search_ad_full.main(mock_google_ads_client, customer_id, customizer_attr_name)

        self._assert_budget_campaign_adgroup_common(customer_id)

        # CustomizerAttributeService
        self.mocked_services["CustomizerAttributeService"].mutate_customizer_attributes.assert_called_once()
        customizer_attr_obj = self.mock_objects.get("CustomizerAttribute")
        self.assertEqual(customizer_attr_obj.name, customizer_attr_name)
        self.assertEqual(customizer_attr_obj.type_, "CUSTOMIZER_PRICE") # Script uses PRICE

        # CustomerCustomizerService
        self.mocked_services["CustomerCustomizerService"].mutate_customer_customizers.assert_called_once()
        customer_customizer_obj = self.mock_objects.get("CustomerCustomizer")
        self.assertEqual(customer_customizer_obj.customizer_attribute, expected_customizer_attr_rn)
        self.assertEqual(customer_customizer_obj.value.type_, "CUSTOMIZER_PRICE") # Script uses PRICE
        self.assertEqual(customer_customizer_obj.value.string_value, "100USD") # Script uses "100USD"

        # AdGroupAd (RSA) - check customizer in description
        self.mocked_services["AdGroupAdService"].mutate_ad_group_ads.assert_called_once()
        ad_group_ad_obj = self.mock_objects.get("AdGroupAd")
        rsa_info = ad_group_ad_obj.ad.responsive_search_ad
        # Script format uses the customizer_attribute_NAME, not resource_name, in the placeholder.
        expected_customizer_desc_text = f"Just {{CUSTOMIZER.{customizer_attr_name}:10USD}}" # Corrected
        self.assertTrue(any(desc.text == expected_customizer_desc_text for desc in rsa_info.descriptions))

        # Keywords & Geo
        self.assertEqual(self.mocked_services["AdGroupCriterionService"].mutate_ad_group_criteria.call_count, 1)
        self.mocked_services["GeoTargetConstantService"].suggest_geo_target_constants.assert_called_once()
        self.assertEqual(self.mocked_services["CampaignCriterionService"].mutate_campaign_criteria.call_count, 1)


if __name__ == '__main__':
    unittest.main()
