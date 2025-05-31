import unittest
from unittest import mock
import sys

sys.path.insert(0, '/app') # Adjusted path for subtask environment

from examples.advanced_operations import add_bidding_seasonality_adjustment

class TestAddBiddingSeasonalityAdjustment(unittest.TestCase):

    @mock.patch("examples.advanced_operations.add_bidding_seasonality_adjustment.GoogleAdsClient.load_from_storage")
    def test_main_functional(self, mock_load_from_storage):
        mock_google_ads_client = mock.Mock()
        mock_google_ads_client.version = "v19"

        mock_bsa_service = mock.Mock()

        def get_service_side_effect(service_name, version=None):
            self.assertEqual("v19", version if version else mock_google_ads_client.version)
            if service_name == "BiddingSeasonalityAdjustmentService":
                return mock_bsa_service
            self.fail(f"Unexpected service requested: {service_name}")
        mock_google_ads_client.get_service.side_effect = get_service_side_effect

        mock_bsa_operation_obj = mock.Mock()
        mock_bsa_create_obj = mock.Mock()
        mock_bsa_operation_obj.create = mock_bsa_create_obj

        def get_type_side_effect(type_name, version=None):
            if type_name == "BiddingSeasonalityAdjustmentOperation":
                return mock_bsa_operation_obj
            self.fail(f"Unexpected type requested: {type_name}")
        mock_google_ads_client.get_type.side_effect = get_type_side_effect

        # Mock enums
        mock_scope_enum = mock.Mock()
        mock_scope_enum.CHANNEL = "CHANNEL_SCOPE_ENUM" # Script uses CHANNEL scope
        mock_google_ads_client.enums.SeasonalityEventScopeEnum = mock_scope_enum

        mock_channel_type_enum = mock.Mock()
        mock_channel_type_enum.SEARCH = "SEARCH_CHANNEL_ENUM"
        mock_google_ads_client.enums.AdvertisingChannelTypeEnum = mock_channel_type_enum

        mock_mutate_response = mock.Mock()
        mock_mutate_response.results = [mock.Mock(resource_name="test_bsa_rn")]
        mock_bsa_service.mutate_bidding_seasonality_adjustments.return_value = mock_mutate_response

        customer_id = "12345"
        start_time = "2024-02-01 00:00:00"
        end_time = "2024-02-02 00:00:00"
        conversion_rate_modifier = 1.2
        # campaign_id is not a direct parameter to main, script uses CHANNEL scope

        appended_channel_types = []
        def append_channel_side_effect(item):
            appended_channel_types.append(item)
        mock_bsa_create_obj.advertising_channel_types = mock.Mock()
        mock_bsa_create_obj.advertising_channel_types.append.side_effect = append_channel_side_effect

        # GoogleAdsService is not used by the script's main logic as it's CHANNEL scope
        # So, no need to mock campaign_path or GoogleAdsService here in get_service

        add_bidding_seasonality_adjustment.main(
            mock_google_ads_client,
            customer_id,
            start_time,
            end_time,
            conversion_rate_modifier
        )

        mock_google_ads_client.get_service.assert_called_once_with("BiddingSeasonalityAdjustmentService")
        # mock_google_ads_client.get_service.assert_any_call("GoogleAdsService") # Not called
        mock_google_ads_client.get_type.assert_called_once_with("BiddingSeasonalityAdjustmentOperation")

        self.assertTrue(hasattr(mock_bsa_create_obj, 'name'))
        self.assertEqual(mock_bsa_create_obj.scope, "CHANNEL_SCOPE_ENUM") # Script uses CHANNEL
        self.assertEqual(mock_bsa_create_obj.conversion_rate_modifier, conversion_rate_modifier)

        # Script appends only SEARCH channel type
        mock_bsa_create_obj.advertising_channel_types.append.assert_called_once_with("SEARCH_CHANNEL_ENUM")
        self.assertIn("SEARCH_CHANNEL_ENUM", appended_channel_types)

        # campaign_ids assertions are removed as script uses CHANNEL scope
        # mock_google_ads_service.campaign_path.assert_called_once_with(customer_id, campaign_id)
        # mock_bsa_create_obj.campaign_ids.extend.assert_called_once_with([f"customers/{customer_id}/campaigns/{campaign_id}"])
        # self.assertIn(f"customers/{customer_id}/campaigns/{campaign_id}", extended_campaign_ids)

        self.assertEqual(mock_bsa_create_obj.start_date_time, start_time)
        self.assertEqual(mock_bsa_create_obj.end_date_time, end_time)

        mock_bsa_service.mutate_bidding_seasonality_adjustments.assert_called_once_with(
            customer_id=customer_id,
            operations=[mock_bsa_operation_obj]
        )

if __name__ == "__main__":
    unittest.main()
