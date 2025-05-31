import unittest
from unittest import mock
import sys
import uuid # Script uses uuid

sys.path.insert(0, '/app') # For subtask environment

from examples.advanced_operations import add_demand_gen_campaign

# Temporary IDs from the script
_BUDGET_TEMPORARY_ID = "-1"
_CAMPAIGN_TEMPORARY_ID = "-2"
_AD_GROUP_TEMPORARY_ID = "-3"
_VIDEO_ASSET_TEMPORARY_ID = "-4"
_LOGO_ASSET_TEMPORARY_ID = "-5"

class TestAddDemandGenCampaign(unittest.TestCase):

    def _setup_common_mocks(self, mock_google_ads_client, customer_id):
        mock_google_ads_client.version = "v19"

        self.mock_google_ads_service = mock.Mock(name="GoogleAdsService")
        mock_mutate_response = mock.Mock(name="MutateResponse")
        mock_mutate_response.mutate_operation_responses = []
        self.mock_google_ads_service.mutate.return_value = mock_mutate_response

        # Mock GoogleAdsService.asset_path specifically for this test's needs
        self.expected_video_asset_rn_for_test = f"customers/{customer_id}/assets/{_VIDEO_ASSET_TEMPORARY_ID}"
        self.expected_logo_asset_rn_for_test = f"customers/{customer_id}/assets/{_LOGO_ASSET_TEMPORARY_ID}"

        def asset_path_side_effect(cust_id, temp_id_str_from_script):
            # Ensure comparison is with string versions of temp IDs
            if str(temp_id_str_from_script) == str(_VIDEO_ASSET_TEMPORARY_ID):
                return self.expected_video_asset_rn_for_test
            elif str(temp_id_str_from_script) == str(_LOGO_ASSET_TEMPORARY_ID):
                return self.expected_logo_asset_rn_for_test
            return f"customers/{cust_id}/assets/{temp_id_str_from_script}" # Fallback
        self.mock_google_ads_service.asset_path.side_effect = asset_path_side_effect

        mock_google_ads_client.get_service.return_value = self.mock_google_ads_service

        enums_to_mock = {
            "BudgetDeliveryMethodEnum": {"STANDARD": "BUDGET_STANDARD"},
            "CampaignStatusEnum": {"PAUSED": "CAMPAIGN_PAUSED"},
            "AdvertisingChannelTypeEnum": {"DEMAND_GEN": "DEMAND_GEN_CHANNEL"},
            "BiddingStrategyTypeEnum": {"TARGET_CPA": "TARGET_CPA_BIDDING"},
            "AdGroupStatusEnum": {"ENABLED": "ADGROUP_ENABLED"},
            "AssetTypeEnum": {"YOUTUBE_VIDEO": "ASSET_YOUTUBE_VIDEO", "IMAGE": "ASSET_IMAGE", "TEXT": "ASSET_TEXT"},
            "AdGroupAdStatusEnum": {"ENABLED": "ADGROUPAD_ENABLED"},
            "AdGroupTypeEnum": {"UNKNOWN": "ADGROUP_TYPE_UNKNOWN"},
        }
        for enum_name, members in enums_to_mock.items():
            enum_mock = mock.Mock(name=enum_name)
            for member_name, str_val in members.items():
                setattr(enum_mock, member_name, str_val)
            setattr(mock_google_ads_client.enums, enum_name, enum_mock)

        self.ad_text_asset_mocks_created_for_ad = []
        def get_type_side_effect(type_name, version=None):
            if type_name.endswith("Operation"):
                base_name = type_name.replace("Operation", "")
                op_mock = mock.Mock(name=type_name)
                create_mock = mock.Mock(name=f"{base_name}_Payload")
                op_mock.create = create_mock
                # self.mock_op_payloads_by_type is not used with HasField check, so removing for now

                if base_name == "Campaign":
                    create_mock.target_cpa = mock.Mock(name="TargetCpa_on_Campaign")
                elif base_name == "AdGroup":
                    create_mock.demand_gen_ad_group_settings = mock.Mock(name="DemandGenAdGroupSettings")
                    create_mock.demand_gen_ad_group_settings.channel_controls = mock.Mock(name="ChannelControls")
                    create_mock.demand_gen_ad_group_settings.channel_controls.selected_channels = mock.Mock(name="SelectedChannels")
                elif base_name == "AdGroupAd":
                    ad_mock = mock.Mock(name="Ad_on_AdGroupAd")
                    dgvra_mock = mock.Mock(name="DemandGenVideoResponsiveAdInfo")
                    dgvra_mock.videos = []
                    dgvra_mock.logos = []
                    dgvra_mock.headlines = []
                    dgvra_mock.long_headlines = []
                    dgvra_mock.descriptions = []
                    ad_mock.demand_gen_video_responsive_ad = dgvra_mock
                    create_mock.ad = ad_mock
                return op_mock
            elif type_name in ["AdTextAsset", "AdImageAsset", "AdVideoAsset"]:
                return mock.Mock(name=type_name)
            self.fail(f"Unexpected type requested by script: {type_name}")
        mock_google_ads_client.get_type.side_effect = get_type_side_effect

        return self.mock_google_ads_service

    @mock.patch("examples.advanced_operations.add_demand_gen_campaign.create_asset_operations")
    @mock.patch("examples.advanced_operations.add_demand_gen_campaign.uuid4") # Corrected patch target
    @mock.patch("examples.utils.example_helpers.get_image_bytes_from_url")
    @mock.patch("examples.advanced_operations.add_demand_gen_campaign.GoogleAdsClient.load_from_storage")
    def test_main_functional(self, mock_load_from_storage, mock_get_image_bytes, mock_script_uuid4, mock_create_asset_operations_helper): # Renamed arg
        mock_google_ads_client = mock.Mock()
        mock_load_from_storage.return_value = mock_google_ads_client

        mock_script_uuid4.side_effect = ["mock-budget-uuid", "mock-campaign-uuid", "mock-adgroup-uuid"] # Use correct mock arg

        customer_id = "custDemandGen123"
        video_id = "testVideoId123"
        # Call _setup_common_mocks and get the google_ads_service_mock instance
        google_ads_service_mock = self._setup_common_mocks(mock_google_ads_client, customer_id)

        mock_get_image_bytes.return_value = b"dummy_logo_image_data"

        # Configure the mocked create_asset_operations
        mock_video_asset_op_wrapper = mock.Mock(name="VideoAsset_MutateOpWrapper")
        mock_logo_asset_op_wrapper = mock.Mock(name="LogoAsset_MutateOpWrapper")
        mock_create_asset_operations_helper.return_value = [mock_video_asset_op_wrapper, mock_logo_asset_op_wrapper]

        # Call main
        add_demand_gen_campaign.main(mock_google_ads_client, customer_id, video_id)

        # --- Assertions ---
        google_ads_service_mock.mutate.assert_called_once() # Use the instance from _setup_common_mocks
        mutate_kwargs = google_ads_service_mock.mutate.call_args[1]
        self.assertEqual(mutate_kwargs['customer_id'], customer_id)
        all_mutate_ops = mutate_kwargs['mutate_operations']

        self.assertEqual(len(all_mutate_ops), 6) # 1B, 1C, 1AG, 2 Assets (mocked), 1AGA

        self.assertIn(mock_video_asset_op_wrapper, all_mutate_ops)
        self.assertIn(mock_logo_asset_op_wrapper, all_mutate_ops)

        remaining_ops = [op for op in all_mutate_ops if op not in [mock_video_asset_op_wrapper, mock_logo_asset_op_wrapper]]
        self.assertEqual(len(remaining_ops), 4)

        has_budget_op = any(op.HasField("campaign_budget_operation") for op in remaining_ops)
        has_campaign_op = any(op.HasField("campaign_operation") for op in remaining_ops)
        has_ad_group_op = any(op.HasField("ad_group_operation") for op in remaining_ops)
        has_ad_group_ad_op = any(op.HasField("ad_group_ad_operation") for op in remaining_ops)

        self.assertTrue(has_budget_op, "CampaignBudgetOperation missing")
        self.assertTrue(has_campaign_op, "CampaignOperation missing")
        self.assertTrue(has_ad_group_op, "AdGroupOperation missing")
        self.assertTrue(has_ad_group_ad_op, "AdGroupAdOperation missing")

        # Verify the call to the mocked helper
        mock_create_asset_operations_helper.assert_called_once_with(
            mock_google_ads_client,
            # These are the generated resource names the script passes
            self.expected_video_asset_rn_for_test,
            video_id,
            self.expected_logo_asset_rn_for_test
        )
        mock_get_image_bytes.assert_not_called()
        self.assertEqual(mock_script_uuid4.call_count, 3) # Use correct mock arg

if __name__ == '__main__':
    unittest.main()
