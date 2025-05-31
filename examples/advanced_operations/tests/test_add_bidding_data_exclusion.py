import unittest
from unittest import mock
import sys

sys.path.insert(0, '/app') # Adjusted path for subtask environment

from examples.advanced_operations import add_bidding_data_exclusion

class TestAddBiddingDataExclusion(unittest.TestCase):

    @mock.patch("examples.advanced_operations.add_bidding_data_exclusion.GoogleAdsClient.load_from_storage")
    def test_main_functional(self, mock_load_from_storage): # Added mock_load_from_storage
        mock_google_ads_client = mock.Mock()
        mock_google_ads_client.version = "v19"

        mock_bde_service = mock.Mock()

        def get_service_side_effect(service_name, version=None):
            self.assertEqual("v19", version if version else mock_google_ads_client.version)
            if service_name == "BiddingDataExclusionService":
                return mock_bde_service
            self.fail(f"Unexpected service requested: {service_name}")
        mock_google_ads_client.get_service.side_effect = get_service_side_effect

        mock_bde_operation_obj = mock.Mock() # This is the operation object itself
        mock_bde_create_obj = mock.Mock() # This is the object assigned to operation.create
        mock_bde_operation_obj.create = mock_bde_create_obj

        def get_type_side_effect(type_name, version=None):
            # self.assertEqual("v19", version if version else mock_google_ads_client.version) # Version not passed to get_type
            if type_name == "BiddingDataExclusionOperation":
                return mock_bde_operation_obj
            self.fail(f"Unexpected type requested: {type_name}")
        mock_google_ads_client.get_type.side_effect = get_type_side_effect

        mock_scope_enum = mock.Mock()
        mock_scope_enum.CHANNEL = "CHANNEL_SCOPE_ENUM"
        mock_google_ads_client.enums.SeasonalityEventScopeEnum = mock_scope_enum

        mock_channel_type_enum = mock.Mock()
        mock_channel_type_enum.SEARCH = "SEARCH_CHANNEL_ENUM" # Corrected Enum name
        mock_google_ads_client.enums.AdvertisingChannelTypeEnum = mock_channel_type_enum

        mock_mutate_response = mock.Mock()
        mock_mutate_response.results = [mock.Mock(resource_name="test_bde_rn")]
        mock_bde_service.mutate_bidding_data_exclusions.return_value = mock_mutate_response

        customer_id = "123"
        start_time = "2024-01-01 00:00:00"
        end_time = "2024-01-02 00:00:00"

        # Path for advertising_channel_types needs to be iterable and mockable for append
        # In the actual script, it's `data_exclusion.advertising_channel_types.extend([...])` or similar
        # For the mock, we directly assign a list if needed, or mock the extend/append method.
        # The example script uses: data_exclusion.advertising_channel_types.append("SEARCH")
        # So we need to mock append on the list attribute.
        appended_channel_types = []
        def append_side_effect(item):
            appended_channel_types.append(item)
        mock_bde_create_obj.advertising_channel_types = mock.Mock() # This needs to be a list-like mock
        mock_bde_create_obj.advertising_channel_types.append.side_effect = append_side_effect


        add_bidding_data_exclusion.main(mock_google_ads_client, customer_id, start_time, end_time)

        mock_google_ads_client.get_service.assert_called_once_with("BiddingDataExclusionService")
        mock_google_ads_client.get_type.assert_called_once_with("BiddingDataExclusionOperation")

        # Assert attributes set on the 'create' object (mock_bde_create_obj)
        self.assertTrue(hasattr(mock_bde_create_obj, 'name')) # name is assigned by the script
        self.assertEqual(mock_bde_create_obj.scope, "CHANNEL_SCOPE_ENUM")

        # Check that append was called on the advertising_channel_types attribute
        mock_bde_create_obj.advertising_channel_types.append.assert_called_with("SEARCH_CHANNEL_ENUM")
        self.assertIn("SEARCH_CHANNEL_ENUM", appended_channel_types) # Verify our side effect list

        self.assertEqual(mock_bde_create_obj.start_date_time, start_time)
        self.assertEqual(mock_bde_create_obj.end_date_time, end_time)

        mock_bde_service.mutate_bidding_data_exclusions.assert_called_once_with(
            customer_id=customer_id, # Corrected: customer_id, not request
            operations=[mock_bde_operation_obj]
        )

if __name__ == "__main__":
    unittest.main()
