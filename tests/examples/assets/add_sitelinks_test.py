import unittest
from unittest.mock import MagicMock, patch, call

from examples.assets import add_sitelinks


class TestAddSitelinks(unittest.TestCase):
    @patch("examples.assets.add_sitelinks.GoogleAdsClient")
    def test_create_sitelink_assets(self, mock_google_ads_client_constructor):
        mock_client_instance = mock_google_ads_client_constructor.return_value
        mock_asset_service = MagicMock()
        mock_client_instance.get_service.return_value = mock_asset_service

        mock_op1, mock_op2, mock_op3 = (
            MagicMock(name="Op1"),
            MagicMock(name="Op2"),
            MagicMock(name="Op3"),
        )
        mock_client_instance.get_type.side_effect = [
            mock_op1,
            mock_op2,
            mock_op3,
        ]

        mock_asset1 = mock_op1.create
        mock_asset1.final_urls = []
        mock_asset1.final_mobile_urls = []
        mock_asset1.sitelink_asset = MagicMock()

        mock_asset2 = mock_op2.create
        mock_asset2.final_urls = []
        mock_asset2.final_mobile_urls = []
        mock_asset2.sitelink_asset = MagicMock()

        mock_asset3 = mock_op3.create
        mock_asset3.final_urls = []
        mock_asset3.final_mobile_urls = []
        mock_asset3.sitelink_asset = MagicMock()

        customer_id = "test_customer_sitelink"

        mock_results = [
            MagicMock(resource_name="rn_sitelink1"),
            MagicMock(resource_name="rn_sitelink2"),
            MagicMock(resource_name="rn_sitelink3"),
        ]
        mock_asset_service.mutate_assets.return_value.results = mock_results

        # Note: The actual function create_sitelink_assets in add_sitelinks.py
        # is defined as def create_sitelink_assets(client, customer_id):
        # It does not take campaign_id. If campaign_id were passed here by a caller,
        # it would be an extra argument. The test reflects its definition.
        returned_resource_names = add_sitelinks.create_sitelink_assets(
            mock_client_instance, customer_id
        )

        self.assertEqual(mock_client_instance.get_type.call_count, 3)
        mock_client_instance.get_type.assert_called_with("AssetOperation")

        self.assertIn(
            "http://example.com/contact/store-finder", mock_asset1.final_urls
        )
        self.assertIn(
            "http://example.com/mobile/contact/store-finder",
            mock_asset1.final_mobile_urls,
        )
        self.assertEqual(
            mock_asset1.sitelink_asset.description1, "Get in touch"
        )
        self.assertEqual(
            mock_asset1.sitelink_asset.description2, "Find your local store"
        )
        self.assertEqual(mock_asset1.sitelink_asset.link_text, "Store locator")

        self.assertIn("http://example.com/store", mock_asset2.final_urls)
        self.assertIn(
            "http://example.com/mobile/store", mock_asset2.final_mobile_urls
        )
        self.assertEqual(
            mock_asset2.sitelink_asset.description1, "Buy some stuff"
        )
        self.assertEqual(
            mock_asset2.sitelink_asset.description2, "It's really good"
        )
        self.assertEqual(mock_asset2.sitelink_asset.link_text, "Store")

        self.assertIn("http://example.com/store/more", mock_asset3.final_urls)
        self.assertIn(
            "http://example.com/mobile/store/more",
            mock_asset3.final_mobile_urls,
        )
        self.assertEqual(
            mock_asset3.sitelink_asset.description1, "Buy some stuff"
        )
        self.assertEqual(
            mock_asset3.sitelink_asset.description2, "It's really good"
        )
        self.assertEqual(mock_asset3.sitelink_asset.link_text, "Store")

        mock_asset_service.mutate_assets.assert_called_once_with(
            customer_id=customer_id, operations=[mock_op1, mock_op2, mock_op3]
        )
        self.assertEqual(
            returned_resource_names, [res.resource_name for res in mock_results]
        )

    @patch("examples.assets.add_sitelinks.GoogleAdsClient")
    def test_link_sitelinks_to_campaign(
        self, mock_google_ads_client_constructor
    ):
        mock_client_instance = mock_google_ads_client_constructor.return_value
        mock_campaign_service = MagicMock()
        mock_campaign_asset_service = MagicMock()

        def get_service_side_effect(service_name):
            if service_name == "CampaignService":
                return mock_campaign_service
            elif service_name == "CampaignAssetService":
                return mock_campaign_asset_service
            return MagicMock()

        mock_client_instance.get_service.side_effect = get_service_side_effect

        num_resource_names = 3
        mock_operations = [
            MagicMock(name=f"CampOp{i}") for i in range(num_resource_names)
        ]
        mock_client_instance.get_type.side_effect = mock_operations

        mock_client_instance.enums.AssetFieldTypeEnum.SITELINK = "SITELINK_ENUM"

        customer_id = "test_customer_sitelink"
        campaign_id = "campaign_abc"
        resource_names = ["rn_sitelink1", "rn_sitelink2", "rn_sitelink3"]
        expected_campaign_path = (
            f"customers/{customer_id}/campaigns/{campaign_id}"
        )
        mock_campaign_service.campaign_path.return_value = (
            expected_campaign_path
        )

        mock_results = [
            MagicMock(resource_name=f"ca_sl_rn_{i}")
            for i in range(num_resource_names)
        ]
        mock_campaign_asset_service.mutate_campaign_assets.return_value.results = (
            mock_results
        )

        add_sitelinks.link_sitelinks_to_campaign(
            mock_client_instance, customer_id, campaign_id, resource_names
        )

        self.assertEqual(
            mock_client_instance.get_type.call_count, num_resource_names
        )
        mock_client_instance.get_type.assert_called_with(
            "CampaignAssetOperation"
        )

        for i, rn in enumerate(resource_names):
            campaign_asset_mock = mock_operations[i].create
            self.assertEqual(campaign_asset_mock.asset, rn)
            self.assertEqual(
                campaign_asset_mock.campaign, expected_campaign_path
            )
            self.assertEqual(campaign_asset_mock.field_type, "SITELINK_ENUM")

        mock_campaign_service.campaign_path.assert_has_calls(
            [call(customer_id, campaign_id)] * num_resource_names
        )
        self.assertEqual(
            mock_campaign_service.campaign_path.call_count, num_resource_names
        )

        mock_campaign_asset_service.mutate_campaign_assets.assert_called_once_with(
            customer_id=customer_id, operations=mock_operations
        )

    @patch("examples.assets.add_sitelinks.link_sitelinks_to_campaign")
    @patch("examples.assets.add_sitelinks.create_sitelink_assets")
    def test_main_function_logic(self, mock_create_assets, mock_link_sitelinks):
        mock_client = MagicMock()
        customer_id = "cust_main_sl"
        campaign_id = "camp_main_sl"  # This is the campaign_id passed by main

        mock_asset_resource_names = ["sl_asset1", "sl_asset2"]
        mock_create_assets.return_value = mock_asset_resource_names

        add_sitelinks.main(mock_client, customer_id, campaign_id)

        # The main function in add_sitelinks.py calls:
        # create_sitelink_assets(client, customer_id, campaign_id)
        # So the mock should be asserted with these three arguments.
        mock_create_assets.assert_called_once_with(mock_client, customer_id)

        mock_link_sitelinks.assert_called_once_with(
            mock_client, customer_id, campaign_id, mock_asset_resource_names
        )
