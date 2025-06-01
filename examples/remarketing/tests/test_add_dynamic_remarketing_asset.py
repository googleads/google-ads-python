import unittest
from unittest.mock import patch, Mock, call, ANY
import io
import sys
from types import SimpleNamespace
import datetime # Real datetime module for creating fixed datetime objects

# SUT (System Under Test)
from examples.remarketing import add_dynamic_remarketing_asset

class TestCreateAsset(unittest.TestCase):
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_create_asset_success(self, mock_stdout):
        mock_client = Mock(name="GoogleAdsClient")
        mock_asset_service = Mock(name="AssetService")
        mock_client.get_service.return_value = mock_asset_service

        mock_asset_operation = Mock(name="AssetOperation")
        mock_asset_to_create = Mock(name="Asset")
        mock_dynamic_education_asset = Mock(name="DynamicEducationAsset")

        mock_asset_to_create.final_urls = []
        mock_asset_to_create.dynamic_education_asset = mock_dynamic_education_asset
        mock_asset_operation.create = mock_asset_to_create

        mock_client.get_type.return_value = mock_asset_operation

        mock_mutate_response = Mock()
        mock_result = Mock(); mock_result.resource_name = "mock_asset_resource_name"
        mock_mutate_response.results = [mock_result]
        mock_asset_service.mutate_assets.return_value = mock_mutate_response

        test_customer_id = "dummy_customer_id"

        returned_resource_name = add_dynamic_remarketing_asset.create_asset(
            mock_client, test_customer_id
        )

        mock_client.get_service.assert_called_once_with("AssetService")
        mock_client.get_type.assert_called_once_with("AssetOperation")

        self.assertEqual(len(mock_asset_to_create.final_urls), 1)
        self.assertEqual(mock_asset_to_create.final_urls[0], "https://www.example.com")

        dea = mock_dynamic_education_asset
        self.assertEqual(dea.school_name, "The University of Unknown")
        self.assertEqual(dea.address, "Building 1, New York, 12345, USA")
        self.assertEqual(dea.program_name, "BSc. Computer Science")
        self.assertEqual(dea.subject, "Computer Science")
        self.assertEqual(dea.program_description, "Slinging code for fun and profit!")
        self.assertEqual(dea.program_id, "bsc-cs-uofu")
        self.assertEqual(dea.location_id, "nyc")
        self.assertEqual(dea.image_url, "https://gaagl.page.link/Eit5")
        self.assertEqual(dea.android_app_link, "android-app://com.example.android/http/example.com/gizmos?1234")
        self.assertEqual(dea.ios_app_link, "exampleApp://content/page")
        self.assertEqual(dea.ios_app_store_id, 123)

        mock_asset_service.mutate_assets.assert_called_once_with(
            customer_id=test_customer_id, operations=[mock_asset_operation]
        )
        self.assertEqual(returned_resource_name, "mock_asset_resource_name")

        # Removed period before \n
        expected_stdout = f"Created a dynamic education asset with resource name 'mock_asset_resource_name'\n"
        self.assertEqual(mock_stdout.getvalue(), expected_stdout)


class TestCreateAssetSet(unittest.TestCase):
    @patch('examples.remarketing.add_dynamic_remarketing_asset.datetime')
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_create_asset_set_success(self, mock_stdout, mock_datetime_module_in_sut):
        mock_client = Mock(name="GoogleAdsClient")
        mock_asset_set_service = Mock(name="AssetSetService")
        mock_client.get_service.return_value = mock_asset_set_service

        mock_asset_set_operation = Mock(name="AssetSetOperation")
        mock_asset_set_to_create = Mock(name="AssetSet")
        mock_asset_set_operation.create = mock_asset_set_to_create
        mock_client.get_type.return_value = mock_asset_set_operation

        mock_client.enums = SimpleNamespace(
            AssetSetTypeEnum=SimpleNamespace(DYNAMIC_EDUCATION="mock_dynamic_education_enum")
        )

        fixed_now_datetime = datetime.datetime(2023, 10, 26, 12, 0, 0)
        mock_datetime_module_in_sut.now.return_value = fixed_now_datetime

        mock_mutate_response = Mock()
        mock_result = Mock(); mock_result.resource_name = "mock_asset_set_resource_name"
        mock_mutate_response.results = [mock_result]
        mock_asset_set_service.mutate_asset_sets.return_value = mock_mutate_response

        test_customer_id = "dummy_customer_id"

        returned_resource_name = add_dynamic_remarketing_asset.create_asset_set(
            mock_client, test_customer_id
        )

        mock_client.get_service.assert_called_once_with("AssetSetService")
        mock_client.get_type.assert_called_once_with("AssetSetOperation")
        mock_datetime_module_in_sut.now.assert_called_once()

        expected_name = f"My dynamic remarketing assets {str(fixed_now_datetime)}"
        self.assertEqual(mock_asset_set_to_create.name, expected_name)
        self.assertEqual(mock_asset_set_to_create.type_, "mock_dynamic_education_enum")

        mock_asset_set_service.mutate_asset_sets.assert_called_once_with(
            customer_id=test_customer_id, operations=[mock_asset_set_operation]
        )
        self.assertEqual(returned_resource_name, "mock_asset_set_resource_name")
        # Removed period before \n
        expected_stdout = f"Created asset set with resource name 'mock_asset_set_resource_name'\n"
        self.assertEqual(mock_stdout.getvalue(), expected_stdout)


class TestAddAssetsToAssetSet(unittest.TestCase):
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_add_assets_to_asset_set_success(self, mock_stdout):
        mock_client = Mock(name="GoogleAdsClient")
        mock_asset_set_asset_service = Mock(name="AssetSetAssetService")
        mock_client.get_service.return_value = mock_asset_set_asset_service

        mock_asa_operation = Mock(name="AssetSetAssetOperation")
        mock_asa_to_create = Mock(name="AssetSetAsset")
        mock_asa_operation.create = mock_asa_to_create
        mock_client.get_type.return_value = mock_asa_operation

        mock_mutate_response = Mock()
        mock_result = Mock(); mock_result.resource_name = "mock_asa_resource_name"
        mock_mutate_response.results = [mock_result]
        mock_asset_set_asset_service.mutate_asset_set_assets.return_value = mock_mutate_response

        test_customer_id = "dummy_customer_id"
        test_asset_rn = "assets/asset123"
        test_asset_set_rn = "assetSets/assetSet456"

        add_dynamic_remarketing_asset.add_assets_to_asset_set(
            mock_client, test_asset_rn, test_asset_set_rn, test_customer_id
        )

        mock_client.get_service.assert_called_once_with("AssetSetAssetService")
        mock_client.get_type.assert_called_once_with("AssetSetAssetOperation")

        self.assertEqual(mock_asa_to_create.asset, test_asset_rn)
        self.assertEqual(mock_asa_to_create.asset_set, test_asset_set_rn)

        mock_asset_set_asset_service.mutate_asset_set_assets.assert_called_once_with(
            customer_id=test_customer_id, operations=[mock_asa_operation]
        )
        # Removed period before \n
        expected_stdout = (
            f"Created asset set asset link with resource name 'mock_asa_resource_name'\n"
        )
        self.assertEqual(mock_stdout.getvalue(), expected_stdout)


class TestLinkAssetSetToCampaign(unittest.TestCase):
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_link_asset_set_to_campaign_success(self, mock_stdout):
        mock_client = Mock(name="GoogleAdsClient")
        mock_google_ads_service = Mock(name="GoogleAdsService")
        mock_campaign_asset_set_service = Mock(name="CampaignAssetSetService")

        def get_service_side_effect(service_name):
            if service_name == "GoogleAdsService":
                return mock_google_ads_service
            elif service_name == "CampaignAssetSetService":
                return mock_campaign_asset_set_service
            return Mock()
        mock_client.get_service.side_effect = get_service_side_effect

        mock_cas_operation = Mock(name="CampaignAssetSetOperation")
        mock_cas_to_create = Mock(name="CampaignAssetSet")
        mock_cas_operation.create = mock_cas_to_create
        mock_client.get_type.return_value = mock_cas_operation

        mock_campaign_path = "campaigns/campaign_path_123"
        mock_google_ads_service.campaign_path.return_value = mock_campaign_path

        mock_mutate_response = Mock()
        mock_result = Mock(); mock_result.resource_name = "mock_cas_resource_name"
        mock_mutate_response.results = [mock_result]
        mock_campaign_asset_set_service.mutate_campaign_asset_sets.return_value = mock_mutate_response

        test_customer_id = "dummy_customer_id"
        test_asset_set_rn = "assetSets/assetSet789"
        test_campaign_id = "campaign_id_456"

        add_dynamic_remarketing_asset.link_asset_set_to_campaign(
            mock_client, test_asset_set_rn, test_customer_id, test_campaign_id
        )

        mock_client.get_service.assert_any_call("GoogleAdsService")
        mock_client.get_service.assert_any_call("CampaignAssetSetService")
        mock_client.get_type.assert_called_once_with("CampaignAssetSetOperation")
        mock_google_ads_service.campaign_path.assert_called_once_with(test_customer_id, test_campaign_id)

        self.assertEqual(mock_cas_to_create.campaign, mock_campaign_path)
        self.assertEqual(mock_cas_to_create.asset_set, test_asset_set_rn)

        mock_campaign_asset_set_service.mutate_campaign_asset_sets.assert_called_once_with(
            customer_id=test_customer_id, operations=[mock_cas_operation]
        )
        # Removed period before \n
        expected_stdout = (
            f"Created a campaign asset set with resource name 'mock_cas_resource_name'\n"
        )
        self.assertEqual(mock_stdout.getvalue(), expected_stdout)


class TestMainFunction(unittest.TestCase):
    @patch('examples.remarketing.add_dynamic_remarketing_asset.link_asset_set_to_campaign')
    @patch('examples.remarketing.add_dynamic_remarketing_asset.add_assets_to_asset_set')
    @patch('examples.remarketing.add_dynamic_remarketing_asset.create_asset_set')
    @patch('examples.remarketing.add_dynamic_remarketing_asset.create_asset')
    def test_main_orchestration(
        self,
        mock_create_asset,
        mock_create_asset_set,
        mock_add_assets,
        mock_link_campaign
    ):
        mock_client = Mock(name="GoogleAdsClient_for_main")
        test_customer_id = "main_cust_id"
        test_campaign_id = "main_camp_id"

        mock_create_asset.return_value = "mocked_asset_resource_name"
        mock_create_asset_set.return_value = "mocked_asset_set_resource_name"

        add_dynamic_remarketing_asset.main(mock_client, test_customer_id, test_campaign_id)

        mock_create_asset.assert_called_once_with(mock_client, test_customer_id)
        mock_create_asset_set.assert_called_once_with(mock_client, test_customer_id)
        mock_add_assets.assert_called_once_with(
            mock_client,
            "mocked_asset_resource_name",
            "mocked_asset_set_resource_name",
            test_customer_id
        )
        mock_link_campaign.assert_called_once_with(
            mock_client,
            "mocked_asset_set_resource_name",
            test_customer_id,
            test_campaign_id
        )


if __name__ == "__main__":
    unittest.main()
