import unittest
from unittest.mock import patch, Mock, call, ANY
import io
import sys
from types import SimpleNamespace
import datetime # Real datetime module for creating fixed datetime objects

# SUT (System Under Test)
from examples.remarketing import add_merchant_center_dynamic_remarketing_campaign

class TestUploadImageAsset(unittest.TestCase):
    @patch('examples.remarketing.add_merchant_center_dynamic_remarketing_campaign.requests.get')
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_upload_image_asset_success(self, mock_stdout, mock_requests_get):
        mock_client = Mock(name="GoogleAdsClient")
        mock_asset_service = Mock(name="AssetService")
        mock_client.get_service.return_value = mock_asset_service

        mock_asset_operation = Mock(name="AssetOperation")
        mock_asset = Mock(name="Asset")
        mock_image_asset_data_obj = Mock(name="ImageAssetData")

        mock_asset.image_asset = mock_image_asset_data_obj
        mock_asset_operation.create = mock_asset

        mock_client.get_type.return_value = mock_asset_operation

        mock_client.enums = SimpleNamespace(
            AssetTypeEnum=SimpleNamespace(IMAGE="MOCK_IMAGE_ASSET_TYPE")
        )

        mock_response_requests = Mock()
        mock_response_requests.content = b"dummy_image_bytes"
        mock_requests_get.return_value = mock_response_requests

        mock_mutate_assets_response = Mock()
        mock_asset_result = Mock()
        mock_asset_result.resource_name = "mock_asset_resource_name_123"
        mock_mutate_assets_response.results = [mock_asset_result]
        mock_asset_service.mutate_assets.return_value = mock_mutate_assets_response

        test_customer_id = "customer_id_abc"
        test_image_url = "http://dummyurl.com/img.png"
        test_asset_name = "Test Image Asset"

        returned_resource_name = add_merchant_center_dynamic_remarketing_campaign.upload_image_asset(
            mock_client, test_customer_id, test_image_url, test_asset_name
        )

        mock_requests_get.assert_called_once_with(test_image_url)
        mock_client.get_service.assert_called_once_with("AssetService")
        mock_client.get_type.assert_called_once_with("AssetOperation")

        self.assertEqual(mock_asset.type_, "MOCK_IMAGE_ASSET_TYPE")
        self.assertEqual(mock_asset.name, test_asset_name)
        self.assertEqual(mock_image_asset_data_obj.data, b"dummy_image_bytes")

        mock_asset_service.mutate_assets.assert_called_once_with(
            customer_id=test_customer_id, operations=[mock_asset_operation]
        )
        self.assertEqual(returned_resource_name, "mock_asset_resource_name_123")

        expected_stdout = f"Created image asset with resource name '{mock_asset_result.resource_name}'.\n"
        self.assertEqual(mock_stdout.getvalue(), expected_stdout)


class TestCreateCampaign(unittest.TestCase):
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_create_campaign_success(self, mock_stdout):
        mock_client = Mock(name="GoogleAdsClient")
        test_customer_id = "cust_camp_123"
        merchant_center_id = 12345
        campaign_budget_id = 67890
        mock_campaign_resource_name = "campaigns/camp_res_name_1"
        mock_budget_resource_path = f"customers/{test_customer_id}/campaignBudgets/{campaign_budget_id}"

        mock_campaign_service = Mock(name="CampaignService")
        mock_budget_service = Mock(name="CampaignBudgetService")

        def get_service_side_effect(service_name):
            if service_name == "CampaignService": return mock_campaign_service
            elif service_name == "CampaignBudgetService": return mock_budget_service
            return Mock()
        mock_client.get_service.side_effect = get_service_side_effect

        mock_budget_service.campaign_budget_path.return_value = mock_budget_resource_path

        mock_campaign_operation = Mock(name="CampaignOperation")
        mock_campaign = Mock(name="Campaign")
        mock_shopping_setting_obj = Mock(name="ShoppingSetting")
        mock_campaign.shopping_setting = mock_shopping_setting_obj
        mock_campaign.manual_cpc = Mock(name="ManualCpcOnCampaign")
        mock_campaign_operation.create = mock_campaign

        mock_manual_cpc_type_obj = Mock(name="ManualCpcType")

        type_map = { "CampaignOperation": mock_campaign_operation, "ManualCpc": mock_manual_cpc_type_obj }
        mock_client.get_type.side_effect = lambda type_name: type_map.get(type_name, Mock())

        mock_client.enums = SimpleNamespace(
            AdvertisingChannelTypeEnum=SimpleNamespace(DISPLAY="MOCK_DISPLAY_CHANNEL"),
            CampaignStatusEnum=SimpleNamespace(PAUSED="MOCK_CAMPAIGN_PAUSED")
        )
        mock_client.copy_from = Mock()

        mock_mutate_campaigns_response = Mock()
        mock_campaign_result = Mock(); mock_campaign_result.resource_name = mock_campaign_resource_name
        mock_mutate_campaigns_response.results = [mock_campaign_result]
        mock_campaign_service.mutate_campaigns.return_value = mock_mutate_campaigns_response

        returned_campaign_name = add_merchant_center_dynamic_remarketing_campaign.create_campaign(
            mock_client, test_customer_id, merchant_center_id, campaign_budget_id
        )

        mock_client.get_service.assert_any_call("CampaignService")
        mock_client.get_service.assert_any_call("CampaignBudgetService")
        mock_budget_service.campaign_budget_path.assert_called_once_with(test_customer_id, campaign_budget_id)
        mock_client.get_type.assert_any_call("CampaignOperation"); mock_client.get_type.assert_any_call("ManualCpc")
        self.assertTrue(mock_campaign.name.startswith("Shopping campaign #"))
        self.assertEqual(mock_shopping_setting_obj.campaign_priority, 0)
        self.assertEqual(mock_shopping_setting_obj.merchant_id, merchant_center_id)
        self.assertTrue(mock_shopping_setting_obj.enable_local)
        self.assertEqual(mock_campaign.advertising_channel_type, "MOCK_DISPLAY_CHANNEL")
        self.assertEqual(mock_campaign.status, "MOCK_CAMPAIGN_PAUSED")
        self.assertEqual(mock_campaign.campaign_budget, mock_budget_resource_path)
        mock_client.copy_from.assert_called_once_with(mock_campaign.manual_cpc, mock_manual_cpc_type_obj)
        mock_campaign_service.mutate_campaigns.assert_called_once_with(
            customer_id=test_customer_id, operations=[mock_campaign_operation]
        )
        self.assertEqual(returned_campaign_name, mock_campaign_resource_name)
        expected_stdout = f"Created campaign with resource name '{mock_campaign_resource_name}'.\n"
        self.assertEqual(mock_stdout.getvalue(), expected_stdout)


class TestCreateAdGroup(unittest.TestCase):
    def test_create_ad_group_success(self):
        mock_client = Mock(name="GoogleAdsClient")
        test_customer_id = "cust_adgroup_456"; test_campaign_rn = "campaigns/camp_rn_xyz"
        mock_ad_group_resource_name = "adGroups/adgroup_res_name_1"
        mock_ad_group_service = Mock(name="AdGroupService")
        mock_client.get_service.return_value = mock_ad_group_service
        mock_ad_group_operation = Mock(name="AdGroupOperation")
        mock_ad_group = Mock(name="AdGroup")
        mock_ad_group_operation.create = mock_ad_group
        mock_client.get_type.return_value = mock_ad_group_operation
        mock_client.enums = SimpleNamespace(AdGroupStatusEnum=SimpleNamespace(ENABLED="MOCK_ADGROUP_ENABLED"))
        mock_mutate_ad_groups_response = Mock()
        mock_ad_group_result = Mock(); mock_ad_group_result.resource_name = mock_ad_group_resource_name
        mock_mutate_ad_groups_response.results = [mock_ad_group_result]
        mock_ad_group_service.mutate_ad_groups.return_value = mock_mutate_ad_groups_response

        returned_ad_group_name = add_merchant_center_dynamic_remarketing_campaign.create_ad_group(
            mock_client, test_customer_id, test_campaign_rn
        )
        mock_client.get_service.assert_called_once_with("AdGroupService")
        mock_client.get_type.assert_called_once_with("AdGroupOperation")
        self.assertEqual(mock_ad_group.name, "Dynamic remarketing ad group")
        self.assertEqual(mock_ad_group.campaign, test_campaign_rn)
        self.assertEqual(mock_ad_group.status, "MOCK_ADGROUP_ENABLED")
        mock_ad_group_service.mutate_ad_groups.assert_called_once_with(
            customer_id=test_customer_id, operations=[mock_ad_group_operation]
        )
        self.assertEqual(returned_ad_group_name, mock_ad_group_resource_name)


class TestCreateAd(unittest.TestCase):
    @patch('examples.remarketing.add_merchant_center_dynamic_remarketing_campaign.upload_image_asset')
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_create_ad_success(self, mock_stdout, mock_upload_image_asset_func):
        mock_client = Mock(name="GoogleAdsClient")
        test_customer_id = "cust_ad_789"
        test_ad_group_rn = "adgroups/ad_group_rn_abc"
        mock_ad_resource_name = "ads/ad_res_name_1"

        mock_ad_group_ad_service = Mock(name="AdGroupAdService")
        mock_client.get_service.return_value = mock_ad_group_ad_service

        mock_upload_image_asset_func.side_effect = ["mock_marketing_image_rn", "mock_square_image_rn"]

        created_ad_image_assets = []
        created_ad_text_assets = []

        mock_ad_group_ad_operation = Mock(name="AdGroupAdOperation")
        mock_ad_group_ad = Mock(name="AdGroupAd")
        mock_ad_group_ad.ad.final_urls = []
        mock_responsive_display_ad_info = Mock(name="ResponsiveDisplayAdInfo")
        mock_responsive_display_ad_info.marketing_images = []
        mock_responsive_display_ad_info.square_marketing_images = []
        mock_responsive_display_ad_info.headlines = []
        mock_responsive_display_ad_info.descriptions = []
        # Initialize long_headline as a mock that can have .text set
        mock_responsive_display_ad_info.long_headline = Mock(name="LongHeadlineTextAsset")
        mock_ad_group_ad.ad.responsive_display_ad = mock_responsive_display_ad_info
        mock_ad_group_ad_operation.create = mock_ad_group_ad

        def get_type_side_effect_for_create_ad(type_name):
            if type_name == "AdGroupAdOperation":
                mock_ad_group_ad.ad.final_urls = []
                mock_responsive_display_ad_info.marketing_images = []
                mock_responsive_display_ad_info.square_marketing_images = []
                mock_responsive_display_ad_info.headlines = []
                mock_responsive_display_ad_info.descriptions = []
                mock_responsive_display_ad_info.long_headline = Mock(name="LongHeadlineTextAsset_Reset")
                mock_ad_group_ad.ad.responsive_display_ad = mock_responsive_display_ad_info
                mock_ad_group_ad_operation.create = mock_ad_group_ad
                return mock_ad_group_ad_operation
            elif type_name == "AdImageAsset":
                img_asset = Mock(name=f"AdImageAssetInstance_{len(created_ad_image_assets)}")
                created_ad_image_assets.append(img_asset)
                return img_asset
            elif type_name == "AdTextAsset":
                txt_asset = Mock(name=f"AdTextAssetInstance_{len(created_ad_text_assets)}")
                created_ad_text_assets.append(txt_asset)
                return txt_asset
            return Mock(name=f"DefaultMock_{type_name}")
        mock_client.get_type.side_effect = get_type_side_effect_for_create_ad

        mock_client.enums = SimpleNamespace(
            DisplayAdFormatSettingEnum=SimpleNamespace(NON_NATIVE="MOCK_NON_NATIVE_FORMAT")
        )

        mock_mutate_response = Mock()
        mock_ad_result = Mock(); mock_ad_result.resource_name = mock_ad_resource_name
        mock_mutate_response.results = [mock_ad_result]
        mock_ad_group_ad_service.mutate_ad_group_ads.return_value = mock_mutate_response

        add_merchant_center_dynamic_remarketing_campaign.create_ad(
            mock_client, test_customer_id, test_ad_group_rn
        )

        mock_upload_image_asset_func.assert_has_calls([
            call(mock_client, test_customer_id, "https://gaagl.page.link/Eit5", "Marketing Image"),
            call(mock_client, test_customer_id, "https://gaagl.page.link/bjYi", "Square Marketing Image")
        ])

        self.assertEqual(len(created_ad_image_assets), 2)
        self.assertEqual(created_ad_image_assets[0].asset, "mock_marketing_image_rn")
        self.assertEqual(created_ad_image_assets[1].asset, "mock_square_image_rn")

        self.assertEqual(len(created_ad_text_assets), 2)
        self.assertEqual(created_ad_text_assets[0].text, "Travel")
        self.assertEqual(created_ad_text_assets[1].text, "Take to the air!")

        self.assertEqual(mock_ad_group_ad.ad_group, test_ad_group_rn)
        self.assertEqual(mock_ad_group_ad.ad.final_urls[0], "http://www.example.com/")

        rda = mock_responsive_display_ad_info
        self.assertIn(created_ad_image_assets[0], rda.marketing_images)
        self.assertIn(created_ad_image_assets[1], rda.square_marketing_images)
        self.assertIn(created_ad_text_assets[0], rda.headlines)
        self.assertEqual(rda.long_headline.text, "Travel the World")
        self.assertIn(created_ad_text_assets[1], rda.descriptions)
        self.assertEqual(rda.business_name, "Interplanetary Cruises")
        self.assertEqual(rda.call_to_action_text, "Apply Now")
        self.assertEqual(rda.main_color, "#0000ff")
        self.assertEqual(rda.accent_color, "#ffff00")
        self.assertFalse(rda.allow_flexible_color)
        self.assertEqual(rda.format_setting, "MOCK_NON_NATIVE_FORMAT")

        mock_ad_group_ad_service.mutate_ad_group_ads.assert_called_once_with(
            customer_id=test_customer_id, operations=[mock_ad_group_ad_operation]
        )
        expected_stdout = f"Created ad group ad with resource name '{mock_ad_result.resource_name}'.\n"
        self.assertEqual(mock_stdout.getvalue(), expected_stdout)


class TestAttachUserList(unittest.TestCase):
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_attach_user_list_success(self, mock_stdout):
        mock_client = Mock(name="GoogleAdsClient")
        test_customer_id = "cust_attach_ul_123"
        test_ad_group_rn = "adgroups/adgroup_attach_rn"
        test_user_list_id = 987654
        mock_user_list_path = f"userLists/{test_user_list_id}"
        mock_criterion_resource_name = "adGroupCriteria/crit_res_name_1"

        mock_ad_group_criterion_service = Mock(name="AdGroupCriterionService")
        mock_user_list_service = Mock(name="UserListService")

        def get_service_side_effect(service_name):
            if service_name == "AdGroupCriterionService": return mock_ad_group_criterion_service
            if service_name == "UserListService": return mock_user_list_service
            return Mock()
        mock_client.get_service.side_effect = get_service_side_effect

        mock_user_list_service.user_list_path.return_value = mock_user_list_path

        mock_ad_group_criterion_operation = Mock(name="AdGroupCriterionOperation")
        mock_ad_group_criterion = Mock(name="AdGroupCriterion")
        mock_ad_group_criterion.user_list = Mock(name="UserListInfoOnCriterion")
        mock_ad_group_criterion_operation.create = mock_ad_group_criterion
        mock_client.get_type.return_value = mock_ad_group_criterion_operation

        mock_mutate_response = Mock()
        mock_criterion_result = Mock(); mock_criterion_result.resource_name = mock_criterion_resource_name
        mock_mutate_response.results = [mock_criterion_result]
        mock_ad_group_criterion_service.mutate_ad_group_criteria.return_value = mock_mutate_response

        add_merchant_center_dynamic_remarketing_campaign.attach_user_list(
            mock_client, test_customer_id, test_ad_group_rn, test_user_list_id
        )

        mock_client.get_service.assert_any_call("AdGroupCriterionService")
        mock_client.get_service.assert_any_call("UserListService")
        # Corrected: SUT passes user_list_id as int
        mock_user_list_service.user_list_path.assert_called_once_with(test_customer_id, test_user_list_id)
        mock_client.get_type.assert_called_once_with("AdGroupCriterionOperation")

        self.assertEqual(mock_ad_group_criterion.ad_group, test_ad_group_rn)
        self.assertEqual(mock_ad_group_criterion.user_list.user_list, mock_user_list_path)

        mock_ad_group_criterion_service.mutate_ad_group_criteria.assert_called_once_with(
            customer_id=test_customer_id, operations=[mock_ad_group_criterion_operation]
        )
        expected_stdout = f"Created ad group criterion with resource name '{mock_criterion_result.resource_name}'.\n"
        self.assertEqual(mock_stdout.getvalue(), expected_stdout)


class TestMainFunction(unittest.TestCase):
    @patch('examples.remarketing.add_merchant_center_dynamic_remarketing_campaign.attach_user_list')
    @patch('examples.remarketing.add_merchant_center_dynamic_remarketing_campaign.create_ad')
    @patch('examples.remarketing.add_merchant_center_dynamic_remarketing_campaign.create_ad_group')
    @patch('examples.remarketing.add_merchant_center_dynamic_remarketing_campaign.create_campaign')
    def test_main_orchestration(
        self,
        mock_create_campaign,
        mock_create_ad_group,
        mock_create_ad,
        mock_attach_user_list
    ):
        mock_client = Mock(name="GoogleAdsClient_for_main")
        test_customer_id = "main_cust_id"
        test_merchant_center_id = 123456
        test_campaign_budget_id = 789012
        test_user_list_id = "ul_id_main"

        mock_create_campaign.return_value = "campaigns/mock_campaign_resource_name"
        mock_create_ad_group.return_value = "adGroups/mock_ad_group_resource_name"

        add_merchant_center_dynamic_remarketing_campaign.main(
            mock_client,
            test_customer_id,
            test_merchant_center_id,
            test_campaign_budget_id,
            test_user_list_id
        )

        mock_create_campaign.assert_called_once_with(
            mock_client,
            test_customer_id,
            test_merchant_center_id,
            test_campaign_budget_id
        )
        mock_create_ad_group.assert_called_once_with(
            mock_client,
            test_customer_id,
            "campaigns/mock_campaign_resource_name"
        )
        mock_create_ad.assert_called_once_with( # create_ad does not use image asset resource name directly from main
            mock_client,
            test_customer_id,
            "adGroups/mock_ad_group_resource_name"
        )
        mock_attach_user_list.assert_called_once_with(
            mock_client,
            test_customer_id,
            "adGroups/mock_ad_group_resource_name", # ad_group_resource_name
            test_user_list_id
        )

if __name__ == "__main__":
    unittest.main()
